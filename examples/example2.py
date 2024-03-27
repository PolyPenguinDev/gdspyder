from PIL import Image
from gdspyder import *
import random

def fragmentShader(UV, TEXTURE):
    d = random.randrange(0, 255)
    COLOR = texture(TEXTURE, UV)
    col = (COLOR.r/255*76) + (COLOR.g/255*150) + (COLOR.b/255*29)
    if col > d:
        col = 255
    else:
        col = 0
    COLOR=Color(col, col, col, 255)
    return COLOR

im = Image.open("foo.png")
image = shader(im, fragmentShader)
image.save("bar.png")