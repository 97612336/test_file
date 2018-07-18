import os
import sys

home = os.environ['HOME']
# print(home)

new_home=os.environ.get("HOME","")
# print(new_home)

res=sys.argv[0]
print(res)