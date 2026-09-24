import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix button layout
old_buttons_css = """    .card-buttons {
      display: flex; gap: 0.4rem; margin-top: 1rem;
      flex-wrap: wrap; justify-content: center;
      position: relative; z-index: 10;
    }"""
new_buttons_css = """    .card-buttons {
      display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.4rem; margin-top: 1rem;
      position: relative; z-index: 10;
    }"""
content = content.replace(old_buttons_css, new_buttons_css)

old_info_btn = """    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #00d4ff; padding: 0.4rem 0.5rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; flex: 1; min-width: 0; text-align: center;
    }"""
new_info_btn = """    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #00d4ff; padding: 0.6rem 0.2rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; text-align: center;
      display: flex; align-items: center; justify-content: center;
    }"""
content = content.replace(old_info_btn, new_info_btn)

# Make sure the card is tall enough (700px instead of 680px just to be safe)
content = content.replace('height: 680px;', 'height: 700px;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS for grid buttons")
