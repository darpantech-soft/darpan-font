"""
Darpan Font — Unified Production Build Pipeline (v6.0 Marathi Engine)
=====================================================================
Features:
1. Shirorekha (Headline) connection fix for brush-paint gaps.
2. 3-glyph & multi-glyph conjunct injection into HALF feature (longest-match-first).
3. COMPLETE FIX for OpenType Marathi LangSys (dev2 MAR / deva MAR):
   - Copies all standard Devanagari features (rphf, half, akhn, pres, blwf, abvs, etc.)
     into LangSys: MAR so browsers with <html lang="mr"> do NOT disable shaping!
   - Adds half-form rules for Marathi localized glyphs (dvLA.mar -> dvL, dvSHA.mar -> dvSH).
   - Generates Marathi conjunct variants for dvLA.mar and dvSHA.mar.
4. Exports production-ready TTF and WOFF2.
5. Automated HarfBuzz validation across both Marathi (mr) and default/Hindi (dflt).
"""

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
import uharfbuzz as hb


def get_glyph_bounds(font, glyph_name):
    """Get bounding box (xMin, yMin, xMax, yMax) of a glyph."""
    glyf = font['glyf']
    if glyph_name not in glyf:
        return None
    g = glyf[glyph_name]
    if g.numberOfContours == 0:
        return None
    return (g.xMin, g.yMin, g.xMax, g.yMax)


def analyze_headline_height(font):
    """Find average headline (shirorekha) yMax by analyzing standard consonants."""
    glyf = font['glyf']
    sample = ['dvKA', 'dvGA', 'dvTA', 'dvDA', 'dvNA', 'dvPA', 'dvMA', 'dvSA']
    heights = [glyf[name].yMax for name in sample if name in glyf and glyf[name].numberOfContours > 0]
    return (sum(heights) / len(heights)) if heights else 750.0


def add_headline_bar(font, glyph_name, headline_y, bar_thickness=45):
    """Add a connecting headline bar to a conjunct glyph."""
    glyf = font['glyf']
    if glyph_name not in glyf:
        return False
    g = glyf[glyph_name]
    if g.numberOfContours <= 0 or g.isComposite():
        return False

    xMin, yMin, xMax, yMax = g.xMin, g.yMin, g.xMax, g.yMax
    if (xMax - xMin) < 100:
        return False

    bar_top = yMax
    bar_bottom = yMax - bar_thickness

    bar_coords = [
        (xMin, bar_top),
        (xMax, bar_top),
        (xMax, bar_bottom),
        (xMin, bar_bottom),
    ]

    coords = list(g.coordinates)
    flags = list(g.flags)
    endPts = list(g.endPtsOfContours)

    new_start = len(coords)
    for pt in bar_coords:
        coords.append(pt)
        flags.append(1)
    endPts.append(new_start + len(bar_coords) - 1)

    g.coordinates = type(g.coordinates)(coords)
    g.flags = type(g.flags)(flags)
    g.endPtsOfContours = endPts
    g.numberOfContours = len(endPts)
    g.recalcBounds(glyf)
    return True


def apply_headline_fixes(font):
    """Apply connecting headline bars across all conjunct glyphs."""
    print("--- Step 1: Applying Shirorekha (Headline) Connection Fixes ---")
    headline_y = analyze_headline_height(font)
    print(f"Detected headline height: {headline_y:.1f} units")

    conjuncts = [
        name for name in font.getGlyphOrder()
        if name.startswith('dv') and '_' in name and not name.startswith('dvm')
    ]

    modified, skipped = 0, 0
    for name in conjuncts:
        if add_headline_bar(font, name, headline_y, bar_thickness=45):
            modified += 1
        else:
            skipped += 1
    print(f"Headline bars added: {modified} glyphs (skipped: {skipped})")


def extract_ligatures(lookup):
    """Extract all ligature rules from a Type 4 lookup."""
    rules = []
    if lookup.LookupType != 4:
        return rules
    for st in lookup.SubTable:
        if hasattr(st, 'ligatures'):
            for fg, ligs in st.ligatures.items():
                for l in ligs:
                    rules.append(([fg] + list(l.Component), l.LigGlyph))
    return rules


def build_lig_subtable(rules):
    """Build a Format 1 LigatureSubst subtable with longest-match-first sorting."""
    st = otTables.LigatureSubst()
    st.Format = 1
    st.ligatures = {}
    for comps, result in rules:
        first = comps[0]
        lig = otTables.Ligature()
        lig.LigGlyph = result
        lig.Component = comps[1:]
        lig.CompCount = len(comps)
        if first not in st.ligatures:
            st.ligatures[first] = []
        st.ligatures[first].append(lig)

    # Longest match first
    for fg in st.ligatures:
        st.ligatures[fg].sort(key=lambda l: -l.CompCount)
    return st


def apply_conjunct_and_marathi_rules(font):
    """Inject conjunct rules and fully wire Marathi LangSys."""
    print("\n--- Step 2: Injecting Conjunct Rules and Fixing Marathi LangSys ---")
    gsub = font['GSUB'].table
    virama = 'dvVirama'

    # Extract half-form mappings: dvK -> dvKA
    half_map = {}
    for li in [11, 12]:
        for comps, res in extract_ligatures(gsub.LookupList.Lookup[li]):
            if len(comps) == 2 and comps[1] == virama:
                half_map[res] = comps[0]
    print(f"Extracted {len(half_map)} half-form mappings")

    # Extract rules from pres (14), rkrf (8), akhn (5)
    pres_rules = extract_ligatures(gsub.LookupList.Lookup[14])
    rkrf_rules = extract_ligatures(gsub.LookupList.Lookup[8])
    akhn_orig = extract_ligatures(gsub.LookupList.Lookup[5])

    three_glyph = []
    for comps, result in pres_rules:
        if len(comps) == 2:
            hf, base = comps
            if hf in half_map:
                three_glyph.append(([half_map[hf], virama, base], result))
        elif len(comps) == 3:
            h1, h2, base = comps
            if h1 in half_map and h2 in half_map:
                three_glyph.append(([half_map[h1], virama, half_map[h2], virama, base], result))
            elif h1 in half_map:
                three_glyph.append(([half_map[h1], virama, h2, base], result))
        elif len(comps) == 4:
            h1, h2, h3, base = comps
            if h1 in half_map and h2 in half_map and h3 in half_map:
                three_glyph.append(([half_map[h1], virama, half_map[h2], virama, half_map[h3], virama, base], result))

    # Add rkrf rules
    existing = set(tuple(r[0]) for r in three_glyph)
    for comps, result in rkrf_rules:
        if tuple(comps) not in existing:
            three_glyph.append((comps, result))
            existing.add(tuple(comps))

    # Add original akhn rules
    for comps, result in akhn_orig:
        if tuple(comps) not in existing:
            three_glyph.append((comps, result))
            existing.add(tuple(comps))

    # Duplicate rules for Marathi alternates: dvLA.mar and dvSHA.mar
    mar_variants = []
    for comps, result in three_glyph:
        if 'dvLA' in comps or 'dvSHA' in comps:
            new_comps = [
                'dvLA.mar' if c == 'dvLA' else ('dvSHA.mar' if c == 'dvSHA' else c)
                for c in comps
            ]
            if tuple(new_comps) not in existing:
                mar_variants.append((new_comps, result))
                existing.add(tuple(new_comps))

    three_glyph.extend(mar_variants)
    print(f"Generated {len(three_glyph)} 3-glyph rules (including {len(mar_variants)} Marathi .mar variants)")

    # Get original half rules
    half_rules_11 = extract_ligatures(gsub.LookupList.Lookup[11])
    # Add half rules for Marathi glyphs so lk, lp, sc, sn form proper half shapes
    half_rules_11.append((['dvLA.mar', virama], 'dvL'))
    half_rules_11.append((['dvSHA.mar', virama], 'dvSH'))

    merged_rules = three_glyph + half_rules_11

    # Create new merged lookup for half
    new_lookup = otTables.Lookup()
    new_lookup.LookupType = 4
    new_lookup.LookupFlag = 0
    new_lookup.SubTable = [build_lig_subtable(merged_rules)]

    new_half_idx = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(new_lookup)
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

    # Update half feature to point to new_half_idx
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'half':
            old = list(fr.Feature.LookupListIndex)
            new_list = [new_half_idx if x == 11 else x for x in old]
            fr.Feature.LookupListIndex = new_list
            fr.Feature.LookupCount = len(new_list)

    # Create akhn lookup
    akhn_lookup = otTables.Lookup()
    akhn_lookup.LookupType = 4
    akhn_lookup.LookupFlag = 0
    akhn_lookup.SubTable = [build_lig_subtable(three_glyph)]
    akhn_idx = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(akhn_lookup)
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'akhn':
            fr.Feature.LookupListIndex = [akhn_idx]
            fr.Feature.LookupCount = 1

    # Add cjct feature
    cjct_lookup = otTables.Lookup()
    cjct_lookup.LookupType = 4
    cjct_lookup.LookupFlag = 0
    cjct_lookup.SubTable = [build_lig_subtable(three_glyph)]
    cjct_idx = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(cjct_lookup)
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

    cjct_rec = otTables.FeatureRecord()
    cjct_rec.FeatureTag = 'cjct'
    cjct_rec.Feature = otTables.Feature()
    cjct_rec.Feature.FeatureParams = None
    cjct_rec.Feature.LookupListIndex = [cjct_idx]
    cjct_rec.Feature.LookupCount = 1
    gsub.FeatureList.FeatureRecord.append(cjct_rec)
    gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)
    cjct_feat = gsub.FeatureList.FeatureCount - 1

    # =========================================================================
    # CRUCIAL: Connect ALL features to LangSys MAR in dev2 and deva!
    # =========================================================================
    for sr in gsub.ScriptList.ScriptRecord:
        if sr.ScriptTag in ('DFLT', 'dev2', 'deva'):
            # Ensure cjct is added to default
            if sr.Script.DefaultLangSys:
                if cjct_feat not in sr.Script.DefaultLangSys.FeatureIndex:
                    sr.Script.DefaultLangSys.FeatureIndex.append(cjct_feat)
                    sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
                dflt_features = list(sr.Script.DefaultLangSys.FeatureIndex)
            else:
                dflt_features = []

            # Now update all LangSys records (especially MAR)
            for lr in sr.Script.LangSysRecord:
                combined = list(lr.LangSys.FeatureIndex)
                # Ensure locl is preserved first, then all dflt features
                for fi in dflt_features:
                    if fi not in combined:
                        combined.append(fi)
                lr.LangSys.FeatureIndex = combined
                lr.LangSys.FeatureCount = len(combined)

    print("Marathi LangSys (MAR) and DefaultLangSys successfully synchronized with all features!")


def update_metadata(font):
    """Set proper font metadata and name table records."""
    name_map = {
        1: 'Darpan',
        2: 'Regular',
        3: 'Darpan-Regular',
        4: 'Darpan Regular',
        5: 'Version 6.000; 2026 (Marathi Fixed)',
        6: 'Darpan-Regular',
        9: 'Catherine Leigh Schmidt (original), Modified for Marathi Web Conjuncts',
        16: 'Darpan',
        17: 'Regular',
    }
    for r in font['name'].names:
        if r.nameID in name_map:
            val = name_map[r.nameID]
            r.string = val.encode('utf-16-be') if r.platformID == 3 else val.encode('utf-8')
    font['head'].fontRevision = 6.0


def validate_font(ttf_path):
    """Automated HarfBuzz validation across Marathi (mr) and default (dflt)."""
    face = hb.Face(hb.Blob(open(ttf_path, 'rb').read()))
    font = hb.Font(face)
    font.scale = (face.upem, face.upem)

    test_words = [
        ("द्विभाषिक", "dvibhaashik"),
        ("स्मरणपत्रे", "smaranpatre"),
        ("उच्च", "uchch"),
        ("दस्तऐवज", "dastaivaj"),
        ("संस्कृती", "sanskruti"),
        ("स्वतंत्र", "svatantra"),
        ("द्वारा", "dvaara"),
        ("तत्त्व", "tattva"),
        ("बुद्धी", "buddhi"),
        ("मराठी", "marathi"),
        ("शुद्ध", "shuddha"),
        ("क्ल", "k-la"),
        ("ग्ल", "g-la"),
        ("प्ल", "p-la"),
        ("ब्ल", "b-la"),
        ("म्ल", "m-la"),
        ("स्ल", "s-la"),
        ("ह्ल", "h-la"),
        ("ल्क", "l-ka"),
        ("ल्ग", "l-ga"),
        ("ल्प", "l-pa"),
        ("ल्ल", "l-la"),
        ("श्च", "sh-ca"),
        ("श्न", "sh-na"),
        ("श्म", "sh-ma"),
        ("श्र", "sh-ra"),
        ("र्क", "r-ka (reph)"),
        ("र्ग", "r-ga (reph)"),
        ("र्म", "r-ma (reph)"),
        ("र्य", "r-ya (reph)"),
        ("र्व", "r-va (reph)"),
    ]

    for lang in ['mr', 'dflt']:
        print(f"\n--- Validation with Language = '{lang}' ---")
        failed = 0
        for word, desc in test_words:
            buf = hb.Buffer()
            buf.add_str(word)
            buf.guess_segment_properties()
            if lang != 'dflt':
                buf.language = lang
            hb.shape(font, buf)
            names = [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]
            has_halant = any(h in ' '.join(names) for h in ['dvVirama', 'uni094D'])
            status = "❌ FAIL" if has_halant else "✅ OK"
            if has_halant:
                failed += 1
            print(f"  {status} {word:14} ({desc:16}) -> {' + '.join(names)}")

        if failed == 0:
            print(f"🎉 Language '{lang}': ALL {len(test_words)} words passed with zero broken conjuncts!")
        else:
            print(f"⚠️ Language '{lang}': {failed}/{len(test_words)} words failed.")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'yatra-source', 'Yatra-Regular.ttf')
    out_dir = os.path.join(base_dir, 'output')
    os.makedirs(out_dir, exist_ok=True)

    out_ttf = os.path.join(out_dir, 'Darpan-Regular.ttf')
    out_woff2 = os.path.join(out_dir, 'Darpan-Regular.woff2')

    print(f"Loading base font: {input_path}")
    font = TTFont(input_path)

    # 1. Headline connection
    apply_headline_fixes(font)

    # 2. Conjunct and Marathi rules
    apply_conjunct_and_marathi_rules(font)

    # 3. Metadata
    update_metadata(font)

    # 4. Save TTF & WOFF2
    print(f"\nSaving TTF: {out_ttf}")
    font.save(out_ttf)

    print(f"Saving WOFF2: {out_woff2}")
    f_woff2 = TTFont(out_ttf)
    f_woff2.flavor = 'woff2'
    f_woff2.save(out_woff2)

    # Also save Darpan-v5 and v4 aliases so test.html always loads them
    v5_woff2 = os.path.join(out_dir, 'Darpan-v5.woff2')
    v4_woff2 = os.path.join(out_dir, 'Darpan-v4.woff2')
    if not os.path.exists(v5_woff2):
        f_woff2.save(v5_woff2)

    ttf_kb = os.path.getsize(out_ttf) / 1024
    woff2_kb = os.path.getsize(out_woff2) / 1024
    print(f"Output sizes: TTF = {ttf_kb:.1f} KB | WOFF2 = {woff2_kb:.1f} KB")

    # 5. Validate both languages
    validate_font(out_ttf)


if __name__ == '__main__':
    main()
