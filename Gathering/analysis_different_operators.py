import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

if __name__ == '__main__':
    files = os.listdir("differentMDOperatorsResults")
    print(files)
    dfs = {}
    outliers = {}
    for file in files:
        df = pd.read_csv(f"differentMDOperatorsResults/{file}", delimiter=",")
        dfs[file.replace('.csv','')] = df
        all_averages = []
        total_mutants = 0
        total_methods = 0
        for idx, row in df.iterrows():
            sloc = row['Source Lines of Code']
            md = row["Mutant Density"]
            if sloc > 99:
                continue
            # all_diffs.append(sloc-md)
            all_averages.append(md / sloc)
            total_methods += 1
            total_mutants += md

        mean = np.mean(all_averages)
        std = np.std(all_averages)
        current_outliers = []
        for idx, row in df.iterrows():
            sloc = row['Source Lines of Code']
            md = row["Mutant Density"]
            average = md/sloc
            if sloc > (mean+std) or sloc < (mean-std):
                current_outliers.append(f"{row['File']};{row['Method Name']}")
        outliers[file.replace('.csv','')] = current_outliers
        # sns.displot(all_averages, kde=True).set(title='opencv distribution plot of average MD : ' + file.replace('.csv',''))
        # plt.xlim(-50, 50)
        # plt.show()
        print(f"Mutations: {file.replace('.csv','')}, Methods: {total_methods}, Total Mutants: {total_mutants}")

    temp = []
    keys = []
    for key, val in outliers.items():
        temp.append(set(val))
        keys.append(key)

    results = set.intersection(*map(set, temp))
    print("------- Outliers over all sets ---------")
    print(results)
    print("------ Single mutation outliers --------")
    for index, list in enumerate(temp):

        for index2, second_list in enumerate(temp):
            if index != index2:
                list = list.difference(second_list)
        print(f"{keys[index]} : {list}")

