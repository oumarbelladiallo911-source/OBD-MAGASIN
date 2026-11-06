# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
Window.clearcolor = get_color_from_hex("#2C3E50")
CODES=["cOqH8Um5SWKKX0j","V0BXrdlB7UgL5V","rYwa6pb7PO99u9yr","4CkyGUImRDY7Nx5","Z0BTbu7Gr8Hu"]
def init_db():
    conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS base_donnees (id INTEGER PRIMARY KEY, date_enregistrement TEXT, id_produit INTEGER, nom_produit TEXT UNIQUE, prix_revient REAL, prix_vente REAL, stock REAL, qte_vendu REAL DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS historique (id INTEGER PRIMARY KEY, date_vente TEXT, id_produit INTEGER, nom_produit TEXT, qte_vendu REAL, prix_fixe REAL, prix_vendu REAL, statut TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS alerte (id INTEGER PRIMARY KEY, date_alerte TEXT, nom_produit TEXT UNIQUE, stock_restant REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS credit (id INTEGER PRIMARY KEY, date_enregistrement TEXT, nom_produit TEXT, qte_credit TEXT DEFAULT '', nom_client TEXT, montant_credit REAL, somme_payee REAL DEFAULT 0, somme_restant REAL, tel_client TEXT, situation TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS comptage_jours (date_unique TEXT PRIMARY KEY)")
    try:c.execute("ALTER TABLE credit ADD COLUMN qte_credit TEXT DEFAULT ''")
    except:pass
    try:c.execute("ALTER TABLE credit ADD COLUMN tel_client TEXT")
    except:pass
    conn.commit();conn.close()
def fmt_fg(v):
    try:return f"{int(float(v)):,} FG".replace(",",".")
    except:return "0 FG"
def fmt_int(v):
    try:return str(int(float(v)))
    except:return "0"
def count_jours():
    conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor()
    auj=date.today().strftime("%d/%m/%Y")
    c.execute("INSERT OR IGNORE INTO comptage_jours VALUES (?)",(auj,))
    conn.commit();c.execute("SELECT COUNT(*) FROM comptage_jours");nb=c.fetchone()[0];conn.close();return nb
class OBDApp(App):
def build(self):
  init_db()
  if count_jours()>31:
   b=BoxLayout(orientation='vertical',padding=20,spacing=10)
   b.add_widget(Label(text="BLOQUE 31j - Contact 628936146",color=(1,0,0,1),bold=True))
   self.cd=TextInput(hint_text="Code reabonnement",multiline=False,size_hint_y=0.2);b.add_widget(self.cd)
   def deb(*a):
    if self.cd.text.strip() in CODES:
     conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("DELETE FROM comptage_jours");c.execute("INSERT INTO comptage_jours VALUES (?)",(date.today().strftime("%d/%m/%Y"),));conn.commit();conn.close();self.stop();OBDApp().run()
    else:Popup(title="Erreur",content=Label(text="Code faux"),size_hint=(0.8,0.3)).open()
   b.add_widget(Button(text="DEBLOQUER",background_color=get_color_from_hex("#27AE60"),on_press=deb));return b
  root=BoxLayout(orientation='vertical',padding=8,spacing=8)
  root.add_widget(Label(text="OBD VISION PHONE FINAL",size_hint_y=0.08,bold=True,color=(1,1,1,1)))
  grid=GridLayout(cols=2,spacing=8,size_hint_y=0.45)
  grid.add_widget(Button(text="Vente\n(Stock Restant)",background_color=get_color_from_hex("#2980B9"),on_press=self.vente))
  grid.add_widget(Button(text="Credit\n(Qte+Tel)",background_color=get_color_from_hex("#D35400"),on_press=self.credit))
  grid.add_widget(Button(text="Annuler Vente",background_color=get_color_from_hex("#E74C3C"),on_press=self.annuler))
  grid.add_widget(Button(text="Stock/Produit",background_color=get_color_from_hex("#27AE60"),on_press=self.ajout_choix))
  grid.add_widget(Button(text="Payer Dette",background_color=get_color_from_hex("#8E44AD"),on_press=self.payer))
  grid.add_widget(Button(text="Stats Magasin",background_color=get_color_from_hex("#2C3E50"),on_press=self.stats))
  root.add_widget(grid)
  tabs=GridLayout(cols=4,size_hint_y=0.07,spacing=2)
  tabs.add_widget(Button(text="Magasin",background_color=get_color_from_hex("#E67E22"),on_press=self.show_magasin))
  tabs.add_widget(Button(text="Hist",background_color=get_color_from_hex("#27AE60"),on_press=self.show_hist))
  tabs.add_widget(Button(text="Credits",background_color=get_color_from_hex("#F1C40F"),on_press=self.show_credits))
  tabs.add_widget(Button(text="Alerte",background_color=get_color_from_hex("#E74C3C"),on_press=self.show_alerte))
  root.add_widget(tabs)
  self.scroll=ScrollView(size_hint_y=0.4)
  self.lbl=Label(text="Bienvenue Chef!\nVente: Prix Fixe+Stock Restant\nCredit: Qte vide(0/Aucun)+Tel\nCouleurs: Faite/Dette=Blanc Annuler=Rouge 1/2=Jaune 100%=Vert",size_hint_y=None,height=800,text_size=(Window.width-20,None),halign='left',valign='top',color=(1,1,1,1))
  self.scroll.add_widget(self.lbl);root.add_widget(self.scroll);return root
def vente(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT nom_produit FROM base_donnees");liste=[r[0] for r in cur.fetchall()];conn.close()
  if not liste:Popup(title="Erreur",content=Label(text="Aucun produit"),size_hint=(0.8,0.3)).open();return
  b=BoxLayout(orientation='vertical',spacing=5,padding=10);sp=Spinner(text=liste[0],values=liste,size_hint_y=0.15)
  info=Label(text="",size_hint_y=0.2,color=get_color_from_hex("#F39C12"),font_size=11);qte=TextInput(hint_text="Qte",input_filter='float',size_hint_y=0.15);prix=TextInput(hint_text="Prix vendu FG",input_filter='float',size_hint_y=0.15)
  def maj(*x):
   conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("SELECT prix_vente,stock,qte_vendu,nom_produit FROM base_donnees WHERE nom_produit=?",(sp.text,));r=c.fetchone();conn.close()
   if r:info.text=f"Fixe:{fmt_fg(r[0])} | {r[3]} | Rest:{fmt_int(r[1]-r[2])}"
  sp.bind(text=lambda *s:maj());maj();b.add_widget(sp);b.add_widget(info);b.add_widget(qte);b.add_widget(prix)
  def val(*x):
   try:
    prod=sp.text;q=float(qte.text);pv=float(prix.text);conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("SELECT id_produit,prix_vente,stock,qte_vendu FROM base_donnees WHERE nom_produit=?",(prod,));idp,pf,stk,qv=c.fetchone()
    if stk-(qv+q)<0:raise Exception("Rupture");c.execute("UPDATE base_donnees SET qte_vendu=qte_vendu+? WHERE nom_produit=?",(q,prod));c.execute("INSERT INTO historique (date_vente,id_produit,nom_produit,qte_vendu,prix_fixe,prix_vendu,statut) VALUES (?,?,?,?,?,?,?)",(datetime.now().strftime("%d/%m/%Y %H:%M"),idp,prod,q,pf,pv,"Vente Faîte"));c.execute("SELECT stock,qte_vendu FROM base_donnees WHERE nom_produit=?",(prod,));s,qv2=c.fetchone();rest=s-qv2
    if rest<=10:c.execute("INSERT OR REPLACE INTO alerte VALUES (NULL,?,?,?)",(datetime.now().strftime("%d/%m/%Y %H:%M"),prod,rest))
    else:c.execute("DELETE FROM alerte WHERE nom_produit=?",(prod,));conn.commit();conn.close();pop.dismiss();self.lbl.text=f"Vente OK:{prod} x{q}"
   except Exception as e:Popup(title="Erreur",content=Label(text=str(e)),size_hint=(0.8,0.3)).open()
  b.add_widget(Button(text="Valider",background_color=get_color_from_hex("#27AE60"),on_press=val));pop=Popup(title="Vente Stock Restant",content=b,size_hint=(0.9,0.8));pop.open()
def credit(self,*a):
  b=BoxLayout(orientation='vertical',spacing=5,padding=10);cl=TextInput(hint_text="Nom Client",size_hint_y=0.12);pr=TextInput(hint_text="Produit ex: Effet personnel (chambre)",size_hint_y=0.12);qt=TextInput(hint_text="Qte? 0/Aucun perso - VIDE=Aucun",size_hint_y=0.12);tel=TextInput(hint_text="Telephone",size_hint_y=0.12);mt=TextInput(hint_text="Montant FG",input_filter='float',size_hint_y=0.12)
  for w in [cl,pr,qt,tel,mt]:b.add_widget(w)
  def val(*x):
   try:c=cl.text.strip();p=pr.text.strip();q=qt.text.strip() or "Aucun";t=tel.text.strip() or "-";m=float(mt.text)
   except:Popup(title="Erreur",content=Label(text="Champs invalides"),size_hint=(0.8,0.3)).open();return
   conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("INSERT INTO credit (date_enregistrement,nom_produit,qte_credit,nom_client,montant_credit,somme_restant,tel_client,situation) VALUES (?,?,?,?,?,?,?,?)",(datetime.now().strftime("%d/%m/%Y %H:%M"),p,q,c,m,m,t,"Dette faîte"));conn.commit();conn.close();pop.dismiss();self.lbl.text=f"Credit:{c}-{p} Qte:{q} Tel:{t}"
  b.add_widget(Button(text="Valider Credit",background_color=get_color_from_hex("#D35400"),on_press=val));pop=Popup(title="Credit Qte+Tel",content=b,size_hint=(0.9,0.85));pop.open()
def annuler(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT DISTINCT nom_produit FROM historique WHERE statut!='Vente annuler'");liste=[r[0] for r in cur.fetchall()];conn.close()
  if not liste:Popup(title="Erreur",content=Label(text="Aucune vente"),size_hint=(0.8,0.3)).open();return
  b=BoxLayout(orientation='vertical',padding=10,spacing=5);sp=Spinner(text=liste[0],values=liste,size_hint_y=0.2);qte=TextInput(hint_text="Qte annuler",input_filter='float',size_hint_y=0.2);b.add_widget(sp);b.add_widget(qte)
  def val(*x):
   try:prod=sp.text;q=float(qte.text);conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("SELECT id FROM historique WHERE LOWER(nom_produit)=LOWER(?) AND qte_vendu=? AND statut!='Vente annuler' LIMIT 1",(prod,q));r=c.fetchone()
   except:return
   if not r:Popup(title="Erreur",content=Label(text="Non trouve"),size_hint=(0.8,0.3)).open();return
   c.execute("UPDATE historique SET statut='Vente annuler' WHERE id=?",(r[0],));c.execute("UPDATE base_donnees SET qte_vendu=qte_vendu-? WHERE LOWER(nom_produit)=LOWER(?)",(q,prod));conn.commit();conn.close();pop.dismiss()
  b.add_widget(Button(text="Valider",background_color=get_color_from_hex("#E74C3C"),on_press=val));pop=Popup(title="Annuler",content=b,size_hint=(0.8,0.6));pop.open()
def ajout_choix(self,*a):
  b=BoxLayout(orientation='vertical',spacing=10,padding=10);b.add_widget(Button(text="Nouveau Produit",background_color=get_color_from_hex("#2980B9"),on_press=lambda x:[pop.dismiss(),self.add_prod()]));b.add_widget(Button(text="Augmenter Stock",background_color=get_color_from_hex("#27AE60"),on_press=lambda x:[pop.dismiss(),self.add_stock()]));pop=Popup(title="Choix",content=b,size_hint=(0.8,0.4));pop.open()
def add_prod(self,*a):
  b=BoxLayout(orientation='vertical',spacing=5,padding=10);nom=TextInput(hint_text="Nom",size_hint_y=0.2);stk=TextInput(hint_text="Stock",input_filter='float',size_hint_y=0.2);pa=TextInput(hint_text="Prix achat",input_filter='float',size_hint_y=0.2);pv=TextInput(hint_text="Prix vente",input_filter='float',size_hint_y=0.2)
  for w in [nom,stk,pa,pv]:b.add_widget(w)
  def val(*x):
   try:conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("SELECT MAX(id_produit) FROM base_donnees");mx=c.fetchone()[0];nid=1 if mx is None else mx+1;c.execute("INSERT INTO base_donnees (date_enregistrement,id_produit,nom_produit,prix_revient,prix_vente,stock) VALUES (?,?,?,?,?,?)",(date.today().strftime("%d/%m/%Y"),nid,nom.text,float(pa.text),float(pv.text),float(stk.text)));conn.commit();conn.close();pop.dismiss()
   except Exception as e:Popup(title="Erreur",content=Label(text=str(e)),size_hint=(0.8,0.3)).open()
  b.add_widget(Button(text="Creer",on_press=val));pop=Popup(title="Nouveau",content=b,size_hint=(0.9,0.7));pop.open()
def add_stock(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT nom_produit FROM base_donnees");liste=[r[0] for r in cur.fetchall()];conn.close()
  if not liste:return
  b=BoxLayout(orientation='vertical',padding=10,spacing=5);sp=Spinner(text=liste[0],values=liste,size_hint_y=0.2);qte=TextInput(hint_text="Qte ajouter",input_filter='float',size_hint_y=0.2);b.add_widget(sp);b.add_widget(qte)
  def val(*x):conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("UPDATE base_donnees SET stock=stock+? WHERE nom_produit=?",(float(qte.text),sp.text));conn.commit();conn.close();pop.dismiss()
  b.add_widget(Button(text="Valider",on_press=val));pop=Popup(title="Stock",content=b,size_hint=(0.8,0.6));pop.open()
def payer(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT DISTINCT nom_client FROM credit WHERE situation!='Rembourser 100%'");liste=[r[0] for r in cur.fetchall()];conn.close()
  if not liste:Popup(title="Erreur",content=Label(text="Aucun client"),size_hint=(0.8,0.3)).open();return
  b=BoxLayout(orientation='vertical',padding=10,spacing=5);sp=Spinner(text=liste[0],values=liste,size_hint_y=0.2);mt=TextInput(hint_text="Montant",input_filter='float',size_hint_y=0.2);b.add_widget(sp);b.add_widget(mt)
  def val(*x):
   try:conn=sqlite3.connect("gestion_magasin.db");c=conn.cursor();c.execute("SELECT id,somme_restant FROM credit WHERE UPPER(nom_client)=UPPER(?) AND situation!='Rembourser 100%' LIMIT 1",(sp.text,));r=c.fetchone();idc,reste=r;p=float(mt.text)
   except:return
   if p>reste:Popup(title="Erreur",content=Label(text="Depasse dette"),size_hint=(0.8,0.3)).open();return
   nst=reste-p;sit="Rembourser 100%" if nst==0 else "Remboursé 1/2";c.execute("UPDATE credit SET somme_payee=somme_payee+?,somme_restant=?,situation=? WHERE id=?",(p,nst,sit,idc));conn.commit();conn.close();pop.dismiss();self.lbl.text=f"Paiement OK reste {fmt_fg(nst)}"
  b.add_widget(Button(text="Payer",background_color=get_color_from_hex("#27AE60"),on_press=val));pop=Popup(title="Payer Dette",content=b,size_hint=(0.8,0.6));pop.open()
def stats(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT date_vente,nom_produit,qte_vendu,prix_vendu,statut FROM historique");hist=cur.fetchall();nj=0;bj=0;bm=0;auj=date.today().strftime("%d/%m/%Y")
  for dt,pr,q,px,st in hist:
   if "ANNUL" in st.upper():continue
   cur.execute("SELECT prix_revient FROM base_donnees WHERE nom_produit=?",(pr,));rev=cur.fetchone();pa=rev[0] if rev else 0;ben=(px-pa)*q;bm+=ben
   if auj in dt:nj+=1;bj+=ben
  conn.close();Popup(title="Bilan",content=Label(text=f"Date:{datetime.now().strftime('%d/%m %H:%M')}\nVentes:{nj}\nBenef Jour:{fmt_fg(bj)}\nBenef Total:{fmt_fg(bm)}"),size_hint=(0.85,0.5)).open()
def show_magasin(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT nom_produit,stock,qte_vendu,prix_vente FROM base_donnees");rows=cur.fetchall();conn.close();txt="MAGASIN:\n"
  for n,s,qv,pv in rows:txt+=f"- {n} | Rest:{fmt_int(s-qv)} | {fmt_fg(pv)}\n"
  self.lbl.text=txt or "Vide";self.lbl.height=max(800,len(rows)*30+100)
def show_hist(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT date_vente,nom_produit,qte_vendu,statut FROM historique ORDER BY id DESC LIMIT 100");rows=cur.fetchall();conn.close();txt="HISTORIQUE Faite=BLANC Annuler=ROUGE:\n"
  for dt,n,q,st in rows:tag="[ROUGE ANNULER]" if "annuler" in st.lower() else "[BLANC FAITE]";txt+=f"{tag} {dt} {n} x{fmt_int(q)} {st}\n"
  self.lbl.text=txt;self.lbl.height=max(800,len(rows)*25+100)
def show_credits(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT nom_produit,qte_credit,nom_client,tel_client,situation,montant_credit FROM credit");rows=cur.fetchall();conn.close();txt="CREDITS Dette=BLANC 1/2=JAUNE 100%=VERT:\n"
  for prod,qte,cl,tel,sit,mt in rows:
   if "100%" in sit:col="[VERT]";elif "1/2" in sit:col="[JAUNE]";else:col="[BLANC]";txt+=f"{col} {cl}|{prod}|Qte:{qte or 'Aucun'}|Tel:{tel}|{sit}|{fmt_fg(mt)}\n"
  self.lbl.text=txt or "Aucun";self.lbl.height=max(800,len(rows)*30+100)
def show_alerte(self,*a):
  conn=sqlite3.connect("gestion_magasin.db");cur=conn.cursor();cur.execute("SELECT nom_produit,stock_restant,date_alerte FROM alerte");rows=cur.fetchall();conn.close();txt="ALERTE <=10:\n"
  for n,s,d in rows:txt+=f"- {n} Rest:{fmt_int(s)} {d}\n"
  self.lbl.text=txt or "Aucune"
if __name__=="__main__":OBDApp().run()
