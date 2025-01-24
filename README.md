# My Personal Website (grenlan.com)

Welcome to the repository of **my personal website**! I built this site to showcase my work as a software engineer,
share articles on technology, and experiment with fun interactive tools.

Key features of my static site include:
- **Dynamic Navigation** and **Footer** generation (via `navFooter.js`)
- **Pizza Calculator** and **Coffee Calculator** (with localStorage integration)
- A **Blog** section that loads content from `blog_data.html` (using a small fetch/render library)
- **Secret toggles** (Konami code, etc.)

I maintain this repository with an eye toward accessibility, performance, and modern web standards.

## Folder Structure

```
.
├── about.html
├── assets
│   ├── images
│   │   ├── favicon.ico
│   │   ├── profile.png
│   │   └── simpson_profile.png
│   ├── js
│   │   ├── blogLogic.js
│   │   ├── coffeeCalc.js
│   │   ├── main.js
│   │   ├── navFooter.js
│   │   ├── pizzaCalc.js
│   │   └── secretToggles.js
├── blog_data.html
├── blog.html
├── coffee.html
├── css
│   └── main.css
├── index.html
├── pizza.html
└── README.md
```

> **Note:** `blog_data.html` is where I keep my blog post content, but you can skip editing or viewing it per the
instructions.

Feel free to open an issue if you spot bugs or have suggestions on how I can improve the site further!
```