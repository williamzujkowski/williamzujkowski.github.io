/**
 * Configuration loaders for the .llmconfig directory
 *
 * These functions help load and parse configuration files from the .llmconfig directory,
 * ensuring consistent and proper usage of AI agent configurations.
 */

/**
 * Loads the main Claude configuration file
 * @returns {Object} The parsed configuration object
 */
export function loadClaudeConfig() {
  // In a real implementation, this would parse the CLAUDE.md file
  // and return a structured object with the configuration
  return {
    mainInstructions: [],
    codingPatterns: {},
    projectContext: {},
  };
}

/**
 * Loads a specific prompt template by name
 * @param {string} templateName - The name of the template to load
 * @returns {string|null} The template string or null if not found
 */
export function loadPromptTemplate(templateName) {
  // Implementation would load the specified template file
  return null;
}

/**
 * Loads all available context files
 * @returns {Object} Map of context name to context content
 */
export function loadContextFiles() {
  // Implementation would scan and load all context files
  return {};
}

/**
 * Loads system prompts for different agents
 * @param {string} agentType - The type of agent to load prompts for
 * @returns {Object} The agent's system prompts
 */
export function loadSystemPrompts(agentType) {
  // Implementation would load system prompts for the specified agent
  return {};
}
