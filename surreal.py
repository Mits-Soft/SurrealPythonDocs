# mi_script.py
import sys
from pathlib import Path

ruta_base = Path(__file__).resolve().parent.parent
mrwalk_path = ruta_base / 'MrWalk'

if mrwalk_path not in sys.path:
    sys.path.append(str(mrwalk_path))

from mrwalk import MrWalk

class Surreal:
    def __init__(self):
        
        self.charles = MrWalk(' "." / "SurrealPythonDocs" ')
        
        print("Charles Walk is charged")
        
        self.structure = self.charles.walk([".py"], [".git", ".vscode"])
        
        print(f"The structure is: {self.structure}")
        
        print(self.charles.tree())
        
        self.structure = self.charles.prune(["SurrealPythonDocs", "trash"])
        
        print(f"The structure after pruning example is: {self.structure}")
        
        print(self.charles.tree())
    
if __name__ == "__main__":
    Surreal()