import _ast

from mutpy.commandline import build_parser, run_mutpy
from python_gathering import gather_python_information
from c_gathering import gather_c_information
from dextool_html_parser import parse_mutants_from_file
import os
import ast
from collections import defaultdict
import pandas as pd
# needs to use bear to create compilation database
def parse_c_dataset(directory_name):
    pass

# use radon for gathering cc and sloc?
def parse_python_dataset(directory_name):
    parser = build_parser()
    run_mutpy(parser, [f"{directory_name}"],  './output/temp_results.csv')
    gather_python_information(f"{directory_name}")
    df1 = pd.read_csv('./output/python-results.csv', delimiter=";")
    df2 = pd.read_csv('./output/temp_results.csv', delimiter=";")
    df = df1.merge(df2, left_on=["File", "Method Name"], right_on=["File", "Method Name"], how="left")
    df = df.dropna(how='any')
    df['Mutant Density'] = df['Mutant Density'].astype(int)
    df.to_csv('./output/python.csv', index=False)
    print(df.dtypes)


def parse_java_dataset(directory_name):
    command = f"python3 -m chaosmeter  -p {directory_name} -t ./output/java.csv"
    os.system(command)

def parse_cpp_dataset(directory_name):
    gather_c_information(directory_name, "./output/t.csv")
    cmd = f"cd {directory_name}"
    # TODO if it has a makefile and no cmake we need bear -- make or something to create compilation database
    # with open("temp_script.sh", "w+") as f:
    #     f.write(cmd + "\n")
    #     f.write("mkdir build" + "\n")
    #     f.write("cd build" + "\n")
    #     f.write("cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -Dgtest_build_tests=ON -Dgmock_build_tests=ON .." + "\n")
    #     f.write("make" + "\n")
    #     f.write("cd .." + "\n")
    #     f.write("mv build/compile_commands.json compile_commands.json \n")
    #     f.write("dub run dextool -- mutate admin --init" + "\n")
    #     f.write("dub run dextool -- mutate analyze" + "\n")
    #     f.write("dub run dextool -- mutate report --style html" + "\n")

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
    read_from_db_file(directory_name, results)


import sqlite3
def read_from_db_file(filename,results):
    with open("temp_script.sh", "w+") as f:
        f.write(f"cd {filename}" + "\n")
        f.write("python /home/senne/School/Master_SE/Thesis/metrixplusplus/metrix++.py collect --std.code.lines.code --std.code.complexity.cyclomatic")

    os.system("chmod +x temp_script.sh")
    os.system("./temp_script.sh")
    dbfile = f"{filename}/metrixpp.db"
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute("SELECT name from sqlite_master WHERE type='table';")
    print(f"Table Name : {cur.fetchall()}")

    df_files = pd.read_sql_query('SELECT * FROM __files__', con)
    df_files.rename(columns={'id': 'file_id'}, inplace=True)
    df_regions = pd.read_sql_query('SELECT * FROM __regions__', con)
    df_complexity = pd.read_sql_query("SELECT * FROM 'std.code.complexity'", con)
    df_lines = pd.read_sql_query("SELECT * FROM 'std.code.lines'", con)
    df = df_complexity.merge(df_files, on='file_id')
    df_final = df.merge(df_regions, on=['file_id', 'region_id'])
    df_final = df_final.merge(df_lines, on=['file_id', 'region_id'])
    df_final = df_final[['path','name','code','cyclomatic', 'line_begin']]
    print(df_final.head(100))
    file_output = ['File,Method Name,Cyclomatic Complexity,Source Lines of Code,Mutant Density\n']

    for index, row in df_final.iterrows():
        file = row['path'].replace('./','')
        name = row['name']
        if 'Game.cpp' in row['path']:
            print()

        key = str(row['line_begin']) +'//' + file + '//' + name
        if key in results:
            print(f"key = {key}     mutant = {results[key]}")
            file_output.append(f"{file}, {name}, {row['cyclomatic']}, {row['code']}, {results[key]}\n")

    with open('output/cpp_result.csv', 'w+') as f:
        for line in file_output:
            f.write(line)

if __name__ == '__main__':
    # cmd = f"pmccabe -v comm_buffer.hpp >> output/c-info-temp.txt"
    # os.system(cmd)
    # parse_python_dataset("./Dataset/Python/large/ansible-devel/lib/ansible")
    # parse_python_dataset("./python_example")
    # parse_python_dataset("./Dataset/Python/large/biopython/Bio")
    # parse_cpp_dataset("./Dataset/Cpp/large/opencv-4.x")
    # parse_cpp_dataset("Dataset/C/SoftEtherVPN")


    # results = parse_cpp_dataset("./Dataset/C/medium/libusb-master")
    # read_from_db_file("./Dataset/C/medium/libusb-master", results)

    parse_java_dataset('./Dataset/Analytics')