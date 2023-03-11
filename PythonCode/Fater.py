import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

registry_game = pd.read_csv('DataSets/registry_game.csv')
product_loaded = pd.read_csv('DataSets/product_loaded.csv')
product_ean_conversion = pd.read_csv('DataSets/product_ean_conversion.csv')
missions_players = pd.read_csv('DataSets/missions_players.csv')
app_accesses = pd.read_csv('DataSets/app_accesses.csv')
awards_moms = pd.read_csv('DataSets/awards_moms.csv')

"""
# Explore datasets
print(registry_game.head())
print(product_loaded.head())
print(product_ean_conversion.head())
print(missions_players.head())
print(app_accesses.head())
print(awards_moms.head())
"""
product_loaded['EAN'] = pd.to_numeric(product_loaded['EAN'], errors='coerce')
# Check for missing values
print(registry_game.isnull().sum())
print(product_loaded.isnull().sum())
print(product_ean_conversion.isnull().sum())
print(missions_players.isnull().sum())
print(app_accesses.isnull().sum())
print(awards_moms.isnull().sum())

# Merge datasets
# df = pd.concat([registry_game, product_loaded], axis=1)
df = pd.merge(registry_game, product_loaded, on='id_player', how='left')
df = pd.merge(df, product_ean_conversion, on='EAN', how='left')
df = pd.merge(df, missions_players, on=['id_player', 'missionDetailId'], how='left')
df = pd.merge(df, app_accesses, on='id_player', how='left')
df = pd.merge(df, awards_moms, on='id_player', how='left')

# Check for missing values after merging
print(df.isnull().sum())

# Feature engineering
df['DtaRegUserData'] = pd.to_datetime(df['DtaRegUserData'])
df['datarichiestapremio'] = pd.to_datetime(df['datarichiestapremio'])
df['time_to_request_award'] = df['datarichiestapremio'] - df['DtaRegUserData']
df['time_to_request_award'] = df['time_to_request_award'].dt.days
df['product_tier'] = df['TIER'].apply(lambda x: 'TIER1' if x == 'Premium' else 'TIER2' if x == 'Mid range' else 'TIER3')
df['mission_type'] = df['type'].apply(lambda x: 'app' if x == 'InApp' else 'other')
df['has_requested_award'] = df['nomepremio'].apply(lambda x: 1 if not pd.isna(x) else 0)

# Save cleaned dataset
df.to_csv('cleaned_data.csv', index=False)