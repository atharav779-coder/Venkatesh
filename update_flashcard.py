import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Modal HTML
content = re.sub(r'<!-- ===== INFO MODAL ===== -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Remove Modal CSS
content = re.sub(r'/\* ===== MODAL ===== \*/.*?@media \(max-width: 600px\) \{.*?\}', '', content, flags=re.DOTALL)
# Also remove the media query that was left behind
content = re.sub(r'@media \(max-width: 600px\) \{.*?\}', '', content, flags=re.DOTALL)

# 3. Update CSS for flashcard to be taller and handle buttons
css_updates = """
    .flashcard {
      perspective: 1500px;
      height: 680px;
      cursor: pointer;
    }
    
    .card-buttons {
      display: flex; gap: 0.4rem; margin-top: 1rem;
      flex-wrap: wrap; justify-content: center;
      position: relative; z-index: 10;
    }
    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #00d4ff; padding: 0.4rem 0.5rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; flex: 1; min-width: 0; text-align: center;
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

content = re.sub(r'\.flashcard \{.*?height: 620px;.*?\}', '', content, flags=re.DOTALL)
content = content.replace('/* ===== FLASHCARD ===== */', '/* ===== FLASHCARD ===== */\n' + css_updates)

# Clean up flashcard-wrapper since we don't need it outside the card anymore
content = re.sub(r'\.flashcard-wrapper \{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'\.flashcard-wrapper \.flashcard \{.*?\}', '', content, flags=re.DOTALL)

# 4. Modify JavaScript render function
# Replace openModal with showDetails
old_js = r'// ============ DETAIL MODAL DATA ============.*?</script>'
new_js = """
// ============ DETAIL DATA ============
const detailData = JSON.parse(document.getElementById('detailDataObj').textContent);

function getDetailHTML(planeName, tab) {
  const data = detailData[planeName];
  if (!data) return `<p>Data coming soon</p>`;
  
  let tabData, tabTitle;
  if (tab === 'cabin') { tabData = data.cabin; tabTitle = 'Cabin & Pax Experience'; }
  else if (tab === 'airframe') { tabData = data.airframe; tabTitle = 'Airframe & Engine'; }
  else { tabData = data.performance; tabTitle = 'Performance & Load'; }

  let gridHTML = Object.entries(tabData).map(([k,v]) => `
    <div class="dynamic-item">
      <div class="d-label">${k}</div>
      <div class="d-value">${v}</div>
    </div>
  `).join('');

  return `
    <div class="dynamic-back-title">${tabTitle}</div>
    <div class="dynamic-grid">${gridHTML}</div>
    <div class="flip-back-hint" style="margin-top: 1.5rem;">Click to flip back</div>
  `;
}
</script>
"""
content = re.sub(old_js, new_js, content, flags=re.DOTALL)

# Now we need to extract detailData json so we can embed it safely
# Actually, the python script earlier injected `const detailData = {...};`
# Let's just fix the script directly instead of parsing out the JSON block.

# First, let's find the createCard function and rewrite it entirely.
create_card_regex = r'function createCard\(plane\) \{.*?\n\}\n'

new_create_card = """function createCard(plane) {
  const statsHTML = Object.entries(plane.stats).map(([k,v]) =>
    `<div class="stat"><span class="stat-label">${k}</span><span class="stat-value">${v}</span></div>`
  ).join('');

  const specsHTML = Object.entries(plane.specs).map(([k,v]) =>
    `<div class="spec-item"><div class="spec-label">${k}</div><div class="spec-val">${v}</div></div>`
  ).join('');

  const prosHTML = (plane.pros || []).map(p => `<li>${p}</li>`).join('');
  const consHTML = (plane.cons || []).map(c => `<li>${c}</li>`).join('');
  const prosConsHTML = (prosHTML || consHTML) ? `
    <div class="pros-cons">
      <div class="pros"><h4>✦ Advantages</h4><ul>${prosHTML}</ul></div>
      <div class="cons"><h4>✦ Disadvantages</h4><ul>${consHTML}</ul></div>
    </div>` : '';

  const defaultBackHTML = `
    <div class="back-header">
      <h3>${plane.name}</h3>
      <div class="subtitle">${plane.origin}</div>
    </div>
    <div class="spec-grid">${specsHTML}</div>
    <div class="back-desc">${plane.desc}</div>
    ${prosConsHTML}
    <div class="flip-back-hint">Click to flip back</div>
  `;

  const fc = document.createElement('div');
  fc.className = 'flashcard reveal';
  fc.innerHTML = `
    <div class="flashcard-inner">
      <div class="flashcard-front">
        <div class="card-img-wrap">
          <img src="${plane.img}" alt="${plane.name}" loading="lazy" />
          <span class="card-category">${plane.category}</span>
        </div>
        <div class="card-body">
          <h3>${plane.name}</h3>
          <div class="origin">${plane.origin}</div>
          <div class="card-stats">${statsHTML}</div>
          
          <div class="card-buttons">
            <button class="info-btn" data-tab="cabin">Cabin</button>
            <button class="info-btn" data-tab="airframe">Airframe</button>
            <button class="info-btn" data-tab="performance">Performance</button>
          </div>
        </div>
      </div>
      <div class="flashcard-back">
        ${defaultBackHTML}
      </div>
    </div>`;

  const backEl = fc.querySelector('.flashcard-back');
  
  // Handle clicks on the buttons
  const btns = fc.querySelectorAll('.info-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // prevent default flip
      const tab = btn.getAttribute('data-tab');
      backEl.innerHTML = getDetailHTML(plane.name, tab);
      fc.classList.add('flipped');
    });
  });

  // Handle general click to flip back to front, or front to default back
  fc.addEventListener('click', () => {
    if (fc.classList.contains('flipped')) {
      fc.classList.remove('flipped');
      // Reset back to default after animation
      setTimeout(() => { backEl.innerHTML = defaultBackHTML; }, 400);
    } else {
      backEl.innerHTML = defaultBackHTML;
      fc.classList.add('flipped');
    }
  });

  return fc;
}
"""
content = re.sub(create_card_regex, new_create_card, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated flashcards!")
