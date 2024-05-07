import io
import tkinter as tk
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PIL import ImageTk, Image

from db.dbManager import Biljka, db_engine
from okviri.framemanager import FrameManager
from tkinter import filedialog

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirNovaBiljka(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.nova_biljka = None
        self.create_widgets()

    def create_widgets(self):

        self.grid(row=1, column=0, sticky="we")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        def upisi():
            #nova_biljka = Biljka(ent_nova_biljka_naziv.get(), ent_nova_biljka_temperatura.get(), ent_nova_biljka_vlaga_tla.get(), ent_nova_biljka_supstrat.get())
            session.add(self.nova_biljka)
            session.commit()
            
            # ent_nova_biljka_naziv.delete(0, tk.END)
            # ent_nova_biljka_temperatura.delete(0, tk.END)
            # ent_nova_biljka_vlaga_tla.delete(0, tk.END)
            # ent_nova_biljka_supstrat.delete(0, tk.END)
            

            #FrameManager.dohvati_okvir("okvir_posude").create_widgets()
            #FrameManager.prikazi_okvir("okvir_posude")
            #FrameManager.restartaj_okvir("okvir_posude", self.master)

        def dodaj_sliku():
            filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
            if filepath:
                image = Image.open(filepath)
                image = image.resize((120,150))

                image_tk = ImageTk.PhotoImage(image)
                lbl_prikaz_slike.config(image=image_tk)
                lbl_prikaz_slike.image = image_tk

                btn_nova_biljka_spremi.grid()

                def convertToBinaryData(filename):
                    # Convert digital data to binary format
                    with open(filename, 'rb') as file:
                        blobData = file.read()
                    return blobData

                slika = convertToBinaryData(filepath)

                stream = io.BytesIO(slika)

                # Open the `io.BytesIO` object as a PIL image
                pil_image = Image.open(stream)

                pil_image = pil_image.resize((120,150))

                stream = io.BytesIO()

                # Save the PIL image to the stream
                pil_image.save(stream, format='PNG')  # Choose the appropriate format (e.g., PNG, JPEG)

                # Retrieve the bytes object from the stream
                blob_slika_biljke = stream.getvalue()

                self.nova_biljka = Biljka(ent_nova_biljka_naziv.get(), ent_nova_biljka_temperatura.get(), ent_nova_biljka_vlaga_tla.get(), ent_nova_biljka_supstrat.get(), blob_slika_biljke)






        lbl_nova_posuda_naslov = tk.Label(self, text="Nova biljka", font=("Ink Free", 35))
        lbl_nova_posuda_naslov.grid(row=0, column=0, columnspan=3, padx=15, pady=25)
        lbl_nova_biljka_naziv = tk.Label(self, text="Naziv biljke: ")
        lbl_nova_biljka_naziv.grid(row=1, column=0, pady=15)
        ent_nova_biljka_naziv = tk.Entry(self)
        ent_nova_biljka_naziv.grid(row=1, column=1, pady=15)

        lbl_nova_biljka_temperatura = tk.Label(self, text="Temperatura: ")
        lbl_nova_biljka_temperatura.grid(row=2, column=0, pady=15)
        ent_nova_biljka_temperatura = tk.Entry(self)
        ent_nova_biljka_temperatura.grid(row=2, column=1, pady=15)

        lbl_nova_biljka_vlaga_tla = tk.Label(self, text="Vlaga tla: ")
        lbl_nova_biljka_vlaga_tla.grid(row=3, column=0, pady=15)
        ent_nova_biljka_vlaga_tla = tk.Entry(self)
        ent_nova_biljka_vlaga_tla.grid(row=3, column=1, pady=15)

        lbl_nova_biljka_supstrat = tk.Label(self, text="Supstrat: ")
        lbl_nova_biljka_supstrat.grid(row=4, column=0, pady=15)
        ent_nova_biljka_supstrat = tk.Entry(self)
        ent_nova_biljka_supstrat.grid(row=4, column=1, pady=15)

        btn_dodaj_sliku = tk.Button(self, text="Uploadaj sliku", command=dodaj_sliku)
        btn_dodaj_sliku.grid(row=5, column=1, pady=15)

        lbl_prikaz_slike = tk.Label(self)
        lbl_prikaz_slike.grid(row=1, column=2, rowspan=5)


        btn_nova_biljka_spremi = tk.Button(self, text="SPREMI", command=upisi)
        btn_nova_biljka_spremi.grid(row=6, column=0, columnspan=2, padx=15, pady=25)
        btn_nova_biljka_spremi.grid_remove()