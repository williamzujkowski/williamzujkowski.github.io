/**
 * Prompt Templates for williamzujkowski.github.io
 *
 * This module exports reusable prompt templates for various LLM operations
 * specific to this technical blog project.
 */

/**
 * Template for generating new blog posts
 */
export const blogPostGenerationTemplate = (
  topic,
  style = "technical",
  wordCount = 1500
) => `
Generate a technical blog post for williamzujkowski.github.io with the following requirements:

Topic: ${topic}
Style: ${style}
Target Word Count: ${wordCount}

Requirements:
1. Use markdown format with proper frontmatter (title, date, tags, excerpt, topic, readingTime)
2. Include relevant code examples with syntax highlighting
3. Structure with clear sections and subsections
4. Add a compelling introduction and conclusion
5. Include relevant technical details and best practices
6. Optimize for SEO with appropriate keywords
7. Maintain a professional yet approachable tone
8. Include practical, actionable insights

Frontmatter format:
---
title: "Your Title Here"
date: ${new Date().toISOString().split("T")[0]}
tags: ["tag1", "tag2", "tag3"]
excerpt: "A brief summary of the post (150-200 characters)"
topic: "main-topic"
readingTime: "X min read"
---

The post should be informative, engaging, and provide real value to readers interested in ${topic}.
`;

/**
 * Template for refactoring existing code
 */
export const codeRefactoringTemplate = (code, goals) => `
Refactor the following code according to the project's standards in agent-rules.md:

Current Code:
\`\`\`
${code}
\`\`\`

Refactoring Goals:
${goals.map((goal, i) => `${i + 1}. ${goal}`).join("\n")}

Requirements:
1. Follow ES6+ conventions and project style guide
2. Improve readability and maintainability
3. Add proper error handling
4. Include JSDoc comments
5. Ensure accessibility compliance
6. Optimize for performance
7. Make the code testable
8. Use meaningful variable and function names

Provide the refactored code with explanations for significant changes.
`;

/**
 * Template for fixing bugs
 */
export const bugFixTemplate = (bugDescription, errorMessage, context) => `
Fix the following bug in the williamzujkowski.github.io project:

Bug Description: ${bugDescription}
Error Message: ${errorMessage || "No specific error message"}
Context: ${context}

Requirements:
1. Identify the root cause of the issue
2. Provide a fix that follows project coding standards
3. Ensure the fix doesn't break existing functionality
4. Add appropriate error handling
5. Include test cases to prevent regression
6. Document any changes made

Provide:
1. Explanation of the bug cause
2. The fixed code
3. Test cases to verify the fix
4. Any additional recommendations
`;

/**
 * Template for creating new components
 */
export const componentCreationTemplate = (componentName, purpose, features) => `
Create a new component for williamzujkowski.github.io:

Component Name: ${componentName}
Purpose: ${purpose}
Required Features:
${features.map((feature, i) => `${i + 1}. ${feature}`).join("\n")}

Requirements:
1. Follow the project's component pattern (see agent-rules.md)
2. Ensure progressive enhancement (works without JS)
3. Include accessibility features (ARIA, keyboard navigation)
4. Use CSS custom properties for theming
5. Add proper error handling and loading states
6. Make it performant and lightweight
7. Include comprehensive JSDoc documentation
8. Create accompanying CSS using BEM-like naming

Deliverables:
1. JavaScript component code
2. CSS styles
3. Usage example in Nunjucks template
4. Basic unit tests
`;

/**
 * Template for optimizing performance
 */
export const performanceOptimizationTemplate = (targetArea, currentMetrics) => `
Optimize performance for the following area of williamzujkowski.github.io:

Target Area: ${targetArea}
Current Metrics:
${Object.entries(currentMetrics)
  .map(([key, value]) => `- ${key}: ${value}`)
  .join("\n")}

Requirements:
1. Identify performance bottlenecks
2. Propose optimizations following project standards
3. Maintain functionality and accessibility
4. Consider impact on Core Web Vitals
5. Ensure changes work across browsers
6. Keep bundle sizes within limits (50KB gzipped for main)

Provide:
1. Analysis of current performance issues
2. Specific optimization recommendations
3. Implementation code
4. Expected performance improvements
5. Any trade-offs to consider
`;

/**
 * Template for content migration
 */
export const contentMigrationTemplate = (sourceFormat, contentType) => `
Migrate content to williamzujkowski.github.io format:

Source Format: ${sourceFormat}
Content Type: ${contentType}

Requirements:
1. Convert to proper markdown format
2. Add appropriate frontmatter
3. Ensure code blocks have syntax highlighting
4. Optimize images and use responsive formats
5. Fix any broken links
6. Maintain SEO value
7. Preserve content structure and meaning
8. Update to match site's style and tone

Output should include:
1. Converted markdown content
2. List of required images to process
3. Any manual steps needed
4. Validation checklist
`;

/**
 * Template for accessibility improvements
 */
export const accessibilityTemplate = (component, wcagLevel = "AA") => `
Improve accessibility for the following component to meet WCAG ${wcagLevel} standards:

Component/Page: ${component}

Requirements:
1. Ensure keyboard navigation works properly
2. Add appropriate ARIA labels and roles
3. Verify color contrast ratios
4. Include focus indicators
5. Add screen reader support
6. Ensure proper heading hierarchy
7. Make interactive elements accessible
8. Add skip links where appropriate

Provide:
1. List of accessibility issues found
2. Fixed code with accessibility improvements
3. Testing recommendations
4. Any limitations or considerations
`;

/**
 * Template for documentation updates
 */
export const documentationTemplate = (targetFile, updateType) => `
Update documentation for williamzujkowski.github.io:

Target: ${targetFile}
Update Type: ${updateType}

Requirements:
1. Follow existing documentation style
2. Be clear and concise
3. Include code examples where helpful
4. Update any related files (FILE_TREE.md, README.md)
5. Ensure accuracy with current implementation
6. Add helpful diagrams or visuals if applicable
7. Include common troubleshooting tips

Provide the updated documentation following the project's standards.
`;

/**
 * Template for test creation
 */
export const testCreationTemplate = (targetCode, testType) => `
Create ${testType} tests for the following code:

Target Code:
\`\`\`
${targetCode}
\`\`\`

Requirements:
1. Follow project testing standards (Jest for unit tests, Playwright for E2E)
2. Achieve high code coverage (85%+ general, 95%+ critical)
3. Test both success and failure cases
4. Include edge cases and boundary conditions
5. Make tests readable and maintainable
6. Use descriptive test names
7. Mock external dependencies appropriately
8. Follow AAA pattern (Arrange, Act, Assert)

Provide comprehensive test suite with clear documentation.
`;

/**
 * Helper function to validate template inputs
 */
export function validateTemplateInputs(inputs, requiredFields) {
  const missing = requiredFields.filter((field) => !inputs[field]);
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(", ")}`);
  }
  return true;
}

/**
 * Get template by name
 */
export function getTemplate(templateName) {
  const templates = {
    blogPost: blogPostGenerationTemplate,
    refactor: codeRefactoringTemplate,
    bugFix: bugFixTemplate,
    component: componentCreationTemplate,
    performance: performanceOptimizationTemplate,
    migration: contentMigrationTemplate,
    accessibility: accessibilityTemplate,
    documentation: documentationTemplate,
    test: testCreationTemplate,
  };

  return templates[templateName] || null;
}
