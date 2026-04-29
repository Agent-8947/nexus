# NEXUS FAULT REGISTRY

| Date | Category | Error Description | Root Cause | Fix Applied | Status |
|      |          |                   |            |             |        |
| 2026-04-11 | PATH_ENCODING | Fail to copy/render media from Cyrillic path "Новая папка" | Shell/Python encoding mismatch on non-standard paths | Using raw path strings and absolute OS paths in delivery scripts | FIXED |

## Incident Report: [2026-04-11_02:42] 
- **Goal**: Deliver synthesized MP4 to User Chat.
- **Fail**: Consecutive FileNotFoundError during manual delivery.
- **Learning**: Avoid Cyrillic names for core production folders. Always use Pathlib for inter-directory operations.
