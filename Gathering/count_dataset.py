import pandas as pd
import numpy as np
import os

def clean_df(df):
    df = df.astype({'Source Lines of Code': int, 'Cyclomatic Complexity': int, 'Mutant Density': int})
    df = df[np.isfinite(df['Source Lines of Code'])]
    df = df[np.isfinite(df['Cyclomatic Complexity'])]
    df = df[np.isfinite(df['Mutant Density'])]

    df = df.drop(df[df['Source Lines of Code'] == 0].index)
    df = df.drop(df[df['Cyclomatic Complexity'] == 0].index)
    df = df.drop(df[df['Mutant Density'] == 0].index)

    return df

if __name__ == '__main__':
    dfs = []
    for file in os.listdir('dataset_results/cpp'):
        df = pd.read_csv(f"dataset_results/cpp/{file}", delimiter=",")
        df = clean_df(df)
        print(f"Name: {file}, Methods: {len(df)}, SLOC: {pd.to_numeric(df['Source Lines of Code'], errors='coerce').sum()}")

    for file in os.listdir('dataset_results/c'):
        df = pd.read_csv(f"dataset_results/c/{file}", delimiter=",")
        df = clean_df(df)
        print(
            f"Name: {file}, Methods: {len(df)}, SLOC: {pd.to_numeric(df['Source Lines of Code'], errors='coerce').sum()}")

    for file in os.listdir('dataset_results/java'):
        df = pd.read_csv(f"dataset_results/java/{file}", delimiter=";")
        df = clean_df(df)
        print(
            f"Name: {file}, Methods: {len(df)}, SLOC: {pd.to_numeric(df['Source Lines of Code'], errors='coerce').sum()}")

    for file in os.listdir('dataset_results/python'):
        df = pd.read_csv(f"dataset_results/python/{file}", delimiter=",")
        df = clean_df(df)
        print(
            f"Name: {file}, Methods: {len(df)}, SLOC: {pd.to_numeric(df['Source Lines of Code'], errors='coerce').sum()}")
