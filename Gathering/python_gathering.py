import os
from fileParser import findPythonFiles

#TODO add filename to method name for duplicates
def gather_python_information(directory):
    files = findPythonFiles(directory)
    if os.path.exists("output/py-info-temp.txt"):
        os.remove("output/py-info-temp.txt")
    output = []
    for file in files:
        cmd = f"python -m mccabe {file} >> output/py-info-temp.txt"
        os.system(cmd)
        functions = splitFileInFunctions(file)
        with open("output/py-info-temp.txt", "r") as f:
            lines = f.readlines()
            if "If " in lines[-1]:
                lines.pop()
            for line in lines:
                splittedline = line.replace('\n', '').replace(' ', '').split('\'')
                output.append(f"{splittedline[1]};{splittedline[-1]};0;{len(functions[splittedline[1]])}")

        if os.path.exists("output/py-info-temp.txt"):
            os.remove("output/py-info-temp.txt")

    with open("output/python-results.csv", "w") as o_file:
        o_file.write("Method Name;Cyclomatic Complexity;Mutant Density;Source Lines of Code\n")
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