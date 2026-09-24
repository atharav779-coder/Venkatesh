import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the modal javascript to take an imgSrc and display it
old_modal_start = "function openModal(planeName, tab) {"
new_modal_start = "function openModal(planeName, tab, imgSrc) {"

old_modal_html = """document.getElementById('modalContent').innerHTML = `
    <div class="modal-title">${tabIcon} ${planeName}</div>
    <div class="modal-subtitle">${tabTitle}</div>
    <div class="modal-grid">${gridHTML}</div>
  `;"""

new_modal_html = """document.getElementById('modalContent').innerHTML = `
    <img src="${imgSrc}" alt="${planeName}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; border: 1px solid rgba(0,212,255,0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.5);" />
    <div class="modal-title">${tabIcon} ${planeName}</div>
    <div class="modal-subtitle">${tabTitle}</div>
    <div class="modal-grid">${gridHTML}</div>
  `;"""

content = content.replace(old_modal_start, new_modal_start)
content = content.replace(old_modal_html, new_modal_html)

# Update the buttons to pass the image URL
old_buttons = """    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'cabin')">
      <span class="btn-icon">🛩️</span>Cabin & Pax Experience
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'airframe')">
      <span class="btn-icon">⚙️</span>Airframe & Engine
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'performance')">
      <span class="btn-icon">📊</span>Performance & Load
    </button>"""

new_buttons = """    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'cabin', '${plane.img}')">
      <span class="btn-icon">🛩️</span>Cabin & Pax Experience
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'airframe', '${plane.img}')">
      <span class="btn-icon">⚙️</span>Airframe & Engine
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'performance', '${plane.img}')">
      <span class="btn-icon">📊</span>Performance & Load
    </button>"""

content = content.replace(old_buttons, new_buttons)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated modal to include photo")
