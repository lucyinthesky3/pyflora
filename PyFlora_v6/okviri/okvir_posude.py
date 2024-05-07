import io
import tkinter as tk
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PIL import ImageTk, Image

from db.dbManager import Korisnik, Posuda, db_engine
from okviri.framemanager import FrameManager

Session = sessionmaker(bind=db_engine)
session = Session()

class OkvirPosude(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        #brisanje svih widgeta
        for widget in self.winfo_children():
            widget.destroy()

        self.grid(row=1, column=0, sticky="nsew")
        self.grid_propagate(False)

        # Konfigurira tri jednako široka stupca
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        ##############################################
        ##############################################
        my_canvas = tk.Canvas(self)#, bg="blue")
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        my_canvas.rowconfigure(0, weight=1)
        my_canvas.columnconfigure(0, weight=1)

        my_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        second_frame = tk.Frame(my_canvas)#, bg="red")
        second_frame.grid_columnconfigure(0, weight=1)
        second_frame.grid_columnconfigure(1, weight=1)

        my_canvas.create_window((0,0), window=second_frame, anchor=tk.NW)
        ##############################################
        ##############################################      














        lbl_posude_naslov = tk.Label(second_frame, text="POSUDE...", font=("Ink Free", 35))
        lbl_posude_naslov.grid(row=0, column=0, columnspan=2, padx=15, pady=25)

        posude = session.query(Posuda).all()

        print("posude:", len(posude), posude)


        brojac = 1
        redak = 0
        for posuda in posude:
            #print(posuda)

            if brojac%2!=0:
                kolona = 0
                redak += 1
            else:
                kolona = 1
                

            
            frm_posude_prikaz = tk.Frame(second_frame, width=350, height=160, highlightthickness=2, highlightbackground="black")
            frm_posude_prikaz.grid(row=redak, column=kolona, padx=15, pady=15)
            frm_posude_prikaz.grid_columnconfigure(0, weight=2)
            frm_posude_prikaz.grid_columnconfigure(1, weight=4)
            frm_posude_prikaz.grid_columnconfigure(2, weight=1)

            frm_posude_prikaz.grid_propagate(False)

            # lijevi stupac
            #slika = Image.open("fotografije/marguerite.jpg")
            slika = Image.open(io.BytesIO(posuda.biljka.fotografija))
            smanjena_slika = slika.resize((120, 150), Image.ANTIALIAS)
            smanjena_slika_tk = ImageTk.PhotoImage(smanjena_slika)

            lbl_posude_prikaz_fotografija =tk.Label(frm_posude_prikaz, image=smanjena_slika_tk)
            lbl_posude_prikaz_fotografija.image = smanjena_slika_tk
            lbl_posude_prikaz_fotografija.grid(row=0, column=0, rowspan=4)

            # srednji stupac
            lbl_posude_prikaz_naziv_text = tk.Label(frm_posude_prikaz, text="Naziv posude:")
            lbl_posude_prikaz_naziv_text.grid(row=0, column=1)
            lbl_posude_prikaz_naziv = tk.Label(frm_posude_prikaz, text=posuda.naziv)
            lbl_posude_prikaz_naziv.grid(row=1, column=1)
            lbl_posude_prikaz_status_text = tk.Label(frm_posude_prikaz, text="Status:")
            lbl_posude_prikaz_status_text.grid(row=2, column=1)
            lbl_posude_prikaz_status_vlaga = tk.Label(frm_posude_prikaz, text="")
            lbl_posude_prikaz_status_vlaga.grid(row=3, column=1)
            lbl_posude_prikaz_status_temp = tk.Label(frm_posude_prikaz, text="")
            lbl_posude_prikaz_status_temp.grid(row=3, column=2)
            if posuda.zadnja_temperatura and posuda.zadnja_temperatura < posuda.biljka.temperatura:
                #pass#lbl_posude_prikaz_status.configure(text="preniska temp")
                # Load an image using PIL (Pillow)
                image_path = "fotografije/temp.png"
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((30, 30))

                # Convert the PIL image to a Tkinter PhotoImage
                tk_image = ImageTk.PhotoImage(pil_image)

                lbl_posude_prikaz_status_temp.configure(image=tk_image)
                lbl_posude_prikaz_status_temp.image = tk_image

            if posuda.zadnja_vlaga and posuda.zadnja_vlaga < posuda.biljka.vlaga_tla:
                #pass#lbl_posude_prikaz_status.configure(text="preniska temp")
                # Load an image using PIL (Pillow)
                image_path = "fotografije/vlaga.png"
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((30, 30))

                # Convert the PIL image to a Tkinter PhotoImage
                tk_image = ImageTk.PhotoImage(pil_image)

                lbl_posude_prikaz_status_vlaga.configure(image=tk_image)
                lbl_posude_prikaz_status_vlaga.image = tk_image
                
                
            
            #lbl_posude_prikaz_status.grid(row=3, column=1)
            # srednji stupac
            def izbrisi(id):
                Posuda.izbrisi_posudu(id)
                #self.create_widgets()
                FrameManager.restartaj_okvir("okvir_posude", self.master)

            def uredi(id):
                print("UREDUJEM POSUDU S ID-em br.:", id)
                # dodati funkcionalnost update-a posude
                FrameManager.dohvati_okvir("okvir_uredi_posudu").posuda_id = id
                FrameManager.dohvati_okvir("okvir_uredi_posudu").create_widgets()
                FrameManager.prikazi_okvir("okvir_uredi_posudu")

            btn_posude_prikaz_izbrisi = tk.Button(frm_posude_prikaz, text="D", command=lambda id=posuda.id: izbrisi(id))
            btn_posude_prikaz_izbrisi.grid(row=0, column=2)

            btn_posude_prikaz_uredi = tk.Button(frm_posude_prikaz, text="U", command=lambda id=posuda.id: uredi(id))
            btn_posude_prikaz_uredi.grid(row=1, column=2)

            brojac += 1

        
        # nakon petlje koja prikazuje posude
            
        

        if kolona == 0:
            kolona = 1
        else:
            kolona = 0
            redak+=1

        frm_posude_prikaz = tk.Frame(second_frame, width=350, height=160, highlightthickness=2, highlightbackground="black")
        frm_posude_prikaz.grid(row=redak, column=kolona, padx=15, pady=15)
        frm_posude_prikaz.grid_columnconfigure(0, weight=1)
        frm_posude_prikaz.grid_propagate(False)
        
        btn_posude_prikaz_nova_posuda = tk.Button(frm_posude_prikaz, text="Nova posuda", command=lambda : FrameManager.prikazi_okvir("okvir_nova_posuda"))
        btn_posude_prikaz_nova_posuda.grid(row=0, column=0, pady=60)
