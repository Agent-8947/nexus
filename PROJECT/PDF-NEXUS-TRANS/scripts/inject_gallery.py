import os, re

deploy_dir = r"E:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\NEXUS-MANUALS-DEPLOY"

for manual in ['k10', 'e06']:
    html_file = os.path.join(deploy_dir, manual, 'index.html')
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    img_dir = os.path.join(deploy_dir, manual, 'images')
    all_imgs = [img for img in os.listdir(img_dir) if img.endswith('.png')]
    valid_imgs = [img for img in all_imgs if os.path.getsize(os.path.join(img_dir, img)) > 5000]
    
    used_imgs = re.findall(r'src="images/(img_p\d+_\d+\.png)"', html)
    missing = [img for img in valid_imgs if img not in used_imgs]
    
    print(f"{manual.upper()}: {len(used_imgs)} used, {len(missing)} missing")
    if missing:
        gallery_html = '<!-- ═════ ГАЛЕРЕЯ ═════ -->\n<div class="content-block" id="ch-gallery" data-block="ch-gallery">\n<div class="block-header"><span class="block-num">Галерея</span><span class="block-title">Дополнительные иллюстрации</span></div>\n<div class="block-body">\n<div class="img-grid">\n'
        for img in sorted(missing):
            gallery_html += f'<div class="img-card"><img src="images/{img}" loading="lazy" onclick="zoom(this.src)" alt="">\n<div class="img-cap">Иллюстрация {img.split(".")[0].replace("img_","")}</div></div>\n'
        gallery_html += '</div>\n</div></div>\n</main>'
        
        new_html = html.replace('</main>', gallery_html)
        nav_link = '<a href="#ch-gallery" data-id="ch-gallery">Иллюстрации</a>\n</nav>'
        new_html = new_html.replace('</nav>', nav_link)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Updated {manual}")
