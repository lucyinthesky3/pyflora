from db.dbManager import Korisnik

class FrameManager:

    boja_aktivnog_zapisa = "lightgreen"

    okviri = {} # dictionary svih kreiranih okvira
    
    @staticmethod # slicno kao i classmethod dekorator ali se ne prenosi instanca klase (nema cls kao parametar)
    def dodaj_okvir(naziv, okvir):
        FrameManager.okviri.update({naziv: okvir})
        
    @staticmethod
    def prikazi_okvir(naziv_okvira):
        okvir = FrameManager.okviri.get(naziv_okvira)
        okvir.tkraise()

    @staticmethod
    def prijava():
        # autorizacija korisnika
        uneseno_korisnicko_ime = FrameManager.dohvati_vrijednost_emtry_widgeta_iz_okvira("okvir_prijava", "ent_prijava_korisnicko_ime")
        unesena_zaporka = FrameManager.dohvati_vrijednost_emtry_widgeta_iz_okvira("okvir_prijava", "ent_prijava_zaporka")

        print("PRIJAVA", uneseno_korisnicko_ime, unesena_zaporka)

        if Korisnik.korisnik_postoji_u_bazi(uneseno_korisnicko_ime, unesena_zaporka):
            #autorizacija korisnika uspješna
            FrameManager.prikazi_okvir("okvir_posude")
            FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_pyfloraposuda")
            FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_nova_biljka")
            FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_mojprofil")

            FrameManager.dohvati_widget_iz_okvira("okvir_prijava", "ent_prijava_korisnicko_ime").delete(0, 'end')
            FrameManager.dohvati_widget_iz_okvira("okvir_prijava", "ent_prijava_zaporka").delete(0, 'end')
            FrameManager.postavi_tekst_widgetu_iz_okvira("okvir_prijava", "lbl_prijava_greska", "")

        
        else:
            #autorizacija korisnika neuspješna
            FrameManager.postavi_tekst_widgetu_iz_okvira("okvir_prijava", "lbl_prijava_greska", "Ne postoji korisnik s tim korisničkim imenom i zaporkom")


    @staticmethod
    def odjava():
        FrameManager.prikazi_okvir("okvir_prijava")
        FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_pyfloraposuda", False)
        FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_nova_biljka", False)
        FrameManager.prikazi_widget_iz_okvira("okvir_zaglavlje", "btn_zaglavlje_mojprofil", False)
        

    @staticmethod
    def dohvati_okvir(naziv_okvira):
        return FrameManager.okviri.get(naziv_okvira)

    @staticmethod
    def dohvati_widget_iz_okvira(naziv_okvira, naziv_widgeta):
        dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
        for widget in dohvaceni_okvir.winfo_children():
            if widget.winfo_name() == naziv_widgeta:
                return widget
    
    @staticmethod
    def dohvati_vrijednost_emtry_widgeta_iz_okvira(naziv_okvira, naziv_widgeta):
        dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
        for widget in dohvaceni_okvir.winfo_children():
            if widget.winfo_name() == naziv_widgeta:
                return widget.get()
            
    @staticmethod
    def postavi_tekst_widgetu_iz_okvira(naziv_okvira, naziv_widgeta, novi_tekst_widgeta):
        dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
        for widget in dohvaceni_okvir.winfo_children():
            if widget.winfo_name() == naziv_widgeta:
                widget.config(text=novi_tekst_widgeta)

    
    @staticmethod
    def prikazi_widget_iz_okvira(naziv_okvira, naziv_widgeta, prikaz=True):
        dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
        for widget in dohvaceni_okvir.winfo_children():
            if widget.winfo_name() == naziv_widgeta:
                if prikaz:
                    widget.grid()
                else:
                    widget.grid_remove()


    @staticmethod
    def restartaj_okvir(naziv_okvira, master):
        print("restartam okvir")

        stari_okvir = FrameManager.dohvati_okvir(naziv_okvira)

        novi_okvir = type(stari_okvir)(master, height=580, padx=15, pady=15)
        FrameManager.dodaj_okvir("okvir_posude", novi_okvir)

        FrameManager.prikazi_okvir("okvir_posude")
    
        
    # @staticmethod
    # def dohvati_widget_iz_okvira(naziv_okvira, naziv_widgeta):
    #     dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
    #     for widget in dohvaceni_okvir.winfo_children():
    #         if widget.winfo_name() == naziv_widgeta:
    #             return widget
            
    # @staticmethod
    # def postavi_bg_boju_widgeta(naziv_okvira, naziv_widgeta, boja=None):
    #     dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
    #     for widget in dohvaceni_okvir.winfo_children():
    #         if widget.winfo_name() == naziv_widgeta:
    #             if boja:
    #                 widget.configure(bg=boja)
    #             else:
    #                 widget.configure(bg=widget.master.cget('bg'))
                    
    # @staticmethod
    # def postavi_bg_boju_grupe_widgeta(naziv_okvira, prefiks_grupe_widgeta, boja=None):
    #     dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
    #     for widget in dohvaceni_okvir.winfo_children():
    #         if widget.winfo_name()[:len(prefiks_grupe_widgeta)] == prefiks_grupe_widgeta:
    #             if boja:
    #                 widget.configure(bg=boja)
    #             else:
    #                 widget.configure(bg=widget.master.cget('bg'))

    # @staticmethod
    # def prikazi_grupu_widgeta(naziv_okvira, prefiks_grupe_widgeta, prikaz=True):
    #     dohvaceni_okvir = FrameManager.dohvati_okvir(naziv_okvira)
    #     for widget in dohvaceni_okvir.winfo_children():
    #         if widget.winfo_name()[:len(prefiks_grupe_widgeta)] == prefiks_grupe_widgeta:
    #             if prikaz:
    #                 widget.grid()
    #             else:
    #                 widget.grid_remove()

    