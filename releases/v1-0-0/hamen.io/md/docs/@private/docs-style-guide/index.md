<doc style="display: none;">
    title: Hamen Docs Style Guide
    titleID: hamen-docs-style-guide
    description: ...
    type: Blog
    tags: ...
    author: Daniel Hamen
    authorID: danielhamen
    date: 2023-08-14
    url: blogs/@private/docs-style-guide
    category: ...
    categorySlug: ...
</doc>

# Hamen Docs Style Guide

## Introduction

This article provides a comprehensive overview of the various components and elements supported within the Docs documentation platform.

## Paragraphs

Paragraphs consist of plain text and are defined by simply typing out the content. For instance:

```markdown
Lorem ipsum; this is a paragraph
```

## Lists

Lists, both ordered and unordered, offer an effective means of organizing content. Here are examples of both types:

- This is an unordered list

- This is another item in the unordered list

Additionally, nested lists are supported:

- Non-nested list item

:- Nested list item

The syntax for creating lists is as follows:

```markdown
&#45; List item 1
&#45; List item 2
&colon;- Sub-list item 1
&colon;- Sub-list item 2
&#45; List item 3
```

## Headings

Headings are used to define titles and delineate sections and subsections within a document. They are indicated using the `#` symbol, with `#` representing the largest heading (Heading 1, typically used for titles) and `######` representing the smallest (Heading 6).

```markdown
&num; Heading 1
&num;# Heading 2
&num;## Heading 3
&num;### Heading 4
&num;#### Heading 5
&num;##### Heading 6
```

## Code Blocks

Code blocks for various programming languages are supported, including Python, JavaScript, Markdown, XML, and a default option with no specific formatting.

If you require a language not listed here, you can request it using the "@UIHeader" decorator:

```markdown
&commat;UIHeader({ "requestLanguage": "C++" })
```

Moreover, code blocks are defined by:
```markdown
&grave;``&lt;LANGUAGE&gt;
...
&grave;``
```
Language names should be in lowercase and contain only alphanumeric characters; specifying a language is mandatory.

Finally, you can use the `language&colon;syntax` metadata specification to create a syntax-code-block:

```python:syntax
str.split(separator: str, max_split: int) -> list[str]
```

## Note

Notes are used to emphasize specific content within a document and come in three types: *INFO*, *WARNING*, and *ERROR*. Each type serves a distinct purpose. To create a note, use the following format:

- *INFO*
- *WARNING*
- *ERROR*

Use each type accordingly. For example:

```markdown
&excl;!!INFO/WARNING/ERROR
This text will be emphasized
&excl;!!
```

This code creates the following:

!!!NOTE
This is a note!
!!!


## Inline styles

Various inline text styles are supported, including **bold**, *italic*, :underline:, ~~strikethrough~~, and `inline code`. Here's how to apply each style:

- **Bold**: `&ast;&ast;bold&ast;&ast;`
- *Italic*: `&ast;Italic&ast;`
- :Underline:: `&colon;Underline&colon;`
- ~~Strikethrough~~: `&#126;&#126;Strikethrough&#126;&#126;`
- `Inline Code`: `&grave;Inline Code&grave;`

## Hyperlinks

Hyperlinks can be added with the following syntax

```markdown:syntax
(Text Content)&#x5b;"url"&#x5d;
```

!!!NOTE
It is imperative to use quotations wrapping your URL; furthermore, ensure to write the whole URL including the protocol (e.g. "https://"), subdomain (e.g. "www."), domain & top-level-domain (e.g. "hamen.io"), and any additional required parameters such as GET or naming anchor parameters
!!!

## Demo Article

If you would like to see the code of any article we offer, simply press `Ctrl+Shift+U` while on a `docs/blogs/` page, to open the GitHub source. Additionally, press `Ctrl+Shift+Alt+U` to open the actual markdown code file hosted on hamen.io.