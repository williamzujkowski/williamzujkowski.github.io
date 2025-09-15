/**
 * Basic Test Runner for williamzujkowski.github.io
 * Provides simple testing infrastructure for the static site
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class TestRunner {
  constructor() {
    this.results = {
      passed: 0,
      failed: 0,
      skipped: 0,
      tests: []
    };
  }

  /**
   * Run all tests in a directory
   */
  async runTests(directory) {
    console.log(`\n🧪 Running tests in ${directory}...\n`);

    const files = fs.readdirSync(directory)
      .filter(file => file.endsWith('.test.js'));

    for (const file of files) {
      const testPath = path.join(directory, file);
      await this.runTestFile(testPath);
    }

    this.printResults();
  }

  /**
   * Run a single test file
   */
  async runTestFile(filePath) {
    const testName = path.basename(filePath, '.test.js');
    console.log(`  Running: ${testName}`);

    try {
      const absolutePath = path.resolve(filePath);
      const testModule = require(absolutePath);

      if (typeof testModule.test === 'function') {
        const result = await testModule.test();
        this.recordResult(testName, result);
      } else {
        this.recordResult(testName, {
          success: false,
          error: 'No test function exported'
        });
      }
    } catch (error) {
      this.recordResult(testName, {
        success: false,
        error: error.message
      });
    }
  }

  /**
   * Record test result
   */
  recordResult(name, result) {
    if (result.success) {
      this.results.passed++;
      console.log(`    ✅ ${name}: PASSED`);
    } else {
      this.results.failed++;
      console.log(`    ❌ ${name}: FAILED - ${result.error}`);
    }

    this.results.tests.push({
      name,
      ...result
    });
  }

  /**
   * Print test results summary
   */
  printResults() {
    console.log('\n' + '='.repeat(50));
    console.log('TEST RESULTS SUMMARY');
    console.log('='.repeat(50));
    console.log(`✅ Passed: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    console.log(`⏭️  Skipped: ${this.results.skipped}`);
    console.log('='.repeat(50));

    if (this.results.failed > 0) {
      console.log('\nFailed Tests:');
      this.results.tests
        .filter(t => !t.success)
        .forEach(t => console.log(`  - ${t.name}: ${t.error}`));
      process.exit(1);
    } else {
      console.log('\n🎉 All tests passed!');
      process.exit(0);
    }
  }
}

// Run tests if called directly
if (require.main === module) {
  const runner = new TestRunner();
  const testDir = process.argv[2] || path.join(__dirname, 'unit');
  runner.runTests(testDir);
}

module.exports = TestRunner;