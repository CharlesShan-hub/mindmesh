from pathlib import Path

def get_ob_titles(base: Path):
    assert base.exists()
    d = {}
    for partten in ['*.md', '*.png', '*.svg', '*.jpg']:
        for f in base.rglob(partten):
            d[f] = {
                'name': f.name,
                'relate': f.relative_to(base)
            }
    return d

if __name__ == '__main__':
    d = get_ob_titles(Path('/Users/kimshan/Public/learn/DigitalGarden/PKM-BOOK'))
    print(d)