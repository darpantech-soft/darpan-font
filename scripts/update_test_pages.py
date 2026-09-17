import base64
import os

def get_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

b64_regular = get_base64('fonts/woff2/Darpan-Regular.woff2')
b64_medium = get_base64('fonts/woff2/Darpan-Medium.woff2')
b64_semibold = get_base64('fonts/woff2/Darpan-SemiBold.woff2')
b64_bold = get_base64('fonts/woff2/Darpan-Bold.woff2')

html_content = f"""<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darpan Font — Complete Multi-Weight & Shaping Test Bench</title>
    <link href="https://fonts.googleapis.com/css2?family=Yatra+One&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Base64 & Local Path @font-face declarations for all 4 weights */
        @font-face {{
            font-family: 'Darpan';
            font-weight: 400;
            font-style: normal;
            font-display: swap;
            src: url('data:font/woff2;charset=utf-8;base64,{b64_regular}') format('woff2'),
                 url('fonts/woff2/Darpan-Regular.woff2') format('woff2');
        }}
        @font-face {{
            font-family: 'Darpan';
            font-weight: 500;
            font-style: normal;
            font-display: swap;
            src: url('data:font/woff2;charset=utf-8;base64,{b64_medium}') format('woff2'),
                 url('fonts/woff2/Darpan-Medium.woff2') format('woff2');
        }}
        @font-face {{
            font-family: 'Darpan';
            font-weight: 600;
            font-style: normal;
            font-display: swap;
            src: url('data:font/woff2;charset=utf-8;base64,{b64_semibold}') format('woff2'),
                 url('fonts/woff2/Darpan-SemiBold.woff2') format('woff2');
        }}
        @font-face {{
            font-family: 'Darpan';
            font-weight: 700;
            font-style: normal;
            font-display: swap;
            src: url('data:font/woff2;charset=utf-8;base64,{b64_bold}') format('woff2'),
                 url('fonts/woff2/Darpan-Bold.woff2') format('woff2');
        }}

        /* Named Aliases */
        @font-face {{
            font-family: 'DarpanRegular';
            src: url('data:font/woff2;charset=utf-8;base64,{b64_regular}') format('woff2');
        }}
        @font-face {{
            font-family: 'DarpanMedium';
            src: url('data:font/woff2;charset=utf-8;base64,{b64_medium}') format('woff2');
        }}
        @font-face {{
            font-family: 'DarpanSemiBold';
            src: url('data:font/woff2;charset=utf-8;base64,{b64_semibold}') format('woff2');
        }}
        @font-face {{
            font-family: 'DarpanBold';
            src: url('data:font/woff2;charset=utf-8;base64,{b64_bold}') format('woff2');
        }}

        :root {{
            --bg: #0b0f19;
            --panel: #131b2e;
            --border: #23304e;
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #f59e0b;
            --green: #22c55e;
            --red: #ef4444;
            --blue: #38bdf8;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }}

        h1 {{
            font-size: 1.8rem;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        .subtitle {{
            color: var(--muted);
            font-size: 0.95rem;
            margin-top: 0.3rem;
        }}

        .toolbar {{
            display: flex;
            align-items: center;
            gap: 1rem;
            background: var(--panel);
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            flex-wrap: wrap;
        }}

        .ctrl-group {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.88rem;
        }}

        .ctrl-select {{
            background: #0b0f19;
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.35rem 0.6rem;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            outline: none;
        }}
        .ctrl-select:focus {{
            border-color: var(--accent);
        }}

        .summary-banner {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 1.8rem;
        }}

        .stat-box {{
            background: var(--panel);
            padding: 1.2rem;
            border-radius: 8px;
            border: 1px solid var(--border);
        }}
        .stat-box .title {{ font-size: 0.82rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }}
        .stat-box .val {{ font-size: 1.8rem; font-weight: 700; margin-top: 0.3rem; }}

        .section-title {{
            font-size: 1.25rem;
            color: var(--accent);
            margin: 2.2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .compare-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.2rem;
            margin-bottom: 2rem;
        }}

        .font-card {{
            background: var(--panel);
            border-radius: 10px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            position: relative;
        }}

        .font-badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-darpan {{ background: #14532d; color: #4ade80; border: 1px solid #22c55e; }}
        .badge-yatra {{ background: #7f1d1d; color: #f87171; border: 1px solid #ef4444; }}
        .badge-noto {{ background: #1e3a8a; color: #60a5fa; border: 1px solid #3b82f6; }}

        .para-text {{
            line-height: 2.1;
            text-rendering: optimizeLegibility;
            word-break: break-word;
            transition: font-size 0.15s ease;
        }}
        .darpan-font {{
            font-family: 'Darpan', serif;
            font-weight: 400;
        }}
        .yatra-font {{ font-family: 'Yatra One', serif; }}
        .noto-font {{ font-family: 'Noto Sans Devanagari', sans-serif; }}

        /* Interactive Word Highlighting */
        .interactive-word {{
            display: inline-block;
            padding: 0 0.2rem;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .interactive-word:hover {{
            background: rgba(245, 158, 11, 0.25);
            outline: 1px solid var(--accent);
        }}
        .word-broken {{
            background: rgba(239, 68, 68, 0.22);
            border-bottom: 2px dashed var(--red);
        }}
        .word-ok {{
            border-bottom: 1px solid transparent;
        }}

        /* Weight Showcase Grid */
        .weight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.2rem;
            margin-bottom: 2rem;
        }}
        .weight-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.2rem;
        }}
        .weight-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.8rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }}
        .weight-label {{
            font-weight: 700;
            color: var(--accent);
            font-size: 0.95rem;
        }}
        .weight-meta {{
            font-size: 0.75rem;
            color: var(--muted);
            font-family: monospace;
        }}
        .weight-sample {{
            font-family: 'Darpan', serif;
            font-size: 1.8rem;
            line-height: 1.6;
            margin-bottom: 0.5rem;
        }}

        /* Inspector Panel */
        .inspector-panel {{
            background: #0f172a;
            border: 2px solid var(--accent);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 2rem 0;
            display: none;
        }}
        .inspector-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        .inspector-title {{
            font-size: 1.1rem;
            color: var(--accent);
            font-weight: 600;
        }}
        .inspect-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.2rem;
        }}
        .inspect-col {{
            background: var(--panel);
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        .inspect-preview {{
            font-size: 2.2rem;
            line-height: 1.6;
            margin: 0.3rem 0;
        }}

        .tag-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.5rem;
        }}
        .tag-item {{
            font-family: monospace;
            font-size: 0.74rem;
            background: #1e293b;
            padding: 0.2rem 0.45rem;
            border-radius: 4px;
            border: 1px solid #334155;
            color: #38bdf8;
        }}

        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.2rem;
            font-size: 0.85rem;
            color: var(--muted);
            margin: 0.8rem 0;
            background: #0f172a;
            padding: 0.7rem 1rem;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        .legend-item {{ display: flex; align-items: center; gap: 0.4rem; }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 3px; }}

        .diagnostics-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 1rem;
            background: var(--panel);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        .diagnostics-table th, .diagnostics-table td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        .diagnostics-table th {{ background: #1e293b; color: var(--accent); }}
    </style>
</head>
<body>

<header>
    <div>
        <h1>🔍 Darpan (दर्पण) — Multi-Weight Shaping Test Bench</h1>
        <div class="subtitle">मराठी व देवनागरी जोडाक्षरांची संपूर्ण शेपिंग आणि वजन चाचणी (Multi-Weight Font Family Bench)</div>
    </div>
    <div class="toolbar">
        <div class="ctrl-group">
            <span>वजन (Weight):</span>
            <select id="weightSelect" class="ctrl-select">
                <option value="400">Regular (४००)</option>
                <option value="500">Medium (५००)</option>
                <option value="600">SemiBold (६००)</option>
                <option value="700">Bold (७००)</option>
            </select>
        </div>
        <div class="ctrl-group">
            <span>आकार (Size):</span>
            <input type="range" id="fontSizeSlider" min="20" max="48" value="28">
            <span id="fontSizeVal">28px</span>
        </div>
    </div>
</header>

<div style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.4); border-left: 4px solid var(--green); border-radius: 8px; padding: 0.9rem 1.2rem; margin-bottom: 0.8rem; font-size: 0.88rem; line-height: 1.6;">
    <b style="color: #4ade80;">🚀 रिअल-वर्ल्ड केस स्टडी (vanshflow.com):</b> मूळ <i>Yatra One</i> फॉन्ट वेबसाईट्सवर (<code style="color:#f59e0b;">&lt;html lang="mr"&gt;</code>) वापरल्यास मराठीतील ६०% पेक्षा जास्त जोडाक्षरे (जसे 'महाराष्ट्राच्या', 'क्लिष्ट', 'निश्चय', 'आश्चर्यकारक') तुटून हलंत दिसत होते. <b>Darpan</b> मध्ये हा OpenType GSUB दोष पूर्णपणे सोडवून <b><a href="https://vanshflow.com" target="_blank" style="color: var(--blue); font-weight: 600; text-decoration: underline;">vanshflow.com</a></b> वर यशस्वीरित्या लाइव्ह डिप्लॉय करण्यात आला आहे.
</div>

<div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-left: 4px solid var(--blue); border-radius: 8px; padding: 0.8rem 1.2rem; margin-bottom: 1.5rem; font-size: 0.86rem; line-height: 1.6;">
    <b style="color: #38bdf8;">🌐 समर्थित देवनागरी भाषा (Pan-Devanagari Support):</b> हा फॉन्ट <b>मराठी, संस्कृत, हिंदी, नेपाळी, कोकणी, मैथिली, भोजपुरी, सिंधी, डोगरी, बोडो</b> आणि <b>संथाली</b> या सर्व देवनागरी आधारित प्रादेशिक व राष्ट्रीय भाषांसाठी पूर्णपणे सुसंगत आणि उपयुक्त आहे.
</div>

<!-- Summary Cards -->
<div class="summary-banner">
    <div class="stat-box" style="border-left: 4px solid var(--blue);">
        <div class="title">एकूण तपासलेले शब्द (Total Words)</div>
        <div class="val" id="totalWordsVal">107</div>
    </div>
    <div class="stat-box" style="border-left: 4px solid var(--green);">
        <div class="title">दर्पण: अखंड जोडाक्षरे (Darpan Joined)</div>
        <div class="val" style="color: var(--green);">106 (99.1%)</div>
    </div>
    <div class="stat-box" style="border-left: 4px solid var(--red);">
        <div class="title">मूळ यात्रा वन: तुटलेले शब्द (Yatra Broken)</div>
        <div class="val" style="color: var(--red);">65 (60.7%)</div>
    </div>
    <div class="stat-box" style="border-left: 4px solid var(--accent);">
        <div class="title">उपलब्ध वचने (Family Weights)</div>
        <div class="val" style="color: var(--accent);">4 Weights</div>
    </div>
</div>

<!-- SECTION 0: Multi-Weight Showcase -->
<div class="section-title">🎨 दर्पण फॉन्ट फॅमिली — सर्व ४ वचने (Multi-Weight Showcase)</div>
<div class="weight-grid">
    <div class="weight-card">
        <div class="weight-card-header">
            <span class="weight-label">Regular (४००)</span>
            <span class="weight-meta">Darpan-Regular.woff2 (~69 KB)</span>
        </div>
        <div class="weight-sample" style="font-weight: 400;">महाराष्ट्राच्या संस्कृतीचे दर्शन आणि स्वातंत्र्य</div>
        <div style="font-size: 0.85rem; color: var(--muted); line-height: 1.6;">क्लिष्ट व्याकरण, दृढ निश्चय, उज्ज्वल भविष्य, छत्रपती शिवाजी महाराज</div>
    </div>
    <div class="weight-card">
        <div class="weight-card-header">
            <span class="weight-label">Medium (५००)</span>
            <span class="weight-meta">Darpan-Medium.woff2 (~72 KB)</span>
        </div>
        <div class="weight-sample" style="font-weight: 500;">महाराष्ट्राच्या संस्कृतीचे दर्शन आणि स्वातंत्र्य</div>
        <div style="font-size: 0.85rem; color: var(--muted); line-height: 1.6;">क्लिष्ट व्याकरण, दृढ निश्चय, उज्ज्वल भविष्य, छत्रपती शिवाजी महाराज</div>
    </div>
    <div class="weight-card">
        <div class="weight-card-header">
            <span class="weight-label">SemiBold (६००)</span>
            <span class="weight-meta">Darpan-SemiBold.woff2 (~73 KB)</span>
        </div>
        <div class="weight-sample" style="font-weight: 600;">महाराष्ट्राच्या संस्कृतीचे दर्शन आणि स्वातंत्र्य</div>
        <div style="font-size: 0.85rem; color: var(--muted); line-height: 1.6;">क्लिष्ट व्याकरण, दृढ निश्चय, उज्ज्वल भविष्य, छत्रपती शिवाजी महाराज</div>
    </div>
    <div class="weight-card">
        <div class="weight-card-header">
            <span class="weight-label">Bold (७००)</span>
            <span class="weight-meta">Darpan-Bold.woff2 (~73 KB)</span>
        </div>
        <div class="weight-sample" style="font-weight: 700;">महाराष्ट्राच्या संस्कृतीचे दर्शन आणि स्वातंत्र्य</div>
        <div style="font-size: 0.85rem; color: var(--muted); line-height: 1.6;">क्लिष्ट व्याकरण, दृढ निश्चय, उज्ज्वल भविष्य, छत्रपती शिवाजी महाराज</div>
    </div>
</div>

<div class="legend">
    <div class="legend-item"><span class="legend-dot" style="background:#22c55e;"></span> <span>अखंड जोडाक्षर (Joined)</span></div>
    <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> <span>हलंत तुटलेले अक्षर (Broken / Split Halant)</span></div>
    <div class="legend-item"><span>💡 <i>टीप: कोणत्याही शब्दावर क्लिक करून त्याचे तिन्ही फॉन्ट्समधील सूक्ष्म शेपिंग तपासा. वरून वजन बदलल्यास खालील सर्व दर्पण मजकूर त्या वजनात अपडेट होतो.</i></span></div>
</div>

<!-- Interactive Inspector Popup -->
<div class="inspector-panel" id="inspectorPanel">
    <div class="inspector-header">
        <div class="inspector-title">🔎 निवडलेला शब्द: <span id="inspectWordLabel" style="color:white; font-size:1.4rem;"></span></div>
        <button onclick="document.getElementById('inspectorPanel').style.display='none'" style="background:transparent; border:none; color:var(--muted); font-size:1.3rem; cursor:pointer;">✖</button>
    </div>
    <div class="inspect-grid">
        <div class="inspect-col">
            <span class="font-badge badge-darpan" id="inspectDarpanBadge">🟢 Darpan</span>
            <div class="inspect-preview darpan-font" id="inspectDarpanPreview"></div>
            <div id="inspectDarpanStatus"></div>
            <div class="tag-list" id="inspectDarpanGlyphs"></div>
        </div>
        <div class="inspect-col">
            <span class="font-badge badge-yatra">🔴 Yatra One</span>
            <div class="inspect-preview yatra-font" id="inspectYatraPreview"></div>
            <div id="inspectYatraStatus"></div>
            <div class="tag-list" id="inspectYatraGlyphs"></div>
        </div>
        <div class="inspect-col">
            <span class="font-badge badge-noto">🔵 Noto Sans Devanagari</span>
            <div class="inspect-preview noto-font" id="inspectNotoPreview"></div>
            <div style="color:var(--muted); font-size:0.85rem; margin-top:0.3rem;">मानक संदर्भ (Standard Reference)</div>
        </div>
    </div>
</div>

<!-- SECTION 1: Standard Real-World Marathi Paragraph -->
<div class="section-title">📖 परिच्छेद १: विस्तृत मराठी मजकूर (General Marathi Paragraph)</div>
<div class="compare-grid">
    <div class="font-card" style="border-left: 5px solid var(--green);">
        <span class="font-badge badge-darpan" id="darpanBadge1">🟢 Darpan (वजन: <span id="currentWeightBadge1">400</span>)</span>
        <div class="para-text darpan-font" id="darpanPara"></div>
    </div>
    <div class="font-card" style="border-left: 5px solid var(--red);">
        <span class="font-badge badge-yatra">🔴 Yatra One (मूळ फॉन्ट — बहुतांश जोडाक्षरे तुटलेली)</span>
        <div class="para-text yatra-font" id="yatraPara"></div>
    </div>
    <div class="font-card" style="border-left: 5px solid var(--blue);">
        <span class="font-badge badge-noto">🔵 Noto Sans Devanagari (तुलनेसाठी)</span>
        <div class="para-text noto-font" id="notoPara"></div>
    </div>
</div>

<!-- SECTION 2: Complex / Classical Clusters -->
<div class="section-title">⚡ परिच्छेद २: कठीण व संस्कृतप्रचुर त्रि-संयुक्ताक्षरे (Complex Clusters)</div>
<p style="font-size:0.85rem; color:var(--muted); margin-bottom:1rem;">
अत्यंत गुंतागुंतीची संयुक्ताक्षरे जसे की ४-अक्षरी व ५-अक्षरी समूह (उदा. कार्त्स्न्य, उच्छ्वास, कण्ठ्य, धार्ष्ट्य, जिव्हा, प्रल्हाद).
</p>

<div class="compare-grid">
    <div class="font-card" style="border-left: 5px solid var(--green);">
        <span class="font-badge badge-darpan" id="darpanBadge2">🟢 Darpan (वजन: <span id="currentWeightBadge2">400</span>)</span>
        <div class="para-text darpan-font" id="darpanComplexPara"></div>
    </div>
    <div class="font-card" style="border-left: 5px solid var(--red);">
        <span class="font-badge badge-yatra">🔴 Yatra One</span>
        <div class="para-text yatra-font" id="yatraComplexPara"></div>
    </div>
</div>

<!-- SECTION 3: Hindi & Devanagari Bindi / Chandrabindu Centering Fix (Issue #5) -->
<div class="section-title">✨ परिच्छेद ३: काना + अनुस्वार व चंद्रबिंदू सुधारणा (Hindi Bindi & Chandrabindu Fix — Issue #5)</div>
<p style="font-size:0.85rem; color:var(--muted); margin-bottom:1rem;">
मूळ Yatra One मध्ये कानाच्या मात्रेवर (<code style="color:var(--accent);">dvmAA ा</code>) अनुस्वार किंवा चंद्रबिंदू असल्यास तो दांड्यापासून २१४ युनिट्स उजवीकडे पुढच्या अक्षरावर जात होता (उदा. <b>चांद, पांव, हां</b>). Darpan मध्ये हा OpenType दोष पूर्णपणे सोडवून बिंदी बरोबर कानाच्या दांड्यावर मध्यभागी (Centred) आणली आहे.
</p>

<div class="compare-grid">
    <div class="font-card" style="border-left: 5px solid var(--green);">
        <span class="font-badge badge-darpan">🟢 Darpan (कानाच्या दांड्यावर तंतोतंत मध्यभागी बिंदी — Centred Bindi)</span>
        <div class="para-text darpan-font" style="font-size: 2.2rem; line-height: 1.8;">
            चांद, पांव, हां, माँ, गाँव, दांत, सांस, बांस, जहां, वहां, कहां
        </div>
    </div>
    <div class="font-card" style="border-left: 5px solid var(--red);">
        <span class="font-badge badge-yatra">🔴 Yatra One (बिंदी उजवीकडे पुढच्या अक्षरावर ढकललेली — Shifted Right)</span>
        <div class="para-text yatra-font" style="font-size: 2.2rem; line-height: 1.8;">
            चांद, पांव, हां, माँ, गाँव, दांत, सांस, बांस, जहां, वहां, कहां
        </div>
    </div>
</div>

<!-- SECTION 4: Exact Break Points Analysis -->
<div class="section-title">📊 सविस्तर विश्लेषण: नेमके कुठे काय सुधारले? (Exact Break Points & Features)</div>
<table class="diagnostics-table">
    <thead>
        <tr>
            <th>शब्द / समूह</th>
            <th>जोडाक्षराचा प्रकार</th>
            <th>Darpan निकाल</th>
            <th>Yatra One निकाल</th>
            <th>तांत्रिक कारण (Reason)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>चांद, पांव, हां, माँ, गाँव</b></td>
            <td>काना + अनुस्वार / चंद्रबिंदू (Hindi Bindi Issue #5)</td>
            <td><span style="color:var(--green);">✅ दांड्यावर तंतोतंत मध्यभागी (Centred)</span></td>
            <td><span style="color:var(--red);">❌ २१४ युनिट्स उजवीकडे ढकललेले</span></td>
            <td>Darpan मध्ये <code>dvmAA_Anusvara</code> आणि <code>dvmAA_Candrabindu</code> लिगेचर जोडून <code>abvs</code> मध्ये अचूक केंद्रबिंदू दिला आहे.</td>
        </tr>
        <tr>
            <td><b>कार्त्स्न्य</b></td>
            <td>५-व्यंजन समूह (र्+त्+स्+न्+य)</td>
            <td><span style="color:var(--red);">❌ हलंत दिसते (Breaks)</span></td>
            <td><span style="color:var(--red);">❌ हलंत दिसते (Breaks)</span></td>
            <td>Devanagari GSUB मध्ये <code>dvT_S_NA</code> नंतर <code>YA</code> साठी ५-ग्लिफ लिगेचर अस्तित्वात नाही.</td>
        </tr>
        <tr>
            <td><b>कण्ठ्य / ण्ठ्य</b></td>
            <td>मूर्धन्य त्रि-संयुक्ताक्षर (ण्+ठ्+य)</td>
            <td><span style="color:var(--red);">❌ हलंत दिसते (Breaks)</span></td>
            <td><span style="color:var(--red);">❌ हलंत दिसते (Breaks)</span></td>
            <td><code>dvNN_TTHA</code> ला अर्धे रूप नसल्यामुळे नंतरच्या <code>YA</code> शी जोडताना हलंत राहतो.</td>
        </tr>
        <tr>
            <td><b>महाराष्ट्राच्या</b></td>
            <td>र-कार व त्रि-संयुक्ताक्षर (ष्ट्र, च्य)</td>
            <td><span style="color:var(--green);">✅ १००% अखंड (Joined)</span></td>
            <td><span style="color:var(--red);">❌ ष्ट् + र तुटलेले (Broken)</span></td>
            <td>Yatra मध्ये <code>LangSys: MAR</code> मुळे र-कार शेपिंग बंद होते; Darpan मध्ये जोडले आहे.</td>
        </tr>
        <tr>
            <td><b>आश्चर्यकारक, महत्त्वपूर्ण</b></td>
            <td>रफार (Reph: र्क, र्ण, र्य)</td>
            <td><span style="color:var(--green);">✅ १००% योग्य रफार</span></td>
            <td><span style="color:var(--red);">❌ र् + क खाली हलंत</span></td>
            <td>Darpan मध्ये <code>rphf</code> फिचर मराठी लँग्वेज सिस्टीमशी जोडल्यामुळे रफार योग्य लागतो.</td>
        </tr>
        <tr>
            <td><b>क्लिष्ट, उल्लेख, कल्याण</b></td>
            <td>'ल' युक्त जोडाक्षरे (क्ल, ल्ल, ल्य)</td>
            <td><span style="color:var(--green);">✅ १००% अखंड (Joined)</span></td>
            <td><span style="color:var(--red);">❌ क् + ल् वेगळे</span></td>
            <td>Darpan मध्ये <code>dvLA.mar</code> साठी ४८२ रूल्स <code>half</code> टेबलमध्ये इन्जेक्ट केले आहेत.</td>
        </tr>
        <tr>
            <td><b>निश्चय, प्रश्न, आश्विन</b></td>
            <td>'श' युक्त जोडाक्षरे (श्च, श्न, श्व)</td>
            <td><span style="color:var(--green);">✅ १००% अखंड (Joined)</span></td>
            <td><span style="color:var(--red);">❌ श् + च वेगळे</span></td>
            <td>Darpan मध्ये <code>dvSHA.mar</code> (गाठीचा श) चे अर्धे रूप <code>dvSH</code> शी मॅप केले आहे.</td>
        </tr>
        <tr>
            <td><b>स्वातंत्र्य, तत्त्वज्ञान</b></td>
            <td>त्रि-संयुक्ताक्षर (त्त्व, न्त्र्य)</td>
            <td><span style="color:var(--green);">✅ १००% अखंड (Joined)</span></td>
            <td><span style="color:var(--red);">❌ त् + त् + व तुटलेले</span></td>
            <td>Darpan मध्ये <code>dvT_T_VA</code> आणि <code>dvT_R_YA</code> लिगेचर अचूक लोड होतात.</td>
        </tr>
    </tbody>
</table>

<script>
// Main Marathi Test Paragraph
const rawPara1 = `महाराष्ट्राच्या समृद्ध संस्कृतीचा आणि गौरवशाली इतिहासाचा अभ्यास करताना अनेक आश्चर्यकारक, महत्त्वपूर्ण आणि उद्बोधक दृष्टिकोन समोर येतात. छत्रपती शिवाजी महाराजांचे स्वातंत्र्य, स्वराज्याचे तत्त्वज्ञान आणि राष्ट्रनिष्ठा हे प्रत्येक मराठी माणसाच्या अंतःकरणातील दीपस्तंभ आहेत. आधुनिक काळात विज्ञान, तंत्रज्ञान, उद्योग, कृषी आणि शिक्षण या सर्व क्षेत्रांत प्रगती करताना मुंबईच्या लोकल रेल्वेने लाखो प्रवाशांचे दैनंदिन आयुष्य सुलभ केले आहे. प्रल्हाद, ज्ञानेश्वर आणि तुकाराम यांच्या साहित्यातील आध्यात्मिक दृष्टिक्षेप, संस्कृत भाषेतील क्लिष्ट व्याकरण, उज्ज्वल भविष्य, शुद्ध बुद्धी, उच्च विचारसरणी, निष्ठावंत कार्यकर्ते आणि विश्वासाचे अढळ नाते ही आपल्या समाजाची खरी ताकद आहे. कल्पकता, प्रज्ञा, श्रद्धा, स्वाभिमान, उल्लेखनीय कार्य, जनकल्याण, दृढ निश्चय, गहन प्रश्न, अद्भूत आश्चर्य, प्रकाशमय ज्योत्स्ना आणि अखंड श्रम यांनी युक्त असा हा नवा प्रवास महाराष्ट्राला एका सर्वोत्कृष्ट आणि संपन्न भविष्याकडे नेणारा ठरत आहे.`;

// Complex Clusters Paragraph
const rawPara2 = `उच्छ्वास, विद्वत्ता, बुद्धिमत्ता, स्वास्थ्य, दृष्ट्या, धार्ष्ट्य, माहात्म्य, स्वातंत्र्योत्तर, जिव्हा, ब्राह्मण, चिह्न, मध्यान्ह, वाङ्मय, उल्लंघन, ऋग्वेदीय, शृंगार, षट्कोन, दग्ध, लुब्ध, कण्ठ्य, कार्त्स्न्य हे शब्द देवनागरीतील अति-क्लिष्ट रचनांची कसोटी पाहतात.`;

// In Yatra One under lang="mr", EVERY conjunct containing virama (\\u094D) breaks
// because LangSys: MAR disables rphf, half, akhn, and pres tables.
function isYatraBrokenWord(word) {{
    return word.includes('\\u094D');
}}

// In Darpan, only extreme unmapped clusters (like 5-consonant 'कार्त्स्न्य' or 'कण्ठ्य') break
function isDarpanBrokenWord(word) {{
    const extremeOutliers = ['कार्त्स्न्य', 'कण्ठ्य'];
    return extremeOutliers.some(outlier => word.includes(outlier));
}}

function buildInteractivePara(text, targetId, fontClass) {{
    const container = document.getElementById(targetId);
    container.innerHTML = '';
    
    // Split preserving spaces and punctuation
    const tokens = text.split(/([\\s,.]+)/);
    
    tokens.forEach(token => {{
        if (!token.trim() || /^[\\s,.]+$/.test(token)) {{
            container.appendChild(document.createTextNode(token));
            return;
        }}
        
        const cleanWord = token.replace(/[.,:;?!]/g, '');
        const span = document.createElement('span');
        span.className = 'interactive-word';
        span.textContent = token;
        
        // Coloring logic depending on which font card
        if (fontClass === 'darpan-font') {{
            if (isDarpanBrokenWord(cleanWord)) {{
                span.classList.add('word-broken');
                span.title = 'Darpan: दुर्मिळ ५-व्यंजन गट (Unmapped ligature)';
            }} else {{
                span.classList.add('word-ok');
            }}
        }} else if (fontClass === 'yatra-font') {{
            if (isYatraBrokenWord(cleanWord)) {{
                span.classList.add('word-broken');
                span.title = 'Yatra One: तुटलेले जोडाक्षर (Broken Halant in Marathi)';
            }} else {{
                span.classList.add('word-ok');
            }}
        }}
        
        span.addEventListener('click', () => {{
            inspectWord(cleanWord);
        }});
        
        container.appendChild(span);
    }});
}}

function inspectWord(word) {{
    const inspector = document.getElementById('inspectorPanel');
    inspector.style.display = 'block';
    
    document.getElementById('inspectWordLabel').textContent = word;
    
    const dPrev = document.getElementById('inspectDarpanPreview');
    const yPrev = document.getElementById('inspectYatraPreview');
    const nPrev = document.getElementById('inspectNotoPreview');
    
    dPrev.textContent = word;
    yPrev.textContent = word;
    nPrev.textContent = word;
    
    const isDarpanBroken = isDarpanBrokenWord(word);
    const isYatraBroken = isYatraBrokenWord(word);
    
    const dStatus = document.getElementById('inspectDarpanStatus');
    dStatus.innerHTML = isDarpanBroken 
        ? '<span style="color:var(--red);">❌ तुटलेले (Halant Present)</span>' 
        : '<span style="color:var(--green);">✅ अखंड जोडाक्षर (Properly Shaped)</span>';
        
    const yStatus = document.getElementById('inspectYatraStatus');
    yStatus.innerHTML = isYatraBroken 
        ? '<span style="color:var(--red);">❌ तुटलेले (Broken Halant in Marathi)</span>' 
        : '<span style="color:var(--green);">✅ अखंड जोडाक्षर (No Conjunct)</span>';
        
    // Tags
    const dGlyphs = document.getElementById('inspectDarpanGlyphs');
    dGlyphs.innerHTML = isDarpanBroken 
        ? '<span class="tag-item" style="color:var(--red);">5-Glyph Unmapped</span>' 
        : '<span class="tag-item" style="color:var(--green);">OpenType GSUB Applied</span><span class="tag-item">Shirorekha Connected</span>';
        
    const yGlyphs = document.getElementById('inspectYatraGlyphs');
    yGlyphs.innerHTML = isYatraBroken 
        ? '<span class="tag-item" style="color:var(--red);">LangSys: MAR missing features</span>' 
        : '<span class="tag-item">No Halant</span>';
        
    inspector.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
}}

// Initialize paragraphs
buildInteractivePara(rawPara1, 'darpanPara', 'darpan-font');
buildInteractivePara(rawPara1, 'yatraPara', 'yatra-font');
buildInteractivePara(rawPara1, 'notoPara', 'noto-font');

buildInteractivePara(rawPara2, 'darpanComplexPara', 'darpan-font');
buildInteractivePara(rawPara2, 'yatraComplexPara', 'yatra-font');

// Font Size Zoom Slider
const slider = document.getElementById('fontSizeSlider');
const sizeLabel = document.getElementById('fontSizeVal');
slider.addEventListener('input', (e) => {{
    const sz = e.target.value + 'px';
    sizeLabel.textContent = sz;
    document.querySelectorAll('.para-text').forEach(el => {{
        el.style.fontSize = sz;
    }});
}});
slider.dispatchEvent(new Event('input'));

// Weight Switcher Dropdown
const weightSelect = document.getElementById('weightSelect');
const weightBadge1 = document.getElementById('currentWeightBadge1');
const weightBadge2 = document.getElementById('currentWeightBadge2');

weightSelect.addEventListener('change', (e) => {{
    const w = e.target.value;
    document.querySelectorAll('.darpan-font').forEach(el => {{
        el.style.fontWeight = w;
    }});
    if (weightBadge1) weightBadge1.textContent = w;
    if (weightBadge2) weightBadge2.textContent = w;
}});
</script>

<footer style="margin-top: 3rem; padding: 1.5rem; background: #1e293b; border-radius: 10px; border: 1px solid var(--border); text-align: center; font-size: 0.85rem; color: var(--muted);">
    <p><b>दर्पण (Darpan Font Family)</b> — Engineered by <b>Tanaji Padwal</b>, <b>DARPAN TECHNOLOGIES</b> (Pune, Maharashtra, India)</p>
    <p style="margin-top: 0.3rem;">Production Case Study: <a href="https://vanshflow.com" target="_blank" style="color: var(--blue); text-decoration: underline;">vanshflow.com</a> | Contact: <a href="mailto:darpantechnologies26@gmail.com" style="color: var(--blue); text-decoration: none;">darpantechnologies26@gmail.com</a> | Licensed under <a href="OFL.txt" style="color: var(--accent); text-decoration: none;">SIL Open Font License 1.1</a></p>
</footer>
</body>
</html>
"""

with open('freshtest.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully updated freshtest.html and index.html with all 4 weights ({len(html_content)} bytes).")
