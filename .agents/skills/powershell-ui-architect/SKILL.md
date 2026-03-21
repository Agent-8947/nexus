# Skill: PowerShell UI Architect

## Overview
Use for admin-oriented interactive tooling, terminal UIs (TUI), and WinForms/WPF integration in Windows environments. Focus on developer productivity and workflow reliability.

## Working Mode
1. **Pain Point Mapping**: Identify friction in current CLI/Terminal workflows.
2. **TUI/WPF Implementation**: Build or recommend the smallest coherent UI intervention.
3. **Safety Boundaries**: Ensure input validation and safe execution for privileged operations.
4. **Validation**: Test normal, failure, and cancellation paths.

## Focus Areas
- **Interactive Flows**: Designing for terminal-first interaction in the NEXUS dashboard.
- **Background Jobs**: Handling long-running tasks without freezing the UI.
- **Error Feedback**: Clarity in operator recovery paths.
- **Separation of Concerns**: Logic vs. Presentation in PowerShell modules.

## Quality Checks
- Verify background task handling (runspaces).
- Check that privileged actions require confirmation.
- Ensure terminal output supports troubleshooting.

## Returns
- PowerShell script/module changes.
- Workflow boundary analysis.
- Residual risk and prioritized follow-ups.
