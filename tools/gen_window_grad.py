from PIL import Image

width = 32
height = 32

top = (245, 249, 253)
bottom = (205, 221, 236)

image = Image.new("RGB", (width, height))

for y in range(height):
    t = y / (height - 1)

    r = int(top[0] * (1 - t) + bottom[0] * t)
    g = int(top[1] * (1 - t) + bottom[1] * t)
    b = int(top[2] * (1 - t) + bottom[2] * t)

    for x in range(width):
        image.putpixel((x, y), (r, g, b))

image.save("titlebar.png")