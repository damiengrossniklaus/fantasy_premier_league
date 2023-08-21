import requests
import pandas as pd
import streamlit as st
from typing import Dict


@st.cache_resource(ttl=3600)
def query_data(url) -> Dict:
    """
    Gets data from url and returns the response as json
    """
    r = requests.get(url)
    json = r.json()

    return json


@st.cache_resource(ttl=3600)
def query_gw_data():
    """
    Gets player data for every played
    game week (gw) and returns them as a dataframe
    """
    player_gw_list = []

    for gw in range(1, 39):

        gw_url = f'https://fantasy.premierleague.com/api/event/{gw}/live/'
        gw_json = query_data(gw_url)

        if gw_json['elements']:

            for player in gw_json['elements']:
                player_dict = {'id': player['id'], 'gw': gw}
                player_dict.update(player['stats'])
                player_gw_list.append(player_dict)

        else:
            break

    return pd.DataFrame(player_gw_list)

