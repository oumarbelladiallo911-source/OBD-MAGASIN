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

# Définition des dossiers système pour Android (évite les bugs d'écriture de base de données)
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

def initialiser_bdd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS base_donnees (id INTEGER PRIMARY KEY AUTOINCREMENT, date_enregistrement TEXT, id_produit INTEGER, nom_produit TEXT UNIQUE, prix_revient REAL, prix_vente REAL, stock REAL, qte_vendu REAL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS historique (id INTEGER PRIMARY KEY AUTOINCREMENT, date_vente TEXT, id_produit INTEGER, nom_produit TEXT, qte_vendu REAL, prix_fixe REAL, prix_vendu REAL, remise_unitaire REAL, remise_totale REAL, montant_total REAL, statut TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS alerte (id INTEGER PRIMARY KEY AUTOINCREMENT, date_alerte TEXT, nom_produit TEXT UNIQUE, stock_restant REAL)")
    
    # Table crédit mise à jour avec les colonnes qte et telephone demandées
    cursor.execute("CREATE TABLE IF NOT EXISTS credit (id INTEGER PRIMARY KEY AUTOINCREMENT, date_enregistrement TEXT, qte REAL DEFAULT 1, nom_produit TEXT, nom_client TEXT, montant_credit REAL, somme_payee REAL DEFAULT 0, somme_restant REAL, jours_faits INTEGER DEFAULT 0, telephone TEXT DEFAULT '', situation TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS comptage_jours (date_unique TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

def enregistrer_jour_utilisation():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    auj = date.today().strftime("%d/%m/%Y")
    c.execute("INSERT OR IGNORE INTO comptage_jours (date_unique) VALUES (?)", (auj,))
    conn.commit()
    c.execute("SELECT COUNT(*) FROM comptage_jours")
    nb = c.fetchone()[0]
    conn.close()
    return nb

initialiser_bdd()
nb_jours = enregistrer_jour_utilisation()

# Gestion du blocage directement compatible Android
if nb_jours > 31:
    class BloqueApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            layout.add_widget(Label(text="APPLICATION BLOQUEE", font_size=24, color=(1,0,0,1)))
            layout.add_widget(Label(text=f"Vous avez utilisé {nb_jours} jours.\nLimite 31 jours atteinte.\nVeuillez Payer pour continuer.", halign='center'))
            layout.add_widget(Label(text="Appelez ce numéro pour payer : 628936146", font_size=18, color=(0.1,0.5,0.8,1)))
            
            self.code_input = TextInput(hint_text="Entrez le code de déblocage", multiline=False, size_hint_y=None, height=50)
            layout.add_widget(self.code_input)
            
            btn_deb = Button(text="DEBLOQUER", background_color=get_color_from_hex("#27AE60"), size_hint_y=None, height=50)
            btn_deb.bind(on_press=self.debloquer)
            layout.add_widget(btn_deb)
            return layout

        def debloquer(self, instance):
            s = self.code_input.text.strip()
            if s in CODES_DEBLOCAGE:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("DELETE FROM comptage_jours")
                auj = date.today().strftime("%d/%m/%Y")
                cur.execute("INSERT INTO comptage_jours (date_unique) VALUES (?)", (auj,))
                conn.commit()
                conn.close()
                os._exit(0)
    BloqueApp().run()
