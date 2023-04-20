import os
def parse_java_dataset(directory_name):
    command = f"python3 -m chaosmeter  -p {directory_name} -t ./output/java.csv"
    os.system(command)


if __name__ == '__main__':
    parse_java_dataset("Dataset/1")