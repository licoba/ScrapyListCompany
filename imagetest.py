from PIL import Image
import pytesseract

codes = pytesseract.image_to_string(Image.open('telephone.png'))
print(codes)