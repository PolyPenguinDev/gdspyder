from PIL import Image
import threading

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
        return self._operate(other, lambda x, y: x * y / 255)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._operate(other, lambda x, y: x / y * 255)

    def __rtruediv__(self, other):
        return self._operate(other, lambda x, y: y / x * 255)

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
    return vector.x, vector.y

def tupleToVector(vector: tuple):
    return Vector2(vector[0], vector[1])

def colorToTuple(color: Color):
    return round(color.r), round(color.g), round(color.b), round(color.a)

def tupleToColor(color: tuple):
    return Color(color[0],color[1],color[2],color[3])

def create_rectangles(start_x, end_x, start_y, end_y, fragment, scale, image):
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            color = fragment(Vector2(x/scale, y/scale))
            image.putpixel((x, y), colorToTuple(color))

def createTexture(size: Vector2, fragment: callable, quality=1, scale=1, num_threads=1) -> Image.Image:
    if quality != 1:
        return createTexture(size*quality, fragment, 1, scale, num_threads).resize((size.x, size.y))
    
    width, height = vectorToTuple(size)
    out = Image.new('RGBA', (width, height), (255, 255, 255, 255)) # Initialize output image

    threads = []
    chunk_size_x = width // num_threads
    chunk_size_y = height // num_threads

    for i in range(num_threads):
        start_x = i * chunk_size_x
        end_x = (i + 1) * chunk_size_x
        start_y = 0
        end_y = height
        thread = threading.Thread(target=create_rectangles, args=(start_x, end_x, start_y, end_y, fragment, scale, out))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return out

def texture(TEXTURE, TEXTURECOORD):
    return tupleToColor(TEXTURE.getpixel(vectorToTuple(TEXTURECOORD)))
def shader(image: Image.Image, fragment:callable):
    image = image.convert("RGBA")
    width, height = image.size
    out = Image.new('RGBA', (width, height), 0xffffff)
    for x in range(width):
        for y in range(height):
            out.putpixel((x,y), colorToTuple(fragment(Vector2(x, y), image)))
    return out