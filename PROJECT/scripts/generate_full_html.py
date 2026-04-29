import json
import os

# Read the HTML template
with open("tmp_presentation.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Replace the external script with embedding
html_template = html_template.replace('<script src="nexus_translations.js"></script>', '')

# Read the updated translations JS
with open("PROJECT/outputs/WEB_UPDATE/nexus_translations.js", "r", encoding="utf-8") as f:
    translations_js = f.read()

# Hide language switcher
html_template = html_template.replace('<div class="lang-sw">', '<div class="lang-sw" style="display:none;">')

os.makedirs("PROJECT/outputs/INSTRUCTIONS_WEB", exist_ok=True)

for lang in ["en", "ru", "ua"]:
    # For each language, we just embed the translations and change the default curLang
    modified_html = html_template
    
    # Inject translations script right before the main script
    injection = f"<script>{translations_js}</script>\n    <script src="
    modified_html = modified_html.replace('<script src=', injection, 1)
    
    # Change default language
    modified_html = modified_html.replace("let curLang = 'en';", f"let curLang = '{lang}';")
    
    # Auto-render the specific language with initialization
    init_script = f"""
        // Wait for DOM to be ready
        document.addEventListener('DOMContentLoaded', () => {{
            setLang('{lang}');
        }});
    </script>
</body>
"""
    modified_html = modified_html.replace('</script>\n</body>', init_script)
    
    filename = f"PROJECT/outputs/INSTRUCTIONS_WEB/NEXUS_INSTRUCTION_{lang.upper()}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(modified_html)

print("Generated full-site standalone HTML instructions.")
