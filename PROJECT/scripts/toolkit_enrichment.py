import json
import os

def enrich_major_tools():
    root_path = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\LLM-TOOLKIT-PORTAL\src\data\locales'
    
    enrichments = {
        "unsloth": {
            "en": {
                "use_case": "Perfect for training your own model on a single consumer GPU (like RTX 3090/4090) without waiting for days.",
                "full_desc": "Unsloth makes LLM fine-tuning 2x faster and uses 70% less memory. It's the 'turbo boost' for training models like Llama 3 or Mistral.",
                "example": "from unsloth import FastLanguageModel\nmodel, tokenizer = FastLanguageModel.from_pretrained('unsloth/llama-3-8b-bnb-4bit')\n# Now just train it like a normal model, but 2x faster!"
            },
            "uk": {
                "use_case": "Ідеально підходить для навчання власної моделі на одній домашній відеокарті (наприклад, RTX 3090/4090), не чекаючи днями.",
                "full_desc": "Unsloth робить донавчання LLM у 2 рази швидшим і споживає на 70% менше пам'яті. Це як 'турбо-режим' для тренування моделей типу Llama 3 або Mistral.",
                "example": "from unsloth import FastLanguageModel\nmodel, tokenizer = FastLanguageModel.from_pretrained('unsloth/llama-3-8b-bnb-4bit')\n# Тепер просто тренуйте як звичайну модель, але вдвічі швидше!"
            },
            "ru": {
                "use_case": "Идеально подходит для обучения собственной модели на одной домашней видеокарте (например, RTX 3090/4090), не дожидаясь днями.",
                "full_desc": "Unsloth делает дообучение LLM в 2 раза быстрее и потребляет на 70% меньше памяти. Это как 'турбо-режим' для тренировки моделей типа Llama 3 или Mistral.",
                "example": "from unsloth import FastLanguageModel\nmodel, tokenizer = FastLanguageModel.from_pretrained('unsloth/llama-3-8b-bnb-4bit')\n# Теперь просто тренируйте как обычную модель, но в два раза быстрее!"
            }
        },
        "langchain": {
            "en": {
                "use_case": "Use this when you want to connect an LLM to your own data, tools, or create a complex sequence of actions (chains).",
                "full_desc": "LangChain is the 'Lego set' of the AI world. It gives you all the blocks (connectors, memory, prompts) to build a production-ready AI app.",
                "example": "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_template('Tell me a joke about {topic}')\nmodel = ChatOpenAI()\nchain = prompt | model\nprint(chain.invoke({'topic': 'bears'}))"
            },
            "uk": {
                "use_case": "Використовуйте це, коли хочете підключити LLM до своїх даних, інструментів або створити складну послідовність дій (ланцюжки).",
                "full_desc": "LangChain — це 'набір Lego' у світі AI. Він дає вам усі блоки (конектори, пам'ять, промпти) для створення готового до продакшену додатка.",
                "example": "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_template('Розкажи анекдот про {topic}')\nmodel = ChatOpenAI()\nchain = prompt | model\nprint(chain.invoke({'topic': 'медведів'}))"
            },
            "ru": {
                "use_case": "Используйте это, когда хотите подключить LLM к своим данным, инструментам или создать сложную последовательность действий (цепочки).",
                "full_desc": "LangChain — это 'набор Lego' в мире AI. Он дает вам все блоки (коннекторы, память, промпты) для создания готового к продакшену приложения.",
                "example": "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_template('Расскажи анекдот про {topic}')\nmodel = ChatOpenAI()\nchain = prompt | model\nprint(chain.invoke({'topic': 'медведей'}))"
            }
        },
        "crewai": {
          "en": {
            "use_case": "When one AI agent is not enough. Create a 'company' of agents: researchers, writers, and reviewers working together.",
            "full_desc": "CrewAI automates group dynamics. You define roles (e.g. 'Senior Researcher') and tasks, and the agents coordinate to deliver a final report.",
            "example": "from crewai import Agent, Task, Crew\nresearcher = Agent(role='Researcher', goal='Find AI news')\ntask = Task(description='Write a summary', agent=researcher)\ncrew = Crew(agents=[researcher], tasks=[task])\nresult = crew.kickoff()"
          },
          "uk": {
            "use_case": "Коли одного AI-агента замало. Створіть 'компанію' агентів: дослідників, письменників та редакторів, що працюють разом.",
            "full_desc": "CrewAI автоматизує групову динаміку. Ви визначаєте ролі (наприклад, 'Старший дослідник') та завдання, а агенти самі координуються для звіту.",
            "example": "from crewai import Agent, Task, Crew\nresearcher = Agent(role='Дослідник', goal='Знайти новини AI')\ntask = Task(description='Написати звіт', agent=researcher)\ncrew = Crew(agents=[researcher], tasks=[task])\nresult = crew.kickoff()"
          },
          "ru": {
            "use_case": "Когда одного AI-агента недостаточно. Создайте 'компанию' агентов: исследователей, писателей и редакторов, работающих вместе.",
            "full_desc": "CrewAI автоматизирует групповую динамику. Вы определяете роли (например, 'Старший исследователь') и задачи, а агенты сами координируются для отчета.",
            "example": "from crewai import Agent, Task, Crew\nresearcher = Agent(role='Исследователь', goal='Найти новости AI')\ntask = Task(description='Написать отчет', agent=researcher)\ncrew = Crew(agents=[researcher], tasks=[task])\nresult = crew.kickoff()"
          }
        }
    }

    for lang in ['en', 'uk', 'ru']:
        file_path = os.path.join(root_path, f'{lang}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for section, items in data.items():
            for item in items:
                if item['slug'] in enrichments:
                    enrichment = enrichments[item['slug']][lang]
                    item.update(enrichment)
                    
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    print("Enriched major tools with 'down-to-earth' content.")

if __name__ == "__main__":
    enrich_major_tools()
