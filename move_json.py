import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the detailDataObj script
match = re.search(r'(<script type="application/json" id="detailDataObj">.*?</script>)', html, re.DOTALL)
if match:
    obj_script = match.group(1)
    # Remove it from the current position
    html = html.replace(obj_script, '')
    # Insert it right before the main script starts
    html = html.replace('<script>', obj_script + '\n<script>', 1)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Moved detailDataObj.")
else:
    print("Not found.")
