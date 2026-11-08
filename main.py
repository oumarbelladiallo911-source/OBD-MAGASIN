# -*- coding: utf-8 -*-
import os
import sqlite3
from datetime import datetime, date

# Configuration de l'environnement pour Android
from kivy.config import Config
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Définition des dossiers système pour Android
data_dir = os.environ.get('KIVY_HOME', '.')
DB_PATH = os.path.join(data_dir, "gestion_magasin.db")

BG_FOND = "#2C3E50"
BLEU_BOUTON = "#2980B9"
MOT_DE_PASSE_ADMIN = "OBD123"

CODES_DEBLOCAGE = [
    "cOqH8Um5SWKKX0j","V0BXrdlB7UgL5V","rYwa6pb7PO99u9yr","4CkyGUImRDY7Nx5","Z0BTbu7Gr8Hu",
    "NQjxnDB9F1pD1c","ZrhJ9jNevOHNW","49nUPsRu0XZY777","ocOsAYGIXArHXKyQ","ig6Epm5obGIHLh",
    "v2W9XkirnVai","ikuNCAEZ2Nma","OOZp7Myfmwz8","dkWmsOqcjMfG6yV","Bps940FbbrrTd9K",
    "2bYm9gA4a94zM","CmFHaI9kgypr","1ffXozw9w5zL9m","Cwkw3Q6wBBb1W","fgAS9B0rZfFf2D2K",
    "QlXEzhFVKvPgI7","FPcCT76jSZCSTf","ognmRnAKb4YxWed","iG7PZv4z7wBAv","Ekf62IoiSvPCTX1",
    "XzKwHjlnT9iv","iYcRtRB1iP8o","gDgNUvT3HGCQgvL","yV2Vtdllsy1Haa","UdgbugE78vSDi",
    "Qrbdct0Fi7ok","wt0ei7gz8UfWgCRY","e15CntXxfuWB","pBZQngIq1vmcp2","ixYXM75G4jsTA",
    "yWObhBfWVyY598V","5VwzpFO1q7kgH","7rrEmDFsfzdui2nz","x7pdSQ3Sb52ZkZ09","L0A55Auhf91v",
    "ns0AP8mEVc2C","ZPykV4cNbEuwdt9","ELPZZvUmjg9dkW5","1EjhzeJ5S5fA3","sDPXP2BwbfaTXLxi",
    "gg8yqkLCAgnJqrc","LetB8yxiWQZHcZJZ","yoGD50xsKc3jY","84jJkIXiwivjRwmf","Lw2MWYiodQw9TvYV"
]
