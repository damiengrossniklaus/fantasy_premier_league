import streamlit as st


def assign_background():
    """
    Assignes background to webapp.
    """

    url = "https://assets-us-01.kc-usercontent.com/31dbcbc6-da4c-0033-328a-d7621d0fa726/d05eaaf9-58f2-4dcc-85f9" \
          "-12be33e2a9ec/Apple%20TV%20-%20Premier%20League.png?w=3840&q=75"

    page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
        background-image: url({url});
        background-size: cover;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """

    return st.markdown(page_bg_img, unsafe_allow_html=True)

def round_plot_borders():
    """
    Round borders of plots in App.
    """
    style_css = """
    <style>[data-testid="column"]{
    box-shadow: 5px 5px 2px black;
        }
    </style>"""

    return st.markdown(style_css, unsafe_allow_html=True)


