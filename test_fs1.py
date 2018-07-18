import time

from faceSynthesis import FaceSynthesis

# cst_time=1.16

start_time = time.time()

fs = FaceSynthesis()

base_path = r'/home/wangkun/Desktop/'
img1 = base_path + 'l.png'
img2 = base_path + 'k.jpg'

fs.get_face_synthesis(img1, img2)

end_time = time.time()

cost_time = end_time - start_time

print(cost_time)


