#!/usr/bin/env node

/**
 * Test LLM Providers
 *
 * This utility helps test both OpenAI and Gemini models with a simple prompt
 * to verify API keys and compare output quality.
 *
 * Usage:
 *   node test-models.js [--provider openai|gemini|both]
 */

const { program } = require("commander");
const dotenv = require("dotenv");
const { generateContent } = require("./llm-providers");

// Load environment variables
dotenv.config();

program
  .option(
    "-p, --provider <provider>",
    "Which LLM provider to test (openai, gemini, claude, or all)",
    "all"
  )
  .parse(process.argv);

const options = program.opts();

// Simple test prompt
const testPrompt = `
Please provide a short summary (3-4 sentences) of the dangers of path traversal vulnerabilities in web applications,
especially in cloud environments. Format your response as a brief paragraph suitable for a technical blog.
`;

async function testOpenAI() {
  console.log("\n=== Testing OpenAI ===");

  if (!process.env.OPENAI_API_KEY) {
    console.error("Error: OPENAI_API_KEY environment variable is missing");
    return false;
  }

  try {
    // Save the original LLM_PROVIDER
    const originalProvider = process.env.LLM_PROVIDER;
    process.env.LLM_PROVIDER = "openai";

    console.log("Sending test prompt to OpenAI...");
    const startTime = Date.now();
    const response = await generateContent(testPrompt, { model: "gpt-4-turbo" });
    const endTime = Date.now();

    console.log("\nResponse:");
    console.log(response);
    console.log(`\nGeneration took ${(endTime - startTime) / 1000} seconds`);

    // Restore the original provider
    process.env.LLM_PROVIDER = originalProvider;
    return true;
  } catch (error) {
    console.error(`Error testing OpenAI: ${error.message}`);
    return false;
  }
}

async function testGemini() {
  console.log("\n=== Testing Google Gemini (gemini-2.0-flash) ===");

  if (!process.env.GOOGLE_API_KEY) {
    console.error("Error: GOOGLE_API_KEY environment variable is missing");
    return false;
  }

  try {
    // Save the original LLM_PROVIDER
    const originalProvider = process.env.LLM_PROVIDER;
    process.env.LLM_PROVIDER = "gemini";

    console.log("Sending test prompt to Gemini...");
    const startTime = Date.now();
    const response = await generateContent(testPrompt, { model: "gemini-2.0-flash" });
    const endTime = Date.now();

    console.log("\nResponse:");
    console.log(response);
    console.log(`\nGeneration took ${(endTime - startTime) / 1000} seconds`);

    // Restore the original provider
    process.env.LLM_PROVIDER = originalProvider;
    return true;
  } catch (error) {
    console.error(`Error testing Gemini: ${error.message}`);
    return false;
  }
}

// Add function to test Claude
async function testClaude() {
  console.log("\n=== Testing Anthropic Claude ===");

  if (!process.env.CLAUDE_API_KEY) {
    console.error("Error: CLAUDE_API_KEY environment variable is missing");
    return false;
  }

  try {
    // Save the original LLM_PROVIDER
    const originalProvider = process.env.LLM_PROVIDER;
    process.env.LLM_PROVIDER = "claude";

    console.log("Sending test prompt to Claude...");
    const startTime = Date.now();
    const response = await generateContent(testPrompt, {
      model: "claude-3-opus-20240229",
    });
    const endTime = Date.now();

    console.log("\nResponse:");
    console.log(response);
    console.log(`\nGeneration took ${(endTime - startTime) / 1000} seconds`);

    // Restore the original provider
    process.env.LLM_PROVIDER = originalProvider;
    return true;
  } catch (error) {
    console.error(`Error testing Claude: ${error.message}`);
    return false;
  }
}

async function main() {
  console.log("Testing LLM providers with a simple prompt");

  let results = {
    openai: false,
    gemini: false,
    claude: false,
  };

  if (options.provider === "openai" || options.provider === "all") {
    results.openai = await testOpenAI();
  }

  if (options.provider === "gemini" || options.provider === "all") {
    results.gemini = await testGemini();
  }

  if (options.provider === "claude" || options.provider === "all") {
    results.claude = await testClaude();
  }

  console.log("\n=== Test Results ===");
  if (options.provider === "openai" || options.provider === "all") {
    console.log(`OpenAI: ${results.openai ? "SUCCESS ✅" : "FAILED ❌"}`);
  }
  if (options.provider === "gemini" || options.provider === "all") {
    console.log(`Gemini: ${results.gemini ? "SUCCESS ✅" : "FAILED ❌"}`);
  }
  if (options.provider === "claude" || options.provider === "all") {
    console.log(`Claude: ${results.claude ? "SUCCESS ✅" : "FAILED ❌"}`);
  }

  // Check if all tested providers are working
  const testedProviders = [];
  if ((options.provider === "openai" || options.provider === "all") && results.openai)
    testedProviders.push("OpenAI");
  if ((options.provider === "gemini" || options.provider === "all") && results.gemini)
    testedProviders.push("Gemini");
  if ((options.provider === "claude" || options.provider === "all") && results.claude)
    testedProviders.push("Claude");

  if (testedProviders.length > 0) {
    console.log(
      `\nWorking providers: ${testedProviders.join(", ")}. You can use any of these for generating vulnerability posts.`
    );
  }
}

main().catch((error) => {
  console.error("Unhandled error:", error);
  process.exit(1);
});
