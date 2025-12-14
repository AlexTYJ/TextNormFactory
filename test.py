#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

MAGIC_ROOT = Path("/home/yujietu/MagicData")

OLD_PREFIX = "/home/yujietu"
NEW_PREFIX = "/mnt/conversationhubhot/yujietu/data"


def rewrite_prefix(path: Path) -> str:
    """
    把 /home/yujietu 前缀替换成 /mnt/conversationhubhot/yujietu/data
    """
    p = str(path.resolve())
    if p.startswith(OLD_PREFIX):
        return p.replace(OLD_PREFIX, NEW_PREFIX, 1)
    return p


def main():
    dataset_dirs = [
        d for d in MAGIC_ROOT.iterdir()
        if d.is_dir() and (d / "json").exists() and (d / "audio").exists()
    ]

    print(f"📁 Found {len(dataset_dirs)} dataset directories")

    for dataset_dir in sorted(dataset_dirs):
        dataset_name = dataset_dir.name
        json_dir = dataset_dir / "json"
        audio_dir = dataset_dir / "audio"

        audio_files = sorted(audio_dir.glob("*.mp3"))
        json_files = sorted(json_dir.glob("*.json"))

        audio_scp_path = dataset_dir / f"audio_{dataset_name}.scp"
        json_scp_path = dataset_dir / f"json_{dataset_name}.scp"

        audio_lines = [
            rewrite_prefix(p) for p in audio_files
        ]
        json_lines = [
            rewrite_prefix(p) for p in json_files
        ]

        audio_scp_path.write_text(
            "\n".join(audio_lines) + "\n",
            encoding="utf-8"
        )
        json_scp_path.write_text(
            "\n".join(json_lines) + "\n",
            encoding="utf-8"
        )

        print(
            f"✅ {dataset_name}: "
            f"{len(audio_lines)} audio, {len(json_lines)} json"
        )

    print("🎉 All scp files generated (one path per line)")


if __name__ == "__main__":
    main()
