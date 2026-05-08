import pandas as pd

def inspect(filename):
    print(f"\n--- {filename} ---")
    xls = pd.ExcelFile(filename)
    print("Sheets:", xls.sheet_names)
    for sheet in xls.sheet_names:
        df = pd.read_excel(filename, sheet_name=sheet)
        print(f"Sheet: {sheet}")
        print("Columns:", df.columns.tolist())
        print(df.head(5))

inspect('attackmitre.xlsx')
inspect('MitreEnterprise.xlsx')
