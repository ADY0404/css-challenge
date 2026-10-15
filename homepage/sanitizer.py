"""
HTML Sanitizer for User and Administrator Content.
Protects against XSS, unsafe script injection, malicious iframes, and dangerous URLs
while allowing safe rich-text formatting (paragraphs, lists, headings, tables, links, images).
"""

import re
from html.parser import HTMLParser
from html import escape
from django.utils.safestring import mark_safe


ALLOWED_TAGS = {
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'strike',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li',
    'blockquote', 'code', 'pre',
    'a', 'img', 'hr',
    'div', 'span',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
}

DANGEROUS_TAGS = {
    'script', 'style', 'iframe', 'frame', 'object', 'embed',
    'applet', 'meta', 'link', 'svg', 'math', 'form', 'input',
    'button', 'textarea', 'select', 'base', 'noscript'
}

ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title', 'target', 'rel', 'class', 'id'},
    'img': {'src', 'alt', 'title', 'class', 'id', 'width', 'height', 'style'},
    'div': {'class', 'id', 'style'},
    'span': {'class', 'id', 'style'},
    'p': {'class', 'id', 'style'},
    'h1': {'class', 'id'},
    'h2': {'class', 'id'},
    'h3': {'class', 'id'},
    'h4': {'class', 'id'},
    'h5': {'class', 'id'},
    'h6': {'class', 'id'},
    'ul': {'class', 'id'},
    'ol': {'class', 'id'},
    'li': {'class', 'id'},
    'table': {'class', 'id'},
    'blockquote': {'class', 'id'},
    'code': {'class', 'id'},
    'pre': {'class', 'id'},
}

ALLOWED_SCHEMES = ('http://', 'https://', 'mailto:', 'tel:', '/', '#')


def is_safe_url(url):
    """Verify that a URL does not use dangerous protocols like javascript: or data:."""
    if not url:
        return False
    url_stripped = url.strip().lower()
    # Check for javascript:, data:, vbscript: even if encoded
    if any(url_stripped.startswith(prefix) for prefix in ('javascript:', 'data:', 'vbscript:')):
        return False
    return any(url_stripped.startswith(scheme) for scheme in ALLOWED_SCHEMES) or url_stripped.startswith(('?', '.'))


class SafeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower in DANGEROUS_TAGS:
            self.ignore_depth += 1
            return

        if self.ignore_depth > 0:
            return

        if tag_lower in ALLOWED_TAGS:
            cleaned_attrs = []
            allowed_for_tag = ALLOWED_ATTRIBUTES.get(tag_lower, {'class', 'id'})
            
            has_target_blank = False
            for attr_name, attr_val in attrs:
                attr_name_lower = attr_name.lower()
                
                # Strip all event handlers
                if attr_name_lower.startswith('on'):
                    continue
                
                if attr_name_lower in allowed_for_tag and attr_val is not None:
                    # Sanitize URL attributes
                    if attr_name_lower in ('href', 'src'):
                        if not is_safe_url(attr_val):
                            continue
                    
                    # Sanitize CSS style attribute
                    if attr_name_lower == 'style':
                        val_lower = attr_val.lower()
                        if any(bad in val_lower for bad in ('expression', 'javascript', 'url(', '@import', 'behavior')):
                            continue

                    if attr_name_lower == 'target' and attr_val.lower() == '_blank':
                        has_target_blank = True

                    escaped_val = escape(attr_val, quote=True)
                    cleaned_attrs.append(f'{attr_name_lower}="{escaped_val}"')

            if tag_lower == 'a' and has_target_blank:
                # Enforce rel="noopener noreferrer" for security on external links
                if not any('rel=' in attr for attr in cleaned_attrs):
                    cleaned_attrs.append('rel="noopener noreferrer"')

            attrs_str = (' ' + ' '.join(cleaned_attrs)) if cleaned_attrs else ''
            if tag_lower in ('br', 'hr', 'img'):
                self.output.append(f'<{tag_lower}{attrs_str} />')
            else:
                self.output.append(f'<{tag_lower}{attrs_str}>')

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in DANGEROUS_TAGS:
            if self.ignore_depth > 0:
                self.ignore_depth -= 1
            return

        if self.ignore_depth > 0:
            return

        if tag_lower in ALLOWED_TAGS and tag_lower not in ('br', 'hr', 'img'):
            self.output.append(f'</{tag_lower}>')

    def handle_data(self, data):
        if self.ignore_depth == 0:
            self.output.append(escape(data))

    def handle_entityref(self, name):
        if self.ignore_depth == 0:
            self.output.append(f'&{name};')

    def handle_charref(self, name):
        if self.ignore_depth == 0:
            self.output.append(f'&#{name};')

    def get_html(self):
        return ''.join(self.output)


def sanitize_html(content):
    """
    Sanitize raw HTML string, stripping dangerous tags, event handlers, and malicious URLs.
    If content is plain text (no HTML tags), automatically format paragraphs.
    """
    if not content:
        return ""

    content_str = str(content).strip()

    # If the text has no HTML markup, convert double newlines to paragraphs
    if not re.search(r'<[a-zA-Z\/][^>]*>', content_str):
        paragraphs = [p.strip() for p in content_str.split('\n\n') if p.strip()]
        formatted = []
        for p in paragraphs:
            # Handle bullet lines
            lines = p.split('\n')
            if all(line.strip().startswith(('-', '*', '•')) for line in lines if line.strip()):
                items = [f"<li>{escape(re.sub(r'^[-*•]\s*', '', line.strip()))}</li>" for line in lines if line.strip()]
                formatted.append(f"<ul class=\"mb-3\">{''.join(items)}</ul>")
            else:
                clean_lines = [escape(l) for l in lines]
                formatted.append(f"<p class=\"mb-3 leading-relaxed\">{'<br>'.join(clean_lines)}</p>")
        return mark_safe('\n'.join(formatted))

    parser = SafeHTMLParser()
    try:
        parser.feed(content_str)
        parser.close()
        sanitized = parser.get_html()
    except Exception:
        sanitized = escape(content_str)

    return mark_safe(sanitized)

