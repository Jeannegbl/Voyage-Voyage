from flask import Flask, session, redirect, request, url_for
from flask import render_template
import mysql.connector
from mysql.connector import connect, Error
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField, IntegerField, DecimalField
from wtforms.validators import DataRequired
import bcrypt
from database import Database
from operator import add

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

@app.route('/circuit', methods=['GET', 'POST'])
def circuit_admin():

    # On verifie que l'utilisateur est bien connecte en tant qu'admin
    if session['role'] == 1:

        # On cree une connexion a la base de donnee sous forme de singleton
        connexion_unique = Database.Instance()

        # On cree le formulaire pour ajouter un circuit
        class AjouterCircuitFormulaire(FlaskForm):
            ajouter_nom_circuit = StringField(validators=[DataRequired()])
            ajouter_descriptif_circuit = StringField(validators=[DataRequired()])
            ajouter_prix_circuit = DecimalField(validators=[DataRequired()])
            ajouter_duree_circuit = IntegerField(validators=[DataRequired()])
            ajouter_nbplace_circuit = IntegerField(validators=[DataRequired()])

        # On creer le formulaire pour modifier ou supprimer un circuit
        class ModifierCircuitFormulaire(FlaskForm):
            modifier_id_circuit = StringField(validators=[DataRequired()])
            modifier_nom_circuit = StringField(validators=[DataRequired()])
            modifier_descriptif_circuit = StringField(validators=[DataRequired()])
            modifier_prix_circuit = DecimalField(validators=[DataRequired()])
            modifier_duree_circuit = IntegerField(validators=[DataRequired()])
            modifier_nbplace_circuit = IntegerField(validators=[DataRequired()])

        # On cree un formulaire pour modifier ou supprimer une etape mais juste pour avoir le token et ainsi pouvoir l'identifier
        class ModifierEtapeFormulaire(FlaskForm):
            modifier_duree_etape1 = IntegerField(validators=[DataRequired()])

        # On cree un formulaire pour ajouter une etape mais juste pour avoir le token et ainsi pouvoir l'identifier
        class AjouterEtapeFormulaire(FlaskForm):
            ajouter_duree_etape1 = IntegerField(validators=[DataRequired()])

        # On recupere les informations sur les circuit dont on a besoin
        query_informations_circuit= "SELECT circuit.id, circuit.nom, descriptif, prix_circuit, duree_jour, nb_place, " \
                                    "date_depart, date_arrivee, depart.nom AS depart_nom, arrivee.nom AS arrive_nom " \
                                    "FROM circuit JOIN ville AS depart ON circuit.ville_depart = depart.id JOIN ville " \
                                    "AS arrivee ON circuit.ville_arrivee = arrivee.id "
        informations_circuit = connexion_unique.fetchall_simple(query_informations_circuit)

        # On recupere une liste avec le nom des villes pour l'implementer dans un select dans le html
        query_nom_villes = "SELECT nom FROM ville"
        liste_nom_villes = connexion_unique.fetchall_simple(query_nom_villes)

        # On recupere les id des circuits afin de les utilises pour recuperer les etapes
        query_id_circuits = " SELECT id FROM circuit ORDER BY id"
        id_circuits = connexion_unique.fetchall_simple(query_id_circuits)

        # On recupere les informations sur les etapes dont on a besoin grace au id des circuits que l'on a recupere
        # precedement et on les met dans une liste
        liste_information_etapes = []
        for id in id_circuits:
            query_informations_etape = "SELECT etape.id_circuit, etape.ordre, lieu.label, etape.duree_en_minute, " \
                                       "etape.date FROM lieu JOIN etape ON lieu.id = etape.id_lieu JOIN circuit ON " \
                                       "etape.id_circuit = circuit.id WHERE circuit.id = '%s' ORDER BY etape.ordre "
            id_str = (str(id)[1:-2])
            id_int = int(id_str)
            id_tupple = (id_int,)
            informations_etape = connexion_unique.fetchall_arguments(query_informations_etape, id_tupple)
            liste_information_etapes.append(informations_etape)

        # On combine les informations des circuits et des etapes correspondant a ce circuit
        # en une liste de liste correspondant a ce schema :
        # [[informations d'un circuit, [informations d'une etape], [informations d'une autre etape], [etc]],
        # [informations d'un autre circuit, [informations d'une etape], [informations d'une autre etape], [etc]], [etc]]

        tupple_information_etapes = [tuple(x) for x in liste_information_etapes]
        tupple_circuit_etape = map(add, informations_circuit, tupple_information_etapes)
        liste_circuit_etape = [list(x) for x in tupple_circuit_etape]

        # On cree une liste qui nous sera utile dans le html pour afficher les etapes qui sont stocker a partir de
        # la position 10 dans la liste de liste cree precedement
        liste_utile = list(range(10, 25))
        # On recupere une liste avec les labels des lieux afin de les implementer dans un select dans le html
        query_label_lieux = "SELECT label FROM lieu"
        liste_label_lieux = connexion_unique.fetchall_simple(query_label_lieux)

        # On cree nos formulaires a pertir des classe crees precedement
        ajouter_circuit_formulaire = AjouterCircuitFormulaire()
        modifier_circuit_formulaire = ModifierCircuitFormulaire()
        modifier_etape_formulaire = ModifierEtapeFormulaire()
        ajouter_etape_formulaire = AjouterEtapeFormulaire()

        # On verifie si le formulaire pour modifier une etape a ete envoyer
        if modifier_etape_formulaire.validate_on_submit():

            # On creer une double boucle for afin de recuperer les informations du bon formulaire grace au "id" crees
            # dans l'attribut "name" du html
            for id in id_circuits:
                str_id = str(id)[1:-2]
                for n in liste_utile:

                    # On verifie que l'utilisateur a cliquer sur le bouton modifier
                    if request.form['modifier_submit_etape'] == f'Modifier{str_id}{n}':
                        lieu_etape = request.form[f'modifier_lieu_etape{str_id}{n}']
                        duree_etape = request.form[f'modifier_duree_etape{str_id}{n}']
                        date_etape = request.form[f'modifier_date_etape{str_id}{n}']
                        ordre_etape = request.form[f'modifier_ordre_etape{str_id}{n}']
                        id_circuit_etape = request.form[f'modifier_id_circuit_etape{str_id}{n}']

                        # On recupere une requete factice, c'est-a-dire qui ne nous servira a rien, mais qui a juste
                        # etee implementer afin de creer la classe de notre formulaire
                        requete_factice = request.form['modifier_duree_etape1']

                        # On recupere l'id du lieu correspondant au label selectionne dans le select
                        query_id_lieu = "SELECT id FROM lieu WHERE label = %s "
                        lieu_etape_str = (str(lieu_etape),)
                        id_lieu_etape = connexion_unique.fetchone_arguments(query_id_lieu, lieu_etape_str)

                        # On met a jour l'etape en fonction des informations recuperees par le formulaire
                        query_update_etape = "UPDATE etape SET id_lieu = %s, date = %s, duree_en_minute = %s WHERE " \
                                             "id_circuit = %s AND ordre = %s "
                        tupple_update_etape = (id_lieu_etape, date_etape, duree_etape, id_circuit_etape, ordre_etape)
                        connexion_unique.commit(query_update_etape, tupple_update_etape)
                        return redirect(url_for('circuit_admin'))

                    # On verifie que l'utilisateur a cliquer sur le bouton supprimer
                    elif request.form['modifier_submit_etape'] == f'Supprimer{str_id}{n}':
                        lieu_etape = request.form[f'modifier_lieu_etape{str_id}{n}']
                        id_circuit_etape = request.form[f'modifier_id_circuit_etape{str_id}{n}']

                        # On recupere une requete factice, c'est-a-dire qui ne nous servira a rien, mais qui a juste
                        # etee implementer afin de creer la classe de notre formulaire
                        requete_factice = request.form['modifier_duree_etape1']

                        # On recupere l'id du lieu correspondant au label selectionne dans le select
                        query_id_lieu = "SELECT id FROM lieu WHERE label = %s "
                        lieu_etape_str = (str(lieu_etape),)
                        id_lieu_etape = connexion_unique.fetchone_arguments(query_id_lieu, lieu_etape_str)

                        # On supprime l'etape en fonction des informations recuperees par le formulaire
                        query_delete_etape = "DELETE FROM etape WHERE id_circuit = %s AND id_lieu = %s "
                        tupple_delete_etape = (id_circuit_etape, id_lieu_etape)
                        connexion_unique.commit(query_delete_etape, tupple_delete_etape)
                        return redirect(url_for('circuit_admin'))

        # On verifie si le formulaire pour ajouter une etape a ete envoyer
        elif ajouter_etape_formulaire.validate_on_submit():
            lieu_etape = request.form['ajouter_lieu_etape']
            duree_etape = request.form['ajouter_duree_etape']
            date_etape = request.form['ajouter_date_etape']
            id_circuit_etape = request.form['ajouter_id_circuit_etape']

            # On recupere une requete factice, c'est-a-dire qui ne nous servira a rien, mais qui a juste
            # etee implementer afin de creer la classe de notre formulaire
            requete_factice = request.form['ajouter_duree_etape1']

            # On recupere l'id du lieu correspondant au label selectionne dans le select
            query_id_lieu = "SELECT id FROM lieu WHERE label = %s "
            lieu_etape_str = (str(lieu_etape),)
            id_lieu_etape = connexion_unique.fetchone_arguments(query_id_lieu, lieu_etape_str)

            # On selectione la valeur de l'ordre la plus importante associee au circuit, si elle existe, et on lui
            # ajoute 1 afin que l'etape que l'on ajoute soit toujours la derniere
            query_ordre_maximum = "SELECT ordre FROM etape WHERE id_circuit = %s ORDER BY ordre DESC LIMIT 1"
            tupple_id_circuit_etape = (id_circuit_etape,)
            ordre_maximum = connexion_unique.fetchall_arguments(query_ordre_maximum, tupple_id_circuit_etape)
            longueur_ordre_maximum = len(ordre_maximum)
            if longueur_ordre_maximum != 0:
                ordre_maximum_etape = connexion_unique.fetchone_arguments(query_ordre_maximum, tupple_id_circuit_etape)
            else:
                ordre_maximum_etape = 0
            ordre_nouvelle_etape = ordre_maximum_etape + 1

            # On insert une nouvelle etape dans la base de donnees grace au informations du formulaire
            query_inserer_etape = "INSERT INTO etape (id_circuit, id_lieu, date, duree_en_minute, ordre) VALUES " \
                                  "(%s, %s, %s, %s, %s) "
            tupple_inserer_etape = (id_circuit_etape, id_lieu_etape, date_etape, duree_etape, ordre_nouvelle_etape)
            connexion_unique.commit(query_inserer_etape, tupple_inserer_etape)
            return redirect(url_for('circuit_admin'))

        # On verifie si le formulaire pour ajouter un circuit a ete envoyer
        elif ajouter_circuit_formulaire.validate_on_submit():
            nom_circuit = request.form['ajouter_nom_circuit']
            descriptif_circuit = request.form['ajouter_descriptif_circuit']
            prix_circuit = request.form['ajouter_prix_circuit']
            duree_circuit = request.form['ajouter_duree_circuit']
            date_depart_circuit = request.form['ajouter_datedepart_circuit']
            date_arrivee_circuit = request.form['ajouter_datearrivee_circuit']
            nb_place_circuit = request.form['ajouter_nbplace_circuit']
            ville_depart_circuit = request.form['ajouter_villedepart_circuit']
            ville_arrivee_circuit = request.form['ajouter_villearrivee_circuit']

            # On recupere l'id de la ville de depart a partir du nom selectionne dans le select
            query_id_villedepart = "SELECT id FROM ville WHERE nom = %s "
            tupple_id_villedepart = (ville_depart_circuit,)
            id_ville_depart = connexion_unique.fetchone_arguments(query_id_villedepart, tupple_id_villedepart)

            # On recupere l'id de la ville d'arrivee a partir du nom selectionne dans le select
            query_id_villearrivee = "SELECT id FROM ville WHERE nom = %s "
            tupple_id_villearrivee = (ville_arrivee_circuit,)
            id_ville_arrivee = connexion_unique.fetchone_arguments(query_id_villearrivee, tupple_id_villearrivee)

            # On insert un nouveau circuit dans la base de donnees a partir des informations du formulaire
            query_inserer_circuit = "INSERT INTO circuit (nom, descriptif, prix_circuit, duree_jour, ville_depart, " \
                                    "ville_arrivee, nb_place, date_depart, date_arrivee) VALUES (%s, %s, %s, %s, %s, " \
                                    "%s, %s, %s, %s) "
            tupple_inserer_circuit = (nom_circuit, descriptif_circuit, prix_circuit, duree_circuit, id_ville_depart,
                                      id_ville_arrivee, nb_place_circuit, date_depart_circuit, date_arrivee_circuit)
            connexion_unique.commit(query_inserer_circuit, tupple_inserer_circuit)
            return redirect(url_for('circuit_admin'))

        # On verifie si le formulaire pour modifier un circuit a ete envoyer
        elif modifier_circuit_formulaire.validate_on_submit():

            # On verifie que l'utilisateur a cliquer sur le bouton modifier
            if request.form['modifier_submit_circuit'] == 'Modifier':
                id_circuit = request.form['modifier_id_circuit']
                nom_circuit = request.form['modifier_nom_circuit']
                descriptif_circuit = request.form['modifier_descriptif_circuit']
                prix_circuit = request.form['modifier_prix_circuit']
                duree_circuit = request.form['modifier_duree_circuit']
                nb_place_circuit = request.form['modifier_nbplace_circuit']
                date_depart_circuit = request.form['modifier_datedepart_circuit']
                date_arrivee_circuit = request.form['modifier_datearrivee_circuit']
                ville_depart_circuit = request.form['modifier_villedepart_circuit']
                ville_arrivee_circuit = request.form['modifier_villearrivee_circuit']
                id_circuit_int = int(id_circuit)

                # On recupere l'id de la ville de depart a partir du nom selectionne dans le select
                query_id_villedepart = "SELECT id FROM ville WHERE nom = %s "
                tupple_id_villedepart = (ville_depart_circuit,)
                id_ville_depart = connexion_unique.fetchone_arguments(query_id_villedepart, tupple_id_villedepart)

                # On recupere l'id de la ville d'arrivee a partir du nom selectionne dans le select
                query_id_villearrivee = "SELECT id FROM ville WHERE nom = %s "
                tupple_id_villearrivee = (ville_arrivee_circuit,)
                id_ville_arrivee = connexion_unique.fetchone_arguments(query_id_villearrivee, tupple_id_villearrivee)

                # On met a jour le circuit en fonction des informations du formulaire
                query_update_circuit = "UPDATE circuit SET nom = %s, descriptif = %s, prix_circuit = %s, duree_jour= " \
                                       "%s, nb_place= %s, date_depart = %s, date_arrivee= %s, ville_depart = %s, " \
                                       "ville_arrivee = %s WHERE id = %s "
                tupple_update_circuit = (nom_circuit, descriptif_circuit, prix_circuit, duree_circuit, nb_place_circuit,
                                         date_depart_circuit, date_arrivee_circuit, id_ville_depart, id_ville_arrivee,
                                         id_circuit_int)
                connexion_unique.commit(query_update_circuit, tupple_update_circuit)
                return redirect(url_for('circuit_admin'))

            # On verifie que l'utilisateur a cliquer sur le bouton supprimer
            elif request.form['modifier_submit_circuit'] == 'Supprimer':
                id_circuit = request.form['modifier_id_circuit']

                # On supprime le circuit grace aux informations du formulaire
                query_delete_circuit = "DELETE FROM circuit WHERE id = %s "
                tupple_delete_circuit = (id_circuit,)
                connexion_unique.commit(query_delete_circuit, tupple_delete_circuit)
                return redirect(url_for('circuit_admin'))
        return render_template('/circuit_admin.html', ajouter_circuit_formulaire=ajouter_circuit_formulaire,
                               modifier_circuit_formulaire=modifier_circuit_formulaire, liste_circuit_etape=liste_circuit_etape,
                               liste_nom_villes=liste_nom_villes, liste_label_lieux=liste_label_lieux, liste_utile=liste_utile,
                               modifier_etape_formulaire=modifier_etape_formulaire,
                               ajouter_etape_formulaire=ajouter_etape_formulaire)
    else:
        return redirect(url_for('index'))

@app.route('/utilisateur', methods=['GET', 'POST'])
def utilisateur():
    if session['role'] == 1:
        connexion_unique = Database.Instance()

        class AjouterUtilisateurFormulaire(FlaskForm):
            ajouter_roleadmin_utilisateur = IntegerField(validators=[DataRequired()])
            ajouter_nom_utilisateur = StringField(validators=[DataRequired()])
            ajouter_prenom_utilisateur = StringField(validators=[DataRequired()])
            ajouter_datenaissance_utilisateur = DateField(validators=[DataRequired()])
            ajouter_login_utilisateur = StringField(validators=[DataRequired()])
            ajouter_email_utilisateur = EmailField(validators=[DataRequired()])
            ajouter_mdp_utilisateur = StringField(validators=[DataRequired()])

        class ModifierUtilisateurFormulaire(FlaskForm):
            modifier_id_utilisateur = IntegerField(validators=[DataRequired()])
            modifier_roleadmin_utilisateur = IntegerField(validators=[DataRequired()])
            modifier_nom_utilisateur = StringField(validators=[DataRequired()])
            modifier_prenom_utilisateur = StringField(validators=[DataRequired()])
            modifier_datenaissance_utilisateur = DateField(validators=[DataRequired()])
            modifier_login_utilisateur = StringField(validators=[DataRequired()])
            modifier_email_utilisateur = EmailField(validators=[DataRequired()])

        class ModifierReservationFormulaire(FlaskForm):
            fake = StringField(validators=[DataRequired()])

        class AjouterReservationFormulaire(FlaskForm):
            faker = StringField(validators=[DataRequired()])

        query_informations_utilisateur = "SELECT id, role_admin, nom, prenom, date_naissance, login, email FROM " \
                                         "utilisateur "
        informations_utilisateur = connexion_unique.fetchall_simple(query_informations_utilisateur)
        query_nom_circuits = "SELECT nom FROM circuit"
        liste_nom_circuits = connexion_unique.fetchall_simple(query_nom_circuits)
        query_id_utilisateurs = "SELECT id FROM utilisateur ORDER BY id"
        id_utilisateurs = connexion_unique.fetchall_simple(query_id_utilisateurs)
        liste_information_reservations = []
        for id in id_utilisateurs:
            query_informations_reservation = "SELECT reservation.id_circuit, reservation.id_utilisateur, " \
                                             "reservation.nb_place, circuit.nom, reservation.date, reservation.heure " \
                                             "FROM circuit JOIN reservation ON circuit.id = reservation.id_circuit " \
                                             "JOIN utilisateur ON reservation.id_utilisateur = utilisateur.id WHERE " \
                                             "utilisateur.id = '%s' "
            id_str = (str(id)[1:-2])
            id_int = int(id_str)
            id_tupple = (id_int,)
            informations_reservation = connexion_unique.fetchall_arguments(query_informations_reservation, id_tupple)
            liste_information_reservations.append(informations_reservation)
        tupple_information_reservations = [tuple(x) for x in liste_information_reservations]
        tupple_utilisateur_reservation = map(add, informations_utilisateur, tupple_information_reservations)
        liste_utilisateur_reservation = [list(x) for x in tupple_utilisateur_reservation]
        liste_utile = list(range(7, 25))
        ajouter_utilisateur_formulaire = AjouterUtilisateurFormulaire()
        modifier_utilisateur_formulaire = ModifierUtilisateurFormulaire()
        modifier_reservation_formulaire = ModifierReservationFormulaire()
        ajouter_reservation_formulaire = AjouterReservationFormulaire()
        if ajouter_reservation_formulaire.validate_on_submit():
            id_circuit = request.form['ajouter_circuit_reservation']
            date_reservation = request.form['ajouter_date_reservation']
            heure_reservation = request.form['ajouter_heure_reservation']
            nbplace_reservation = request.form['ajouter_nbplace_reservation']
            id_utilisateur_reservation = request.form['ajouter_id_utilisateur_reservation']
            requete_factice = request.form['faker']
            query_id_circuit = "SELECT id FROM circuit WHERE nom = %s "
            tupple_id_circuit = (id_circuit,)
            id_circuit_reservation = connexion_unique.fetchone_arguments(query_id_circuit, tupple_id_circuit)
            query_inserer_reservation = "INSERT INTO reservation (id_circuit, id_utilisateur, nb_place, date, heure) " \
                                        "VALUES (%s, %s, %s, %s, %s) "
            tupple_inserer_reservation = (id_circuit_reservation, id_utilisateur_reservation, nbplace_reservation,
                                          date_reservation, heure_reservation)
            connexion_unique.commit(query_inserer_reservation, tupple_inserer_reservation)
            return redirect(url_for('utilisateur'))
        elif modifier_reservation_formulaire.validate_on_submit():
            for id in id_utilisateurs:
                str_id = str(id)[1:-2]
                for n in liste_utile:
                    if request.form['modifier_submit_reservation'] == f'Modifier{str_id}{n}':
                        nom_circuit_reservation = request.form[f'modifier_circuit_reservation{str_id}{n}']
                        date_reservation = request.form[f'modifier_date_reservation{str_id}{n}']
                        heure_reservation = request.form[f'modifier_heure_reservation{str_id}{n}']
                        nbplace_reservation = request.form[f'modifier_nbplace_reservation{str_id}{n}']
                        id_circuit = request.form[f'modifier_id_circuit_reservation{str_id}{n}']
                        id_utilisateur_reservation = request.form[f'modifier_id_utilisateur_reservation{str_id}{n}']
                        requete_factice = request.form['fake']
                        query_id_circuit = "SELECT id FROM circuit WHERE nom = %s "
                        tupple_nom_circuit = (nom_circuit_reservation,)
                        id_circuit_reservation = connexion_unique.fetchone_arguments(query_id_circuit, tupple_nom_circuit)
                        query_update_reservation = "UPDATE reservation SET id_circuit = %s, nb_place = %s, date = %s, " \
                                                   "heure = %s WHERE id_circuit = %s AND id_utilisateur = %s "
                        tupple_update_reservation = (id_circuit_reservation, nbplace_reservation, date_reservation,
                                                     heure_reservation, id_circuit_reservation, id_utilisateur_reservation)
                        connexion_unique.commit(query_update_reservation, tupple_update_reservation)
                        return redirect(url_for('utilisateur'))
                    elif request.form['modifier_submit_reservation'] == f'Supprimer{str_id}{n}':
                        id_circuit = request.form[f'modifier_id_circuit_reservation{str_id}{n}']
                        id_utilisateur_reservation = request.form[f'modifier_id_utilisateur_reservation{str_id}{n}']
                        requete_factice = request.form['fake']
                        query_delete_reservation = "DELETE FROM reservation WHERE id_circuit = %s AND id_utilisateur = %s "
                        tupple_delete_reservation = (id_circuit, id_utilisateur_reservation)
                        connexion_unique.commit(query_delete_reservation, tupple_delete_reservation)
                        return redirect(url_for('utilisateur'))
        elif ajouter_utilisateur_formulaire.validate_on_submit():
            role_admin_utilisateur = request.form['ajouter_roleadmin_utilisateur']
            nom_utilisateur = request.form['ajouter_nom_utilisateur']
            prenom_utilisateur = request.form['ajouter_prenom_utilisateur']
            date_naissance_utilisateur = request.form['ajouter_datenaissance_utilisateur']
            login_utilisateur = request.form['ajouter_login_utilisateur']
            email_utilisateur = request.form['ajouter_email_utilisateur']
            mdp_utilisateur = request.form['ajouter_mdp_utilisateur']
            sel = bcrypt.gensalt()
            mdp = mdp_utilisateur.encode(encoding='UTF-8', errors='strict')
            mdp_crypter = bcrypt.hashpw(mdp, sel)
            query_inserer_utilisateur = "INSERT INTO utilisateur (role_admin, nom, prenom, date_naissance, login, " \
                                        "email, mdp) VALUES (%s, %s, %s, %s, %s, %s, %s) "
            tupple_inserer_utilisateur = (role_admin_utilisateur, nom_utilisateur, prenom_utilisateur,
                                          date_naissance_utilisateur, login_utilisateur, email_utilisateur, mdp_crypter)
            connexion_unique.commit(query_inserer_utilisateur, tupple_inserer_utilisateur)
            return redirect(url_for('utilisateur'))
        elif modifier_utilisateur_formulaire.validate_on_submit():
            if request.form['modifier_submit_utilisateur'] == 'Modifier':
                id_utilisateur = request.form['modifier_id_utilisateur']
                role_admin_utilisateur = request.form['modifier_roleadmin_utilisateur']
                nom_utilisateur = request.form['modifier_nom_utilisateur']
                prenom_utilisateur = request.form['modifier_prenom_utilisateur']
                date_naissance_utilisateur = request.form['modifier_datenaissance_utilisateur']
                login_utilisateur = request.form['modifier_login_utilisateur']
                email_utilisateur = request.form['modifier_email_utilisateur']
                query_update_utilisateur = "UPDATE utilisateur SET role_admin = %s, nom = %s, prenom = %s, " \
                                           "date_naissance = %s, login = %s, email = %s WHERE id = %s "
                tupple_update_utilisateur = (role_admin_utilisateur, nom_utilisateur, prenom_utilisateur,
                                             date_naissance_utilisateur, login_utilisateur, email_utilisateur,
                                             id_utilisateur)
                connexion_unique.commit(query_update_utilisateur, tupple_update_utilisateur)
                return redirect(url_for('utilisateur'))
            elif request.form['modifier_submit_utilisateur'] == 'Supprimer':
                id_utilisateur = request.form['modifier_id_utilisateur']
                role_admin_utilisateur = request.form['modifier_roleadmin_utilisateur']
                nom_utilisateur = request.form['modifier_nom_utilisateur']
                prenom_utilisateur = request.form['modifier_prenom_utilisateur']
                date_naissance_utilisateur = request.form['modifier_datenaissance_utilisateur']
                login_utilisateur = request.form['modifier_login_utilisateur']
                email_utilisateur = request.form['modifier_email_utilisateur']
                query_delete_utilisateur = "DELETE FROM utilisateur WHERE id = %s "
                tupple_delete_utilisateur = (id_utilisateur,)
                connexion_unique.commit(query_delete_utilisateur, tupple_delete_utilisateur)
                return redirect(url_for('utilisateur'))

        return render_template('/utilisateur.html', modifier_utilisateur_formulaire=modifier_utilisateur_formulaire,
                               liste_utilisateur_reservation=liste_utilisateur_reservation,
                               ajouter_utilisateur_formulaire=ajouter_utilisateur_formulaire,
                               liste_nom_circuits=liste_nom_circuits, liste_utile=liste_utile,
                               modifier_reservation_formulaire=modifier_reservation_formulaire,
                               ajouter_reservation_formulaire=ajouter_reservation_formulaire)
    else:
         return redirect(url_for('index'))

@app.route('/pays', methods=['GET', 'POST'])
def pays():
    if session['role'] == 1:
        connexion_unique = Database.Instance()

        class ajouter_pays_form(FlaskForm):
            nom_pays = StringField('nom pays', validators=[DataRequired()])

        class modifier_pays_form(FlaskForm):
            nom_pays_existant = StringField('nom pays', validators=[DataRequired()])
            id_pays_existant = StringField('id pays', validators=[DataRequired()])

        query39 = "SELECT id, nom FROM pays "
        yio = connexion_unique.fetchall_simple(query39)
        form = ajouter_pays_form()
        forml = modifier_pays_form()
        if form.validate_on_submit():
            pays_nom = request.form['nom_pays']
            query38 = "INSERT INTO pays (nom) VALUES (%s) "
            mip = (pays_nom,)
            connexion_unique.commit(query38, mip)
            return redirect(url_for('pays'))
        if forml.validate_on_submit():
            if request.form['tu'] == 'GO':
                pays_nom_existant = request.form['nom_pays_existant']
                pays_id_existant = request.form['id_pays_existant']
                query40 = "UPDATE pays SET nom = %s WHERE id = %s "
                migos = (pays_nom_existant, pays_id_existant)
                connexion_unique.commit(query40, migos)
                return redirect(url_for('pays'))
            elif request.form['tu'] == 'Delete':
                pays_nom_existant = request.form['nom_pays_existant']
                pays_id_existant = request.form['id_pays_existant']
                query41 = "DELETE FROM pays WHERE id = %s "
                pute = (pays_id_existant,)
                connexion_unique.commit(query41, pute)
                return redirect(url_for('pays'))

        return render_template('/pays.html', form=form, your_list=yio, forml=forml)
    else:
        return redirect(url_for('index'))

@app.route('/ville', methods=['GET', 'POST'])
def ville():
    if session['role'] == 1:
        connexion_unique = Database.Instance()

        class ajouter_ville_form(FlaskForm):
            nom_ville = StringField('nom ville', validators=[DataRequired()])

        class modifier_ville_form(FlaskForm):
            nom_ville_existant = StringField('nom ville', validators=[DataRequired()])
            id_ville_existant = StringField('id ville', validators=[DataRequired()])

        query42 = "SELECT nom FROM pays "
        yiop = connexion_unique.fetchall_simple(query42)
        query39 = "SELECT ville.id, ville.nom, pays.nom FROM ville JOIN pays ON ville.id_pays = pays.id"
        yio = connexion_unique.fetchall_simple(query39)
        form = ajouter_ville_form()
        forml = modifier_ville_form()
        if form.validate_on_submit():
            ville_nom = request.form['nom_ville']
            ville_pays = request.form['liop']
            query43 = "SELECT id FROM pays WHERE nom = %s "
            crop = (ville_pays,)
            ji = connexion_unique.fetchone_arguments(query43, crop)
            query44 = "INSERT INTO ville (nom, id_pays) VALUES (%s, %s) "
            puff = (ville_nom, ji)
            connexion_unique.commit(query44, puff)
            return redirect(url_for('ville'))
        if forml.validate_on_submit():
            if request.form['tut'] == 'GO':
                nom_ville_existant = request.form['nom_ville_existant']
                id_ville_existant = request.form['id_ville_existant']
                nom_pays_ville_existant = request.form['liopo']
                query45 = "SELECT id FROM pays WHERE nom = %s "
                trip = (nom_pays_ville_existant,)
                lo = connexion_unique.fetchone_arguments(query45, trip)
                query46 = "UPDATE ville SET nom = %s, id_pays = %s WHERE id = %s "
                op = (nom_ville_existant, lo, id_ville_existant)
                connexion_unique.commit(query46, op)
                return redirect(url_for('ville'))
            elif request.form['tut'] == 'Delete':
                nom_ville_existant = request.form['nom_ville_existant']
                id_ville_existant = request.form['id_ville_existant']
                query47 = "DELETE FROM ville WHERE id = %s "
                fuark = (id_ville_existant,)
                connexion_unique.commit(query47, fuark)
                return redirect(url_for('ville'))

        return render_template('/ville.html', form=form, your_list=yio, forml=forml, liste=yiop)
    else:
        return redirect(url_for('index'))

@app.route('/lieu_admin', methods=['GET', 'POST'])
def lieu_admin():
    if session['role'] == 1:
        connexion_unique = Database.Instance()

        class AjouterLieuFormulaire(FlaskForm):
            ajouter_label_lieu = StringField(validators=[DataRequired()])
            ajouter_description_lieu = StringField(validators=[DataRequired()])
            ajouter_prix_lieu = DecimalField(validators=[DataRequired()])

        class ModifierLieuFormulaire(FlaskForm):
            modifier_label_lieu = StringField(validators=[DataRequired()])
            modifier_description_lieu = StringField(validators=[DataRequired()])
            modifier_prix_lieu = DecimalField(validators=[DataRequired()])
            modifier_id_lieu = IntegerField(validators=[DataRequired()])

        query_nom_villes = "SELECT nom FROM ville "
        liste_nom_villes = connexion_unique.fetchall_simple(query_nom_villes)
        query_informations_lieu = "SELECT lieu.id, lieu.label, lieu.description, lieu.prix_visite, ville.nom FROM " \
                                  "lieu JOIN ville ON lieu.id_ville = ville.id "
        liste_lieu = connexion_unique.fetchall_simple(query_informations_lieu)
        ajouter_lieu_formulaire = AjouterLieuFormulaire()
        modifier_lieu_formulaire = ModifierLieuFormulaire()
        if ajouter_lieu_formulaire.validate_on_submit():
            label_lieu = request.form['ajouter_label_lieu']
            description_lieu = request.form['ajouter_description_lieu']
            prix_lieu = request.form['ajouter_prix_lieu']
            nom_ville_lieu = request.form['ajouter_ville_lieu']
            query_id_ville = "SELECT id FROM ville WHERE nom = %s "
            tupple_nom_ville = (nom_ville_lieu,)
            id_ville_lieu = connexion_unique.fetchone_arguments(query_id_ville, tupple_nom_ville)
            query_inserer_lieu = "INSERT INTO lieu (id_ville, label, description, prix_visite) VALUES (%s, %s, %s, %s) "
            tupple_inserer_lieu = (id_ville_lieu, label_lieu, description_lieu, prix_lieu)
            connexion_unique.commit(query_inserer_lieu, tupple_inserer_lieu)
            return redirect(url_for('lieu_admin'))
        if modifier_lieu_formulaire.validate_on_submit():
            if request.form['modifier_submit_lieu'] == 'Modifier':
                id_lieu = request.form['modifier_id_lieu']
                label_lieu = request.form['modifier_label_lieu']
                description_lieu = request.form['modifier_description_lieu']
                prix_lieu = request.form['modifier_prix_lieu']
                nom_ville_lieu = request.form['modifier_ville_lieu']
                query_id_villes = "SELECT id FROM ville WHERE nom = %s "
                tupple_nom_ville = (nom_ville_lieu,)
                id_ville_lieu = connexion_unique.fetchone_arguments(query_id_villes, tupple_nom_ville)
                query_update_lieu = "UPDATE lieu SET label = %s, id_ville = %s, description = %s, prix_visite = %s " \
                                    "WHERE id = %s "
                tupple_update_lieu = (label_lieu, id_ville_lieu, description_lieu, prix_lieu, id_lieu)
                connexion_unique.commit(query_update_lieu, tupple_update_lieu)
                return redirect(url_for('lieu_admin'))
            elif request.form['modifier_submit_lieu'] == 'Supprimer':
                id_lieu = request.form['modifier_id_lieu']
                label_lieu = request.form['modifier_label_lieu']
                description_lieu = request.form['modifier_description_lieu']
                prix_lieu = request.form['modifier_prix_lieu']
                print(id_lieu)
                query_delete_lieu = "DELETE FROM lieu WHERE id = %s "
                tupple_delete_lieu = (id_lieu,)
                connexion_unique.commit(query_delete_lieu, tupple_delete_lieu)
                return redirect(url_for('lieu_admin'))

        return render_template('/lieu_admin.html', modifier_lieu_formulaire=modifier_lieu_formulaire,
                               liste_nom_villes=liste_nom_villes, ajouter_lieu_formulaire=ajouter_lieu_formulaire,
                               liste_lieu=liste_lieu)
    else:
        return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)