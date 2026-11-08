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

def initialiser_bdd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS base_donnees (id INTEGER PRIMARY KEY AUTOINCREMENT, date_enregistrement TEXT, id_produit INTEGER, nom_produit TEXT UNIQUE, prix_revient REAL, prix_vente REAL, stock REAL, qte_vendu REAL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS historique (id INTEGER PRIMARY KEY AUTOINCREMENT, date_vente TEXT, id_produit INTEGER, nom_produit TEXT, qte_vendu REAL, prix_fixe REAL, prix_vendu REAL, remise_unitaire REAL, remise_totale REAL, montant_total REAL, statut TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS alerte (id INTEGER PRIMARY KEY AUTOINCREMENT, date_alerte TEXT, nom_produit TEXT UNIQUE, stock_restant REAL)")
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
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

initialiser_bdd()

def formater_fg(v):
    try: return f"{int(float(v)):,}".replace(",", ".") + " FG"
    except: return "0 FG"

def formater_entier(v):
    try: return str(int(float(v)))
    except: return "0"

def afficher_popup_erreur(titre, message):
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text=message, halign='center'))
    btn = Button(text="OK", size_hint_y=None, height=40, background_color=get_color_from_hex("#E74C3C"))
    box.add_widget(btn)
    p = Popup(title=titre, content=box, size_hint=(0.85, 0.3))
    btn.bind(on_press=p.dismiss)
    p.open()

def afficher_popup_info(titre, message):
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text=message, halign='center'))
    btn = Button(text="OK", size_hint_y=None, height=40, background_color=get_color_from_hex("#27AE60"))
    box.add_widget(btn)
    p = Popup(title=titre, content=box, size_hint=(0.85, 0.3))
    btn.bind(on_press=p.dismiss)
    p.open()

def verifier_mot_de_passe_mobile(on_success):
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Zone Protégée - Entrez le mot de passe :"))
    pwd = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
    box.add_widget(pwd)
    bl = BoxLayout(spacing=10, size_hint_y=None, height=40)
    bv = Button(text="Valider", background_color=get_color_from_hex("#27AE60"))
    ba = Button(text="Annuler", background_color=get_color_from_hex("#E74C3C"))
    bl.add_widget(bv); bl.add_widget(ba); box.add_widget(bl)
    p = Popup(title="Sécurité Admin", content=box, size_hint=(0.85, 0.35))
    ba.bind(on_press=p.dismiss)
    def valider_pwd(ins):
        if pwd.text.strip() == MOT_DE_PASSE_ADMIN:
            p.dismiss(); on_success()
        else: afficher_popup_erreur("Accès Refusé", "Incorrect !")
    bv.bind(on_press=valider_pwd); p.open()

def rafraichir_tableaux():
    app = App.get_running_app()
    if app and app.root:
        try: app.root.get_screen('principal').mettre_a_jour_les_donnees()
        except: pass
