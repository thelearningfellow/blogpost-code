from transformers import AutoModel, AutoTokenizer
import torch
import os
import argparse
import fitz  # PyMuPDF
from PIL import Image

os.environ["CUDA_VISIBLE_DEVICES"] = '0'

model_name = 'deepseek-ai/DeepSeek-OCR'

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, _attn_implementation='flash_attention_2', trust_remote_code=True, use_safetensors=True)
model = model.eval().cuda().to(torch.bfloat16)

def main():
    parser = argparse.ArgumentParser(description="Run OCR on a PDF file.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("output_path", help="Path to the output directory.")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    # Convert PDF to images
    pdf_document = fitz.open(args.pdf_path)
    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    prompt = "<image>\n<|grounding|>Convert the document to markdown. "

    for i, image in enumerate(images):
        image_path = os.path.join(args.output_path, f"page_{i+1}.jpg")
        image.save(image_path, "JPEG")

        res = model.infer(
            tokenizer,
            prompt=prompt,
            image_file=image_path,
            output_path=args.output_path,
            base_size=1024,
            image_size=640,
            crop_mode=True,
            save_results=True,
            test_compress=True
        )
        print(f"Processed page {i+1}")

if __name__ == "__main__":
    main()
