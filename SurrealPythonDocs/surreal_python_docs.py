import os
from MrWalk import MrWalk
from pathlib import Path
import copy
import shutil

class SurrealPythonDocs:
    """
    SurrealPythonDocs is a class to explore Python project directories,
    extract docstrings from source files, and generate structured documentation
    from the collected information.

    It allows traversing directory trees, filtering files, extracting class and method names,
    and rendering documentation in HTML format. It is designed to facilitate automatic documentation
    of Python projects, providing utilities to analyze code structure and its documentation comments.
    """
    def __init__(self, root_path="."):
        """
        Initializes the class with the base directory to explore.
        If root_path is not provided, the current directory is used.
        """
        self.set_root_path(root_path)
        self.tree = None
        self.generated_docstrings = {}
        self.clsss_and_mthds = {
            "classes": [],
            "methods": []
        }
        self.final_documents_text = ""
        print(
            f"SurrealPythonDocs: Surreal initialized with root_path: {self.root_path}")

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

    def prune(self, exclude):
        """
        Elimina directorios específicos del recorrido.
        """
        self.tree = self.charles.prune(exclude)
        print(f"SurrealPythonDocs: Pruned tree structure: {self.tree}")
        return self.tree

    def show_tree(self):
        """
        Devuelve la representación en árbol del directorio.
        """
        tree_output = self.charles.tree()
        print(tree_output)
        return tree_output
    
    def extract_node_name_from_line(self, line):
        if "(" in line:
            title = line.split("(")[0].strip()
        else: 
            title = line.split(":")[0].strip()
        return title

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
                new_path = f"{current_path}/{key}".lstrip(
                    "/") if current_path else key
                if isinstance(value, dict):
                    traverse_tree(value, new_path)
                elif key.endswith(".py"):
                    file_path = new_path
                    with open(file_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        visited_objects = set()  # Para evitar duplicados
                        for i, line in enumerate(lines):
                            if line.startswith("class"):
                                stripped_line = line.strip()
                                clss_nm = self.extract_node_name_from_line(stripped_line)
                                clss_obj = {
                                    "class_name": clss_nm,
                                    "line_number": i + 1,
                                    "file_path": file_path
                                }
                                self.clsss_and_mthds["classes"].append(clss_obj)
                            elif line.strip().startswith("def"):
                                stripped_line = line.strip()
                                mthd_nm = self.extract_node_name_from_line(stripped_line)
                                mthd_obj = {
                                    "class_name": mthd_nm,
                                    "line_number": i + 1,
                                    "file_path": file_path
                                }
                                self.clsss_and_mthds["methods"].append(mthd_obj)
                            if '"""' in line or "'''" in line:
                                # Buscar la línea anterior con class o def
                                title = "Module-level docstring"
                                # Línea del docstring (1-based index)
                                line_number = i + 1
                                for j in range(i - 1, -1, -1):
                                    stripped_line = lines[j].strip()
                                    if stripped_line.startswith(("class ", "def ")):
                                        title = self.extract_node_name_from_line(stripped_line)                                      
                                        # Línea del objeto (1-based index)
                                        line_number = j + 1
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
                                description = "\n".join(docstring_lines).strip(
                                    '"""').strip("'''").strip()
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

    def render_document(self, data: dict = [], title: str = "Title", year: str = "2025", company: str = "Mits-Soft", license: str = "MIT Licenes"):
        """
        Renders an html document.

        Args:
            data (obj): the pertinent data retrieved from the directories walk 
            title: title of the html page
            year: creation year
            company: company the document belongs to
            license: asociated license to the content

        Returns:
            rendered_page (str): the html markup generated from the data
        """
        modules = []
        document = {
            "module_name": "",
            "document_path": "",
            "classes": [
                {
                    "class_zero": {
                        "name": "zero",
                        "line_number": 0,
                        "markup_index": 0,
                        "markup": "",
                        "methods": [
                            {
                                "method_zero": {
                                    "name": "method_zero",
                                    "line_number": 0,
                                    "markup_index": 0
                                }
                            }
                        ]
                    }
                }
            ],
            "markup": []
        }
        for d in data.items():
            elements = []
            doc = copy.deepcopy(document)
            dcmnt_pth = d[0]
            doc["document_path"] = dcmnt_pth
            pth_prts = Path(dcmnt_pth).parts
            doc["module_name"] = pth_prts[len(pth_prts)-1].split(".")[0]
            dcstrngs = d[1]
            current_class_name = ""
            for indx, dcstrng in enumerate(dcstrngs):
                dcstrng_ttl = dcstrng["title"]
                dcstrng_type = dcstrng["title"].split(" ")[0]
                dcstrng_description = dcstrng["description"]
                dcstrng_line_number = dcstrng["line_number"]
                dcstrng_markup_index = indx
                if dcstrng_type == "class":
                    if not current_class_name == dcstrng_ttl:
                        current_class_name = dcstrng_ttl
                    class_doc_template = copy.deepcopy(doc["classes"][0])
                    elem = ClassDiv(dcstrng_ttl, dcstrng_description)
                    cz_cdt = class_doc_template["class_zero"]
                    elem.title = dcstrng_ttl
                    cz_cdt["name"] = dcstrng_ttl
                    elem.type = dcstrng_type
                    elem.line_number = dcstrng_line_number
                    cz_cdt["line_number"] = dcstrng_line_number
                    cz_cdt["markup_index"] = dcstrng_markup_index
                    nmd_cz_cdt = {dcstrng_ttl: cz_cdt}
                    doc["classes"].append(nmd_cz_cdt)
                    elements.append(elem)
                elif dcstrng_type == "def":
                    if not current_class_name:
                        current_class_name, line_numb = self.return_upper_nearest_class(dcmnt_pth, dcstrng_line_number)
                        class_doc_template = copy.deepcopy(doc["classes"][0])
                        cz_cdt = class_doc_template["class_zero"]
                        cz_cdt["name"] = current_class_name
                        cz_cdt["line_number"] = line_numb
                        cz_cdt["markup_index"] = -1
                        nmd_cz_cdt = {current_class_name: cz_cdt}
                        doc["classes"].append(nmd_cz_cdt)            
                    method_doc_template = copy.deepcopy(doc["classes"][0]["class_zero"]["methods"][0])
                    elem = MethodDiv(dcstrng_ttl, dcstrng_description)
                    mz_mdt = method_doc_template["method_zero"]
                    elem.title = dcstrng_ttl
                    mz_mdt["name"] = dcstrng_ttl
                    elem.type = dcstrng_type
                    elem.line_number = dcstrng_line_number
                    mz_mdt["line_number"] = dcstrng_line_number
                    mz_mdt["markup_index"] = dcstrng_markup_index
                    current_class = self.get_class_by_name(doc, current_class_name)
                    nmd_mz_mdt = {dcstrng_ttl: mz_mdt}
                    current_class["methods"].append(nmd_mz_mdt)
                    elements.append(elem)
            doc["markup"] = elements
            modules.append(doc)
        rendered_documents = []
        for module in modules:
            for cl_indx in range(1, len(module["classes"])):
                cl = module["classes"][cl_indx]
                cl_val = list(cl.values())[0]
                cl_mrkp = module["markup"][cl_val["markup_index"]]
                cl_mthds = []
                for mthd_indx in range(1, len(cl_val["methods"])):
                    mthd = cl_val["methods"][mthd_indx]
                    mthd_val = list(mthd.values())[0]
                    mthd_mrkup = module["markup"][mthd_val["markup_index"]]
                    cl_mthds.append(mthd_mrkup.template)
                cl_mrkp.add_methods(cl_mthds)
                cl_mrkp.dcmnt_path = module["document_path"]
                cl[list(cl.keys())[0]]["markup"] = cl_mrkp
                rendered_documents.append(cl)
        final_documents = []
        for module in modules:
            module["markup"] = [elem for elem in module["markup"]]
            html_doc = HtmlDocument(title, year, company, license)
            class_html = ""
            for cl_indx in range(1, len(module["classes"])):
                cl = module["classes"][cl_indx]
                cl_val = list(cl.values())[0]
                cl_mrkp = cl_val["markup"]
                class_html += cl_mrkp.template.replace('\n', '')
            html_doc.add_content(class_html)
            final_documents.append({module["document_path"]: html_doc.template.replace('\n', '').strip()})
            self.final_documents_text = final_documents
            self.save_documentation_to_files()            
        return final_documents
    
    def save_documentation_to_files(self):
        pth = Path(".") / "docs"
        os.makedirs(pth, exist_ok=True)
        src_css_dir = Path(".") / "resources" / "css"
        dst_css_dir = pth / "css"
        if src_css_dir.exists() and src_css_dir.is_dir():
            if dst_css_dir.exists():
                shutil.rmtree(dst_css_dir)
            shutil.copytree(src_css_dir, dst_css_dir)
        files_names = []
        files_contents = []
        for file_text in self.final_documents_text:
            files_contents.append(list(file_text.values())[0])
        for file_path in self.final_documents_text:
            module_name = Path(list(file_path.keys())[0]).stem  # solo el nombre del archivo sin extensión
            html_file_name = f"{module_name}.html"
            files_names.append(html_file_name)
        for idx, file_name in enumerate(files_names):
            file_path = pth / file_name
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(files_contents[idx])
            
    def get_class_by_name(self, document, class_name):
        for class_dict in document["classes"]:
            # Cada elemento es un diccionario con un solo par clave:valor
            for key, value in class_dict.items():
                if key == class_name:
                    return value  # Devuelve el diccionario de la clase encontrada
        return None  # Si no se encuentra la clase
    
    def return_upper_nearest_class(self, fpath, dcstrng_line_number):
        stored_classes = self.clsss_and_mthds["classes"]
        for index, cls in enumerate(stored_classes):
            if cls["file_path"] == fpath:
                if cls["line_number"] > dcstrng_line_number:
                    return (stored_classes[index - 1]["class_name"], stored_classes[index - 1]["line_number"])


class HtmlDocument:
    """
    Class representing the html document the docstrings are rendered to
    """
    def __init__(self, title, year, company, license):
        self.template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="css/light_styles.css">
            <title>{title}</title>
        </head>
        <body>
            <div class="main-container">
            <!-- Content goes here -->
            </div>
        </body>
        <footer>
            <p>&copy; {year} {company}. All rights reserved. Licensed under {license}.</p>
        </footer>
        </html>
        """

    def add_content(self, content):
        """Reemplaza el marcador de contenido en el template."""
        self.template = self.template.replace(
            "<!-- Content goes here -->", content.replace('\n', ''))


class ClassDiv:
    """
    Class representing the classes docstrings 
    """
    def __init__(self, name, description):
        self.title = ""
        self.type = ""
        self.line_number = 0
        self.dcmnt_path = ""
        self.clss_dscrptn_objct = self.extract_class_description_parts(description)
        # Construir la descripción de la clase usando las partes extraídas
        short_desc = self.clss_dscrptn_objct.get("short_description", "")
        long_desc = self.clss_dscrptn_objct.get("long_description", "")
        attributes = self.clss_dscrptn_objct.get("attributes", [])
        methods = self.clss_dscrptn_objct.get("methods", [])
        other_sections = self.clss_dscrptn_objct.get("other_sections", {})

        attributes_html = ""
        if attributes:
            attributes_html = "<div class='class-attributes'><h3>Attributes</h3><ul>"
            for attr in attributes:
                attributes_html += f"<li>{attr}</li>"
            attributes_html += "</ul></div>"# <br>

        # Métodos en la descripción de la clase (sin línea en blanco entre título y descripción)
        methods_html = ""
        if methods:
            methods_html = "<div class='class-methods'><h3>Methods</h3><ul style='list-style-type:none;'>"
            for mthd in methods:
                # Si hay ":", tabula la descripción corta
                if ":" in mthd:
                    mthd_name, mthd_desc = mthd.split(":", 1)
                    methods_html += (
                        f"<li><b>{mthd_name.strip()}</b>:"
                        f"<span style='margin-left: 1.5em'>{mthd_desc.strip()}</span></li>"
                    )
                else:
                    methods_html += f"<li>{mthd}</li>"
            methods_html += "</ul><br></div>"

        other_sections_html = ""
        for sec, content in other_sections.items():
            if content:
                sec_title = sec.replace("_", " ").title()
                lines = [ln for ln in content.splitlines() if ln.strip() != ""]
                section_html = ""
                for ln in lines:
                    section_html += f"{ln}<br>"
                other_sections_html += f"<div class='class-section'><h3>{sec_title}</h3><p>{section_html}</p></div>"

        self.template = f"""
        <div class="class-external">
            <h1>{name}</h1>
            <p class="class-short-description">{short_desc}</p>
            {'<p class="class-long-description">' + long_desc + '</p>' if long_desc else ''}
            {attributes_html}
            {methods_html}
            {other_sections_html}
            <div class="methods">
            <h2>Methods</h2>
            <!-- Methods for this class will be added here -->
            </div>
        </div>
        """
    
    def extract_class_description_parts(self, class_description: str):
        """
        Extracts the parts of a class docstring: short description, long description, attributes, methods, and other sections.

        Args:
            class_description (str): The class docstring.

        Returns:
            dict: A dictionary with the parts: 'short_description', 'long_description', 'attributes', 'methods', 'other_sections'
        """
        parts = {
            "short_description": "",
            "long_description": "",
            "attributes": [],
            "methods": [],
            "other_sections": {}
        }

        lines = [ln.strip() for ln in class_description.splitlines() if ln.strip()]
        if not lines:
            return parts

        # Short description: first non-empty line
        parts["short_description"] = lines[0]

        # Find section indices (Attributes, Methods, Internal Methods, Examples, etc.)
        section_indices = {}
        for idx, ln in enumerate(lines):
            lower_ln = ln.lower()
            if lower_ln.startswith("attributes"):
                section_indices["attributes"] = idx
            elif lower_ln.startswith("methods"):
                section_indices["methods"] = idx
            elif lower_ln.startswith("internal methods"):
                section_indices["internal_methods"] = idx
            elif lower_ln.startswith("examples"):
                section_indices["examples"] = idx
            elif lower_ln.startswith("note"):
                section_indices["note"] = idx
            elif lower_ln.startswith("see also"):
                section_indices["see_also"] = idx

        # Attributes
        if "attributes" in section_indices:
            attr_start = section_indices["attributes"] + 1
            next_sections = [i for k, i in section_indices.items() if i > section_indices["attributes"]]
            attr_end = min(next_sections) if next_sections else len(lines)
            attrs = []
            for ln in lines[attr_start:attr_end]:
                if ln:
                    attrs.append(ln)
            parts["attributes"] = attrs

        # Methods (conservar líneas y saltos)
        if "methods" in section_indices:
            mthd_start = section_indices["methods"] + 1
            next_sections = [i for k, i in section_indices.items() if i > section_indices["methods"]]
            mthd_end = min(next_sections) if next_sections else len(lines)
            mthds = []
            for ln in lines[mthd_start:mthd_end]:
                if ln:
                    mthds.append(ln)
            parts["methods"] = mthds

        # Other sections (including Internal Methods, Examples, etc.)
        for sec, idx in section_indices.items():
            if sec in ("attributes", "methods"):
                continue
            next_sections = [i for k, i in section_indices.items() if i > idx]
            sec_end = min(next_sections) if next_sections else len(lines)
            parts["other_sections"][sec] = "\n".join(lines[idx+1:sec_end]).strip()

        return parts
        
    def add_methods(self, methods):
        """Replace the methods placeholder with a list of methods in HTML."""
        methods_html = "".join(
            f"{method}" for method in methods
        )
        self.template = self.template.replace(
            "<!-- Methods for this class will be added here -->", methods_html
        )


class MethodDiv:
    """
    Class representing the methods docstrings 
    """
    def __init__(self, name, description):
        self.title = ""
        self.type = ""
        self.line_number = 0
        clnd_mthd = self.extract_method_parts(description)
        clean_desc = " ".join(clnd_mthd["clean_description"])
        self.template = f"""
        <div class="method">
            <h3>{name}</h3>
            <p>{clean_desc}</p>
            <div class="parameters">
                <h4>Parameters</h4>
                <!-- Method parameters will be added here -->
            </div>
            <div class="return">
                <h4>Returns</h4>
                <!-- Method return value will be described here -->
            </div>
            <div class="raises">
                <h4>Raises</h4>
                <!-- Method exceptions will be described here -->
            </div>
        </div>
        """
        self.add_parameters(clnd_mthd["args"])
        self.add_return(clnd_mthd["return"])
        self.add_raises(clnd_mthd["raises"])
    def extract_method_parts(self, method_docstr: str):
        mthd_rtrn_prts = {
            "clean_description": "",
            "args": "",
            "return": "",
            "raises": ""
        }
        prts_nchrs = {
            "args": None,
            "return": None,
            "raises": None
        }
        mthd_dcstr_lns = method_docstr.splitlines()
        # Find section anchors
        for idx, ln in enumerate(mthd_dcstr_lns):
            lower_ln = ln.strip().lower()
            if prts_nchrs["args"] is None and (lower_ln.startswith("args") or lower_ln.startswith("arguments") or lower_ln.startswith("parameters")):
                prts_nchrs["args"] = idx
            elif prts_nchrs["return"] is None and (lower_ln.startswith("return") or lower_ln.startswith("returns")):
                prts_nchrs["return"] = idx
            elif prts_nchrs["raises"] is None and (lower_ln.startswith("raises") or lower_ln.startswith("exceptions") or lower_ln.startswith("throws")):
                prts_nchrs["raises"] = idx

        # Determine section indices
        args_idx = prts_nchrs["args"]
        return_idx = prts_nchrs["return"]
        raises_idx = prts_nchrs["raises"]

        # Clean description: everything before the first section (args/return/raises)
        section_indices = [i for i in [args_idx, return_idx, raises_idx] if i is not None]
        if section_indices:
            first_section = min(section_indices)
            cln_dscrptn_strng = [line for line in mthd_dcstr_lns[:first_section] if line.strip()]
        else:
            cln_dscrptn_strng = [line for line in mthd_dcstr_lns if line.strip()]
        mthd_rtrn_prts["clean_description"] = cln_dscrptn_strng

        # Extract arguments
        if args_idx is not None:
            next_sections = [i for i in [return_idx, raises_idx] if i is not None and i > args_idx]
            end_idx = min(next_sections) if next_sections else len(mthd_dcstr_lns)
            mthd_rtrn_prts["args"] = [mthd_dcstr_lns[i].strip() for i in range(args_idx + 1, end_idx) if mthd_dcstr_lns[i].strip()]
        else:
            mthd_rtrn_prts["args"] = []

        # Extract return
        if return_idx is not None:
            next_sections = [i for i in [raises_idx] if i is not None and i > return_idx]
            end_idx = min(next_sections) if next_sections else len(mthd_dcstr_lns)
            mthd_rtrn_prts["return"] = [mthd_dcstr_lns[i].strip() for i in range(return_idx + 1, end_idx) if mthd_dcstr_lns[i].strip()]
        else:
            mthd_rtrn_prts["return"] = []

        # Extract raises
        if raises_idx is not None:
            end_idx = len(mthd_dcstr_lns)
            mthd_rtrn_prts["raises"] = [mthd_dcstr_lns[i].strip() for i in range(raises_idx + 1, end_idx) if mthd_dcstr_lns[i].strip()]
        else:
            mthd_rtrn_prts["raises"] = []

        return mthd_rtrn_prts

    def add_parameters(self, parameters):
        """Replace the parameters placeholder with a list of parameters in HTML."""
        parameters_html = "".join(
            f"<li>{param}</li>" for param in parameters
        )
        self.template = self.template.replace(
            "<!-- Method parameters will be added here -->",
            f"<ul>{parameters_html}</ul>"
        )
        
    def add_return(self, return_description):
        """Replace the return placeholder with a description of the return value."""
        if isinstance(return_description, list):
            return_html = "".join(f"<li>{item}</li>" for item in return_description if item)
            return_html = f"<ul>{return_html}</ul>" if return_html else ""
        else:
            return_html = f"<p>{return_description}</p>"
        self.template = self.template.replace(
            "<!-- Method return value will be described here -->",
            return_html
        )

    def add_raises(self, raises_description):
        """Replace the raises placeholder with a description of the exceptions raised."""
        if isinstance(raises_description, list):
            raises_html = "".join(f"<li>{item}</li>" for item in raises_description if item)
            raises_html = f"<ul>{raises_html}</ul>" if raises_html else ""
        else:
            raises_html = f"<p>{raises_description}</p>"
        self.template = self.template.replace(
            "<!-- Method exceptions will be described here -->",
            raises_html
        )

