const { exec } = require('child_process');

exec('npm install -g pa11y', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error installing pa11y: ${error.message}`);
        return;
    }
    console.log(`Pa11y installed: ${stdout}`);
    
    exec('pa11y http://localhost:8080', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error running accessibility checks: ${error.message}`);
            return;
        }
        console.log(`Accessibility check results:\n${stdout}`);
    });
});
