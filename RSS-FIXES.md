# RSS Feed Issues and Fixes

After investigating the RSS/Atom feed, we've identified two issues:

## 1. Syntax Error in feed.njk Template

The following line in `src/feed.njk` contains a syntax error:

```njk
<updated>{{ collections.posts  < /dev/null  < /dev/null |   getNewestCollectionItemDate | dateToRfc3339 }}</updated>
```

The `< /dev/null |` part is causing a Nunjucks parse error. It should be:

```njk
<updated>{{ collections.posts | getNewestCollectionItemDate | dateToRfc3339 }}</updated>
```

## 2. Non-Standard Author Tag Format

The Atom feed specification (RFC 4287) requires `<name>` tags for author names, but the current template uses `<n>` tags:

```xml
<author>
  <n>{{ site.author }}</n>
  <email>{{ site.email }}</email>
</author>
```

It should be:

```xml
<author>
  <name>{{ site.author }}</name>
  <email>{{ site.email }}</email>
</author>
```

## How to Fix

To fix these issues, replace your current `src/feed.njk` file with:

```njk
---
permalink: /feed.xml
eleventyExcludeFromCollections: true
---

<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{{ site.title }}</title>
  <subtitle>{{ site.description }}</subtitle>
  <link href="{{ site.url }}/feed.xml" rel="self" />
  <link href="{{ site.url }}" />
  <updated>{{ collections.posts | getNewestCollectionItemDate | dateToRfc3339 }}</updated>
  <id>{{ site.url }}</id>
  <author>
    <name>{{ site.author }}</name>
    <email>{{ site.email }}</email>
  </author>
  {%- for post in collections.posts | reverse %} {% set absolutePostUrl %}{{ site.url
  }}{{ post.url }}{% endset %}
  <entry>
    <title>{{ post.data.title }}</title>
    <link href="{{ absolutePostUrl }}" />
    <updated>{{ post.date | dateToRfc3339 }}</updated>
    <id>{{ absolutePostUrl }}</id>
    <content type="html">
      {% if post.templateContent %} {{ post.templateContent |
      htmlToAbsoluteUrls(absolutePostUrl) }} {% else %}
      <p>No content available</p>
      {% endif %}
    </content>
  </entry>
  {%- endfor %}
</feed>
```

After making these changes, your feed will be valid and compliant with the Atom specification.
