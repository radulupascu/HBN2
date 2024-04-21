import pandas as pd

df_name = pd.read_csv("prediction_name.csv", header=None)
df_code = pd.read_csv("prediction_code.csv", header=None)
df_url = pd.read_csv("input.csv")
df_url = df_url['url']
df_url = df_url.iloc[0:1000]

df_name.columns = ['product_name', 'predicted_family_name']
df_code.columns = ['product_name', 'predicted_family_code']

df_code.drop('product_name', axis=1, inplace=True)

df_name = df_name.reset_index(drop=False, inplace=False)
df_code = df_code.reset_index(drop=False, inplace=False)
df_url = df_url.reset_index(drop=False, inplace=False)

print(df_name)
# Merge the DataFrames on the 'ID' column
df_merged = pd.merge(df_url, df_name, on='index')
df_merged = pd.merge(df_merged, df_code, on='index')

# Display the merged DataFrame
#print(df_merged.info())
df_merged.to_csv("out.csv", index=False, encoding='utf-8')

#print(df_name.info(), df_code.info(), df_url.info())
