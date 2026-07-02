# Notion API Block Formats

When exporting to the Notion API (`POST https://api.notion.com/v1/pages`), format blocks using the children list:

## Heading 1
```json
{
  "object": "block",
  "type": "heading_1",
  "heading_1": {
    "rich_text": [{"type": "text", "text": {"content": "Heading Text"}}]
  }
}
```

## Paragraph
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"type": "text", "text": {"content": "Paragraph text content."}}]
  }
}
```

## Bulleted List Item
```json
{
  "object": "block",
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{"type": "text", "text": {"content": "List item text"}}]
  }
}
```

## Code Block
```json
{
  "object": "block",
  "type": "code",
  "code": {
    "rich_text": [{"type": "text", "text": {"content": "print('hello world')"}}],
    "language": "python"
  }
}
```
