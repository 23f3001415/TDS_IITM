// Function that counts frequency of each item in an array
function countFrequency(items) {
  return items.reduce((frequencyMap, item) => {
    frequencyMap[item] = (frequencyMap[item] || 0) + 1;
    return frequencyMap;
  }, {});
}

module.exports = { countFrequency };
