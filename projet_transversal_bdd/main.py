from flask import Flask, session, redirect, request, url_for
from flask import render_template
import mysql.connector
from mysql.connector import connect, Error
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField
from wtforms.validators import DataRequired
import bcrypt
from database import Database

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.route('/index')
def index():
    #connexion à la base de donnée avec la liasion du fichier database.py
    connexion_unique = Database.Instance()
    #sélectionne dans circuit le nom et le descriptif depuis la base de donnée
    query_index = "SELECT circuit.nom, circuit.descriptif FROM circuit"
    #prend le select dans une liste à réutiliser plus tard
    index_circuit = connexion_unique.fetchall_simple(query_index)
    #si quelqu'un ce connecte, on récupère le login et son role(admin ou non)
    if 'pseudo' in session:
        pseudo = session['pseudo']
        role = session['role']
        #charge la page avec le template "index.html" en récupérent les données du select, le nom du login et le role(id)
        return render_template('index.html', liste_circuit=index_circuit, pseudo=pseudo, role=role)
    else:
        #charge la page avec le template "index.html" en récupérent les données du select
        return render_template('index.html', liste_circuit=index_circuit)

@app.route('/deconnexion')
#s'il est appelé, efface la connexion en cours
def deconnexion():
    del session['pseudo']
    del session['role']
    #change l'url en "/index" donc appele l'app.route du même nom
    return redirect(url_for('index'))

@app.route('/<circuit>')
def circuit(circuit):
    #connexion à la base de donnée avec la liasion du fichier database.py
    connexion_unique = Database.Instance()
    # sélectionne dans circuit le nom depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_nomcircuit = "SELECT nom FROM circuit WHERE circuit.nom = '%s' " % circuit
    nom_circuit = connexion_unique.query_for2_3(query_nomcircuit)
    # sélectionne dans circuit le descriptif depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_desccircuit = "SELECT descriptif FROM circuit WHERE circuit.nom = '%s' " % circuit
    description_circuit = connexion_unique.query_for2_3(query_desccircuit)
    # sélectionne dans circuit le prix depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_prixcircuit = "SELECT prix_circuit FROM circuit WHERE circuit.nom = '%s' " % circuit
    prix_circuit = connexion_unique.query_for1_4(query_prixcircuit)
    # sélectionne dans circuit le date de départ depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_datedepart = "SELECT date_depart FROM circuit WHERE circuit.nom = '%s'  " % circuit
    date_circuit_debut = connexion_unique.query_for15_3(query_datedepart)
    # sélectionne dans circuit le date d'arrivée depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_datearrivee = "SELECT date_arrivee FROM circuit WHERE circuit.nom = '%s'  " % circuit
    date_circuit_fin = connexion_unique.query_for15_3(query_datearrivee)
    # sélectionne dans circuit le nom de la ville de départ depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_nomdepart = "SELECT depart.nom FROM `circuit` JOIN ville AS depart ON circuit.ville_depart = depart.id JOIN etape ON circuit.id = etape.id_circuit WHERE circuit.nom = '%s' " %circuit
    depart_circuit = connexion_unique.query_for2_3(query_nomdepart)
    # sélectionne dans circuit le nom de la ville d'arrivée depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_nomarrivee = "SELECT arrivee.nom FROM `circuit` JOIN ville AS arrivee ON circuit.ville_arrivee = arrivee.id JOIN etape ON circuit.id = etape.id_circuit WHERE circuit.nom = '%s' " %circuit
    arrivee_circuit = connexion_unique.query_for2_3(query_nomarrivee)
    # sélectionne dans circuit l'url des photos de tout les lieux dans ce circuit sans doublons si on passe plusieur fois dans le lieu de la ville de départ depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_img_lieucircuit ="SELECT DISTINCT image.url, lieu.label from image join lieu ON lieu.id = image.id_lieu JOIN etape ON etape.id_lieu = lieu.id JOIN circuit ON etape.id_circuit = circuit.id WHERE circuit.nom = '%s' GROUP BY etape.ordre " % circuit
    circuit_lieu = connexion_unique.fetchall_simple(query_img_lieucircuit)
    reservation = "Inscription pour réserver"
    # sélectionne dans circuit son id depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/<circuit>")
    query_idcircuit = "SELECT id FROM circuit WHERE circuit.nom = '%s' " % circuit
    id_circuit = connexion_unique.query_for2_3(query_idcircuit)
    # garde de côté l'id du circuit pour l'utilisé dans la réservation
    session['circuit'] = circuit
    #si quelqu'un ce connecte, on récupère le login et son role(admin ou non) et change l'état de la réservation
    if 'pseudo' in session:
        pseudo = session['pseudo']
        role = session['role']
        reservation = "Réserver"
        # charge la page avec le template "circuit.html" en récupérent toutes les informations sélectionné, le login, le role(id), l'id du circuit et l'état de la réservation
        return render_template('circuit.html', nom_circuit=nom_circuit, description_circuit=description_circuit, prix_circuit=prix_circuit,
                               circuit_lieu=circuit_lieu, date_circuit_debut=date_circuit_debut, date_circuit_fin=date_circuit_fin,
                               depart_circuit=depart_circuit, arrivee_circuit=arrivee_circuit, pseudo=pseudo, role=role, reservation=reservation, id_circuit=id_circuit)
    else:
        # charge la page avec le template "circuit.html" en récupérent toutes les informations sélectionné et l'état de la réservation
        return render_template('circuit.html', nom_circuit=nom_circuit, description_circuit=description_circuit, prix_circuit=prix_circuit,
                               circuit_lieu=circuit_lieu, date_circuit_debut=date_circuit_debut, date_circuit_fin=date_circuit_fin,
                               depart_circuit=depart_circuit, arrivee_circuit=arrivee_circuit, reservation=reservation)

@app.route('/circuit/<lieu>')
def lieu(lieu):
    #connexion à la base de donnée avec la liasion du fichier database.py
    connexion_unique = Database.Instance()
    # sélectionne dans lieu l'url de la photo depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/circuit/<lieu>")
    query_imglieu = "SELECT url FROM `image` JOIN lieu ON id_lieu = lieu.id WHERE lieu.label = '%s' " % lieu
    url_lieu = connexion_unique.query_for2_3(query_imglieu)
    # sélectionne dans lieu le nom depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/circuit/<lieu>")
    query_nomville = "SELECT nom FROM ville JOIN lieu ON ville.id = id_ville WHERE lieu.label = '%s' " % lieu
    ville_lieu = connexion_unique.query_for2_3(query_nomville)
    #garde le nom de la ville de côté pour l'utiliser juste après
    nom = ville_lieu
    # sélectionne dans pays le nom depuis la base de donnée par rapport au nom de la ville ou se trouve le lieu
    query_nompays = "SELECT pays.nom FROM pays JOIN ville ON pays.id = id_pays WHERE ville.nom = '%s' " % nom
    pays_lieu = connexion_unique.query_for2_3(query_nompays)
    # sélectionne dans lieu la description depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/circuit/<lieu>")
    query_desclieu = "SELECT description FROM lieu WHERE lieu.label = '%s' " % lieu
    description_lieu = connexion_unique.query_for2_3(query_desclieu)
    # sélectionne dans lieu le prix depuis la base de donnée par rapport au nom dans la barre de recherche (dans "/circuit/<lieu>")
    query_prixlieu = "SELECT prix_visite FROM lieu WHERE lieu.label = '%s' " % lieu
    prix_lieu = connexion_unique.query_for1_4(query_prixlieu)
    # garde le nom du lieu de côté
    nom_lieu = lieu
    #si quelqu'un ce connecte, on récupère le login et son role(admin ou non)
    if 'pseudo' in session:
        pseudo = session['pseudo']
        role = session['role']
        # charge la page avec le template "lieu.html" en récupérent toutes les informations sélectionné, le login et le role(id)
        return render_template('lieu.html', url=url_lieu, nom_lieu=nom_lieu, ville_lieu=ville_lieu, pays_lieu=pays_lieu,
                           description_lieu=description_lieu, prix_lieu=prix_lieu, pseudo=pseudo, role=role)
    else:
        # charge la page avec le template "lieu.html" en récupérent toutes les informations sélectionné
        return render_template('lieu.html', url=url_lieu, nom_lieu=nom_lieu, ville_lieu=ville_lieu, pays_lieu=pays_lieu,
                           description_lieu=description_lieu, prix_lieu=prix_lieu)


@app.route('/creercompte', methods=['GET', 'POST'])
def creercompte():
    # initialisation du formulaire
    class inscriptionform(FlaskForm):
        user = StringField('user', validators=[DataRequired()])
        mail = EmailField('mail', validators=[DataRequired()])
        mdp = StringField('mdp', validators=[DataRequired()])
        nom = StringField('nom')
        prenom = StringField('prenom')
        anniversaire = DateField('Start', format = '%Y-%m-%d')
    form = inscriptionform()
    # récupère les informations du formulaire
    if form.validate_on_submit():
        user = request.form['user']
        mail = request.form['mail']
        mdp = request.form['mdp']
        nom = request.form['nom']
        prenom = request.form['prenom']
        anniversaire = form.anniversaire.data.strftime('%Y-%m-%d')
        #crypte le mot de passe
        sel = bcrypt.gensalt()
        mdp = mdp.encode(encoding = 'UTF-8', errors = 'strict')
        mdpcrypter = bcrypt.hashpw(mdp, sel)
        #connexion à la base de donnée avec la liasion du fichier database.py
        connexion_unique = Database.Instance()
        # fait une insertion de donnée avec les données récupéré du formulaire
        query_nouvelleutilisateur = "INSERT INTO utilisateur (role_admin, nom, prenom, date_naissance, login, email, mdp) VALUES " \
                 "(%s, %s, %s, %s, %s, %s, %s) "
        connexion_unique.commit(query_nouvelleutilisateur, (0, nom, prenom, anniversaire, user, mail, mdpcrypter))
        # change l'url en "/connexion" donc appele l'app.route du même nom
        return redirect(url_for('connexion'))
    # charge la page avec le template "creercompte.html" en prenant le formulaire à remplir
    return render_template('creercompte.html', form=form)


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    # initialisation du formulaire
    class connexionform(FlaskForm):
        user = StringField('user', validators=[DataRequired()])
        mdp = PasswordField('mdp', validators=[DataRequired()])
    form = connexionform()
    # récupère les informations du formulaire
    if form.validate_on_submit():
        user = request.form['user']
        mdpform = request.form['mdp']
        #connexion à la base de donnée avec la liasion du fichier database.py
        connexion_unique = Database.Instance()
        query_mdputilisateur = "SELECT mdp FROM utilisateur WHERE login = '%s' " % user
        #décrypte le mot de passe
        md = connexion_unique.fetchone_simple(query_mdputilisateur)
        mdpform = mdpform.encode('utf-8')
        md = md.encode('utf-8')
        if bcrypt.checkpw(mdpform, md):
            # sélectionne dans utilisateur le login, nom, prenom, email, role depuis la base de donnée par rapport au nom du écrit dans formulaire
            query_connexionutilisateur = "SELECT login, nom, prenom, email, role_admin FROM utilisateur WHERE login = '%s' " % user
            connect = connexion_unique.fetchall_simple(query_connexionutilisateur)
            for row in connect:
                pseudo = row[0]
                nom = row[1]
                prenom = row[2]
                email = row[3]
                role = row[4]
            session['pseudo'] = pseudo
            session['nom'] = nom
            session['prenom'] = prenom
            session['email'] = email
            session['role'] = role
            #change l'url en "/index" donc appele l'app.route du même nom
            return redirect(url_for('index'))
        else:
            #recharge la page si le compte n'est pas trouver dans la base de donnée
            return redirect(url_for('connexion'))
    # charge la page avec le template "connexion.html" en prenant le formulaire à remplir
    return render_template('connexion.html', form=form)


@app.route('/reserver', methods=['GET', 'POST'])
def reserver():
    #la personne est forcément connecté pour être la, on récupère son le login et son role(admin ou non) ainsi que le circuit séléctionné avec @app.route(/<circuit>)
    pseudo = session['pseudo']
    circuit = session['circuit']
    role = session['role']
    # initialisation du formulaire
    class reserverform(FlaskForm):
        place = StringField('nb_place', validators=[DataRequired()])
    form = reserverform()
    # récupère les informations du formulaire
    if form.validate_on_submit():
        place = request.form['place']
        #connexion à la base de donnée avec la liasion du fichier database.py
        connexion_unique = Database.Instance()
        # sélectionne dans circuit l'id depuis la base de donnée par rapport au nom du circuit défini à l'initialisation de la page
        query_circuit = "SELECT circuit.id FROM circuit WHERE circuit.nom = '%s' " % circuit
        circuit_id = connexion_unique.query_for1_2(query_circuit)
        # sélectionne dans utilisateur l'id depuis la base de donnée par rapport au nom du pseudo défini à l'initialisation de la page
        query_utilisateur = "SELECT utilisateur.id FROM utilisateur WHERE utilisateur.login = '%s' " % pseudo
        pseudo_id = connexion_unique.query_for1_2(query_utilisateur)
        # fait une insertion de donnée avec les données récupéré du formulaire
        query_insert = "INSERT INTO `reservation` (`id_circuit`, `id_utilisateur`, `nb_place`, `date`, `heure`) VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME);"
        connexion_unique.commit(query_insert, (circuit_id, pseudo_id, place))
        # change l'url en "/listereservation" donc appele l'app.route du même nom
        return redirect(url_for('listereservation'))
    # charge la page avec le template "reserver.html"en prenant le formulaire à remplir et récupére toutes les informations sélectionné, le login et le role(id)
    return render_template('/reserver.html', form=form, pseudo=pseudo, circuit=circuit, role=role)

@app.route('/listereservation')
def listereservation():
    # la personne est forcément connecté pour être la, on récupère son le login et son role(admin ou non)
    pseudo = session['pseudo']
    role = session['role']
    #connexion à la base de donnée avec la liasion du fichier database.py
    connexion_unique = Database.Instance()
    query_reservation = "SELECT circuit.nom, reservation.nb_place, circuit.date_depart, circuit.date_arrivee FROM `reservation` JOIN circuit ON circuit.id = reservation.id_circuit JOIN utilisateur ON utilisateur.id = reservation.id_utilisateur WHERE utilisateur.login = '%s'" % pseudo
    listereservation_reservation = connexion_unique.fetchall_simple(query_reservation)
    # charge la page avec le template "listereservation.html" en récupére toutes les informations sélectionné, le login et le role(id)
    return render_template('listereservation.html', liste_reservation=listereservation_reservation, pseudo=pseudo, role=role)



if __name__ == '__main__':
    app.run(debug=True)