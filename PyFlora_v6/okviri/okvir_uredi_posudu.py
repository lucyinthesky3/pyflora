import io
import tkinter as tk
from tkinter import scrolledtext
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PIL import ImageTk, Image

from db.dbManager import Biljka, Ocitanje, Posuda, db_engine
from okviri.framemanager import FrameManager

import pandas
import matplotlib.pyplot as plt

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirUrediPosudu(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.master = master
        self.posuda_id = None
        #self.create_widgets()

    def create_widgets(self):

        dohvacena_posuda = session.query(Posuda).filter_by(id=self.posuda_id).one_or_none()

        self.grid(row=1, column=0, sticky="we")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        def upisi():
            
            dohvacena_posuda.naziv = ent_uredi_posudu_naziv.get()
            #dohvacena_posuda.id_biljke = ent_uredi_posudu_id_biljke.get()

            #print(om_odabrana_biljka.get())
            indeks_naziva_biljke = nazivi_biljaka.index(om_odabrana_biljka.get())

            dohvacena_posuda.id_biljke = idevi_biljaka[indeks_naziva_biljke]


            session.commit()
            
            ent_uredi_posudu_naziv.delete(0, tk.END)
            #ent_uredi_posudu_id_biljke.delete(0, tk.END)

            #FrameManager.dohvati_okvir("okvir_posude").create_widgets()
            #FrameManager.prikazi_okvir("okvir_posude")
            FrameManager.restartaj_okvir("okvir_posude", self.master)


        lbl_uredi_posudu_naslov = tk.Label(self, text="Uređivanje posude", font=("Ink Free", 35))
        lbl_uredi_posudu_naslov.grid(row=0, column=0, columnspan=2, padx=15, pady=15)
        lbl_uredi_posudu_naziv = tk.Label(self, text="Naziv posude: ")
        lbl_uredi_posudu_naziv.grid(row=1, column=0, pady=15)
        ent_uredi_posudu_naziv = tk.Entry(self)
        ent_uredi_posudu_naziv.insert(0, dohvacena_posuda.naziv)
        ent_uredi_posudu_naziv.grid(row=1, column=1, pady=15)

        lbl_uredi_posudu_id_biljke = tk.Label(self, text="Biljka: ")
        lbl_uredi_posudu_id_biljke.grid(row=2, column=0, pady=15)
        
        # ent_uredi_posudu_id_biljke = tk.Entry(self)
        # ent_uredi_posudu_id_biljke.grid(row=2, column=1, pady=15)
        # ent_uredi_posudu_id_biljke.insert(0, dohvacena_posuda.id_biljke)
    	
        nazivi_biljaka = []
        idevi_biljaka = []
        biljke = session.query(Biljka).all()
        for biljka in biljke:
            nazivi_biljaka.append(biljka.naziv)
            idevi_biljaka.append(biljka.id)
        
        indeks_ida_biljke = idevi_biljaka.index(dohvacena_posuda.id_biljke)


        om_odabrana_biljka = tk.StringVar(self)
        om_odabrana_biljka.set(nazivi_biljaka[indeks_ida_biljke])

        om_uredi_posudu_biljke = tk.OptionMenu(self, om_odabrana_biljka, *nazivi_biljaka)
        om_uredi_posudu_biljke.config(width=10)
        om_uredi_posudu_biljke.grid(row=2, column=1, pady=15)
        
        btn_uredi_posudu_spremi = tk.Button(self, text="SPREMI", command=upisi)
        btn_uredi_posudu_spremi.grid(row=3, column=0, columnspan=2, padx=15, pady=5)

        #############################################################################

        ocitanja = dohvacena_posuda.ocitanja

        if ocitanja:

        
            def on_scroll(*args):
                text.yview(*args)

            second_frame = tk.Frame(self)
            second_frame.grid(row=4, column=0, padx=15)#, pady=25)

            # Create a Text widget
            text = scrolledtext.ScrolledText(second_frame, wrap=tk.WORD, width=40, height=10)
            text.pack(expand=True, fill='both')

            # Create a vertical scrollbar and associate it with the Text widget
            scrollbar = tk.Scrollbar(second_frame, command=on_scroll)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text.config(yscrollcommand=scrollbar.set)

            for ocitanje in ocitanja:
                text.insert(tk.END, ocitanje)
                text.insert(tk.END, "\n")

            #############################################################################
                
            df = pandas.read_sql_query(
                sql = session.query(Ocitanje.vrijeme, Ocitanje.vrijednost).filter(Ocitanje.id_posude == self.posuda_id).statement,
                con = db_engine
            )

            #print("type(df)", type(df))

            #print("df", df)

            

            # prikazati podatke iz DF-a grafikonom korištenjem modula matplotlib

            # Plotting a bar graph using matplotlib
            
            plt.title('Temperatura u posudi ' + dohvacena_posuda.naziv)
            plt.xlabel('Vrijeme')
            plt.ylabel('Temperatura')
            #plt.show()

            plt.rcParams['figure.figsize'] = [5, 3]

            df.plot(kind='bar', x='vrijeme', y='vrijednost', legend=False)

            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png')

            im = Image.open(img_buf)
            #im.show(title="My Image")

            tk_image = ImageTk.PhotoImage(im)

            img_buf.close()

            label = tk.Label(self, image=tk_image)
            #label.config(image=tk_image)
            label.image = tk_image
            label.grid(row=4, column=1, padx=15, pady=25)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # # prikazati podatke iz DF-a grafikonom korištenjem modula matplotlib

            # # Plotting a bar graph using matplotlib
            # #df.plot(kind='bar', x='vrijeme', y='vrijednost', legend=False)
            
            # #plt.show()

            # # plotting a line plot after changing it's width and height 
            # # f = plt.figure() 
            # # f.set_figwidth(6.4) 
            # # f.set_figheight(4.8)

            

            # #plt.figure(figsize=(4, 2))
            # plt.title('Temperatura u posudi ' + dohvacena_posuda.naziv)
            # plt.xlabel('Vrijeme')
            # plt.ylabel('Temperatura')

            # df.plot(kind='bar', x='vrijeme', y='vrijednost', legend=False)
            
            

            # #plt.rcParams['figure.figsize'] = [5, 3]

            # # 
            # #plt.show()

            # img_buf = io.BytesIO()
            # plt.savefig(img_buf, format='png')

            # im = Image.open(img_buf)
            # #im.show(title="My Image")

            # tk_image = ImageTk.PhotoImage(im)

            # img_buf.close()

            # label = tk.Label(self, image=tk_image)
            # #label.config(image=tk_image)
            # label.image = tk_image
            # label.grid(row=4, column=1, padx=15)#, pady=25)