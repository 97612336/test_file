from PIL import Image

def blend_two_images():
    img1 = Image.open("15.jpg")
    img1 = img1.convert('RGBA')

    img2 = Image.open("16.png")
    img2 = img2.convert('RGBA')

    img = Image.blend(img1, img2, 1)
    img.show()
    img.save("blend.png")

    return

blend_two_images()