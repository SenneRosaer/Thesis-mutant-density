import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

def unique_between():
    df_1= pd.read_csv("better_output/spring_outliers_cc_sloc.csv", delimiter=";")
    df_3= pd.read_csv("better_output/spring_outliers_md_sloc.csv", delimiter=";")
    df_2 = pd.read_csv("better_output/cc_sloc_outliers1.csv", delimiter=";")

    s1 = set()
    s2 = set()
    s3 = set()
    for idx, row in df_1.iterrows():
        s1.add(f"{row['File']};{row['Method Name']}")
        if 'Frame' in f"{row['File']};{row['Method Name']}":
            print(f"{row['File']};{row['Method Name']}")
    print('-----------------------------------------------')
    for idx, row in df_2.iterrows():
        s2.add(f"{row['File']};{row['Method Name']}")
        if 'Frame' in f"{row['File']};{row['Method Name']}":
            print(f"{row['File']};{row['Method Name']}")

    for idx, row in df_3.iterrows():
        s3.add(f"{row['File']};{row['Method Name']}")
        if 'Frame' in f"{row['File']};{row['Method Name']}":
            print(f"{row['File']};{row['Method Name']}")
    same = s1.intersection(s2)
    unique_new = s2.difference(s1)
    unique_new = unique_new.difference(s3)

    same2 = s2.intersection(s3)
    same3 = same.update(same2)
    merged_outer = pd.merge(df_1, df_2, on=['File', 'Method Name'], how='outer', indicator=True)
    unique_df = merged_outer[merged_outer['_merge'].isin([ 'right_only'])]
    np.savetxt("better_output/unique.csv", unique_df.to_numpy(), fmt='%s', delimiter=';')

    for idx, row in df_2.iterrows():
        s2.add(f"{row['File']};{row['Method Name']}")
        if f"{row['File']};{row['Method Name']}" in unique_new:
            print(f"{row['File']};{row['Method Name']}    : {row['Z-score']}")
    print()
if __name__ == '__main__':
    unique_between()
    # df_spring = pd.read_csv("better_output/md_sloc_average_outliers_specific.csv", delimiter=";")
    # df_complete = pd.read_csv("better_output/md_sloc_average_outliers1.csv", delimiter=";")
    df_spring = pd.read_csv("better_output/spring_outliers_md_sloc.csv", delimiter=";")
    df_complete = pd.read_csv("better_output/md_sloc_average_outliers1.csv", delimiter=";")
    df_complete = df_complete.loc[df_complete["File"].str.contains('spring')]
    print(df_spring)

    df = df_complete.merge(df_spring, on=["File", "Method Name"])
    print(df)
    methods = df["Method Name"].tolist()

    df_unique = df_spring[~df_spring["Method Name"].isin(methods)]
    np.savetxt("better_output/unique.csv", df_unique.to_numpy(), fmt='%s', delimiter=';')
    print(df_unique)

    data_complete = {}
    data_unique = {}

    for idx, row in df_complete.iterrows():
        zscore = math.floor(row["Z-score"])
        if zscore not in data_complete:
            data_complete[zscore] = 1
        else:
            data_complete[zscore] += 1

    for idx, row in df_unique.iterrows():
        zscore = math.floor(row["Z-score"])
        if zscore not in data_unique:
            data_unique[zscore] = 1
        else:
            data_unique[zscore] += 1

    x_values = sorted(set(list(data_complete.keys()) + list(data_unique.keys())))
    y_values1 = [data_complete.get(x, 0) for x in x_values]
    y_values2 = [data_unique.get(x, 0) for x in x_values]

    fig, ax = plt.subplots()

    bar1 = ax.bar(x_values, y_values1, color='tab:blue')
    bar2 = ax.bar(x_values, y_values2, bottom=y_values1, color='tab:orange')

    ax.legend((bar1[0], bar2[0]), ('Shared outliers', 'Spring only outliers'))
    ax.set_xlabel('Standard deviations from mean')
    ax.set_ylabel('Count')
    plt.show()