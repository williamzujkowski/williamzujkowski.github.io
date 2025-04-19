/**
 * Global setup for Playwright tests
 * Part of Phase 4 testing implementation
 */

const { chromium } = require('@playwright/test');
const { ensureDir } = require('./helpers');
const config = require('./config');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

/**
 * Start server and setup directories for tests
 * @param {import('@playwright/test').FullConfig} testConfig
 */
async function globalSetup(testConfig) {
  // Ensure screenshot and report directories exist
  ensureDir(config.screenshotDir);
  ensureDir(config.reportDir);
  ensureDir(path.join(config.reportDir, 'artifacts'));
  
  // Check if we need to start a local server
  // Only start if baseUrl is localhost
  const needsServer = config.baseUrl.includes('localhost');
  
  if (needsServer) {
    try {
      // Try connecting to server first to see if it's already running
      const browser = await chromium.launch();
      const page = await browser.newPage();
      
      try {
        // If this fails, the server isn't running
        await page.goto(config.baseUrl, { timeout: 2000 });
        console.log('Development server is already running');
        global.__SERVER_ALREADY_RUNNING = true;
      } catch (e) {
        console.log('Starting development server...');
        
        // Start the development server
        const serverProcess = exec('npm run serve');
        
        // Store the server process for teardown
        global.__SERVER_PROCESS = serverProcess;
        
        // Wait for the server to start
        await new Promise(resolve => setTimeout(resolve, 10000));
        
        console.log('Development server started');
      } finally {
        await browser.close();
      }
    } catch (error) {
      console.error('Failed to start development server:', error);
      process.exit(1);
    }
  }
  
  // Create a timestamp for this test run
  global.__TEST_RUN_TIMESTAMP = new Date().toISOString().replace(/[:.]/g, '-');
}

module.exports = globalSetup;