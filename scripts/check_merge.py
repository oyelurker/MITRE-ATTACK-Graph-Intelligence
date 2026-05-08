import pandas as pd

attack_df = pd.read_excel('attackmitre.xlsx')
enterprise_df = pd.read_excel('MitreEnterprise.xlsx')

attack_df['Tactic ID'] = attack_df['Group Techniques'].str.split('; ')
attack_exploded = attack_df.explode('Tactic ID')
attack_exploded['Tactic ID'] = attack_exploded['Tactic ID'].str.strip()

merged_df = pd.merge(
    attack_exploded, 
    enterprise_df, 
    on='Tactic ID', 
    how='inner'
)

print(f"Merged records: {len(merged_df)}")
print(merged_df[['APT Group Name', 'Tactic ID', 'Tactic Name']].head(20))
