from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'press', 'image', 'content']
        labels = {
            'title': '제목',
            'press': '언론사',
            'image': '대표 이미지',
            'content': '본문 (Markdown)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요'}),
            'press': forms.Select(),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'content': forms.Textarea(attrs={'rows': 12, 'data-markdown-source': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-input').strip()

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content.strip():
            raise forms.ValidationError('본문을 입력해주세요.')
        return content
