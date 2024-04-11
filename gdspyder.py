from PIL import Image

class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def _operate(self, other, operation):
        if isinstance(other, (int, float)):
            return Color(operation(self.r, other),
                         operation(self.g, other),
                         operation(self.b, other),
                         operation(self.a, other))
        elif isinstance(other, Color):
            return Color(operation(self.r, other.r),
                         operation(self.g, other.g),
                         operation(self.b, other.b),
                         operation(self.a, other.a))
        else:
            raise TypeError(f"Unsupported operand type(s) for operation: 'Color' and '{type(other)}'")

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)

    def __rsub__(self, other):
        return self._operate(other, lambda x, y: y - x)

    def __mul__(self, other):
        return self._operate(other, lambda x, y: x * y)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._operate(other, lambda x, y: x / y)

    def __rtruediv__(self, other):
        return self._operate(other, lambda x, y: y / x)

    def __floordiv__(self, other):
        return self._operate(other, lambda x, y: x // y)

    def __rfloordiv__(self, other):
        return self._operate(other, lambda x, y: y // x)

    def __mod__(self, other):
        return self._operate(other, lambda x, y: x % y)

    def __rmod__(self, other):
        return self._operate(other, lambda x, y: y % x)

    def __pow__(self, other):
        return self._operate(other, lambda x, y: x ** y)

    def __rpow__(self, other):
        return self._operate(other, lambda x, y: y ** x)

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def _operate(self, other, operation):
        if isinstance(other, (int, float)):
            return Vector2(operation(self.x, other),
                         operation(self.y, other))
        elif isinstance(other, Vector2):
            return Vector2(operation(self.x, other.x),
                         operation(self.y, other.y))
        else:
            raise TypeError(f"Unsupported operand type(s) for operation: 'Vector2' and '{type(other)}'")

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)

    def __rsub__(self, other):
        return self._operate(other, lambda x, y: y - x)

    def __mul__(self, other):
        return self._operate(other, lambda x, y: x * y)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._operate(other, lambda x, y: x / y)

    def __rtruediv__(self, other):
        return self._operate(other, lambda x, y: y / x)

    def __floordiv__(self, other):
        return self._operate(other, lambda x, y: x // y)

    def __rfloordiv__(self, other):
        return self._operate(other, lambda x, y: y // x)

    def __mod__(self, other):
        return self._operate(other, lambda x, y: x % y)

    def __rmod__(self, other):
        return self._operate(other, lambda x, y: y % x)

    def __pow__(self, other):
        return self._operate(other, lambda x, y: x ** y)

    def __rpow__(self, other):
        return self._operate(other, lambda x, y: y ** x)

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

def vectorToTuple(vector: Vector2):
    return((vector.x, vector.y))

def tupleToVector(vector: tuple):
    return Vector2(vector[0], vector[1])

def colorToTuple(color: Color):
    return((round(color.r), round(color.g), round(color.b), round(color.a)))

def tupleToColor(color: tuple):
    return Color(color[0],color[1],color[2],color[3])

def createTexture(size: tuple, fragment: callable, quality=1, scale=1):
    size *= scale
    width, height = vectorToTuple(size)
    out = Image.new('RGBA', (width, height), 0xffffff) 
    for x in range(width):
        for y in range(height):
            color = Color(0, 0, 0, 0)
            qual = quality * quality  # Total number of samples
            for lx in range(quality):
                for ly in range(quality):
                    sample_x = (x + (lx + 0.5) / quality) / scale
                    sample_y = (y + (ly + 0.5) / quality) / scale
                    color += fragment(Vector2(sample_x, sample_y))
            out.putpixel((x, y), colorToTuple(color / qual))
    return out

def texture(TEXTURE, TEXTURECOORD):
    return tupleToColor(TEXTURE.getpixel(vectorToTuple(TEXTURECOORD)))
def shader(image: Image, fragment:callable):
    image = image.convert("RGBA")
    width, height = image.size
    out = Image.new('RGBA', (width, height), 0xffffff)
    for x in range(width):
        for y in range(height):
            out.putpixel((x,y), colorToTuple(fragment(Vector2(x, y), image)))
    return out