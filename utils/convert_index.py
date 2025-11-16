#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def parse_array(line_value: str):
    """
    TOML/YAML 風: ["a", "b"] を ["a", "b"] にするだけの簡易パーサ。
    """
    m = re.match(r"\[(.*)\]", line_value.strip())
    if not m:
        return []

    inner = m.group(1).strip()
    if not inner:
        return []

    items = []
    for part in inner.split(","):
        part = part.strip()
        # 先頭と末尾の ' or " を削除
        if (part.startswith('"') and part.endswith('"')) or (
            part.startswith("'") and part.endswith("'")
        ):
            part = part[1:-1]
        if part:
            items.append(part)
    return items


def extract_frontmatter(text: str):
    """
    先頭の TOML (+ + +) or YAML (---) フロントマターを切り出して
    (header_text, body_text, header_type) を返す。
    header_type は "toml" / "yaml" / None。
    """
    # TOML +++ ... +++
    if text.startswith("+++"):
        m = re.match(
            r"^\+\+\+\s*\n(.*?)^\+\+\+\s*\n?",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        if not m:
            return None, text, None
        header = m.group(1)
        body = text[m.end():]
        return header, body, "toml"

    # YAML --- ... ---
    if text.startswith("---"):
        m = re.match(
            r"^---\s*\n(.*?)^---\s*\n?",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        if not m:
            return None, text, None
        header = m.group(1)
        body = text[m.end():]
        return header, body, "yaml"

    return None, text, None


def parse_toml_header(header_text: str):
    """
    超簡易 TOML パーサ： key = value の行だけ扱う。
    """
    data = {}
    for line in header_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*=\s*(.+)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()

        # 文字列
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            data[key] = value[1:-1]
        # 配列
        elif value.startswith("[") and value.endswith("]"):
            data[key] = parse_array(value)
        else:
            # その他 (数値, bool, 日付など) はそのまま文字列として保持
            data[key] = value
    return data


def parse_yaml_header(header_text: str):
    """
    超簡易 YAML パーサ： key: value の1行形式だけ扱う。
    (複数行の配列などは対象外)
    """
    data = {}
    for line in header_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()

        if value == "" or value.lower() == "null":
            data[key] = ""
        # 文字列
        elif (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            data[key] = value[1:-1]
        # 配列
        elif value.startswith("[") and value.endswith("]"):
            data[key] = parse_array(value)
        else:
            # その他 (数値, bool, 日付など) はそのまま文字列として保持
            data[key] = value
    return data


def yaml_escape_single_quoted(s: str) -> str:
    """
    YAML の single-quoted 用に ' を '' にエスケープ。
    """
    return s.replace("'", "''")


def yaml_escape_double_quoted(s: str) -> str:
    """
    YAML の double-quoted 用に最低限のエスケープ。
    """
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    return s


def build_yaml_frontmatter(data: dict) -> str:
    """
    目的の YAML フロントマター文字列を組み立てる。

    ---
    title: '...'
    description: ""
    pubDate: ...
    heroImage: '@/assets/blog-placeholder-2.jpg'
    tags: ["..."]
    ---
    """
    title = data.get("title", "")
    # date(TOML) or pubDate(YAML) のどちらでも拾う
    date = data.get("pubDate", data.get("date", ""))

    # description があれば引き継ぎ、なければ空文字
    description = data.get("description", "")

    # categories があればそれを tags に、なければ元の tags を使用
    categories = data.get("categories")
    tags = categories if categories else data.get("tags", [])

    # tags は配列前提
    if not isinstance(tags, list):
        tags = [str(tags)]

    # heroImage が YAML にすでにあれば引き継ぎ、なければデフォルト
    hero_image = data.get("heroImage", '@/assets/blog-placeholder-2.jpg')

    title_escaped = yaml_escape_single_quoted(str(title))
    desc_escaped = yaml_escape_double_quoted(str(description))

    # tags を ["a", "b"] の形に
    tags_inner = ", ".join(f'"{t}"' for t in tags)
    tags_line = f"[{tags_inner}]"

    lines = [
        "---",
        f"title: '{title_escaped}'",
        f'description: "{desc_escaped}"',
        f"pubDate: {date}",
        f"heroImage: '{hero_image}'",
        f"tags: {tags_line}",
        "---",
        "",
    ]
    return "\n".join(lines)


def convert_file(path: Path, dry_run: bool = False):
    text = path.read_text(encoding="utf-8")
    header_text, body, header_type = extract_frontmatter(text)

    if header_type is None:
        print(f"[SKIP] No frontmatter found: {path}")
        return

    if header_type == "toml":
        data = parse_toml_header(header_text)
    elif header_type == "yaml":
        data = parse_yaml_header(header_text)
    else:
        print(f"[SKIP] Unknown frontmatter type for: {path}")
        return

    new_header = build_yaml_frontmatter(data)
    new_text = new_header + body

    if dry_run:
        print(f"===== {path} (converted preview) =====")
        print(new_text)
    else:
        path.write_text(new_text, encoding="utf-8")
        print(f"[OK] Converted ({header_type} -> yaml): {path}")


def main():
    ap = argparse.ArgumentParser(
        description=(
            "Convert frontmatter to YAML for Markdown files under "
            "src/content/blog/**/index.md (supports TOML +++ and YAML ---)."
        )
    )
    ap.add_argument(
        "--root",
        type=str,
        default="src/content/blog",
        help="Root directory to search (default: src/content/blog)",
    )
    ap.add_argument(
        "--pattern",
        type=str,
        default="index.md",
        help="Filename pattern to match (default: index.md)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print converted result to stdout instead of overwriting files",
    )
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] Root directory not found: {root}")
        return

    targets = sorted(root.rglob(args.pattern))

    if not targets:
        print(f"[INFO] No files matched: {root}/**/{args.pattern}")
        return

    print(f"[INFO] Found {len(targets)} files under {root} matching {args.pattern}")
    for path in targets:
        convert_file(path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
