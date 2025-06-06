/**
 * Configuration Loaders for williamzujkowski.github.io
 *
 * This module provides utility functions for loading and managing
 * LLM configurations and context files.
 */

/**
 * Load Claude configuration from .llmconfig/CLAUDE.md
 * @returns {Promise<Object>} Configuration object
 */
export async function loadClaudeConfig() {
  try {
    const fs = await import("fs").then((m) => m.promises);
    const path = await import("path");

    const configPath = path.join(process.cwd(), ".llmconfig", "CLAUDE.md");
    const content = await fs.readFile(configPath, "utf-8");

    return {
      raw: content,
      mainInstructions: extractSection(content, "## Main Instructions"),
      projectContext: extractSection(content, "## Project Context"),
      technologyStack: extractSection(content, "## Technology Stack"),
      codingPatterns: extractSection(content, "## Coding Patterns"),
      fileOrganization: extractSection(content, "## File Organization"),
      contentGuidelines: extractSection(content, "## Content Guidelines"),
      performanceConsiderations: extractSection(
        content,
        "## Performance Considerations"
      ),
      securityPractices: extractSection(content, "## Security Practices"),
      testingRequirements: extractSection(content, "## Testing Requirements"),
      commonTasks: extractSection(content, "## Common Tasks"),
    };
  } catch (error) {
    console.error("Failed to load Claude config:", error);
    return null;
  }
}

/**
 * Load agent rules from .llmconfig/agent-rules.md
 * @returns {Promise<Object>} Agent rules object
 */
export async function loadAgentRules() {
  try {
    const fs = await import("fs").then((m) => m.promises);
    const path = await import("path");

    const rulesPath = path.join(process.cwd(), ".llmconfig", "agent-rules.md");
    const content = await fs.readFile(rulesPath, "utf-8");

    return {
      raw: content,
      corePrinciples: extractSection(content, "## Core Principles"),
      codeStyleRules: extractSection(content, "## Code Style Rules"),
      fileNamingConventions: extractSection(content, "## File Naming Conventions"),
      gitCommitStandards: extractSection(content, "## Git Commit Standards"),
      testingRequirements: extractSection(content, "## Testing Requirements"),
      performanceGuidelines: extractSection(content, "## Performance Guidelines"),
      securityRequirements: extractSection(content, "## Security Requirements"),
      accessibilityChecklist: extractSection(content, "## Accessibility Checklist"),
      commonPatterns: extractSection(content, "## Common Patterns"),
      dosAndDonts: extractSection(content, "## Do's and Don'ts"),
      reviewChecklist: extractSection(content, "## Review Checklist"),
    };
  } catch (error) {
    console.error("Failed to load agent rules:", error);
    return null;
  }
}

/**
 * Load context types from .llmconfig/context/context-types.js
 * @returns {Promise<Object>} Context types object
 */
export async function loadContextTypes() {
  try {
    const path = await import("path");
    const contextPath = path.join(
      process.cwd(),
      ".llmconfig",
      "context",
      "context-types.js"
    );

    // Dynamic import for ES modules
    const contextModule = await import(contextPath);

    return {
      DomainContext: contextModule.DomainContext,
      ProjectContext: contextModule.ProjectContext,
      UserIntent: contextModule.UserIntent,
      TechnicalConstraints: contextModule.TechnicalConstraints,
      CodePatterns: contextModule.CodePatterns,
      DataStructures: contextModule.DataStructures,
    };
  } catch (error) {
    console.error("Failed to load context types:", error);
    return null;
  }
}

/**
 * Load prompt templates from .llmconfig/prompt-templates/index.js
 * @returns {Promise<Object>} Prompt templates object
 */
export async function loadPromptTemplates() {
  try {
    const path = await import("path");
    const templatesPath = path.join(
      process.cwd(),
      ".llmconfig",
      "prompt-templates",
      "index.js"
    );

    // Dynamic import for ES modules
    const templatesModule = await import(templatesPath);

    return {
      blogPostGenerationTemplate: templatesModule.blogPostGenerationTemplate,
      codeRefactoringTemplate: templatesModule.codeRefactoringTemplate,
      bugFixTemplate: templatesModule.bugFixTemplate,
      componentCreationTemplate: templatesModule.componentCreationTemplate,
      performanceOptimizationTemplate: templatesModule.performanceOptimizationTemplate,
      contentMigrationTemplate: templatesModule.contentMigrationTemplate,
      accessibilityTemplate: templatesModule.accessibilityTemplate,
      documentationTemplate: templatesModule.documentationTemplate,
      testCreationTemplate: templatesModule.testCreationTemplate,
      getTemplate: templatesModule.getTemplate,
      validateTemplateInputs: templatesModule.validateTemplateInputs,
    };
  } catch (error) {
    console.error("Failed to load prompt templates:", error);
    return null;
  }
}

/**
 * Load example responses from .llmconfig/examples/index.js
 * @returns {Promise<Object>} Example responses object
 */
export async function loadExampleResponses() {
  try {
    const path = await import("path");
    const examplesPath = path.join(process.cwd(), ".llmconfig", "examples", "index.js");

    // Dynamic import for ES modules
    const examplesModule = await import(examplesPath);

    return examplesModule.exampleResponses || examplesModule.default;
  } catch (error) {
    console.error("Failed to load example responses:", error);
    return null;
  }
}

/**
 * Load system prompts from .llmconfig/system-prompts/index.js
 * @returns {Promise<Object>} System prompts object
 */
export async function loadSystemPrompts() {
  try {
    const path = await import("path");
    const promptsPath = path.join(
      process.cwd(),
      ".llmconfig",
      "system-prompts",
      "index.js"
    );

    // Dynamic import for ES modules
    const promptsModule = await import(promptsPath);

    return {
      baseSystemPrompt: promptsModule.baseSystemPrompt,
      systemPrompts: promptsModule.systemPrompts,
      getSystemPrompt: promptsModule.getSystemPrompt,
      combineRoles: promptsModule.combineRoles,
    };
  } catch (error) {
    console.error("Failed to load system prompts:", error);
    return null;
  }
}

/**
 * Load all LLM configurations
 * @returns {Promise<Object>} Complete configuration object
 */
export async function loadAllConfigurations() {
  const [
    claudeConfig,
    agentRules,
    contextTypes,
    promptTemplates,
    exampleResponses,
    systemPrompts,
  ] = await Promise.all([
    loadClaudeConfig(),
    loadAgentRules(),
    loadContextTypes(),
    loadPromptTemplates(),
    loadExampleResponses(),
    loadSystemPrompts(),
  ]);

  return {
    claude: claudeConfig,
    rules: agentRules,
    context: contextTypes,
    templates: promptTemplates,
    examples: exampleResponses,
    systemPrompts: systemPrompts,

    // Convenience methods
    getTemplate: promptTemplates?.getTemplate,
    getSystemPrompt: systemPrompts?.getSystemPrompt,

    // Validation
    isValid: () => {
      return !!(
        claudeConfig &&
        agentRules &&
        contextTypes &&
        promptTemplates &&
        exampleResponses &&
        systemPrompts
      );
    },
  };
}

/**
 * Validate configuration completeness
 * @param {Object} config - Configuration object
 * @returns {Object} Validation result
 */
export function validateConfiguration(config) {
  const required = [
    "claude",
    "rules",
    "context",
    "templates",
    "examples",
    "systemPrompts",
  ];

  const missing = required.filter((key) => !config[key]);
  const warnings = [];

  // Check for specific required methods
  if (!config.templates?.getTemplate) {
    warnings.push("Missing getTemplate function in prompt templates");
  }

  if (!config.systemPrompts?.getSystemPrompt) {
    warnings.push("Missing getSystemPrompt function in system prompts");
  }

  return {
    isValid: missing.length === 0,
    missing,
    warnings,
    score: ((required.length - missing.length) / required.length) * 100,
  };
}

/**
 * Get project file paths for common operations
 * @returns {Object} File paths object
 */
export function getProjectPaths() {
  const path = require("path");
  const root = process.cwd();

  return {
    root,
    llmconfig: path.join(root, ".llmconfig"),
    src: path.join(root, "src"),
    posts: path.join(root, "src", "posts"),
    includes: path.join(root, "src", "_includes"),
    layouts: path.join(root, "src", "_layouts"),
    css: path.join(root, "src", "css"),
    js: path.join(root, "src", "js"),
    assets: path.join(root, "assets"),
    scripts: path.join(root, "scripts"),
    tests: path.join(root, "tests"),
    docs: path.join(root, "docs"),
    fileTree: path.join(root, "FILE_TREE.md"),
    packageJson: path.join(root, "package.json"),
  };
}

/**
 * Helper function to extract sections from markdown
 * @param {string} content - Markdown content
 * @param {string} sectionTitle - Section title to extract
 * @returns {string} Extracted section content
 */
function extractSection(content, sectionTitle) {
  const lines = content.split("\n");
  const startIndex = lines.findIndex((line) => line.trim() === sectionTitle);

  if (startIndex === -1) return "";

  let endIndex = lines.length;
  for (let i = startIndex + 1; i < lines.length; i++) {
    if (lines[i].startsWith("## ") && lines[i].trim() !== sectionTitle) {
      endIndex = i;
      break;
    }
  }

  return lines
    .slice(startIndex + 1, endIndex)
    .join("\n")
    .trim();
}

/**
 * Export all loader functions
 */
export default {
  loadClaudeConfig,
  loadAgentRules,
  loadContextTypes,
  loadPromptTemplates,
  loadExampleResponses,
  loadSystemPrompts,
  loadAllConfigurations,
  validateConfiguration,
  getProjectPaths,
};
