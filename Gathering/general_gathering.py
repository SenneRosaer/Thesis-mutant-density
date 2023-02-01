from mutpy.commandline import build_parser, run_mutpy
from python_gathering import gather_python_information
from c_gathering import gather_c_information
from dextool_html_parser import parse_mutants_from_file
import os

# needs to use bear to create compilation database
def parse_c_dataset(directory_name):
    pass

# use radon for gathering cc and sloc?
def parse_python_dataset(directory_name):
    parser = build_parser()
    run_mutpy(parser, ['./python_example'], ['./python_example/test/simple_good_test.py'], './output/temp_results.csv')
    # gather_python_information('./python_example')


def parse_java_dataset(directory_name):
    pass

def parse_cpp_dataset(directory_name):
    # gather_c_information(directory_name, "./output/t.csv")
    cmd = f"cd {directory_name}"
    # with open("temp_script.sh", "w+") as f:
    #     f.write(cmd + "\n")
        # f.write("mkdir build" + "\n")
        # f.write("cd build" + "\n")
        # f.write("cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -Dgtest_build_tests=ON -Dgmock_build_tests=ON .." + "\n")
        # f.write("make" + "\n")
        # f.write("cd .." + "\n")
        # f.write("mv build/compile_commands.json compile_commands.json")
        # f.write("dub run dextool -- mutate admin --init" + "\n")
        # f.write("dub run dextool -- mutate analyze" + "\n")
        # f.write("dub run dextool -- mutate report --style html" + "\n")

    # os.system("chmod +x temp_script.sh")
    # os.system("./temp_script.sh")
    files = os.listdir(f"{directory_name}/html/files")
    results = {}
    total1 = 0

    for file in files:
        tmp = parse_mutants_from_file(f"{directory_name}/html/files/{file}")
        for val in tmp.values():
            total1 += val

        results.update(tmp)

    total = 0
    for val in results.values():
        total += val
    print(total1)
    print(total)



if __name__ == '__main__':
    # parse_python_dataset("")
    parse_cpp_dataset("Dataset/Cpp/large/opencv-4.x")
    # parse_cpp_dataset("RoadFighter")