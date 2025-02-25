const fs = require('fs');
const path = require('path');

const logFilePath = path.join(__dirname, 'error.log');

function logError(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `${timestamp} - ERROR: ${message}\n`;
    fs.appendFileSync(logFilePath, logMessage, { encoding: 'utf8' });
    console.error(logMessage);
}

function logInfo(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `${timestamp} - INFO: ${message}\n`;
    fs.appendFileSync(logFilePath, logMessage, { encoding: 'utf8' });
    console.log(logMessage);
}

module.exports = {
    logError,
    logInfo,
};
