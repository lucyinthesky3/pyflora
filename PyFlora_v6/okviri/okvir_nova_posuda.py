import tkinter as tk
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PIL import ImageTk, Image

from db.dbManager import Biljka, Posuda, db_engine
from okviri.framemanager import FrameManager

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirNovaPosuda(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        self.grid(row=1, column=0, sticky="we")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        def upisi():
            indeks_naziva_biljke = nazivi_biljaka.index(om_odabrana_biljka.get())

            nova_posuda = Posuda(ent_nova_posuda_naziv.get(), idevi_biljaka[indeks_naziva_biljke])
            session.add(nova_posuda)
            session.commit()
            ent_nova_posuda_naziv.delete(0, tk.END)
            #ent_nova_posuda_id_biljke.delete(0, tk.END)

            #FrameManager.dohvati_okvir("okvir_posude").create_widgets()
            #FrameManager.prikazi_okvir("okvir_posude")
            FrameManager.restartaj_okvir("okvir_posude", self.master)


        lbl_nova_posuda_naslov = tk.Label(self, text="Nova posuda", font=("Ink Free", 35))
        lbl_nova_posuda_naslov.grid(row=0, column=0, columnspan=2, padx=15, pady=25)
        lbl_nova_posuda_naziv = tk.Label(self, text="Naziv posude: ")
        lbl_nova_posuda_naziv.grid(row=1, column=0, pady=15)
        ent_nova_posuda_naziv = tk.Entry(self)
        ent_nova_posuda_naziv.grid(row=1, column=1, pady=15)

        lbl_nova_posuda_id_biljke = tk.Label(self, text="Biljka: ")
        lbl_nova_posuda_id_biljke.grid(row=2, column=0, pady=15)
        #ent_nova_posuda_id_biljke = tk.Entry(self)
        #ent_nova_posuda_id_biljke.grid(row=2, column=1, pady=15)

        nazivi_biljaka = []
        idevi_biljaka = []
        biljke = session.query(Biljka).all()
        for biljka in biljke:
            nazivi_biljaka.append(biljka.naziv)
            idevi_biljaka.append(biljka.id)
        
        #indeks_ida_biljke = idevi_biljaka.index(dohvacena_posuda.id_biljke)


        om_odabrana_biljka = tk.StringVar(self)
        om_odabrana_biljka.set(nazivi_biljaka[0])

        om_uredi_posudu_biljke = tk.OptionMenu(self, om_odabrana_biljka, *nazivi_biljaka)
        om_uredi_posudu_biljke.config(width=10)
        om_uredi_posudu_biljke.grid(row=2, column=1, pady=15)

        btn_nova_posuda_spremi = tk.Button(self, text="SPREMI", command=upisi)
        btn_nova_posuda_spremi.grid(row=3, column=0, columnspan=2, padx=15, pady=25)