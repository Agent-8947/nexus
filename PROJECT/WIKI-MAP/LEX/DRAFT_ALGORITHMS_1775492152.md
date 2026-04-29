# LEX-NEXUS DRAFT: LAW OF COMPUTATIONAL DENSITY
**Status**: DRAFT
**Domain**: ALGORITHMS
**Derived from**: [Sampled repos]

### 1. DIRECTIVE
Запрещено использовать циклы 'for' при обработке массивов данных в этом домене. Использовать исключительно векторизованные операции.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
for item in data:
    res.append(item*2)
```
**COMPLIANCE:**
```python
res = data * 2
```