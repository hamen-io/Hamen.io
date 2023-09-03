import os
import shutil

def remove_py_cache() -> None:
  for root, dirs, files in os.walk(".", topdown=False):
      for dir_name in dirs:
         if dir_name == "__pycache__":
           dir_path = os.path.join(root, dir_name)
           shutil.rmtree(dir_path)

if __name__ == "__main__":
  remove_py_cache()