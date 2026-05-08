import pandas as pd
df = pd.read_excel('attackmitre.xlsx')
print(df[['Group Techniques', 'APT Group Name', 'Software ID']].head(10))

df2 = pd.read_excel('MitreEnterprise.xlsx')
print(df2[['Tactic ID', 'Tactic Name']].head(10))
