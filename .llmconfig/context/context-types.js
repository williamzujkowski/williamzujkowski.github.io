/**
 * Type definitions for context objects used in LLM interactions
 *
 * These types define the structure of context information that can be
 * provided to LLMs like Claude to improve the quality and relevance
 * of generated code and responses.
 */

/**
 * Represents domain-specific context about the application area
 * @typedef {Object} DomainContext
 * @property {string} area - The general domain area (e.g., "web development")
 * @property {string[]} concepts - Key domain concepts relevant to the task
 * @property {Object} terminology - Domain-specific terminology mapping
 * @property {string[]} constraints - Domain-specific constraints to consider
 */

/**
 * Represents project-level context about the codebase
 * @typedef {Object} ProjectContext
 * @property {string} name - The project name
 * @property {string} description - Brief project description
 * @property {string[]} technologies - Key technologies used
 * @property {string} architecture - Brief description of project architecture
 * @property {Object} patterns - Common patterns used in the project
 * @property {string[]} conventions - Coding conventions specific to this project
 */

/**
 * Represents information about the user's intent for a task
 * @typedef {Object} UserIntent
 * @property {string} goal - The primary goal the user is trying to achieve
 * @property {string} taskType - Type of task (e.g., "bugfix", "feature", "refactor")
 * @property {string[]} requirements - Specific requirements for the task
 * @property {string[]} constraints - Constraints that must be respected
 * @property {string} priority - Priority indicator ("high", "medium", "low")
 * @property {string[]} relatedFiles - Files related to the current task
 */

// Export type definitions (these would be actual exports in TypeScript)
export const types = {
  DomainContext: "DomainContext",
  ProjectContext: "ProjectContext",
  UserIntent: "UserIntent",
};
