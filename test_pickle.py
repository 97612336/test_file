import pickle

with open("a","rb") as f1:
    num_list=pickle.load(f1)

print(num_list)
print(type(num_list))