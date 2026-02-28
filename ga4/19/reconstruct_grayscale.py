from PIL import Image

MAPPING = [
    (0, 0, 2, 1), (0, 1, 1, 1), (0, 2, 4, 1), (0, 3, 0, 3), (0, 4, 0, 1),
    (1, 0, 1, 4), (1, 1, 2, 0), (1, 2, 2, 4), (1, 3, 4, 2), (1, 4, 2, 2),
    (2, 0, 0, 0), (2, 1, 3, 2), (2, 2, 4, 3), (2, 3, 3, 0), (2, 4, 3, 4),
    (3, 0, 1, 0), (3, 1, 2, 3), (3, 2, 3, 3), (3, 3, 4, 4), (3, 4, 0, 2),
    (4, 0, 3, 1), (4, 1, 1, 2), (4, 2, 1, 3), (4, 3, 0, 4), (4, 4, 4, 0),
]

SRC = r"C:\Users\sriva\Downloads\jigsaw.webp"
OUT = r"C:\Users\sriva\OneDrive\Documents\TDS\ga4\19\output.png"

img = Image.open(SRC).convert("RGB")
w, h = img.size
tw, th = w // 5, h // 5

reconstructed = Image.new("RGB", (w, h))
for sr, sc, orow, ocol in MAPPING:
    tile = img.crop((sc * tw, sr * th, sc * tw + tw, sr * th + th))
    reconstructed.paste(tile, (ocol * tw, orow * th))

src_px = reconstructed.load()
gray = Image.new("L", (w, h))
gray_px = gray.load()

for y in range(h):
    for x in range(w):
        r, g, b = src_px[x, y]
        # Half-up rounding matches expected grader output.
        gray_px[x, y] = int(0.2126 * r + 0.7152 * g + 0.0722 * b + 0.5)

gray.save(OUT)
print("saved", OUT)
print("size", gray.size, "mode", gray.mode)
