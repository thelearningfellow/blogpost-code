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

def combine_files(output_path, combined_filename, keep_individual_files):
    combined_content = ""
    # Ensure the files are sorted by page number
    mmd_files = sorted([f for f in os.listdir(output_path) if f.endswith('.mmd') and f[:-4].isdigit()], key=lambda x: int(x[:-4]))
    for mmd_file in mmd_files:
        mmd_file_path = os.path.join(output_path, mmd_file)
        with open(mmd_file_path, "r") as f:
            combined_content += f.read() + "\n"
        if not keep_individual_files:
            os.remove(mmd_file_path)

    with open(os.path.join(output_path, combined_filename), "w") as f:
        f.write(combined_content)


def main():
    parser = argparse.ArgumentParser(description="Run OCR on a PDF file.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("output_path", help="Path to the output directory.")
    parser.add_argument("--combine", action="store_true", help="Combine all .mmd files into a single file.")
    parser.add_argument("--combined_filename", default="combined.mmd", help="Name of the combined file.")
    parser.add_argument("--keep_individual_files", action="store_true", help="Keep individual .mmd files after combining.")
    parser.add_argument("--model_setting", type=str, default="gundam", choices=["tiny", "small", "base", "large", "gundam"], help="Model setting to use for inference.")
    args = parser.parse_args()

    # Model settings
    settings = {
        "tiny": {"base_size": 512, "image_size": 512, "crop_mode": False},
        "small": {"base_size": 640, "image_size": 640, "crop_mode": False},
        "base": {"base_size": 1024, "image_size": 1024, "crop_mode": False},
        "large": {"base_size": 1280, "image_size": 1280, "crop_mode": False},
        "gundam": {"base_size": 1024, "image_size": 640, "crop_mode": True},
    }
    
    selected_setting = settings[args.model_setting]
    base_size = selected_setting["base_size"]
    image_size = selected_setting["image_size"]
    crop_mode = selected_setting["crop_mode"]

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

        model.infer(
            tokenizer,
            prompt=prompt,
            image_file=image_path,
            output_path=args.output_path,
            base_size=base_size,
            image_size=image_size,
            crop_mode=crop_mode,
            save_results=True,
            test_compress=True
        )
        
        # Rename the output file
        old_file_path = os.path.join(args.output_path, "result.mmd")
        new_file_path = os.path.join(args.output_path, f"{i+1}.mmd")
        os.rename(old_file_path, new_file_path)

        # Remove the temporary image file
        os.remove(image_path)

        print(f"Processed page {i+1}")

    # Combine all .mmd files into a single file
    if args.combine:
        combine_files(args.output_path, args.combined_filename, args.keep_individual_files)
        print(f"Combined all .mmd files into {args.combined_filename}")


if __name__ == "__main__":
    main()
