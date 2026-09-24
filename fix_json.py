import json
import re

with open('add_buttons.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract detail_data dictionary creation code
code = text.split('# 3. Add detailed data for all planes')[1].split('# 4. Now inject')[0]
local_env = {}
exec(code, {}, local_env)
detail_data = local_env['detail_data']

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

json_str = json.dumps(detail_data)
html = html.replace('</body>', f'<script type="application/json" id="detailDataObj">{json_str}</script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added JSON data.")
