## Setup
```
uv sync
source .venv/bin/activate
uv pip install pip setuptools
```


For English spaCY model
```
python -m spacy download en_core_web_lg
```

To work with images using Tesseract OCR
```
brew install tesseract
```

## Anonymize text
Using the stock entities that Presidio supports
```
python default_entities.py
```

Using the custom entities
```
python custom_entities.py
```

## Anonymize image
This will take the image from the data directory and try to anonymize it and create a new image with `anonymized` prepended to the image name
```
python anonymize_image.py image_with_text.png
```