/**
 * standardize-frontmatter.js
 *
 * Script to standardize frontmatter across all blog posts:
 * 1. Ensures all required frontmatter elements are present
 * 2. Adds eleventyNavigation to posts that don't have it
 * 3. Standardizes date formats
 * 4. Ensures consistent tag formatting
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { globSync } from "glob";
import matter from "gray-matter";
import slugify from "slugify";

// Set up paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "../");
const postsDir = path.join(projectRoot, "src/posts");

// Constants
const REQUIRED_FRONTMATTER = [
  "title",
  "description",
  "date",
  "layout",
  "tags",
  "image",
  "image_alt",
];

// Main function
async function standardizeFrontmatter() {
  console.log("Starting frontmatter standardization...");

  // Get all markdown files in posts directory
  const postFiles = globSync("*.md", { cwd: postsDir });
  console.log(`Found ${postFiles.length} blog posts to process`);

  let modified = 0;

  for (const file of postFiles) {
    const filePath = path.join(postsDir, file);
    const fileContent = fs.readFileSync(filePath, "utf8");

    // Parse frontmatter
    const { data, content } = matter(fileContent);

    // Track if we need to update this file
    let needsUpdate = false;

    // Check for required frontmatter
    for (const field of REQUIRED_FRONTMATTER) {
      if (!data[field]) {
        console.log(`Post ${file} is missing required frontmatter: ${field}`);

        // Add missing field with default value
        if (field === "layout") {
          data.layout = "post.njk";
          needsUpdate = true;
        } else if (field === "tags") {
          data.tags = ["posts"];
          needsUpdate = true;
        }
        // Other fields require manual intervention
      }
    }

    // Ensure date is in standardized format
    if (data.date) {
      // Convert to ISO string format if not already
      const dateStr = new Date(data.date).toISOString();
      if (dateStr !== data.date) {
        data.date = dateStr;
        needsUpdate = true;
      }
    }

    // Ensure tags includes 'posts' as the first tag
    if (data.tags && Array.isArray(data.tags)) {
      if (!data.tags.includes("posts")) {
        data.tags.unshift("posts");
        needsUpdate = true;
      } else if (data.tags[0] !== "posts") {
        // Reorder to make 'posts' the first tag
        data.tags = data.tags.filter((tag) => tag !== "posts");
        data.tags.unshift("posts");
        needsUpdate = true;
      }
    }

    // Add eleventyNavigation if missing
    if (!data.eleventyNavigation) {
      const title = data.title;
      // Create a slug from the title
      const key = slugify(title, { lower: true, strict: true });

      data.eleventyNavigation = {
        key,
        title: title.length > 40 ? title.substring(0, 40) + "..." : title,
        parent: "blog",
      };

      needsUpdate = true;
    }

    // Update file if changes were made
    if (needsUpdate) {
      // Create new content with updated frontmatter
      const updatedFileContent = matter.stringify(content, data);
      fs.writeFileSync(filePath, updatedFileContent);
      console.log(`Updated frontmatter for ${file}`);
      modified++;
    }
  }

  console.log(
    `Standardization complete. Modified ${modified} out of ${postFiles.length} files.`
  );
}

// Run the function
standardizeFrontmatter().catch((error) => {
  console.error("Error standardizing frontmatter:", error);
  process.exit(1);
});
