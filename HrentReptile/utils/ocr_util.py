import pytesseract
from PIL import Image
from urllib.request import urlopen
import io


def image_to_string(url):
    image_bytes = urlopen(url).read()
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 7')
    image.save('D:/Document/tesseract-images/%s.tiff' % url.split('/')[len(url.split('/')) - 1].split('.')[0])
    return text
