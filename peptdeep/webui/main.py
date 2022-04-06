# from alphapept.gui

import streamlit as st
from peptdeep.webui import startpage, rescore_ui, library_ui
from PIL import Image
import os
import socket
import peptdeep

_this_file = __file__
_this_directory = os.path.dirname(_this_file)
LOGO_PATH = os.path.join(_this_directory, 'logos', 'peptdeep.png')
ICON_PATH = os.path.join(_this_directory, 'logos', 'peptdeep.ico')
image = Image.open(LOGO_PATH)
icon = Image.open(ICON_PATH)
computer_name = socket.gethostname()

st.set_page_config(
    page_title=f"AlphaPeptDeep {peptdeep.__version__}",
    page_icon=icon,
    layout="wide",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.image(image, width = 300)
st.sidebar.code(f"AlphaPeptDeep {peptdeep.__version__} \n{computer_name}")

sidebar = {
    'Start': startpage.show,
    'Rescore': rescore_ui.show,
    'Library': library_ui.show,
}

menu = st.sidebar.radio("", list(sidebar.keys()))

if menu:
    sidebar[menu]()

link = f'[AlphaPeptDeep on GitHub]({peptdeep.__github__})'
st.sidebar.markdown(link, unsafe_allow_html=True)