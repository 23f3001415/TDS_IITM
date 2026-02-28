# Question 9: GitHub Copilot Data Transformation

## Final Answer (submit this function)
```javascript
// Function that counts frequency of each item in an array
function countFrequency(items) {
  return items.reduce((frequencyMap, item) => {
    frequencyMap[item] = (frequencyMap[item] || 0) + 1;
    return frequencyMap;
  }, {});
}
```

## ELI15 Step-by-Step (for a complete novice)
1. Open VS Code and create `transform.js`.
2. Add this comment: `// Function that counts frequency of each item in an array`.
3. Let Copilot suggest code and accept it.
4. Use this test input:
   - `['apple', 'banana', 'apple', 'orange', 'banana', 'apple']`
5. Call `countFrequency(testData)`.
6. Expected output is:
   - `{ apple: 3, banana: 2, orange: 1 }`
7. Paste the function code in the grader.
