# Evaluation Frameworks: AI Engineering Nexus

## ⚖️ AI-as-a-Judge (The "Meta-Reviewer")
**When to use**: Automated QA for generated content (Ads, Scripts, Code).
**Prompt Logic**:
1. Provide the source requirements.
2. Provide the generated output.
3. Ask the judge to score from 1-10 on:
   - **Accuracy**: Is it factually correct?
   - **Tone**: Does it match the Brand DNA?
   - **Structure**: Is the formatting correct?
4. Demand a "Reasoning" field for every score.

## ⏱ Performance Benchmarking
- **TTFT (Time to First Token)**: Target < 500ms for interactive agents.
- **Tokens/Sec**: Measure throughput for background batch jobs.
- **Cost Analysis**: Track $ per request. If cost > $0.05 per ad synthesis, investigate prompt compression.

## 🧪 Pairwise Comparison (A/B Testing)
**Process**:
1. Generate two variants (A and B) using different prompts or models.
2. Present both to a judge model.
3. Ask: "Which one is better for [Target Goal] and why?"
4. Track the "Win Rate" for specific prompt versions.

## 🛡 Safety & Alignment
- **Negative Constraints**: Test if the agent follows "DO NOT" rules.
- **Adversarial Testing**: Try to "jailbreak" or trick the agent into violating brand guidelines.
