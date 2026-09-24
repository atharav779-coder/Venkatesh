import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

search_html = """
    <div class="nav-links" id="navLinks">
      <a href="#commercial">Commercial</a>
      <a href="#fighter-jets">Fighter Jets</a>
      <a href="#private-jets">Private Jets</a>
      <a href="#cargo">Cargo</a>
      <a href="#military">Military</a>
      <a href="#trainers">Trainers</a>
      <a href="#helicopters">Helicopters</a>
      <a href="#seaplanes">Seaplanes</a>
    </div>
    <div class="search-container">
      <input type="text" id="searchInput" placeholder="Search aircraft..." autocomplete="off">
    </div>
"""

content = re.sub(r'<div class="nav-links" id="navLinks">.*?</div>', search_html, content, flags=re.DOTALL)

search_css = """
    .search-container {
      margin-left: 1rem;
      position: relative;
    }
    #searchInput {
      background: rgba(0,212,255,0.05);
      border: 1px solid rgba(0,212,255,0.2);
      border-radius: 20px;
      padding: 0.4rem 1rem;
      color: #fff;
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      width: 200px;
      transition: all 0.3s;
    }
    #searchInput:focus {
      outline: none;
      background: rgba(0,212,255,0.1);
      border-color: #00d4ff;
      box-shadow: 0 0 10px rgba(0,212,255,0.3);
      width: 250px;
    }
    #searchInput::placeholder {
      color: rgba(255,255,255,0.4);
    }
    @media (max-width: 900px) {
      .search-container { display: none; }
    }
"""

content = re.sub(r'/\* ===== HERO ===== \*/', search_css + '\n    /* ===== HERO ===== */', content)

search_js = """
// ============ SEARCH FUNCTIONALITY ============
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', (e) => {
  const term = e.target.value.toLowerCase();
  const allCards = document.querySelectorAll('.flashcard');
  const sections = document.querySelectorAll('.section');
  
  allCards.forEach(card => {
    const text = card.innerText.toLowerCase();
    if (text.includes(term)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });

  // Hide sections if all cards inside are hidden
  sections.forEach(sec => {
    const cards = sec.querySelectorAll('.flashcard');
    const hasVisible = Array.from(cards).some(c => c.style.display !== 'none');
    sec.style.display = (hasVisible || term === '') ? 'block' : 'none';
  });
});
"""

content = re.sub(r'// ============ MOBILE NAV ============', search_js + '\n// ============ MOBILE NAV ============', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added search bar.")
