import pandas as pd
import streamlit as st
import plotly.express as px
from utils.design_functions import assign_background
from utils.plots import build_hist, build_team_points_bar, build_heatmap, build_points_dev_plot, \
    build_player_cost_points_chart
from utils.api_connection import query_data, query_gw_data



# ---- GET DATA ----

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
json = query_data(url)

# Player gw data
player_gw_df = query_gw_data()


# ---- MANIPULATION ----

# Build data frames
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])

# Total dataframe
fpl_df = elements_df[['first_name', 'second_name', 'team', 'element_type',
                      'selected_by_percent', 'now_cost', 'minutes', 'transfers_in',
                      'value_season', 'total_points', 'form', 'creativity', 'threat', 'influence',
                      'expected_assists_per_90',  'expected_goals_per_90',
                      'expected_goal_involvements_per_90',
                      'expected_goals_conceded_per_90', 'saves_per_90', 'starts_per_90']]

# Create new columns for analysis
fpl_df['position'] = fpl_df['element_type'].map(elements_types_df.set_index('id')['singular_name'])
fpl_df['team'] = fpl_df['team'].map(teams_df.set_index('id')['name'])
fpl_df['value'] = fpl_df['value_season'].apply(lambda x: float(x))
fpl_df['cost'] = fpl_df['now_cost'] / 10
fpl_df['name'] = fpl_df['first_name'] + " " + fpl_df['second_name']
fpl_df['form'] = fpl_df['form'].astype('float')
fpl_df['creativity'] = fpl_df['creativity'].astype('float')
fpl_df['threat'] = fpl_df['threat'].astype('float')
fpl_df['influence'] = fpl_df['influence'].astype('float')


fpl_df = fpl_df[(fpl_df['minutes'] > 0) & (fpl_df['total_points'] > 0)].copy()

# Game week dataframe
# Map names to df
name_dict = dict(zip(elements_df['id'], elements_df['first_name'] + " " + elements_df['second_name']))
player_gw_df['name'] = player_gw_df['id'].map(name_dict)
player_gw_df['cumulative_points'] = player_gw_df.groupby('name', as_index=False)['total_points'].cumsum()

# ---- BODY ----

assign_background()

st.markdown("## ⚽ Fantasy Premier League Dashboard")

costs_points_scatter_fig = build_player_cost_points_chart(fpl_df)

st.markdown("### Cost vs. Total Points")
st.plotly_chart(costs_points_scatter_fig)
st.markdown("---")


# Position Histograms
gk_df = fpl_df[fpl_df['position'] == 'Goalkeeper']
def_df = fpl_df[fpl_df['position'] == 'Defender']
mid_df = fpl_df[fpl_df['position'] == 'Midfielder']
fwd_df = fpl_df[fpl_df['position'] == 'Forward']

gk_hist = build_hist(gk_df,
                     'value',
                     'darkorange',
                     'Goalkeepers',
                     'Points / Cost Ratio')

def_hist = build_hist(def_df,
                     'value',
                     'mediumseagreen',
                     'Defenders',
                     'Points / Cost Ratio')

mid_hist = build_hist(mid_df,
                     'value',
                     'midnightblue',
                     'Midfielders',
                     'Points / Cost Ratio')

fwd_hist = build_hist(fwd_df,
                     'value',
                     'crimson',
                     'Forwards',
                     'Points / Cost Ratio')

st.markdown("### Points / Cost Ratio Distribution per Position")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.plotly_chart(gk_hist, use_container_width=True)
col2.plotly_chart(def_hist, use_container_width=True)
col3.plotly_chart(mid_hist, use_container_width=True)
col4.plotly_chart(fwd_hist, use_container_width=True)

top_gk = gk_df.sort_values('value', ascending=False).head(2)
top_def = def_df.sort_values('value', ascending=False).head(5)
top_mid = mid_df.sort_values('value', ascending=False).head(5)
top_fwd = fwd_df.sort_values('value', ascending=False).head(3)

display_columns = ['name', 'team', 'position', 'total_points', 'cost', 'value', 'selected_by_percent', 'minutes', ]
best_points_cost_players_df = pd.concat([top_gk, top_def, top_mid, top_fwd])[display_columns]

st.markdown("## Most Valuable Team")
st.dataframe(best_points_cost_players_df, use_container_width=True)
st.markdown("---")

# Points per Team Ranking
st.markdown("### Total Points per Team")
team_points_fig = build_team_points_bar(fpl_df)
st.plotly_chart(team_points_fig, use_container_width=True)
st.markdown("---")

# Heatmap
st.markdown("### Variable Correlation Heatmap")
heatmap_fig = build_heatmap(fpl_df)
st.write(heatmap_fig)
st.markdown("---")

# Player GW points development
st.markdown("### Player Points Development")
player_gw_df = player_gw_df[player_gw_df['minutes'] > 0]
player_list = player_gw_df['name'].unique().tolist()
player_list.sort()
top_10_players_default = player_gw_df.sort_values('cumulative_points', ascending=False)['name'].head(10).to_list()
player_choices = st.multiselect('Select Players',
                                player_list,
                                default=top_10_players_default)

selected_players_df = player_gw_df[player_gw_df['name'].isin(player_choices)]

points_dev_fig = build_points_dev_plot(selected_players_df)

st.plotly_chart(points_dev_fig)
st.markdown("---")


# Dataframe
st.markdown("### Player Data")
display_df = fpl_df[['name', 'team', 'position', 'total_points', 'form', 'cost', 'value',
                     'creativity', 'threat', 'influence',
                     'selected_by_percent', 'now_cost', 'minutes', 'transfers_in',
                     'value_season', 'expected_assists_per_90', 'expected_goals_per_90',
                     'expected_goal_involvements_per_90', 'expected_goals_conceded_per_90', 'saves_per_90',
                     'starts_per_90']]
st.dataframe(display_df)

st.markdown("### GW Data")
st.dataframe(player_gw_df)