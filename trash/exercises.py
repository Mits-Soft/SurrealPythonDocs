# files = ["file1","file2","file3","file4","file5"]

# for index, name in enumerate(files, start=1):
#     print(f"Archivo {index}: {name}" )

# index = 1   
# while index < len(files):
#    print(f"Archivo {index}: {files[index - 1]}")
#    index += 1 
   
# z = zip((range(len(files))), files)

# print("Files zipeado")
# for zn, file in enumerate(z):
#     print(f"{zn} es : {file}")
    
# for i in range(2, 6):
#     print(i)
    
# from pathlib import Path
# ruta = Path("carpeta") / "subcarpeta" / "archivo.txt"
# print(ruta)  # "carpeta/subcarpeta/archivo.txt"

# print(f"Las partes de la ruta son: {ruta.parts}")

# mr = Path("source")

# print(f"La versión absoluta es: {mr.absolute}")

import os
from pathlib import Path

# class MrWalk:
#     def __init__(self, root_path):
#         if not isinstance(root_path, Path):
#             raise TypeError("root_path must be a pathlib.Path object")
#         if not root_path.exists():
#             raise FileNotFoundError(f"The path {root_path} does not exist")
#         if not root_path.is_dir():
#             raise NotADirectoryError(f"The path {root_path} is not a directory")
        
#         self.root_path = root_path

#     def walk(self):
#         mrwalk = {}
#         for root, dirs, files in os.walk(self.root_path):
#             root_parts = Path(root).parts
#             current_level = mrwalk
#             for part in root_parts:
#                 current_level = current_level.setdefault(part, {})
#             for dir in dirs:
#                 current_level[dir] = {}
#                 print(f"Root: {root}")
#                 print(f"Folder: {dir}")
#             for file in files:
#                 current_level[file] = Path(file).suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
#                 print(f"Root: {root}")
#                 print(f"File: {file}")
#         return mrwalk

# Modified constructor to accept string paths with "/" and convert them internally to Path
class MrWalk:
    def __init__(self, root_path):
        if not isinstance(root_path, str):
            raise TypeError("root_path must be a string")
        # Split the string by "/" and create a Path object
        ps = root_path.split("/")
        np = []
        i = 0
        for s in ps:           
            np.append(str(s).strip().replace('"', ''))
            i += 1
        root_path = Path(*np)
        
        
        if not root_path.exists():
            raise FileNotFoundError(f"The path {root_path} does not exist")
        if not root_path.is_dir():
            raise NotADirectoryError(f"The path {root_path} is not a directory")
        
        self.root_path = root_path
        
        if not root_path.exists():
            raise FileNotFoundError(f"The path {root_path} does not exist")
        if not root_path.is_dir():
            raise NotADirectoryError(f"The path {root_path} is not a directory")
        
        self.root_path = root_path

    def walk(self):
        mrwalk = {}
        for root, dirs, files in os.walk(self.root_path):
            root_parts = Path(root).parts
            current_level = mrwalk
            for part in root_parts:
                current_level = current_level.setdefault(part, {})
            print(f"Root: {root}")
            for dir in dirs:
                current_level[dir] = {}
                print(f"Folder: {dir}")
            for file in files:
                current_level[file] = Path(file).suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
                print(f"File: {file}")
        return mrwalk

# Example usage:
# root_path = "." / "source" / "jsondot"
walker = MrWalk('"."')
structure = walker.walk()
print(structure)

# import os

# mrwalk = {}
# for root, dirs, files in os.walk("source"):
#     root_parts = Path(root).parts
#     current_level = mrwalk
#     for part in root_parts:
#         current_level = current_level.setdefault(part, {})
#     for dir in dirs:
#         current_level[dir] = {}
#         print(f"Root: {root}")
#         print(f"Folder: {dir}")
#     for file in files:
#         current_level[file] = Path(file).suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
#         print(f"Root: {root}")
#         print(f"File: {file}")
    
# print("Motherfucker!!! ")
