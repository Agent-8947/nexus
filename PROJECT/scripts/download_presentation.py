import urllib.request
with urllib.request.urlopen('https://nexus-presentation-v2.vercel.app/') as response:
    html = response.read().decode('utf-8')
    with open('tmp_presentation.html', 'w', encoding='utf-8') as f:
        f.write(html)
