import os
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

font_path = r'd:\web\projects\fontmake\yatra-source\Yatra-Regular.ttf'
out_dir = r'd:\web\projects\fontmake\output'
os.makedirs(out_dir, exist_ok=True)
out_ttf = os.path.join(out_dir, 'Darpan-Regular.ttf')
out_woff2 = os.path.join(out_dir, 'Darpan-Regular.woff2')

print("Loading font...")
font = TTFont(font_path)

# Update head version
font['head'].fontRevision = 2.000

# Update name table
name_dict = {
    1: 'Darpan',
    2: 'Regular',
    3: 'Darpan-Regular',
    4: 'Darpan Regular',
    5: 'Version 2.000',
    6: 'Darpan-Regular',
    9: 'Catherine Leigh Schmidt (original), Modified for Marathi',
    11: '',
    13: 'This Font Software is licensed under the SIL Open Font License, Version 1.1.',
    14: 'https://openfontlicense.org',
    16: 'Darpan',
    17: 'Regular'
}

for record in font['name'].names:
    if record.nameID == 0:
        old_text = record.toUnicode()
        if 'Modified version' not in old_text:
            new_text = old_text + ' Modified version. Original by Catherine Leigh Schmidt.'
            record.string = new_text.encode('utf-16-be') if record.platformID == 3 else new_text.encode('mac-roman')
    elif record.nameID in name_dict:
        new_text = name_dict[record.nameID]
        if new_text == '':
            record.string = b''
        else:
            record.string = new_text.encode('utf-16-be') if record.platformID == 3 else new_text.encode('mac-roman')

# Get some glyph names to figure out how devanagari is named
deva_glyphs = [g for g in font.getGlyphOrder() if 'deva' in g.lower()]
print(f"Found {len(deva_glyphs)} deva glyphs.")
# Just print a few to see the naming convention
print("Sample deva glyphs:", deva_glyphs[:20])

# Also check GSUB features
gsub = font['GSUB'].table
features = gsub.FeatureList.FeatureRecord
print("Existing features:")
for f in features:
    print(f.FeatureTag)

# Look for 'pres' lookups
pres_lookups = []
for f in features:
    if f.FeatureTag == 'pres':
        pres_lookups.extend(f.Feature.LookupListIndex)
print("PRES Lookups indices:", pres_lookups)

# For now, let's just save without cjct to test
font.save(out_ttf)
font.flavor = 'woff2'
font.save(out_woff2)
print("Saved modified fonts temporarily.")
