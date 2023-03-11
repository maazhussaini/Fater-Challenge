import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt


def load_data():

    registry_game = pd.read_csv('DataSets/registry_game.csv')
    product_loaded = pd.read_csv('DataSets/product_loaded.csv')
    product_ean_conversion = pd.read_csv('DataSets/product_ean_conversion.csv')
    missions_players = pd.read_csv('DataSets/missions_players.csv')
    app_accesses = pd.read_csv('DataSets/app_accesses.csv')
    awards_moms = pd.read_csv('DataSets/awards_moms.csv')

    return registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms


def check_missing_values(registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms):
    print(registry_game.isnull().sum())
    print('\n')
    print(product_loaded.isnull().sum())
    print('\n')
    print(product_ean_conversion.isnull().sum())
    print('\n')
    print(missions_players.isnull().sum())
    print('\n')
    print(app_accesses.isnull().sum())
    print('\n')
    print(awards_moms.isnull().sum())


def descriptive_stats(registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms):

    def show_description(registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms):
        print(registry_game.describe())
        print(product_loaded.describe())
        print(product_ean_conversion.describe())
        print(missions_players.describe())
        print(app_accesses.describe())
        print(awards_moms.describe())

    def show_info(registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms):
        print(registry_game.info())
        print('\n')
        print(product_loaded.info())
        print('\n')
        print(product_ean_conversion.info())
        print('\n')
        print(missions_players.info())
        print('\n')
        print(app_accesses.info())
        print('\n')
        print(awards_moms.info())

    show_description(registry_game, product_loaded, product_ean_conversion,
                     missions_players, app_accesses, awards_moms)
    show_info(registry_game, product_loaded, product_ean_conversion,
              missions_players, app_accesses, awards_moms)


def deal_with_garbage_data(registry_game):

    registry_game = registry_game[~registry_game['DtaPresuntoParto'].isnull()]
    registry_game['ETA_MM_BambinoREG'] = registry_game['ETA_MM_BambinoREG'].abs()
    return registry_game


def detect_outliers(registry_game):
    # Identify potential outliers
    sns.boxplot(data=registry_game[[
                'ETA_MM_BambinoREG', 'ETA_MM_BambinoTODAY', 'DtaRegUserData']])
    plt.title('Boxplot for Age Variables')
    plt.xlabel('Variable')
    plt.ylabel('Age')
    plt.show()


def merge_all_data(registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms):
    # Merge relevant columns from different tables using the id_player as key
    product_mission_merge = pd.merge(missions_players, product_loaded,
                                     how='inner', on='id_player')

    product_mission_merge = product_mission_merge.rename(columns={
        'points_x': 'mission_points',
        'created_at_x': 'mission_created_at',
        'points_y': 'product_points',
        'created_at_y': 'product_created_at'
    })

    product_mission_merge['EAN'] = pd.to_numeric(
        product_mission_merge['EAN'], errors='coerce')

    product_mission_merge = pd.merge(
        product_mission_merge, product_ean_conversion, how='inner', on='EAN')

    product_mission_merge['total_points_gained'] = product_mission_merge['mission_points'] + \
        product_mission_merge['product_points']

    print(product_mission_merge.columns)
    print(product_mission_merge.info())

    product_mission_result = product_mission_merge.groupby('TIER')[
        'id_player'].count()
    print(product_mission_result)
    product_mission_result.plot(kind='bar')
    plt.xlabel('TIER')
    plt.ylabel('Customers')
    plt.title('Count of Y grouped by X')
    plt.show()
    return product_mission_result


def feature_engineering(registry_game):

    # Feature engineering
    # create age groups
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']
    registry_game['age_group'] = pd.cut(
        registry_game['ETA_MM_BambinoTODAY'], bins=bins, labels=labels)

    registry_game_result = registry_game.groupby('age_group')[
        'id_player'].count()
    print(registry_game_result)
    registry_game_result.plot(kind='bar')
    plt.xlabel('TIER')
    plt.ylabel('Customers')
    plt.title('Count of Y grouped by X')
    plt.show()

    # view the data
    print(registry_game_result.head())


def active_users(missions_players, app_accesses):

    # Get today's date
    todayDate = datetime.today().strftime('%Y-%m-%d')

    # Convert today's date to datetime
    todayDate = pd.DataFrame(
        [pd.to_datetime(todayDate)], columns=['TodayDate'])

    todayDate['TodayDate'] = pd.to_datetime(todayDate['TodayDate']).dt.date

    missions_players['created_at'] = pd.to_datetime(
        missions_players['created_at'])

    # extract the date part and save it to a new column 'date_only'
    missions_players['created_at'] = missions_players['created_at'].dt.date

    missions_players_dates = missions_players.groupby('id_player')[
        'created_at'].max()

    missions_players_dates_max = missions_players_dates.index

    print(missions_players_dates.head())
    print(missions_players_dates.info())

    # date_result = todayDate['TodayDate'] - missions_players_dates['created_at']

    # missions_players_dates['diff_date'] = (
    #     todayDate['TodayDate'] - missions_players_dates['created_at']).dt.days

    # print(missions_players_dates)


def main():

    registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms = load_data()
    check_missing_values(registry_game, product_loaded,
                         product_ean_conversion, missions_players, app_accesses, awards_moms)
    # descriptive_stats(registry_game, product_loaded, product_ean_conversion, missions_players,app_accesses, awards_moms)
    # detect_outliers(registry_game)
    registry_game = deal_with_garbage_data(registry_game)
    # detect_outliers(registry_game)

    # merge_df = merge_all_data(registry_game, product_loaded,
    #                           product_ean_conversion, missions_players, app_accesses, awards_moms)
    # feature_engineering(registry_game)
    active_users(missions_players, app_accesses)


main()

# # Get today's date
# todayDate = datetime.today().strftime('%Y-%m-%d')

# # Convert today's date to datetime
# todayDate = pd.DataFrame([pd.to_datetime(todayDate)], columns=['TodayDate'])

# todayDate['TodayDate'] = pd.to_datetime(todayDate['TodayDate']).dt.date
# print(todayDate)
