from PIL import Image
from presidio_image_redactor import ImageRedactorEngine
import sys

# Fetch filename from cli args
filename = sys.argv[1]

# Get the image to redact using PIL lib (pillow)
image = Image.open(f"./data/{filename}")

# Initialize the engine
engine = ImageRedactorEngine()

# Redact the image with pink color
redacted_image = engine.redact(image, (255, 192, 203))

# save the redacted image 
redacted_image.save(f"./data/anonymized_{filename}")