# mi_script.py
import sys
from pathlib import Path

ruta_base = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_base / 'MrWalk'))

from mrwalk import MrWalk

class Surreal:
    def __init__(self):
        
        self.charles = MrWalk(' "." / "SurrealPythonDocs" ')
        
        print("Charles Walk is charged")
        
        self.structure = self.charles.walk([".py"], [".git", ".vscode"])
        
        print(f"The structure is: {self.structure}")
    
if __name__ == "__main__":
    Surreal()