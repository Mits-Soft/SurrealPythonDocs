from MrWalk import MrWalk
from pathlib import Path
import re

class SurrealPythonDocs:
    def __init__(self, root_path="."):
        """
        Inicializa la clase con el directorio base a explorar.
        Si no se proporciona root_path, se usa el directorio actual.
        """
        self.set_root_path(root_path)
        self.tree = None
        self.generated_docstrings = {}
        print(f"SurrealPythonDocs: Surreal initialized with root_path: {self.root_path}")

    def set_root_path(self, root_path):
        """
        Cambia el root_path y reinicia el objeto MrWalk.
        """
        self.root_path = Path(root_path)
        self.charles = MrWalk(str(self.root_path))
        print(f"SurrealPythonDocs: Root path set to: {self.root_path}")

    def walk(self, include_extensions=None, exclude=None):
        """
        Realiza un recorrido por los archivos y directorios.
        """
        include_extensions = include_extensions or [".py"]
        exclude = exclude or [".git", ".vscode"]
        self.tree = self.charles.walk(include_extensions, exclude)
        print(f"SurrealPythonDocs: Tree structure: {self.tree}")
        return self.tree

    def prune(self, exclude_dirs):
        """
        Elimina directorios específicos del recorrido.
        """
        self.tree = self.charles.prune(exclude_dirs)
        print(f"SurrealPythonDocs: Pruned tree structure: {self.tree}")
        return self.tree

    def show_tree(self):
        """
        Devuelve la representación en árbol del directorio.
        """
        tree_output = self.charles.tree()
        print(tree_output)
        return tree_output

    def extract_docstrings(self):
        """
        Extrae los docstrings de los archivos .py en el árbol,
        reconstruyendo las rutas a partir de la estructura del objeto tree.
        También incluye el path relativo del archivo y el número de línea del objeto.
        """
        if not self.tree:
            print("SurrealPythonDocs: No tree structure found. Run walk() first.")
            return []

        docstrings = {}

        def traverse_tree(tree, current_path=""):
            for key, value in tree.items():
                new_path = f"{current_path}/{key}".lstrip("/") if current_path else key
                if isinstance(value, dict):
                    traverse_tree(value, new_path)
                elif key.endswith(".py"):
                    file_path = new_path
                    with open(file_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        visited_objects = set()  # Para evitar duplicados
                        for i, line in enumerate(lines):
                            if '"""' in line or "'''" in line:
                                # Buscar la línea anterior con class o def
                                title = "Module-level docstring"
                                line_number = i + 1  # Línea del docstring (1-based index)
                                for j in range(i - 1, -1, -1):
                                    stripped_line = lines[j].strip()
                                    if stripped_line.startswith(("class ", "def ")):
                                        title = stripped_line.split("(")[0].strip()  # Extract class or function name
                                        line_number = j + 1  # Línea del objeto (1-based index)
                                        break

                                # Evitar duplicados
                                object_key = (file_path, title, line_number)
                                if object_key in visited_objects:
                                    continue
                                visited_objects.add(object_key)

                                # Extraer el contenido del docstring
                                docstring_lines = [line.strip()]
                                for k in range(i + 1, len(lines)):
                                    docstring_lines.append(lines[k].strip())
                                    if lines[k].strip().endswith(('"""', "'''")):
                                        break
                                description = "\n".join(docstring_lines).strip('"""').strip("'''").strip()
                                if file_path not in docstrings:
                                    docstrings[file_path] = []
                                docstrings[file_path].append({
                                    "title": title,
                                    "description": description,
                                    "line_number": line_number
                                })

        traverse_tree(self.tree)
        print(f"SurrealPythonDocs: Extracted docstrings: {docstrings}")
        self.generated_docstrings = docstrings
        return docstrings
    
class HtmlDocument:
    def __init__(self, title, year, company, license):
        self.template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body>
            <!-- Content goes here -->
        </body>
        <footer>
            <p>&copy; {year} {company}. All rights reserved. Licensed under {license}.</p>
        </footer>
        </html>
        """

    def add_content(self, content):
        """Reemplaza el marcador de contenido en el template."""
        self.template = self.template.replace(
            "<!-- Content goes here -->", content)


class ClassDiv:
    def __init__(self, name, description):
        self.template = f"""
        <div>
            <h1>{name}</h1>
            <p>{description}</p>
            <div class="methods">
            <h2>Métodos</h2>
            <!-- Aquí se añadirán los métodos de la clase -->
            </div>
        </div>
        """

    def add_methods(self, methods):
        """Reemplaza el marcador de métodos con una lista de métodos en HTML."""
        methods_html = "".join(
            f"<div><h3>{method}</h3></div>" for method in methods
        )
        self.template = self.template.replace(
            "<!-- Aquí se añadirán los métodos de la clase -->", methods_html)


class MethodDiv:
    def __init__(self, name, description):
        self.template = f"""
        <div class="method">
            <h3>{name}</h3>
            <p>{description}</p>
            <div class="parameters">
                <h4>Parámetros</h4>
                <!-- Aquí se añadirán los parámetros del método -->
            </div>
            <div class="return">
                <h4>Retorno</h4>
                <!-- Aquí se describirá el valor de retorno del método -->
            </div>
        </div>
        """

    def add_parameters(self, parameters):
        """Reemplaza el marcador de parámetros con una lista de parámetros en HTML."""
        parameters_html = "".join(
            f"<li>{param}</li>" for param in parameters
        )
        self.template = self.template.replace(
            "<!-- Aquí se añadirán los parámetros del método -->",
            f"<ul>{parameters_html}</ul>"
        )

    def add_return(self, return_description):
        """Reemplaza el marcador de retorno con una descripción del valor de retorno."""
        self.template = self.template.replace(
            "<!-- Aquí se describirá el valor de retorno del método -->",
            f"<p>{return_description}</p>"
        )


# if __name__ == "__main__":
#     SurrealPythonDocs()