import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

award_info_df = pd.read_csv(
    'DataSet/business_game_napoli_csv/premi_mamme.csv')

registry_df = pd.read_csv(
    'DataSet/business_game_napoli_csv/anagrafica.csv')

mission_player = pd.read_csv(
    'DataSet/business_game_napoli_csv/missioni_players.csv')

def redeemingPoints_player(registry_df, award_info_df):

    """
    Check which players are redeeming their points
    """

    redeemingPoints_df = pd.merge(registry_df, award_info_df, on='id_player', how='outer')

    redeemingPoints_player = redeemingPoints_df.groupby(['id_player'])[['puntipremio']].sum()

    # #Using reset_index, inplace=True
    redeemingPoints_player.reset_index(inplace=True)
    print(redeemingPoints_player.describe())

    plt.plot(redeemingPoints_player.puntipremio, list(redeemingPoints_player.index.array))
    plt.ylabel('Players', fontsize=14)
    plt.xlabel('Point', fontsize=14)
    plt.grid(True)
    
    return plt.show()

    """
    END
    """

def checkPlayerIsPlaying(registry_df, mission_player):
    """
    Check which players are actively playing
    """
    playingPlayer_df = pd.merge(registry_df, mission_player, on='id_player', how='outer')

    playingPlayer = playingPlayer_df.groupby(['id_player'])[['missionDetailId']].count()

    # #Using reset_index, inplace=True
    playingPlayer.reset_index(inplace=True)
    print(playingPlayer.describe())

    playingPlayer.reset_index(inplace=True)
    print(playingPlayer.describe())

    plt.plot(playingPlayer.id_player, playingPlayer.missionDetailId, color = 'red', marker = '*')
    plt.xlabel('Players', fontsize=14)
    plt.ylabel('missionDetailId', fontsize=14)
    plt.grid(True)
    
    return plt.show()

def playingGameAndRedeemingPoints(registry_df, mission_player, award_info_df):
    
    """
        Check which player is playing game, but he is not redeeming their points.
    """

    playingPlayer_df = pd.merge(registry_df, mission_player, on='id_player', how='inner')
    
    notCollectingAwards = playingPlayer_df[~playingPlayer_df['id_player'].isin(award_info_df.id_player)]
    CollectingAwards = playingPlayer_df[playingPlayer_df['id_player'].isin(award_info_df.id_player)]

    notCollectingAwardsGroupBy = notCollectingAwards.groupby(['id_player']).id_player.count()

    print( notCollectingAwards.describe(), "\n###\n",CollectingAwards.describe())
    

playingGameAndRedeemingPoints(registry_df, mission_player, award_info_df)