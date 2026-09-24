import re

with open('current_styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Fonts
css = css.replace("'Rajdhani'", "'Outfit'")
css = css.replace("'Orbitron'", "'Montserrat'")

# 2. Body & Background
old_body = """    body {
      font-family: 'Outfit', sans-serif;
      background: #030712;
      color: #e2e8f0;
      margin: 0; padding: 0;
      overflow-x: hidden;
    }"""
new_body = """    body {
      font-family: 'Outfit', sans-serif;
      background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
      background-attachment: fixed;
      color: #1e293b;
      margin: 0; padding: 0;
      overflow-x: hidden;
    }"""
css = css.replace(old_body, new_body)

# Body grid -> smooth blobs
old_body_before = """    body::before {
      content: '';
      position: fixed; inset: 0;
      background: linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
                  linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
      background-size: 50px 50px;
      z-index: -1;
    }"""
new_body_before = """    body::before {
      content: '';
      position: fixed; inset: 0;
      background: radial-gradient(circle at top left, rgba(255,255,255,0.5), transparent 40%),
                  radial-gradient(circle at bottom right, rgba(255,255,255,0.4), transparent 40%);
      z-index: -1;
    }"""
css = css.replace(old_body_before, new_body_before)

# 3. Navbar
old_nav = """    .navbar {
      position: fixed; top: 0; width: 100%;
      background: rgba(3, 7, 18, 0.8);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(0,212,255,0.1);
      z-index: 1000;
      display: flex; justify-content: space-between; align-items: center;
      padding: 1rem 3rem;
      transition: all 0.3s;
    }"""
new_nav = """    .navbar {
      position: fixed; top: 0; width: 100%;
      background: rgba(255, 255, 255, 0.5);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.4);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
      z-index: 1000;
      display: flex; justify-content: space-between; align-items: center;
      padding: 1rem 3rem;
      transition: all 0.3s;
    }"""
css = css.replace(old_nav, new_nav)

css = css.replace("color: #00d4ff;", "color: #0284c7;")
css = css.replace("color: #fff;", "color: #0f172a;")
css = css.replace("background: rgba(0,212,255,0.1);", "background: rgba(2,132,199,0.1);")
css = css.replace("background: rgba(0,212,255,0.05);", "background: rgba(255,255,255,0.6);")
css = css.replace("background: #00d4ff;", "background: #0284c7;")

# Nav links hover
css = css.replace("color: #94a3b8;", "color: #475569;") # muted text
old_nav_hover = """    .nav-links a:hover, .nav-links a.active {
      background: rgba(0, 212, 255, 0.1);
      color: #0284c7;
    }"""
new_nav_hover = """    .nav-links a:hover, .nav-links a.active {
      background: rgba(2, 132, 199, 0.15);
      color: #0284c7;
    }"""
css = css.replace(old_nav_hover, new_nav_hover)

# 4. Search box
old_search = """    .search-box {
      width: 100%; padding: 1rem 1.5rem;
      background: rgba(0,0,0,0.4);
      border: 1px solid rgba(0,212,255,0.2);
      border-radius: 50px;
      color: #0f172a; font-size: 1.1rem;
      font-family: 'Outfit', sans-serif; outline: none;
      box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
      transition: all 0.3s;
    }
    .search-box::placeholder { color: #475569; }
    .search-box:focus {
      background: rgba(0,0,0,0.6);
      border-color: #0284c7;
      box-shadow: 0 0 15px rgba(0,212,255,0.3);
    }"""
new_search = """    .search-box {
      width: 100%; padding: 1rem 1.5rem;
      background: rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 50px;
      color: #0f172a; font-size: 1.1rem;
      font-family: 'Outfit', sans-serif; outline: none;
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
      transition: all 0.3s;
    }
    .search-box::placeholder { color: #64748b; }
    .search-box:focus {
      background: rgba(255, 255, 255, 0.9);
      border-color: #0284c7;
      box-shadow: 0 8px 25px rgba(2, 132, 199, 0.15);
    }"""
css = css.replace(old_search, new_search)

# 5. Flashcards
old_front_back = """    .flashcard-front, .flashcard-back {
      position: absolute; inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 12px; overflow: hidden;
      border: 1px solid rgba(0,212,255,0.15);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }"""
new_front_back = """    .flashcard-front, .flashcard-back {
      position: absolute; inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 16px; overflow: hidden;
      background: rgba(255, 255, 255, 0.65);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.8);
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
    }"""
css = css.replace(old_front_back, new_front_back)

old_front = """    /* FRONT */
    .flashcard-front {
      background: linear-gradient(160deg, rgba(12,18,34,.95), rgba(5,8,16,.98));
      display: flex; flex-direction: column;
    }
    .flashcard-front::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,212,255,0.02) 2px, rgba(0,212,255,0.02) 4px);
    }"""
new_front = """    /* FRONT */
    .flashcard-front {
      display: flex; flex-direction: column;
    }"""
css = css.replace(old_front, new_front)

old_back = """    /* BACK */
    .flashcard-back {
      background: linear-gradient(160deg, rgba(5,8,16,.98), rgba(12,18,34,.95));
      transform: rotateY(180deg);
      padding: 2rem 1.5rem; display: flex; flex-direction: column;
      overflow-y: auto;
    }
    .flashcard-back::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background: radial-gradient(circle at center, rgba(0,212,255,0.05) 0%, transparent 70%);
    }"""
new_back = """    /* BACK */
    .flashcard-back {
      transform: rotateY(180deg);
      padding: 2rem 1.5rem; display: flex; flex-direction: column;
      overflow-y: auto;
    }"""
css = css.replace(old_back, new_back)

# Buttons
old_info_btn_css = """    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #0284c7; padding: 0.6rem 0.2rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Outfit', sans-serif; font-weight: 700;
      font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; text-align: center;
      display: flex; align-items: center; justify-content: center;
    }
    .info-btn:hover {
      background: #0284c7; color: #0f172a;
      box-shadow: 0 0 10px rgba(0,212,255,0.5);
    }"""
new_info_btn_css = """    .info-btn {
      background: rgba(255, 255, 255, 0.8);
      border: 1px solid rgba(2, 132, 199, 0.2);
      color: #0284c7; padding: 0.6rem 0.2rem;
      border-radius: 8px; cursor: pointer;
      font-family: 'Outfit', sans-serif; font-weight: 700;
      font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; text-align: center;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .info-btn:hover {
      background: #0284c7; color: #fff;
      box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
      border-color: #0284c7;
    }"""
css = css.replace(old_info_btn_css, new_info_btn_css)

# Update the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace fonts in HTML head
old_fonts = '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">'
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;900&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
html = html.replace(old_fonts, new_fonts)

# Replace the style block
html = re.sub(r'<style>.*?</style>', css, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated theme and typography")
