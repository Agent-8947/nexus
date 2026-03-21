# NEXUS JavaScript Code Quality Standard (Gold Standard 2026)

This standard is based on the [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript) principles. All JS/TS code within the **NEXUS** project MUST adhere to these rules.

## Core Directives

### 1. Variables & Naming

- **Use meaningful and pronounceable names.** Avoid `data`, `info`, `item`, `val`.
- **Avoid Mental Mapping.** No single-letter variables in complex logic.
- **No Unneeded Context.** If the class is `User`, don't name the variable `userName`; use `name`.

### 2. Functions

- **Small and Focused.** Functions must do exactly one thing.
- **No Side Effects.** Functions should not mutate global state.
- **Arguments Limit.** Maximum 2 arguments. Use objects for more.
- **One Level of Abstraction.** Don't mix low-level details (e.g., regex) with high-level logic in the same function.

### 3. Concurrency

- **Modern Syntax.** Use `async/await` exclusively. `Promise.then()` is considered Legacy for NEXUS.

### 4. Logic & Conditionals

- **Encapsulate Conditionals.** `if (shouldShowSpinner(state, user))` vs `if (state === 'loading' && !user.isSilent)`.
- **Avoid Negative Conditionals.** Use `isNotBlocked` instead of `!isBlocked` if possible.

## Integration with Adversarial Reviewer

The `adversarial-reviewer` script leverages these rules to validate all JavaScript/TypeScript components before they are accepted into the `PROJECT/` core.

## Maintenance

*Maintained by: NEXUS Meta-Agent: Polymorph*
