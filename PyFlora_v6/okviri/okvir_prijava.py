import tkinter as tk
from okviri.framemanager import FrameManager

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from db.dbManager import Korisnik, db_engine

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirPrijava(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.master = master
        self.create_widgets()

    def create_widgets(self):

        self.grid(row=1, column=0, sticky="we")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        self.grid_columnconfigure(0, weight=1)

        lbl_naslov = tk.Label(self, text="Prijava", font=("Ink Free", 35))
        lbl_naslov.grid(row=0, column=0, padx=15, pady=50)

        lbl_prijava_korisnicko_ime = tk.Label(self, text="Korisničko ime: ")
        lbl_prijava_korisnicko_ime.grid(row=2, column=0, pady=15)

        ent_prijava_korisnicko_ime = tk.Entry(self, name="ent_prijava_korisnicko_ime")
        ent_prijava_korisnicko_ime.grid(row=3, column=0, pady=15)

        lbl_prijava_lozinka = tk.Label(self, text="Zaporka: ")
        lbl_prijava_lozinka.grid(row=5, column=0, pady=15)

        ent_prijava_zaporka = tk.Entry(self, show="*", name="ent_prijava_zaporka")
        ent_prijava_zaporka.grid(row=6, column=0, pady=15)

        btn_prijava_podnesi = tk.Button(self, text="Prijava", command=FrameManager.prijava)
        btn_prijava_podnesi.grid(row=8, column=0, pady=15)

        lbl_prijava_greska = tk.Label(self, text="", name="lbl_prijava_greska", fg="red")
        lbl_prijava_greska.grid(row=9, column=0, pady=15)









    
