/**
 * Site-wide configuration settings.
 * Edit these values to match your information.
 */
module.exports = {
    // Site title
    title: "My Personal Website",

    // Short site description
    description: "A personal website for my projects, thoughts, and curated links",

    // Your name
    author: "Your Name",

    // Current year for copyright notice
    copyrightYear: new Date().getFullYear(),

    // Base URL of your site (no trailing slash)
    url: "https://your-username.github.io",

    // Social media profiles
    social: {
        github: "https://github.com/your-username",
        twitter: "https://twitter.com/your-username",
        linkedin: "https://linkedin.com/in/your-username",
        instagram: "https://instagram.com/your-username"
    },

    // Navigation menu links
    // (You can edit these in the nav.njk component instead)
    navigation: [
        { label: "Home", url: "/" },
        { label: "Portfolio", url: "/projects/" },
        { label: "About", url: "/about/" },
        { label: "Links", url: "/links/" },
        { label: "Blog", url: "/posts/" }
    ],

    // Default featured image for social sharing
    // (Relative path from the root of your site)
    defaultImage: "/assets/images/default-social.jpg",

    // Default posts per page for pagination
    postsPerPage: 5
};