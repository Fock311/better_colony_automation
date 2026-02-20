import os
from pathlib import Path
import shutil

COPY_FOLDERS = [
    "common",
    "events",
    "gfx",
    "interface",
    "localisation"
]

COPY_FLILES = [
    "descriptor.mod",
    "license",
    "thumbnail.png",
    "README.md",
    "README_EN.md"
]

CURRENT_ROOT:Path = Path(__file__).parent
RELEASE_ROOT:Path = CURRENT_ROOT.parent / 'release_better_colony_automation'


def clear_release_root():
    if RELEASE_ROOT.exists() and RELEASE_ROOT.is_dir():
        for item in RELEASE_ROOT.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        RELEASE_ROOT.mkdir(parents=True, exist_ok=True)

def copy_folders_and_files():
    for folder in COPY_FOLDERS:
        src = CURRENT_ROOT / folder
        dst = RELEASE_ROOT / folder
        if src.exists() and src.is_dir():
            shutil.copytree(src, dst)
    for file in COPY_FLILES:
        src = CURRENT_ROOT / file
        dst = RELEASE_ROOT / file
        if src.exists() and src.is_file():
            shutil.copy2(src, dst)

if __name__ == "__main__":
    clear_release_root()
    copy_folders_and_files()


