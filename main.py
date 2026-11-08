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
    if not liste_prods: afficher_popup_erreur("Erreur", "Aucun produit disponible."); return
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
        if not cl or not prod or mt <= 0 or qte <= 0: afficher_popup_erreur("Erreur", "Veuillez remplir tous les champs."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id_produit, prix_vente, stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        row_prod = cr.fetchone()
        if not row_prod: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        idp, pf, stk, qv = row_prod; stock_rest = stk - (qv + qte)
        if stock_rest < 0: afficher_popup_erreur("Vente Bloquée !", f"Stock insuffisant. Reste: {int(stk-qv)}"); cn.close(); return
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu + ? WHERE nom_produit=?", (qte, prod))
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rem_u = pf - (mt / qte)
        cr.execute("INSERT INTO historique (date_vente, id_produit, nom_produit, qte_vendu, prix_fixe, prix_vendu, remise_unitaire, remise_totale, montant_total, statut) VALUES (?,?,?,?,?,?,?,?,?,?)", (dt, idp, prod, qte, pf, mt/qte, rem_u, rem_u*qte, mt, "Vente à Crédit"))
        cr.execute("INSERT INTO credit (date_enregistrement, qte, nom_produit, nom_client, montant_credit, somme_restant, telephone, situation) VALUES (?,?,?,?,?,?,?,?)", (dt, qte, prod, cl, mt, mt, tel, "Vente à Crédit"))
        if stock_rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (dt, prod, stock_rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Crédit enregistré !"); rafraichir_tableaux()
    bv.bind(on_press=Enregistrer); p.open()

def job_annuler_vente():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT DISTINCT nom_produit FROM historique WHERE statut!='Vente annuler'")
    liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_erreur("Erreur", "Aucune vente à annuler."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Produit à Annuler :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=40); box.add_widget(combo)
    box.add_widget(Label(text="Quantité à annuler :"))
    e_q = TextInput(text="1", multiline=False, size_hint_y=None, height=40); box.add_widget(e_q)
    bv = Button(text="Valider l'Annulation", background_color=get_color_from_hex("#E74C3C"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Annuler Une Vente", content=box, size_hint=(0.9, 0.5))
    def exec_ann(ins):
        prod = combo.text
        try: q = float(e_q.text)
        except: afficher_popup_erreur("Erreur", "Quantité invalide."); return
        if q <= 0: return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id, statut FROM historique WHERE LOWER(nom_produit)=LOWER(?) AND qte_vendu=? AND statut!='Vente annuler' LIMIT 1", (prod.strip(), q))
        row = cr.fetchone()
        if not row: afficher_popup_erreur("Erreur", "Aucune vente correspondante."); cn.close(); return
        cr.execute("UPDATE historique SET statut='Vente annuler' WHERE id=?", (row[0],))
        cr.execute("UPDATE base_donnees SET qte_vendu = qte_vendu - ? WHERE LOWER(nom_produit)=LOWER(?)", (q, prod.strip()))
        cr.execute("SELECT stock, qte_vendu FROM base_donnees WHERE LOWER(nom_produit)=LOWER(?)", (prod.strip(),))
        stk, qv = cr.fetchone(); rest = stk - qv
        if rest > 10: cr.execute("DELETE FROM alerte WHERE LOWER(nom_produit)=LOWER(?)", (prod.strip(),))
        else: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), prod.strip(), rest))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Vente Annulée !"); rafraichir_tableaux()
    bv.bind(on_press=exec_ann); p.open()
def job_imprimer_achats_pdf():
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Titre du document PDF :"))
    e_t = TextInput(hint_text="Ex: Alerte du jour", multiline=False, size_hint_y=None, height=40); box.add_widget(e_t)
    bv = Button(text="Générer le PDF", background_color=get_color_from_hex("#2980B9"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Imprimer en PDF", content=box, size_hint=(0.9, 0.4))
    def ok_pdf(ins):
        titre = e_t.text.strip()
        if not titre: return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT nom_produit, stock_restant, date_alerte FROM alerte"); lignes = cr.fetchall(); cn.close()
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Mes Achats - Alerte Stock", 0, 1, "C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"Titre: {titre}", 0, 1)
            pdf.cell(0, 8, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
            pdf.ln(10)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(50, 10, "Date Alerte", 1, 0, "C")
            pdf.cell(70, 10, "Produit", 1, 0, "C")
            pdf.cell(50, 10, "Stock Restant", 1, 0, "C")
            pdf.ln()
            pdf.set_font("Arial", "", 10)
            for li in lignes:
                pdf.cell(50, 8, str(li[2]), 1)
                pdf.cell(70, 8, str(li[0]), 1)
                pdf.cell(50, 8, str(int(li[1])), 1, 0, "C")
                pdf.ln()
            nom_safe = "".join(c for c in titre if c.isalnum() or c in " -_").strip()
            chemin = os.path.join(os.environ.get('KIVY_HOME', '.'), f"{nom_safe}.pdf")
            pdf.output(chemin)
            p.dismiss(); afficher_popup_info("PDF Créé", f"Fichier enregistré :\n{chemin}")
        except Exception:
            try:
                nom_safe = "".join(c for c in titre if c.isalnum() or c in " -_").strip()
                chemin = os.path.join(os.environ.get('KIVY_HOME', '.'), f"{nom_safe}.txt")
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write(f"Mes Achats - Alerte Stock\nTitre: {titre}\nDate: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
                    for li in lignes:
                        f.write(f"Date: {li[2]} | Produit: {li[0]} | Stock rest: {int(li[1])}\n")
                p.dismiss(); afficher_popup_info("Rapport créé", f"Fichier enregistré (Format Texte) :\n{chemin}")
            except Exception as e2: afficher_popup_error("Erreur Export", str(e2))
    bv.bind(on_press=ok_pdf); p.open()

def job_bilan_produit():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees"); liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_error("Erreur", "Aucun produit disponible."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Sélectionnez le Produit :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=40); box.add_widget(combo)
    bv = Button(text="Afficher le Bilan", background_color=get_color_from_hex("#2980B9"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Bilan Par Produit", content=box, size_hint=(0.9, 0.4))
    def voir_bilan(ins):
        prod_demande = combo.text
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT date_vente, nom_produit, qte_vendu, prix_vendu, statut FROM historique")
        hist = cr.fetchall()
        cr.execute("SELECT prix_revient FROM base_donnees WHERE LOWER(nom_produit)=LOWER(?)", (prod_demande.strip(),))
        row_rev = cr.fetchone()
        if not row_rev: afficher_popup_erreur("Erreur", "Produit introuvable."); cn.close(); return
        pa = row_rev[0]; q_j, q_j_tous, b_j, auj = 0, 0, 0, date.today().strftime("%d/%m/%Y")
        for dt, pr, q, px, st in hist:
            if st.upper() == "VENTE ANNULER" or "CREDIT" in st.upper(): continue
            if auj in dt: q_j_tous += q
            if pr.upper() == prod_demande.upper():
                if auj in dt: q_j += q; b_j += (px - pa) * q
        cn.close(); p.dismiss()
        pct = (q_j / q_j_tous * 100) if q_j_tous > 0 else 0
        afficher_popup_info(f"Bilan : {prod_demande.upper()}", f"Quantité Vendue Aujourd'hui : {int(q_j)}\nBénéfice Réel Jour : {formater_fg(b_j)}\nPourcentage : {pct:.0f} %")
    bv.bind(on_press=voir_bilan); p.open()

def job_statistique_magasin():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT date_vente, nom_produit, qte_vendu, prix_vendu, statut FROM historique")
    hist = cur.fetchall(); nj, bj, bm_total, dj = 0, 0, 0, {}
    auj_str = date.today().strftime("%d/%m/%Y")
    for dt_str, pr, q, px, st in hist:
        if "ANNUL" in st.upper() or "CREDIT" in st.upper(): continue
        cur.execute("SELECT prix_revient FROM base_donnees WHERE nom_produit=?", (pr,))
        rev = cur.fetchone(); pa = rev[0] if rev else 0
        benef = (px - pa) * q
        bm_total += benef
        if auj_str in dt_str: nj += 1; bj += benef; dj[pr] = dj.get(pr, 0) + q
    dt_f = datetime.now().strftime("%d/%m/%Y %H:%M")
    if nj == 0: txt = f"BILAN MAGASIN\nDate: {dt_f}\nAucune Vente comptabilisée aujourd'hui (hors crédits).\n"
    else:
        max_p = max(dj, key=dj.get); min_p = min(dj, key=dj.get)
        txt = f"BILAN MAGASIN\nDate: {dt_f}\nVentes Jour: {nj}\nMax: {max_p} ({int(dj[max_p])})\nMin: {min_p} ({int(dj[min_p])})\nBénéfice Jour: {formater_fg(bj)}\n"
    txt += f"-----------------------------------------\nBénéfice Total Réel: {formater_fg(bm_total)}"
    conn.close(); afficher_popup_info("BILAN MAGASIN", txt)
def modifier_produit_existant_form():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees"); liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_erreur("Erreur", "Aucun produit existant."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Sélectionnez le Produit :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=38); box.add_widget(combo)
    box.add_widget(Label(text="Quantité à AJOUTER :"))
    e_q = TextInput(text="0", multiline=False, size_hint_y=None, height=38); box.add_widget(e_q)
    box.add_widget(Label(text="Nouveau Prix d'achat / Revient (FG) :"))
    e_pa = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_pa)
    box.add_widget(Label(text="Nouveau Prix de Vente Fixe (FG) :"))
    e_pv = TextInput(multiline=False, size_hint_y=None, height=38); box.add_widget(e_pv)
    bv = Button(text="Enregistrer les Modifications", background_color=get_color_from_hex("#27AE60"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Modifier & Réapprovisionner", content=box, size_hint=(0.95, 0.85))
    def ok_mod(ins):
        prod = combo.text
        try: q_add = float(e_q.text); n_pa = float(e_pa.text); n_pv = float(e_pv.text)
        except: afficher_popup_erreur("Erreur", "Champs invalides."); return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("UPDATE base_donnees SET stock = stock + ?, prix_revient = ?, prix_vente = ? WHERE nom_produit = ?", (q_add, n_pa, n_pv, prod))
        cr.execute("SELECT stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        stk, qv = cr.fetchone(); rest = stk - qv
        if rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), prod, rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Informations et stock mis à jour !"); rafraichir_tableaux()
    bv.bind(on_press=ok_mod); p.open()

def augmenter_stock_existant_form():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT nom_produit FROM base_donnees"); liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_erreur("Erreur", "Aucun produit existant."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Sélectionnez le Produit :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=40); box.add_widget(combo)
    box.add_widget(Label(text="Quantité à ajouter :"))
    e_add = TextInput(multiline=False, size_hint_y=None, height=40); box.add_widget(e_add)
    bv = Button(text="Valider l'Ajout", background_color=get_color_from_hex("#27AE60"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Augmenter Stock", content=box, size_hint=(0.9, 0.45))
    def ok_add(ins):
        prod = combo.text
        try: q = float(e_add.text)
        except: afficher_popup_erreur("Erreur", "Quantité invalide."); return
        if q <= 0: return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("UPDATE base_donnees SET stock = stock + ? WHERE nom_produit=?", (q, prod))
        cr.execute("SELECT stock, qte_vendu FROM base_donnees WHERE nom_produit=?", (prod,))
        stk, qv = cr.fetchone(); rest = stk - qv
        if rest <= 10: cr.execute("INSERT OR REPLACE INTO alerte (date_alerte, nom_produit, stock_restant) VALUES (?, ?, ?)", (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), prod, rest))
        else: cr.execute("DELETE FROM alerte WHERE nom_produit=?", (prod,))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Stock augmenté !"); rafraichir_tableaux()
    bv.bind(on_press=ok_add); p.open()

def job_ajouter_stock():
    box = BoxLayout(orientation='vertical', padding=15, spacing=10)
    box.add_widget(Label(text="Voulez-vous apporter des modifications\naux informations du produit ?", halign='center'))
    bl = BoxLayout(spacing=15, size_hint_y=None, height=45)
    by = Button(text="Oui (Modifier Infos)", background_color=get_color_from_hex("#2980B9"))
    bn = Button(text="Non (Juste Stock)", background_color=get_color_from_hex("#27AE60"))
    bl.add_widget(by); bl.add_widget(bn); box.add_widget(bl)
    p = Popup(title="Ajout Stock / Produit", content=box, size_hint=(0.9, 0.35))
    by.bind(on_press=lambda x: [p.dismiss(), modifier_produit_existant_form()])
    bn.bind(on_press=lambda x: [p.dismiss(), augmenter_stock_existant_form()])
    p.open()

def job_payer_dette():
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.execute("SELECT DISTINCT nom_client FROM credit WHERE situation!='Rembourser 100%'")
    liste = [r[0] for r in cur.fetchall()]; conn.close()
    if not liste: afficher_popup_erreur("Erreur", "Aucun client endetté."); return
    box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    box.add_widget(Label(text="Selectionnez le Client :"))
    combo = Spinner(text=liste[0], values=liste, size_hint_y=None, height=40); box.add_widget(combo)
    lbl = Label(text="", color=(0.8,0.2,0.2,1)); box.add_widget(lbl)
    def maj(sp, text):
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT SUM(somme_restant) FROM credit WHERE UPPER(nom_client)=UPPER(?) AND situation!='Rembourser 100%'", (text,))
        res = cr.fetchone(); cn.close()
        if res and res[0] is not None: lbl.text = f"Reste : {formater_fg(res[0])}"
    combo.bind(text=maj); maj(combo, combo.text)
    box.add_widget(Label(text="Montant du Versement (FG) :"))
    e_p = TextInput(multiline=False, size_hint_y=None, height=40); box.add_widget(e_p)
    bv = Button(text="Valider le Paiement", background_color=get_color_from_hex("#27AE60"), size_hint_y=None, height=45)
    box.add_widget(bv)
    p = Popup(title="Payer Dette", content=box, size_hint=(0.9, 0.6))
    def encaisser(ins):
        client = combo.text
        try: p_paye = float(e_p.text)
        except: afficher_popup_erreur("Erreur", "Montant invalide."); return
        if p_paye <= 0: return
        cn = sqlite3.connect(DB_PATH); cr = cn.cursor()
        cr.execute("SELECT id, somme_restant, nom_produit, qte FROM credit WHERE UPPER(nom_client)=UPPER(?) AND situation!='Rembourser 100%' LIMIT 1", (client,))
        row = cr.fetchone()
        if not row: afficher_popup_erreur("Erreur", "Dette introuvable."); cn.close(); return
        id_c, reste, prod_endette, qte_endette = row
        if p_paye > reste: afficher_popup_erreur("Erreur", "La somme dépasse la dette !"); cn.close(); return
        nst = reste - p_paye; sit = "Rembourser 100%" if nst == 0 else "Remboursé 1/2"
        cr.execute("UPDATE credit SET somme_payee=somme_payee+?, somme_restant=?, situation=? WHERE id=?", (p_paye, nst, sit, id_c))
        if nst == 0:
            cr.execute("SELECT id FROM historique WHERE LOWER(nom_produit)=LOWER(?) AND qte_vendu=? AND statut='Vente à Crédit' LIMIT 1", (prod_endette.strip(), qte_endette))
            h_row = cr.fetchone()
            if h_row: cr.execute("UPDATE historique SET statut='Vente Faîte' WHERE id=?", (h_row[0],))
        cn.commit(); cn.close(); p.dismiss(); afficher_popup_info("Succès", "Paiement pris en compte !"); rafraichir_tableaux()
    bv.bind(on_press=encaisser); p.open()
