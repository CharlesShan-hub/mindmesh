from mistune import create_markdown
from mistune.renderers.markdown import MarkdownRenderer

def wikilink_plugin(md):
    # 定义维基链接的正则表达式模式
    WIKI_LINK_PATTERN = r'\[\[(?P<link_text>[^\|\]]+?)\|(?P<link_target>[^\]]+?)\]\]'
    
    # 注册行内插件
    md.inline.register('wikilink', WIKI_LINK_PATTERN, parse_wikilink, before='link')
    
    # 如果使用 HTML 渲染器，注册相应的渲染器函数
    if md.renderer and md.renderer.NAME == 'markdown':
        md.renderer.register('wikilink', render_wikilink)

def parse_wikilink(inline, m, state):
    link_text = m.group('link_text')
    link_target = m.group('link_target')
    # 添加解析后的令牌
    state.append_token({'type': 'wikilink', 'text': link_text, 'target': link_target})
    # 返回解析文本的结束位置
    return m.end()

def render_wikilink(renderer, text, target):
    # 返回 Markdown 格式的链接
    return f'[{text}]({target})'


if __name__ == '__main__':
    # 创建 Markdown 实例并添加插件
    markdown = create_markdown(renderer=MarkdownRenderer(),plugins=[wikilink_plugin])

    # 使用 Markdown 实例转换文本
    converted_text = markdown('这是一个~~维基链接~~：[[链接文本|链接地址]]')
    print(converted_text)
