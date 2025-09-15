/**
 * Scripts Tests
 * Validates Python and shell scripts
 */

const fs = require('fs');
const path = require('path');

module.exports = {
  async test() {
    try {
      const scriptsDir = path.join(__dirname, '../../scripts');

      // Test 1: Check if scripts directory exists
      if (!fs.existsSync(scriptsDir)) {
        return {
          success: false,
          error: 'Scripts directory not found'
        };
      }

      // Test 2: Check for critical scripts
      const criticalScripts = [
        'optimize-blog-content.py',
        'generate-blog-hero-images.py',
        'optimize-blog-images.sh'
      ];

      for (const script of criticalScripts) {
        const scriptPath = path.join(scriptsDir, script);
        if (!fs.existsSync(scriptPath)) {
          return {
            success: false,
            error: `Critical script ${script} not found`
          };
        }
      }

      // Test 3: Validate Python scripts have proper shebang
      const pythonScripts = fs.readdirSync(scriptsDir)
        .filter(file => file.endsWith('.py'));

      for (const script of pythonScripts) {
        const scriptPath = path.join(scriptsDir, script);
        const content = fs.readFileSync(scriptPath, 'utf8');
        const firstLine = content.split('\n')[0];

        // Check if executable scripts have shebang
        const stats = fs.statSync(scriptPath);
        if (stats.mode & parseInt('111', 8)) {  // Check if executable
          if (!firstLine.startsWith('#!/usr/bin/env python') && !firstLine.startsWith('#!/usr/bin/python')) {
            console.warn(`Warning: Executable script ${script} missing shebang`);
          }
        }
      }

      // Test 4: Check shell scripts are executable
      const shellScripts = fs.readdirSync(scriptsDir)
        .filter(file => file.endsWith('.sh'));

      for (const script of shellScripts) {
        const scriptPath = path.join(scriptsDir, script);
        const stats = fs.statSync(scriptPath);
        if (!(stats.mode & parseInt('111', 8))) {
          return {
            success: false,
            error: `Shell script ${script} is not executable`
          };
        }
      }

      return {
        success: true,
        message: `Script validation passed. Found ${pythonScripts.length} Python scripts and ${shellScripts.length} shell scripts.`
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};