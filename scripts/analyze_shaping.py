"""Analyze Yatra One font shaping with uharfbuzz.
Tests critical Marathi words and identifies broken conjuncts."""

import uharfbuzz as hb
import sys

def shape_text(font_path, text, script="dev2", language="MAR"):
    with open(font_path, "rb") as f:
        blob = hb.Blob(f.read())
    face = hb.Face(blob)
    font = hb.Font(face)
    font.scale = (face.upem, face.upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    infos = buf.glyph_infos
    positions = buf.glyph_positions
    results = []
    for info, pos in zip(infos, positions):
        glyph_name = font.glyph_to_string(info.codepoint)
        results.append({
            "gid": info.codepoint,
            "name": glyph_name,
            "cluster": info.cluster,
            "x_advance": pos.x_advance,
        })
    return results

def check_for_halant(glyphs):
    halant_names = ["dvVirama", "uni094D", "halant"]
    for g in glyphs:
        if any(h in g["name"] for h in halant_names):
            return True
    return False

def main():
    font_path = sys.argv[1] if len(sys.argv) > 1 else r"d:\web\projects\fontmake\yatra-source\Yatra-Regular.ttf"
    test_words = [
        ("द्विभाषिक", "dvibhaashik"),
        ("स्मरणपत्रे", "smaranpatre"),
        ("उच्च", "uchch"),
        ("दस्तऐवज", "dastaivaj"),
        ("संस्कृती", "sanskruti"),
        ("स्वतंत्र", "svatantra"),
        ("द्वारा", "dvaara"),
        ("विद्यालय", "vidyaalay"),
        ("तत्त्व", "tattva"),
        ("बुद्धी", "buddhi"),
        ("वृत्त", "vrutt"),
        ("शुद्ध", "shuddha"),
        ("अस्त्र", "astra"),
        ("मराठी", "marathi"),
        ("कृत्य", "krutya"),
        ("पृष्ठभूमी", "prushthabhumi"),
        ("स्वतंत्र", "svatantra"),
        ("उच्चगुणवत्ता", "uchchgunavatta"),
    ]
    print(f"Font: {font_path}")
    print("=" * 80)
    broken = []
    working = []
    for word, desc in test_words:
        glyphs = shape_text(font_path, word)
        has_halant = check_for_halant(glyphs)
        status = "BROKEN" if has_halant else "OK"
        glyph_names = " + ".join(g["name"] for g in glyphs)
        print(f"\n[{status}] {word} ({desc})")
        print(f"  Glyphs: {glyph_names}")
        if has_halant:
            broken.append((word, desc))
        else:
            working.append((word, desc))
    print(f"\n{'='*80}")
    print(f"Working: {len(working)}/{len(test_words)}")
    print(f"Broken:  {len(broken)}/{len(test_words)}")
    if broken:
        print(f"\nBroken words:")
        for w, d in broken:
            print(f"  - {w} ({d})")

if __name__ == "__main__":
    main()
