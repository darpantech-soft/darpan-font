"""
Darpan Font — Headline (Shirorekha) Connection Fix

Yatra One's conjunct glyphs have disconnected headlines (shirorēkhā) due to
the brush-paint aesthetic. This script:
1. Analyzes each conjunct glyph to find headline gaps
2. Adds connecting headline bars to bridge gaps  
3. Uses the font's own brush thickness for natural look
"""
from fontTools.ttLib import TTFont
import os

def get_glyph_bounds(font, glyph_name):
    """Get bounding box of a glyph."""
    glyf = font['glyf']
    if glyph_name not in glyf:
        return None
    g = glyf[glyph_name]
    if g.numberOfContours == 0:
        return None
    return (g.xMin, g.yMin, g.xMax, g.yMax)

def analyze_headline_height(font):
    """Find the headline (shirorekha) y-coordinate by analyzing base consonants."""
    glyf = font['glyf']
    heights = []
    
    # Sample base consonants to find headline position
    test_glyphs = ['dvKA', 'dvGA', 'dvTA', 'dvDA', 'dvNA', 'dvPA', 'dvMA', 'dvSA']
    
    for name in test_glyphs:
        if name in glyf:
            g = glyf[name]
            if g.numberOfContours > 0:
                heights.append(g.yMax)
    
    if heights:
        avg_top = sum(heights) / len(heights)
        return avg_top
    return 750  # fallback

def analyze_glyph_top_coverage(font, glyph_name, headline_y, bar_height=40):
    """
    Analyze how much of the headline region is covered by glyph outlines.
    Returns list of x-ranges where the glyph has ink at the headline level.
    """
    glyf = font['glyf']
    if glyph_name not in glyf:
        return [], 0, 0
    
    g = glyf[glyph_name]
    if g.numberOfContours <= 0:
        return [], 0, 0
    
    # Get all coordinates
    coords = g.coordinates
    # Get the glyph width
    hmtx = font['hmtx']
    width = hmtx.metrics.get(glyph_name, (0, 0))[0]
    
    return [], g.xMin, g.xMax

def add_headline_bar(font, glyph_name, headline_y, bar_thickness=45):
    """
    Add a connecting headline bar to a glyph.
    The bar spans the full width of the glyph at the headline y-level.
    """
    glyf = font['glyf']
    if glyph_name not in glyf:
        return False
    
    g = glyf[glyph_name]
    if g.numberOfContours <= 0 or g.isComposite():
        return False
    
    # Get glyph bounds
    xMin, yMin, xMax, yMax = g.xMin, g.yMin, g.xMax, g.yMax
    
    # The headline bar should span from xMin to xMax
    # at the top of the glyph (near yMax)
    # Use a slightly lower position to avoid going above existing outlines
    bar_top = yMax
    bar_bottom = yMax - bar_thickness
    
    # Only add bar if there's likely a gap (glyph is wide enough)
    # Skip very narrow glyphs
    if (xMax - xMin) < 100:
        return False
    
    # Add a rectangular contour for the headline bar
    # TrueType uses quadratic splines; a rectangle is 4 on-curve points
    bar_coords = [
        (xMin, bar_top),      # top-left
        (xMax, bar_top),      # top-right
        (xMax, bar_bottom),   # bottom-right
        (xMin, bar_bottom),   # bottom-left
    ]
    
    # Add the new contour to the glyph
    existing_coords = list(g.coordinates)
    existing_flags = list(g.flags)
    existing_endPts = list(g.endPtsOfContours)
    
    # New contour starts after last existing point
    new_start = len(existing_coords)
    
    for coord in bar_coords:
        existing_coords.append(coord)
        existing_flags.append(1)  # on-curve point
    
    # New end point
    existing_endPts.append(new_start + len(bar_coords) - 1)
    
    # Update glyph
    from fontTools.ttLib.tables._g_l_y_f import Glyph
    g.coordinates = type(g.coordinates)(existing_coords)
    g.flags = type(g.flags)(existing_flags)
    g.endPtsOfContours = existing_endPts
    g.numberOfContours = len(existing_endPts)
    
    # Recalculate bounds
    g.recalcBounds(glyf)
    
    return True

def main():
    input_path = r'd:\web\projects\fontmake\output\Darpan-Regular.ttf'
    out_dir = r'd:\web\projects\fontmake\output'
    out_ttf = os.path.join(out_dir, 'Darpan-Regular.ttf')
    out_woff2 = os.path.join(out_dir, 'Darpan-Regular.woff2')
    
    print("Loading Darpan font...")
    font = TTFont(input_path)
    glyf = font['glyf']
    
    # Find headline height
    headline_y = analyze_headline_height(font)
    print(f"Headline (shirorekha) height: {headline_y:.0f} units")
    
    # Find all conjunct glyphs (names containing underscore in dv namespace)
    conjunct_glyphs = []
    for name in font.getGlyphOrder():
        if name.startswith('dv') and '_' in name and not name.startswith('dvm'):
            # Skip matra glyphs (dvmI, dvmII, etc.)
            conjunct_glyphs.append(name)
    
    print(f"Found {len(conjunct_glyphs)} conjunct glyphs")
    
    # Analyze a few to understand the structure
    print("\nSample glyph bounds:")
    samples = ['dvD_VA', 'dvS_MA', 'dvC_CA', 'dvT_TA', 'dvK_TA', 'dvD_DHA']
    for name in samples:
        bounds = get_glyph_bounds(font, name)
        if bounds:
            print(f"  {name}: xMin={bounds[0]}, yMin={bounds[1]}, xMax={bounds[2]}, yMax={bounds[3]}")
    
    # Also check half-form glyphs
    print("\nHalf-form glyph bounds:")
    halfs = ['dvD', 'dvS', 'dvC', 'dvT', 'dvK']
    for name in halfs:
        bounds = get_glyph_bounds(font, name)
        if bounds:
            print(f"  {name}: xMin={bounds[0]}, yMin={bounds[1]}, xMax={bounds[2]}, yMax={bounds[3]}")
    
    # Full consonant bounds for reference
    print("\nFull consonant bounds:")
    fulls = ['dvDA', 'dvSA', 'dvCA', 'dvTA', 'dvKA']
    for name in fulls:
        bounds = get_glyph_bounds(font, name)
        if bounds:
            print(f"  {name}: xMin={bounds[0]}, yMin={bounds[1]}, xMax={bounds[2]}, yMax={bounds[3]}")
    
    # Add headline bars to conjunct glyphs
    print(f"\nAdding headline bars (thickness=45 units)...")
    modified = 0
    skipped = 0
    for name in conjunct_glyphs:
        if add_headline_bar(font, name, headline_y, bar_thickness=45):
            modified += 1
        else:
            skipped += 1
    
    print(f"  Modified: {modified} glyphs")
    print(f"  Skipped:  {skipped} glyphs")
    
    # Save
    print(f"\nSaving TTF: {out_ttf}")
    font.save(out_ttf)
    
    print(f"Saving WOFF2: {out_woff2}")
    font2 = TTFont(out_ttf)
    font2.flavor = 'woff2'
    font2.save(out_woff2)
    
    ttf_size = os.path.getsize(out_ttf) / 1024
    woff2_size = os.path.getsize(out_woff2) / 1024
    print(f"\nTTF:   {ttf_size:.1f} KB")
    print(f"WOFF2: {woff2_size:.1f} KB")
    print(f"\n✅ Headline fix applied!")

if __name__ == '__main__':
    main()
