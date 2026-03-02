import os
import re
import shutil
import json
from pathlib import Path

class SkillMigrator:
    def __init__(self, source_dir, output_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.stats = {"processed": 0, "errors": 0}

    def sanitize_name(self, name):
        # mgechev rule: 1-64 chars, lowercase, numbers, hyphens only
        name = name.lower()
        name = re.sub(r'[^a-z0-9\-]', '-', name)
        name = re.sub(r'-+', '-', name)
        return name[:64].strip('-')

    def parse_skill_md(self, content):
        # Extract frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        frontmatter = fm_match.group(1) if fm_match else ""
        body = content[fm_match.end():] if fm_match else content

        # Split into sections based on typical headers
        sections = {}
        current_section = "General"
        
        # Split by markdown headers
        lines = body.split('\n')
        for line in lines:
            header_match = re.match(r'^#+\s+(.*)', line)
            if header_match:
                current_section = header_match.group(1).strip()
                sections[current_section] = []
            else:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line)

        # Merge lines back to strings
        for sec in sections:
            sections[sec] = '\n'.join(sections[sec]).strip()

        return frontmatter, sections

    def migrate_skill(self, skill_path):
        try:
            skill_md_path = skill_path / "SKILL.md"
            if not skill_md_path.exists():
                return

            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter, sections = self.parse_skill_md(content)
            
            # Identify skill name from frontmatter or folder
            skill_name = self.sanitize_name(skill_path.name)
            
            # Create new structure
            new_skill_dir = self.output_dir / skill_name
            os.makedirs(new_skill_dir / "references", exist_ok=True)
            os.makedirs(new_skill_dir / "assets", exist_ok=True)
            os.makedirs(new_skill_dir / "scripts", exist_ok=True)

            # Move heavy sections to references
            ref_links = []
            for section_title, section_body in list(sections.items()):
                if len(section_body.split('\n')) > 10 or section_title in ["Capabilities", "Knowledge Base", "Behavioral Traits"]:
                    ref_file = self.sanitize_name(section_title) + ".md"
                    with open(new_skill_dir / "references" / ref_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {section_title}\n\n{section_body}")
                    ref_links.append(f"- `references/{ref_file}`: {section_title}")
                    del sections[section_title]

            # Generate lean SKILL.md
            new_content = [f"---\n{frontmatter}\n---\n", f"# {skill_path.name}\n"]
            
            if "Instructions" in sections or "Procedures" in sections:
                new_content.append("## Procedures\n")
                new_content.append(sections.get("Instructions", sections.get("Procedures", "1. Analyize requirement\n2. Execute logic.")))
            else:
                new_content.append("## Procedures\n1. Analyze input.\n2. Apply domain knowledge from references.\n")

            if ref_links:
                new_content.append("\n## References\n")
                new_content.append('\n'.join(ref_links))

            with open(new_skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_content))

            self.stats["processed"] += 1
        except Exception as e:
            print(f"Error migrating {skill_path.name}: {e}")
            self.stats["errors"] += 1

    def run(self, limit=None):
        skills = [d for d in self.source_dir.iterdir() if d.is_dir()]
        processed_count = 0
        
        for skill_dir in skills:
            if limit and processed_count >= limit:
                break
            print(f"Migrating: {skill_dir.name}...")
            self.migrate_skill(skill_dir)
            processed_count += 1
        
        print(f"\nMigration Finished!")
        print(f"Processed: {self.stats['processed']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Output: {self.output_dir}")

if __name__ == "__main__":
    SOURCE = r"E:\Downloads\--skill-agt — 002\antigravity-awesome-skills\--0000 archive\skills"
    OUTPUT = r"E:\Downloads\--skill-agt — 002\antigravity-awesome-skills\skills-pro-nexus"
    
    migrator = SkillMigrator(SOURCE, OUTPUT)
    # Process all skills
    migrator.run()
