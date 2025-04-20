# Vulnerability Blog Post Generator

This directory contains tools to automatically generate vulnerability analysis blog posts for williamzujkowski.github.io. The system is designed to produce high-quality vulnerability summaries with a focus on critical CVEs relevant to AWS PaaS providers.

## Features

- Generate detailed vulnerability analysis blog posts using an LLM
- Supports multiple LLM providers:
  - OpenAI GPT-4 Turbo
  - Google Gemini 2.0 Flash
  - Anthropic Claude 3 Opus
- Focus on cloud-relevant security issues
- Include threat actor information when available
- Maintain a regular posting schedule (maximum once daily, minimum weekly rollup)
- Automatically format posts for the blog's requirements
- CI/CD integration via GitHub Actions

## Setup

1. Install dependencies:

   ```
   npm install
   ```

2. Create an environment file:

   ```
   cp .env.sample .env
   ```

3. Edit `.env` and add your OpenAI API key.

4. (Optional) Set up the daily cron job:
   ```
   ./setup-cron.sh
   ```

## Usage

### Manual Generation

To generate a post for a specific CVE:

```
node generate-vuln-post.js --cve CVE-2023-XXXXX
```

To generate a post for the latest critical vulnerability:

```
node generate-vuln-post.js --latest
```

To generate a weekly rollup:

```
node generate-vuln-post.js --weekly
```

### Automated Scheduling

The scheduler can be run manually:

```
node schedule-posts.js
```

Or automatically via the installed cron job, which runs daily and determines whether a new post should be generated based on the configured frequency.

### Testing LLM Providers

To test your LLM provider configuration:

```
# Test OpenAI configuration
npm run test-openai

# Test Gemini configuration
npm run test-gemini

# Test Claude configuration
npm run test-claude

# Test all providers
npm run test-models
```

These tests will send a simple prompt to the specified LLM provider(s) and display the response, allowing you to verify your API keys and compare the output quality between providers.

You can also run the test workflow in GitHub Actions to verify your API key setup in the repository secrets.

## Customization

The vulnerability selection criteria and blog post format are defined in:

- `/home/william/git/williamzujkowski.github.io/Prompts/threat-blog-post.prompt`

You can modify this file to adjust the focus, style, or content structure of the generated posts.

## Logs

- `vulnerability-posts.log` - Records when posts are generated
- `cron.log` - Contains the output from the scheduled cron job

## Maintenance

To stop the automatic post generation, remove the cron job:

```
crontab -e
```

Then delete the line containing `schedule-posts.js`.
