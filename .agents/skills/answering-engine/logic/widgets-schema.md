# Widget Schema

## Stock Widget
```json
{
  "type": "widget",
  "name": "Stock",
  "props": {
    "symbol": "string",
    "name": "string",
    "price": "number",
    "change": "string",
    "currency": "string"
  }
}
```

## Weather Widget
```json
{
  "type": "widget",
  "name": "Weather",
  "props": {
    "location": "string",
    "temperature": "number",
    "condition": "string",
    "humidity": "number"
  }
}
```

## Layout Principle
Widgets should appear at the top of the response (Message Preamble) when relevant to provide quick-glance data before the detailed text answer.
