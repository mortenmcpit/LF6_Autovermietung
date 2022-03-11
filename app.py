from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

app = Flask(__name__, template_folder='templates', static_folder='static')
# Hier MySQL Connection Daten einfügen
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:W8meister!@localhost:3306/autovermitung'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

Bootstrap(app)
db = SQLAlchemy(app)


# DB
class Personal(db.Model):
    __tablename__ = "personal"
    idPersonal = db.Column("idPersonal", db.Integer, primary_key=True, autoincrement=True, index=True)
    Nachname = db.Column("Nachname", db.String(20))
    Vorname = db.Column("Vorname", db.String(20))

    vorgaenge_personal = db.relationship("Vorgang", back_populates="personal", lazy="select")

    def __repr__(self):
        return f'{self.Nachname}, {self.Vorname}'


class Kunde(db.Model):
    __tablename__ = "kunde"
    idKunde = db.Column("idKunde", db.Integer, primary_key=True, index=True)  # kundennummer
    Plz = db.Column("plz", db.String())

    Nachname = db.Column("Nachname", db.String(20))
    Vorname = db.Column("Vorname", db.String(20))
    Strasse = db.Column("Strasse", db.String(20))
    Stadt = db.Column("Stadt", db.String(20))
    Land = db.Column("Land", db.String(20))
    Geburtsdatum = db.Column("Geburtsdatum", db.Date)
    Telefon = db.Column("Telefon", db.String(20))

    vorgaenge_kunde = db.relationship("Vorgang", back_populates="kunde", lazy="select")

    def __repr__(self):
        return f'{self.Nachname}, {self.Vorname}'


class Auto(db.Model):
    __tablename__ = "auto"
    idAuto = db.Column("idAuto", db.Integer, primary_key=True, autoincrement=True, index=True)
    baujahr = db.Column("baujahr", db.Integer)
    ps = db.Column("ps", db.Integer)
    ccm = db.Column("ccm", db.Integer)

    kennzeichen = db.Column("kennzeichen", db.String(20))
    hersteller = db.Column("hersteller", db.String(20))
    typ = db.Column("typ", db.String(20))
    farbe = db.Column("farbe", db.String(20))
    kraftstoff = db.Column("kraftstoff", db.String(10))
    sitzplaetze = db.Column("sitzplaetze", db.Integer)
    extras = db.Column("extras", db.String(20))
    zubehoer1 = db.Column("zubehoer1", db.String(20))
    zubehoer2 = db.Column("zubehoer2", db.String(20))
    versicherungs_nr = db.Column("versicherungsNr", db.String(20))

    tuv = db.Column("tuv", db.Date)
    asu = db.Column("asu", db.Date)

    idPreisgruppe = db.Column("idPreisgruppe", db.Integer,
                              db.ForeignKey("preisgruppe.idPreisgruppe"))
    preisgruppe = db.relationship("Preisgruppe", back_populates="auto", lazy="select")

    vorgaenge_auto = db.relationship("Vorgang", back_populates="auto", lazy="select")

    def __repr__(self):
        return f'{self.hersteller} {self.typ}'


class Preisgruppe(db.Model):
    __tablename__ = "preisgruppe"
    idPreisgruppe = db.Column("idPreisgruppe", db.Integer, primary_key=True, autoincrement=True, index=True)
    preisStunde = db.Column("preisStunde", db.Float)
    preisTag = db.Column("preisTag", db.Float)
    preisWoche = db.Column("preisWoche", db.Float)
    preisKm = db.Column("preisKm", db.Float)

    auto = db.relationship("Auto", back_populates="preisgruppe", lazy="select")
    vorgaenge_preisgruppe = db.relationship("Vorgang", back_populates="preisgruppe", lazy="select")

    def __repr__(self):
        return f'{self.idPreisgruppe}'


class Vorgang(db.Model):
    __tablename__ = "vorgang"
    idVorgang = db.Column("idVorgang", db.Integer, primary_key=True, autoincrement=True, index=True)
    ausleihDatum = db.Column("ausleihDatum", db.Date)
    rueckgabeDatum = db.Column("rueckgabeDatum", db.Date)
    anfangsKm = db.Column("anfangsKm", db.Integer)
    endKm = db.Column("endKm", db.Integer)

    idKunde = db.Column("idKunde", db.Integer, db.ForeignKey("kunde.idKunde"))
    kunde = db.relationship("Kunde", back_populates="vorgaenge_kunde", lazy="select")

    idPersonal = db.Column("idPersonal", db.Integer, db.ForeignKey("personal.idPersonal"))
    personal = db.relationship("Personal", back_populates="vorgaenge_personal", lazy="select")

    idAuto = db.Column("idAuto", db.Integer, db.ForeignKey("auto.idAuto"))
    auto = db.relationship("Auto", back_populates="vorgaenge_auto", lazy="select")

    idPreisgruppe = db.Column("idPreisgruppe", db.Integer,
                              db.ForeignKey("preisgruppe.idPreisgruppe"))
    preisgruppe = db.relationship("Preisgruppe", back_populates="vorgaenge_preisgruppe", lazy="select")


# Forms
class PersonalForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], render_kw={'placeholder': 'ID'})
    nachname = StringField('Nachname', validators=[DataRequired()], render_kw={'placeholder': 'Nachname'})
    vorname = StringField('Vorname', render_kw={'placeholder': 'Vorname'})


class ProcessForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], render_kw={'placeholder': 'ID'})
    ausleihDatum = DateField('Nachname', validators=[DataRequired()], render_kw={'placeholder': 'Ausleih Datum'})
    rueckgabeDatum = DateField('Vorname', render_kw={'placeholder': 'Rückgabe Datum'})
    anfangsKm = FloatField('Anfangs Km', render_kw={'placeholder': 'Anfangs Km'})
    endKm = FloatField('Kilometerstand', render_kw={'placeholder': 'Kilometerstand Rückgabe'})
    kunde = QuerySelectField('Kunde', query_factory=db.session.query(Kunde).all, allow_blank=True)
    personal = QuerySelectField('Personal', query_factory=db.session.query(Personal).all, allow_blank=True)
    auto = QuerySelectField('Auto', query_factory=db.session.query(Auto).all, allow_blank=True)
    preisgruppe = QuerySelectField('Preisgruppe', query_factory=db.session.query(Preisgruppe).all, allow_blank=True)


class RentingForm(FlaskForm):
    car = QuerySelectField('Auto', query_factory=db.session.query(Auto).all, allow_blank=True)
    kunde = QuerySelectField('Kunde', query_factory=db.session.query(Kunde).all, allow_blank=True)
    ausleihDatum = DateField('Ausleihdatum', render_kw={'placeholder': 'Start'})
    rueckgabedatum = DateField('Rückgabedatum', render_kw={'placeholder': 'Ende'})


# URL Routes
@app.route('/home/')
@app.route('/', methods=['GET', 'POST'])
def home():
    form = RentingForm(request.form)
    return render_template('renting.html', form=form)


@app.route('/cars/')
def cars():
    cars = db.session.query(Auto).all()
    return render_template('cars.html', cars=cars)


@app.route('/processes/', methods=['GET', 'POST'])
def processes():
    form = ProcessForm(request.form)
    processes = db.session.query(Vorgang).all()
    if request.method == 'POST':
        if form.validate_on_submit():
            process = Vorgang(idVorgang=form.id.data, ausleihDatum=form.ausleihDatum.data,
                              rueckgabeDatum=form.rueckgabeDatum.data, anfangsKm=form.anfangsKm.data,
                              endKm=form.endKm.data, idKunde=form.kunde.data.idKunde, idAuto=form.auto.data.idAuto,
                              idPersonal=form.personal.data.idPersonal,
                              idPreisgruppe=form.preisgruppe.data.idPreisgruppe)
            db.session.add(process)
            db.session.commit()
            return redirect(url_for('processes'))
    return render_template('processes.html', processes=processes, form=form)


@app.route('/personal/', methods=['GET', 'POST'])
def personal():
    personal = db.session.query(Personal).all()
    form = PersonalForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            personal = Personal(idPersonal=form.id.data, Nachname=form.nachname.data, Vorname=form.vorname.data)
            db.session.add(personal)
            db.session.commit()
            return redirect(url_for('personal'))
    return render_template('personal.html', personal=personal, form=form)


@app.route('/prices/')
def prices():
    prices = db.session.query(Preisgruppe).all()
    return render_template('prices.html', prices=prices)


@app.route('/customers/')
def customers():
    customers = db.session.query(Kunde).all()
    return render_template('customers.html', customers=customers)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
