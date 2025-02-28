const getDailyFact = require('../_data/numbersAPI');

module.exports = async (req, res) => {
    try {
        const fact = await getDailyFact();
        res.setHeader('Content-Type', 'text/plain');
        res.end(fact);
    } catch (error) {
        console.error('Error fetching daily fact:', error);
        res.statusCode = 500;
        res.end('Could not fetch the daily fact. Please try again later.');
    }
};
