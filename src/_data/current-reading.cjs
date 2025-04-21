// src/_data/current-reading.cjs
// This file loads current-reading.json data for use in templates

const fs = require("fs");
const path = require("path");

module.exports = function () {
  // Set the path to the current-reading.json file
  const dataPath = path.join(__dirname, "..", "..", "_data", "current-reading.json");

  try {
    // Check if the file exists
    if (fs.existsSync(dataPath)) {
      // Read and parse the JSON file
      const fileContents = fs.readFileSync(dataPath, "utf8");
      // Check if the content is not empty and parse it
      if (fileContents && fileContents.trim() !== "") {
        const data = JSON.parse(fileContents);
        // Debug output
        console.log("Loaded current reading data:", JSON.stringify(data));
        return data;
      } else {
        console.warn(
          "Warning: current-reading.json is empty. Using empty array instead."
        );
        return [];
      }
    } else {
      console.warn(
        "Warning: current-reading.json not found. Using empty array instead."
      );
      return [];
    }
  } catch (error) {
    console.error("Error reading current-reading.json:", error);
    return [];
  }
};
