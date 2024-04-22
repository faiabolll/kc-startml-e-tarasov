import hashlib

hash = hashlib.md5()
with open('image-3.jpg', 'rb') as f:
    hash.update(f.read())

print(hash.hexdigest())