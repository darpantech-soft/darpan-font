"""
Darpan v5 — Add three-glyph conjunct rules to HALF feature.

Strategy: The half feature is PROVEN to fire in browsers. By adding
three-glyph rules (fullC + virama + fullC → conjunct) to the half
feature's lookup, we leverage LigatureSubst's longest-match-first
behavior:
  - 3-glyph: dvKA + dvVirama + dvLA → dvK_LA (fires first!)
  - 2-glyph: dvKA + dvVirama → dvK (fires if no 3-glyph match)
"""
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
import os

def extract_lig(lookup):
    rules = []
    if lookup.LookupType != 4: return rules
    for st in lookup.SubTable:
        if hasattr(st, 'ligatures'):
            for fg, ligs in st.ligatures.items():
                for l in ligs:
                    rules.append(([fg]+list(l.Component), l.LigGlyph))
    return rules

def build_lig_subtable(rules):
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
    # Sort: longest first for each first glyph
    for fg in st.ligatures:
        st.ligatures[fg].sort(key=lambda l: -l.CompCount)
    return st

def main():
    input_path = r'd:\web\projects\fontmake\yatra-source\Yatra-Regular.ttf'
    out_dir = r'd:\web\projects\fontmake\output'
    
    print("Loading original font...")
    font = TTFont(input_path)
    gsub = font['GSUB'].table
    
    # Extract half-form mappings
    virama = 'dvVirama'
    half_map = {}  # halfGlyph → fullConsonant
    for li in [11, 12]:
        for c, r in extract_lig(gsub.LookupList.Lookup[li]):
            if len(c) == 2 and c[1] == virama:
                half_map[r] = c[0]
    print(f"Half-form mappings: {len(half_map)}")
    
    # Extract pres rules (lookup 14)
    pres_rules = extract_lig(gsub.LookupList.Lookup[14])
    print(f"Pres rules: {len(pres_rules)}")
    
    # Extract rkrf rules (lookup 8)
    rkrf_rules = extract_lig(gsub.LookupList.Lookup[8])
    print(f"Rkrf rules: {len(rkrf_rules)}")
    
    # Build three-glyph rules from pres
    three_glyph = []
    for comps, result in pres_rules:
        if len(comps) == 2:
            hf = comps[0]
            base = comps[1]
            if hf in half_map:
                full = half_map[hf]
                three_glyph.append(([full, virama, base], result))
        elif len(comps) == 3:
            h1, h2, base = comps
            if h1 in half_map and h2 in half_map:
                f1, f2 = half_map[h1], half_map[h2]
                three_glyph.append(([f1, virama, f2, virama, base], result))
            elif h1 in half_map:
                f1 = half_map[h1]
                three_glyph.append(([f1, virama, h2, base], result))
        elif len(comps) == 4:
            h1, h2, h3, base = comps
            if h1 in half_map and h2 in half_map and h3 in half_map:
                f1, f2, f3 = half_map[h1], half_map[h2], half_map[h3]
                three_glyph.append(([f1, virama, f2, virama, f3, virama, base], result))

    # Add rkrf rules (already 3-glyph)
    existing = set(tuple(r[0]) for r in three_glyph)
    for comps, result in rkrf_rules:
        if tuple(comps) not in existing:
            three_glyph.append((comps, result))
            existing.add(tuple(comps))
    
    # Add original akhn rules
    akhn_orig = extract_lig(gsub.LookupList.Lookup[5])
    for comps, result in akhn_orig:
        if tuple(comps) not in existing:
            three_glyph.append((comps, result))
            existing.add(tuple(comps))
    
    print(f"Total three-glyph rules: {len(three_glyph)}")
    
    # STRATEGY: Merge three-glyph rules INTO the half feature lookups
    # Create a new lookup with ALL rules: three-glyph FIRST, then existing half rules
    
    # Get existing half rules from lookups 11 and 12
    half_rules_11 = extract_lig(gsub.LookupList.Lookup[11])
    half_rules_12 = extract_lig(gsub.LookupList.Lookup[12])
    print(f"Existing half rules: lookup11={len(half_rules_11)}, lookup12={len(half_rules_12)}")
    
    # Create merged lookup: three-glyph + half rules (longest first)
    merged_rules = three_glyph + half_rules_11
    print(f"Merged rules for new half lookup: {len(merged_rules)}")
    
    # Create new lookup
    new_lookup = otTables.Lookup()
    new_lookup.LookupType = 4
    new_lookup.LookupFlag = 0
    new_lookup.SubTable = [build_lig_subtable(merged_rules)]
    
    new_idx = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(new_lookup)
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
    print(f"New merged lookup at index {new_idx}")
    
    # Update half feature to use our merged lookup instead of lookup 11
    for i, fr in enumerate(gsub.FeatureList.FeatureRecord):
        if fr.FeatureTag == 'half':
            old = list(fr.Feature.LookupListIndex)
            new_list = [new_idx if x == 11 else x for x in old]
            fr.Feature.LookupListIndex = new_list
            fr.Feature.LookupCount = len(new_list)
            print(f"half feature {i}: {old} → {new_list}")
    
    # ALSO keep akhn with the same rules (belt + suspenders)
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
    
    # ALSO add cjct
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
    
    for sr in gsub.ScriptList.ScriptRecord:
        if sr.ScriptTag in ('DFLT', 'dev2', 'deva'):
            if sr.Script.DefaultLangSys:
                sr.Script.DefaultLangSys.FeatureIndex.append(cjct_feat)
                sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
            for lr in sr.Script.LangSysRecord:
                lr.LangSys.FeatureIndex.append(cjct_feat)
                lr.LangSys.FeatureCount = len(lr.LangSys.FeatureIndex)
    
    # Update naming
    name_map = {
        1:'Darpan', 2:'Regular', 3:'Darpan-Regular', 4:'Darpan Regular',
        5:'Version 5.000', 6:'Darpan-Regular', 16:'Darpan', 17:'Regular',
    }
    for r in font['name'].names:
        if r.nameID in name_map:
            r.string = name_map[r.nameID].encode('utf-16-be') if r.platformID == 3 else name_map[r.nameID].encode('utf-8')
    font['head'].fontRevision = 5.0
    
    # Save
    ttf = os.path.join(out_dir, 'Darpan-v5.ttf')
    woff2 = os.path.join(out_dir, 'Darpan-v5.woff2')
    print(f"\nSaving {ttf}")
    font.save(ttf)
    f2 = TTFont(ttf)
    f2.flavor = 'woff2'
    f2.save(woff2)
    
    s1 = os.path.getsize(ttf) / 1024
    s2 = os.path.getsize(woff2) / 1024
    print(f"TTF: {s1:.1f} KB | WOFF2: {s2:.1f} KB")
    print(f"\n✅ Darpan v5 built! Rules in half + akhn + cjct features.")

if __name__ == '__main__':
    main()
