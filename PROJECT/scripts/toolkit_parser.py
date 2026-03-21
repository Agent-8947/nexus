import re
import json
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    return re.sub(r'-+', '-', text).strip('-')

def parse_markdown_tables(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by headers
    sections = re.split(r'\n## ', content)
    data = {}

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        section_name = lines[0].strip()
        
        # Skip garbage sections
        if section_name.lower() in ["quick links", "stay updated", "related repositories", "star history", "llm interview questions and answers book"]:
            continue

        items = []
        # Find tables
        table_rows = re.findall(r'\|(.*?)\|(.*?)\|(.*?)\|', section)
        for row in table_rows:
            name = row[0].strip()
            # Remove Markdown links from name if present, e.g. [unsloth](...) -> unsloth
            clean_name = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', name)
            # Remove emojis
            clean_name = re.sub(r'[^\w\s\-\.]', '', clean_name).strip()
            
            desc = row[1].strip()
            link_match = re.search(r'\(?(https?://[^\s\)]+)\)?', row[2])
            link = link_match.group(1) if link_match else row[2].strip()
            
            # Skip header rows and separators
            if clean_name.lower() in ['library', '---', ''] or all(c in '- ' for c in clean_name):
                continue
            
            # Additional cleanup for description
            desc = re.sub(r'\[Link\]\(.*?\)', '', desc).strip()
            
            items.append({
                "name": clean_name,
                "slug": slugify(clean_name),
                "original_description": desc,
                "url": link
            })
            
        if items:
            data[section_name] = items
            
    return data

def main():
    root_path = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT'
    readme_path = os.path.join(root_path, 'llm-engineer-toolkit', 'README.md')
    output_path = os.path.join(root_path, 'LLM-TOOLKIT-PORTAL', 'src', 'data', 'toolkit_raw.json')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    raw_data = parse_markdown_tables(readme_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
    print(f"Parsed {sum(len(v) for v in raw_data.values())} libraries into {output_path}")

if __name__ == "__main__":
    main()
