import hashlib
import uuid

def hash_password(raw):
  salt = uuid.uuid4().hex
  hashed = hashlib.sha512(raw + salt).hexdigest()
  return hashed + '$' + salt

def is_password_valid(raw, hashed, salt):
  h = hashlib.sha512(raw + salt).hexdigest()
  if h == hashed:
    return true
  else:
    return false;
