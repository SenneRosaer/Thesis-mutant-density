import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
# from sklearn.metrics import r2_score
import numpy as np

def rel_freq(data):
    freqs = [(value, data.count(value) / len(data)) for value in set(data)]
    x = []
    y = []
    for item in freqs:
        x.append(item[0])
        y.append(item[1])
    return x,y


def calculate_pearson(sloc, other_data, min_sloc=1):
    input1 = []
    input2 = []
    for index, item in enumerate(sloc):
        if item >= min_sloc:
            input1.append(sloc[index])
            input2.append(other_data[index])
    print(f"coverage={len(input1)/len(sloc)}")
    print(f"methods={len(input1)}")
    return pearsonr(input1, input2)

#TODO all of this data uses logical sloc and not normal sloc
if __name__ == '__main__':
    java_dfs = []
    for file in os.listdir('dataset_results/java'):
        java_dfs.append(pd.read_csv(f"dataset_results/java/{file}", delimiter=";"))
    df_java = pd.concat(java_dfs, ignore_index=True)

    cpp_dfs = []
    for file in os.listdir('dataset_results/cpp'):
        cpp_dfs.append(pd.read_csv(f"dataset_results/cpp/{file}", delimiter=","))
    df_cpp = pd.concat(cpp_dfs, ignore_index=True)

    c_dfs = []
    for file in os.listdir('dataset_results/c'):
        c_dfs.append(pd.read_csv(f"dataset_results/c/{file}", delimiter=","))
    df_c = pd.concat(c_dfs, ignore_index=True)

    python_dfs = []
    for file in os.listdir('dataset_results/python'):
        python_dfs.append(pd.read_csv(f"dataset_results/python/{file}", delimiter=","))
    df_python = pd.concat(python_dfs, ignore_index=True)

    # df = df[np.isfinite(df['Source Lines of Code'])]
    # df = df[np.isfinite(df['Cyclomatic Complexity'])]
    # df = df[np.isfinite(df['Mutant Density'])]
    #
    # df = df.drop(df[df['Source Lines of Code'] == 0].index)
    # df = df.drop(df[df['Cyclomatic Complexity'] == 0].index)
    # df = df.drop(df[df['Mutant Density'] == 0].index)

    sns.set_theme()
    slocs_per_method = []
    ccs_per_method = []
    mds_per_method = []
    min_sloc = 1000
    max_sloc = 0
    boxplot_cc_sloc = [[] for i in range(0,100)]
    boxplot_md_sloc = [[] for i in range(0, 100)]
    for idx, row in df_python.iterrows():
        sloc_for_method = row['Source Lines of Code']
        cc_for_method = row['Cyclomatic Complexity']
        md_for_method = row["Mutant Density"]
        if sloc_for_method < min_sloc:
            min_sloc = sloc_for_method
        if sloc_for_method > max_sloc:
            max_sloc = sloc_for_method
        slocs_per_method.append(sloc_for_method)
        ccs_per_method.append(cc_for_method)
        mds_per_method.append(md_for_method)
        if sloc_for_method <=100:
            boxplot_cc_sloc[sloc_for_method-1].append(cc_for_method)
            boxplot_md_sloc[sloc_for_method-1].append(md_for_method)

    # plt.xscale('log')
    # plt.yscale('log')
    # sns.histplot(df, x='Source Lines of Code',kde=False, binwidth=0.1).set(title="Java SLOC frequency")
    # plt.show()
    # plt.xscale('log')
    # plt.yscale('log')
    # sns.histplot(df, x='Cyclomatic Complexity', kde=False, binwidth=0.1).set(title="Java CC frequency")
    # plt.show()
    # plt.xscale('log')
    # plt.yscale('log')
    # sns.histplot(df, x='Mutant Density', kde=False, binwidth=0.1).set(title="Java Mutant Density frequency")
    # plt.show()
    #
    # ####### log log scatterplot #########
    # plt.xscale('log')
    # plt.yscale('log')
    # sns.scatterplot(df, x='Source Lines of Code', y='Cyclomatic Complexity').set(title="Log-log Scatterplot")
    # plt.show()
    #
    # plt.xscale('log')
    # plt.yscale('log')
    # sns.scatterplot(df, x='Source Lines of Code', y='Mutant Density').set(title="Log-log Scatterplot sloc md")
    # plt.show()
    #
    # plt.xscale('log')
    # plt.yscale('log')
    # sns.scatterplot(df, x='Cyclomatic Complexity', y='Mutant Density').set(title="Log-log Scatterplot cc md")
    # plt.show()
    #
    # ####### normal scatter plot #########
    # plt.ylim(0,500)
    # plt.xlim(0,1750)
    # sns.lmplot(df, x='Source Lines of Code', y='Cyclomatic Complexity').set(title="Scatterplot")
    # plt.show()
    #
    # plt.ylim(0,800)
    # plt.xlim(0,1750)
    # sns.lmplot(df, x='Source Lines of Code', y='Mutant Density').set(title="Scatterplot MD SLOC")
    # plt.show()
    #
    # plt.xlim(0,500)
    # plt.ylim(0,800)
    # sns.lmplot(df, x='Cyclomatic Complexity', y='Mutant Density').set(title="Scatterplot MD CC")
    # plt.show()
    #
    # ####### box plot #########
    # fig = plt.figure()
    # fig.set_figwidth(12)
    # fig.set_figheight(4)
    # plt.xlim(0,100)
    # plt.ylim(0,140)
    #
    # g = sns.boxplot(boxplot_cc_sloc)
    # # test = np.random.normal(100,20,200)
    # # ax = fig.add_axes([0, 0, 1, 1])
    # # bp = ax.boxplot(boxplot_cc_sloc)
    # g.set(title="Boxplot")
    # g.set_xticks(range(0,100,10))
    # # g.set_yticks(range(0,140,20))
    # plt.show()
    #
    # fig = plt.figure()
    # fig.set_figwidth(12)
    # fig.set_figheight(4)
    # plt.xlim(0, 100)
    # plt.ylim(0, 140)
    # g = sns.boxplot(boxplot_md_sloc)
    # g.set(title="Boxplot md on sloc")
    # g.set_xticks(range(0, 100, 10))
    # plt.show()

    #TODO log scale
    ####### Relative frequency #########
    # plt.xscale('log')
    # fig = plt.figure()
    # fig.set_figwidth(10)
    # fig.set_figheight(4)
    # cc_freq_x, cc_freq_y = rel_freq(ccs_per_method)
    # sloc_freq_x, sloc_freq_y = rel_freq(slocs_per_method)
    # md_freq_x, md_freq_y = rel_freq(mds_per_method)
    # plt.plot(cc_freq_x[1:], cc_freq_y[1:])
    # plt.title("relative frequency cc java")
    # plt.show()
    #
    # plt.xscale('log')
    # plt.plot(sloc_freq_x, sloc_freq_y)
    # plt.title("relative frequency sloc java")
    # plt.show()
    #
    # plt.xscale('log')
    # plt.plot(md_freq_x, md_freq_y)
    # plt.title("relative frequency md java")
    # plt.show()

    print(f"pearson cc sloc 1 = {calculate_pearson(slocs_per_method,ccs_per_method,1)}")
    print(f"pearson cc sloc 3 = {calculate_pearson(slocs_per_method,ccs_per_method,3)}")
    print(f"pearson cc sloc 5 = {calculate_pearson(slocs_per_method,ccs_per_method,5)}")
    print(f"pearson cc sloc 9 = {calculate_pearson(slocs_per_method,ccs_per_method,9)}")
    print("-------------------------------")
    print(f"pearson md sloc 1 = {calculate_pearson(slocs_per_method, mds_per_method, 1)}")
    print(f"pearson md sloc 3 = {calculate_pearson(slocs_per_method, mds_per_method, 3)}")
    print(f"pearson md sloc 5 = {calculate_pearson(slocs_per_method, mds_per_method, 5)}")
    print(f"pearson md sloc 9 = {calculate_pearson(slocs_per_method, mds_per_method, 9)}")
    print(f"----------------------------")

    print(f"pearson cc md= {pearsonr(ccs_per_method,mds_per_method)}")
    # print(f"pearson sloc md= {calculate_pearson(slocs_per_method,mds_per_method, 1)}")

    # print()