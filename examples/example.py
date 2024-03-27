from gdspyder import *

size = Vector2(500, 500)
def fragmentTexture(UV):
    UV/=500/255
    COLOR = Color(UV.x,UV.y,(UV.x+UV.y)/2, 255)
    return COLOR
image = createTexture(size, fragmentTexture)
image.save("foo.png")