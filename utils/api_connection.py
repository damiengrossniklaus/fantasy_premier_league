import requests
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


