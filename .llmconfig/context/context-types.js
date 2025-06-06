/**
 * Context Type Definitions for williamzujkowski.github.io
 *
 * This module defines the context types and structures that LLM agents
 * should be aware of when working with this project.
 */

/**
 * Domain-specific context for the technical blog
 */
export const DomainContext = {
  projectType: "Technical Blog",
  audience: "Software developers, engineers, and tech enthusiasts",

  topics: {
    primary: [
      "AI/ML and Large Language Models",
      "Cloud Computing and Architecture",
      "Cybersecurity and Vulnerability Analysis",
      "Quantum Computing",
      "DevOps and Platform Engineering",
      "High-Performance Computing",
      "Software Development Best Practices",
    ],

    secondary: [
      "Open Source Software",
      "Blockchain and Distributed Systems",
      "Edge Computing",
      "Sustainable Computing",
      "Robotics and Embodied AI",
    ],
  },

  contentTypes: {
    "technical-article": {
      description: "In-depth technical articles with code examples",
      typicalLength: "1500-3000 words",
      structure: ["introduction", "technical-content", "code-examples", "conclusion"],
    },

    "vulnerability-analysis": {
      description: "Security vulnerability deep-dives",
      typicalLength: "2000-3500 words",
      structure: [
        "overview",
        "technical-details",
        "exploitation",
        "mitigation",
        "references",
      ],
    },

    tutorial: {
      description: "Step-by-step guides and how-tos",
      typicalLength: "1000-2500 words",
      structure: ["objectives", "prerequisites", "steps", "troubleshooting", "summary"],
    },

    opinion: {
      description: "Thought pieces on technology trends",
      typicalLength: "800-1500 words",
      structure: ["thesis", "arguments", "counter-arguments", "conclusion"],
    },
  },
};

/**
 * Project structure context
 */
export const ProjectContext = {
  architecture: {
    type: "Static Site Generator",
    framework: "Eleventy (11ty)",
    version: "2.x",

    key_technologies: {
      templating: "Nunjucks",
      styling: "CSS with custom properties",
      javascript: "ES6+ modules",
      bundling: "Rollup",
      testing: ["Jest", "Playwright"],
    },
  },

  file_structure: {
    content: "/src/posts/",
    templates: "/src/_includes/",
    layouts: "/src/_layouts/",
    data: "/src/_data/",
    styles: "/src/css/",
    scripts: "/src/js/",
    assets: "/assets/",
    build_output: "/_site/",
  },

  naming_conventions: {
    posts: "YYYY-MM-DD-title-in-kebab-case.md",
    components: "component-name.js",
    styles: "component-name.css",
    tests: "component-name.test.js",
  },

  build_process: {
    command: "npm run build",
    stages: ["clean", "copy-assets", "build-css", "build-js", "build-html", "optimize"],
    output: "_site directory",
  },
};

/**
 * User intent classifications
 */
export const UserIntent = {
  CREATE: {
    "new-post": "Create a new blog post",
    component: "Create a new UI component",
    feature: "Add a new feature to the site",
    test: "Create tests for existing code",
  },

  MODIFY: {
    refactor: "Refactor existing code",
    optimize: "Optimize performance",
    "fix-bug": "Fix a bug or issue",
    "update-content": "Update existing content",
    "improve-accessibility": "Improve accessibility",
  },

  ANALYZE: {
    review: "Review code for improvements",
    "security-audit": "Check for security issues",
    "performance-audit": "Analyze performance",
    "accessibility-audit": "Check accessibility compliance",
  },

  DOCUMENT: {
    "add-docs": "Add documentation",
    "update-docs": "Update existing documentation",
    "api-docs": "Document APIs or interfaces",
  },
};

/**
 * Technical constraints and requirements
 */
export const TechnicalConstraints = {
  performance: {
    "bundle-size": "50KB gzipped for main bundle",
    "page-load": "Target < 3s on 3G",
    "core-web-vitals": {
      LCP: "< 2.5s",
      FID: "< 100ms",
      CLS: "< 0.1",
    },
  },

  browser_support: {
    modern: ["Chrome 90+", "Firefox 88+", "Safari 14+", "Edge 90+"],
    no_support: ["Internet Explorer"],
  },

  accessibility: {
    standard: "WCAG 2.1 AA",
    testing_tools: ["axe", "WAVE", "NVDA"],
    requirements: [
      "Keyboard navigable",
      "Screen reader compatible",
      "Proper color contrast",
      "Focus indicators",
    ],
  },

  security: {
    csp: "Strict Content Security Policy",
    dependencies: "Regular vulnerability scanning",
    https: "All resources over HTTPS",
  },
};

/**
 * Common patterns and conventions
 */
export const CodePatterns = {
  component_structure: `
export class ComponentName {
  constructor(element, options = {}) {
    this.element = element;
    this.options = { ...this.defaults, ...options };
    this.init();
  }

  get defaults() {
    return {
      // Default options
    };
  }

  init() {
    // Initialization logic
  }

  // Public methods
}`,

  error_handling: `
try {
  // Risky operation
} catch (error) {
  console.error('Descriptive error message:', error);
  // Graceful fallback
}`,

  async_pattern: `
async function fetchData(endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(\`HTTP \${response.status}\`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw error;
  }
}`,
};

/**
 * Data structures used in the project
 */
export const DataStructures = {
  frontmatter: {
    required: ["title", "date", "tags", "excerpt"],
    optional: ["topic", "readingTime", "author", "image", "draft"],
  },

  config_files: {
    "site.js": "Global site configuration",
    "navigation.json": "Navigation menu structure",
    "theme.json": "Theme configuration",
    "blog.json": "Blog-specific settings",
  },

  api_responses: {
    "arxiv-feed": "Academic paper recommendations",
    "github-pins": "Pinned repositories",
    "contribution-heatmap": "GitHub contribution data",
  },
};

/**
 * Export all context types
 */
export default {
  DomainContext,
  ProjectContext,
  UserIntent,
  TechnicalConstraints,
  CodePatterns,
  DataStructures,
};
