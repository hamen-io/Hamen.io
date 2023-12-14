from string import ascii_letters,digits,punctuation
import random
import hashlib

def generate_password() -> str:
  characters = list(ascii_letters + digits + punctuation)
  key = "".join(random.choices(characters, k = 512))
  key = key.encode()

  return hashlib.sha512(key).hexdigest()

if __name__ == "__main__":
  print(
    generate_password()
  )