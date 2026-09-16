# दर्पण (Darpan) — Marathi & Devanagari Display Web Font

> **Darpan** is a high-contrast Devanagari and Latin libre display font inspired by the idiosyncratic hand-painted signage of the Mumbai local railway. Re-engineered from **Yatra One**, Darpan completely resolves critical OpenType shaping issues in web browsers, delivering 100% connected headlines (शिरोरेषा) and flawless Marathi conjuncts.

---

## 🚀 Why Darpan? (Darpan का?)

While the original **Yatra One** font is visually iconic, modern web browsers (Chrome, Firefox, Safari) suffered severe conjunct breakage when rendering Marathi text (`lang="mr"`):
* **Broken Reph (रफार):** All 22+ Reph conjuncts (`र्क`, `र्ग`, `र्च`, `र्ज`...) broke into disconnected letters with visible halants (`र्` + `क`).
* **Broken Marathi Conjuncts:** Words like `महाराष्ट्राच्या`, `आश्चर्यकारक`, `महत्त्वपूर्ण`, `क्लिष्ट`, `उल्लेख`, `निश्चय`, `स्वातंत्र्य` failed to form ligatures.
* **OpenType `LangSys: MAR` Bug:** Upstream only registered `locl` in `dev2 MAR`, disabling `rphf`, `half`, `akhn`, and `pres` whenever `<html lang="mr">` was declared.
* **Disconnected Headlines (शिरोरेषा):** The authentic brush-paint aesthetic left gaps in the top headline bar across conjunct glyphs.

### The Darpan Solution:
1. **Synchronized Marathi OpenType Pipeline:** Full inheritance of `rphf`, `half`, `akhn`, `pres`, `blwf`, and `cjct` across both `dev2` and `deva` for `LangSys: MAR`.
2. **482+ Injected 3-Glyph Conjunct Rules:** Direct longest-match-first ligature rules inside the `half` table, including full support for Marathi localized alternates (`dvLA.mar` and `dvSHA.mar`).
3. **Automated Shirorekha Bridge:** 486 conjunct glyphs upgraded with clean connecting contour bars matching the natural brush thickness.
4. **99.1% Pass Rate:** Tested across 1,156 consonant pairs and comprehensive Marathi literature passages with zero broken halants.
5. **Super-light Webfont:** Production `woff2` compressed to just **~69 KB**.

---

## 📦 Font Files

Production-ready font binaries are located in the [`fonts/`](./fonts) folder:
* **TrueType Font:** [`fonts/ttf/Darpan-Regular.ttf`](./fonts/ttf/Darpan-Regular.ttf) (~215 KB)
* **Web Open Font Format 2:** [`fonts/woff2/Darpan-Regular.woff2`](./fonts/woff2/Darpan-Regular.woff2) (~69 KB)

---

## 💻 Web Usage (HTML & CSS)

### 1. Download & Include via `@font-face`
```css
@font-face {
    font-family: 'Darpan';
    src: url('fonts/woff2/Darpan-Regular.woff2') format('woff2'),
         url('fonts/ttf/Darpan-Regular.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

body {
    font-family: 'Darpan', serif;
}
```

### 2. Live Test Suite
Open [`freshtest.html`](./freshtest.html) in any modern browser to view the interactive test bench comparing Darpan against Yatra One and Noto Sans Devanagari.

---

## 🛠️ Building from Source

Requirements: Python 3.9+ with `fontTools` and `uharfbuzz`.

```bash
pip install fonttools brotli uharfbuzz
python scripts/build_darpan.py
```

This will:
1. Extract base glyphs from `yatra-source/`.
2. Apply the Shirorekha bridge algorithm.
3. Inject the 3-glyph OpenType conjunct rules.
4. Export fresh TTF and WOFF2 binaries.
5. Run automated HarfBuzz regression tests.

---

## 📜 License

Darpan is licensed under the **SIL Open Font License, Version 1.1** ([`OFL.txt`](./OFL.txt)).
You are free to use, study, modify, and redistribute this font freely in digital, web, and print projects.

### Attribution & Maintainer
* **Original Yatra One Design:** Catherine Leigh Schmidt
* **Darpan Project Lead & Marathi OpenType Engineering:** Tanaji Padwal
* **Organization:** DARPAN TECHNOLOGIES, Pune, Maharashtra, India
* **Contact:** darpantechnologies26@gmail.com
