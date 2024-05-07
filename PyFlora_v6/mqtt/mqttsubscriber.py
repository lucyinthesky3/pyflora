from threading import Thread
import paho.mqtt.client as mqtt
from okviri.framemanager import FrameManager
#from time import sleep
from datetime import datetime
import tkinter as tk

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from db.dbManager import Posuda, Ocitanje, db_engine

Session = sessionmaker(bind=db_engine)
session = Session()


class MqttSubscriber(Thread):
    def __init__(self, id_posude, posuda_koja_salje):
        super().__init__()
        self.id_posude = id_posude
        self.posuda_koja_salje = posuda_koja_salje

    def on_message(self, client, userdata, message):
        podaci = str(message.payload.decode("utf-8"))
        
        print("PRIMLJENI PODACI: ", podaci)
        
        try:
          
            vrsta_ocitanja = podaci[:podaci.index(" ")]
            print("vrsta_ocitanja", vrsta_ocitanja)

            vrijednost = float(podaci[podaci.index(" ")+1:])
            print("temp", vrijednost)

            # datetime object containing current date and time
            now = datetime.now()
            
            print("now =", now)

            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string)

            novo_ocitanje = Ocitanje(dt_string, vrijednost, vrsta_ocitanja, self.id_posude)
            session.add(novo_ocitanje)

            dohvacena_posuda = session.query(Posuda).filter_by(id=self.posuda_id).one_or_none()
            if vrsta_ocitanja == "temperatura":
                dohvacena_posuda.zadnja_temperatura = vrijednost
            else:
                dohvacena_posuda.zadnja_vlaga = vrijednost

            session.commit()

        except:
            print("NEMA TEMPERATURE")

    def run(self):
        #mqttBroker = "45.143.217.198"
        #mqttBroker = "broker.hivemq.com"
        #mqttBroker = "test.mosquitto.org"
        mqttBroker = "localhost"


        try:
            #client = mqtt.Client("WindowsSubscribe"+self.posuda_koja_salje)
            client = mqtt.Client(self.posuda_koja_salje)
            client.connect(mqttBroker) 


            client.loop_start()
            print("loop POČETAK")

            client.subscribe(self.posuda_koja_salje)

            #client.on_message=self.on_message

        except ConnectionRefusedError as e:
            #FrameManager.postavi_tekst_widgetu_iz_okvira("okvir_tlocrt", "lbl_dnevna_soba_temperatura", "MQTT broker nedostupan")
            print("Uhvacena greska: ConnectionRefusedError", e)
        
        except Exception as e:
            #FrameManager.postavi_tekst_widgetu_iz_okvira("okvir_tlocrt", "lbl_dnevna_soba_temperatura", "MQTT greška")
            print("Uhvacena greska:", e)

        else:
            client.on_message=self.on_message
            print("MQTT poruka primljena")


        #sleep(100)
        #print("loop KRAJ")
        #client.loop_stop()