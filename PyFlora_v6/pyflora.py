# dodati mogucnost unosa nove biljke (bez slike...)


import tkinter as tk
from okviri.framemanager import FrameManager
from okviri.okvir_nova_biljka import OkvirNovaBiljka
from okviri.okvir_nova_posuda import OkvirNovaPosuda
from okviri.okvir_posude import OkvirPosude
from okviri.okvir_prijava import OkvirPrijava
from okviri.okvir_profil import OkvirProfil
from okviri.okvir_uredi_posudu import OkvirUrediPosudu
from okviri.okvir_zaglavlje import OkvirZaglavlje

from mqtt.mqttsubscriber import MqttSubscriber

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from db.dbManager import Posuda, db_engine

Session = sessionmaker(bind=db_engine)
session = Session()

root = tk.Tk()
root.geometry("1200x650+300+100")
root.title("Contact Manager")
root.grid_columnconfigure(0, weight=1)


###################################################
# Kreiranje okvira 

frm_zaglavlje = OkvirZaglavlje(root, height=70, padx=15, pady=15, bg="grey")
FrameManager.dodaj_okvir("okvir_zaglavlje", frm_zaglavlje)

frm_prijava = OkvirPrijava(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_prijava", frm_prijava)

frm_posude = OkvirPosude(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_posude", frm_posude)

frm_profil = OkvirProfil(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_profil", frm_profil)

frm_nova_posuda = OkvirNovaPosuda(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_nova_posuda", frm_nova_posuda)

frm_uredi_posudu = OkvirUrediPosudu(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_uredi_posudu", frm_uredi_posudu)

frm_nova_biljka = OkvirNovaBiljka(root, height=580, padx=15, pady=15)#, bg="grey")
FrameManager.dodaj_okvir("okvir_nova_biljka", frm_nova_biljka)

#prebacuje inicijalno u prvi plan početni okvir
FrameManager.prikazi_okvir("okvir_prijava")

# za testiranje - bez autorizacije
#FrameManager.prikazi_okvir("okvir_posude")

posude = session.query(Posuda).all()

for posuda in posude:
    mqtt = MqttSubscriber(posuda.id, posuda.naziv)
    mqtt.start()


root.mainloop()