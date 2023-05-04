import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def parse_java_dataset(directory_name):
    command = f"python3 -m chaosmeter  -p {directory_name} -t ./output/java.csv"
    os.system(command)


if __name__ == '__main__':
    parse_java_dataset("Dataset/1")
    df = pd.read_csv('output/java.csv/FinalReport.csv', delimiter=';')

    all_cc = []
    all_md = []
    above = 0
    below = 0
    for idx, row in df.iterrows():
        sloc = row['Source Lines of Code']
        cc = row['Cyclomatic Complexity']
        md = row["Mutant Density"]
        all_cc.append(cc)
        all_md.append(md)
        if md <= 10:
            below += 1
        else:
            above += 1

    print(above/(above+below))
    plt.xlim(0,50)
    plt.yscale('log')
    sns.histplot(all_cc, bins=[i for i in range(0,50)])
    plt.show()

    plt.xlim(0, 50)
    plt.yscale('log')
    sns.histplot(all_md, bins=[i for i in range(0, 50)])
    plt.show()