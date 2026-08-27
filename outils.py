import datetime
import os

import openpyxl


def lister_exports(dossier):
    exports = []
    for nom_fichier in os.listdir(dossier):
        if nom_fichier.startswith("export_") and nom_fichier.endswith(".xlsx"):
            texte_date = nom_fichier[7:17]  # ex: "2025-09-01"
            annee = int(texte_date[0:4])
            mois = int(texte_date[5:7])
            jour = int(texte_date[8:10])
            date_export = datetime.date(annee, mois, jour)
            chemin_complet = os.path.join(dossier, nom_fichier)
            exports.append((date_export, chemin_complet))

    return sorted(exports)


def fichiers_dans_plage(exports_disponibles, date_debut, date_fin):
    fichiers = []
    for date_export, chemin in exports_disponibles:
        if date_debut <= date_export <= date_fin:
            fichiers.append(chemin)
    return fichiers


def charger_periode(fichiers):
    tous_les_tickets = []
    for chemin in fichiers:
        tous_les_tickets.extend(charger_tickets(chemin))
    return tous_les_tickets


def texte_horaires_jour(plages):
    if len(plages) == 0:
        return "-"

    premier_debut, premiere_fin = plages[0]
    texte = str(premier_debut) + "h-" + str(premiere_fin) + "h"

    for i in range(1, len(plages)):
        debut, fin = plages[i]
        texte = texte + " / " + str(debut) + "h-" + str(fin) + "h"

    return texte


def charger_commandes(chemin):
    classeur = openpyxl.load_workbook(chemin, data_only=True)
    feuille = classeur["ORDERS"]

    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    commandes = {}
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        commande = {}
        for i in range(len(entetes)):
            commande[entetes[i]] = ligne[i]
        commandes[commande["order_id"]] = commande

    return commandes


def montant_ticket(ticket, commandes):
    order_id = ticket["order_id"]
    if order_id is None or order_id not in commandes:
        return None
    return commandes[order_id]["montant_total"]


# Le montant total de la commande n'est pas le coût réel pour l'entreprise :
# un remboursement rend le prix payé, mais un remplacement ou un geste commercial
# ne coûtent qu'une fraction du prix de vente (coût matière/logistique, pas le
# panier complet). Ces fractions évitent de gonfler artificiellement les pertes.
FRACTION_REMBOURSEMENT = 1.0
FRACTION_REMPLACEMENT = 0.35
FRACTION_GESTE_COMMERCIAL = 0.15

FRACTIONS_PERTE = {
    "Remboursement": FRACTION_REMBOURSEMENT,
    "Remplacement produit": FRACTION_REMPLACEMENT,
    "Remplacement accessoire": FRACTION_REMPLACEMENT,
    "Geste commercial": FRACTION_GESTE_COMMERCIAL,
}


def montant_perte_estime(ticket, commandes, type_perte):
    montant_commande = montant_ticket(ticket, commandes)
    if montant_commande is None:
        return None
    fraction = FRACTIONS_PERTE.get(type_perte, 1.0)
    return montant_commande * fraction


def montant_cout_garantie(ticket, commandes):
    montant_commande = montant_ticket(ticket, commandes)
    if montant_commande is None:
        return None
    return montant_commande * FRACTION_REMPLACEMENT


def formater_montant(valeur):
    return str(round(valeur)) + " €"


def commandes_par_email(commandes):
    par_email = {}
    for order_id in commandes:
        commande = commandes[order_id]
        email = commande["email_client"]
        if email in par_email:
            par_email[email].append(commande)
        else:
            par_email[email] = [commande]
    return par_email


def premiere_commande_apres(ticket, index_par_email, fenetre_jours):
    email = ticket["requester_email"]
    commandes_client = index_par_email.get(email, [])

    date_debut = ticket["created_at"]
    date_fin = date_debut + datetime.timedelta(days=fenetre_jours)

    candidates = []
    for commande in commandes_client:
        if date_debut < commande["order_date"] <= date_fin:
            candidates.append(commande)

    if len(candidates) == 0:
        return None

    def obtenir_date(commande):
        return commande["order_date"]

    candidates_triees = sorted(candidates, key=obtenir_date)
    return candidates_triees[0]


def charger_nps(chemin):
    classeur = openpyxl.load_workbook(chemin, data_only=True)
    feuille = classeur["NPS"]

    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    reponses = []
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        reponse = {}
        for i in range(len(entetes)):
            reponse[entetes[i]] = ligne[i]
        reponses.append(reponse)

    return reponses


def calculer_nps(reponses):
    if len(reponses) == 0:
        return None

    promoteurs = 0
    detracteurs = 0

    for reponse in reponses:
        score = reponse["score"]
        if score >= 9:
            promoteurs = promoteurs + 1
        elif score <= 6:
            detracteurs = detracteurs + 1

    return (promoteurs - detracteurs) / len(reponses) * 100


def extraire_code_macro(texte):
    if texte is None:
        return None

    debut = texte.find("MAC-")
    if debut == -1:
        return None

    fin = debut + 4
    while fin < len(texte) and texte[fin].isdigit():
        fin = fin + 1

    return texte[debut:fin]


def charger_texte_macro(code, dossier_macros):
    if code is None:
        return None

    chemin = os.path.join(dossier_macros, code + ".md")
    if not os.path.exists(chemin):
        return None

    with open(chemin, "r", encoding="utf-8") as fichier:
        return fichier.read()


def extraire_nom_fichier_faq(texte_macro):
    if texte_macro is None:
        return None

    marqueur = "knowledge_base/faq/"
    debut = texte_macro.find(marqueur)
    if debut == -1:
        return None

    debut = debut + len(marqueur)
    fin = debut
    while fin < len(texte_macro) and texte_macro[fin] not in (" ", "\n", "\r"):
        fin = fin + 1

    return texte_macro[debut:fin]


def charger_texte_faq(nom_fichier, dossier_faq):
    if nom_fichier is None:
        return None

    chemin = os.path.join(dossier_faq, nom_fichier)
    if not os.path.exists(chemin):
        return None

    with open(chemin, "r", encoding="utf-8") as fichier:
        return fichier.read()


def charger_calendrier_evenements(chemin):
    if not os.path.exists(chemin):
        return []

    classeur = openpyxl.load_workbook(chemin, data_only=True)
    if "EVENEMENTS" not in classeur.sheetnames:
        return []

    feuille = classeur["EVENEMENTS"]
    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    evenements = []
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        evenement = {}
        for i in range(len(entetes)):
            valeur = ligne[i]
            if isinstance(valeur, datetime.datetime):
                valeur = valeur.date()
            evenement[entetes[i]] = valeur
        evenements.append(evenement)

    return evenements


def evenements_dans_periode(evenements, date_debut, date_fin):
    evenements_periode = []
    for evenement in evenements:
        if evenement["date_debut"] <= date_fin and evenement["date_fin"] >= date_debut:
            evenements_periode.append(evenement)
    return evenements_periode


def charger_suivi_suggestions(chemin):
    if not os.path.exists(chemin):
        return {}

    classeur = openpyxl.load_workbook(chemin, data_only=True)
    if "SUIVI" not in classeur.sheetnames:
        return {}

    feuille = classeur["SUIVI"]
    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    if "sujet" not in entetes:
        return {}

    idx_sujet = entetes.index("sujet")
    idx_statut = entetes.index("statut")
    idx_date = entetes.index("date_action")
    idx_notes = entetes.index("notes")

    suivi = {}
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        sujet = ligne[idx_sujet]
        if sujet is None:
            continue

        date_action = ligne[idx_date]
        if isinstance(date_action, datetime.datetime):
            date_action = date_action.date()

        suivi[sujet] = {
            "statut": ligne[idx_statut],
            "date_action": date_action,
            "notes": ligne[idx_notes],
        }

    return suivi


def impact_avant_apres(tickets_sujet, date_action):
    avant = []
    apres = []
    for ticket in tickets_sujet:
        date_ticket = ticket["created_at"]
        if isinstance(date_ticket, datetime.datetime):
            date_ticket = date_ticket.date()

        if date_ticket < date_action:
            avant.append(ticket)
        else:
            apres.append(ticket)

    return {
        "volume_avant": len(avant),
        "volume_apres": len(apres),
        "csat_avant": moyenne(avant, "csat"),
        "csat_apres": moyenne(apres, "csat"),
        "macro_avant": taux_rempli(avant, "macro_applied"),
        "macro_apres": taux_rempli(apres, "macro_applied"),
    }


def charger_tickets(chemin):
    classeur = openpyxl.load_workbook(chemin, data_only=True)
    feuille = classeur["RAW_TICKETS"]

    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    tickets = []
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        ticket = {}
        for i in range(len(entetes)):
            ticket[entetes[i]] = ligne[i]
        tickets.append(ticket)

    return tickets


def delai_jours(date_debut, date_fin):
    difference = date_fin - date_debut
    return difference.days


def niveau_anciennete_defaut(jours):
    if jours < 30:
        return "Défaut précoce (< 30j)"
    elif jours < 180:
        return "Défaut intermédiaire (30-180j)"
    else:
        return "Usure normale probable (> 180j)"


def evolution_pourcentage(ancienne_valeur, nouvelle_valeur):
    difference = nouvelle_valeur - ancienne_valeur
    return difference / ancienne_valeur * 100


def moyenne(tickets, champ):
    valeurs = []
    for ticket in tickets:
        if ticket[champ] is not None:
            valeurs.append(ticket[champ])

    if len(valeurs) == 0:
        return None

    return sum(valeurs) / len(valeurs)


def taux_rempli(tickets, champ):
    if len(tickets) == 0:
        return None

    nombre_rempli = 0
    for ticket in tickets:
        if ticket[champ] is not None:
            nombre_rempli = nombre_rempli + 1
    return nombre_rempli / len(tickets) * 100


def evenements_periode(tickets):
    evenements = []
    for ticket in tickets:
        valeur = ticket["evenement_semaine"]
        if valeur is not None and valeur not in evenements:
            evenements.append(valeur)

    if len(evenements) == 0:
        return "Non renseigné"

    texte = evenements[0]
    for i in range(1, len(evenements)):
        texte = texte + " | " + evenements[i]
    return texte


SEUIL_DEBORDEMENT_MIN = 480  # au-delà, on suppose que la réponse a débordé hors créneau

NOM_AGENT_DEFAUT = "DEFAUT"  # horaires utilisés pour un agent absent du planning

# Horaires de secours si le fichier n'a pas d'onglet PLANNING (ex : anciens exports).
HORAIRES_PAR_DEFAUT = {
    0: [(10, 12), (13, 17)],
    1: [(10, 12), (13, 17)],
    2: [(10, 12), (13, 17)],
    3: [(10, 12), (13, 17)],
    4: [(10, 12), (13, 17)],
    5: [],
    6: [],
}

JOURS_SEMAINE = {
    "Lundi": 0,
    "Mardi": 1,
    "Mercredi": 2,
    "Jeudi": 3,
    "Vendredi": 4,
    "Samedi": 5,
    "Dimanche": 6,
}


def charger_planning(chemin):
    classeur = openpyxl.load_workbook(chemin, data_only=True)

    if "PLANNING" not in classeur.sheetnames:
        return {NOM_AGENT_DEFAUT: HORAIRES_PAR_DEFAUT}

    feuille = classeur["PLANNING"]
    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)
    idx_agent = entetes.index("agent")
    idx_jour = entetes.index("jour")
    idx_debut = entetes.index("heure_debut")
    idx_fin = entetes.index("heure_fin")

    planning = {}

    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        agent = ligne[idx_agent]
        jour_texte = ligne[idx_jour]
        heure_debut = ligne[idx_debut]
        heure_fin = ligne[idx_fin]
        jour_numero = JOURS_SEMAINE[jour_texte]

        if agent not in planning:
            planning[agent] = {}
        if jour_numero not in planning[agent]:
            planning[agent][jour_numero] = []

        planning[agent][jour_numero].append((heure_debut, heure_fin))

    return planning


def charger_roles_planning(chemin):
    classeur = openpyxl.load_workbook(chemin, data_only=True)

    if "PLANNING" not in classeur.sheetnames:
        return {}

    feuille = classeur["PLANNING"]
    entetes = []
    for cellule in feuille[1]:
        entetes.append(cellule.value)

    if "role" not in entetes:
        return {}

    idx_agent = entetes.index("agent")
    idx_role = entetes.index("role")

    roles = {}
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        agent = ligne[idx_agent]
        role = ligne[idx_role]
        if role is not None and agent not in roles:
            roles[agent] = role

    return roles


def detecter_changements_planning(agents_s1, agents_s2, planning_s1, planning_s2):
    changements = []

    for agent in agents_s2:
        if agent not in agents_s1:
            changements.append("Nouvel agent : " + agent)

    for agent in agents_s1:
        if agent not in agents_s2:
            changements.append("Agent absent cette période : " + agent)

    for agent in agents_s2:
        if agent in agents_s1:
            horaires_avant = horaires_agent(planning_s1, agent)
            horaires_apres = horaires_agent(planning_s2, agent)
            if horaires_avant != horaires_apres:
                changements.append("Horaires modifiés : " + agent)

    return changements


def horaires_agent(planning, agent):
    if agent in planning:
        return planning[agent]
    return planning.get(NOM_AGENT_DEFAUT, HORAIRES_PAR_DEFAUT)


def construire_plannings_periode(fichiers, exports_disponibles):
    dates_par_fichier = {}
    for date_export, chemin in exports_disponibles:
        dates_par_fichier[chemin] = date_export

    plannings_periode = []
    for chemin in fichiers:
        date_debut_fichier = dates_par_fichier[chemin]
        date_fin_fichier = date_debut_fichier + datetime.timedelta(days=6)
        planning_fichier = charger_planning(chemin)
        plannings_periode.append((date_debut_fichier, date_fin_fichier, planning_fichier))

    return plannings_periode


def planning_pour_date(plannings_periode, date_cible):
    for date_debut, date_fin, planning in plannings_periode:
        if date_debut <= date_cible <= date_fin:
            return planning

    if len(plannings_periode) > 0:
        return plannings_periode[-1][2]

    return {NOM_AGENT_DEFAUT: HORAIRES_PAR_DEFAUT}


def horaires_agent_periode(plannings_periode, agent, date_cible):
    planning_actif = planning_pour_date(plannings_periode, date_cible)
    return horaires_agent(planning_actif, agent)


def type_creneau(moment, agent, plannings_periode):
    plages_du_jour = horaires_agent_periode(plannings_periode, agent, moment.date()).get(moment.weekday(), [])

    for debut, fin in plages_du_jour:
        if debut <= moment.hour < fin:
            return "En créneau"

    if len(plages_du_jour) > 0:
        premiere_plage_debut = plages_du_jour[0][0]
        derniere_plage_fin = plages_du_jour[-1][1]
        if premiere_plage_debut <= moment.hour < derniere_plage_fin:
            return "Pause déjeuner"

    return "Hors créneau (soir/nuit/week-end)"


def type_hors_creneau_detaille(moment, agent, plannings_periode):
    jour = moment.weekday()

    if jour == 5:
        return "Samedi"
    elif jour == 6:
        return "Dimanche"

    plages_du_jour = horaires_agent_periode(plannings_periode, agent, moment.date()).get(jour, [])

    if len(plages_du_jour) == 0:
        return "Jour sans couverture"

    premiere_plage_debut = plages_du_jour[0][0]
    derniere_plage_fin = plages_du_jour[-1][1]

    if moment.hour < premiere_plage_debut:
        return "Avant l'ouverture"
    elif moment.hour >= derniere_plage_fin:
        return "Après la fermeture"
    else:
        return "Pause déjeuner"


def separer_creneau(tickets, plannings_periode):
    en_creneau = []
    pause_dejeuner = []
    hors_creneau = []

    for ticket in tickets:
        type_du_ticket = type_creneau(ticket["created_at"], ticket["assignee"], plannings_periode)
        if type_du_ticket == "En créneau":
            en_creneau.append(ticket)
        elif type_du_ticket == "Pause déjeuner":
            pause_dejeuner.append(ticket)
        else:
            hors_creneau.append(ticket)

    return en_creneau, pause_dejeuner, hors_creneau


SEUIL_SLA_EN_CRENEAU_MIN = 60  # règle : 1re réponse en 1h max quand le ticket arrive en créneau


def echeance_sla(date_creation, agent, plannings_periode):
    jour_candidat = date_creation.date()
    heure_reference = date_creation.hour

    for _ in range(14):  # sécurité : on ne cherche pas plus de 2 semaines devant
        horaires = horaires_agent_periode(plannings_periode, agent, jour_candidat)
        plages = horaires.get(jour_candidat.weekday(), [])

        for debut, fin in plages:
            deja_passee = jour_candidat == date_creation.date() and heure_reference >= fin
            if not deja_passee:
                return datetime.datetime.combine(jour_candidat, datetime.time(fin, 0))

        jour_candidat = jour_candidat + datetime.timedelta(days=1)
        heure_reference = 0

    return None


def sla_respecte(ticket, plannings_periode):
    minutes = ticket["first_reply_time_min"]
    if minutes is None:
        return None

    created_at = ticket["created_at"]
    agent = ticket["assignee"]

    if type_creneau(created_at, agent, plannings_periode) == "En créneau":
        return minutes <= SEUIL_SLA_EN_CRENEAU_MIN

    echeance = echeance_sla(created_at, agent, plannings_periode)
    if echeance is None:
        return None

    moment_reponse = created_at + datetime.timedelta(minutes=minutes)
    return moment_reponse <= echeance


def taux_sla(tickets, plannings_periode):
    respectes = 0
    total = 0

    for ticket in tickets:
        resultat = sla_respecte(ticket, plannings_periode)
        if resultat is not None:
            total = total + 1
            if resultat:
                respectes = respectes + 1

    if total == 0:
        return None

    return respectes / total * 100


def niveau_reponse_ouvree(minutes):
    if minutes > SEUIL_DEBORDEMENT_MIN:
        return "DEBORDEMENT"
    elif minutes < 90:
        return "OK"
    elif minutes < 120:
        return "A SURVEILLER"
    else:
        return "CRITIQUE"


def niveau_macro(valeur):
    if valeur is None:
        return ""
    if valeur < 50:
        return "CRITIQUE"
    elif valeur < 70:
        return "A SURVEILLER"
    else:
        return "OK"


def couleur_niveau(valeur):
    if valeur in ("OK", "CORRECT", "Correct", "EXCELLENT", "Excellent", "En créneau", "Fort potentiel"):
        return "background-color: #c6f0d2"
    elif valeur in ("A SURVEILLER", "À surveiller", "Potentiel moyen"):
        return "background-color: #ffe8a1"
    elif valeur in ("CRITIQUE", "Critique", "DEBORDEMENT", "Débordement", "Risque de perte du prospect"):
        return "background-color: #f7c6c2"
    elif valeur in ("NOUVEAU", "Nouveau"):
        return "background-color: #c6dcf7"
    elif valeur in ("DISPARU", "Disparu"):
        return "background-color: #e0e0e0"
    else:
        return ""


LIBELLES_NIVEAUX = {
    "CORRECT": "Correct",
    "EXCELLENT": "Excellent",
    "A SURVEILLER": "À surveiller",
    "CRITIQUE": "Critique",
    "DEBORDEMENT": "Débordement",
    "NOUVEAU": "Nouveau",
    "DISPARU": "Disparu",
}


def libelle_niveau(valeur):
    return LIBELLES_NIVEAUX.get(valeur, valeur)


def grouper_par(tickets, champ):
    groupes = {}
    for ticket in tickets:
        cle = ticket[champ]
        if cle in groupes:
            groupes[cle].append(ticket)
        else:
            groupes[cle] = [ticket]
    return groupes


def cles_combinees(dict_actuel, dict_precedent):
    cles = []
    for cle in dict_actuel:
        cles.append(cle)
    for cle in dict_precedent:
        if cle not in cles:
            cles.append(cle)
    return cles


def grouper_par_categorie(tickets):
    par_categorie = {}
    for ticket in tickets:
        categorie = categoriser(ticket)
        if categorie in par_categorie:
            par_categorie[categorie].append(ticket)
        else:
            par_categorie[categorie] = [ticket]
    return par_categorie


CATEGORIE_SAV_PRODUIT = "SAV produit (défaut)"


# NB : la colonne "is_sav" du fichier source n'est pas utilisée ici — elle est
# redondante avec ticket_reason == "SAV" et cette fonction affine encore la
# distinction SAV usage / SAV produit à partir de resolution_type.
def categoriser(ticket):
    raison = ticket["ticket_reason"]

    if raison in ("Livraison", "Suivi commande"):
        return "Livraison"
    elif raison in ("Abonnement / paiement", "Retour / remboursement"):
        return "Après-vente commande/admin"
    elif raison == "Conseil programme / produit":
        return "Avant-vente / conseil"
    elif raison == "Utilisation / routine":
        return "SAV usage (besoin d'aide)"
    elif raison == "SAV":
        if ticket["resolution_type"] == "Information / résolution à distance":
            return "SAV usage (besoin d'aide)"
        else:
            return CATEGORIE_SAV_PRODUIT
    else:
        return "Autre"


def niveau_csat(valeur):
    if valeur is None:
        return ""
    if valeur <= 3:
        return "CRITIQUE"
    elif valeur < 4:
        return "A SURVEILLER"
    elif valeur < 5:
        return "CORRECT"
    else:
        return "EXCELLENT"


MOTS_VIDES_FR = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "à", "a", "est", "c'est", "je", "j'ai",
    "que", "qui", "pour", "pas", "ne", "se", "sur", "au", "aux", "en", "dans", "avec", "mon", "ma",
    "mes", "ce", "cette", "il", "elle", "on", "vous", "nous", "plus", "très", "bien", "depuis",
    "après", "quand", "comment", "donc", "mais", "où", "suis", "ai", "avez", "avoir", "été", "cela",
    "ça", "fait", "faire", "peut", "peux", "pouvez", "merci", "bonjour", "cordialement", "votre",
    "vos", "leur", "leurs", "sont", "être", "toujours", "encore", "aussi", "alors", "tout", "toute",
}


def obtenir_compte_mot(paire_mot_compte):
    return paire_mot_compte[1]


def mots_frequents(tickets, champ, nombre_max):
    compteur = {}
    for ticket in tickets:
        texte = ticket[champ]
        if texte is None:
            continue

        texte_nettoye = texte.lower()
        for caractere in ("'", ",", ".", "?", "!", ":", ";", "\n"):
            texte_nettoye = texte_nettoye.replace(caractere, " ")

        for mot in texte_nettoye.split():
            if len(mot) < 4 or mot in MOTS_VIDES_FR:
                continue
            if mot in compteur:
                compteur[mot] = compteur[mot] + 1
            else:
                compteur[mot] = 1

    mots_tries = sorted(compteur.items(), key=obtenir_compte_mot, reverse=True)

    resultat = []
    for i in range(min(nombre_max, len(mots_tries))):
        resultat.append(mots_tries[i])
    return resultat


def cible_perte_confiance(categorie):
    if categorie == CATEGORIE_SAV_PRODUIT:
        return "Confiance produit + marque"
    elif categorie == "Livraison":
        return "Confiance marque"
    elif categorie == "SAV usage (besoin d'aide)":
        return "Confiance produit (usage)"
    elif categorie == "Avant-vente / conseil":
        return "Conversion potentielle perdue"
    elif categorie == "Après-vente commande/admin":
        return "Confiance marque (process)"
    else:
        return "Non catégorisé"


def type_perte_financiere(ticket):
    resolution = ticket["resolution_type"]

    if resolution == "Remboursement":
        return "Remboursement"
    elif resolution == "Remplacement produit":
        return "Remplacement produit"
    elif resolution == "Remplacement appareil / accessoire":
        return "Remplacement accessoire"
    elif resolution == "Geste commercial":
        return "Geste commercial"
    else:
        return None


MARQUEUR_HORS_CATALOGUE = "(hors catalogue)"


def detecter_opportunites_hors_catalogue(tickets, seuil):
    par_sujet = {}
    for ticket in tickets:
        sujet = ticket["subject_cluster"]
        if sujet is not None and MARQUEUR_HORS_CATALOGUE in sujet:
            if sujet in par_sujet:
                par_sujet[sujet].append(ticket)
            else:
                par_sujet[sujet] = [ticket]

    opportunites = []
    for sujet, tickets_sujet in par_sujet.items():
        if len(tickets_sujet) >= seuil:
            opportunites.append((sujet, tickets_sujet))

    return opportunites


def niveau_hausse_sujet(delta, seuil_surveiller, seuil_critique):
    if delta >= seuil_critique:
        return "CRITIQUE"
    elif delta >= seuil_surveiller:
        return "A SURVEILLER"
    else:
        return "OK"


def formater_pourcentage(valeur):
    if valeur is None:
        return "N/A"
    return str(round(valeur)) + " %"


def formater_csat(valeur):
    if valeur is None:
        return "N/A"
    return str(round(valeur, 2))


def formater_duree(minutes):
    if minutes is None:
        return "N/A"

    minutes = round(minutes)
    jours = minutes // 1440
    heures = (minutes % 1440) // 60
    minutes_restantes = minutes % 60

    if jours > 0:
        return str(jours) + "j " + str(heures) + "h"
    elif heures > 0:
        return str(heures) + "h " + str(minutes_restantes) + "min"
    else:
        return str(minutes_restantes) + "min"
