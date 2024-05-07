import tkinter as tk
from okviri.framemanager import FrameManager

#from db.dbManager import Tvrtka, Zaposlenik, db_engine

class OkvirZaglavlje(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        
        self.grid(row=0, column=0, sticky="we")
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # lbl_zaglavlje_pyfloraposuda = tk.Label(self, text="PyFloraPosuda", name="lbl_zaglavlje_pyfloraposuda")
        # lbl_zaglavlje_pyfloraposuda.grid(row=1, column=0)
        # lbl_zaglavlje_pyfloraposuda.grid_remove()

        btn_zaglavlje_pyfloraposuda = tk.Button(self, text="PyFloraPosuda", name="btn_zaglavlje_pyfloraposuda", command=lambda: FrameManager.prikazi_okvir("okvir_posude"))
        btn_zaglavlje_pyfloraposuda.grid(row=1, column=0)
        btn_zaglavlje_pyfloraposuda.grid_remove()

        btn_zaglavlje_nova_biljka = tk.Button(self, text="Nova Biljka", name="btn_zaglavlje_nova_biljka", command=lambda: FrameManager.prikazi_okvir("okvir_nova_biljka"))
        btn_zaglavlje_nova_biljka.grid(row=1, column=1)
        btn_zaglavlje_nova_biljka.grid_remove()

        btn_zaglavlje_mojprofil = tk.Button(self, text="Moj profil", name="btn_zaglavlje_mojprofil", command=lambda: FrameManager.prikazi_okvir("okvir_profil"))
        btn_zaglavlje_mojprofil.grid(row=1, column=2)
        btn_zaglavlje_mojprofil.grid_remove()