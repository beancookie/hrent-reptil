import pytesseract
from PIL import Image
from urllib.request import urlopen
import io


def image_to_string(url):
    # url = 'https://tse3.mm.bing.net/th?id=OIP.yhBBCRwWFrN_LvUVisIniAHaFn&pid=Api'
    image_bytes = urlopen(url).read()
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 7')
    return text
