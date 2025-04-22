# Vulnerability Blog Generator Migration

This document outlines the process of migrating the vulnerability blog post generator from an integrated part of this repository to a standalone repository with a Git submodule integration.

## Migration Summary

The vulnerability blog generator has been:

1. Extracted into a separate repository: [williamzujkowski/vuln-post-generator](https://github.com/williamzujkowski/vuln-post-generator)
2. Integrated back as a Git submodule in `tools/vuln-blog/`
3. GitHub Actions workflows updated to use the submodule
4. Package.json scripts updated to use the submodule

## Benefits of This Approach

- **Clearer separation of concerns**: The vulnerability generator is now a standalone project
- **Independent development**: Changes to the generator can be made without affecting the main website
- **Simpler maintenance**: Each project can have its own versioning, issues, and pull requests
- **Reusability**: The generator can now be used in other projects
- **Cleaner repository**: The main website repository is now more focused on website content

## Integration Method Used

The vulnerability blog generator is integrated as a Git submodule:

```bash
git submodule add https://github.com/williamzujkowski/vuln-post-generator.git tools/vuln-blog
```

The GitHub Actions workflows have been updated to:

1. Checkout the repository with submodules: `submodules: recursive`
2. Install dependencies for both projects
3. Create a wrapper script that calls the generator from the main repository
4. Run the generator via the wrapper which sets the `OUTPUT_DIR` to the appropriate path in the main repository
5. Commit changes and create a pull request in the main repository only, avoiding submodule changes

## How to Work with the Submodule

### Cloning the Repository

When cloning this repository, use the `--recursive` flag to also clone the submodule:

```bash
git clone --recursive https://github.com/williamzujkowski/williamzujkowski.github.io.git
```

Or, if you've already cloned the repository:

```bash
git submodule update --init --recursive
```

### Updating the Submodule

To update the submodule to the latest version:

```bash
git submodule update --remote tools/vuln-blog
git add tools/vuln-blog
git commit -m "Update vulnerability blog generator to latest version"
```

### Making Changes to the Submodule

If you need to make changes to the vulnerability blog generator:

1. Go to the submodule directory: `cd tools/vuln-blog`
2. Make your changes
3. Commit and push to the vuln-post-generator repository
4. Update the submodule in the main repository as described above

## Backups

Before the migration, comprehensive backups were created:

- Main vulnerability scripts: `/backup/vuln-blog-generator-backup.tar.gz`
- Prompt templates: `/backup/vuln-prompts.tar.gz`
- GitHub workflow files: `/backup/vuln-workflows.tar.gz`
- Combined backup: `/vulnerability-generator-complete.tar.gz`

These backups can be used to restore the original files if needed.

## Testing

The integration includes several test suites:

### Integration Tests

Located in `tests/integration/vuln-blog-integration.test.js`, these tests verify:

- The submodule structure and presence of required files
- Package.json scripts are correctly configured
- GitHub Actions workflows include submodule checkout
- The OUTPUT_DIR environment variable is properly set

Run these tests with:

```bash
npm test -- tests/integration/vuln-blog-integration.test.js
```

### End-to-End Tests

Located in `tests/e2e/vuln-generator-e2e.test.js`, these tests:

- Create a mock environment with test API keys
- Run the generator with mock APIs
- Verify a post is correctly generated with all required elements

Run these tests with:

```bash
npm test -- tests/e2e/vuln-generator-e2e.test.js
```

### Mocking Support

The submodule includes a mock implementation in `tools/vuln-blog/mocks/` that:

- Provides mock responses for all external APIs
- Can be activated by setting `MOCK_APIS=true`
- Enables testing without actual API keys

You can run a mock generation with:

```bash
cd tools/vuln-blog
npm run test:mock
```

## Future Considerations

- Consider integrating with continuous deployment
- Add more documentation on how to use the vulnerability blog generator
- Add a contributor guide for the vulnerability blog generator
- Enhance mocking capabilities for more robust testing
