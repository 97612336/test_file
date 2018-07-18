from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# 设置字体，如果没有，也可以不设置
# font = ImageFont.truetype()

# 打开底版图片
imageFile = "15.jpg"
im1 = Image.open(imageFile)

# 在图片上添加文字 1
draw = ImageDraw.Draw(im1)
draw.text((30, 20), "this is a word in the country", (255, 255, 0))
draw = ImageDraw.Draw(im1)

# 保存
im1.save("target.png")
