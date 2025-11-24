import markdown
import bleach


class MarkdownRenderer:
    allowed_tags = [
        'a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'p', 'pre',
        'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'hr'
    ]
    allowed_attributes = {
        '*': ['class'],
        'a': ['href', 'title', 'name', 'target', 'rel'],
        'img': ['src', 'alt', 'title'],
    }
    allowed_protocols = ['http', 'https', 'mailto']
    markdown_extensions = ['fenced_code', 'codehilite', 'tables', 'sane_lists']

    @classmethod
    def render(cls, raw_text: str) -> str:
        html = markdown.markdown(raw_text or '', extensions=cls.markdown_extensions)
        return bleach.clean(
            html,
            tags=cls.allowed_tags,
            attributes=cls.allowed_attributes,
            protocols=cls.allowed_protocols,
            strip=True,
        )
