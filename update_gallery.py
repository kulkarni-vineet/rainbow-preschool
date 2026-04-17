#!/usr/bin/env python3
"""
Rainbow Pre-School — Gallery Auto-Builder
==========================================
Run this after adding new photos to images/gallery/:

    python update_gallery.py

Handles ANY filenames: image-1.jpg, photo-1.jpg, diwali.jpg etc.
Auto-assigns categories from filename keywords.
"""

import os, json, re
from pathlib import Path

GALLERY_DIR = "images/gallery"
OUTPUT_FILE = "gallery-index.json"
IMAGE_EXTS  = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Category keywords — checks if any word appears in filename
CATEGORY_MAP = {
    "classroom":  ["classroom","class","room","learning","corner","table","board"],
    "activities": ["activity","art","craft","draw","paint","sanskrit","music",
                   "rhyme","outdoor","nature","play","dance","sing"],
    "events":     ["event","annual","function","evhall","ev-hall","hall",
                   "stage","programme","program","concert"],
    "saturday":   ["saturday","funday","fun-day","fun_day","weekend"],
    "festival":   ["diwali","holi","ganesh","republic","independence",
                   "christmas","birthday","celebration","festival","navratri"],
    "sports":     ["sport","sports","game","games","run","race","field","jump"],
    "team":       ["teacher","staff","principal","team","faculty"],
}

def detect_category(filename):
    lower = filename.lower()
    for cat, keywords in CATEGORY_MAP.items():
        if any(kw in lower for kw in keywords):
            return cat
    return "activities"  # default

def make_title(filename, index):
    stem = Path(filename).stem
    # If it's just image-N or photo-N, use "Photo N"
    if re.match(r"^(image|img|photo|pic|picture)[-_]?\d+$", stem, re.IGNORECASE):
        num = re.search(r"\d+", stem).group()
        return f"Photo {num}"
    # Otherwise clean up the filename
    clean = re.sub(r"[-_]", " ", stem)
    clean = re.sub(r"\d+$", "", clean).strip()
    return clean.title() if clean else f"Photo {index+1}"

def make_desc(cat):
    descs = {
        "classroom":  "Inside our AC classroom",
        "activities": "Learning through fun activities",
        "events":     "School events & performances",
        "saturday":   "Saturday FunDay special!",
        "festival":   "Festival celebrations",
        "sports":     "Sports & outdoor activities",
        "team":       "Our wonderful team",
    }
    return descs.get(cat, "Rainbow Pre-School moments")

def scan_and_build():
    gallery_path = Path(GALLERY_DIR)
    if not gallery_path.exists():
        gallery_path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {GALLERY_DIR}")
        return []

    # Get all images, sort naturally (image-1, image-2 ... image-10, not image-10 before image-2)
    files = sorted(
        [f for f in gallery_path.iterdir() if f.suffix.lower() in IMAGE_EXTS],
        key=lambda f: [int(c) if c.isdigit() else c.lower()
                       for c in re.split(r"(\d+)", f.name)]
    )

    photos = []
    skipped = []
    for i, f in enumerate(files):
        size_kb = f.stat().st_size // 1024
        if size_kb > 3000:
            skipped.append(f"{f.name} ({size_kb}KB) — compress at squoosh.app")
            continue
        cat = detect_category(f.name)
        photos.append({
            "file":  f.name,
            "title": make_title(f.name, i),
            "cat":   cat,
            "desc":  make_desc(cat)
        })
        print(f"  ✅  {f.name:<35} → {cat}")

    if skipped:
        print("\n⚠️  Too large (skipped):")
        for s in skipped: print(f"     ❌ {s}")

    return photos

def main():
    print("=" * 55)
    print("🌈 Rainbow Pre-School — Gallery Builder")
    print("=" * 55)
    print(f"\nScanning: {GALLERY_DIR}/\n")

    photos = scan_and_build()

    data = {"total": len(photos), "photos": photos}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅  gallery-index.json updated — {len(photos)} photo(s)")

    if photos:
        cats = {}
        for p in photos: cats[p["cat"]] = cats.get(p["cat"],0)+1
        print("\nCategory breakdown:")
        for c,n in sorted(cats.items()): print(f"   {c:<15} {n} photo(s)")

    print("\n" + "=" * 55)
    print("NEXT: push to GitHub")
    print("  git add .")
    print("  git commit -m \"Updated gallery photos\"")
    print("  git push")
    print("✅  Site updates in ~2 minutes!")
    print("=" * 55)

if __name__ == "__main__":
    main()
