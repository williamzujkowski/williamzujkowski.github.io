/**
 * Enhanced CSS Optimization Script
 *
 * Implements CSS code splitting and optimization strategies:
 * - Separates critical CSS for inline loading
 * - Creates component-specific CSS files
 * - Optimizes and minifies CSS
 * - Generates stats about CSS size reduction
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import postcss from "postcss";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";
import { PurgeCSS } from "purgecss";
import chalk from "chalk";

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..");

// Configuration
const config = {
  input: path.join(rootDir, "src", "css", "main.css"),
  output: path.join(rootDir, "_site", "css"),
  optimizedDir: path.join(rootDir, "src", "css", "optimized"),
  tailwindConfig: path.join(rootDir, "config", "tailwind.config.cjs"),
  components: [
    {
      name: "base",
      description: "Core styles (critical CSS)",
      patterns: ["body", "html", "main", "header", "footer", "a", ".container"],
    },
    {
      name: "components",
      description: "UI components",
      patterns: [
        ".btn",
        ".card",
        ".alert",
        ".badge",
        ".tag",
        ".breadcrumbs",
        ".pagination",
      ],
    },
    {
      name: "utilities",
      description: "Utility classes",
      patterns: [
        ".flex",
        ".grid",
        ".text-",
        ".bg-",
        ".p-",
        ".m-",
        ".w-",
        ".h-",
        ".gap-",
        ".space-",
        ".border",
        ".rounded",
        ".shadow",
      ],
    },
    {
      name: "theme",
      description: "Theme-specific styles",
      patterns: [
        ".theme-",
        ":root",
        "[data-theme",
        ".dark",
        ".light",
        ".text-theme-",
        ".bg-theme-",
        ".border-theme-",
      ],
    },
    {
      name: "mobile",
      description: "Mobile-specific styles",
      patterns: ["@media (max-width"],
    },
  ],
};

// Statistics for reporting
const stats = {
  original: {
    size: 0,
    files: 1,
  },
  optimized: {
    size: 0,
    files: 0,
  },
  savings: {
    bytes: 0,
    percent: 0,
  },
};

/**
 * Create directory if it doesn't exist
 * @param {string} dirPath - Directory path
 */
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Process CSS with PostCSS plugins
 * @param {string} css - CSS content
 * @param {Object} options - Processing options
 * @returns {Promise<string>} Processed CSS
 */
async function processCss(css, options = {}) {
  const plugins = [
    tailwindcss(options.tailwindConfig || config.tailwindConfig),
    autoprefixer(),
  ];

  if (options.minify) {
    plugins.push(
      cssnano({
        preset: [
          "default",
          {
            discardComments: {
              removeAll: true,
            },
            normalizeWhitespace: true,
            minifyFontValues: true,
            minifySelectors: true,
            reduceIdents: false, // Preserve custom animations
          },
        ],
      })
    );
  }

  const result = await postcss(plugins).process(css, {
    from: options.from || config.input,
    to: options.to || config.output,
  });

  return result.css;
}

/**
 * Extract specific CSS based on patterns
 * @param {string} css - Full CSS content
 * @param {string[]} patterns - CSS selector patterns to extract
 * @returns {Promise<string>} Extracted CSS
 */
async function extractCss(css, patterns) {
  const purgecss = new PurgeCSS();

  // Create a temporary file for PurgeCSS
  const tempFile = path.join(config.output, "temp.css");
  fs.writeFileSync(tempFile, css);

  // Create fake HTML content with all the patterns to extract
  const fakeHtml = patterns
    .map((pattern) => {
      // Handle media queries and other complex selectors
      if (pattern.startsWith("@media")) {
        return `<!-- ${pattern} -->`;
      }

      // Handle pseudo-classes and elements
      if (pattern.includes(":")) {
        const base = pattern.split(":")[0];
        return `<div class="${base.replace(".", "")}"></div><!-- ${pattern} -->`;
      }

      // Handle attribute selectors
      if (pattern.includes("[")) {
        const attribute = pattern.match(/\[(.*?)\]/)[1];
        return `<div ${attribute}></div>`;
      }

      // Handle element selectors
      if (!pattern.startsWith(".") && !pattern.startsWith("#")) {
        return `<${pattern}></${pattern}>`;
      }

      // Handle class selectors
      return `<div class="${pattern.replace(".", "")}"></div>`;
    })
    .join("\n");

  const fakeHtmlFile = path.join(config.output, "fake.html");
  fs.writeFileSync(fakeHtmlFile, fakeHtml);

  // Use PurgeCSS to extract matching CSS
  const result = await purgecss.purge({
    content: [fakeHtmlFile],
    css: [tempFile],
    safelist: {
      standard: patterns,
      deep: patterns.map((p) => new RegExp(p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))),
      greedy: patterns.map(
        (p) => new RegExp(`^${p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}.*`)
      ),
    },
    rejected: false,
  });

  // Clean up temporary files
  fs.unlinkSync(tempFile);
  fs.unlinkSync(fakeHtmlFile);

  return result[0].css;
}

/**
 * Generate component CSS files
 * @param {string} css - Full CSS content
 * @returns {Promise<Object>} Component CSS files
 */
async function generateComponentCss(css) {
  const componentCss = {};

  // Extract CSS for each component
  for (const component of config.components) {
    console.log(chalk.cyan(`Extracting ${component.name} CSS...`));

    const extractedCss = await extractCss(css, component.patterns);
    componentCss[component.name] = extractedCss;

    // Write component CSS file
    const outputPath = path.join(config.optimizedDir, `${component.name}.css`);
    fs.writeFileSync(outputPath, extractedCss);

    // Update statistics
    stats.optimized.files++;
    stats.optimized.size += Buffer.byteLength(extractedCss, "utf8");

    console.log(
      chalk.green(
        `  ✓ Created ${component.name}.css (${formatBytes(Buffer.byteLength(extractedCss, "utf8"))})`
      )
    );
  }

  // Create main.css that imports all components
  const imports = config.components
    .map((component) => `@import './${component.name}.css';`)
    .join("\n");

  const mainCssPath = path.join(config.optimizedDir, "main.css");
  fs.writeFileSync(mainCssPath, imports);

  console.log(chalk.green(`✓ Created main.css with imports`));

  return componentCss;
}

/**
 * Generate optimization statistics
 */
function generateStats() {
  stats.savings.bytes = stats.original.size - stats.optimized.size;
  stats.savings.percent = Math.round((stats.savings.bytes / stats.original.size) * 100);

  const statsOutput = {
    original: {
      size: formatBytes(stats.original.size),
      files: stats.original.files,
    },
    optimized: {
      size: formatBytes(stats.optimized.size),
      files: stats.optimized.files,
    },
    savings: {
      bytes: formatBytes(stats.savings.bytes),
      percent: `${stats.savings.percent}%`,
    },
    components: config.components.map((c) => ({
      name: c.name,
      description: c.description,
    })),
  };

  const statsFile = path.join(config.optimizedDir, "optimization-stats.json");
  fs.writeFileSync(statsFile, JSON.stringify(statsOutput, null, 2));

  return statsOutput;
}

/**
 * Create an example usage HTML file
 * @param {Object} componentCss - Component CSS files
 */
function createExampleUsage(componentCss) {
  const criticalCss = componentCss.base;

  const exampleHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Optimized CSS Example</title>

  <!-- Critical CSS inlined -->
  <style>
${criticalCss}
  </style>

  <!-- Async load of other CSS -->
  <link rel="preload" href="components.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <link rel="preload" href="utilities.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <link rel="preload" href="theme.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <link rel="preload" href="mobile.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

  <!-- Fallback for browsers without JS -->
  <noscript>
    <link rel="stylesheet" href="components.css">
    <link rel="stylesheet" href="utilities.css">
    <link rel="stylesheet" href="theme.css">
    <link rel="stylesheet" href="mobile.css">
  </noscript>
</head>
<body>
  <header>
    <h1>Optimized CSS Example</h1>
  </header>

  <main>
    <section>
      <h2>CSS Optimization Results</h2>
      <p>Original CSS: ${formatBytes(stats.original.size)}</p>
      <p>Optimized CSS: ${formatBytes(stats.optimized.size)}</p>
      <p>Savings: ${formatBytes(stats.savings.bytes)} (${stats.savings.percent}%)</p>
    </section>

    <section>
      <h2>Usage</h2>
      <p>Critical CSS is inlined in the head for fast initial render.</p>
      <p>Other CSS components are loaded asynchronously.</p>
    </section>
  </main>

  <footer>
    <p>Generated on ${new Date().toLocaleString()}</p>
  </footer>
</body>
</html>`;

  const exampleFile = path.join(config.optimizedDir, "example-usage.html");
  fs.writeFileSync(exampleFile, exampleHtml);

  console.log(chalk.green(`✓ Created example usage HTML`));
}

/**
 * Format byte size to human-readable format
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size
 */
function formatBytes(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

/**
 * Main function
 */
async function main() {
  console.log(chalk.blue.bold("CSS Optimization Process"));
  console.log(chalk.blue("======================="));

  try {
    // Ensure output directories exist
    ensureDirectoryExists(config.output);
    ensureDirectoryExists(config.optimizedDir);

    // Read main CSS file
    console.log(chalk.cyan(`Reading CSS from ${config.input}...`));
    const cssContent = fs.readFileSync(config.input, "utf8");

    // Process full CSS
    console.log(chalk.cyan("Processing CSS with PostCSS..."));
    const processedCss = await processCss(cssContent);

    // Write full CSS to output
    const fullCssPath = path.join(config.output, "styles.css");
    fs.writeFileSync(fullCssPath, processedCss);

    // Update statistics
    stats.original.size = Buffer.byteLength(processedCss, "utf8");
    console.log(
      chalk.green(`✓ Processed full CSS (${formatBytes(stats.original.size)})`)
    );

    // Generate component CSS files
    console.log(chalk.cyan("Generating component CSS files..."));
    const componentCss = await generateComponentCss(processedCss);

    // Create README file
    const readmePath = path.join(config.optimizedDir, "README.md");
    const readme = `# Optimized CSS

This directory contains optimized CSS files split into components for better performance:

${config.components.map((c) => `- \`${c.name}.css\`: ${c.description}`).join("\n")}

## Usage

For best performance:

1. Inline the critical CSS (\`base.css\`) in the \`<head>\` of your HTML
2. Load other components asynchronously using \`<link rel="preload">\`

See \`example-usage.html\` for a complete example.

## Statistics

- Original CSS: ${formatBytes(stats.original.size)}
- Optimized CSS: ${formatBytes(stats.optimized.size)}
- Savings: ${formatBytes(stats.savings.bytes)} (${stats.savings.percent}%)

Generated on ${new Date().toLocaleString()}
`;
    fs.writeFileSync(readmePath, readme);

    // Generate optimization statistics
    const statsOutput = generateStats();

    // Create example usage HTML
    createExampleUsage(componentCss);

    console.log(chalk.blue("======================="));
    console.log(chalk.green.bold("CSS Optimization Complete"));
    console.log(chalk.green(`Original Size: ${statsOutput.original.size}`));
    console.log(chalk.green(`Optimized Size: ${statsOutput.optimized.size}`));
    console.log(
      chalk.green(
        `Savings: ${statsOutput.savings.bytes} (${statsOutput.savings.percent})`
      )
    );
  } catch (error) {
    console.error(chalk.red("Error optimizing CSS:"), error);
    process.exit(1);
  }
}

// Run the script if called directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
