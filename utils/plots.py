import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def build_hist(df: pd.DataFrame,
               x: str,
               color: str,
               title: str,
               label: str) -> go.Figure:
    """
    Creates histogram for variable x in passed df.
    """
    fig = px.histogram(data_frame=df,
                       x=x, nbins=15,
                       title=title,
                       labels={x: label})

    fig.update_traces(marker_color=color)

    return fig


def build_player_cost_points_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates scatterplot of player costs vs total points.
    """
    fig = px.scatter(df,
                     x='cost', y='total_points',
                     size='total_points',
                     color='position',
                     labels={'cost': 'Costs',
                             'total_points': 'Total Points'},
                     custom_data=['name'])

    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b> <br>'
                                    'Total Points: %{y} <br>'
                                    'Costs: %{x} m'
                                    '<extra></extra>')

    return fig


def build_team_points_bar(df: pd.DataFrame) -> go.Figure:
    """
    Create sorted barchart of points per team.
    """
    team_df = df.groupby('team', as_index=False)['total_points'].sum().sort_values('total_points', ascending=False)

    team_fig = px.bar(team_df,
                      x='team', y='total_points',
                      color='team')

    return team_fig


def build_heatmap(df: pd.DataFrame) -> plt.Figure:
    """
    Creates seaborn heatmap from pd.DataFrame.
    """
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 12))
    mask = np.triu(np.ones_like(df.corr(numeric_only=True)))

    sns.heatmap(df.corr(numeric_only=True), ax=ax,
                annot=True, cmap='viridis', center=0,
                mask=mask)

    return fig


def build_points_dev_plot(df: pd.DataFrame) -> go.Figure:
    """
    Creates lineplot of player cumulative points development
    """

    fig = px.line(df,
                  x='gw',
                  y='cumulative_points',
                  color='name',
                  custom_data=['name'],
                  labels={'gw': 'Gameweek',
                          'cumulative_points': 'Points'})

    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>'
                                    'Total Points: %{y}<br>'
                                    'Gw: %{x}'
                                    '<extra></extra>')





    return fig
