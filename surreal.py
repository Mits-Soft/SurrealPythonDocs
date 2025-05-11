# mi_script.py
from mrwalk import MrWalk
import sys
from pathlib import Path

ruta_base = Path(__file__).resolve().parent.parent
mrwalk_path = ruta_base / 'MrWalk'

if mrwalk_path not in sys.path:
    sys.path.append(str(mrwalk_path))


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


if __name__ == "__main__":
    Surreal()
