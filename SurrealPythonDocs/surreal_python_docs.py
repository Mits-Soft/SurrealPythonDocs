from MrWalk import MrWalk
from pathlib import Path

class SurrealPythonDocs:
    def __init__(self, root_path="."):
        """
        Inicializa la clase con el directorio base a explorar.
        Si no se proporciona root_path, se usa el directorio actual.
        """
        self.set_root_path(root_path)
        print(f"Surreal initialized with root_path: {self.root_path}")

    def set_root_path(self, root_path):
        """
        Cambia el root_path y reinicia el objeto MrWalk.
        """
        self.root_path = Path(root_path).resolve()
        self.charles = MrWalk(str(self.root_path))
        print(f"Root path set to: {self.root_path}")

    def walk(self, include_extensions=None, exclude_dirs=None):
        """
        Realiza un recorrido por los archivos y directorios.
        """
        include_extensions = include_extensions or [".py"]
        exclude_dirs = exclude_dirs or [".git", ".vscode"]
        self.tree = self.charles.walk(include_extensions, exclude_dirs)
        print(f"Tree structure: {self.tree}")
        return self.tree

    def prune(self, exclude_dirs):
        """
        Elimina directorios específicos del recorrido.
        """
        self.tree = self.charles.prune(exclude_dirs)
        print(f"Pruned tree structure: {self.tree}")
        return self.tree

    def tree(self):
        """
        Devuelve la representación en árbol del directorio.
        """
        tree_output = self.charles.tree()
        print(tree_output)
        return tree_output
    
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
