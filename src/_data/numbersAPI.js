const fetch = require('node-fetch');

async function getDailyFact() {
    const response = await fetch('http://numbersapi.com/random/date');
    const fact = await response.text();
    return fact;
}

module.exports = getDailyFact;
