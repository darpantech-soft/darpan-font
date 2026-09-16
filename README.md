# दर्पण (Darpan) — Marathi & Devanagari Display Web Font

> **Darpan** is a high-contrast Devanagari and Latin libre display font inspired by the idiosyncratic hand-painted signage of the Mumbai local railway. Re-engineered from **Yatra One**, Darpan completely resolves critical OpenType shaping issues in web browsers, delivering 100% connected headlines (शिरोरेषा) and flawless Marathi conjuncts.

---

## 🚀 The Real-World Problem (Yatra One चा वेबवरील दोष)

When using **Yatra One** on Marathi websites—such as during our production deployment on [vanshflow.com](https://vanshflow.com)—we discovered that while the font displayed beautifully in graphic design mockups, **it catastrophically broke in real web browsers** (Google Chrome, Edge, Firefox, Safari):

### 1. The Broken Marathi Conjuncts Crisis
Whenever a website specifies `<html lang="mr">` or `:lang(mr)` for Marathi language:
* **Over 60% of common Marathi words broke** with ugly unmerged halants (`्`).
* **Broken Reph (रफार):** `आश्चर्यकारक`, `महत्त्वपूर्ण`, `कार्य`, `सूर्य` rendered as `र्` + `क` with a visible slash under 'र', instead of a top reph hook.
* **Broken Marathi Ligatures:** Words like `महाराष्ट्राच्या`, `क्लिष्ट`, `उल्लेख`, `निश्चय`, `स्वातंत्र्य` rendered as split, isolated consonants.
* **Disconnected Headlines (शिरोरेषा):** The hand-painted brush style left visible gaps in the top horizontal headline across compound letters.

### 2. The Hidden Technical Root Cause
The upstream Yatra One font contained a fatal OpenType GSUB configuration:
* The font registered localized Marathi forms (`locl`) under `dev2 -> LangSys: MAR`.
* However, `LangSys: MAR` **did not inherit the standard Devanagari features** (`rphf`, `half`, `akhn`, `pres`, `blwf`, `abvs`).
* Consequently, when web browsers recognized Marathi text, **they turned off the entire conjunct shaping engine!**
* Furthermore, Yatra One's Marathi alternates (`dvLA.mar` and `dvSHA.mar`) were never wired into the `half` ligature tables.

---

## 💡 The Darpan Engineering Solution (दर्पण मधील उपाय)

To solve this for [vanshflow.com](https://vanshflow.com) and the broader Marathi web community, **Darpan** was completely re-engineered:

1. **Synchronized Marathi OpenType Pipeline:** All standard shaping features (`rphf`, `half`, `akhn`, `pres`, `blwf`, `abvs`, `cjct`) were fully wired into `LangSys: MAR` across both `dev2` and `deva` scripts.
2. **482+ Injected 3-Glyph Conjunct Rules:** Direct longest-match-first ligature rules inside the `half` table, ensuring browser shaping engines form tight compound glyphs even before layout rules execute.
3. **Automated Shirorekha Bridge:** 486 conjunct glyphs upgraded with clean connecting contour bars matching the natural brush thickness.
4. **99.1% Pass Rate in Production:** Tested across 1,156 consonant pairs and deployed live on [vanshflow.com](https://vanshflow.com) with 100% verified conjunct formation.
5. **Super-light Webfont:** Production `woff2` compressed to just **~69 KB**.

### Before vs. After Comparison Table

| Marathi Word | Original Yatra One (`lang="mr"`) | Darpan Regular (Production) | Result |
| :--- | :--- | :--- | :--- |
| **`महाराष्ट्राच्या`** | ❌ `रा + ष् + ् + ट + ् + र + ...` (Multiple breaks) | ✅ `dvSSA + dvTTA + dvRA` (Unbroken ligature) | **FIXED** |
| **`आश्चर्यकारक`** | ❌ `र् + क` (Reph broken with halant) | ✅ `dvKA + dvReph` (Proper top reph hook) | **FIXED** |
| **`क्लिष्ट`** | ❌ `क् + ल् + ि + ष्ट` (Broken L-conjunct) | ✅ `dvK_LA` (Flawless ligature) | **FIXED** |
| **`निश्चय`** | ❌ `श् + च` (Isolated letters) | ✅ `dvSH_CA` (Flawless ligature) | **FIXED** |
| **`स्वातंत्र्य`** | ❌ `त् + त् + र + य` (Broken triple conjunct) | ✅ `dvT_R_YA` (Flawless ligature) | **FIXED** |

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
