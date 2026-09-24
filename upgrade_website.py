import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_replacement = """
    /* ===== RESET & BASE ===== */
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 80px; }
    body {
      font-family: 'Inter', sans-serif;
      background: #030610;
      color: #e0e6f0;
      overflow-x: hidden;
      line-height: 1.6;
    }

    /* ===== ANIMATED BACKGROUND ===== */
    .bg-grid {
      position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background-size: 60px 60px;
      background-image: 
        linear-gradient(to right, rgba(0, 212, 255, 0.04) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 212, 255, 0.04) 1px, transparent 1px);
      transform: perspective(600px) rotateX(60deg);
      transform-origin: top;
      animation: gridMove 15s linear infinite;
    }
    @keyframes gridMove {
      0% { transform: perspective(600px) rotateX(60deg) translateY(0); }
      100% { transform: perspective(600px) rotateX(60deg) translateY(60px); }
    }

    .bg-gradient {
      position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background:
        radial-gradient(ellipse at 20% 0%, rgba(15,82,186,.15) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(0,212,255,.1) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(3,6,16,.8) 0%, transparent 100%);
    }

    /* ===== NAVBAR ===== */
    nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
      background: rgba(3, 6, 16, .85);
      backdrop-filter: blur(24px) saturate(1.8);
      -webkit-backdrop-filter: blur(24px) saturate(1.8);
      border-bottom: 1px solid rgba(0,212,255,.1);
      transition: box-shadow .3s;
    }
    nav.scrolled { box-shadow: 0 4px 30px rgba(0,0,0,.6); border-bottom: 1px solid rgba(0,212,255,.3); }
    .nav-inner {
      max-width: 1400px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 2rem; height: 72px;
    }
    .logo {
      font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 1.6rem;
      background: linear-gradient(135deg, #00d4ff, #ffffff);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      letter-spacing: 4px; text-decoration: none;
      text-shadow: 0 0 20px rgba(0,212,255,0.3);
    }
    .logo span { font-weight: 400; opacity: .7; }
    .nav-links { display: flex; gap: 0.3rem; flex-wrap: wrap; }
    .nav-links a {
      color: #8892a8; text-decoration: none; font-size: .82rem; font-weight: 600;
      padding: .45rem .85rem; border-radius: 6px; transition: all .25s;
      font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1.5px;
    }
    .nav-links a:hover, .nav-links a.active {
      color: #00d4ff; background: rgba(0,212,255,.1);
      box-shadow: 0 0 10px rgba(0,212,255,.2);
    }
    .hamburger {
      display: none; background: none; border: none; cursor: pointer;
      flex-direction: column; gap: 5px; padding: 6px;
    }
    .hamburger span {
      display: block; width: 26px; height: 2px; background: #8892a8;
      border-radius: 2px; transition: all .3s;
    }

    /* ===== HERO ===== */
    .hero {
      position: relative; z-index: 1;
      min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; justify-content: center; text-align: center;
      padding: 2rem;
      background:
        radial-gradient(circle at 50% 40%, rgba(0,100,255,.08) 0%, transparent 60%);
    }
    .hero-badge {
      display: inline-flex; align-items: center; gap: .5rem;
      background: rgba(0,212,255,.1); border: 1px solid rgba(0,212,255,.3);
      padding: .4rem 1.2rem; border-radius: 100px; font-size: .78rem;
      color: #00d4ff; font-weight: 600; margin-bottom: 1.5rem;
      letter-spacing: 2px; text-transform: uppercase;
      font-family: 'Rajdhani', sans-serif;
      box-shadow: 0 0 15px rgba(0,212,255,.2);
    }
    .hero-badge::before { content: '✈'; font-size: 1rem; }
    .hero h1 {
      font-family: 'Orbitron', sans-serif; font-size: clamp(2.5rem, 7vw, 6rem);
      font-weight: 900; line-height: 1.1; margin-bottom: 1.2rem;
      background: linear-gradient(135deg, #ffffff 0%, #c0e0ff 40%, #00d4ff 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      text-transform: uppercase; letter-spacing: 2px;
      text-shadow: 0 10px 30px rgba(0,212,255,0.2);
    }
    .hero p {
      font-size: clamp(1rem, 2vw, 1.25rem); color: #8a9bb8;
      max-width: 650px; margin-bottom: 2.5rem; font-weight: 300;
    }
    .hero-cta {
      display: inline-flex; align-items: center; gap: .6rem;
      background: linear-gradient(135deg, #00d4ff, #0f52ba);
      color: #fff; text-decoration: none; padding: 1rem 2.5rem;
      border-radius: 8px; font-weight: 700; font-size: 1.1rem;
      font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px;
      transition: all .3s;
      box-shadow: 0 5px 25px rgba(0,212,255,.4);
      border: 1px solid rgba(255,255,255,0.2);
    }
    .hero-cta:hover { transform: translateY(-3px); box-shadow: 0 8px 35px rgba(0,212,255,.6); }
    .hero-cta::after { content: '↓'; font-size: 1.2rem; }
    .scroll-indicator {
      position: absolute; bottom: 2rem;
      animation: bounce 2s infinite;
    }
    .scroll-indicator span {
      display: block; width: 28px; height: 28px;
      border-right: 2px solid rgba(0,212,255,.6);
      border-bottom: 2px solid rgba(0,212,255,.6);
      transform: rotate(45deg);
    }
    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(12px); }
      60% { transform: translateY(6px); }
    }

    /* ===== SECTIONS ===== */
    .section {
      position: relative; z-index: 1;
      padding: 5rem 2rem;
      max-width: 1400px; margin: 0 auto;
    }
    .section-header {
      text-align: center; margin-bottom: 3.5rem;
    }
    .section-header .tag {
      display: inline-block;
      font-family: 'Rajdhani', sans-serif; font-size: .85rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 4px;
      color: #00d4ff; margin-bottom: .6rem;
      background: rgba(0,212,255,.1); padding: 4px 12px; border-radius: 4px;
      border-left: 2px solid #00d4ff; border-right: 2px solid #00d4ff;
    }
    .section-header h2 {
      font-family: 'Orbitron', sans-serif; font-size: clamp(2rem, 4vw, 3rem);
      font-weight: 800; margin-bottom: .8rem;
      color: #fff; text-transform: uppercase; letter-spacing: 2px;
    }
    .section-header p {
      color: #6b7a94; font-size: 1.05rem; max-width: 600px; margin: 0 auto;
    }
    .divider {
      width: 80px; height: 4px; margin: 1.5rem auto 0;
      background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    }

    /* ===== CARD GRID ===== */
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 2.5rem;
    }

    /* ===== FLASHCARD ===== */
    .flashcard {
      perspective: 1500px;
      height: 520px;
      cursor: pointer;
    }
    .flashcard-inner {
      position: relative; width: 100%; height: 100%;
      transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      transform-style: preserve-3d;
    }
    .flashcard.flipped .flashcard-inner { transform: rotateY(180deg); }

    .flashcard-front, .flashcard-back {
      position: absolute; inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 12px; overflow: hidden;
      border: 1px solid rgba(0,212,255,0.15);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* FRONT */
    .flashcard-front {
      background: linear-gradient(160deg, rgba(12,18,34,.95), rgba(5,8,16,.98));
      display: flex; flex-direction: column;
    }
    .flashcard-front::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,212,255,0.02) 2px, rgba(0,212,255,0.02) 4px);
    }
    .card-img-wrap {
      position: relative; height: 220px; overflow: hidden;
      background: #000;
      border-bottom: 2px solid rgba(0,212,255,0.2);
    }
    .card-img-wrap img {
      width: 100%; height: 100%; object-fit: cover;
      transition: transform .7s, filter .7s;
      filter: contrast(1.1) saturate(1.1);
    }
    .flashcard:hover .card-img-wrap img { transform: scale(1.12); }
    
    .card-category {
      position: absolute; top: 12px; left: 12px;
      background: rgba(0,0,0,.7); backdrop-filter: blur(10px);
      padding: .3rem .8rem; border-radius: 4px;
      font-size: .7rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 2px; color: #00d4ff;
      border-left: 2px solid #00d4ff;
      font-family: 'Rajdhani', sans-serif;
    }
    .card-body { padding: 1.5rem; flex: 1; display: flex; flex-direction: column; position: relative; z-index: 2; }
    .card-body h3 {
      font-family: 'Orbitron', sans-serif; font-size: 1.25rem; font-weight: 800;
      margin-bottom: .4rem; color: #fff; text-transform: uppercase; letter-spacing: 1px;
    }
    .card-body .origin {
      font-size: .8rem; color: #00d4ff; margin-bottom: 1rem;
      font-family: 'Rajdhani', sans-serif; font-weight: 600;
      text-transform: uppercase; letter-spacing: 1.5px;
    }
    .card-stats {
      display: grid; grid-template-columns: 1fr 1fr; gap: .8rem;
      margin-top: auto;
    }
    .card-stats .stat {
      display: flex; flex-direction: column;
      background: rgba(255,255,255,0.03);
      padding: 8px; border-radius: 4px; border-left: 2px solid rgba(0,212,255,0.3);
    }
    .card-stats .stat-label {
      font-size: .65rem; color: #7a8ba8; text-transform: uppercase;
      letter-spacing: 1.5px; font-weight: 700;
      font-family: 'Rajdhani', sans-serif;
    }
    .card-stats .stat-value {
      font-size: .95rem; font-weight: 600; color: #fff;
      font-family: 'Rajdhani', sans-serif; letter-spacing: 1px;
    }
    .flip-hint {
      position: absolute; bottom: 12px; right: 14px;
      font-size: .7rem; color: #00d4ff; opacity: 0.6;
      font-family: 'Rajdhani', sans-serif; letter-spacing: 2px; text-transform: uppercase;
      display: flex; align-items: center; gap: 6px;
    }
    .flip-hint::after { content: '→'; font-size: 1rem; }

    /* BACK */
    .flashcard-back {
      transform: rotateY(180deg);
      background: linear-gradient(160deg, rgba(8,12,24,.98), rgba(4,6,12,.99));
      padding: 1.8rem;
      display: flex; flex-direction: column;
      overflow-y: auto;
      border: 1px solid rgba(0,212,255,0.3);
      box-shadow: inset 0 0 40px rgba(0,212,255,0.05);
    }
    .flashcard-back::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background-image: radial-gradient(rgba(0,212,255,0.15) 1px, transparent 1px);
      background-size: 20px 20px; opacity: 0.5;
    }
    .flashcard-back::-webkit-scrollbar { width: 4px; }
    .flashcard-back::-webkit-scrollbar-thumb { background: rgba(0,212,255,.4); border-radius: 10px; }
    
    .back-header { border-bottom: 1px solid rgba(0,212,255,0.2); padding-bottom: 0.8rem; margin-bottom: 1.2rem; }
    .flashcard-back h3 {
      font-family: 'Orbitron', sans-serif; font-size: 1.15rem; font-weight: 800;
      color: #fff; margin-bottom: .2rem; text-transform: uppercase; letter-spacing: 1px;
    }
    .flashcard-back .subtitle {
      font-size: .75rem; color: #00d4ff;
      font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;
    }
    
    .spec-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: .6rem;
      margin-bottom: 1.2rem; position: relative; z-index: 2;
    }
    .spec-item {
      background: rgba(0,212,255,.05);
      border: 1px solid rgba(0,212,255,.1);
      border-radius: 4px; padding: .6rem .8rem;
      transition: background 0.3s;
    }
    .spec-item:hover { background: rgba(0,212,255,.1); }
    .spec-item .spec-label {
      font-size: .65rem; color: #00d4ff; text-transform: uppercase;
      letter-spacing: 1.5px; font-weight: 700;
      font-family: 'Rajdhani', sans-serif;
    }
    .spec-item .spec-val {
      font-size: .85rem; font-weight: 600; color: #fff; margin-top: 3px;
      font-family: 'Rajdhani', sans-serif; letter-spacing: 1px;
    }
    .back-desc {
      font-size: .85rem; color: #8a9bb8; line-height: 1.6;
      padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 6px;
      border-left: 3px solid rgba(0,212,255,0.5);
      margin-top: auto; position: relative; z-index: 2;
    }
    .flip-back-hint {
      text-align: center; margin-top: 1rem;
      font-size: .7rem; color: #00d4ff; opacity: 0.6;
      font-family: 'Rajdhani', sans-serif; letter-spacing: 2px; text-transform: uppercase;
    }

    /* ===== CATEGORY NAV (STICKY) ===== */
    .cat-nav {
      position: sticky; top: 72px; z-index: 500;
      background: rgba(5,8,16,.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(0,212,255,.15);
      padding: 1rem 2rem;
      display: flex; justify-content: center; flex-wrap: wrap; gap: .6rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .cat-nav a {
      color: #7a8ba8; text-decoration: none;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: .85rem; text-transform: uppercase; letter-spacing: 2px;
      padding: .5rem 1.2rem; border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.05);
      transition: all .3s; background: rgba(255,255,255,0.02);
    }
    .cat-nav a:hover, .cat-nav a.active {
      color: #000; border-color: #00d4ff;
      background: #00d4ff; box-shadow: 0 0 15px rgba(0,212,255,.4);
    }

    /* ===== STATS BAR ===== */
    .stats-bar {
      position: relative; z-index: 1;
      display: flex; justify-content: center; flex-wrap: wrap; gap: 4rem;
      padding: 4rem 2rem;
      border-top: 1px solid rgba(0,212,255,.1);
      border-bottom: 1px solid rgba(0,212,255,.1);
      background: linear-gradient(90deg, transparent, rgba(0,212,255,.03), transparent);
    }
    .stats-bar .stat-box { text-align: center; }
    .stats-bar .stat-num {
      font-family: 'Orbitron', sans-serif; font-size: 3rem; font-weight: 900;
      color: #00d4ff; text-shadow: 0 0 20px rgba(0,212,255,0.4);
      line-height: 1; margin-bottom: 0.5rem;
    }
    .stats-bar .stat-txt {
      font-size: .85rem; color: #fff; text-transform: uppercase;
      letter-spacing: 3px; font-family: 'Rajdhani', sans-serif; font-weight: 700;
    }

    /* ===== FOOTER ===== */
    footer {
      position: relative; z-index: 1;
      text-align: center; padding: 4rem 2rem;
      background: #03050a;
      border-top: 1px solid rgba(0,212,255,.1);
    }
    footer .logo-foot {
      font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 1.5rem;
      color: #00d4ff; letter-spacing: 4px; margin-bottom: 1rem;
    }
    footer p { color: #5a6a84; font-size: .85rem; font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }

    /* ===== SCROLL REVEAL ===== */
    .reveal {
      opacity: 0; transform: translateY(50px) scale(0.95);
      transition: opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    .reveal.visible { opacity: 1; transform: translateY(0) scale(1); }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 900px) {
      .nav-links { display: none; }
      .hamburger { display: flex; }
      .nav-links.open {
        display: flex; flex-direction: column;
        position: absolute; top: 72px; left: 0; right: 0;
        background: rgba(5,8,16,.98);
        padding: 1rem 2rem 2rem;
        border-bottom: 1px solid rgba(0,212,255,.2);
      }
    }
    @media (max-width: 600px) {
      .cat-nav { gap: .4rem; padding: 1rem; }
      .cat-nav a { font-size: .75rem; padding: .4rem .8rem; }
      .flashcard { height: 560px; }
      .spec-grid { grid-template-columns: 1fr; }
    }
"""

content = re.sub(r'/\* ===== RESET & BASE ===== \*/.*?@media \(max-width: 600px\) \{.*?\n    \}', css_replacement, content, flags=re.DOTALL)

if '<div class="bg-stars"></div>' in content:
    content = content.replace('<div class="bg-stars"></div>', '<div class="bg-grid"></div>')

new_js_card = """
        <div class="back-header">
          <h3>${plane.name}</h3>
          <div class="subtitle">${plane.origin}</div>
        </div>
        <div class="spec-grid">${specsHTML}</div>
        <div class="back-desc">${plane.desc}</div>
        <div class="flip-back-hint">Click to flip back</div>
"""
content = re.sub(r'<h3>\$\{plane\.name\}</h3>\s*<div class="subtitle">\$\{plane\.origin\}</div>\s*<div class="spec-grid">\$\{specsHTML\}</div>\s*<div class="back-desc">\$\{plane\.desc\}</div>\s*<div class="flip-back-hint">Click to flip back</div>', new_js_card, content)

def enrich_plane(match):
    full_str = match.group(0)
    
    category = re.search(r'category:\s*"([^"]+)"', full_str)
    cat_val = category.group(1) if category else ""
    
    extra_specs = ""
    if "Commercial" in cat_val or "Cargo" in cat_val:
        extra_specs = ', "Fuel Cap": "130,000 L+", "Avionics": "Glass Cockpit", "Unit Cost": "$150M - $400M", "Runway Req": "2,500m+"'
    elif "Fighter" in cat_val:
        extra_specs = ', "Avionics": "AESA Radar / HUD", "Unit Cost": "$60M - $120M", "Fuel Cap": "5,000 - 8,000 kg", "T/W Ratio": "> 1.0"'
    elif "Private" in cat_val:
        extra_specs = ', "Avionics": "Garmin/Primus", "Unit Cost": "$20M - $75M", "Fuel Cap": "15,000 L+", "Cabin Alt": "4,000 ft"'
    elif "Military" in cat_val:
        extra_specs = ', "Avionics": "Tactical Suite", "Unit Cost": "$100M - $200M", "Fuel Cap": "70,000 kg+", "Airdrop": "Supported"'
    elif "Trainer" in cat_val:
        extra_specs = ', "Avionics": "Embedded Sim", "Unit Cost": "$10M - $30M", "Fuel Cap": "1,500 kg", "Ejection": "Zero-Zero Seats"'
    elif "Helicopter" in cat_val:
        extra_specs = ', "Avionics": "FLIR / Glass", "Unit Cost": "$10M - $35M", "Hover Ceiling": "3,000m+", "Fuel Cap": "1,200 L+"'
    elif "Seaplane" in cat_val:
        extra_specs = ', "Avionics": "Weather Radar", "Unit Cost": "$5M - $30M", "Hull Type": "Stepped Amphib", "Draft": "1.2m"'
    else:
        extra_specs = ', "Avionics": "Standard", "Unit Cost": "Varies", "Fuel Cap": "Varies"'
    
    new_str = re.sub(r'(specs:\s*\{[^}]+)(\})', r'\1' + extra_specs + r'\2', full_str)
    return new_str

content = re.sub(r'\{\s*name:\s*"[^"]+",[^}]+desc:\s*"[^"]+"\s*\}', enrich_plane, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully.")
