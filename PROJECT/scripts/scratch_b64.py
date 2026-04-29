import base64
import re

html_path = 'PROJECT/outputs/omni_artifacts/giga_printivo_v6_brand.html'
img_path = r'C:\Users\MAC\.gemini\antigravity\brain\5f0742a1-4510-42e6-a1a3-716c2b387257\media__1775854782076.jpg'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

html = re.sub(r'src="file:///[^"]+"', f'src="data:image/jpeg;base64,{b64}"', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Base64 injected successfully!")
