import os
from fileParser import findPythonFiles
import ast
from collections import defaultdict
#TODO add filename to method name for duplicates
def gather_python_information(directory):
    files = findPythonFiles(directory)
    if os.path.exists("output/py-info-temp.txt"):
        os.remove("output/py-info-temp.txt")
    output = []




    for file in files:
        data = str(open(file, "r").read())
        tree = ast.parse(data)
        v = visitor()
        v.visit(tree)
        print()
        results = {}
        for key, item in v.data.items():
            results[key] = len(item)

        cmd = f"python -m mccabe {file} >> output/py-info-temp.txt"
        os.system(cmd)
        functions = splitFileInFunctions(file)
        with open("output/py-info-temp.txt", "r") as f:
            lines = f.readlines()
            if not lines:
                continue
            if "If " in lines[-1]:
                lines.pop()
            for line in lines:
                splittedline = line.replace('\n', '').replace(' ', '').split('\'')
                fname = file.split('/')[-1].replace(".py", "")
                output.append(f"{fname};{splittedline[1]};{splittedline[-1]};{results[splittedline[1]]}")

        if os.path.exists("output/py-info-temp.txt"):
            os.remove("output/py-info-temp.txt")

    with open("output/python-results.csv", "w") as o_file:
        o_file.write("File;Method Name;Cyclomatic Complexity;Source Lines of Code\n")
        for line in output:
            o_file.write(line + '\n')


def splitFileInFunctions(filename):
    entered_function = False
    entered_function_name = ""
    functions = {}
    code = []
    current_indentations = 0
    with open(filename) as f:
        for line in f.readlines():
            if entered_function:
                # \t
                second_split = line.split('\t')
                intendations_infunc = 0
                for item in second_split:
                    if item == '':
                        intendations_infunc += 1
                    else:
                        break

                if intendations_infunc < current_indentations + 1 and line != '\n':
                    entered_function = False
                    functions[entered_function_name] = code
                    code = []
                    current_indentations = 0
                else:
                    code.append(second_split[-1])

            splitted = line.split("def ")
            #TODO match with regex
            if len(splitted) > 1 and "line.split" not in line:
                current_indentations = 0
                for item in splitted:
                    if item == "    ":
                        current_indentations += 1
                    else:
                        break
                entered_function = True
                entered_function_name = splitted[-1].split('(')[0]
                continue
    return functions



class visitor(ast.NodeVisitor):
    def __init__(self):
        def f():
            return set()
        self.data = defaultdict(f)
        self.current_function = None
        self.current_class = None
        self.line_no = None
    def visit_ClassDef(self, node):
        print()
        self.current_class = node.name
        ast.NodeVisitor.generic_visit(self, node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.line_no = node.lineno
        self.generic_visit(node)
        self.current_function = None
        self.line_no = None


    def generic_visit(self, node):
        if self.current_function != None:
                try:
                    if node.lineno != self.line_no:
                        if self.current_class:
                            self.data[self.current_class + "." +self.current_function].add(node.lineno)
                        else:
                            self.data[self.current_function].add(node.lineno)

                except:
                    pass
        ast.NodeVisitor.generic_visit(self, node)
