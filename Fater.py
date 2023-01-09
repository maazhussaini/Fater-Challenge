import pandas as pd

accessi_app_df = pd.read_csv(
    'DataSet/business_game_napoli_csv/accessi_app.csv')

print(accessi_app_df.describe)
