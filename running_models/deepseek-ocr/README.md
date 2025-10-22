Pytorch 2.8.0
GPU A40

cd home
git clone https://github.com/thelearningfellow/blogpost-code.git
cd blogpost-code/running_models/deepseek-ocr
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation
wget https://github.com/deepseek-ai/DeepSeek-OCR/raw/main/DeepSeek_OCR_paper.pdf
python run_ocr.py --pdf_path DeepSeek_OCR_paper.pdf --output_path output