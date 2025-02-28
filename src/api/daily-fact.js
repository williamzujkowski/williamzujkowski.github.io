const getDailyFact = require('../_data/numbersAPI');

module.exports = async (req, res) => {
    const fact = await getDailyFact();
    res.setHeader('Content-Type', 'text/plain');
    res.end(fact);
};
