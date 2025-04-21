# Vulnerability Blog Generator Integration

The Vulnerability Blog Generator has been moved to its own repository to maintain clean separation of concerns, preserve history, and enable independent development.

## Integration Guide

This document explains how to integrate the separate vulnerability blog generator repository with your website.

### Option 1: Git Submodule (Recommended)

This approach keeps the blog generator code separate yet version-controlled within your website repo.

1. Clone the vulnerability blog generator repository:

   ```bash
   git submodule add https://github.com/yourusername/vuln-post-generator.git tools/vuln-blog
   git submodule update --init --recursive
   ```

2. Update your GitHub Actions workflow:

   ```yaml
   # In .github/workflows/vulnerability-posts.yml
   steps:
     - uses: actions/checkout@v4
       with:
         submodules: recursive

     - name: Setup Node.js
       uses: actions/setup-node@v4
       with:
         node-version: "18"

     - name: Generate Vulnerability Posts
       run: |
         cd tools/vuln-blog
         npm install
         node generate-vuln-post.js --latest
   ```

3. Document submodule workflow in your README:

   ````markdown
   To clone this repository including all submodules:

   ```bash
   git clone --recursive https://github.com/yourusername/website-repo.git
   ```
   ````

   ```

   ```

### Option 2: NPM Package

If you prefer to use the blog generator as an npm package:

1. Add the package to your dependencies:

   ```bash
   npm install --save github:yourusername/vuln-post-generator
   ```

2. Use the package in your code:

   ```javascript
   const { generateVulnerabilityPost } = require("vuln-post-generator");

   async function runGenerator() {
     await generateVulnerabilityPost({
       cve: "CVE-2023-12345",
       provider: "openai",
       outputDir: "./content/posts/",
     });
   }
   ```

### Option 3: Copy Generated Posts

You can set up a workflow that runs the generator in a separate repository and copies the output to your website:

1. In the vulnerability blog generator repository, set up a GitHub Action to generate posts and upload them as artifacts.

2. In your website repository, set up a GitHub Action to download the artifacts and include them in your site build.

## Transferring API Keys

Remember to transfer all your API keys from the website repository to the new vulnerability blog generator repository:

1. Go to Settings → Secrets and variables → Actions in both repositories
2. Add all necessary API keys to the new repository
3. Consider rotating your API keys for security

## Troubleshooting

If you encounter issues with the integration:

1. Verify the submodule is correctly initialized and updated
2. Check that your GitHub Secrets are correctly configured in the new repository
3. Test the generator locally before integrating with your website
4. Consult the documentation in the vulnerability blog generator repository

## Maintaining Updates

To keep your integrated copy up to date:

```bash
# Update the submodule to the latest version
git submodule update --remote tools/vuln-blog
git add tools/vuln-blog
git commit -m "Update vulnerability blog generator to latest version"
```

## Further Resources

- [Vulnerability Blog Generator Repository](https://github.com/yourusername/vuln-post-generator)
- [GitHub Submodule Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
