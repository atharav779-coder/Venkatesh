import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix remaining light-text colors in the CSS
# e2e8f0 -> 334155 (slate-700)
html = html.replace('#e2e8f0', '#334155')
# 6b7a94 -> 64748b (slate-500)
html = html.replace('#6b7a94', '#64748b')
# 7a8ba8 -> 64748b
html = html.replace('#7a8ba8', '#64748b')
# a1a1aa -> 64748b
html = html.replace('#a1a1aa', '#64748b')
# border bottom on card img
html = html.replace('border-bottom: 2px solid rgba(0,212,255,0.2);', 'border-bottom: 2px solid rgba(2, 132, 199, 0.2);')

# Let's adjust the stats grid inside the card
# The stats boxes originally had dark background
html = html.replace('background: rgba(255,255,255,0.6); padding: 8px; border-radius: 4px;', 'background: rgba(255, 255, 255, 0.7); padding: 8px; border-radius: 8px; border: 1px solid rgba(2, 132, 199, 0.1);')
html = html.replace('background: rgba(0,0,0,0.2);', 'background: rgba(255, 255, 255, 0.7); border: 1px solid rgba(2, 132, 199, 0.1);')
html = html.replace('background: rgba(0, 0, 0, 0.2);', 'background: rgba(255, 255, 255, 0.7); border: 1px solid rgba(2, 132, 199, 0.1);')

# Make the card image wrapper not have a black background
html = html.replace('background: #000;', 'background: #e2e8f0;')

# Make the Pros/Cons look elegant
html = html.replace('background: rgba(16, 185, 129, 0.1);', 'background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2);')
html = html.replace('background: rgba(239, 68, 68, 0.1);', 'background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2);')
html = html.replace('color: #34d399;', 'color: #059669;')
html = html.replace('color: #f87171;', 'color: #dc2626;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cleaned up remaining text colors.")
