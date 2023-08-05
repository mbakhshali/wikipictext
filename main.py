import requests
import re
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def wikiPic(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.content, 'html.parser')

    # finds H1
    try:
        txt = bsObj.h1.get_text()
    except:
        txt = ''

    try:
        # looks for the class names, in order to find the img tag inside
        img = bsObj.findAll('td', {'class': re.compile('^infobox|^sidebar|^image$')})[0].findNext('img').attrs['src']

        # makes the absolute URL
        img = 'https:' + img

        # gets the img
        img = requests.get(img, stream=True).content

        # open the img (URL-based)
        img = Image.open(BytesIO(img))

        # make an object of the img
        imgObj = ImageDraw.Draw(img)

        # set the font details
        myfont = ImageFont.truetype('Comen.ttf', 17)

        # print on the img
        imgObj.text(((img.width / len(txt) * 4), 0), txt, fill='white', stroke_width=1, stroke_fill='black', font=myfont)

        try:
            # saves the img with text on it
            img.save(txt + ".jpg")
        except:
            img.save(txt + ".png")

        # open the final result
        img.show()

    # if no img was found, it creates an empty colored box
    except:
        img = Image.new('RGB', (400, 400), color='salmon')
        imgObj = ImageDraw.Draw(img)
        txt = '404 Error'
        myfont = ImageFont.truetype('Comen.ttf', 17)
        imgObj.text(((img.width / len(txt)*4), 0), txt, fill='red', stroke_width=1, stroke_fill='black', font=myfont)
        img.save("404.jpg")
        img.show()


# URL of the English wikipedia
wikiPic('https://en.wikipedia.org/wiki/Sylvester_Stallone')
