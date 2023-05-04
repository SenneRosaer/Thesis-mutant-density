import math
import os

import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
# from sklearn.metrics import r2_score
import numpy as np

matplotlib.use('TkAgg')
from scipy import stats
import matplotlib.ticker as ticker

def rel_freq(data):
    freqs = [(value, data.count(value) / len(data)) for value in set(data)]
    x = []
    y = []
    for item in freqs:
        x.append(item[0])
        y.append(item[1])
    return x, y


def calculate_pearson(sloc, other_data, min_sloc=1):
    input1 = []
    input2 = []
    for index, item in enumerate(sloc):
        if item >= min_sloc:
            input1.append(sloc[index])
            input2.append(other_data[index])
    print(f"coverage={len(input1) / len(sloc)}")
    print(f"methods={len(input1)}")
    return pearsonr(input1, input2)


def calculate_outliers_from_boxplot(boxplot_information):
    for index, list in enumerate(boxplot_information):
        if list is not []:
            q1 = np.percentile(list, 25)
            q3 = np.percentile(list, 75)
            iqr = q3 - q1
            upper_lim = q3 + 1.5 * iqr
            lower_lim = q1 + 1.5 * iqr

            outliers = []
            for item in list:
                if item < lower_lim or item > upper_lim:
                    outliers.append(item)
            print(outliers)


# TODO all of this data uses logical sloc and not normal sloc


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
    df = df.astype({'Source Lines of Code': int, 'Cyclomatic Complexity': int, 'Mutant Density': int})
    df = df[np.isfinite(df['Source Lines of Code'])]
    df = df[np.isfinite(df['Cyclomatic Complexity'])]
    df = df[np.isfinite(df['Mutant Density'])]

    df = df.drop(df[df['Source Lines of Code'] == 0].index)
    df = df.drop(df[df['Cyclomatic Complexity'] == 0].index)
    df = df.drop(df[df['Mutant Density'] == 0].index)

    return df


def outliers(data, df, title, output, lim=50, symlog=False):
    print(f"-----------{title}---------------")
    mean = np.mean(data)
    std = np.std(data)
    z = stats.zscore(data)
    distribution = {}
    with open(output, "w+") as f:
        f.write(f"File;Method Name;Z-score\n")
        for idx, row in df.iterrows():
            sloc = row['Source Lines of Code']
            if sloc > 99:
                continue
            zscore = z[idx]
            if math.floor(zscore) not in distribution:
                distribution[math.floor(zscore)] = 1
            else:
                distribution[math.floor(zscore)] += 1
            f.write(f"{row['File']};{row['Method Name']};{zscore}\n")
    print(distribution)
    if symlog:
        sns.displot(data, kde=True, bins=8).set(title=title)
        plt.yscale('symlog')
        plt.yticks([0, 1, 10, 100, 1000, 10000], ['0',f'$10^0$', f'$10^1$', f'$10^2$', f'$10^3$', f'$10^4$'])
        ax = plt.gca()
        ax.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 10, 100, 1000, 10000]))
        plt.xlim(-lim, lim)
        plt.show()
    else:
        sns.displot(data, kde=True, bins=80).set(title=title)
        plt.xlim(-lim, lim)
        plt.show()
    print('-------------------------------------')

def freq_dist(df, axis,title):
    plt.yscale('log')
    plt.xlim(0, 100)
    sns.histplot(df, x=axis, binwidth=1).set(title=title)
    plt.show()

def scatterplot_loglog(df, x, y, title):
    ###### log log scatterplot #########
    plt.xscale('log')
    plt.yscale('log')
    sns.scatterplot(df, x=x, y=y).set(title=title)
    plt.show()

def scatterplot(df, x, y, title):
    ###### log log scatterplot #########
    plt.xlim(0,200)
    plt.ylim(0,200)
    sns.regplot(df, x=x, y=y, color='red', scatter_kws={'color': 'blue'}).set(title=title)
    plt.show()

def boxplot(data, title):
    ####### box plot #########
    fig = plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(4)
    plt.xlim(0, 100)
    plt.ylim(0, 140)
    g = sns.boxplot(data)
    g.set(title=title)
    g.set_xticks(range(0, 100, 10))
    plt.show()

def get_outlier_functions(data, df, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    z = stats.zscore(data)
    distribution = {}
    outliers = []
    for idx, row in df.iterrows():
        sloc = row['Source Lines of Code']
        if sloc > 99:
            continue
        zscore = z[idx]
        if math.floor(zscore) not in distribution:
            distribution[math.floor(zscore)] = 1
        else:
            distribution[math.floor(zscore)] += 1
        if abs(zscore) >= threshold:
            outliers.append(f"{row['File']}@{row['Method Name']}")
    print(outliers)

def get_set_theory(outliers1, outliers2):
    outliers1 = set(outliers1)
    outliers2 = set(outliers2)
    print(f"First set: {len(outliers1)} & Second set: {len(outliers2)}")
    print(f"1 -2 : {len(outliers1.difference(outliers2))}")
    print(f"2 -1 : {len(outliers2.difference(outliers1))}")
    print(f"intersection: {len(outliers2.intersection(outliers1))}")
    unique = outliers1.difference(outliers2)
    print(unique)

if __name__ == '__main__':
    java_dfs = []
    # java_dfs = [pd.read_csv("dataset_results/java/fastjson.csv", delimiter=";")]
    for file in os.listdir('dataset_results/java'):
        java_dfs.append(pd.read_csv(f"dataset_results/java/{file}", delimiter=";"))
    df_java = pd.concat(java_dfs, ignore_index=True)
    df_java = df_java[df_java['Mutant Density'] != 0]
    df_java = clean_df(df_java)

    # cpp_dfs = [pd.read_csv("dataset_results/cpp/opencv.csv", delimiter=",")]
    cpp_dfs = []
    for file in os.listdir('dataset_results/cpp'):
        cpp_dfs.append(pd.read_csv(f"dataset_results/cpp/{file}", delimiter=","))
    df_cpp = pd.concat(cpp_dfs, ignore_index=True)
    df_cpp = clean_df(df_cpp)

    # c_dfs = [pd.read_csv("dataset_results/c/redis.csv", delimiter=',')]
    c_dfs = []
    for file in os.listdir('dataset_results/c'):
        c_dfs.append(pd.read_csv(f"dataset_results/c/{file}", delimiter=","))
    df_c = pd.concat(c_dfs, ignore_index=True)
    df_c = clean_df(df_c)

    # python_dfs = [pd.read_csv("dataset_results/python/flask.csv", delimiter=",")]
    python_dfs = []
    for file in os.listdir('dataset_results/python'):
        python_dfs.append(pd.read_csv(f"dataset_results/python/{file}", delimiter=","))
    df_python = pd.concat(python_dfs, ignore_index=True)
    df_python = clean_df(df_python)

    df = df_java
    print(len(df))
    df = df.reset_index(drop=True)
    sns.set_theme()
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
    cc_sloc_diff = []
    md_sloc_diff = []
    cc_md_average = []
    cc_sloc_average = []
    md_sloc_average = []

    cc_md_ratio = []
    cc_sloc_ratio = []
    md_sloc_ratio = []

    metrics = {}
    for idx, row in df.iterrows():
        sloc_for_method = row['Source Lines of Code']
        cc_for_method = row['Cyclomatic Complexity']
        md_for_method = row["Mutant Density"]
        cc_md_average.append((cc_for_method - md_for_method) / sloc_for_method)
        cc_sloc_average.append(abs(cc_for_method / sloc_for_method))
        md_sloc_average.append(abs(md_for_method / sloc_for_method))

        cc_md_diff.append((cc_for_method - md_for_method))
        cc_sloc_diff.append(sloc_for_method - cc_for_method)
        md_sloc_diff.append(sloc_for_method-  md_for_method)

        cc_md_ratio.append(((cc_for_method - md_for_method) / sloc_for_method) * (sloc_for_method)/100)
        cc_sloc_ratio.append(abs(cc_for_method / sloc_for_method) * (sloc_for_method)/100)
        md_sloc_ratio.append(abs(md_for_method / sloc_for_method) * (sloc_for_method)/100)

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


    language = "Java"

    # freq_dist(df, 'Source Lines of Code', f"{language} Source Lines of Code frequency")
    # freq_dist(df, 'Cyclomatic Complexity', f"{language} Cyclomatic Complexity frequency")
    # freq_dist(df, 'Mutant Density', f"{language} Mutant Density frequency")
    #
    # outliers(cc_sloc_diff, df, f"{language} CC and SLOC difference distribution", "better_output/cc_sloc_outliers1.csv")
    # outliers(md_sloc_diff, df, f"{language} MD and SLOC difference distribution", "better_output/cc_sloc_outliers1.csv")
    # outliers(cc_md_diff, df, f"{language} CC and MD difference distribution", "better_output/cc_sloc_outliers1.csv")
    # outliers(cc_sloc_average, df, f"{language} CC and SLOC average distribution", "better_output/cc_sloc_outliers1.csv", lim=3, symlog=True)
    # outliers(md_sloc_average, df, f"{language} MD and SLOC average distribution", "better_output/cc_sloc_outliers1.csv",lim=3, symlog=True)
    # outliers(cc_md_average, df, f"{language} CC and MD average distribution", "better_output/cc_sloc_outliers1.csv",lim=3, symlog=True)

    outliers(cc_sloc_ratio, df, f"{language} CC and SLOC ratio distribution", "better_output/cc_sloc_outliers1.csv", lim=3, symlog=True)
    outliers(md_sloc_ratio, df, f"{language} MD and SLOC ratio distribution", "better_output/cc_sloc_outliers1.csv",lim=10, symlog=True)
    outliers(cc_md_ratio, df, f"{language} CC and MD ratio distribution", "better_output/cc_sloc_outliers1.csv",lim=10, symlog=True)


    # scatterplot_loglog(df,'Source Lines of Code','Cyclomatic Complexity' , f"{language} Log-log Scatterplot SLOC & CC")
    # scatterplot_loglog(df, 'Source Lines of Code', 'Mutant Density',  f"{language} Log-log Scatterplot SLOC & MD")
    # scatterplot_loglog(df, 'Cyclomatic Complexity', 'Mutant Density',  f"{language} Log-log Scatterplot CC & MD")

    # scatterplot(df, 'Source Lines of Code', 'Cyclomatic Complexity', f"{language} Scatterplot SLOC & CC")
    # scatterplot(df, 'Source Lines of Code', 'Mutant Density', f"{language} Scatterplot SLOC & MD")
    # scatterplot(df, 'Cyclomatic Complexity', 'Mutant Density', f"{language} Scatterplot CC & MD")
    #
    # boxplot(boxplot_cc_sloc, f"{language} Boxplot CC on SLOC")
    # boxplot(boxplot_md_sloc, f"{language} Boxplot MD on sloc")




    print(f"pearson cc sloc 1 = {calculate_pearson(slocs_per_method, ccs_per_method, 1)}")
    print(f"pearson cc sloc 3 = {calculate_pearson(slocs_per_method, ccs_per_method, 3)}")
    print(f"pearson cc sloc 5 = {calculate_pearson(slocs_per_method, ccs_per_method, 5)}")
    print(f"pearson cc sloc 9 = {calculate_pearson(slocs_per_method, ccs_per_method, 9)}")
    print("-------------------------------")
    print(f"pearson md sloc 1 = {calculate_pearson(slocs_per_method, mds_per_method, 1)}")
    print(f"pearson md sloc 3 = {calculate_pearson(slocs_per_method, mds_per_method, 3)}")
    print(f"pearson md sloc 5 = {calculate_pearson(slocs_per_method, mds_per_method, 5)}")
    print(f"pearson md sloc 9 = {calculate_pearson(slocs_per_method, mds_per_method, 9)}")
    print(f"----------------------------")

    print(f"pearson cc md= {pearsonr(ccs_per_method, mds_per_method)}")
    print(f"pearson sloc md= {calculate_pearson(slocs_per_method, mds_per_method, 1)}")

    print()
