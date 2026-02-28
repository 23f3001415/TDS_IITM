# Question 19: Reconstruct and Desaturate an Image

## Final Output (upload this file)
- [output.png](C:\Users\sriva\OneDrive\Documents\TDS\ga4\19\output.png)

## ELI15 Step-by-Step (for a complete novice)
1. Open the scrambled image `jigsaw.webp`.
2. Split it into a 5x5 tile grid (each tile is 100x100 for a 500x500 image).
3. Use the given mapping table to move each scrambled tile to its original position.
4. After reconstruction, convert each pixel to grayscale using:
   - `L = int(0.2126*R + 0.7152*G + 0.0722*B + 0.5)`
5. Save the grayscale image as a lossless PNG (`output.png`) without resizing.
6. Upload `output.png` to the grader.

## Repro script
- [reconstruct_grayscale.py](C:\Users\sriva\OneDrive\Documents\TDS\ga4\19\reconstruct_grayscale.py)
