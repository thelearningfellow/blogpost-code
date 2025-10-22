# How to run DeepSeek OCR
I have written this code and setup instructions using a runpod machine but this should work on any other GPU Cloud provider as well or your local linux machine.

## Environment
- Pytorch 2.8.0
- Python 3.12
- Ubuntu 24.04
- CUDA 12.8
- GPU: A40

## Setup
Install all the pre-requisites
```sh
cd home
git clone https://github.com/thelearningfellow/blogpost-code.git
cd blogpost-code/running_models/deepseek-ocr
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install setuptools psutil torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 
pip install flash-attn==2.7.3 --no-build-isolation
```
## Running the 
Download a sample PDF that you want to extract text from in the form of a markdown
```sh
wget https://github.com/deepseek-ai/DeepSeek-OCR/raw/main/DeepSeek_OCR_paper.pdf
```

Run DeepSeek OCR to convert the PDF doc to markdown
```sh
python run_ocr.py DeepSeek_OCR_paper.pdf output --combine
```

If you want to check other options available simply run
```sh
python run_ocr.py --help
```