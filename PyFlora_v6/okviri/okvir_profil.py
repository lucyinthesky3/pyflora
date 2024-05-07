import tkinter as tk
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PIL import ImageTk, Image

from db.dbManager import Korisnik, Posuda, db_engine
from okviri.framemanager import FrameManager

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirProfil(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.master = master
        self.create_widgets()

    def create_widgets(self):

        self.grid(row=1, column=0, sticky="we")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        lbl_profil_naslov = tk.Label(self, text="PROFIL...", font=("Ink Free", 35))
        lbl_profil_naslov.grid(row=0, column=0, columnspan=2, padx=15, pady=25)

        btn_profil_odjava = tk.Button(self, text="ODJAVA", command=FrameManager.odjava)
        btn_profil_odjava.grid(row=1, column=0, columnspan=2, padx=15, pady=25)