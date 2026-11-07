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

def job_effectuer_vente():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees"); liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_erreur("Erreur", "Aucun produit disponible."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Sélectionnez le Produit :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=40); box.add_widget(combo)
    box.add_widget(Label(text="Quantité :"))
    e_qte = TextInput(text="1", multiline=False, size_hint_y=None, height=40); box.add_widget(e_qte)
    lbl_p = Label(text="", color=(0.8,0.4,0,1)); box.add_widget(lbl_p)
    def maj(sp, text):
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT prix_vente FROM base_donnees WHERE nom_produit=?", (text,))
        res = cr.fetchone(); cn.close()
        if res: lbl_p.text = f"Prix Fixe : {formater_fg(res[0])}"
    combo.bind(text=maj); maj(combo, combo.text)
    box.add_widget(Label(text="Prix Vendu (FG) :"))
    e_prix = TextInput(multiline=False, size_hint_y=None, height=40); box.add_widget(e_prix)
    bv = Button(text="Officialiser la Vente", background_color=get_color_from_hex("#27AE60"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Saisie Vente", content=box, size_hint=(0.9, 0.75))
    def valider(ins):
        prod = combo.text
        try: qte, pv = float(e_qte.text), float(e_prix.text)
        except: afficher_popup_erreur("Erreur", "Champs invalides."); return
        if qte <= 0 or pv <= 0: return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        idp, pf, stk, qv = cr.fetchone()
        if qte > (stk - qv): afficher_popup_erreur("Impossible !", "Stock insuffisant."); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, pv, pf-pv, (pf-pv)*qte, pv*qte, "Vente Faîte"))
        if (stk - qv - qte) <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stk-qv-qte))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Vente faite !"); rafraichir_tableaux()
    bv.bind(on_press=valider); p.open()
def job_vente_credit():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees")
    liste_prods = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste_prods:
        afficher_popup_erreur("Erreur", "Aucun produit disponible.")
        return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Nom du Client :"))
    e_cl = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_cl)
    box.add_widget(Label(text="Numéro de Téléphone :"))
    e_tel = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_tel)
    box.add_widget(Label(text="Produit Endetté :"))
    combo_prod = Spinner(text=liste_prods[0], values=liste_prods, size_hint_y=None, height=38); box.add_widget(combo_prod)
    box.add_widget(Label(text="Quantité Endettée :"))
    e_qte = TextInput(text="1", multiline=False, size_hint_y=None, height=38); box.add_widget(e_qte)
    box.add_widget(Label(text="Montant Total Crédit (FG) :"))
    e_mt = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_mt)
    bv = Button(text="Valider le Crédit", background_color=get_color_from_hex("#D35400"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Vente A Crédit", content=box, size_hint=(0.95, 0.85))
    def Enregistrer(ins):
        cl = e_cl.text.strip(); tel = e_tel.text.strip(); prod = combo_prod.text
        try: qte = float(e_qte.text); mt = float(e_mt.text)
        except: afficher_popup_erreur("Erreur", "Champs numériques erronés."); return
        if not cl or not prod or mt <= 0 or qte <= 0:
            afficher_popup_erreur("Erreur", "Veuillez remplir tous les champs."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        row_prod = cr.fetchone()
        if not row_prod: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        idp, pf, stk, qv = row_prod; stock_rest = stk - (qv + qte)
        if stock_rest < 0:
            afficher_popup_erreur("Vente Bloquée !", f"Stock insuffisant. Reste: {int(stk-qv)}"); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rem_u = pf - (mt / qte)
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, mt/qte, rem_u, rem_u*qte, mt, "Vente à Crédit"))
        cr.execute("INSERT INTO credit (date_enregistrement, qte, nom_produit, nom_client, montant_credit, somme_restant, telephone, situation) VALUES (?,?,?,?,?,?,?,?)", (dt, qte, prod, cl, mt, mt, tel, "Vente à Crédit"))
        if stock_rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stock_rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Crédit enregistré !"); rafraichir_tableaux()
    bv.bind(on_press=Enregistrer); p.open()

def job_vente_credit():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees")
    liste_prods = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste_prods:
        afficher_popup_erreur("Erreur", "Aucun produit disponible.")
        return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Nom du Client :"))
    e_cl = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_cl)
    box.add_widget(Label(text="Numéro de Téléphone :"))
    e_tel = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_tel)
    box.add_widget(Label(text="Produit Endetté :"))
    combo_prod = Spinner(text=liste_prods[0], values=liste_prods, size_hint_y=None, height=38); box.add_widget(combo_prod)
    box.add_widget(Label(text="Quantité Endettée :"))
    e_qte = TextInput(text="1", multiline=False, size_hint_y=None, height=38); box.add_widget(e_qte)
    box.add_widget(Label(text="Montant Total Crédit (FG) :"))
    e_mt = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_mt)
    bv = Button(text="Valider le Crédit", background_color=get_color_from_hex("#D35400"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Vente A Crédit", content=box, size_hint=(0.95, 0.85))
    def Enregistrer(ins):
        cl = e_cl.text.strip(); tel = e_tel.text.strip(); prod = combo_prod.text
        try: qte = float(e_qte.text); mt = float(e_mt.text)
        except: afficher_popup_erreur("Erreur", "Champs numériques erronés."); return
        if not cl or not prod or mt <= 0 or qte <= 0:
            afficher_popup_erreur("Erreur", "Veuillez remplir tous les champs."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        row_prod = cr.fetchone()
        if not row_prod: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        idp, pf, stk, qv = row_prod; stock_rest = stk - (qv + qte)
        if stock_rest < 0:
            afficher_popup_erreur("Vente Bloquée !", f"Stock insuffisant. Reste: {int(stk-qv)}"); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rem_u = pf - (mt / qte)
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, mt/qte, rem_u, rem_u*qte, mt, "Vente à Crédit"))
        cr.execute("INSERT INTO credit (date_enregistrement, qte, nom_produit, nom_client, montant_credit, somme_restant, telephone, situation) VALUES (?,?,?,?,?,?,?,?)", (dt, qte, prod, cl, mt, mt, tel, "Vente à Crédit"))
        if stock_rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stock_rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Crédit enregistré !"); rafraichir_tableaux()
    bv.bind(on_press=Enregistrer); p.open()

def job_vente_credit():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees")
    liste_prods = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste_prods:
        afficher_popup_erreur("Erreur", "Aucun produit disponible.")
        return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Nom du Client :"))
    e_cl = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_cl)
    box.add_widget(Label(text="Numéro de Téléphone :"))
    e_tel = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_tel)
    box.add_widget(Label(text="Produit Endetté :"))
    combo_prod = Spinner(text=liste_prods[0], values=liste_prods, size_hint_y=None, height=38); box.add_widget(combo_prod)
    box.add_widget(Label(text="Quantité Endettée :"))
    e_qte = TextInput(text="1", multiline=False, size_hint_y=None, height=38); box.add_widget(e_qte)
    box.add_widget(Label(text="Montant Total Crédit (FG) :"))
    e_mt = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_mt)
    bv = Button(text="Valider le Crédit", background_color=get_color_from_hex("#D35400"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Vente A Crédit", content=box, size_hint=(0.95, 0.85))
    def Enregistrer(ins):
        cl = e_cl.text.strip(); tel = e_tel.text.strip(); prod = combo_prod.text
        try: qte = float(e_qte.text); mt = float(e_mt.text)
        except: afficher_popup_erreur("Erreur", "Champs numériques erronés."); return
        if not cl or not prod or mt <= 0 or qte <= 0:
            afficher_popup_erreur("Erreur", "Veuillez remplir tous les champs."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        row_prod = cr.fetchone()
        if not row_prod: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        idp, pf, stk, qv = row_prod; stock_rest = stk - (qv + qte)
        if stock_rest < 0:
            afficher_popup_erreur("Vente Bloquée !", f"Stock insuffisant. Reste: {int(stk-qv)}"); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rem_u = pf - (mt / qte)
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, mt/qte, rem_u, rem_u*qte, mt, "Vente à Crédit"))
        cr.execute("INSERT INTO credit (date_enregistrement, qte, nom_produit, nom_client, montant_credit, somme_restant, telephone, situation) VALUES (?,?,?,?,?,?,?,?)", (dt, qte, prod, cl, mt, mt, tel, "Vente à Crédit"))
        if stock_rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stock_rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Crédit enregistré !"); rafraichir_tableaux()
    bv.bind(on_press=Enregistrer); p.open()

def job_vente_credit():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees")
    liste_prods = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste_prods:
        afficher_popup_erreur("Erreur", "Aucun produit disponible.")
        return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Nom du Client :"))
    e_cl = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_cl)
    box.add_widget(Label(text="Numéro de Téléphone :"))
    e_tel = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_tel)
    box.add_widget(Label(text="Produit Endetté :"))
    combo_prod = Spinner(text=liste_prods[0], values=liste_prods, size_hint_y=None, height=38); box.add_widget(combo_prod)
    box.add_widget(Label(text="Quantité Endettée :"))
    e_qte = TextInput(text="1", multiline=False, size_hint_y=None, height=38); box.add_widget(e_qte)
    box.add_widget(Label(text="Montant Total Crédit (FG) :"))
    e_mt = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_mt)
    bv = Button(text="Valider le Crédit", background_color=get_color_from_hex("#D35400"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Vente A Crédit", content=box, size_hint=(0.95, 0.85))
    def Enregistrer(ins):
        cl = e_cl.text.strip(); tel = e_tel.text.strip(); prod = combo_prod.text
        try: qte = float(e_qte.text); mt = float(e_mt.text)
        except: afficher_popup_erreur("Erreur", "Champs numériques erronés."); return
        if not cl or not prod or mt <= 0 or qte <= 0:
            afficher_popup_erreur("Erreur", "Veuillez remplir tous les champs."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        row_prod = cr.fetchone()
        if not row_prod: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        idp, pf, stk, qv = row_prod; stock_rest = stk - (qv + qte)
        if stock_rest < 0:
            afficher_popup_erreur("Vente Bloquée !", f"Stock insuffisant. Reste: {int(stk-qv)}"); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rem_u = pf - (mt / qte)
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, mt/qte, rem_u, rem_u*qte, mt, "Vente à Crédit"))
        cr.execute("INSERT INTO credit (date_enregistrement, qte, nom_produit, nom_client, montant_credit, somme_restant, telephone, situation) VALUES (?,?,?,?,?,?,?,?)", (dt, qte, prod, cl, mt, mt, tel, "Vente à Crédit"))
        if stock_rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stock_rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Crédit enregistré !"); rafraichir_tableaux()
    bv.bind(on_press=Enregistrer); p.open()

