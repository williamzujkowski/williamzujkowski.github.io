#!/usr/bin/env node

/**
 * Knowledge Management Standards Validator
 * Checks if documentation follows KM standards
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Color codes for output
const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  reset: '\x1b[0m'
};

// Files to check
const requiredFiles = [
  'README.md',
  'CLAUDE.md',
  'MANIFEST.yaml'
];

const checks = {
  // Check if required files exist
  checkRequiredFiles: () => {
    console.log('\n📁 Checking required files...');
    let passed = true;
    
    requiredFiles.forEach(file => {
      if (fs.existsSync(file)) {
        console.log(`${colors.green}✓${colors.reset} ${file} exists`);
      } else {
        console.log(`${colors.red}✗${colors.reset} ${file} missing`);
        passed = false;
      }
    });
    
    return passed;
  },

  // Check README.md has version metadata
  checkReadmeMetadata: () => {
    console.log('\n📄 Checking README.md metadata...');
    const content = fs.readFileSync('README.md', 'utf8');
    const hasVersion = content.includes('**Version:**');
    const hasLastUpdated = content.includes('**Last Updated:**');
    const hasStatus = content.includes('**Status:**');
    
    const passed = hasVersion && hasLastUpdated && hasStatus;
    
    console.log(`${hasVersion ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Version`);
    console.log(`${hasLastUpdated ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Last Updated`);
    console.log(`${hasStatus ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Status`);
    
    return passed;
  },

  // Check MANIFEST.yaml is valid
  checkManifest: () => {
    console.log('\n📊 Checking MANIFEST.yaml...');
    
    try {
      const manifest = yaml.load(fs.readFileSync('MANIFEST.yaml', 'utf8'));
      const hasVersion = !!manifest.version;
      const hasDocuments = !!manifest.documents && manifest.documents.length > 0;
      const hasStack = !!manifest.stack;
      
      const passed = hasVersion && hasDocuments && hasStack;
      
      console.log(`${hasVersion ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Version`);
      console.log(`${hasDocuments ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Documents registry`);
      console.log(`${hasStack ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Technical stack`);
      
      return passed;
    } catch (e) {
      console.log(`${colors.red}✗${colors.reset} Invalid YAML: ${e.message}`);
      return false;
    }
  },

  // Check documentation structure
  checkDocStructure: () => {
    console.log('\n📚 Checking documentation structure...');
    const docsExists = fs.existsSync('docs');
    const hasGuides = fs.existsSync('docs/guides');
    const hasStandards = fs.existsSync('docs/standards');
    
    const passed = docsExists && hasGuides && hasStandards;
    
    console.log(`${docsExists ? colors.green + '✓' : colors.red + '✗'}${colors.reset} docs/ directory`);
    console.log(`${hasGuides ? colors.green + '✓' : colors.red + '✗'}${colors.reset} docs/guides/`);
    console.log(`${hasStandards ? colors.green + '✓' : colors.red + '✗'}${colors.reset} docs/standards/`);
    
    return passed;
  },

  // Check for cross-references
  checkCrossReferences: () => {
    console.log('\n🔗 Checking cross-references...');
    const content = fs.readFileSync('README.md', 'utf8');
    const hasClaude = content.includes('[CLAUDE.md]');
    const hasManifest = content.includes('[MANIFEST.yaml]');
    
    const passed = hasClaude && hasManifest;
    
    console.log(`${hasClaude ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Links to CLAUDE.md`);
    console.log(`${hasManifest ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Links to MANIFEST.yaml`);
    
    return passed;
  },

  // Check standards integration
  checkStandardsIntegration: () => {
    console.log('\n🎯 Checking standards integration...');
    
    // Check for standards submodule
    const hasSubmodule = fs.existsSync('.standards');
    console.log(`${hasSubmodule ? colors.green + '✓' : colors.red + '✗'}${colors.reset} .standards submodule`);
    
    // Check CLAUDE.md mentions standards router
    let claudeIntegration = false;
    if (fs.existsSync('CLAUDE.md')) {
      const claudeContent = fs.readFileSync('CLAUDE.md', 'utf8');
      claudeIntegration = claudeContent.includes('.standards/docs/core/CLAUDE.md');
    }
    console.log(`${claudeIntegration ? colors.green + '✓' : colors.red + '✗'}${colors.reset} CLAUDE.md integration`);
    
    // Check for standards checklist
    const hasChecklist = fs.existsSync('docs/STANDARDS_IMPLEMENTATION_CHECKLIST.md');
    console.log(`${hasChecklist ? colors.green + '✓' : colors.red + '✗'}${colors.reset} Standards checklist`);
    
    const passed = hasSubmodule && claudeIntegration && hasChecklist;
    return passed;
  }
};

// Run all checks
console.log('🔍 Knowledge Management Standards Validator\n');

const results = Object.values(checks).map(check => check());
const allPassed = results.every(result => result);

console.log('\n' + '='.repeat(40));
if (allPassed) {
  console.log(`${colors.green}✓ All checks passed!${colors.reset}`);
  process.exit(0);
} else {
  console.log(`${colors.red}✗ Some checks failed${colors.reset}`);
  console.log(`${colors.yellow}See above for details${colors.reset}`);
  process.exit(1);
}