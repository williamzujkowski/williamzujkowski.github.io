## README.md


# William Zujkowski’s Personal Website

Welcome to the repository for my personal website, [grenlan.com](https://grenlan.com)! I built it to showcase my
professional background as a cybersecurity engineer, share blog posts, and provide some fun tools like a pizza
calculator and a coffee calculator. This is a modern, lightweight static site that uses JavaScript to dynamically load
navigation, footers, and blog content.

## Key Features

- **Dynamic Navigation & Footer**
All pages include a dynamic nav and footer, generated from a single, consolidated `main.js` file.

- **Unified Calculators**
I have a fun Pizza Calculator and a Coffee Calculator, both consolidated in the single `main.js` script.
- *Pizza Calculator* helps me figure out how many slices my developer friends and I need after hours of debugging.
- *Coffee Calculator* estimates how many cups (or pots!) of coffee are needed to fuel late-night coding sessions.

- **Blog Section**
- My blog posts are stored in `blog_data.html`.
- The site fetches and renders them dynamically, so the main pages remain clean and minimal.

- **Secret Toggles**
I’ve included a Konami Code Easter egg for a bit of geeky fun. See if you can find it on the homepage!

## File Structure

After consolidating scripts, the repository looks like this:

```
.
├── about.html
├── assets
│ ├── css
│ │ └── styles.css
│ ├── images
│ │ ├── favicon.ico
│ │ ├── profile.png
│ │ └── simpson_profile.png
│ └── js
│ └── main.js
├── blog_data.html
├── blog.html
├── coffee.html
├── index.html
├── pizza.html
└── README.md
```

### How to Use or Contribute

1. **Clone or Download**
Feel free to clone this repository or download the files and open them in your favorite IDE or text editor.

2. **Serve Locally**
Because it’s a static site, you can simply open the `.html` files in your browser. To see dynamic features (like blog
fetching) work reliably, consider serving it via a local server (e.g., using `python3 -m http.server 8080` or similar).

3. **Suggest Improvements**
I love feedback! If you have suggestions, open a pull request or file an issue.

4. **Have Fun!**
This site includes silly features for pizza ordering, coffee consumption estimates, and a hidden Easter egg. Enjoy
exploring.

---

**Thanks for checking out my website’s source code.**
If you’d like to chat about cybersecurity, HPC solutions, DevSecOps, or AI/ML in security automation, feel free to reach
out!
