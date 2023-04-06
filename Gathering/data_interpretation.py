import pandas as pd
import numpy as np

if __name__ == '__main__':
    df_spring = pd.read_csv("better_output/python/md_cc_outliers.csv", delimiter=";")
    df_complete = pd.read_csv("better_output/complete_dataset_calculation/md_cc_outliers.csv", delimiter=";")
    print(df_spring)

    df = df_complete.merge(df_spring, on=["File", "Method Name"])
    print(df)
    methods = df["Method Name"].tolist()

    df_unique = df_spring[~df_spring["Method Name"].isin(methods)]
    np.savetxt("better_output/unique.csv", df_unique.to_numpy(), fmt='%s', delimiter=';')
    print(df_unique)