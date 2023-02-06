import os
from fileParser import findCppFiles

def gather_c_information(directory, output_name):
    files = findCppFiles(directory)

    if os.path.exists("output/c-info-temp.txt"):
        os.remove("output/c-info-temp.txt")
    output = []
    for file in files:
        if os.path.exists("output/c-info-temp.txt"):
            os.remove("output/c-info-temp.txt")
        if "comm_buffer" in file:
            print()
        cmd = f"pmccabe -v {file} >> output/c-info-temp.txt"
        os.system(cmd)

        with open("output/c-info-temp.txt", "r") as f:
            lines = f.readlines()
            for line in lines[7:]:
                splittedline = line.replace('\n', '').replace(': ', '\t').split('\t')
                output.append(f"{splittedline[-1]};{splittedline[1]};0;{splittedline[4]}")
        if os.path.exists("output/py-info-temp.txt"):
            os.remove("output/py-info-temp.txt")

    with open(output_name, "w+") as o_file:
        o_file.write("Method Name;Cyclomatic Complexity;Mutant Density;Source Lines of Code\n")
        for line in output:
            o_file.write(line + '\n')


