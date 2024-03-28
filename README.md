<img src="https://github.com/PolyPenguinDev/gdspyder/blob/main/icon.png?raw=true" alt="gdspyder logo" width="200"/>

### A Godot inspired module to create and edit images in Python
## How to install
`pip install gdspyder`
## Usage
### Image Creation
```python
from gdspyder import * #import gdspyder

def fragmentTexture(UV):
    COLOR = Color(255, 255, 255, 255) #create a COLOR variable of a custom Color object
    UV += Vector2(3, 4) #UV is a Vector2 object
    COLOR.r = UV.x
    COLOR.g = UV.y
    return COLOR
size = Vector2(100, 100)
image = createTexture(size, fragmentTexture)
image.save("path/to/image.png")
```

### Image Modification
```python
from gdspyder import * #import gdspyder
from PIL import Image #Allow you to open image

def shaderTexture(UV, TEXTURE):
    COLOR = texture(TEXTURE, UV) #set the color to that pixle on the image
    bw = (COLOR.r + COLOR.g + COLOR.b)/3 #find the average of all the color channels
    COLOR = Color(bw, bw, bw, 255) #set the color to be a black and white version of og image
    return COLOR
size = Vector2(100, 100)
im = Image.open("path/to/input/image.png")
image = createTexture(im, fragmentShader)
image.save("path/to/output/image.png")
```