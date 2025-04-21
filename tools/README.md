# Tools Directory

This directory contains external tools and utilities used by the website but maintained in separate repositories.

## Contents

### 1. Vulnerability Blog Generator

Located in: `vuln-blog/`

This is a Git submodule that points to [williamzujkowski/vuln-post-generator](https://github.com/williamzujkowski/vuln-post-generator), which contains a comprehensive system for generating high-quality vulnerability analysis blog posts.

#### Key Features

- Multi-source vulnerability data collection (NVD, MITRE, CERT/CC, ZDI, VulDB, etc.)
- Multi-model support (OpenAI, Google Gemini, Anthropic Claude)
- Retrieval-Augmented Generation (RAG) for enhanced context
- Token optimization strategies
- Secure credential management through GitHub Secrets

#### Integration

The vulnerability blog generator is integrated with the website through:

1. GitHub Actions workflows:

   - `.github/workflows/vulnerability-posts.yml`
   - `.github/workflows/test-llm-providers.yml`

2. NPM scripts:
   ```json
   "generate:vuln": "cd tools/vuln-blog && node generate-vuln-post.js --",
   "generate:latest": "cd tools/vuln-blog && node generate-vuln-post.js --latest",
   "schedule:vuln": "cd tools/vuln-blog && node schedule-posts.js",
   ```

#### Updating the Submodule

To update the submodule to the latest version:

```bash
git submodule update --remote tools/vuln-blog
git add tools/vuln-blog
git commit -m "Update vulnerability blog generator to latest version"
```

#### Working with the Submodule

When cloning this repository, use:

```bash
git clone --recursive https://github.com/williamzujkowski/williamzujkowski.github.io.git
```

Or, if you've already cloned the repository:

```bash
git submodule update --init --recursive
```
