import time

from new_fs import get_face_synthesis

# cost_time=0.23

start_time = time.time()

base_path = r'/home/wangkun/Desktop/'
img1 = base_path + '15.png'
img2 = base_path + '1236.png'

get_face_synthesis(img1, img2)

end_time = time.time()

cost_time = end_time - start_time

print(cost_time)
