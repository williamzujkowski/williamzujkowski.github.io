/**
 * Prompt templates for various code generation and modification tasks
 *
 * This file exports standardized templates that can be used when
 * prompting Claude or other LLMs for code-related tasks.
 */

/**
 * Template for generating new code components
 * @param {Object} params - Parameters to customize the template
 * @returns {string} The formatted prompt template
 */
export function codeGenerationTemplate(params = {}) {
  const { feature, requirements, constraints } = params;

  return `
# Code Generation Request: ${feature || "[Feature Name]"}

## Requirements
${requirements || "- List specific requirements here"}

## Technical Constraints
${constraints || "- List any technical constraints or dependencies"}

Please generate code following the project's coding standards as defined in CLAUDE.md.
Use appropriate patterns and ensure the code is:
- Well-documented
- Testable
- Performant
- Follows best practices for web development
  `;
}

/**
 * Template for code refactoring tasks
 * @param {Object} params - Parameters to customize the template
 * @returns {string} The formatted prompt template
 */
export function refactoringTemplate(params = {}) {
  const { codeToRefactor, goal, constraints } = params;

  return `
# Code Refactoring Request

## Original Code
\`\`\`
${codeToRefactor || "// Insert code to refactor here"}
\`\`\`

## Refactoring Goal
${goal || "Explain the goal of the refactoring"}

## Constraints
${constraints || "- List any constraints for the refactoring"}

Please refactor this code following the project's coding standards.
Explain key changes and why they improve the code.
  `;
}

/**
 * Template for bug fix requests
 * @param {Object} params - Parameters to customize the template
 * @returns {string} The formatted prompt template
 */
export function bugFixTemplate(params = {}) {
  const { bugDescription, codeWithBug, expectedBehavior } = params;

  return `
# Bug Fix Request

## Bug Description
${bugDescription || "Describe the bug here"}

## Code With Bug
\`\`\`
${codeWithBug || "// Insert problematic code here"}
\`\`\`

## Expected Behavior
${expectedBehavior || "Describe what the code should do"}

Please fix this bug while adhering to the project's coding standards.
Include an explanation of what caused the bug and how your solution addresses it.
  `;
}
