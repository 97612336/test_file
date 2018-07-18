import base64

from aip import AipFace

APP_ID = "11208980"
API_KEY = "6eCk1WCGrTVpNkCfoNnkyaMP"
SECRET_KEY = "PL89yO7jpW7FtIifnr0Hni6teeC7mzG0"

cilent = AipFace(APP_ID, API_KEY, SECRET_KEY)

with open("/home/wangkun/Pictures/u=473021653,3453602651&fm=200&gp=0.jpg", "rb") as f1:
    b64_img = base64.b64encode(f1.read()).decode()

print(type(b64_img))

