import urllib
import re
import requests
import os
import sys
import Tkinter as tk
from PIL import Image
from bs4 import BeautifulSoup

def main(argv):
    url = 'http://explosm.net/comics/' + argv[0]
    print url

    link = urllib.urlopen(url)
    soup = BeautifulSoup(link, "html.parser")
    img = soup.findAll('img', {'id': "main-comic"})[0].get('src')
    img = "http://" + img[2:]

    f = open('temp.png','wb')
    f.write( requests.get(img ).content )
    f.close()

    comic = Image.open('temp.png','r')
    comic_width, comic_height = comic.size

    #defaults write com.apple.desktop Background '{default = {ImageFilePath = "/path/to/your/image"; }; }'; killAll Dock;

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    background = Image.new('RGBA', (screen_width+100,screen_height+100), (255,255,255,255))
    background_width, background_height = background.size

    #if(background_width < comic_width):

    imageName = img.split('/')[4]

    offset = ( (background_width - comic_width)/2, (background_height - comic_height)/2)
    offset_width, offset_height = offset
    print background.size
    print comic.size

    trueSize = True
    if comic_width > background_width*1.05 or comic_height > background_height*1.05:
        trueSize = False

    trueSizeCounter = 2
    while not trueSize:
        background = Image.new('RGBA', (screen_width*trueSizeCounter,screen_height*trueSizeCounter), (255,255,255,255))
        background_width, background_height = background.size
        offset = ((background_width - comic_width)/2, (background_height - comic_height)/2)
        if comic_width > background_width*1.05 or comic_height > background_height*1.05:
            trueSize = False
            trueSizeCounter = trueSizeCounter + 1
        else:
            trueSize = True


    background.paste(comic, offset)
    background.save(imageName + '.png')

    os.remove("temp.png")

    osxcmd = 'osascript -e \'tell application "System Events" to set picture of every desktop to "' + "/Users/stephen/Desktop/" + imageName + '.png' + '" \''
    os.system(osxcmd)

    os.remove(imageName + '.png')

if __name__ == "__main__":
    main(sys.argv[1:])
