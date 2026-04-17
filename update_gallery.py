#!/usr/bin/env python3
"""
🌈 Rainbow Pre-School — Gallery Auto-Builder
============================================
Run this script from Git Bash whenever you add new photos:
 
    python update_gallery.py
 
It scans images/gallery/ and rebuilds gallery-index.json automatically.
Then push to GitHub and the website updates within 2 minutes!
"""
 
import os
import json
import re
from pathlib import Path
 
# ── Settings ──────────────────────────────────────────────
GALLERY_DIR  = "images/gallery"
OUTPUT_FILE  = "gallery-index.json"
IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
 
# ── Category detection from filename ──────────────────────
# File name keywords → category for filter tabs
CATEGORY_MAP = {
    "classroom":       "classroom",
    "class":           "classroom",
    "room":            "classroom",
    "learning":        "classroom",
    "corner":          "classroom",
    "activity":        "activities",
    "activities":      "activities",
    "art":             "activities",
    "craft":           "activities",
    "draw":            "activities",
    "paint":           "activities",
    "sanskrit":        "activities",
    "music":           "activities",
    "rhyme":           "activities",
    "rhymes":          "activities",
    "outdoor":         "activities",
    "nature":          "activities",
    "sport":           "sports",
    "sports":          "sports",
    "game":            "sports",
    "games":           "sports",
    "run":             "sports",
    "play":            "activities",
    "event":           "events",
    "events":          "events",
    "annual":          "events",
    "function":        "events",
    "ev-hall":         "events",
    "evhall":          "events",
    "hall":            "events",
    "stage":           "events",
    "saturday":        "saturday",
    "funday":          "saturday",
    "fun-day":         "saturday",
    "fun_day":         "saturday",
    "festival":        "festival",
    "diwali":          "festival",
    "holi":            "festival",
    "ganesh":          "festival",
    "republic":        "festival",
    "independence":    "festival",
    "christmas":       "festival",
    "birthday":        "festival",
    "celebration":     "festival",
    "team":            "team",
    "teacher":         "team",
    "staff":           "team",
    "principal":       "team",
}
 
def filename_to_title(filename):
    """Convert filename like 'art-craft-day.jpg' → 'Art Craft Day'"""
    stem = Path(filename).stem          # remove extension
    stem = re.sub(r'[-_]', ' ', stem)  # hyphens/underscores → space
    stem = re.sub(r'\d+$', '', stem)   # remove trailing numbers
    return stem.strip().title()
 
def detect_category(filename):
    """Detect category from keywords in filename"""
    lower = filename.lower()
    for keyword, cat in CATEGORY_MAP.items():
        if keyword in lower:
            return cat
    return "activities"  # default category
 
def scan_gallery():
    """Scan gallery folder and return list of photo objects"""
    gallery_path = Path(GALLERY_DIR)
 
    if not gallery_path.exists():
        print(f"⚠️  Folder not found: {GALLERY_DIR}")
        print(f"   Creating it now...")
        gallery_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {GALLERY_DIR}")
        return []
 
    photos = []
    skipped = []
 
    for f in sorted(gallery_path.iterdir()):
        if f.suffix.lower() in IMAGE_EXTS:
            size_kb = f.stat().st_size // 1024
            if size_kb > 2048:
                skipped.append(f"{f.name} ({size_kb}KB — too large, compress at squoosh.app)")
                continue
            photos.append({
                "file":  f.name,
                "title": filename_to_title(f.name),
                "cat":   detect_category(f.name),
                "desc":  ""   # optional: you can manually add descriptions
            })
            print(f"  ✅ {f.name:<40} → category: {detect_category(f.name)}")
 
    if skipped:
        print(f"\n⚠️  Skipped (too large — please compress these at squoosh.app):")
        for s in skipped:
            print(f"   ❌ {s}")
 
    return photos
 
def write_json(photos):
    """Write gallery-index.json"""
    data = {
        "total":  len(photos),
        "photos": photos
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Written: {OUTPUT_FILE} ({len(photos)} photos)")
 
def main():
    print("=" * 55)
    print("🌈 Rainbow Pre-School — Gallery Builder")
    print("=" * 55)
    print(f"\nScanning: {GALLERY_DIR}/\n")
 
    photos = scan_gallery()
 
    if not photos:
        print("\n⚠️  No images found in images/gallery/")
        print("   Add .jpg/.png/.webp photos to that folder and run again.")
        # Still write empty JSON so website doesn't error
        write_json([])
    else:
        write_json(photos)
 
        # Summary by category
        cats = {}
        for p in photos:
            cats[p["cat"]] = cats.get(p["cat"], 0) + 1
        print("\nCategory breakdown:")
        for cat, count in sorted(cats.items()):
            print(f"   {cat:<15} {count} photo{'s' if count>1 else ''}")
 
    print("\n" + "=" * 55)
    print("NEXT STEPS:")
    print("  1. git add .")
    print('  2. git commit -m "Updated gallery photos"')
    print("  3. git push")
    print("  ✅ Website updates in ~2 minutes!")
    print("=" * 55)
 
if __name__ == "__main__":
    main()
