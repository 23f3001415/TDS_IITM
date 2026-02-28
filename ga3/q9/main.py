import json
import sys

import fitz  # PyMuPDF


def extract_boxes(pdf_path: str, target_text: str):
    doc = fitz.open(pdf_path)
    try:
        all_boxes = []
        for page in doc:
            rects = page.search_for(target_text)
            for r in rects:
                all_boxes.append(
                    [int(round(r.x0)), int(round(r.y0)), int(round(r.x1)), int(round(r.y1))]
                )
        return all_boxes
    finally:
        doc.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <pdf_path> <text>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    target_text = sys.argv[2]
    boxes = extract_boxes(pdf_path, target_text)
    print(json.dumps(boxes))


if __name__ == "__main__":
    main()
