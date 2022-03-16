from flask import Flask, session, redirect, request, url_for
from flask import render_template
import mysql.connector
from mysql.connector import connect, Error
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired
import bcrypt
from database import Database

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.route('/index')
def index():
    connexion_unique = Database.Instance()
    query_index = "SELECT circuit.nom, circuit.descriptif FROM circuit"
    index_circuit = connexion_unique.fetchall_simple(query_index)
    if 'pseudo' in session:
        pseudo = session['pseudo']
        return render_template('index.html', liste_circuit=index_circuit, pseudo=pseudo)
    else:
        return render_template('index.html', liste_circuit=index_circuit)
@app.route('/deconnexion')
def deconnexion():
    del session['pseudo']
    return redirect(url_for('index'))

@app.route('/<circuit>')
def circuit(circuit):
    connexion_unique = Database.Instance()
    query_nomcircuit = "SELECT nom FROM circuit WHERE circuit.nom = '%s' " % circuit
    nom_circuit = connexion_unique.query_for2_3(query_nomcircuit)
    query_desccircuit = "SELECT descriptif FROM circuit WHERE circuit.nom = '%s' " % circuit
    description_circuit = connexion_unique.query_for2_3(query_desccircuit)
    query_prixcircuit = "SELECT prix_circuit FROM circuit WHERE circuit.nom = '%s' " % circuit
    prix_circuit = connexion_unique.query_for1_4(query_prixcircuit)
    query_datedepart = "SELECT date_depart FROM circuit WHERE circuit.nom = '%s'  " % circuit
    date_circuit_debut = connexion_unique.query_for15_3(query_datedepart)
    query_datearrivee = "SELECT date_arrivee FROM circuit WHERE circuit.nom = '%s'  " % circuit
    date_circuit_fin = connexion_unique.query_for15_3(query_datearrivee)
    query_nomdepart = "SELECT depart.nom FROM `circuit` JOIN ville AS depart ON circuit.ville_depart = depart.id JOIN etape ON circuit.id = etape.id_circuit WHERE circuit.nom = '%s' " %circuit
    depart_circuit = connexion_unique.query_for2_3(query_nomdepart)
    query_nomarrivee = "SELECT arrivee.nom FROM `circuit` JOIN ville AS arrivee ON circuit.ville_arrivee = arrivee.id JOIN etape ON circuit.id = etape.id_circuit WHERE circuit.nom = '%s' " %circuit
    arrivee_circuit = connexion_unique.query_for2_3(query_nomarrivee)
    query_img_lieucircuit ="SELECT DISTINCT image.url, lieu.label from image join lieu ON lieu.id = image.id_lieu JOIN etape ON etape.id_lieu = lieu.id JOIN circuit ON etape.id_circuit = circuit.id WHERE circuit.nom = '%s' GROUP BY etape.ordre " % circuit
    circuit_lieu = connexion_unique.fetchall_simple(query_img_lieucircuit)
    reservation = "Inscription pour réserver"
    query_idcircuit = "SELECT id FROM circuit WHERE circuit.nom = '%s' " % circuit
    id_circuit = connexion_unique.query_for2_3(query_idcircuit)
    session['circuit'] = circuit
    if 'pseudo' in session:
        pseudo = session['pseudo']
        reservation = "Réserver"
        return render_template('circuit.html', nom_circuit=nom_circuit, description_circuit=description_circuit, prix_circuit=prix_circuit,
                               circuit_lieu=circuit_lieu, date_circuit_debut=date_circuit_debut, date_circuit_fin=date_circuit_fin,
                               depart_circuit=depart_circuit, arrivee_circuit=arrivee_circuit, pseudo=pseudo, reservation=reservation, id_circuit=id_circuit)
    else:
        return render_template('circuit.html', nom_circuit=nom_circuit, description_circuit=description_circuit, prix_circuit=prix_circuit,
                               circuit_lieu=circuit_lieu, date_circuit_debut=date_circuit_debut, date_circuit_fin=date_circuit_fin,
                               depart_circuit=depart_circuit, arrivee_circuit=arrivee_circuit, reservation=reservation)

@app.route('/circuit/<lieu>')
def lieu(lieu):
    connexion_unique = Database.Instance()
    query_imglieu = "SELECT url FROM `image` JOIN lieu ON id_lieu = lieu.id WHERE lieu.label = '%s' " % lieu
    url_lieu = connexion_unique.query_for2_3(query_imglieu)
    query_nomville = "SELECT nom FROM ville JOIN lieu ON ville.id = id_ville WHERE lieu.label = '%s' " % lieu
    ville_lieu = connexion_unique.query_for2_3(query_nomville)
    nom = ville_lieu
    query_nompays = "SELECT pays.nom FROM pays JOIN ville ON pays.id = id_pays WHERE ville.nom = '%s' " % nom
    pays_lieu = connexion_unique.query_for2_3(query_nompays)
    query_desclieu = "SELECT description FROM lieu WHERE lieu.label = '%s' " % lieu
    description_lieu = connexion_unique.query_for2_3(query_desclieu)
    query_prixlieu = "SELECT prix_visite FROM lieu WHERE lieu.label = '%s' " % lieu
    prix_lieu = connexion_unique.query_for1_4(query_prixlieu)
    nom_lieu = lieu
    if 'pseudo' in session:
        pseudo = session['pseudo']
        return render_template('lieu.html', url=url_lieu, nom_lieu=nom_lieu, ville_lieu=ville_lieu, pays_lieu=pays_lieu,
                           description_lieu=description_lieu, prix_lieu=prix_lieu, pseudo=pseudo)
    else:
        return render_template('lieu.html', url=url_lieu, nom_lieu=nom_lieu, ville_lieu=ville_lieu, pays_lieu=pays_lieu,
                           description_lieu=description_lieu, prix_lieu=prix_lieu)


@app.route('/creercompte', methods=['GET', 'POST'])
def creercompte():
    class testform(FlaskForm):
        user = StringField('user', validators=[DataRequired()])
        mail = StringField('mail', validators=[DataRequired()])
        mdp = StringField('mdp', validators=[DataRequired()])
        nom = StringField('nom')
        prenom = StringField('prenom')
        anniversaire = DateField('Start', format = '%Y-%m-%d')
    form = testform()
    if form.validate_on_submit():
        user = request.form['user']
        mail = request.form['mail']
        mdp = request.form['mdp']
        nom = request.form['nom']
        prenom = request.form['prenom']
        anniversaire = form.anniversaire.data.strftime('%Y-%m-%d')
        sel = bcrypt.gensalt()
        mdp = mdp.encode(encoding = 'UTF-8', errors = 'strict')
        mdpcrypter = bcrypt.hashpw(mdp, sel)
        connexion_unique = Database.Instance()
        query_nouvelleutilisateur = "INSERT INTO utilisateur (role_admin, nom, prenom, date_naissance, login, email, mdp) VALUES " \
                 "(%s, %s, %s, %s, %s, %s, %s) "
        connexion_unique.commit(query_nouvelleutilisateur, (0, nom, prenom, anniversaire, user, mail, mdpcrypter))
        return redirect(url_for('connexion'))
    return render_template('/creercompte.html', form=form)


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    class connexionform(FlaskForm):
        user = StringField('user', validators=[DataRequired()])
        mdp = PasswordField('mdp', validators=[DataRequired()])
    form = connexionform()
    if form.validate_on_submit():
        user = request.form['user']
        mdpform = request.form['mdp']
        connexion_unique = Database.Instance()
        query_mdputilisateur = "SELECT mdp FROM utilisateur WHERE login = '%s' " % user
        md = connexion_unique.fetchone_simple(query_mdputilisateur)
        mdpform = mdpform.encode('utf-8')
        md = md.encode('utf-8')
        if bcrypt.checkpw(mdpform, md):
            query_connexionutilisateur = "SELECT login, nom, prenom, email, role_admin FROM utilisateur WHERE login = '%s' " % user
            connect = connexion_unique.fetchall_simple(query_connexionutilisateur)
            for row in connect:
                p = row[0]
                n = row[1]
                pr = row[2]
                m = row[3]
                r = row[4]
            session['pseudo'] = p
            session['nom'] = n
            session['prenom'] = pr
            session['email'] = m
            session['role'] = r
            return redirect(url_for('index'))
        else:
            return redirect(url_for('connexion'))
    return render_template('/connexion.html', form=form)


@app.route('/reserver', methods=['GET', 'POST'])
def reserver():
    pseudo = session['pseudo']
    circuit = session['circuit']
    class reserverform(FlaskForm):
        place = StringField('nb_place', validators=[DataRequired()])
    form = reserverform()
    if form.validate_on_submit():
        place = request.form['place']
        connexion_unique = Database.Instance()
        query_circuit = "SELECT circuit.id FROM circuit WHERE circuit.nom = '%s' " % circuit
        circuit_id = connexion_unique.query_for1_2(query_circuit)
        query_utilisateur = "SELECT utilisateur.id FROM utilisateur WHERE utilisateur.login = '%s' " % pseudo
        pseudo_id = connexion_unique.query_for1_2(query_utilisateur)
        query_insert = "INSERT INTO `reservation` (`id_circuit`, `id_utilisateur`, `nb_place`, `date`, `heure`) VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME);"
        connexion_unique.commit(query_insert, (circuit_id, pseudo_id, place))
        return redirect(url_for('listereservation'))
    return render_template('/reserver.html', form=form, pseudo=pseudo, circuit=circuit)

@app.route('/listereservation')
def listereservation():
    pseudo = session['pseudo']
    connexion_unique = Database.Instance()
    query_reservation = "SELECT circuit.nom, reservation.nb_place, circuit.date_depart, circuit.date_arrivee FROM `reservation` JOIN circuit ON circuit.id = reservation.id_circuit JOIN utilisateur ON utilisateur.id = reservation.id_utilisateur WHERE utilisateur.login = '%s'" % pseudo
    listereservation_reservation = connexion_unique.fetchall_simple(query_reservation)
    return render_template('listereservation.html', liste_reservation=listereservation_reservation, pseudo=pseudo)



if __name__ == '__main__':
    app.run(debug=True)