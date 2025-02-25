---
title: Getting Started with 11ty
description: A beginner's guide to setting up and using Eleventy for static site generation.
date: 2024-05-01
tags:
  - posts
  - development
  - 11ty
  - tutorial
layout: layouts/post.njk
---

# Getting Started with 11ty

[Eleventy (11ty)](https://www.11ty.dev/) is a simple static site generator that transforms a directory of templates into HTML. Unlike other JavaScript frameworks, Eleventy works with your project's existing directory structure.

## Why Choose 11ty?

There are several reasons why 11ty has become a popular choice for developers:

1. **Zero client-side JavaScript requirements**
2. **Flexible templating options** (supports multiple languages)
3. **Fast build times**
4. **Simple and intuitive API**
5. **Great documentation and community support**

## Basic Setup

Let's walk through setting up a basic 11ty project:

```bash
# Create a new directory for your project
mkdir my-11ty-site
cd my-11ty-site

# Initialize a new npm project
npm init -y

# Install 11ty
npm install @11ty/eleventy --save-dev
```

## Creating Your First Page

Create an `index.md` file in your project root:

```markdown
---
title: My First 11ty Site
---

# {{ title }}

Welcome to my website built with 11ty!
```

## Running the Development Server

Add the following scripts to your `package.json`:

```json
"scripts": {
  "start": "eleventy --serve",
  "build": "eleventy"
}
```

Now you can run:

```bash
npm start
```

This will start a local development server, usually at `http://localhost:8080`.

## Next Steps

From here, you can:

- Create more pages
- Add layouts and includes
- Configure collections
- Customize your build process

11ty's flexibility makes it suitable for a wide range of projects, from simple blogs to complex documentation sites.

Stay tuned for more tutorials on advanced 11ty features!
