/**
 * Prompt Injection Detection Patterns
 */
export const INJECTION_PATTERNS = [
  // Direct instruction override
  {
    name: 'Ignore instructions',
    pattern: /ignore\s+(all\s+)?(previous|prior|above|system)\s+(instructions?|prompts?|rules?)/i,
    severity: 'high',
  },
  {
    name: 'Disregard instructions',
    pattern: /disregard\s+(all\s+)?(previous|prior|above|system)/i,
    severity: 'high',
  },
  // System prompt extraction
  {
    name: 'System prompt request',
    pattern: /what\s+(is|are)\s+(your|the)\s+(system\s+)?(prompt|instructions?|rules?)/i,
    severity: 'medium',
  },
  {
    name: 'Repeat instructions',
    pattern: /repeat\s+(your|the|all|everything)\s+(system\s+)?(instructions?|prompts?|above)/i,
    severity: 'high',
  },
  // Jailbreak attempts
  {
    name: 'DAN mode',
    pattern: /\b(DAN|do\s+anything\s+now)\b/i,
    severity: 'high',
  },
  {
    name: 'Developer mode',
    pattern: /\b(developer|dev)\s+mode/i,
    severity: 'high',
  },
  {
    name: 'Jailbreak',
    pattern: /\bjailbreak\b/i,
    severity: 'high',
  }
];

export function containsInjectionAttempt(userInput) {
  const lowerInput = userInput.toLowerCase();
  for (const item of INJECTION_PATTERNS) {
    if (item.pattern.test(lowerInput)) {
      return { found: true, pattern: item.name, severity: item.severity };
    }
  }
  return { found: false };
}
