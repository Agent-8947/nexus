import os
from crewai import Agent, Task, Crew, Process

# NEXUS Marketing Strategist
# Этот скрипт демонстрирует разделение ролей между агентами для создания маркетинговых материалов

def generate_marketing_kit(project_name="NEXUS IDE-optimus"):
    print(f"📣 Initializing Marketing Crew for {project_name}...")
    
    # Мы используем Anthropic (Claude 3.5) через langchain_anthropic
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("❌ Error: ANTHROPIC_API_KEY environment variable is not set.")
        return

    # Define Agents
    researcher = Agent(
        role='Market Research Analyst',
        goal=f'Analyze the competition and target audience for {project_name}',
        backstory='Expert in tech industry trends, developer tools, and SEO potential of Open Source projects.',
        verbose=True,
        allow_delegation=False
    )

    writer = Agent(
        role='Technical Content Strategist',
        goal=f'Write a compelling landing page copy and social media posts for {project_name}',
        backstory='Senior tech writer with a talent for translating complex backend features into "wow-effect" value propositions.',
        verbose=True,
        allow_delegation=False
    )

    # Define Tasks
    task1 = Task(
        description=f'Identify 3 key USPs (Unique Selling Points) of {project_name} and find 5 high-impact SEO keywords.',
        agent=researcher,
        expected_output="A list of 3 USPs and 5 SEO keywords for optimal discoverability."
    )

    task2 = Task(
        description=f'Using the research, create a catchy LinkedIn post and a "About" section for the landing page.',
        agent=writer,
        expected_output="A professional LinkedIn post and a concise 'About' section for a website."
    )

    # Instantiate the Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        process=Process.sequential,
        verbose=True
    )

    print("🚀 Crew is starting the mission...")
    result = crew.kickoff()
    
    output_path = os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "outputs", "marketing_kit.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# NEXUS Marketing Kit\n\n")
        f.write(str(result))
        
    print(f"✅ Marketing Kit generated and saved to: {output_path}")
    return result

if __name__ == "__main__":
    generate_marketing_kit()
