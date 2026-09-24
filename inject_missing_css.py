import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_to_insert = """
    .flashcard {
      perspective: 1500px;
      height: 700px;
      cursor: pointer;
    }
    
    .card-buttons {
      display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.4rem; margin-top: 1rem;
      position: relative; z-index: 10;
    }
    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #00d4ff; padding: 0.6rem 0.2rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; text-align: center;
      display: flex; align-items: center; justify-content: center;
    }
    .info-btn:hover {
      background: #00d4ff; color: #000;
      box-shadow: 0 0 10px rgba(0,212,255,0.5);
    }
    
    /* Dynamic back content */
    .dynamic-back-title {
      font-family: 'Orbitron', sans-serif; font-size: 1.1rem; font-weight: 800;
      color: #00d4ff; text-transform: uppercase; letter-spacing: 1px;
      margin-bottom: 1rem; border-bottom: 1px solid rgba(0,212,255,0.2); padding-bottom: 0.5rem;
    }
    .dynamic-grid {
      display: grid; grid-template-columns: 1fr; gap: 0.8rem;
    }
    .dynamic-item {
      background: rgba(0,212,255,0.05); padding: 0.6rem; border-radius: 4px;
      border-left: 2px solid #00d4ff;
    }
    .dynamic-item .d-label {
      font-family: 'Rajdhani', sans-serif; font-size: 0.7rem; color: #7a8ba8;
      text-transform: uppercase; font-weight: 700; margin-bottom: 2px;
    }
    .dynamic-item .d-value {
      font-family: 'Rajdhani', sans-serif; font-size: 0.9rem; color: #fff; font-weight: 600;
    }
"""

# Find .card-grid { ... } and insert our CSS right after it
match = re.search(r'\.card-grid \{.*?\}', content, re.DOTALL)
if match:
    # First remove any lingering .flashcard-wrapper junk
    content = content.replace('.flashcard-wrapper \n    .flashcard-inner {', '.flashcard-inner {')
    content = content.replace('.flashcard-wrapper\n    .flashcard-inner {', '.flashcard-inner {')
    
    insert_pos = match.end()
    content = content[:insert_pos] + "\n" + css_to_insert + content[insert_pos:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected missing CSS")
else:
    print("Could not find .card-grid")
