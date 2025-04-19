#!/usr/bin/env node

/**
 * Configuration Validator
 *
 * This utility verifies the integrity of configuration files to ensure
 * they conform to expected formats and contain required properties.
 *
 * Usage:
 * node scripts/validation/validate-config.js [--fix]
 *
 * Options:
 * --fix  Attempt to fix common issues automatically
 */

import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG_DIR = path.join(__dirname, "..", "..", "src", "_data", "config");
const FIX_MODE = process.argv.includes("--fix");

// Schema definitions for each config file type
const SCHEMAS = {
  // Basic schema for meta.json
  "meta.json": {
    required: ["title", "description", "url", "author"],
    types: {
      title: "string",
      description: "string",
      url: "string",
      author: "string",
    },
  },

  // Schema for navigation.json
  "navigation.json": {
    required: ["mainNavigation"],
    types: {
      mainNavigation: "array",
    },
    arrayItems: {
      mainNavigation: {
        required: ["text", "url"],
        types: {
          text: "string",
          url: "string",
        },
      },
    },
  },

  // Schema for theme.json
  "theme.json": {
    required: ["name", "colors"],
    types: {
      name: "string",
      description: "string",
      isDark: "boolean",
      colors: "object",
    },
    nested: {
      colors: {
        required: ["primaryHue", "primaryChroma", "primaryLightness", "accentHue"],
        types: {
          primaryHue: "number",
          primaryChroma: "number",
          primaryLightness: "number",
          accentHue: "number",
        },
      },
    },
  },
};

// Schemas for subdirectory files
const SUBDIRECTORY_SCHEMAS = {
  // Schema for homepage files
  homepage: {
    "about.json": {
      required: ["heading", "content"],
      types: {
        heading: "string",
        content: "string",
      },
    },
    "display.json": {
      required: ["showGithubStats", "showRepositories"],
      types: {
        showGithubStats: "boolean",
        showRepositories: "boolean",
      },
    },
  },

  // Schema for blog files
  blog: {
    "settings.json": {
      required: ["postsPerPage", "showCategories"],
      types: {
        postsPerPage: "number",
        showCategories: "boolean",
      },
    },
  },
};

// Validate a value against a type
function validateType(value, expectedType) {
  if (expectedType === "array") {
    return Array.isArray(value);
  }
  return typeof value === expectedType;
}

// Validate a configuration file against its schema
async function validateConfigFile(filePath, schema) {
  try {
    // Read and parse the file
    const content = await fs.readFile(filePath, "utf8");
    let data;

    try {
      data = JSON.parse(content);
    } catch (error) {
      return {
        valid: false,
        errors: [`Invalid JSON: ${error.message}`],
        data: null,
      };
    }

    const errors = [];

    // Check required fields
    if (schema.required) {
      for (const field of schema.required) {
        if (data[field] === undefined) {
          errors.push(`Missing required field: ${field}`);
        }
      }
    }

    // Check types
    if (schema.types) {
      for (const [field, expectedType] of Object.entries(schema.types)) {
        if (data[field] !== undefined && !validateType(data[field], expectedType)) {
          errors.push(
            `Field ${field} should be of type ${expectedType}, got ${typeof data[field]}`
          );
        }
      }
    }

    // Check array items
    if (schema.arrayItems) {
      for (const [arrayField, itemSchema] of Object.entries(schema.arrayItems)) {
        if (Array.isArray(data[arrayField])) {
          for (let i = 0; i < data[arrayField].length; i++) {
            const item = data[arrayField][i];

            // Check required fields in array items
            if (itemSchema.required) {
              for (const field of itemSchema.required) {
                if (item[field] === undefined) {
                  errors.push(`Missing required field ${field} in ${arrayField}[${i}]`);
                }
              }
            }

            // Check types in array items
            if (itemSchema.types) {
              for (const [field, expectedType] of Object.entries(itemSchema.types)) {
                if (
                  item[field] !== undefined &&
                  !validateType(item[field], expectedType)
                ) {
                  errors.push(
                    `Field ${arrayField}[${i}].${field} should be of type ${expectedType}, got ${typeof item[field]}`
                  );
                }
              }
            }
          }
        }
      }
    }

    // Check nested objects
    if (schema.nested) {
      for (const [nestedField, nestedSchema] of Object.entries(schema.nested)) {
        if (typeof data[nestedField] === "object" && data[nestedField] !== null) {
          // Check required fields in nested object
          if (nestedSchema.required) {
            for (const field of nestedSchema.required) {
              if (data[nestedField][field] === undefined) {
                errors.push(`Missing required field ${field} in ${nestedField}`);
              }
            }
          }

          // Check types in nested object
          if (nestedSchema.types) {
            for (const [field, expectedType] of Object.entries(nestedSchema.types)) {
              if (
                data[nestedField][field] !== undefined &&
                !validateType(data[nestedField][field], expectedType)
              ) {
                errors.push(
                  `Field ${nestedField}.${field} should be of type ${expectedType}, got ${typeof data[nestedField][field]}`
                );
              }
            }
          }
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      data,
    };
  } catch (error) {
    return {
      valid: false,
      errors: [`Error reading file: ${error.message}`],
      data: null,
    };
  }
}

// Fix common issues in configuration files
async function fixConfigFile(filePath, schema, validationResult) {
  if (validationResult.valid || !validationResult.data) {
    return validationResult;
  }

  const data = { ...validationResult.data };
  let fixed = false;

  // Add missing required fields with default values
  if (schema.required) {
    for (const field of schema.required) {
      if (data[field] === undefined) {
        // Provide sensible defaults based on field name and type
        if (schema.types && schema.types[field]) {
          const type = schema.types[field];
          if (type === "string") {
            data[field] =
              field === "title"
                ? "William Zujkowski"
                : field === "description"
                  ? "Personal website and blog"
                  : field === "url"
                    ? "https://williamzujkowski.github.io"
                    : field === "author"
                      ? "William Zujkowski"
                      : "";
          } else if (type === "number") {
            data[field] = 0;
          } else if (type === "boolean") {
            data[field] = false;
          } else if (type === "array") {
            data[field] = [];
          } else if (type === "object") {
            data[field] = {};
          }
          fixed = true;
          console.log(`Added missing field ${field} with default value`);
        }
      }
    }
  }

  // Fix type issues by converting values
  if (schema.types) {
    for (const [field, expectedType] of Object.entries(schema.types)) {
      if (data[field] !== undefined && !validateType(data[field], expectedType)) {
        try {
          if (expectedType === "string") {
            data[field] = String(data[field]);
          } else if (expectedType === "number") {
            data[field] = Number(data[field]);
          } else if (expectedType === "boolean") {
            data[field] = Boolean(data[field]);
          } else if (expectedType === "array" && !Array.isArray(data[field])) {
            data[field] = data[field] ? [data[field]] : [];
          } else if (expectedType === "object" && typeof data[field] !== "object") {
            data[field] = {};
          }
          fixed = true;
          console.log(`Fixed type for field ${field}`);
        } catch (error) {
          console.error(
            `Could not convert ${field} to ${expectedType}: ${error.message}`
          );
        }
      }
    }
  }

  // Save the fixed data
  if (fixed) {
    await fs.writeFile(filePath, JSON.stringify(data, null, 2), "utf8");
    console.log(`Saved fixed version of ${path.basename(filePath)}`);
  }

  // Re-validate to see if fixes resolved the issues
  return await validateConfigFile(filePath, schema);
}

// Main validation function
async function validateConfigs() {
  console.log(
    `Validating configuration files${FIX_MODE ? " (with auto-fix enabled)" : ""}...`
  );

  let totalFiles = 0;
  let validFiles = 0;
  let fixedFiles = 0;

  // Validate root config files
  for (const [fileName, schema] of Object.entries(SCHEMAS)) {
    const filePath = path.join(CONFIG_DIR, fileName);

    try {
      // Check if file exists
      await fs.access(filePath);

      totalFiles++;
      console.log(`\nValidating ${fileName}...`);

      // Validate the file
      let validationResult = await validateConfigFile(filePath, schema);

      // Try to fix issues if requested
      if (!validationResult.valid && FIX_MODE) {
        console.log(`Attempting to fix issues in ${fileName}...`);
        validationResult = await fixConfigFile(filePath, schema, validationResult);
        if (validationResult.valid) {
          fixedFiles++;
        }
      }

      // Report validation results
      if (validationResult.valid) {
        console.log(`✓ ${fileName} is valid`);
        validFiles++;
      } else {
        console.error(`✗ ${fileName} has issues:`);
        validationResult.errors.forEach((error) => console.error(`  - ${error}`));
      }
    } catch (error) {
      if (error.code === "ENOENT") {
        console.warn(`⚠ ${fileName} does not exist, skipping`);
      } else {
        console.error(`Error validating ${fileName}:`, error);
      }
    }
  }

  // Validate subdirectory config files
  for (const [dirName, dirSchemas] of Object.entries(SUBDIRECTORY_SCHEMAS)) {
    const dirPath = path.join(CONFIG_DIR, dirName);

    try {
      // Check if directory exists
      await fs.access(dirPath);

      for (const [fileName, schema] of Object.entries(dirSchemas)) {
        const filePath = path.join(dirPath, fileName);

        try {
          // Check if file exists
          await fs.access(filePath);

          totalFiles++;
          console.log(`\nValidating ${dirName}/${fileName}...`);

          // Validate the file
          let validationResult = await validateConfigFile(filePath, schema);

          // Try to fix issues if requested
          if (!validationResult.valid && FIX_MODE) {
            console.log(`Attempting to fix issues in ${dirName}/${fileName}...`);
            validationResult = await fixConfigFile(filePath, schema, validationResult);
            if (validationResult.valid) {
              fixedFiles++;
            }
          }

          // Report validation results
          if (validationResult.valid) {
            console.log(`✓ ${dirName}/${fileName} is valid`);
            validFiles++;
          } else {
            console.error(`✗ ${dirName}/${fileName} has issues:`);
            validationResult.errors.forEach((error) => console.error(`  - ${error}`));
          }
        } catch (error) {
          if (error.code === "ENOENT") {
            console.warn(`⚠ ${dirName}/${fileName} does not exist, skipping`);
          } else {
            console.error(`Error validating ${dirName}/${fileName}:`, error);
          }
        }
      }
    } catch (error) {
      if (error.code === "ENOENT") {
        console.warn(`⚠ Directory ${dirName} does not exist, skipping`);
      } else {
        console.error(`Error accessing directory ${dirName}:`, error);
      }
    }
  }

  // Print summary
  console.log("\nValidation Summary:");
  console.log(`Total files checked: ${totalFiles}`);
  console.log(`Valid files: ${validFiles}`);
  if (FIX_MODE) {
    console.log(`Files automatically fixed: ${fixedFiles}`);
  }
  console.log(`Files with issues: ${totalFiles - validFiles}`);

  // Exit with appropriate code
  process.exit(totalFiles === validFiles ? 0 : 1);
}

// Run the validation
validateConfigs();
