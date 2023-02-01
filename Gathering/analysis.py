import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
if __name__ == '__main__':
    df = pd.read_csv('FinalReport.csv', delimiter=';')
    sns.set_theme()
    slocs_per_method = []
    for idx, row in df.iterrows():
        sloc_for_method = row['Source Lines of Code']
        print(sloc_for_method)
        slocs_per_method.append(sloc_for_method)

    sns.histplot(df, x='Source Lines of Code',kde=False,)
    plt.show()

    png = sns.load_dataset("penguins")
    print()