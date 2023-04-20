import os

import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
# from sklearn.metrics import r2_score
import numpy as np
matplotlib.use('TkAgg')

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

def calculate_outliers_from_boxplot(boxplot_information):
    for index, list in enumerate(boxplot_information):
        if list is not []:
            q1 = np.percentile(list, 25)
            q3 = np.percentile(list, 75)
            iqr = q3-q1
            upper_lim = q3+1.5*iqr
            lower_lim = q1+1.5*iqr

            outliers = []
            for item in list:
                if item < lower_lim or item > upper_lim:
                    outliers.append(item)
            print(outliers)
#TODO all of this data uses logical sloc and not normal sloc


def calculate_means_per_project(df_list):
    for df in df_list:
        slocs_per_method = []
        ccs_per_method = []
        mds_per_method = []
        min_sloc = 1000
        max_sloc = 0
        boxplot_cc_sloc = [[] for i in range(0, 100)]
        boxplot_md_sloc = [[] for i in range(0, 100)]
        cc_sloc_std = [[] for i in range(0, 100)]
        md_sloc_std = [[] for i in range(0, 100)]
        cc_md_diff = []

        for idx, row in df.iterrows():
            sloc_for_method = row['Source Lines of Code']
            cc_for_method = row['Cyclomatic Complexity']
            md_for_method = row["Mutant Density"]
            cc_md_diff.append(abs(cc_for_method - md_for_method))
            if sloc_for_method < min_sloc:
                min_sloc = sloc_for_method
            if sloc_for_method > max_sloc:
                max_sloc = sloc_for_method
            slocs_per_method.append(sloc_for_method)
            ccs_per_method.append(cc_for_method)
            mds_per_method.append(md_for_method)
            if sloc_for_method <= 100:
                boxplot_cc_sloc[sloc_for_method - 1].append(cc_for_method)
                boxplot_md_sloc[sloc_for_method - 1].append(md_for_method)

        for index, list in enumerate(boxplot_cc_sloc):
            mean = np.mean(list)
            std = np.std(list)
            cc_sloc_std[index] = (mean, std)

        for index, list in enumerate(boxplot_md_sloc):
            mean = np.mean(list)
            std = np.std(list)
            md_sloc_std[index] = (mean, std)


def clean_df(df):
    df = df.astype({'Source Lines of Code': int, 'Cyclomatic Complexity': int, 'Mutant Density': int })
    df = df[np.isfinite(df['Source Lines of Code'])]
    df = df[np.isfinite(df['Cyclomatic Complexity'])]
    df = df[np.isfinite(df['Mutant Density'])]

    df = df.drop(df[df['Source Lines of Code'] == 0].index)
    df = df.drop(df[df['Cyclomatic Complexity'] == 0].index)
    df = df.drop(df[df['Mutant Density'] == 0].index)

    return df
if __name__ == '__main__':
    # java_dfs = []
    java_dfs = [pd.read_csv("dataset_results/java/spring.csv", delimiter=";")]
    # for file in os.listdir('dataset_results/java'):
    #     java_dfs.append(pd.read_csv(f"dataset_results/java/{file}", delimiter=";"))
    df_java = pd.concat(java_dfs, ignore_index=True)
    df_java = df_java[df_java['Mutant Density'] != 0]
    df_java = clean_df(df_java)

    # cpp_dfs = [pd.read_csv("dataset_results/cpp/opencv.csv", delimiter=",")]
    cpp_dfs = []
    for file in os.listdir('dataset_results/cpp'):
        cpp_dfs.append(pd.read_csv(f"dataset_results/cpp/{file}", delimiter=","))
    df_cpp = pd.concat(cpp_dfs, ignore_index=True)
    df_cpp = clean_df(df_cpp)

    c_dfs = [pd.read_csv("dataset_results/c/redis.csv", delimiter=',')]
    # c_dfs = []
    # for file in os.listdir('dataset_results/c'):
    #     c_dfs.append(pd.read_csv(f"dataset_results/c/{file}", delimiter=","))
    df_c = pd.concat(c_dfs, ignore_index=True)
    df_c = clean_df(df_c)

    python_dfs = [pd.read_csv("dataset_results/python/flask.csv", delimiter=",")]
    # python_dfs = []
    # for file in os.listdir('dataset_results/python'):
    #     python_dfs.append(pd.read_csv(f"dataset_results/python/{file}", delimiter=","))
    df_python = pd.concat(python_dfs, ignore_index=True)
    df_python = clean_df(df_python)


    sns.set_theme()
    slocs_per_method = []
    ccs_per_method = []
    mds_per_method = []
    min_sloc = 1000
    max_sloc = 0
    boxplot_cc_sloc = [[] for i in range(0,100)]
    boxplot_md_sloc = [[] for i in range(0, 100)]
    cc_sloc_std = [[] for i in range(0,100)]
    md_sloc_std = [[] for i in range(0,100)]
    cc_md_diff = []
    cc_sloc_diff = []
    md_sloc_diff = []
    for idx, row in df_java.iterrows():
        sloc_for_method = row['Source Lines of Code']
        cc_for_method = row['Cyclomatic Complexity']
        md_for_method = row["Mutant Density"]
        cc_md_diff.append((cc_for_method- md_for_method)/sloc_for_method)
        cc_sloc_diff.append(abs(cc_for_method/sloc_for_method))
        md_sloc_diff.append(abs(md_for_method/sloc_for_method))

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

    for index, list in enumerate(boxplot_cc_sloc):
        mean = np.mean(list)
        std = np.std(list)
        cc_sloc_std[index] = (mean, std)

    for index, list in enumerate(boxplot_md_sloc):
        mean = np.mean(list)
        std = np.std(list)
        md_sloc_std[index] = (mean, std)

    ########## Outliers of cc in comparison to sloc
    mean_diff = np.mean(cc_sloc_diff)
    std_diff = np.std(cc_sloc_diff)
    all_diffs = []
    cc_outliers = set()
    print(f"cc sloc mean= {mean_diff} & std = {std_diff}")
    with open("better_output/cc_sloc_outliers.csv", "w+") as f:
        f.write(f"File;Method Name;Average; Distance From Mean\n")
        for idx, row in df_java.iterrows():
            sloc = row['Source Lines of Code']
            cc = row["Cyclomatic Complexity"]
            if sloc > 99:
                continue
            mean, std = cc_sloc_std[sloc]
            # all_diffs.append(sloc-cc)
            all_diffs.append(cc/sloc)
            if std == 0:
                continue
            if (cc/sloc) < (mean_diff-std_diff*2) or (cc/sloc) > (mean_diff + std_diff*2):
                f.write(f"{row['File']};{row['Method Name']};{cc/sloc};{abs((cc/sloc) - mean_diff) * (sloc+cc)/100}\n")
                cc_outliers.add(f"{row['File']};{row['Method Name']};{sloc}")

    # sns.displot(all_diffs, kde=True).set(title='java distribution plot of differences CC & SLOC')
    # plt.xlim(-50, 50)
    # plt.show()
    ########## Outliers of md in comparison to sloc
    mean_diff = np.mean(md_sloc_diff)
    std_diff = np.std(md_sloc_diff)
    all_diffs = []
    print(f"md sloc mean= {mean_diff} & std = {std_diff}")
    md_outliers = set()
    with open("better_output/md_sloc_outliers.csv", "w+") as f:
        f.write(f"File;Method Name;Average; Distance From Mean\n")
        for idx, row in df_java.iterrows():
            sloc = row['Source Lines of Code']
            md = row["Mutant Density"]
            if sloc > 99:
                continue
            # all_diffs.append(sloc-md)
            all_diffs.append(md/sloc)
            mean, std = md_sloc_std[sloc]
            if std == 0:
                continue
            if (md/sloc) < (mean_diff-std_diff*4) or (md/sloc) > (mean_diff + std_diff*4):
                f.write(f"{row['File']};{row['Method Name']};{md/sloc};{abs((md/sloc) - mean_diff)}\n")
                md_outliers.add(f"{row['File']};{row['Method Name']};{sloc}")
    # sns.displot(all_diffs, kde=True).set(title='java distribution plot of differences SLOC & MD')
    # plt.xlim(-50, 50)
    # plt.show()
    t = md_outliers.difference(cc_outliers)
    print(md_outliers.difference(cc_outliers))
    ########## Outliers of difference between md and cc
    mean_diff = np.mean(cc_md_diff)
    std_diff = np.std(cc_md_diff)
    all_diffs = []
    print(f"better_output/md_cc_outliers.csv mean diff = {mean_diff} & mean std {std_diff}")
    with open("better_output/md_cc_outliers.csv", "w+") as f:
        f.write(f"File;Method Name;Average; Distance\n")
        for idx, row in df_java.iterrows():
            cc = row["Cyclomatic Complexity"]
            md = row["Mutant Density"]
            sloc = row['Source Lines of Code']
            diff = cc -md
            # all_diffs.append(cc - md)
            all_diffs.append(diff/sloc)
            if diff/sloc > mean_diff + std_diff*2 or diff/sloc < mean_diff - std_diff*2:
                f.write(f"{row['File']};{row['Method Name']};{diff/sloc};{abs(diff/sloc - mean_diff) * (sloc+cc+md)/100} \n")
    # sns.displot(all_diffs, kde=True).set(title='java distribution plot of differences CC & MD')
    # plt.xlim(-50,50)
    # plt.show()

    # plt.xscale('log')
    # plt.yscale('log')
    # plt.xlim(0,50)
    # sns.histplot(df_java, x='Source Lines of Code',kde=False,bins=25).set(title="Java SLOC frequency")
    # sns.histplot(df_java, x='Source Lines of Code', stat='percent', binwidth=1).set(title="Java dataset SLOC frequency")
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
    # calculate_outliers_from_boxplot(boxplot_cc_sloc)

    # print(f"pearson cc sloc 1 = {calculate_pearson(slocs_per_method,ccs_per_method,1)}")
    # print(f"pearson cc sloc 3 = {calculate_pearson(slocs_per_method,ccs_per_method,3)}")
    # print(f"pearson cc sloc 5 = {calculate_pearson(slocs_per_method,ccs_per_method,5)}")
    # print(f"pearson cc sloc 9 = {calculate_pearson(slocs_per_method,ccs_per_method,9)}")
    # print("-------------------------------")
    # print(f"pearson md sloc 1 = {calculate_pearson(slocs_per_method, mds_per_method, 1)}")
    # print(f"pearson md sloc 3 = {calculate_pearson(slocs_per_method, mds_per_method, 3)}")
    # print(f"pearson md sloc 5 = {calculate_pearson(slocs_per_method, mds_per_method, 5)}")
    # print(f"pearson md sloc 9 = {calculate_pearson(slocs_per_method, mds_per_method, 9)}")
    # print(f"----------------------------")

    # print(f"pearson cc md= {pearsonr(ccs_per_method,mds_per_method)}")
    # print(f"pearson sloc md= {calculate_pearson(slocs_per_method,mds_per_method, 1)}")

    # print()