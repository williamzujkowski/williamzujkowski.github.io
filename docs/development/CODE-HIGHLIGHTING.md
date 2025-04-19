# Code Block Syntax Highlighting Guide

This document provides guidance on correctly formatting code blocks in markdown files to ensure proper syntax highlighting in our 11ty website.

## The Issue

We identified an issue where code blocks were sometimes displaying with incorrect syntax highlighting. In particular, some code blocks showed a language identifier of `####` instead of the actual language name, resulting in no syntax highlighting.

## Root Cause Analysis

The problem was caused by improperly formatted code fences in the markdown files:

1. **Missing language identifier**: Some code blocks didn't specify a language after the opening backticks (` ``` `).

2. **Malformed code blocks**: In some cases, the closing backticks of one code block and the opening backticks of the next code block were not properly separated by a blank line, causing content between them to be interpreted as part of the language identifier.

3. **Special characters**: Certain special characters like underscores (\_) and asterisks (\*) were not being properly escaped in code blocks, causing formatting issues.

## How to Fix

When creating code blocks in markdown files, follow these guidelines:

### 1. Always specify a language identifier

````markdown
<!-- GOOD: Specify a language -->

```javascript
const message = "Hello, world!";
console.log(message);
```
````

<!-- BAD: No language specified -->

```
const message = "Hello, world!";
console.log(message);
```

````

Common language identifiers:
- `javascript` (or `js`)
- `typescript` (or `ts`)
- `python`
- `java`
- `csharp` (or `cs`)
- `html`
- `css`
- `json`
- `yaml` (or `yml`)
- `bash` (or `sh`)
- `sql`
- `xml`
- `markdown` (or `md`)

For ASCII art or plain text, use `ascii` or `text`.

### 2. Use proper spacing between code blocks

```markdown
<!-- GOOD: Proper spacing between code blocks -->
```javascript
const firstExample = "This is the first code block";
````

```python
second_example = "This is the second code block"
```

<!-- BAD: No space between code blocks -->

```javascript
const firstExample = "This is the first code block";
```

```python
second_example = "This is the second code block"
```

````

### 3. Format code with proper indentation

For better readability and maintenance, format your code with proper indentation and line breaks:

```markdown
<!-- GOOD: Well-formatted code -->
```javascript
function calculateTotal(items) {
  return items
    .filter(item => item.inStock)
    .reduce((total, item) => {
      return total + (item.price * item.quantity);
    }, 0);
}
````

<!-- BAD: Poorly formatted code -->

```javascript
function calculateTotal(items) {
  return items
    .filter((item) => item.inStock)
    .reduce((total, item) => {
      return total + item.price * item.quantity;
    }, 0);
}
```

````

### 4. Escape special characters

If you need to include characters that have special meaning in markdown (like asterisks or underscores) in your code blocks, either:

1. Use the standard code fence which should correctly preserve these characters
2. Escape them with a backslash if needed: `\*` for * and `\_` for _

## Troubleshooting Existing Issues

If you encounter a page with broken syntax highlighting:

1. Check the markdown source file for the affected code blocks
2. Ensure each code block has proper language specification
3. Add blank lines between consecutive code blocks
4. Format the code for better readability
5. Verify that Markdown's formatting characters aren't interfering with the code

## Implementation Details

Our site uses the official [Eleventy Syntax Highlight Plugin](https://www.11ty.dev/docs/plugins/syntaxhighlight/) which is based on [Prism.js](https://prismjs.com/) for syntax highlighting. The plugin is configured in `.eleventy.cjs`:

```javascript
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
// ...
eleventyConfig.addPlugin(syntaxHighlight);
````

## Additional Resources

- [Eleventy Syntax Highlighting Documentation](https://www.11ty.dev/docs/plugins/syntaxhighlight/)
- [PrismJS Documentation](https://prismjs.com/)
- [Markdown Guide - Code Blocks](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks)
