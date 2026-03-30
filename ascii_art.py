from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps


img = Image.open("image_choice/image1.JPG")
img = img.filter(ImageFilter.SHARPEN)
enhancer = ImageEnhance.Contrast(img)

img = enhancer.enhance(4.5)
img = img.resize((76, 38))
print(f"Image size : {img.size}")
# Convert to grayscale — each pixel becomes one brightness number (0-255)
img = img.convert("L")
img = ImageOps.autocontrast(img)
sharpener = ImageEnhance.Sharpness(img)
img = sharpener.enhance(2.0)


pixels = list(img.get_flattened_data())
print(f"Total pixels: {len(pixels)}")
print(f"First 10 brightness values: {pixels[:10]}")

CHARS = "  .,:10@"

def brightness_to_char(brightness):
    # Map 0-255 to an index in the CHARS string
    
    index = int(brightness / 255 * (len(CHARS) - 1))
    return CHARS[index]


for b in pixels[:10]:
    print(f"{b} → {brightness_to_char(b)}")
# Build and print the Full ASCII art
for row in range(img.height):
    line = ""
    for col in range(img.width):
        brightness = img.getpixel((col, row))
        char = brightness_to_char(brightness)
        line += char   
    print(line)