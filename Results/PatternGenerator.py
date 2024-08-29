import matplotlib.pyplot as plt
def plot_dimension(model_names, year, dimension, title="Dimension CEC", file_name_queries=None, special=None):
  for model in model_names:
    folder_path = f'./results/{model}'
    all_dataframes = []
    file_list = os.listdir(folder_path)
    for file_name in file_list:
      if file_name_queries is None:
        if file_name.endswith(f'{year}.csv'):
          file_path = os.path.join(folder_path, file_name)
          print(file_path)
          df = pd.read_csv(file_path)
          df = df.transpose()
          all_dataframes.append(df)
      else:
        if file_name in file_name_queries and file_name.endswith(f'{year}.csv'):
          file_path = os.path.join(folder_path, file_name)
          print(file_path)
          df = pd.read_csv(file_path)
          df = df.transpose()
          all_dataframes.append(df)
    combined_df = pd.concat(all_dataframes, axis=0)
    average_df = combined_df.groupby(level=0).mean()
    average_df = average_df.transpose()
    average_df['Rank'] = average_df['10'].rank()
    plt.plot(average_df['Unnamed: 0'].astype(int).astype(str), average_df['Rank'], marker='o', linewidth=1, label=model)
    plt.title(f'{dimension} {title} {year}')
    plt.xlabel('Population Size')
    plt.ylabel('Average Rank')
    plt.grid(True, axis="y")
    plt.legend()
    if special is None:
      saving_file_name = f'./results/Plots/{dimension}-CEC-{year}.png'
    else:
      saving_file_name = f'./results/Plots/{dimension}-{special}-CEC-{year}.png'
    plt.savefig(saving_file_name, dpi=300, bbox_inches='tight')
  plt.clf()

if __name__ == "__main__":
  all_algos = ['OriginalGWO', 'OBGWO', 'RWGWO', 'AGWO', 'IGWO', 'MELGWO', 'MGWO']
  for year in [2019, 2021, 2022]:
    for dimension in [10, 30, 50, 100]:
        plot_dimension(all_algos, year, dimension)

