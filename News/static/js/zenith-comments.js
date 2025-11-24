const ZENITH_EMBED_URL = 'http://localhost:3000';
const ZENITH_SITE_ID = 'zenith-news';

class ZenithCommentsEmbed {
    constructor(container, threadId, isAuthenticated) {
        this.container = container;
        this.threadId = threadId;
        this.isAuthenticated = isAuthenticated;
        this.iframe = null;

        this.init();
    }

    async init() {
        this.container.innerHTML = '<div class="zenith-loading">댓글을 불러오는 중...</div>';

        try {
            let sessionData = null;

            if (this.isAuthenticated) {
                console.log('[Zenith] Creating session...');
                sessionData = await this.createSession();
                console.log('[Zenith] Session created:', sessionData);
            }

            console.log('[Zenith] Creating iframe...');
            this.createIframe(sessionData);
        } catch (error) {
            console.error('[Zenith] Init failed:', error);
            this.showError('댓글을 불러오는데 실패했습니다: ' + error.message);
        }
    }

    async createSession() {
        const userResponse = await fetch('/main/api/comment-user/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({}),
        });

        if (!userResponse.ok) {
            throw new Error('Failed to create comment user');
        }

        const userData = await userResponse.json();

        const sessionResponse = await fetch('/main/api/comment-session/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId: userData.id }),
        });

        if (!sessionResponse.ok) {
            throw new Error('Failed to create comment session');
        }

        const sessionData = await sessionResponse.json();

        return {
            sessionId: sessionData.sessionId,
            userId: userData.id,
            displayName: userData.displayName || userData.username,
            avatar: userData.profilePictureUrl || '',
        };
    }

    createIframe(sessionData) {
        this.iframe = document.createElement('iframe');

        const params = new URLSearchParams();
        params.set('thread_id', this.threadId);

        if (sessionData) {
            params.set('session_id', sessionData.sessionId);
            params.set('user_id', sessionData.userId);
            params.set('display_name', sessionData.displayName);
            if (sessionData.avatar) {
                params.set('avatar', sessionData.avatar);
            }
        } else {
            params.set('site_id', ZENITH_SITE_ID);
        }

        this.iframe.src = `${ZENITH_EMBED_URL}/embed?${params.toString()}`;
        this.iframe.style.cssText = 'width: 100%; border: none; min-height: 400px;';
        this.iframe.setAttribute('title', 'Zenith Comments');

        this.container.innerHTML = '';
        this.container.appendChild(this.iframe);

        window.addEventListener('message', (event) => this.handleMessage(event));
    }

    handleMessage(event) {
        const { type, height } = event.data || {};

        if (type === 'ZENITH_RESIZE' && height) {
            if (this.iframe) {
                this.iframe.style.height = `${height}px`;
            }
        }
    }

    showError(message) {
        this.container.innerHTML = `<div class="zenith-error">${message}</div>`;
    }
}

window.ZenithCommentsEmbed = ZenithCommentsEmbed;
