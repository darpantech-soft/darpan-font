# Technical Report: Resolving Devanagari & Marathi Shaping Failures in Yatra One

**Project:** Darpan Font  
**Authors:** Tanaji Padwal (DARPAN TECHNOLOGIES, Pune, Maharashtra, India)  
**Production Case Study:** Deployed on [vanshflow.com](https://vanshflow.com)  
**Date:** September 2026  
**License:** SIL Open Font License, Version 1.1  

---

## 1. Executive Summary

When deploying Google Fonts' **Yatra One** on Marathi websites—specifically during real-world production at [vanshflow.com](https://vanshflow.com)—we observed an immediate, catastrophic breakdown of Devanagari conjunct shaping. Words like `महाराष्ट्राच्या`, `आश्चर्यकारक`, `महत्त्वपूर्ण`, `क्लिष्ट`, `उल्लेख`, and `निश्चय` failed to form ligatures in Chromium and WebKit browsers, rendering with unsightly exposed viramas (`्`).

This technical report details:
1. The root cause in the upstream OpenType GSUB `LangSys: MAR` table.
2. The mechanical failure of Reph (`rphf`) and 3-glyph ligature shaping.
3. The geometric disconnection of compound headlines (शिरोरेषा).
4. The engineering solution implemented in **Darpan**.
5. Live production verification and test metrics.

---

## 2. Root Cause Analysis

### 2.1 The OpenType `LangSys: MAR` Omission
The OpenType specification defines `LangSys` records within scripts (e.g., `dev2`, `deva`). If a `LangSys` is explicitly declared, it must register all feature lookups it supports; otherwise, the shaper disables unregistered features for that language.

In upstream **Yatra One**, the Adobe Feature File (`family.fea`) contained:
```fea
feature locl {
  script dev2;
  language MAR;
    sub dvSHA by dvSHA.mar;
    sub dvLA by dvLA.mar;
} locl;
```
Because `languagesystem dev2 MAR;` was not declared at the top level of the feature file, FontTools / feaLib created a standalone `LangSysRecord` for `MAR` containing **ONLY** `['locl']`.

**Result:** Whenever a web page declared `<html lang="mr">` or used CSS `:lang(mr)`:
* `rphf` (Reph) was disabled $\longrightarrow$ All 22+ Reph conjuncts broke (`र्क` $\rightarrow$ `र्` + `क`).
* `half` (Half-forms) was disabled $\longrightarrow$ Consonants failed to join (`क्` + `ल`).
* `pres` (Pre-base) was disabled $\longrightarrow$ Compound ligatures failed.
* `blwf` & `abvs` were disabled.

### 2.2 Unmapped Marathi Alternates (`.mar`)
Yatra One provided localized glyphs `dvLA.mar` (Marathi 'ल') and `dvSHA.mar` (Marathi looped 'श'). However:
* `dvLA.mar` had no rule in the `half` table (`dvLA.mar + dvVirama -> dvL`).
* No 3-glyph ligature rules existed for `.mar` components (e.g., `dvKA + dvVirama + dvLA.mar -> dvK_LA`).
* Consequently, even if `half` fired, words containing Marathi 'ल' or 'श' broke into loose glyphs with viramas.

### 2.3 Headline (Shirorekha) Gaps
Yatra One's brush-painted aesthetic left gaps in the top horizontal shirorekha bar across compound glyphs. When conjuncts were displayed at headline sizes, the headline appeared fractured.

---

## 3. The Darpan Engineering Solution

### 3.1 Synchronizing `LangSys: MAR`
In `scripts/build_darpan.py`, we iterate over all script records (`DFLT`, `dev2`, `deva`) and merge all feature indices from `DefaultLangSys` into every `LangSysRecord` (including `MAR`):
```python
for lr in sr.Script.LangSysRecord:
    combined = list(lr.LangSys.FeatureIndex)
    for fi in dflt_features:
        if fi not in combined:
            combined.append(fi)
    lr.LangSys.FeatureIndex = combined
```

### 3.2 Injected 482 3-Glyph Conjunct Rules
To bypass browser shaper ordering limitations, we converted all 2-glyph pre-base rules into explicit 3-glyph ligature rules:
$$\text{dvKA} + \text{dvVirama} + \text{dvLA} \longrightarrow \text{dvK\_LA}$$
$$\text{dvKA} + \text{dvVirama} + \text{dvLA.mar} \longrightarrow \text{dvK\_LA}$$
$$\text{dvLA.mar} + \text{dvVirama} \longrightarrow \text{dvL}$$
$$\text{dvSHA.mar} + \text{dvVirama} \longrightarrow \text{dvSH}$$

These rules are injected into the **`half`** feature with **longest-match-first** sorting. When HarfBuzz or DirectWrite encounters `KA + Virama + LA`, it immediately forms `dvK_LA` before individual half-forms can separate.

### 3.3 Automated Shirorekha Bridge
Using font geometry analysis, we compute the average `yMax` of base consonants (~619 units) and programmatically append 45-unit rectangular contours across 486 conjunct glyphs, producing unbroken headlines.

---

## 4. Empirical Test Results

### 4.1 Exhaustive Consonant Pair Test
We tested all $34 \times 34 = 1,156$ possible Devanagari consonant pairs ($C_1 + \text{virama} + C_2$) using `uharfbuzz` with `language="mr"`:
* **Yatra One:** 60%+ failures with visible halants.
* **Darpan Regular:** **0 failures out of 1,156 pairs (100% joined).**

### 4.2 Production Passage Test (107 Words)
Tested on a comprehensive Marathi text containing all conjunct categories:
* **Yatra One:** 65 words broken (60.7% failure rate).
* **Darpan Regular:** 106 words unbroken (**99.1% success rate**). The only unmerged cluster was the extreme 5-consonant Sanskrit cluster `कार्त्स्न्य`.

---

## 5. Live Deployment

Darpan is deployed live in production on:
* **Website:** [vanshflow.com](https://vanshflow.com)
* **Status:** Verified flawless rendering in Chrome, Edge, Safari, and Firefox.
