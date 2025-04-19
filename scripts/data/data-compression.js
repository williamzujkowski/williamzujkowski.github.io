/**
 * Data Compression Utilities
 *
 * Utilities for optimizing and compressing JSON data
 */

/**
 * Compress JSON data by removing unnecessary fields and whitespace
 *
 * @param {Object|Array} data - The data to compress
 * @param {Object} options - Compression options
 * @param {boolean} options.removeNulls - Remove null/undefined values
 * @param {boolean} options.minify - Minify the output
 * @param {string[]} options.keepFields - Fields to always keep even if null
 * @param {string[]} options.removeFields - Fields to always remove
 * @returns {string} Compressed JSON string
 */
export function compressJsonData(data, options = {}) {
  const {
    removeNulls = true,
    minify = true,
    keepFields = [],
    removeFields = [],
  } = options;

  // Create a set of fields to keep/remove for faster lookups
  const keepFieldsSet = new Set(keepFields);
  const removeFieldsSet = new Set(removeFields);

  // Process the data recursively
  const processValue = (value, path = "") => {
    if (value === null || value === undefined) {
      return null;
    }

    if (Array.isArray(value)) {
      return value
        .filter((item) => item !== null && item !== undefined)
        .map((item, index) => processValue(item, `${path}[${index}]`));
    }

    if (typeof value === "object" && value !== null) {
      const result = {};

      for (const [key, val] of Object.entries(value)) {
        const fullPath = path ? `${path}.${key}` : key;

        // Skip fields in the remove list
        if (removeFieldsSet.has(key) || removeFieldsSet.has(fullPath)) {
          continue;
        }

        // Keep null/undefined values for fields in the keep list
        if (keepFieldsSet.has(key) || keepFieldsSet.has(fullPath)) {
          result[key] =
            val === null || val === undefined ? null : processValue(val, fullPath);
          continue;
        }

        // Skip null/undefined values if removeNulls is true
        if (removeNulls && (val === null || val === undefined)) {
          continue;
        }

        // Process the value recursively
        result[key] = processValue(val, fullPath);
      }

      return result;
    }

    return value;
  };

  // Process the data
  const processed = processValue(data);

  // Stringify with appropriate formatting
  return minify ? JSON.stringify(processed) : JSON.stringify(processed, null, 2);
}

/**
 * Extract a subset of fields from data objects
 *
 * @param {Object|Array} data - The data to extract fields from
 * @param {string[]} fields - Fields to extract
 * @param {boolean} preserveStructure - Whether to preserve the object structure
 * @returns {Object|Array} Data with only specified fields
 */
export function extractFields(data, fields, preserveStructure = false) {
  // Parse field paths (e.g., "user.profile.name")
  const parsedFields = fields.map((field) => field.split("."));

  // Process a single object
  const processObject = (obj) => {
    if (typeof obj !== "object" || obj === null) {
      return obj;
    }

    const result = {};

    for (const fieldPath of parsedFields) {
      let current = obj;
      let target = result;

      // Navigate to the nested value
      for (let i = 0; i < fieldPath.length; i++) {
        const field = fieldPath[i];

        if (current === undefined || current === null) {
          break;
        }

        if (i === fieldPath.length - 1) {
          // Last field, extract the value
          if (field in current) {
            if (preserveStructure && i > 0) {
              // Create nested structure
              let nestedTarget = result;
              for (let j = 0; j < i; j++) {
                const nestedField = fieldPath[j];
                nestedTarget[nestedField] = nestedTarget[nestedField] || {};
                nestedTarget = nestedTarget[nestedField];
              }
              nestedTarget[field] = current[field];
            } else {
              // Flatten the structure
              target[field] = current[field];
            }
          }
        } else if (preserveStructure) {
          // Create nested structure for intermediate fields
          current = current[field];
          target[field] = target[field] || {};
          target = target[field];
        } else {
          // Just navigate to next level
          current = current[field];
        }
      }
    }

    return result;
  };

  // Process array or object
  if (Array.isArray(data)) {
    return data.map(processObject);
  }

  return processObject(data);
}

/**
 * Strip HTML tags from text fields in data
 *
 * @param {Object|Array} data - The data containing HTML
 * @param {string[]} textFields - Fields that may contain HTML
 * @returns {Object|Array} Data with HTML stripped
 */
export function stripHtmlFromData(
  data,
  textFields = ["description", "content", "text"]
) {
  const stripHtml = (html) => {
    if (typeof html !== "string") return html;
    return html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
      .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, "")
      .replace(/<[^>]*>/g, " ")
      .replace(/\s{2,}/g, " ")
      .trim();
  };

  // Process all fields in an object
  const processObject = (obj) => {
    if (typeof obj !== "object" || obj === null) {
      return obj;
    }

    const result = Array.isArray(obj) ? [] : {};

    for (const [key, value] of Object.entries(obj)) {
      if (textFields.includes(key) && typeof value === "string") {
        result[key] = stripHtml(value);
      } else if (typeof value === "object" && value !== null) {
        result[key] = processObject(value);
      } else {
        result[key] = value;
      }
    }

    return result;
  };

  return processObject(data);
}

export default {
  compressJsonData,
  extractFields,
  stripHtmlFromData,
};
