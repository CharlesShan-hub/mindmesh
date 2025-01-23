from mistune import Markdown
from mistune.renderers.markdown import MarkdownRenderer

# 维基链接的正则表达式模式
WIKILINK_PATTERN = r'\[\[(?P<link_text>[^\]\|]+)?\|?(?P<link_target>[^\]\|]+)?\]\]'

def parse_wikilink(inline, m, state):
    link_text = m.group('link_text') or m.group('link_target')
    link_target = m.group('link_target') or link_text
    state.append_token({'type': 'wikilink', 'text': link_text, 'target': link_target})
    return m.end()

class ObsidianMarkdownRenderer(MarkdownRenderer):
    def wikilink(self, token, state):
        text = token['text']
        target = token['target']
        return f'[{target}]({text})'
    
class ObsidianMarkdown(Markdown):
    def __init__(self, renderer=None, *args, **kwargs):
        if renderer is None:
            renderer = ObsidianMarkdownRenderer()
        super().__init__(renderer=renderer, *args, **kwargs)
        self.inline.register('wikilink', WIKILINK_PATTERN, parse_wikilink, before='link')


if __name__ == '__main__':
    markdown = ObsidianMarkdown()

    test_string = '这是一个维基链接：[[链接文本|链接地址]]'
    converted_text = markdown(test_string)
    print(converted_text) 
