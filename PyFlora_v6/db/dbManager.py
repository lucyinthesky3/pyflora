import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

#from okviri.framemanager import FrameManager

Base = declarative_base()

# otvara koenkciju prema bazi podataka
db_engine = db.create_engine('sqlite:///PyFloraDB.db')#, echo=True)
Session = sessionmaker(bind=db_engine)
session = Session()

class Korisnik(Base):
    __tablename__ = "korisnici"

    id = db.Column(db.Integer, primary_key=True)
    korisnicko_ime = db.Column(db.String)
    zaporka = db.Column(db.String)

    def __init__(self, korisnicko_ime, zaporka):
        self.korisnicko_ime = korisnicko_ime
        self.zaporka = zaporka

    def __str__(self):
        return("KORISNIK: " + " " + str(self.id) + " " + self.korisnicko_ime + " " + self.zaporka)
    
    @classmethod
    def korisnik_postoji_u_bazi(cls, uneseno_korisnicko_ime, unesena_zaporka):
        korisnik_postoji = session.query(cls).filter_by(korisnicko_ime = uneseno_korisnicko_ime, zaporka = unesena_zaporka).one_or_none()
        if korisnik_postoji:
            return True
        else:
            return False

class Posuda(Base):
    __tablename__ = "posude"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String)
    id_biljke = db.Column(db.Integer, db.ForeignKey("biljke.id"))
    zadnja_temperatura = db.Column(db.Float)
    zadnja_vlaga = db.Column(db.Float)
    #zadnja_temperatura = db.Column(db.Float)

    biljka = relationship("Biljka", back_populates="posuda")
    ocitanja = relationship("Ocitanje", back_populates="posuda", uselist=True)


    def __init__(self, naziv, id_biljke=None, zadnja_temperatura=18, zadnja_vlaga=40):
        self.naziv = naziv
        self.zadnja_temperatura = zadnja_temperatura
        self.zadnja_vlaga = zadnja_vlaga
        if id_biljke:
            self.id_biljke = id_biljke

    def __str__(self):
        return("POSUDA: " + " " + str(self.id) + " " + self.naziv)
    
    @classmethod
    def izbrisi_posudu(cls, id_posude):
        session.query(cls).filter_by(id=id_posude).delete()
        session.commit()
   
class Biljka(Base):
    __tablename__ = "biljke"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String)
    temperatura = db.Column(db.INTEGER)
    vlaga_tla = db.Column(db.INTEGER)
    supstrat = db.Column(db.INTEGER)
    fotografija = db.Column(db.BLOB)

    posuda = relationship("Posuda", back_populates="biljka", uselist=False)
    
    def __init__(self, naziv, temperatura=0, vlaga_tla=0, supstrat=0, fotografija=None):
        self.naziv = naziv
        self.temperatura = temperatura
        self.vlaga_tla = vlaga_tla
        self.supstrat = supstrat
        self.fotografija = fotografija

    def __str__(self):
        return("BILJKA: " + " " + str(self.id) + " " + self.naziv)
    
class Ocitanje(Base):
    __tablename__ = "ocitanja"

    id = db.Column(db.Integer, primary_key=True)
    vrijeme = db.Column(db.String)
    vrijednost = db.Column(db.Float)
    vrsta_senzora = db.Column(db.String) # temperatura / vlaga
    id_posude = db.Column(db.Integer, db.ForeignKey("posude.id"))

    posuda = relationship("Posuda", back_populates="ocitanja", uselist=False)
    
    def __init__(self, vrijeme, vrijednost, vrsta_senzora, id_posude):
        self.vrijeme = vrijeme
        self.vrijednost = vrijednost
        self.vrsta_senzora = vrsta_senzora
        self.id_posude = id_posude

    def __str__(self):
        return("OCITANJE: " + " " + str(self.id) + " " + self.vrijeme + " " + str(self.vrijednost) + " " + self.vrsta_senzora)
    
# sve objekte koji nasljeđuju Base kreira u bazi podataka
Base.metadata.create_all(bind=db_engine)