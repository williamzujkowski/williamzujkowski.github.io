/**
 * Backup Old CSS Files
 * 
 * This script moves old CSS files to the backup directory with timestamps.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..', '..');
const cssDir = path.join(rootDir, 'src', 'css');
const backupDir = path.join(cssDir, 'backup');

// Create backup directory if it doesn't exist
if (!fs.existsSync(backupDir)) {
  fs.mkdirSync(backupDir, { recursive: true });
}

// Files to backup
const filesToBackup = [
  'styles.css',
  'basic.css',
  'blog-enhanced.css'
];

// Get timestamp
const timestamp = new Date().toISOString().replace(/:/g, '-');

// Backup files
let backupCount = 0;
for (const file of filesToBackup) {
  const srcPath = path.join(cssDir, file);
  
  if (fs.existsSync(srcPath)) {
    const destPath = path.join(backupDir, `${file}.${timestamp}.bak`);
    fs.copyFileSync(srcPath, destPath);
    backupCount++;
    console.log(`Backed up ${file} to ${destPath}`);
  }
}

console.log(`Backed up ${backupCount} CSS files`);