import os
from pathlib import Path
class Surreal:
    def __init__(self):
        self.structure = {}
        self.files = []
        self.structure = self.search_python_files(os.path.relpath(".\\"))
        pass    

    def search_python_files(self, path):
        path = Path(path)
        carpeta_obj = {
            "name": path.name or str(path),
            "files": [],
            "folders": []
        }

        for item in path.iterdir():
            if item.is_file() and item.suffix == ".py":
                carpeta_obj["files"].append(item.name)
            
            elif item.is_dir():
                carpeta_obj["folders"].append(self.search_python_files(item))

        return carpeta_obj
        
    # def search_python_files(self, folder):
    #     python_files = []
    #     current_dir_parent = self.structure
    #     prev_dir_parent = {}
    #     for root, directories, files in os.walk(folder):
    #         for d in directories:
    #             if d not in current_dir_parent:
    #                 prev_dir_parent[root] = {}
    #                 prev_dir_parent[root][d] = {}
    #             current_dir_parent  = prev_dir_parent
    #         for file in files:
    #             if file.endswith(".py"):
    #                 full_path = os.path.join(root, file)
    #                 python_files.append(full_path)
    #     self.files = python_files
    
if __name__ == "__main__":
    Surreal()