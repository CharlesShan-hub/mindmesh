from pathlib import Path
import click
import shutil
import mindmesh as mm

@click.command()
@click.option('--src', type=click.Path(exists=True, file_okay=False, dir_okay=True), help='Base path of src project.')
@click.option('--dist', type=click.Path(exists=True, file_okay=False, dir_okay=True), help='Base path of dist project.')
@click.option('--src_kind', help='kind of src project.')
@click.option('--dist_kind', help='kind of dist project.')
def convert(src: Path, dist: Path, src_kind: str,dist_kind: str):
    src_path = Path(src)
    dist_path = Path(dist)

    if src_kind == 'obsidian' and dist_kind == 'origin':
        converter = mm.ObsidianMarkdown()

    for file in src_path.rglob("*"):
        if not file.is_file() or file.name == '.DS_Store':
            continue
        relative_path = file.relative_to(src_path)
        print(f"🚀 Start processing: {relative_path}")
        target_dir = dist_path / relative_path.parent
        if not target_dir.exists():
            print(f"📁 Creating directory: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

        if file.suffix.lower() == ".md":
            with file.open('r', encoding='utf-8') as f:
                content = f.read()
            content = converter(content)
            with (dist_path / relative_path).open('w', encoding='utf-8') as f:
                f.write(content)
        else:
            shutil.copy2(file, dist_path / relative_path)


if __name__ == '__main__':
    convert()