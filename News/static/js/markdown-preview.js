document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.querySelector('[data-markdown-source]');
    const preview = document.querySelector('[data-markdown-preview]');
    
    if (!textarea || !preview) {
        console.warn('Markdown preview: textarea 또는 preview 요소를 찾을 수 없습니다.');
        return;
    }

    const form = textarea.closest('form');
    const getCookie = (name) => {
        const cookieValue = document.cookie
            ?.split(';')
            .map((c) => c.trim())
            .find((c) => c.startsWith(`${name}=`));
        return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
    };

    const previewUrl = form?.dataset.previewUrl || textarea.dataset.previewUrl;
    const csrfToken =
        form?.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');
    
    console.log('Markdown preview 초기화:', {
        previewUrl,
        hasToken: !!csrfToken,
        textareaFound: !!textarea,
        previewFound: !!preview
    });

    let debounce;

    const renderFallback = () => {
        if (textarea.value.trim()) {
            preview.textContent = textarea.value;
        } else {
            preview.innerHTML = '미리보기 영역입니다. 내용을 입력하면 렌더링됩니다.';
        }
    };

    const updatePreview = () => {
        if (!previewUrl || !csrfToken) {
            console.warn('Markdown preview: URL 또는 CSRF 토큰이 없습니다.', {
                previewUrl,
                hasToken: !!csrfToken
            });
            renderFallback();
            return;
        }

        clearTimeout(debounce);
        debounce = setTimeout(async () => {
            try {
                const formData = new FormData();
                formData.append('content', textarea.value);
                const response = await fetch(previewUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    credentials: 'same-origin',
                    body: formData,
                });
                
                if (!response.ok) {
                    console.error('Markdown preview API 오류:', response.status, response.statusText);
                    throw new Error(`Preview request failed: ${response.status}`);
                }
                
                const data = await response.json();
                console.log('Markdown preview 렌더링 성공');
                preview.innerHTML = data.html || '';
                
                if (!data.html) {
                    renderFallback();
                }
            } catch (error) {
                console.error('Markdown preview 오류:', error);
                renderFallback();
            }
        }, 200);
    };

    textarea.addEventListener('input', updatePreview);
    renderFallback();
    updatePreview();
});
