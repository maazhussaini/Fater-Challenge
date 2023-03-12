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
    registry_game['ETA_MM_BambinoTODAY'] = registry_game['ETA_MM_BambinoTODAY'].abs()
    return registry_game


def detect_outliers(registry_game):
    # Identify potential outliers
    sns.boxplot(data=registry_game[[
                'ETA_MM_BambinoREG', 'ETA_MM_BambinoTODAY', 'DtaRegUserData']])
    plt.title('Boxplot for Age Variables')
    plt.xlabel('Variable')
    plt.ylabel('Age')
    plt.show()


def tier_based_product(product_loaded, product_ean_conversion, missions_players):
    # Merge relevant columns from different tables using the id_player as key
    product_mission_merge = pd.merge(missions_players[['id_player', 'points']], product_loaded[['id_player', 'points', 'EAN']],
                                     how='inner', on='id_player')

    product_mission_merge = product_mission_merge.rename(columns={
        'points_x': 'mission_points',
        'points_y': 'product_points',
    })

    product_mission_merge['EAN'] = pd.to_numeric(
        product_mission_merge['EAN'], errors='coerce')

    product_mission_merge = pd.merge(
        product_mission_merge, product_ean_conversion[['EAN', 'TIER']], how='inner', on='EAN')

    product_mission_merge['total_points_gained'] = product_mission_merge['mission_points'] + \
        product_mission_merge['product_points']

    product_mission_result = product_mission_merge.groupby('TIER')[
        'id_player'].count()
    print(product_mission_result)
    product_mission_result.plot(kind='bar')
    plt.xlabel('TIER')
    plt.ylabel('Customers')
    plt.title('Count of Y grouped by X')
    plt.show()

    return product_mission_merge


def feature_engineering(registry_game):

    # Feature engineering
    # create age groups
    bins = [-1, 2, 6, 8, 10, int(
        max(registry_game.ETA_MM_BambinoTODAY.to_list()))]

    labels = ['0-2', '3-6', '7-8', '9-10', '10+']
    registry_game['age_group'] = pd.cut(
        registry_game['ETA_MM_BambinoTODAY'], bins=bins, labels=labels)

    registry_game_result = registry_game.groupby('age_group')[
        'id_player'].count()
    print(registry_game_result)
    registry_game_result.plot(kind='bar')
    plt.xlabel('Range of Age')
    plt.ylabel('Number of Child')
    plt.title('Children of Different Age Group')
    plt.show()

    # view the data
    print(registry_game_result.head())


def active_age_group(registry_game, activeUsers_df):
    bins = [-1, 2, 6, 8, 10, int(
        max(registry_game.ETA_MM_BambinoTODAY.to_list()))]

    labels = ['0-2', '3-6', '7-8', '9-10', '10+']
    registry_game['age_group'] = pd.cut(
        registry_game['ETA_MM_BambinoTODAY'], bins=bins, labels=labels)

    # ---------------------------------------------------------------------------------------

    activeUsers_df = activeUsers_df[activeUsers_df['flag'] == 1]
    df = pd.merge(registry_game, activeUsers_df[[
                  'id_player']], how='inner', on='id_player')

    registry_game_result = df.groupby('age_group')[
        'id_player'].count()
    print(registry_game_result)
    registry_game_result.plot(kind='bar')
    plt.xlabel('Age of Year')
    plt.ylabel('Number of Active Child')
    plt.title('Children of Different Age Group')
    plt.show()


def active_users(missions_players, app_accesses):

    app_accesses['updated_at'] = pd.to_datetime(
        app_accesses['updated_at'])

    # extract the date part and save it to a new column 'date_only'
    app_accesses['updated_at'] = app_accesses['updated_at'].dt.date

    app_accesses_dates = app_accesses.groupby('id_player')[
        'updated_at'].max()

    app_accesses_dates = app_accesses_dates.rename_axis(
        'id_player').reset_index()

    """
    Assuming max date is a today date.
    """
    todayDate_access = max(app_accesses_dates['updated_at'].to_list())

    # ---------------------------------------------------------------------------------------

    missions_players['created_at'] = pd.to_datetime(
        missions_players['created_at'])

    # extract the date part and save it to a new column 'date_only'
    missions_players['created_at'] = missions_players['created_at'].dt.date

    missions_players_dates = missions_players.groupby('id_player')[
        'created_at'].max()

    missions_players_dates = missions_players_dates.rename_axis(
        'id_player').reset_index()

    """
    Assuming max date is a today date.
    """
    todayDate_mission = max(missions_players_dates['created_at'].to_list())

    todayDate = max(todayDate_mission, todayDate_access)
    print(todayDate)

    # ---------------------------------------------------------------------------------------

    app_accesses_dates['todayDate_access'] = todayDate
    app_accesses_dates['diff_date_access'] = (app_accesses_dates['todayDate_access'] -
                                              app_accesses_dates['updated_at']).dt.days

    print("\n\napp_accesses_dates: \n",
          app_accesses_dates[app_accesses_dates['diff_date_access'] > 30].shape)

    missions_players_dates['todayDate_mission'] = todayDate
    missions_players_dates['diff_date_mission'] = (missions_players_dates['todayDate_mission'] -
                                                   missions_players_dates['created_at']).dt.days

    print("missions_players_dates: \n",
          missions_players_dates[missions_players_dates['diff_date_mission'] > 30].shape)

    # ---------------------------------------------------------------------------------------

    mission_access_merge = pd.merge(
        missions_players_dates, app_accesses_dates, how='inner', on='id_player')

    mission_access_merge['diff_date'] = abs(mission_access_merge['diff_date_mission'] -
                                            mission_access_merge['diff_date_access'])

    mission_access_merge['flag'] = mission_access_merge['diff_date'].apply(
        lambda x: 0 if x > 30 else 1)

    activeUsers_df = mission_access_merge

    return activeUsers_df


def tier_active_age(product_mission, active_users_df):
    print(product_mission.head())


def award_details():
    pass


def main():

    registry_game, product_loaded, product_ean_conversion, missions_players, app_accesses, awards_moms = load_data()
    # check_missing_values(registry_game, product_loaded,
    #                      product_ean_conversion, missions_players, app_accesses, awards_moms)
    # descriptive_stats(registry_game, product_loaded, product_ean_conversion, missions_players,app_accesses, awards_moms)
    # detect_outliers(registry_game)
    registry_game = deal_with_garbage_data(registry_game)
    # detect_outliers(registry_game)

    product_mission = tier_based_product(
        product_loaded, product_ean_conversion, missions_players)
    # feature_engineering(registry_game)
    active_users_df = active_users(missions_players, app_accesses)
    # active_age_group(registry_game, active_users_df)
    tier_active_age(product_mission, active_users_df)


main()
