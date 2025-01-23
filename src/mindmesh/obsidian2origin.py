from mistune import Markdown
from mistune.renderers.markdown import MarkdownRenderer
from pathlib import Path

# 维基链接的正则表达式模式
WIKILINK_PATTERN = r'\[\[(?P<wikilink_content>[^\[\]]+?)\]\]'

def parse_wikilink(inline, m, state):
    wikilink_content = m.group('wikilink_content')
    if '|' in wikilink_content:
        link_target, link_text = wikilink_content.split('|')
    else:
        link_target, link_text = [wikilink_content, None]
    if not link_text:
        link_text = Path(link_target).name
    state.append_token({'type': 'wikilink', 'text': link_text, 'target': link_target})
    return m.end()

class Obsidian2Origin(MarkdownRenderer):
    def wikilink(self, token, state):
        text = token['text']
        target = token['target']
        return f'[{target}]({text})'
    
class ObsidianOriginMarkdown(Markdown):
    def __init__(self, renderer=None, *args, **kwargs):
        if renderer is None:
            renderer = Obsidian2Origin()
        super().__init__(renderer=renderer, *args, **kwargs)
        self.inline.register('wikilink', WIKILINK_PATTERN, parse_wikilink, before='link')


if __name__ == '__main__':
    markdown = ObsidianOriginMarkdown()

    print(markdown('链接1：[[a/b/c|c]]')) # 链接1：[a/b/c](c)
    print(markdown('链接2：[[c]]')) # 链接2：[c](c)
    print(markdown('链接3：[[a/b/c]]')) # 链接3：[a/b/c](c)
    print(markdown('链接4：![[a/b/c.png|logo]]')) # 链接4：![a/b/c.png](logo)
    print(markdown('链接5：![a/b/c.png](logo)')) # 链接5：![a/b/c.png](logo)
