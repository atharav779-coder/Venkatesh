import re
import json

# 1. Update package.json scripts
try:
    with open('package.json', 'r', encoding='utf-8') as f:
        pkg = json.load(f)
    pkg.setdefault('scripts', {})['dev'] = 'vite'
    pkg['scripts']['build'] = 'vite build'
    pkg['scripts']['preview'] = 'vite preview'
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(pkg, f, indent=2)
except Exception as e:
    print("package.json error:", e)

# 2. Configure Tailwind
tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
with open('tailwind.config.js', 'w', encoding='utf-8') as f:
    f.write(tailwind_config)

# 3. Extract CSS from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    css_content = style_match.group(1)
    # Write to style.css with Tailwind directives
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n" + css_content)
    
    # Replace <style> block in index.html with <link>
    html = html.replace(style_match.group(0), '<link rel="stylesheet" href="./style.css" />')
    
    # Vite expects index.html to have a module script if there is JS, 
    # but since our JS is inline in <script>, it should be fine.
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Migrated CSS to style.css and updated index.html")
else:
    print("No <style> block found in index.html")
