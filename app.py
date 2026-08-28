import base64
import datetime
import os
import altair as alt
import pandas as pd
import streamlit as st

from outils import (
    charger_tickets,
    fichiers_dans_plage,
    charger_periode,
    charger_planning,
    construire_plannings_periode,
    charger_commandes,
    charger_couts_produits,
    montant_perte_estime,
    montant_cout_garantie,
    formater_montant,
    formater_nombre_espace,
    commandes_par_email,
    premiere_commande_apres,
    tickets_par_email,
    dernier_ticket_avant,
    charger_nps,
    calculer_nps,
    charger_suivi_suggestions,
    impact_avant_apres,
    mots_frequents,
    extraire_code_macro,
    charger_texte_macro,
    extraire_nom_fichier_faq,
    charger_texte_faq,
    lister_exports,
    detecter_opportunites_hors_catalogue,
    horaires_agent,
    texte_horaires_jour,
    charger_roles_planning,
    NOM_AGENT_DEFAUT,
    moyenne,
    taux_rempli,
    formater_duree,
    formater_csat,
    formater_pourcentage,
    grouper_par,
    grouper_par_categorie,
    cles_combinees,
    evolution_pourcentage,
    categoriser,
    CATEGORIE_SAV_PRODUIT,
    couleur_texte_csat,
    niveau_macro,
    niveau_charge_creneau,
    niveau_reponse_ouvree,
    niveau_hausse_sujet,
    couleur_niveau,
    libelle_niveau,
    evenements_periode,
    detecter_changements_planning,
    delai_jours,
    niveau_anciennete_defaut,
    separer_creneau,
    type_hors_creneau_detaille,
    taux_sla,
    type_perte_financiere,
)


def obtenir_tickets(ligne):
    return ligne["Tickets"]


def obtenir_sav_recurrents(ligne):
    return ligne["SAV récurrents"]


DEFINITION_EN_CRENEAU = (
    "« En créneau » = uniquement les tickets arrivés pendant les horaires de travail planifiés. "
    "Ça isole la vraie performance de l'équipe, sans le délai dû aux horaires hors couverture "
    "(voir l'onglet Couverture & réactivité pour le détail du planning et du hors créneau)."
)

ROLE_RESPONSABLE_EQUIPE = "Responsable d'équipe"


NOMS_MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def formater_mois_annee(annee, mois):
    return NOMS_MOIS[mois - 1] + " " + str(annee)


NOMS_MOIS_ABREGES = [
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
]


# Format compact pour le bandeau d'en-tête global (ex. "7-13 sept. 2026" ou, à cheval sur deux
# mois, "28 sept.-4 oct. 2026").
def formater_plage_courte(date_debut, date_fin):
    mois_debut = NOMS_MOIS_ABREGES[date_debut.month - 1]
    mois_fin = NOMS_MOIS_ABREGES[date_fin.month - 1]

    if date_debut.year != date_fin.year:
        return (
            str(date_debut.day) + " " + mois_debut + " " + str(date_debut.year) + " - "
            + str(date_fin.day) + " " + mois_fin + " " + str(date_fin.year)
        )
    if date_debut.month != date_fin.month:
        return (
            str(date_debut.day) + " " + mois_debut + "-" + str(date_fin.day) + " " + mois_fin
            + " " + str(date_fin.year)
        )
    if date_debut.day == date_fin.day:
        return str(date_debut.day) + " " + mois_debut + " " + str(date_debut.year)
    return str(date_debut.day) + "-" + str(date_fin.day) + " " + mois_debut + " " + str(date_debut.year)


def construire_texte_evenements(exports_disponibles, date_debut, date_fin):
    fichiers_periode = []
    for date_export, chemin in exports_disponibles:
        if date_debut <= date_export <= date_fin:
            fichiers_periode.append((date_export, chemin))

    if len(fichiers_periode) == 0:
        return "Non renseigné"

    evenements_par_semaine = []
    for date_export, chemin in fichiers_periode:
        evenement = evenements_periode(charger_tickets(chemin))
        evenements_par_semaine.append((date_export, evenement))

    if len(evenements_par_semaine) == 1:
        return evenements_par_semaine[0][1]

    if len(evenements_par_semaine) == 2:
        lignes = []
        for date_export, evenement in evenements_par_semaine:
            lignes.append("Semaine du " + date_export.strftime("%d/%m/%Y") + " : " + evenement)
        return "  \n".join(lignes)

    evenements_par_mois = {}
    for date_export, evenement in evenements_par_semaine:
        cle_mois = (date_export.year, date_export.month)
        if cle_mois not in evenements_par_mois:
            evenements_par_mois[cle_mois] = []
        if evenement not in evenements_par_mois[cle_mois]:
            evenements_par_mois[cle_mois].append(evenement)

    cles_mois_triees = sorted(evenements_par_mois.keys())

    lignes = []
    for cle_mois in cles_mois_triees:
        annee_mois, numero_mois = cle_mois
        texte_evenements_mois = "; ".join(evenements_par_mois[cle_mois])
        lignes.append(formater_mois_annee(annee_mois, numero_mois) + " : " + texte_evenements_mois)

    return "  \n".join(lignes)


DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))

IMAGE_PRODUIT_ECLATEE = os.path.join(DOSSIER_PROJET, "assets", "produit_vue_eclatee.png")
IMAGE_PRODUIT_ASSEMBLEE = os.path.join(DOSSIER_PROJET, "assets", "produit_vue_assemblee.png")

ZONES_PHOTO_PRODUIT = {
    "Fixation capsule / diffusion parfum": (41, 11),
    "Module lumineux / LED": (41, 21),
    "Bouton / commande": (42, 27),
    "Coque / structure": (43, 47),
    "Batterie / charge": (41, 75),
    "Socle": (41, 91),
}


def image_en_base64(chemin):
    with open(chemin, "rb") as fichier_image:
        contenu = fichier_image.read()
    return base64.b64encode(contenu).decode("utf-8")


def construire_schema_composants(par_composant, couleur):
    comptes = {}
    for composant, tickets_composant in par_composant.items():
        comptes[composant] = len(tickets_composant)

    comptes_sur_schema = {}
    for composant in ZONES_PHOTO_PRODUIT:
        if composant in comptes:
            comptes_sur_schema[composant] = comptes[composant]

    if len(comptes_sur_schema) == 0:
        return None

    compte_max = max(comptes_sur_schema.values())

    image_encodee = image_en_base64(IMAGE_PRODUIT_ECLATEE)

    badges_html = ""
    for composant, (x_pourcent, y_pourcent) in ZONES_PHOTO_PRODUIT.items():
        if composant not in comptes_sur_schema:
            continue

        compte = comptes_sur_schema[composant]
        taille_badge = 24 + (compte ** 0.5) * 3.4
        if taille_badge > 58:
            taille_badge = 58
        opacite = 0.55 + 0.4 * (compte / compte_max)

        badges_html += (
            '<div title="' + composant + " : " + str(compte) + ' tickets" style="'
            + "position:absolute; left:" + str(x_pourcent) + "%; top:" + str(y_pourcent) + "%; "
            + "transform:translate(-50%,-50%); width:" + str(round(taille_badge, 1)) + "px; "
            + "height:" + str(round(taille_badge, 1)) + "px; border-radius:50%; "
            + "background:" + couleur + "; opacity:" + str(round(opacite, 2)) + "; "
            + "border:2px solid #FFFFFF; box-shadow:0 1px 5px rgba(0,0,0,0.4); "
            + "display:flex; align-items:center; justify-content:center; "
            + 'color:#FFFFFF; font-size:12px; font-weight:600;">' + str(compte) + "</div>"
        )

    return (
        '<div style="position:relative; width:100%; max-width:380px; margin:0 auto;">'
        + '<img src="data:image/png;base64,' + image_encodee + '" '
        + 'style="width:100%; display:block; border-radius:10px;" />'
        + badges_html
        + "</div>"
    )


def construire_fonction_couleur_bloc(colonne_valeur, niveaux_par_ligne):
    def appliquer_couleur_bloc(ligne):
        couleur = couleur_niveau(niveaux_par_ligne[ligne.name])
        styles = []
        for nom_colonne in ligne.index:
            if nom_colonne == colonne_valeur:
                styles.append(couleur)
            else:
                styles.append("")
        return styles

    return appliquer_couleur_bloc


def afficher_tableau_colore(lignes, colonne_figee=None, colonnes_couleur_bloc=None):
    if len(lignes) == 0:
        st.write("Aucune donnée.")
        return

    tableau = pd.DataFrame(lignes)

    colonnes_niveaux = []
    for colonne in tableau.columns:
        if colonne.startswith("Niveau") or colonne == "Évolution":
            colonnes_niveaux.append(colonne)

    for colonne in colonnes_niveaux:
        tableau[colonne] = tableau[colonne].map(libelle_niveau)

    tableau_stylise = tableau.style.map(couleur_niveau, subset=colonnes_niveaux)

    # Le CSAT se colore directement sur le chiffre (pas de colonne "Niveau CSAT" séparée) —
    # cohérent partout où une colonne "CSAT" existe, pas besoin de le déclarer à chaque appel.
    if "CSAT" in tableau.columns:
        tableau_stylise = tableau_stylise.map(couleur_texte_csat, subset=["CSAT"])

    # colonnes_couleur_bloc : {colonne affichée à colorer: liste des niveaux, un par ligne,
    # dans le même ordre que `lignes`} — pour colorer le bloc d'une valeur (ex: un temps, un %)
    # directement, sans colonne "Niveau ..." séparée. Les niveaux sont passés à part (pas comme
    # colonne du tableau) car Styler.hide() n'est pas respecté par le rendu st.dataframe.
    if colonnes_couleur_bloc is not None:
        for colonne_valeur, niveaux_par_ligne in colonnes_couleur_bloc.items():
            tableau_stylise = tableau_stylise.apply(
                construire_fonction_couleur_bloc(colonne_valeur, niveaux_par_ligne), axis=1
            )

    configuration_colonnes = None
    if colonne_figee is not None:
        configuration_colonnes = {colonne_figee: st.column_config.Column(pinned=True)}

    st.dataframe(
        tableau_stylise,
        hide_index=True,
        width="stretch",
        column_config=configuration_colonnes,
    )


JOURS_ORDRE = [
    ("Lundi", 0), ("Mardi", 1), ("Mercredi", 2), ("Jeudi", 3),
    ("Vendredi", 4), ("Samedi", 5), ("Dimanche", 6),
]


def construire_ligne_planning(nom_affiche, horaires, role):
    ligne = {"Agent": nom_affiche, "Rôle": role}

    total_heures = 0
    for nom_jour, numero_jour in JOURS_ORDRE:
        plages = horaires.get(numero_jour, [])
        ligne[nom_jour] = texte_horaires_jour(plages)
        for debut, fin in plages:
            total_heures = total_heures + (fin - debut)

    ligne["Total heures/semaine"] = total_heures
    return ligne


def couleur_disponibilite_jour(valeur):
    if valeur == "-":
        return couleur_niveau("DISPARU")
    else:
        return couleur_niveau("OK")


HEURE_DEBUT_HOTSPOTS = 7
HEURE_FIN_HOTSPOTS = 21


def statut_creneau_standard(horaires_standard, jour, heure):
    plages = horaires_standard.get(jour, [])

    for debut, fin in plages:
        if debut <= heure < fin:
            return "Couverture requise"

    if len(plages) > 0:
        premiere_debut = plages[0][0]
        derniere_fin = plages[-1][1]
        if premiere_debut <= heure < derniere_fin:
            return "Pause déjeuner"

    return "Hors standard"


def agents_en_poste(planning, agents_grille, jour, heure):
    presents = []
    for agent in agents_grille:
        # Volontairement pas horaires_agent() ici : sa bascule vers l'horaire DEFAUT pour un
        # agent absent du planning gonflerait artificiellement les effectifs des semaines dont
        # le PLANNING est incomplet (ex : premiers exports, sans ligne par agent) — un agent
        # sans ligne cette semaine-là doit compter pour 0 heure, pas suivre le créneau standard.
        if agent not in planning:
            continue

        plages = planning[agent].get(jour, [])
        for debut, fin in plages:
            if debut <= heure < fin:
                presents.append(agent)
                break
    return presents


COULEUR_PRIMAIRE = "#CC5500"
COULEUR_SECONDAIRE = "#96234A"
COULEUR_ACCENT_FONCE = "#8B4513"

# Système de cartes/bandeaux (distinct du code couleur vert/jaune/rouge/bleu/gris des
# tableaux, qui garde son propre rôle de signal de statut — voir couleur_niveau()).
COULEUR_FOND_CARTE = "#FAFAF9"
COULEUR_BORDURE_CARTE = "#E8E3DD"
COULEUR_TEXTE_LABEL = "#8A7F73"
COULEUR_TEXTE_VALEUR = "#2B2620"
COULEUR_HAUSSE_FOND = "#DCF3E4"
COULEUR_HAUSSE_TEXTE = "#1E7A42"
COULEUR_BAISSE_FOND = "#FBDFDC"
COULEUR_BAISSE_TEXTE = "#B23A2E"
COULEUR_NEUTRE_FOND = "#EFECE8"
COULEUR_NEUTRE_TEXTE = "#6A6258"
COULEUR_FOND_BANDEAU = "#FBF3EC"
COULEUR_BORDURE_BANDEAU = "#EAD9C4"

# Variantes plus saturées de couleur_niveau() (outils.py), pensées pour un liseré de carte
# plutôt qu'un fond de cellule de tableau — même langage de statut, contexte différent.
COULEUR_ACCENT_OK = "#3FA76B"
COULEUR_ACCENT_SURVEILLER = "#E0A72E"
# Distinct du rouge (tension pendant l'ouverture) : la question "hors couverture" est d'une
# autre nature — pas un débordement de l'équipe en poste, une question de capacité/horaires.
COULEUR_ACCENT_HORS_COUVERTURE = "#D9822E"
COULEUR_ACCENT_CRITIQUE = "#D1483B"
COULEUR_ACCENT_DEBORDEMENT = "#A6291E"

# Fonds de cellule pour la heatmap de couverture (onglet Couverture & réactivité) — même
# langage de couleur que les accents ci-dessus, en teinte pâle pour un fond de cellule
# plutôt qu'un liseré.
COULEUR_HEATMAP_CONFORTABLE = "#D9EDDD"
COULEUR_HEATMAP_SURVEILLER = "#F7E2B8"
COULEUR_HEATMAP_HOTSPOT = "#F3D2CB"
COULEUR_HEATMAP_HORS_COUVERTURE = "#F4F2EE"


def formater_delta_kpi(delta, delta_couleur):
    if isinstance(delta, str):
        texte_signe = delta
        est_negatif = texte_signe.startswith("-")
    else:
        est_negatif = delta < 0
        if delta >= 0:
            texte_signe = "+" + str(delta)
        else:
            texte_signe = str(delta)

    if est_negatif:
        fleche = "↓"
    else:
        fleche = "↑"

    if delta_couleur == "off":
        fond, texte_couleur = COULEUR_NEUTRE_FOND, COULEUR_NEUTRE_TEXTE
    elif delta_couleur == "inverse":
        if est_negatif:
            fond, texte_couleur = COULEUR_HAUSSE_FOND, COULEUR_HAUSSE_TEXTE
        else:
            fond, texte_couleur = COULEUR_BAISSE_FOND, COULEUR_BAISSE_TEXTE
    else:
        if est_negatif:
            fond, texte_couleur = COULEUR_BAISSE_FOND, COULEUR_BAISSE_TEXTE
        else:
            fond, texte_couleur = COULEUR_HAUSSE_FOND, COULEUR_HAUSSE_TEXTE

    return fleche + " " + texte_signe, fond, texte_couleur


def construire_carte_kpi(label, valeur, delta=None, delta_couleur="normal", sous_texte=None, accent=None):
    if accent is None:
        bordure_gauche = "border-left:1px solid " + COULEUR_BORDURE_CARTE + ";"
    else:
        bordure_gauche = "border-left:6px solid " + accent + ";"

    html = (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        + bordure_gauche
        + 'border-radius:10px; padding:16px 18px 14px; margin-bottom:8px; min-height:104px;">'
        '<div style="font-size:12px; text-transform:uppercase; letter-spacing:0.04em; color:' + COULEUR_TEXTE_LABEL + "; "
        'font-weight:600; margin-bottom:6px;">' + label + "</div>"
        '<div style="font-size:28px; font-weight:600; color:' + COULEUR_TEXTE_VALEUR + '; line-height:1.2;">'
        + str(valeur) + "</div>"
    )

    if delta is not None:
        texte_delta, fond_delta, couleur_delta = formater_delta_kpi(delta, delta_couleur)
        html = html + (
            '<div style="display:inline-block; margin-top:8px; padding:2px 9px; border-radius:12px; '
            "font-size:12px; font-weight:600; background-color:" + fond_delta + "; color:" + couleur_delta + ';">'
            + texte_delta + "</div>"
        )

    if sous_texte is not None:
        html = html + (
            '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:6px;">' + sous_texte + "</div>"
        )

    html = html + "</div>"
    return html


def construire_bandeau_info(texte_html):
    return (
        '<div style="background-color:' + COULEUR_FOND_BANDEAU + "; border:1px solid " + COULEUR_BORDURE_BANDEAU + "; "
        'border-radius:8px; padding:14px 16px; color:' + COULEUR_TEXTE_VALEUR + '; font-size:14px; line-height:1.5;">'
        + texte_html + "</div>"
    )


# Style distinct pour LE titre principal de chaque onglet (un seul par onglet, celui qui
# introduit le sujet central) — les st.subheader() suivants restent la hiérarchie "normale"
# (déjà assagie par la règle CSS globale h2/h3), pour donner un vrai repère visuel de premier
# niveau sans devoir reclasser individuellement chaque sous-titre de l'app.
def titre_section_principale(texte):
    return (
        '<div style="border-left:4px solid ' + COULEUR_PRIMAIRE + "; padding-left:14px; margin:10px 0 6px;\">"
        '<span style="font-size:23px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">' + texte + "</span>"
        "</div>"
    )


COULEUR_FOND_HEATMAP_PAR_NIVEAU = {
    "CONFORTABLE": COULEUR_HEATMAP_CONFORTABLE,
    "A_SURVEILLER": COULEUR_HEATMAP_SURVEILLER,
    "HOTSPOT": COULEUR_HEATMAP_HOTSPOT,
    "HORS_COUVERTURE": COULEUR_HEATMAP_HORS_COUVERTURE,
}


# Au-delà de 3 prénoms, la cellule tronque ("+N") pour rester compacte — la liste
# complète reste disponible via l'attribut title (tooltip au survol).
def construire_texte_agents_cellule(agents):
    if len(agents) == 0:
        return ""
    if len(agents) <= 3:
        return " · ".join(agents)
    return " · ".join(agents[:3]) + " +" + str(len(agents) - 3)


def construire_cellule_heatmap(entree):
    couleur_fond = COULEUR_FOND_HEATMAP_PAR_NIVEAU[entree["niveau"]]

    titre_tooltip = ""
    if len(entree["agents"]) > 0:
        titre_tooltip = ", ".join(entree["agents"])

    if entree["niveau"] == "HORS_COUVERTURE":
        # Fermé par conception (horaire standard, pause, week-end) : le volume peut
        # attendre la réouverture, pas de couleur de tension ni de mention d'effectif.
        if entree["demandes"] > 0:
            contenu = '<div class="hm-muted">' + str(entree["demandes"]) + " demandes</div>"
        else:
            contenu = '<div class="hm-muted">—</div>'
    elif entree["nb_agents"] > 0:
        texte_agents = construire_texte_agents_cellule(entree["agents"])
        if entree["nb_agents"] == 1:
            texte_effectif = "1 agent"
        else:
            texte_effectif = str(entree["nb_agents"]) + " agents"

        contenu = (
            '<div class="hm-line-agents">' + texte_agents + "</div>"
            '<div class="hm-line-demandes">' + texte_effectif + " · " + str(entree["demandes"]) + " demandes</div>"
            '<div class="hm-line-ratio">' + str(round(entree["ratio"], 1)) + " / agent</div>"
        )
    else:
        # Créneau censé être couvert mais personne en poste — anomalie réelle, pas une
        # fermeture assumée : on la montre, pas de ratio calculable.
        contenu = (
            '<div class="hm-line-agents">Aucun agent en poste</div>'
            '<div class="hm-line-demandes">' + str(entree["demandes"]) + " demandes</div>"
        )

    return (
        '<div class="hm-cell" style="background-color:' + couleur_fond + ';" title="' + titre_tooltip + '">'
        + contenu + "</div>"
    )


# Première heure d'ouverture et dernière heure de fermeture, toutes plages/jours confondus dans
# le planning standard — sert à savoir quelles heures, avant l'ouverture et après la fermeture,
# peuvent être regroupées en un seul bloc dans la heatmap plutôt qu'affichées heure par heure.
def determiner_bornes_ouverture(horaires_standard):
    premiere_ouverture = None
    derniere_fermeture = None

    for jour in range(7):
        plages = horaires_standard.get(jour, [])
        for debut, fin in plages:
            if premiere_ouverture is None or debut < premiere_ouverture:
                premiere_ouverture = debut
            if derniere_fermeture is None or fin > derniere_fermeture:
                derniere_fermeture = fin

    return premiere_ouverture, derniere_fermeture


# Découpe la plage 7h-21h en "bandes" à afficher dans la heatmap : les heures avant la première
# ouverture et après la dernière fermeture sont regroupées en un seul bloc chacune (toujours
# fermées par conception, quel que soit le jour), les heures effectivement couvertes par au moins
# un jour restent détaillées heure par heure. Si aucune ouverture n'est définie, pas de
# regroupement (repli sur le détail heure par heure complet).
def construire_bandes_heatmap(premiere_ouverture, derniere_fermeture):
    bandes = []

    if premiere_ouverture is None or derniere_fermeture is None:
        for heure in range(HEURE_DEBUT_HOTSPOTS, HEURE_FIN_HOTSPOTS):
            bandes.append(("HEURE", heure, heure + 1))
        return bandes

    if premiere_ouverture > HEURE_DEBUT_HOTSPOTS:
        bandes.append(("AVANT_OUVERTURE", HEURE_DEBUT_HOTSPOTS, premiere_ouverture))

    borne_basse = max(HEURE_DEBUT_HOTSPOTS, premiere_ouverture)
    borne_haute = min(HEURE_FIN_HOTSPOTS, derniere_fermeture)
    for heure in range(borne_basse, borne_haute):
        bandes.append(("HEURE", heure, heure + 1))

    if derniere_fermeture < HEURE_FIN_HOTSPOTS:
        bandes.append(("APRES_FERMETURE", derniere_fermeture, HEURE_FIN_HOTSPOTS))

    return bandes


def construire_cellule_heatmap_bande(demandes_total):
    if demandes_total > 0:
        contenu = '<div class="hm-muted">' + str(demandes_total) + " demandes</div>"
    else:
        contenu = '<div class="hm-muted">—</div>'

    return (
        '<div class="hm-cell hm-cell-bande" style="background-color:' + COULEUR_HEATMAP_HORS_COUVERTURE + ';">'
        + contenu + "</div>"
    )


SEUIL_PART_TELEPHONE_SIGNAL = 30


# Le canal n'est montré ici que pour le téléphone, et seulement s'il pèse vraiment sur le
# créneau : c'est le seul canal impliquant une attente synchrone, donc le seul où "quel canal
# domine" change concrètement la lecture opérationnelle d'un hotspot (cf. heatmap, où le canal
# n'est volontairement jamais montré cellule par cellule).
def construire_carte_situation(entree, est_pic_semaine):
    titre = entree["jour"] + " · " + str(entree["heure"]) + "h-" + str(entree["heure"] + 1) + "h"

    texte_agents = construire_texte_agents_cellule(entree["agents"])
    if texte_agents == "":
        texte_agents = "Aucun agent en poste"

    if entree["ratio"] is not None:
        ligne_detail = str(entree["demandes"]) + " demandes · " + str(round(entree["ratio"], 1)) + " / agent"
        if est_pic_semaine:
            verdict = "Charge la plus élevée de la semaine"
        else:
            verdict = str(round(entree["ratio"], 1)) + " demandes / agent"
    else:
        ligne_detail = str(entree["demandes"]) + " demandes"
        verdict = "Aucun agent en poste"

    ligne_canal = ""
    if entree.get("canal_dominant") == "Téléphone" and entree.get("part_canal_dominant", 0) >= SEUIL_PART_TELEPHONE_SIGNAL:
        ligne_canal = (
            '<div style="font-size:11px; color:' + COULEUR_ACCENT_HORS_COUVERTURE + '; margin-top:2px;">'
            "Dont " + str(round(entree["part_canal_dominant"])) + " % téléphone — implique une attente "
            "synchrone.</div>"
        )

    return (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        "border-left:6px solid " + COULEUR_ACCENT_CRITIQUE + '; border-radius:10px; padding:12px 14px; margin-bottom:8px;">'
        '<div style="font-size:13px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">' + titre + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;">' + texte_agents + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + ligne_detail + "</div>"
        + ligne_canal
        + '<div style="font-size:12px; font-weight:600; color:' + COULEUR_ACCENT_CRITIQUE + '; margin-top:4px;">'
        + verdict + "</div>"
        "</div>"
    )


NB_SEMAINES_BASELINE_HORS_COUVERTURE = 6
SEUIL_VOLUME_HORS_COUVERTURE_MIN = 20
SEUIL_DELTA_HORS_COUVERTURE_PCT = 25


# Volume "hors couverture" (pause, avant/après horaire standard, week-end) des N derniers
# exports disponibles AVANT la période affichée — sert de référence pour juger si le volume
# hors couverture de la période actuelle est inhabituel, plutôt que de réagir à un seul
# samedi chargé.
def calculer_baseline_hors_couverture(exports_disponibles, date_a_debut, nb_semaines):
    exports_avant_periode = []
    for date_export, chemin in exports_disponibles:
        if date_export < date_a_debut:
            exports_avant_periode.append((date_export, chemin))

    exports_baseline = exports_avant_periode[-nb_semaines:]

    volumes_baseline = []
    for date_export, chemin in exports_baseline:
        tickets_semaine = charger_tickets(chemin)
        planning_semaine = construire_plannings_periode([chemin], exports_disponibles)
        en_creneau_semaine, pause_semaine, hors_semaine = separer_creneau(tickets_semaine, planning_semaine)
        volumes_baseline.append(len(pause_semaine) + len(hors_semaine))

    return volumes_baseline


def hors_couverture_est_significatif(volume_actuel, moyenne_baseline):
    if volume_actuel < SEUIL_VOLUME_HORS_COUVERTURE_MIN:
        return False

    if moyenne_baseline is None or moyenne_baseline == 0:
        return True

    delta_pct = (volume_actuel - moyenne_baseline) / moyenne_baseline * 100
    return delta_pct >= SEUIL_DELTA_HORS_COUVERTURE_PCT


# Distinction volontairement simple (pas une vraie analyse de tendance) : si la majorité
# des semaines de référence étaient déjà au-dessus du seuil, ce n'est pas un pic isolé.
def type_signal_hors_couverture(volumes_baseline):
    if len(volumes_baseline) == 0:
        return "Volume à surveiller"

    nb_semaines_elevees = 0
    for volume in volumes_baseline:
        if volume >= SEUIL_VOLUME_HORS_COUVERTURE_MIN:
            nb_semaines_elevees = nb_semaines_elevees + 1

    if nb_semaines_elevees / len(volumes_baseline) >= 0.5:
        return "Pattern récurrent depuis plusieurs semaines"
    return "Volume à surveiller"


def construire_repartition_jours_texte(tickets):
    compteur_jour = {}
    for ticket in tickets:
        numero_jour = ticket["created_at"].weekday()
        if numero_jour in compteur_jour:
            compteur_jour[numero_jour] = compteur_jour[numero_jour] + 1
        else:
            compteur_jour[numero_jour] = 1

    morceaux = []
    for nom_jour, numero_jour in JOURS_ORDRE:
        if numero_jour in compteur_jour:
            morceaux.append(str(compteur_jour[numero_jour]) + " " + nom_jour.lower())

    return " · ".join(morceaux)


def construire_repartition_canaux_texte(tickets):
    compteur_canal = {}
    total = len(tickets)
    for ticket in tickets:
        canal = ticket["via_channel"]
        if canal in compteur_canal:
            compteur_canal[canal] = compteur_canal[canal] + 1
        else:
            compteur_canal[canal] = 1

    parts = []
    for canal, compte in compteur_canal.items():
        parts.append((canal, compte / total * 100))

    def obtenir_part(item):
        canal, part = item
        return part

    parts_triees = sorted(parts, key=obtenir_part, reverse=True)

    morceaux = []
    for canal, part in parts_triees:
        morceaux.append(str(round(part)) + "% " + canal)

    return " · ".join(morceaux)


def construire_carte_hors_couverture(volume_actuel, moyenne_baseline, nb_semaines_baseline, type_signal, tickets_hors_tout):
    ligne_volume = str(volume_actuel) + " demandes reçues hors couverture"

    if moyenne_baseline is not None and moyenne_baseline > 0:
        delta_pct = (volume_actuel - moyenne_baseline) / moyenne_baseline * 100
        ligne_delta = (
            "+" + str(round(delta_pct)) + "% vs moyenne des " + str(nb_semaines_baseline)
            + " derniers exports disponibles"
        )
    else:
        ligne_delta = "Pas d'historique de comparaison disponible sur cette période"

    lignes_detail = ""
    repartition_jours = construire_repartition_jours_texte(tickets_hors_tout)
    if repartition_jours != "":
        lignes_detail = lignes_detail + (
            '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + repartition_jours + "</div>"
        )

    repartition_canaux = construire_repartition_canaux_texte(tickets_hors_tout)
    if repartition_canaux != "":
        lignes_detail = lignes_detail + (
            '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + repartition_canaux + "</div>"
        )

    return (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        "border-left:6px solid " + COULEUR_ACCENT_HORS_COUVERTURE + '; border-radius:10px; padding:12px 14px; margin-bottom:8px;">'
        '<div style="font-size:13px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">Hors couverture</div>'
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;">' + ligne_volume + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + ligne_delta + "</div>"
        + lignes_detail
        + '<div style="font-size:12px; font-weight:600; color:' + COULEUR_ACCENT_HORS_COUVERTURE + '; margin-top:4px;">'
        + type_signal + "</div>"
        "</div>"
    )


SLA_OBJECTIF_PCT = 85
SEUIL_PIC_EXCEPTIONNEL_PCT = 30


# Agents à afficher dans la grille de couverture : priorité au planning réellement déclaré
# (un agent programmé cette semaine mais qui n'a clôturé aucun ticket ne doit pas disparaître),
# les assignees de tickets non présents dans le planning sont ajoutés en complément.
def construire_agents_grille(tickets, planning_dernier):
    agents_de_la_periode = grouper_par(tickets, "assignee")
    agents_a_afficher = cles_combinees(planning_dernier, agents_de_la_periode)

    agents_grille = []
    for agent in agents_a_afficher:
        if agent != NOM_AGENT_DEFAUT:
            agents_grille.append(agent)
    return agents_grille


def obtenir_canal_dominant(compteur_canal, total_demandes):
    if total_demandes == 0 or len(compteur_canal) == 0:
        return None, 0

    canal_max = None
    compte_max = 0
    for canal, compte in compteur_canal.items():
        if compte > compte_max:
            compte_max = compte
            canal_max = canal

    return canal_max, compte_max / total_demandes * 100


# Une entrée par (jour, heure) 7h-21h, dans l'ordre heure par heure puis jour par jour — cet
# ordre est celui dans lequel la heatmap HTML est ensuite émise (grille CSS en mode
# "auto-flow: row", qui suit l'ordre du DOM).
def construire_grille_creneaux(tickets, planning_dernier, agents_grille, horaires_standard):
    demandes_par_jour_heure = {}
    canaux_par_jour_heure = {}
    for nom_jour, numero_jour in JOURS_ORDRE:
        demandes_par_jour_heure[numero_jour] = {}
        canaux_par_jour_heure[numero_jour] = {}
        for heure in range(HEURE_DEBUT_HOTSPOTS, HEURE_FIN_HOTSPOTS):
            demandes_par_jour_heure[numero_jour][heure] = 0
            canaux_par_jour_heure[numero_jour][heure] = {}

    for ticket in tickets:
        moment = ticket["created_at"]
        jour_ticket = moment.weekday()
        heure_ticket = moment.hour
        if HEURE_DEBUT_HOTSPOTS <= heure_ticket < HEURE_FIN_HOTSPOTS:
            demandes_par_jour_heure[jour_ticket][heure_ticket] = demandes_par_jour_heure[jour_ticket][heure_ticket] + 1

            compteur_canal = canaux_par_jour_heure[jour_ticket][heure_ticket]
            canal = ticket["via_channel"]
            if canal in compteur_canal:
                compteur_canal[canal] = compteur_canal[canal] + 1
            else:
                compteur_canal[canal] = 1

    grille = []
    for heure in range(HEURE_DEBUT_HOTSPOTS, HEURE_FIN_HOTSPOTS):
        for nom_jour, numero_jour in JOURS_ORDRE:
            presents = agents_en_poste(planning_dernier, agents_grille, numero_jour, heure)
            nb_agents = len(presents)
            demandes = demandes_par_jour_heure[numero_jour][heure]
            statut = statut_creneau_standard(horaires_standard, numero_jour, heure)

            if nb_agents > 0:
                ratio = demandes / nb_agents
            else:
                ratio = None

            niveau = niveau_charge_creneau(statut, nb_agents, ratio)
            canal_dominant, part_canal_dominant = obtenir_canal_dominant(
                canaux_par_jour_heure[numero_jour][heure], demandes
            )

            grille.append({
                "jour": nom_jour,
                "heure": heure,
                "nb_agents": nb_agents,
                "agents": presents,
                "demandes": demandes,
                "ratio": ratio,
                "canal_dominant": canal_dominant,
                "part_canal_dominant": part_canal_dominant,
                "niveau": niveau,
            })
    return grille


# Distingue un pic exceptionnel (une semaine précise très au-dessus du rythme habituel) du
# rythme habituel lui-même (déjà agrégé sur toute la période sélectionnée) — seulement pertinent
# quand plusieurs semaines sont sélectionnées. Recharge chaque fichier individuellement (même
# schéma que calculer_baseline_hors_couverture) pour comparer semaine par semaine plutôt que sur
# l'agrégat.
def detecter_pic_exceptionnel(fichiers_actuels, agents_grille, ratio_habituel, jour_habituel, heure_habituel):
    if len(fichiers_actuels) <= 1 or ratio_habituel is None or ratio_habituel <= 0:
        return None

    meilleur_ratio = -1
    meilleur_jour = None
    meilleur_heure = None

    for chemin in fichiers_actuels:
        tickets_fichier = charger_tickets(chemin)
        planning_fichier = charger_planning(chemin)
        horaires_standard_fichier = planning_fichier.get(NOM_AGENT_DEFAUT, {})
        grille_fichier = construire_grille_creneaux(
            tickets_fichier, planning_fichier, agents_grille, horaires_standard_fichier
        )
        for entree in grille_fichier:
            if entree["ratio"] is not None and entree["ratio"] > meilleur_ratio:
                meilleur_ratio = entree["ratio"]
                meilleur_jour = entree["jour"]
                meilleur_heure = entree["heure"]

    if meilleur_jour is None:
        return None

    delta_pct = (meilleur_ratio - ratio_habituel) / ratio_habituel * 100
    meme_creneau = meilleur_jour == jour_habituel and meilleur_heure == heure_habituel

    if delta_pct >= SEUIL_PIC_EXCEPTIONNEL_PCT and not meme_creneau:
        return {"jour": meilleur_jour, "heure": meilleur_heure, "ratio": meilleur_ratio}
    return None


RANG_NIVEAU_REPONSE = {"OK": 0, "A SURVEILLER": 1, "CRITIQUE": 2, "DEBORDEMENT": 3}


# Le canal qui contribue le plus au retard : le pire niveau de réponse, départagé par volume
# en cas d'égalité — sert de base à l'insight de la section SLA, à celui de la section Canal, et
# à la conclusion de l'onglet (une seule détermination, réutilisée, pas trois calculs différents).
def canal_le_plus_problematique(lignes_canal, niveaux_canal):
    pire_canal = None
    pire_rang = -1

    for index in range(len(lignes_canal)):
        ligne = lignes_canal[index]
        niveau = niveaux_canal[index]
        if niveau == "":
            continue

        rang = RANG_NIVEAU_REPONSE[niveau]
        if rang > pire_rang:
            pire_rang = rang
            pire_canal = ligne
        elif rang == pire_rang and pire_canal is not None and ligne["Tickets"] > pire_canal["Tickets"]:
            pire_canal = ligne

    return pire_canal


def construire_barre_progression_sla(taux, objectif):
    largeur = min(taux, 100)
    if taux >= objectif:
        couleur = COULEUR_ACCENT_OK
    elif taux >= objectif - 10:
        couleur = COULEUR_ACCENT_SURVEILLER
    else:
        couleur = COULEUR_ACCENT_CRITIQUE

    return (
        '<div style="position:relative; width:100%; height:8px; background-color:' + COULEUR_NEUTRE_FOND + '; '
        'border-radius:4px; margin:10px 0 6px;">'
        '<div style="position:absolute; left:0; top:0; height:100%; width:' + str(largeur) + '%; '
        "background-color:" + couleur + '; border-radius:4px;"></div>'
        '<div style="position:absolute; left:' + str(objectif) + '%; top:-3px; height:14px; width:2px; '
        'background-color:' + COULEUR_TEXTE_VALEUR + ';" title="Objectif ' + str(objectif) + ' %"></div>'
        "</div>"
    )


def construire_carte_sla(taux, objectif, delta=None):
    ecart = round(taux - objectif, 1)
    if ecart >= 0:
        texte_ecart = "+" + str(ecart) + " pts au-dessus de l'objectif"
        couleur_ecart = COULEUR_HAUSSE_TEXTE
    else:
        texte_ecart = str(ecart) + " pts sous l'objectif"
        couleur_ecart = COULEUR_BAISSE_TEXTE

    html = (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        'border-radius:10px; padding:20px 22px 16px;">'
        '<div style="font-size:12px; text-transform:uppercase; letter-spacing:0.04em; color:' + COULEUR_TEXTE_LABEL + "; "
        'font-weight:600;">SLA respecté</div>'
        '<div style="font-size:40px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + '; line-height:1.15; margin-top:2px;">'
        + formater_pourcentage(taux) + "</div>"
    )

    html = html + construire_barre_progression_sla(taux, objectif)

    html = html + (
        '<div style="font-size:12px; color:' + couleur_ecart + '; font-weight:600;">' + texte_ecart + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;">Objectif : ' + str(objectif) + " %</div>"
    )

    if delta is not None:
        texte_delta, fond_delta, couleur_delta = formater_delta_kpi(delta, "normal")
        html = html + (
            '<div style="display:inline-block; margin-top:8px; padding:2px 9px; border-radius:12px; '
            "font-size:12px; font-weight:600; background-color:" + fond_delta + "; color:" + couleur_delta + ';">'
            + texte_delta + " pts vs période précédente</div>"
        )

    html = html + "</div>"
    return html


def construire_barre_empilee_reponse(compte_niveaux, total):
    segments = [
        ("Dans le SLA", "OK", COULEUR_ACCENT_OK),
        ("Léger dépassement", "A SURVEILLER", COULEUR_ACCENT_SURVEILLER),
        ("Retard important", "CRITIQUE", COULEUR_ACCENT_CRITIQUE),
        ("Débordement", "DEBORDEMENT", COULEUR_ACCENT_DEBORDEMENT),
    ]

    html = '<div style="display:flex; width:100%; height:14px; border-radius:7px; overflow:hidden; margin-bottom:10px;">'
    for label, cle, couleur in segments:
        compte = compte_niveaux[cle]
        if total > 0:
            largeur = compte / total * 100
        else:
            largeur = 0
        if largeur > 0:
            html = html + '<div style="width:' + str(largeur) + '%; background-color:' + couleur + ';" title="' + label + '"></div>'
    html = html + "</div>"

    html = html + '<div style="display:flex; flex-wrap:wrap; gap:14px; font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">'
    for label, cle, couleur in segments:
        compte = compte_niveaux[cle]
        if total > 0:
            pct = compte / total * 100
        else:
            pct = 0
        html = html + (
            '<div><span style="display:inline-block; width:8px; height:8px; border-radius:2px; '
            'background-color:' + couleur + '; margin-right:5px;"></span>'
            + label + " — " + str(round(pct)) + " % (" + str(compte) + ")</div>"
        )
    html = html + "</div>"
    return html


def construire_insight_sla(taux, objectif, pire_canal):
    if taux is None:
        return None
    if taux >= objectif:
        return "Le SLA dépasse l'objectif sur cette période."
    if pire_canal is not None:
        return "Le SLA reste sous l'objectif, principalement en raison du canal " + pire_canal["Canal"] + "."
    return "Le SLA reste sous l'objectif de " + str(objectif) + " %."


def construire_insight_canal(pire_canal):
    if pire_canal is None:
        return None
    return (
        "Le canal " + pire_canal["Canal"] + " concentre le principal retard de réponse : "
        + str(pire_canal["Tickets"]) + " demandes et " + pire_canal["1re réponse moyenne"]
        + " de 1re réponse moyenne."
    )


def obtenir_volume_ligne(ligne):
    return ligne["Volume"]


# Périodes hors couverture mutuellement exclusives (type_hors_creneau_detaille ne retourne
# jamais "Jour sans couverture" pour un samedi/dimanche, donc pas de double comptage). Une ligne
# "Week-end" agrégée est ajoutée en tête si samedi et/ou dimanche sont présents, pour donner le
# chiffre de synthèse avant le détail — le détail par jour reste disponible juste en dessous.
def construire_lignes_hors_couverture(tickets_hors_tout, planning_ref, volume_total_creneaux):
    groupes_type = {}
    for ticket in tickets_hors_tout:
        type_detail = type_hors_creneau_detaille(ticket["created_at"], ticket["assignee"], planning_ref)
        if type_detail in groupes_type:
            groupes_type[type_detail].append(ticket)
        else:
            groupes_type[type_detail] = [ticket]

    tickets_weekend = []
    if "Samedi" in groupes_type:
        tickets_weekend = tickets_weekend + groupes_type["Samedi"]
    if "Dimanche" in groupes_type:
        tickets_weekend = tickets_weekend + groupes_type["Dimanche"]

    lignes = []

    if len(tickets_weekend) > 0:
        pct_weekend = len(tickets_weekend) / volume_total_creneaux * 100
        frt_weekend = moyenne(tickets_weekend, "first_reply_time_min")
        ligne_weekend = {
            "Période": "Week-end", "Volume": len(tickets_weekend),
            "Part du volume": formater_pourcentage(pct_weekend), "Délai moyen de rattrapage": "N/A",
        }
        if frt_weekend is not None:
            ligne_weekend["Délai moyen de rattrapage"] = formater_duree(frt_weekend)
        lignes.append(ligne_weekend)

    lignes_detail = []
    for type_detail, tickets_type in groupes_type.items():
        frt_type = moyenne(tickets_type, "first_reply_time_min")
        pct_type = len(tickets_type) / volume_total_creneaux * 100
        ligne = {
            "Période": type_detail, "Volume": len(tickets_type),
            "Part du volume": formater_pourcentage(pct_type), "Délai moyen de rattrapage": "N/A",
        }
        if frt_type is not None:
            ligne["Délai moyen de rattrapage"] = formater_duree(frt_type)
        lignes_detail.append(ligne)

    lignes_detail_triees = sorted(lignes_detail, key=obtenir_volume_ligne, reverse=True)
    return lignes + lignes_detail_triees


# 3 observations maximum, chacune dérivée des chiffres déjà calculés plus haut dans l'onglet —
# aucun nouveau calcul, uniquement de la synthèse textuelle (donnée -> signal -> insight).
def construire_conclusion_onglet(
    taux_sla_global, objectif, nb_tensions, pire_canal, part_hors_couverture, hors_couverture_significatif
):
    observations = []

    if nb_tensions == 0:
        observations.append((
            "Ce qui va bien",
            "La couverture actuelle absorbe correctement les volumes pendant les horaires ouverts.",
        ))
    elif taux_sla_global is not None and taux_sla_global >= objectif:
        observations.append((
            "Ce qui va bien",
            "Le SLA dépasse l'objectif malgré les tensions ponctuelles identifiées sur la période.",
        ))

    if pire_canal is not None:
        observations.append((
            "À surveiller",
            "Le délai du canal " + pire_canal["Canal"] + " reste le principal point de friction de la période.",
        ))
    elif nb_tensions > 0:
        observations.append((
            "À surveiller", str(nb_tensions) + " créneau(x) en tension identifié(s) cette période.",
        ))

    if hors_couverture_significatif:
        observations.append((
            "À comprendre",
            formater_pourcentage(part_hors_couverture) + " des demandes arrivent hors couverture, avec un "
            + "volume en hausse significative par rapport à l'historique récent.",
        ))
    else:
        observations.append((
            "À comprendre",
            formater_pourcentage(part_hors_couverture) + " des demandes arrivent hors couverture, sans créer "
            + "pour l'instant de tension significative à la réouverture.",
        ))

    return observations[:3]


# ------------------------------------------------------------------
# Architecture rôles (conceptuelle) — pas de système de permissions réel dans cette démo (pas de
# login), mais l'app ne doit pas supposer que tout utilisateur futur verra tout. Cette structure
# documente, pour chaque onglet, le rôle minimum censé y avoir accès, et marque les données jugées
# sensibles (coûts unitaires) — prête à être branchée sur une vraie gestion d'accès plus tard, sans
# rien construire ici qui ressemblerait à une fausse authentification.
# ------------------------------------------------------------------

ROLE_AGENT = "Agent"
ROLE_TEAM_LEAD = "Team Lead / Customer Care Manager"
ROLE_HEAD_CX = "Head of CX / Direction"
ROLE_ADMIN = "Admin"

ROLES_ONGLET = {
    "Contexte": [ROLE_AGENT, ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Vue d'ensemble": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Tendances": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Agents": [ROLE_AGENT, ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Alertes & suggestions": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Couverture & réactivité": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Produit": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Livraison": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Avant-vente & conversion": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
    "Impact & confiance": [ROLE_HEAD_CX, ROLE_ADMIN],
}

# Un agrégat (total, moyenne, répartition par composant/type) reste visible à un rôle qui n'a pas
# accès au détail unitaire — c'est déjà le cas dans l'UI actuelle : les coûts de revient unitaires
# du futur fichier product_costs_fictif.xlsx ne sont jamais affichés en tableau brut, seulement
# utilisés pour calculer des totaux/répartitions. Cette liste documente l'intention explicitement.
DONNEES_SENSIBLES = {
    "cout_revient_produit": [ROLE_HEAD_CX, ROLE_ADMIN],
    "cout_logistique_remplacement": [ROLE_HEAD_CX, ROLE_ADMIN],
}


DOSSIER_EXPORTS = os.path.join(DOSSIER_PROJET, "exports_hebdomadaires")
FICHIER_SHOPIFY = os.path.join(DOSSIER_PROJET, "data_shopify", "commandes_shopify_fictif.xlsx")
FICHIER_COUTS_PRODUITS = os.path.join(DOSSIER_PROJET, "data_shopify", "product_costs_fictif.xlsx")
FICHIER_NPS = os.path.join(DOSSIER_PROJET, "data_shopify", "nps_fictif.xlsx")
FICHIER_SUIVI_SUGGESTIONS = os.path.join(DOSSIER_PROJET, "data_suivi", "suivi_suggestions.xlsx")
DOSSIER_MACROS = os.path.join(DOSSIER_PROJET, "knowledge_base", "macros")
DOSSIER_FAQ = os.path.join(DOSSIER_PROJET, "knowledge_base", "faq")
FENETRE_CONVERSION_JOURS = 30

SEUIL_MINIMUM_SUJET = 5
SEUIL_MACRO_BASSE = 20
SEUIL_MACRO_HAUTE = 50
SEUIL_CSAT_INSATISFAISANT = 4
SEUIL_HAUSSE_SUJET_SURVEILLER = 5
SEUIL_HAUSSE_SUJET_CRITIQUE = 10
SEUIL_REPLIES_FAQ = 3
SEUIL_CSAT_VERBATIM = 2
SEUIL_VERBATIMS_GROUPE = 10

OBJECTIF_MACRO_PCT = 70
SEUIL_DELTA_CSAT_NOTABLE = 0.2
SEUIL_DELTA_FRT_NOTABLE_MIN = 15
SEUIL_DELTA_MACRO_NOTABLE_PT = 5


# Une ligne par sujet, avec évolution/niveau si une période de comparaison est active — logique
# inchangée, seulement extraite pour être calculée une fois (réutilisée par les insights
# prioritaires ET par les expanders détaillés de "Vue d'ensemble", au lieu d'être recalculée à
# chaque ouverture d'expander).
def construire_lignes_sujets(tickets_cat_s2, tickets_cat_s1, comparaison_disponible):
    sujets_cat_s2 = grouper_par(tickets_cat_s2, "subject_cluster")
    sujets_cat_s1 = grouper_par(tickets_cat_s1, "subject_cluster")

    if comparaison_disponible:
        sujets_a_afficher = cles_combinees(sujets_cat_s2, sujets_cat_s1)
    else:
        sujets_a_afficher = list(sujets_cat_s2.keys())

    lignes_sujets = []
    for sujet in sujets_a_afficher:
        tickets_sujet_s2 = sujets_cat_s2.get(sujet, [])
        volume_s2 = len(tickets_sujet_s2)
        ligne_sujet = {"Sujet": sujet, "Tickets": volume_s2}

        if comparaison_disponible:
            volume_s1 = len(sujets_cat_s1.get(sujet, []))
            delta = volume_s2 - volume_s1

            if delta >= 0:
                delta_texte = "+" + str(delta)
            else:
                delta_texte = str(delta)

            ligne_sujet["Évolution"] = delta_texte

            if volume_s2 == 0:
                ligne_sujet["Niveau"] = "DISPARU"
            elif volume_s1 == 0:
                ligne_sujet["Niveau"] = "NOUVEAU"
            else:
                ligne_sujet["Niveau"] = niveau_hausse_sujet(delta, SEUIL_HAUSSE_SUJET_SURVEILLER, SEUIL_HAUSSE_SUJET_CRITIQUE)

        lignes_sujets.append(ligne_sujet)

    return sorted(lignes_sujets, key=obtenir_tickets, reverse=True)


# Le seuil de hausse/baisse (niveau_hausse_sujet) travaille déjà sur un delta ABSOLU, pas un % —
# une variation de 1 vers 2 tickets (100 %) ne franchit jamais ce seuil. Pas besoin d'un garde-fou
# de volume supplémentaire ici : le seuil absolu joue déjà ce rôle.
def obtenir_sujets_notables(lignes_sujets):
    notables = []
    for ligne in lignes_sujets:
        niveau = ligne.get("Niveau", "")
        if niveau == "CRITIQUE" or niveau == "A SURVEILLER":
            notables.append(ligne)
        elif niveau == "NOUVEAU" and ligne["Tickets"] >= SEUIL_MINIMUM_SUJET:
            notables.append(ligne)
    return notables


def obtenir_score_insight(insight):
    return insight["score"]


# 3 à 5 observations maximum, classées par magnitude — pas un insight généré artificiellement pour
# chaque métrique. Sans comparaison, repli sur des signaux à seuil absolu (objectif macro, CSAT
# bas, plus gros volume) plutôt que sur des évolutions qui n'existent pas sans période B.
def construire_insights_vue_ensemble(
    lignes_categories_apercu_triees, categories_s2, categories_s1, comparaison_disponible,
    sujets_notables_par_categorie, csat_s2, csat_s1, frt_s2, frt_s1, macro_s2, macro_s1,
):
    candidats = []

    if comparaison_disponible:
        for ligne in lignes_categories_apercu_triees:
            categorie = ligne["Catégorie"]
            volume_actuel = ligne["Tickets"]
            volume_precedent = len(categories_s1.get(categorie, []))
            if volume_precedent == 0:
                continue

            delta_absolu = volume_actuel - volume_precedent
            if abs(delta_absolu) < SEUIL_HAUSSE_SUJET_SURVEILLER:
                continue

            evolution = evolution_pourcentage(volume_precedent, volume_actuel)
            if delta_absolu > 0:
                texte = (
                    categorie + " augmente de " + str(round(evolution)) + " % par rapport à la "
                    "période précédente (" + str(volume_precedent) + " → " + str(volume_actuel) + " tickets)."
                )
            else:
                texte = (
                    categorie + " diminue de " + str(round(abs(evolution))) + " % par rapport à la "
                    "période précédente (" + str(volume_precedent) + " → " + str(volume_actuel) + " tickets)."
                )
            candidats.append({"titre": "Volume — " + categorie, "texte": texte, "score": abs(delta_absolu)})

        if csat_s2 is not None and csat_s1 is not None:
            delta_csat = csat_s2 - csat_s1
            if abs(delta_csat) >= SEUIL_DELTA_CSAT_NOTABLE:
                if delta_csat < 0:
                    texte = (
                        "Le CSAT moyen baisse de " + str(round(abs(delta_csat), 2)) + " point(s) par "
                        "rapport à la période précédente (" + formater_csat(csat_s1) + " → " + formater_csat(csat_s2) + ")."
                    )
                else:
                    texte = (
                        "Le CSAT moyen progresse de " + str(round(delta_csat, 2)) + " point(s) par "
                        "rapport à la période précédente (" + formater_csat(csat_s1) + " → " + formater_csat(csat_s2) + ")."
                    )
                candidats.append({"titre": "CSAT global", "texte": texte, "score": abs(delta_csat) * 20})

        if frt_s2 is not None and frt_s1 is not None:
            delta_frt = frt_s2 - frt_s1
            if abs(delta_frt) >= SEUIL_DELTA_FRT_NOTABLE_MIN:
                if delta_frt > 0:
                    texte = (
                        "Le délai de 1re réponse augmente de " + str(round(delta_frt)) + " min par "
                        "rapport à la période précédente (" + formater_duree(frt_s1) + " → " + formater_duree(frt_s2) + ")."
                    )
                else:
                    texte = (
                        "Le délai de 1re réponse s'améliore de " + str(round(abs(delta_frt))) + " min "
                        "par rapport à la période précédente (" + formater_duree(frt_s1) + " → " + formater_duree(frt_s2) + ")."
                    )
                candidats.append({"titre": "Délai de 1re réponse", "texte": texte, "score": abs(delta_frt)})

        if macro_s2 is not None and macro_s1 is not None:
            delta_macro = macro_s2 - macro_s1
            if abs(delta_macro) >= SEUIL_DELTA_MACRO_NOTABLE_PT:
                if delta_macro < 0:
                    texte = "L'utilisation des macros recule de " + str(round(abs(delta_macro), 1)) + " pt par rapport à la période précédente."
                else:
                    texte = "L'utilisation des macros progresse de " + str(round(delta_macro, 1)) + " pt par rapport à la période précédente."
                candidats.append({"titre": "Utilisation macro", "texte": texte, "score": abs(delta_macro) * 4})
    else:
        if macro_s2 is not None and macro_s2 < OBJECTIF_MACRO_PCT:
            candidats.append({
                "titre": "Utilisation macro",
                "texte": (
                    "L'utilisation des macros est à " + formater_pourcentage(macro_s2) + ", sous "
                    "l'objectif de " + str(OBJECTIF_MACRO_PCT) + " %."
                ),
                "score": OBJECTIF_MACRO_PCT - macro_s2,
            })
        if csat_s2 is not None and csat_s2 < SEUIL_CSAT_INSATISFAISANT:
            candidats.append({
                "titre": "CSAT global",
                "texte": "Le CSAT moyen est à " + formater_csat(csat_s2) + " sur 5 sur la période.",
                "score": (SEUIL_CSAT_INSATISFAISANT - csat_s2) * 20,
            })
        if len(lignes_categories_apercu_triees) > 0:
            plus_gros = lignes_categories_apercu_triees[0]
            candidats.append({
                "titre": "Volume — " + plus_gros["Catégorie"],
                "texte": (
                    plus_gros["Catégorie"] + " concentre le plus gros volume de la période ("
                    + str(plus_gros["Tickets"]) + " tickets)."
                ),
                "score": 1,
            })

    # sujets_notables_par_categorie n'est jamais peuplé sans comparaison active (obtenir_sujets_notables
    # ne garde que des lignes avec "Niveau" défini, lui-même seulement présent quand comparaison_disponible),
    # et "Évolution" est alors toujours renseigné (y compris pour un sujet NOUVEAU, delta = volume - 0) —
    # pas de cas où delta_texte serait vide ici.
    for categorie, sujets_categorie in sujets_notables_par_categorie.items():
        for sujet_ligne in sujets_categorie:
            delta_texte = sujet_ligne["Évolution"]
            niveau_sujet = sujet_ligne["Niveau"]
            score_sujet = abs(int(delta_texte))
            texte = (
                "« " + sujet_ligne["Sujet"] + " » (" + categorie + ") évolue de " + delta_texte
                + " tickets — " + libelle_niveau(niveau_sujet).lower() + "."
            )

            candidats.append({"titre": "Sujet — " + sujet_ligne["Sujet"], "texte": texte, "score": score_sujet})

    candidats_tries = sorted(candidats, key=obtenir_score_insight, reverse=True)
    return candidats_tries[:5]


st.set_page_config(page_title="Dashboard Customer Care : Emyria", layout="wide")

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');"
    "html, body, [class*='css'] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }"
    "h1 { letter-spacing: -0.02em; }"
    "h2, h3 { letter-spacing: -0.01em; font-weight: 600; color: #3A342C; }"
    "[data-testid='stAlert'] { border-radius: 8px; }"
    "[data-testid='stButton'] button { border-radius: 8px; }"
    "</style>",
    unsafe_allow_html=True,
)

st.title("Dashboard Customer Care : Emyria")

exports_disponibles = lister_exports(DOSSIER_EXPORTS)

semaines_disponibles = []
for date_export_boucle, chemin_boucle in exports_disponibles:
    semaines_disponibles.append(date_export_boucle)


def formater_semaine_menu(date_semaine):
    return "Semaine du " + date_semaine.strftime("%d/%m/%Y")


def reinitialiser_periode():
    for cle in ("semaine_a", "fin_a", "etendre_a", "semaine_b", "fin_b", "etendre_b", "comparer"):
        if cle in st.session_state:
            del st.session_state[cle]


st.sidebar.header("Période d'analyse")
date_dernier_export = exports_disponibles[-1][0]
st.sidebar.caption("Dernières données disponibles : " + date_dernier_export.strftime("%d/%m/%Y"))
st.sidebar.caption(
    str(len(semaines_disponibles)) + " semaines représentatives disponibles (pas un historique "
    "hebdomadaire continu) — les semaines listées ci-dessous sont les seules pour lesquelles un "
    "export existe."
)
st.sidebar.button("Réinitialiser (dernières données)", on_click=reinitialiser_periode, type="primary")

st.sidebar.markdown("**Période A**")
semaine_a = st.sidebar.selectbox(
    "Semaine", semaines_disponibles, index=len(semaines_disponibles) - 1,
    format_func=formater_semaine_menu, key="semaine_a",
)

etendre_a = st.sidebar.checkbox("Étendre la période", value=False, key="etendre_a")

if etendre_a:
    fin_a = st.sidebar.selectbox(
        "Jusqu'à", semaines_disponibles, index=len(semaines_disponibles) - 1,
        format_func=formater_semaine_menu, key="fin_a",
    )
else:
    fin_a = semaine_a

if semaine_a <= fin_a:
    date_a_debut = semaine_a
    date_a_fin = fin_a + datetime.timedelta(days=6)
else:
    date_a_debut = fin_a
    date_a_fin = semaine_a + datetime.timedelta(days=6)

fichiers_actuels = fichiers_dans_plage(exports_disponibles, date_a_debut, date_a_fin)

comparer = st.sidebar.checkbox("Comparer à une autre période", value=False, key="comparer")

comparaison_disponible = False
tickets_s1 = []
fichiers_precedents = []
changements_planning = []

if comparer:
    st.sidebar.markdown("**Période B (comparaison)**")
    semaine_b = st.sidebar.selectbox(
        "Semaine (B)", semaines_disponibles, index=0,
        format_func=formater_semaine_menu, key="semaine_b",
    )

    etendre_b = st.sidebar.checkbox("Étendre la période (B)", value=False, key="etendre_b")

    if etendre_b:
        fin_b = st.sidebar.selectbox(
            "Jusqu'à (B)", semaines_disponibles, index=0,
            format_func=formater_semaine_menu, key="fin_b",
        )
    else:
        fin_b = semaine_b

    if semaine_b <= fin_b:
        date_b_debut = semaine_b
        date_b_fin = fin_b + datetime.timedelta(days=6)
    else:
        date_b_debut = fin_b
        date_b_fin = semaine_b + datetime.timedelta(days=6)

    fichiers_precedents = fichiers_dans_plage(exports_disponibles, date_b_debut, date_b_fin)

    if len(fichiers_precedents) > 0:
        comparaison_disponible = True

if len(fichiers_actuels) == 0:
    st.warning("Aucun export disponible sur la période A choisie.")
    st.stop()

tickets_s2 = charger_periode(fichiers_actuels)

if len(tickets_s2) == 0:
    st.warning("Les exports de la période A ne contiennent aucun ticket.")
    st.stop()

planning_s2_dernier = charger_planning(fichiers_actuels[-1])
planning_s2 = construire_plannings_periode(fichiers_actuels, exports_disponibles)

if comparaison_disponible:
    tickets_s1 = charger_periode(fichiers_precedents)
    planning_s1_dernier = charger_planning(fichiers_precedents[-1])
    planning_s1 = construire_plannings_periode(fichiers_precedents, exports_disponibles)
    agents_s1_liste = list(grouper_par(tickets_s1, "assignee").keys())
    agents_s2_liste = list(grouper_par(tickets_s2, "assignee").keys())
    changements_planning = detecter_changements_planning(agents_s1_liste, agents_s2_liste, planning_s1_dernier, planning_s2_dernier)

texte_bandeau_periode = formater_plage_courte(date_a_debut, date_a_fin)
if comparaison_disponible:
    texte_bandeau_periode = texte_bandeau_periode + " vs " + formater_plage_courte(date_b_debut, date_b_fin)

st.markdown(
    '<div style="font-size:15px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + '; margin:-6px 0 12px;">'
    + texte_bandeau_periode + "</div>",
    unsafe_allow_html=True,
)
if comparer and not comparaison_disponible:
    st.caption("Aucun export disponible sur la période B choisie — pas de comparaison possible.")

categories_s1 = grouper_par_categorie(tickets_s1)
categories_s2 = grouper_par_categorie(tickets_s2)

# Chargés une seule fois ici (au lieu de dans un onglet) car utilisés à la fois par
# "Avant-vente & conversion" et "Impact & confiance" — éviter de recharger deux fois.
commandes = charger_commandes(FICHIER_SHOPIFY)
couts_produits = charger_couts_produits(FICHIER_COUTS_PRODUITS)

fichiers_tous_business = []
for date_export_hist, chemin_hist in exports_disponibles:
    fichiers_tous_business.append(chemin_hist)
tickets_historique_business = charger_periode(fichiers_tous_business)

# Chargé ici (au lieu de dans un onglet) car utilisé à la fois par "Agents" et "Couverture & réactivité".
# Fusionné sur tous les fichiers de la période (pas seulement le dernier) : avec "Étendre
# sur plusieurs semaines" coché, un agent peut ne pas apparaître dans le rôle du dernier
# export pris isolément (rôle non renseigné ce jour-là, agent parti avant le dernier export...).
# Le dernier fichier traité l'emporte en cas de rôle différent d'un export à l'autre.
roles_periode = {}
for chemin_role in fichiers_actuels:
    roles_fichier = charger_roles_planning(chemin_role)
    for agent_role, role_valeur in roles_fichier.items():
        roles_periode[agent_role] = role_valeur

(
    onglet_contexte, onglet_vue, onglet_tendances, onglet_agents, onglet_alertes,
    onglet_creneaux, onglet_produit, onglet_livraison, onglet_conversion, onglet_impact,
) = st.tabs(
    [
        "Contexte", "Vue d'ensemble", "Tendances", "Agents",
        "Alertes & suggestions", "Couverture & réactivité", "Produit", "Livraison",
        "Avant-vente & conversion", "Impact & confiance",
    ]
)


# ------------------------------------------------------------------
# Onglet 0 : Contexte
# ------------------------------------------------------------------

with onglet_contexte:
    colonne_hero_texte, colonne_hero_image = st.columns([2, 1])

    with colonne_hero_texte:
        st.markdown(
            '<div style="background-color:' + COULEUR_PRIMAIRE + '; padding:28px 32px; border-radius:10px; color:white; margin-bottom:20px;">'
            '<h1 style="margin:0; color:white;">Emyria</h1>'
            '<p style="margin:6px 0 0; font-size:17px; color:white;">Diffuseur d\'ambiance connecté — lumière LED &amp; capsules de parfum interchangeables</p>'
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            construire_bandeau_info(
                "Ce tableau de bord est une démonstration construite sur des données 100 % fictives "
                "(tickets, commandes, avis) — pas l'audit d'une entreprise réelle. Il illustre un outil de "
                "pilotage du service client conçu pour ce type de scale-up e-commerce."
            ),
            unsafe_allow_html=True,
        )

    with colonne_hero_image:
        st.image(IMAGE_PRODUIT_ASSEMBLEE, caption="Emyria — produit fictif, généré pour cette démo")

    colonne_ctx_a, colonne_ctx_b = st.columns(2)

    with colonne_ctx_a:
        st.markdown(titre_section_principale("L'entreprise (fictive)"), unsafe_allow_html=True)
        st.markdown(
            "- **Produit** : diffuseur d'ambiance connecté, avec 6 programmes de parfum — "
            "Sérénité, Éveil, Cocon, Clarté, Évasion, Douceur\n"
            "- **Positionnement** : haut de gamme — diffuseur de 179 € à 289 €, recharges de "
            "29 € à 45 €, panier moyen ~184 €\n"
            "- **Distribution** : vente en ligne en Europe + 18 boutiques partenaires (France, Belgique)\n"
            "- **Canaux de communication** : email, chat, WhatsApp, téléphone (appel direct ou "
            "consultation programmée sur rendez-vous pour l'avant-vente — cohérent avec le "
            "positionnement haut de gamme)\n"
            "- **Équipe** : 38 personnes, dont 4-5 au service client (Sam en renfort saisonnier "
            "en décembre)\n"
            "- **Stade** : scale-up, post-Série A, forte croissance\n"
            "- **Fondée en** : 2021\n"
            "- **Volume support** : très saisonnier — les pics Black Friday/Noël représentent un "
            "mode « surge » assumé (macros en priorité, SLA temporairement élargi, renfort "
            "week-end), pas le rythme soutenable habituel de l'équipe"
        )

    with colonne_ctx_b:
        st.markdown(titre_section_principale("Ce que permet ce tableau de bord"), unsafe_allow_html=True)
        st.markdown(
            "- Repérer ce qui mérite l'attention du manager sur la période choisie (barre latérale), "
            "pas seulement consulter des chiffres\n"
            "- Suivre alertes, réactivité et couverture au quotidien\n"
            "- Piloter le volet business : conversion avant-vente, coûts SAV, confiance client (NPS), "
            "opportunités produit hors catalogue"
        )

        st.markdown(titre_section_principale("Comment lire les onglets"), unsafe_allow_html=True)
        st.markdown(
            "Les onglets suivent la cadence à laquelle chaque sujet se pilote réellement, "
            "pas un ordre arbitraire :\n"
            "- **Vue d'ensemble → Alertes** : pilotage courant de l'équipe (catégories incluses)\n"
            "- **Couverture & réactivité** : disponibilité de l'équipe, SLA, tensions de couverture\n"
            "- **Produit** : cadence trimestrielle (usure, défauts récurrents)\n"
            "- **Livraison** : cadence mensuelle, pensé pour un point avec le transporteur\n"
            "- **Avant-vente & conversion** : conversion réelle après contact avant-vente\n"
            "- **Impact & confiance** : coûts SAV, confiance client (NPS)\n\n"
            "CSAT noté sur une échelle de 0 à 5. La période analysée (et la comparaison, si activée) "
            "est affichée en haut de chaque page, réglée une seule fois dans la barre latérale."
        )

    st.divider()
    st.markdown(titre_section_principale("Sources de données"), unsafe_allow_html=True)
    st.markdown(
        "- **Tickets support** — export hebdomadaire représentatif (canal, catégorie, agent, "
        "délais, CSAT)\n"
        "- **Planning des agents** — horaires, rôles, présence par créneau\n"
        "- **Commandes** — fichier Shopify (produit, montant, pays, date)\n"
        "- **Réponses NPS** — score de recommandation par client, indépendant de la période affichée\n"
        "- **Suivi des suggestions** — macros/FAQ créées et leur effet mesuré"
    )
    st.caption(
        "Toutes les données (tickets, commandes, avis NPS) sont générées aléatoirement pour cette "
        "démonstration — les chiffres n'ont aucune valeur réelle."
    )

    with st.expander("Limites connues de cette démo"):
        st.markdown(
            "- **Coût des incidents clients** : remboursement et remplacement/garantie utilisent un vrai "
            "coût de revient produit (product_costs_fictif.xlsx) ; seul le geste commercial reste une "
            "fraction estimée du prix de vente, faute d'un montant réellement accordé enregistré par "
            "ticket — voir l'onglet Impact & confiance pour le détail par ligne.\n"
            "- **Exports disponibles** : semaines représentatives espacées dans l'année (pas un "
            "historique hebdomadaire continu) — voir l'onglet Tendances pour le détail des écarts.\n"
            "- **Volume support en période de pic** : les semaines Black Friday/Noël dépassent le "
            "rythme soutenable d'un fonctionnement normal — volontaire, pensé comme un mode « surge » "
            "temporaire plutôt qu'un défaut de modélisation.\n"
            "- **Suivi des suggestions** (onglet Alertes & suggestions) : inclut volontairement un cas "
            "(MAC-018) où la macro créée a bien été adoptée par l'équipe mais n'a pas amélioré le CSAT — "
            "un vrai outil de pilotage doit pouvoir montrer un échec, pas seulement des réussites."
        )


# ------------------------------------------------------------------
# Onglet 1 : Vue d'ensemble
# ------------------------------------------------------------------

with onglet_vue:
    nombre_s2 = len(tickets_s2)
    csat_s2 = moyenne(tickets_s2, "csat")
    frt_s2 = moyenne(tickets_s2, "first_reply_time_min")
    macro_s2 = taux_rempli(tickets_s2, "macro_applied")

    # Calculés inconditionnellement (moyenne/taux_rempli renvoient None sur une liste vide) —
    # réutilisés à la fois par les cartes KPI ci-dessous et par les insights prioritaires plus bas.
    nombre_s1 = len(tickets_s1)
    csat_s1 = moyenne(tickets_s1, "csat")
    frt_s1 = moyenne(tickets_s1, "first_reply_time_min")
    macro_s1 = taux_rempli(tickets_s1, "macro_applied")

    with st.container(border=True):
        colonne1, colonne2, colonne3, colonne4 = st.columns(4)

        if comparaison_disponible:
            colonne1.markdown(
                construire_carte_kpi(
                    "Tickets reçus", formater_nombre_espace(nombre_s2),
                    delta=nombre_s2 - nombre_s1, delta_couleur="off",
                ),
                unsafe_allow_html=True,
            )

            if csat_s2 is not None and csat_s1 is not None:
                colonne2.markdown(
                    construire_carte_kpi("CSAT moyen", formater_csat(csat_s2), delta=round(csat_s2 - csat_s1, 2)),
                    unsafe_allow_html=True,
                )
            else:
                colonne2.markdown(construire_carte_kpi("CSAT moyen", formater_csat(csat_s2)), unsafe_allow_html=True)

            if frt_s2 is not None and frt_s1 is not None:
                colonne3.markdown(
                    construire_carte_kpi(
                        "1re réponse", formater_duree(frt_s2),
                        delta=str(round(frt_s2 - frt_s1)) + " min", delta_couleur="inverse",
                    ),
                    unsafe_allow_html=True,
                )
            else:
                colonne3.markdown(construire_carte_kpi("1re réponse", formater_duree(frt_s2)), unsafe_allow_html=True)

            if macro_s2 is not None and macro_s1 is not None:
                colonne4.markdown(
                    construire_carte_kpi(
                        "Utilisation macro", formater_pourcentage(macro_s2),
                        delta=str(round(macro_s2 - macro_s1, 1)) + " pt",
                    ),
                    unsafe_allow_html=True,
                )
            else:
                colonne4.markdown(
                    construire_carte_kpi("Utilisation macro", formater_pourcentage(macro_s2)), unsafe_allow_html=True
                )
        else:
            colonne1.markdown(
                construire_carte_kpi("Tickets reçus", formater_nombre_espace(nombre_s2)), unsafe_allow_html=True
            )
            colonne2.markdown(construire_carte_kpi("CSAT moyen", formater_csat(csat_s2)), unsafe_allow_html=True)
            colonne3.markdown(construire_carte_kpi("1re réponse", formater_duree(frt_s2)), unsafe_allow_html=True)
            colonne4.markdown(
                construire_carte_kpi("Utilisation macro", formater_pourcentage(macro_s2)), unsafe_allow_html=True
            )

    evenements_texte = construire_texte_evenements(exports_disponibles, date_a_debut, date_a_fin)
    for changement in changements_planning:
        evenements_texte = evenements_texte + "  \nChangement planning : " + changement

    evenements_html = "Événement(s) de la période :<br>" + evenements_texte.replace("  \n", "<br>")
    st.markdown(construire_bandeau_info(evenements_html), unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Sujets par catégorie — calculés une seule fois ici (réutilisés par les insights
    # prioritaires ci-dessous ET par les expanders détaillés plus bas, pas recalculés deux fois).
    # ------------------------------------------------------------------

    if comparaison_disponible:
        categories_a_afficher = cles_combinees(categories_s2, categories_s1)
    else:
        categories_a_afficher = list(categories_s2.keys())

    lignes_categories_apercu = []
    for categorie in categories_a_afficher:
        tickets_cat = categories_s2.get(categorie, [])
        lignes_categories_apercu.append({"Catégorie": categorie, "Tickets": len(tickets_cat)})

    lignes_categories_apercu_triees = sorted(lignes_categories_apercu, key=obtenir_tickets, reverse=True)

    sujets_par_categorie = {}
    sujets_notables_par_categorie = {}
    for ligne in lignes_categories_apercu_triees:
        categorie = ligne["Catégorie"]
        tickets_cat_s2 = categories_s2.get(categorie, [])
        tickets_cat_s1 = categories_s1.get(categorie, [])
        lignes_sujets_cat = construire_lignes_sujets(tickets_cat_s2, tickets_cat_s1, comparaison_disponible)
        sujets_par_categorie[categorie] = lignes_sujets_cat
        sujets_notables_par_categorie[categorie] = obtenir_sujets_notables(lignes_sujets_cat)

    # ------------------------------------------------------------------
    # Insights prioritaires — 3 à 5 observations maximum, pas un dump de tous les chiffres.
    # ------------------------------------------------------------------

    insights_vue_ensemble = construire_insights_vue_ensemble(
        lignes_categories_apercu_triees, categories_s2, categories_s1, comparaison_disponible,
        sujets_notables_par_categorie, csat_s2, csat_s1, frt_s2, frt_s1, macro_s2, macro_s1,
    )

    st.markdown(titre_section_principale("Ce qui mérite votre attention"), unsafe_allow_html=True)
    if len(insights_vue_ensemble) > 0:
        for insight in insights_vue_ensemble:
            st.markdown(
                '<div style="margin-bottom:10px;"><span style="font-size:11px; font-weight:700; '
                'text-transform:uppercase; letter-spacing:0.04em; color:' + COULEUR_PRIMAIRE + ';">'
                + insight["titre"] + '</span><br><span style="font-size:14px; color:' + COULEUR_TEXTE_VALEUR + ';">'
                + insight["texte"] + "</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("Aucune variation significative sur cette période — situation stable.")

    st.divider()
    st.markdown(titre_section_principale("Répartition par famille"), unsafe_allow_html=True)
    if comparaison_disponible:
        st.caption("Barres groupées : volume par catégorie sur les deux périodes, avec l'évolution en %")

    if comparaison_disponible:
        ordre_categories = []
        lignes_graphique_long = []
        lignes_graphique_deltas = []

        for ligne in lignes_categories_apercu_triees:
            categorie = ligne["Catégorie"]
            ordre_categories.append(categorie)
            volume_actuel = ligne["Tickets"]
            volume_precedent = len(categories_s1.get(categorie, []))

            lignes_graphique_long.append({"Catégorie": categorie, "Période": "Période actuelle", "Tickets": volume_actuel})
            lignes_graphique_long.append({"Catégorie": categorie, "Période": "Période précédente", "Tickets": volume_precedent})

            volume_max = max(volume_actuel, volume_precedent)
            if volume_precedent > 0:
                evolution = evolution_pourcentage(volume_precedent, volume_actuel)
                if evolution >= 0:
                    texte_evolution = "▲ +" + str(round(evolution)) + " %"
                else:
                    texte_evolution = "▼ " + str(round(evolution)) + " %"
            else:
                texte_evolution = "Nouveau"

            lignes_graphique_deltas.append({"Catégorie": categorie, "Volume max": volume_max, "Évolution": texte_evolution})

        tableau_long = pd.DataFrame(lignes_graphique_long)
        tableau_deltas = pd.DataFrame(lignes_graphique_deltas)

        barres_categories = alt.Chart(tableau_long).mark_bar().encode(
            x=alt.X("Catégorie:N", sort=ordre_categories, title=None),
            xOffset=alt.XOffset("Période:N", sort=["Période actuelle", "Période précédente"]),
            y=alt.Y("Tickets:Q", title="Tickets"),
            color=alt.Color(
                "Période:N",
                sort=["Période actuelle", "Période précédente"],
                scale=alt.Scale(
                    domain=["Période actuelle", "Période précédente"],
                    range=[COULEUR_PRIMAIRE, COULEUR_SECONDAIRE],
                ),
                legend=alt.Legend(title=None),
            ),
        )

        etiquettes_evolution = alt.Chart(tableau_deltas).mark_text(
            align="center", dy=-8, fontSize=13, fontWeight="bold", color=COULEUR_ACCENT_FONCE
        ).encode(
            x=alt.X("Catégorie:N", sort=ordre_categories),
            y=alt.Y("Volume max:Q"),
            text="Évolution:N",
        )

        graphique_categories = (
            (barres_categories + etiquettes_evolution)
            .properties(height=340)
            .configure_view(strokeWidth=0)
            .configure_axisX(labelAngle=-30)
        )
        with st.container(border=True):
            st.altair_chart(graphique_categories, width="stretch")
    else:
        lignes_graphique_categories = []
        for ligne in lignes_categories_apercu_triees:
            lignes_graphique_categories.append(
                {"Catégorie": ligne["Catégorie"], "Période actuelle": ligne["Tickets"]}
            )
        tableau_graphique_categories = pd.DataFrame(lignes_graphique_categories).set_index("Catégorie")
        with st.container(border=True):
            st.bar_chart(tableau_graphique_categories, color=COULEUR_PRIMAIRE)

    st.caption(
        "Sujets qui évoluent significativement (À surveiller/Critique) mise en avant ; le détail "
        "complet de chaque catégorie reste accessible."
    )
    for ligne in lignes_categories_apercu_triees:
        categorie = ligne["Catégorie"]
        lignes_sujets_cat_triees = sujets_par_categorie[categorie]
        sujets_notables = sujets_notables_par_categorie[categorie]

        with st.expander(categorie + " — " + str(ligne["Tickets"]) + " tickets"):
            if len(sujets_notables) > 0:
                afficher_tableau_colore(sujets_notables)
            elif comparaison_disponible:
                st.caption("Aucun sujet en évolution notable dans cette catégorie.")

            with st.expander("Voir tous les sujets de " + categorie):
                afficher_tableau_colore(lignes_sujets_cat_triees)

    st.divider()
    with st.expander("Performance par catégorie (détail)"):
        st.caption(DEFINITION_EN_CRENEAU)
        st.caption(
            "* 1re réponse en créneau : sous 1h (OK), 1h-2h (à surveiller), au-delà de 2h "
            "(critique) — le bloc se colore selon ce seuil. Utilisation macro : objectif minimum "
            "70 % des demandes traitées via macro, au moins une fois dans la conversation."
        )

        lignes_categories = []
        niveaux_reponse_categories = []
        niveaux_macro_categories = []

        if comparaison_disponible:
            categories_a_afficher_perf = cles_combinees(categories_s2, categories_s1)
        else:
            categories_a_afficher_perf = list(categories_s2.keys())

        for categorie in categories_a_afficher_perf:
            tickets_cat_s2 = categories_s2.get(categorie, [])
            tickets_cat_s1 = categories_s1.get(categorie, [])

            csat_cat_s2 = moyenne(tickets_cat_s2, "csat")
            macro_cat_s2 = taux_rempli(tickets_cat_s2, "macro_applied")

            if len(tickets_cat_s2) > 0:
                en_creneau_cat = separer_creneau(tickets_cat_s2, planning_s2)[0]
                frt_en_creneau_cat = moyenne(en_creneau_cat, "first_reply_time_min")
            else:
                frt_en_creneau_cat = None

            ligne = {"Catégorie": categorie}

            if comparaison_disponible:
                ligne["Volume période précédente"] = len(tickets_cat_s1)

            ligne["Volume période actuelle"] = len(tickets_cat_s2)
            ligne["CSAT"] = "N/A"
            ligne["1re réponse (en créneau)"] = "N/A"
            ligne["Utilisation macro (%)"] = formater_pourcentage(macro_cat_s2)

            if csat_cat_s2 is not None:
                ligne["CSAT"] = formater_csat(csat_cat_s2)

            niveau_reponse_categorie = ""
            if frt_en_creneau_cat is not None:
                ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_cat)
                niveau_reponse_categorie = niveau_reponse_ouvree(frt_en_creneau_cat)

            lignes_categories.append(ligne)
            niveaux_reponse_categories.append(niveau_reponse_categorie)
            niveaux_macro_categories.append(niveau_macro(macro_cat_s2))

        afficher_tableau_colore(
            lignes_categories,
            colonnes_couleur_bloc={
                "1re réponse (en créneau)": niveaux_reponse_categories,
                "Utilisation macro (%)": niveaux_macro_categories,
            },
        )


SEUIL_TENDANCE_STABLE_PCT = 15


def obtenir_valeurs_colonne(lignes_tendance, cle):
    valeurs = []
    for ligne in lignes_tendance:
        valeur = ligne[cle]
        if valeur is not None:
            valeurs.append(valeur)
    return valeurs


# Classification simple à partir d'une moyenne glissante (tous les points sauf les deux
# derniers) : le dernier point ET l'avant-dernier au-dessus de cette moyenne = tendance
# structurelle ; seul le dernier point élevé, l'avant-dernier proche de la moyenne = pic ponctuel ;
# le dernier point revient proche de la moyenne après un avant-dernier élevé = retour à la normale.
# Pas assez de points pour distinguer un aléa d'une vraie tendance -> le dire plutôt qu'inventer.
def classifier_tendance(valeurs):
    if len(valeurs) < 3:
        return "historique insuffisant"

    dernier = valeurs[-1]
    avant_dernier = valeurs[-2]
    # valeurs[:-2] a toujours au moins 1 élément ici (garanti par le "len(valeurs) < 3" ci-dessus).
    historique = valeurs[:-2]

    moyenne_historique = sum(historique) / len(historique)
    if moyenne_historique == 0:
        return "historique insuffisant"

    ecart_dernier_pct = (dernier - moyenne_historique) / moyenne_historique * 100
    ecart_avant_dernier_pct = (avant_dernier - moyenne_historique) / moyenne_historique * 100

    dernier_stable = abs(ecart_dernier_pct) < SEUIL_TENDANCE_STABLE_PCT
    avant_dernier_stable = abs(ecart_avant_dernier_pct) < SEUIL_TENDANCE_STABLE_PCT
    dernier_eleve = ecart_dernier_pct >= SEUIL_TENDANCE_STABLE_PCT
    avant_dernier_eleve = ecart_avant_dernier_pct >= SEUIL_TENDANCE_STABLE_PCT
    dernier_bas = ecart_dernier_pct <= -SEUIL_TENDANCE_STABLE_PCT
    avant_dernier_bas = ecart_avant_dernier_pct <= -SEUIL_TENDANCE_STABLE_PCT

    # Le retour à la normale doit être vérifié avant tout, sinon un dernier point simplement
    # stable masque le fait que l'avant-dernier était, lui, nettement écarté de la moyenne.
    if dernier_stable:
        if avant_dernier_stable:
            return "stabilité"
        return "retour à la normale"

    if dernier_eleve and avant_dernier_eleve:
        return "hausse structurelle"
    if dernier_bas and avant_dernier_bas:
        return "baisse structurelle"
    return "pic ponctuel"


def construire_ligne_classification_tendances(lignes_tendance):
    metriques = [
        ("Volume", "Tickets"),
        ("CSAT", "CSAT"),
        ("1re réponse", "1re réponse (min)"),
        ("Utilisation macro", "Utilisation macro (%)"),
    ]

    morceaux = []
    for label, cle in metriques:
        valeurs = obtenir_valeurs_colonne(lignes_tendance, cle)
        morceaux.append(label + " : " + classifier_tendance(valeurs))

    return " · ".join(morceaux)


# ------------------------------------------------------------------
# Onglet 2 : Tendances
# ------------------------------------------------------------------

with onglet_tendances:
    exports_jusqu_a_periode = []
    for date_export, chemin in exports_disponibles:
        if date_export <= date_a_fin:
            exports_jusqu_a_periode.append((date_export, chemin))

    if len(exports_jusqu_a_periode) > 1:
        texte_nombre_exports = str(len(exports_jusqu_a_periode)) + " exports disponibles"
    else:
        texte_nombre_exports = str(len(exports_jusqu_a_periode)) + " export disponible"

    st.caption(
        "Évolution sur les " + texte_nombre_exports + " jusqu'à la période sélectionnée dans la barre "
        "latérale — pas de données au-delà de la Période A, pour garder une lecture cohérente avec "
        "« où on en est ». Voir une vraie tendance plutôt que comparer seulement deux instantanés."
    )
    st.caption(
        "⚠️ Chaque point est une semaine représentative isolée, pas un suivi hebdomadaire continu — "
        "certains écarts entre points vont jusqu'à 6-7 semaines sans export. Les lignes en pointillé "
        "relient les points pour la lisibilité, mais n'illustrent pas une évolution semaine par semaine réelle."
    )

    lignes_tendance = []
    for date_export, chemin in exports_jusqu_a_periode:
        tickets_fichier = charger_tickets(chemin)
        if len(tickets_fichier) == 0:
            continue

        lignes_tendance.append({
            "Date": date_export,
            "Tickets": len(tickets_fichier),
            "CSAT": moyenne(tickets_fichier, "csat"),
            "1re réponse (min)": moyenne(tickets_fichier, "first_reply_time_min"),
            "Utilisation macro (%)": taux_rempli(tickets_fichier, "macro_applied"),
            "Événement": evenements_periode(tickets_fichier),
        })

    tableau_tendance = pd.DataFrame(lignes_tendance)

    st.markdown(
        '<div style="font-size:13px; font-weight:600; color:' + COULEUR_TEXTE_VALEUR + '; margin-bottom:14px;">'
        + construire_ligne_classification_tendances(lignes_tendance) + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(titre_section_principale("Volume de tickets"), unsafe_allow_html=True)
    graphique_volume = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Tickets:Q"),
        tooltip=["Date:T", "Tickets:Q", "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_volume, width="stretch")

    st.markdown(titre_section_principale("CSAT moyen"), unsafe_allow_html=True)
    graphique_csat = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_SECONDAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("CSAT:Q", scale=alt.Scale(domain=[1, 5])),
        tooltip=["Date:T", alt.Tooltip("CSAT:Q", format=".2f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_csat, width="stretch")

    st.markdown(titre_section_principale("Temps de 1re réponse moyen"), unsafe_allow_html=True)
    graphique_frt = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_ACCENT_FONCE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("1re réponse (min):Q", title="Minutes"),
        tooltip=["Date:T", alt.Tooltip("1re réponse (min):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_frt, width="stretch")

    st.markdown(titre_section_principale("Utilisation macro"), unsafe_allow_html=True)
    graphique_macro = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Utilisation macro (%):Q", scale=alt.Scale(domain=[0, 100])),
        tooltip=["Date:T", alt.Tooltip("Utilisation macro (%):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_macro, width="stretch")


# Le quadrant volume/CSAT reste un signal relatif à comprendre, jamais un jugement — les 4
# libellés décrivent symétriquement les deux axes (volume, CSAT) plutôt que de qualifier l'agent
# ("va vite"/"soigné"), et l'écart réel (pas juste au-dessus/en-dessous) est toujours affiché.
def construire_profil_agent(volume, volume_moyen_equipe, csat_agent, csat_moyen_equipe):
    if volume_moyen_equipe > 0:
        ecart_volume_pct = (volume - volume_moyen_equipe) / volume_moyen_equipe * 100
    else:
        ecart_volume_pct = 0

    volume_haut = volume > volume_moyen_equipe

    if csat_agent is not None and csat_moyen_equipe is not None:
        ecart_csat = csat_agent - csat_moyen_equipe
        csat_haut = csat_agent > csat_moyen_equipe
    else:
        ecart_csat = None
        csat_haut = False

    if ecart_volume_pct >= 0:
        texte_volume = "volume +" + str(round(ecart_volume_pct)) + " % vs équipe"
    else:
        texte_volume = "volume " + str(round(ecart_volume_pct)) + " % vs équipe"

    if ecart_csat is not None:
        if ecart_csat >= 0:
            texte_csat = "CSAT +" + str(round(ecart_csat, 2)) + " vs équipe"
        else:
            texte_csat = "CSAT " + str(round(ecart_csat, 2)) + " vs équipe"
    else:
        texte_csat = "CSAT N/A"

    if volume_haut and csat_haut:
        libelle = "Volume et CSAT au-dessus de la moyenne"
    elif volume_haut and not csat_haut:
        libelle = "Volume élevé, CSAT sous la moyenne"
    elif not volume_haut and csat_haut:
        libelle = "CSAT élevé, volume sous la moyenne"
    else:
        libelle = "Volume et CSAT sous la moyenne — à investiguer"

    return libelle + " (" + texte_volume + ", " + texte_csat + ")"


def obtenir_categorie_dominante(tickets_agent):
    categories_agent = grouper_par_categorie(tickets_agent)
    if len(categories_agent) == 0:
        return "N/A"

    plus_grosse_categorie = None
    plus_gros_volume = -1
    for categorie, tickets_cat in categories_agent.items():
        if len(tickets_cat) > plus_gros_volume:
            plus_gros_volume = len(tickets_cat)
            plus_grosse_categorie = categorie
    return plus_grosse_categorie


# ------------------------------------------------------------------
# Onglet 3 : Agents
# ------------------------------------------------------------------

with onglet_agents:
    st.caption(DEFINITION_EN_CRENEAU)

    par_agent = grouper_par(tickets_s2, "assignee")

    # Le/la responsable d'équipe traite volontairement moins de tickets (temps pris par le
    # management) : l'inclure dans la moyenne d'équipe fausserait le point de comparaison pour
    # tout le monde, et la comparer aux autres sur le volume n'a pas de sens non plus.
    volumes = []
    csats_valides = []

    for agent, tickets_agent in par_agent.items():
        if roles_periode.get(agent) == ROLE_RESPONSABLE_EQUIPE:
            continue
        volumes.append(len(tickets_agent))
        csat_agent_valeur = moyenne(tickets_agent, "csat")
        if csat_agent_valeur is not None:
            csats_valides.append(csat_agent_valeur)

    if len(volumes) > 0:
        volume_moyen_equipe = sum(volumes) / len(volumes)
    else:
        volume_moyen_equipe = 0

    if len(csats_valides) > 0:
        csat_moyen_equipe = sum(csats_valides) / len(csats_valides)
    else:
        csat_moyen_equipe = None

    lignes_agents_avec_niveaux = []

    for agent, tickets_agent in par_agent.items():
        volume = len(tickets_agent)
        csat_agent = moyenne(tickets_agent, "csat")
        macro_agent = taux_rempli(tickets_agent, "macro_applied")

        en_creneau_agent = separer_creneau(tickets_agent, planning_s2)[0]
        frt_en_creneau_agent = moyenne(en_creneau_agent, "first_reply_time_min")

        resolution_agent = moyenne(tickets_agent, "full_resolution_time_hours")
        reopens_agent = moyenne(tickets_agent, "reopens")

        role_agent = roles_periode.get(agent, "—")

        if role_agent == ROLE_RESPONSABLE_EQUIPE:
            profil = "Management (volume non comparable aux conseillers)"
        else:
            profil = construire_profil_agent(volume, volume_moyen_equipe, csat_agent, csat_moyen_equipe)

        ligne = {
            "Agent": agent,
            "Rôle": role_agent,
            "Tickets": volume,
            "Catégorie dominante": obtenir_categorie_dominante(tickets_agent),
            "CSAT": formater_csat(csat_agent),
            "1re réponse (en créneau)": "N/A",
            "Résolution moyenne": "N/A",
            "Réouvertures moyennes": "N/A",
            "Utilisation macro (%)": formater_pourcentage(macro_agent),
            "Profil": profil,
        }

        if resolution_agent is not None:
            ligne["Résolution moyenne"] = formater_duree(resolution_agent * 60)

        if reopens_agent is not None:
            ligne["Réouvertures moyennes"] = str(round(reopens_agent, 2))

        niveau_reponse_agent = ""
        if frt_en_creneau_agent is not None:
            ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_agent)
            niveau_reponse_agent = niveau_reponse_ouvree(frt_en_creneau_agent)

        lignes_agents_avec_niveaux.append((ligne, niveau_reponse_agent, niveau_macro(macro_agent)))

    def obtenir_tickets_agent_avec_niveaux(item):
        ligne_agent, niveau_reponse_item, niveau_macro_item = item
        return ligne_agent["Tickets"]

    lignes_agents_avec_niveaux_triees = sorted(
        lignes_agents_avec_niveaux, key=obtenir_tickets_agent_avec_niveaux, reverse=True
    )

    lignes_agents_triees = []
    niveaux_reponse_agents = []
    niveaux_macro_agents = []
    for ligne_agent, niveau_reponse_item, niveau_macro_item in lignes_agents_avec_niveaux_triees:
        lignes_agents_triees.append(ligne_agent)
        niveaux_reponse_agents.append(niveau_reponse_item)
        niveaux_macro_agents.append(niveau_macro_item)

    with st.container(border=True):
        afficher_tableau_colore(
            lignes_agents_triees,
            colonne_figee="Agent",
            colonnes_couleur_bloc={
                "1re réponse (en créneau)": niveaux_reponse_agents,
                "Utilisation macro (%)": niveaux_macro_agents,
            },
        )

    st.markdown(titre_section_principale("Détail par agent"), unsafe_allow_html=True)
    st.caption("D'abord par grande catégorie, puis choisis une catégorie pour voir le détail par sujet")

    for agent, tickets_agent in par_agent.items():
        if agent is not None:
            agent_affiche = agent
        else:
            agent_affiche = "Non assigné"

        with st.expander(agent_affiche):
            categories_agent = grouper_par_categorie(tickets_agent)

            lignes_categories_agent = []
            for categorie, tickets_cat_agent in categories_agent.items():
                csat_cat_agent = moyenne(tickets_cat_agent, "csat")
                macro_cat_agent = taux_rempli(tickets_cat_agent, "macro_applied")

                en_creneau_cat_agent, pause_cat_agent, hors_cat_agent = separer_creneau(tickets_cat_agent, planning_s2)
                frt_cat_agent = moyenne(en_creneau_cat_agent, "first_reply_time_min")

                ligne_cat = {
                    "Catégorie": categorie,
                    "Tickets": len(tickets_cat_agent),
                    "CSAT": "N/A",
                    "1re réponse (en créneau)": "N/A",
                    "Utilisation macro (%)": formater_pourcentage(macro_cat_agent),
                }

                if csat_cat_agent is not None:
                    ligne_cat["CSAT"] = formater_csat(csat_cat_agent)

                if frt_cat_agent is not None:
                    ligne_cat["1re réponse (en créneau)"] = formater_duree(frt_cat_agent)

                lignes_categories_agent.append(ligne_cat)

            lignes_categories_agent_triees = sorted(lignes_categories_agent, key=obtenir_tickets, reverse=True)
            st.dataframe(lignes_categories_agent_triees, hide_index=True, width="stretch")

            noms_categories_agent = list(categories_agent.keys())
            categorie_choisie = st.selectbox(
                "Détail par sujet pour :", noms_categories_agent, key="categorie_" + agent_affiche
            )

            tickets_cat_choisie = categories_agent[categorie_choisie]
            sujets_cat_choisie = grouper_par(tickets_cat_choisie, "subject_cluster")

            lignes_sujets_agent = []
            for sujet, tickets_sujet in sujets_cat_choisie.items():
                csat_sujet = moyenne(tickets_sujet, "csat")
                macro_sujet = taux_rempli(tickets_sujet, "macro_applied")
                reopens_sujet = moyenne(tickets_sujet, "reopens")

                en_creneau_sujet, pause_sujet, hors_sujet = separer_creneau(tickets_sujet, planning_s2)
                frt_sujet = moyenne(en_creneau_sujet, "first_reply_time_min")

                ligne_sujet = {
                    "Sujet": sujet,
                    "Tickets": len(tickets_sujet),
                    "CSAT": "N/A",
                    "1re réponse (en créneau)": "N/A",
                    "Réouvertures moyennes": "N/A",
                    "Utilisation macro (%)": formater_pourcentage(macro_sujet),
                }

                if csat_sujet is not None:
                    ligne_sujet["CSAT"] = formater_csat(csat_sujet)

                if frt_sujet is not None:
                    ligne_sujet["1re réponse (en créneau)"] = formater_duree(frt_sujet)

                if reopens_sujet is not None:
                    ligne_sujet["Réouvertures moyennes"] = str(round(reopens_sujet, 2))

                lignes_sujets_agent.append(ligne_sujet)

            lignes_sujets_agent_triees = sorted(lignes_sujets_agent, key=obtenir_tickets, reverse=True)
            st.dataframe(lignes_sujets_agent_triees, hide_index=True, width="stretch")


SEUIL_TOP_ALERTES = 6


def construire_carte_alerte(alerte):
    return (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        "border-left:6px solid " + COULEUR_ACCENT_CRITIQUE + '; border-radius:10px; padding:14px 16px; margin-bottom:10px;">'
        '<div style="font-size:13px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">' + alerte["quoi"] + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:5px;"><b>Pourquoi</b> : '
        + alerte["pourquoi"] + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;"><b>Cause probable</b> : '
        + alerte["cause"] + "</div>"
        '<div style="font-size:12px; font-weight:600; color:' + COULEUR_ACCENT_CRITIQUE + '; margin-top:5px;">'
        "<b>Action</b> : " + alerte["action"] + "</div>"
        "</div>"
    )


# Catégorie où CSAT ET délai se dégradent ensemble — le score pondère par le volume concerné
# (une dégradation sur 5 tickets ne mérite pas la même place qu'une dégradation sur 80).
def construire_candidats_categorie(categories_s2, categories_s1):
    candidats = []
    for categorie, tickets_cat_s2 in categories_s2.items():
        tickets_cat_s1 = categories_s1.get(categorie, [])
        if len(tickets_cat_s1) == 0:
            continue

        csat_cat_s1 = moyenne(tickets_cat_s1, "csat")
        csat_cat_s2 = moyenne(tickets_cat_s2, "csat")
        frt_cat_s1 = moyenne(tickets_cat_s1, "first_reply_time_min")
        frt_cat_s2 = moyenne(tickets_cat_s2, "first_reply_time_min")

        if csat_cat_s1 is None or csat_cat_s2 is None or frt_cat_s1 is None or frt_cat_s2 is None:
            continue

        delta_csat = csat_cat_s2 - csat_cat_s1
        delta_frt = frt_cat_s2 - frt_cat_s1
        if delta_csat >= 0 or delta_frt <= 0:
            continue

        volume = len(tickets_cat_s2)
        candidats.append({
            "quoi": (
                categorie + " — CSAT " + formater_csat(csat_cat_s1) + " → " + formater_csat(csat_cat_s2)
                + ", 1re réponse " + formater_duree(frt_cat_s1) + " → " + formater_duree(frt_cat_s2)
            ),
            "pourquoi": (
                "CSAT et délai de 1re réponse se dégradent ensemble sur " + str(volume) + " tickets — "
                "signal plus fiable qu'une seule métrique isolée."
            ),
            "cause": "à confirmer avec les événements de la période (onglet Vue d'ensemble).",
            "action": "Ouvrir Vue d'ensemble pour isoler quels sujets de " + categorie + " tirent la dégradation.",
            "score": volume * (abs(delta_csat) + delta_frt / 60),
        })
    return candidats


def construire_candidats_macro(suggestions_creation, suggestions_amelioration):
    candidats = []
    for ligne in suggestions_creation:
        candidats.append({
            "quoi": (
                "« " + ligne["Sujet"] + " » — " + str(ligne["Tickets"]) + " tickets, CSAT " + ligne["CSAT"]
                + ", quasi aucune macro utilisée"
            ),
            "pourquoi": (
                "Volume suffisant et satisfaction insuffisante, sans réponse-type en place — le traitement "
                "repose sur chaque agent individuellement."
            ),
            "cause": "Aucune macro n'existe encore pour ce sujet.",
            "action": "Créer une macro pour « " + ligne["Sujet"] + " ».",
            "score": ligne["Tickets"] * 3,
        })
    for ligne in suggestions_amelioration:
        candidats.append({
            "quoi": (
                "« " + ligne["Sujet"] + " » — " + str(ligne["Tickets"]) + " tickets, CSAT " + ligne["CSAT"]
                + ", macro déjà bien utilisée"
            ),
            "pourquoi": (
                "La macro est utilisée mais la satisfaction reste insuffisante — le contenu ou le process, "
                "pas l'adoption, semble en cause."
            ),
            "cause": "à investiguer : contenu de la macro ou nature du problème sous-jacent.",
            "action": "Relire la macro de « " + ligne["Sujet"] + " » et vérifier si le problème dépasse ce "
            "qu'une réponse-type peut résoudre.",
            "score": ligne["Tickets"] * 3.5,
        })
    return candidats


def construire_candidats_faq(suggestions_faq):
    candidats = []
    for ligne in suggestions_faq:
        candidats.append({
            "quoi": (
                "« " + ligne["Sujet"] + " » — " + str(ligne["Tickets"]) + " tickets, " + ligne["Échanges moyens"]
                + " échanges en moyenne"
            ),
            "pourquoi": (
                "La résolution demande plusieurs allers-retours — signe qu'une information manque au client "
                "dès le premier contact."
            ),
            "cause": "Pas de FAQ/page d'aide dédiée à ce sujet actuellement.",
            "action": "Créer une FAQ pour « " + ligne["Sujet"] + " ».",
            "score": ligne["Tickets"] * float(ligne["Échanges moyens"]),
        })
    return candidats


def construire_candidats_verbatims(sujets_verbatims_tries):
    candidats = []
    for sujet, tickets_sujet_verbatims in sujets_verbatims_tries:
        candidats.append({
            "quoi": (
                "« " + sujet + " » — " + str(len(tickets_sujet_verbatims)) + " commentaires clients à CSAT très bas"
            ),
            "pourquoi": "Volume de retours négatifs assez important pour être un irritant récurrent, pas un client isolé.",
            "cause": "voir le détail qualitatif des commentaires plus bas.",
            "action": "Lire les verbatims de « " + sujet + " » pour qualifier l'irritant exact.",
            "score": len(tickets_sujet_verbatims) * 2,
        })
    return candidats


# ------------------------------------------------------------------
# Onglet 4 : Alertes & suggestions
# ------------------------------------------------------------------

with onglet_alertes:
    # ------------------------------------------------------------------
    # Données — chaque générateur reste inchangé (mêmes seuils, mêmes calculs), simplement
    # regroupé ici avant tout affichage pour pouvoir prioriser sur l'ensemble des candidats
    # avant de décider ce qui mérite la place principale de la page.
    # ------------------------------------------------------------------

    candidats_categorie = []
    if comparaison_disponible:
        candidats_categorie = construire_candidats_categorie(categories_s2, categories_s1)

    categories_resolution = {}
    for ticket in tickets_s2:
        if ticket["full_resolution_time_hours"] is None:
            continue
        categorie_ticket = categoriser(ticket)
        if categorie_ticket in categories_resolution:
            categories_resolution[categorie_ticket].append(ticket)
        else:
            categories_resolution[categorie_ticket] = [ticket]

    lignes_resolution_categorie = []
    for categorie, tickets_categorie in categories_resolution.items():
        resolution_moyenne = moyenne(tickets_categorie, "full_resolution_time_hours")
        macro_categorie = taux_rempli(tickets_categorie, "macro_applied")

        resolutions_types = grouper_par(tickets_categorie, "resolution_type")
        resolution_principale = "—"
        plus_grand_compte = 0
        for type_resolution, tickets_type_resolution in resolutions_types.items():
            if len(tickets_type_resolution) > plus_grand_compte:
                plus_grand_compte = len(tickets_type_resolution)
                resolution_principale = type_resolution

        if macro_categorie < SEUIL_MACRO_BASSE:
            commentaire_macro = "Peu/pas de macro utilisée"
        else:
            commentaire_macro = "Macro bien utilisée"

        lignes_resolution_categorie.append({
            "resolution_tri": resolution_moyenne,
            "Catégorie": categorie,
            "Tickets": len(tickets_categorie),
            "Résolution moyenne": formater_duree(resolution_moyenne * 60),
            "Résolution la plus fréquente": resolution_principale,
            "Macro": commentaire_macro,
        })

    def obtenir_resolution_tri(ligne):
        return ligne["resolution_tri"]

    lignes_resolution_categorie_triees = sorted(lignes_resolution_categorie, key=obtenir_resolution_tri, reverse=True)
    for ligne in lignes_resolution_categorie_triees:
        del ligne["resolution_tri"]

    def obtenir_resolution(ticket):
        return ticket["full_resolution_time_hours"]

    tickets_avec_resolution = []
    for ticket in tickets_s2:
        if ticket["full_resolution_time_hours"] is not None:
            tickets_avec_resolution.append(ticket)

    tickets_tries_par_resolution = sorted(tickets_avec_resolution, key=obtenir_resolution, reverse=True)

    lignes_longs = []
    for ticket in tickets_tries_par_resolution[:10]:
        lignes_longs.append(
            {
                "Ticket": ticket["ticket_id"],
                "Agent": ticket["assignee"],
                "Catégorie": categoriser(ticket),
                "Résolution": formater_duree(ticket["full_resolution_time_hours"] * 60),
                "Résolu par": ticket["resolution_type"],
            }
        )

    sujets_s2 = grouper_par(tickets_s2, "subject_cluster")

    suivi_suggestions = charger_suivi_suggestions(FICHIER_SUIVI_SUGGESTIONS)

    suggestions_creation = []
    suggestions_partielle = []
    suggestions_amelioration = []

    for sujet, tickets_sujet in sujets_s2.items():
        volume = len(tickets_sujet)
        if volume < SEUIL_MINIMUM_SUJET:
            continue

        csat_sujet = moyenne(tickets_sujet, "csat")
        if csat_sujet is None or csat_sujet >= SEUIL_CSAT_INSATISFAISANT:
            continue

        entree_suivi = suivi_suggestions.get(sujet)
        if entree_suivi is not None and entree_suivi["statut"] == "Fait" and entree_suivi["date_action"] is not None:
            continue

        macro_sujet = taux_rempli(tickets_sujet, "macro_applied")

        ligne = {
            "Sujet": sujet,
            "Tickets": volume,
            "CSAT": formater_csat(csat_sujet),
            "Utilisation macro (%)": formater_pourcentage(macro_sujet),
        }

        if macro_sujet < SEUIL_MACRO_BASSE:
            suggestions_creation.append(ligne)
        elif macro_sujet >= SEUIL_MACRO_HAUTE:
            suggestions_amelioration.append(ligne)
        else:
            suggestions_partielle.append(ligne)

    suggestions_faq = []
    for sujet, tickets_sujet in sujets_s2.items():
        volume = len(tickets_sujet)
        if volume < SEUIL_MINIMUM_SUJET:
            continue

        entree_suivi = suivi_suggestions.get(sujet)
        if entree_suivi is not None and entree_suivi["statut"] == "Fait" and entree_suivi["date_action"] is not None:
            continue

        replies_moyen = moyenne(tickets_sujet, "replies")
        if replies_moyen is None or replies_moyen < SEUIL_REPLIES_FAQ:
            continue

        suggestions_faq.append({
            "Sujet": sujet,
            "Tickets": volume,
            "Échanges moyens": str(round(replies_moyen, 1)),
        })

    tickets_verbatims = []
    for ticket in tickets_s2:
        csat_ticket = ticket["csat"]
        commentaire = ticket["csat_comment"]
        if csat_ticket is not None and csat_ticket <= SEUIL_CSAT_VERBATIM and commentaire:
            tickets_verbatims.append(ticket)

    sujets_verbatims = grouper_par(tickets_verbatims, "subject_cluster")

    sujets_verbatims_significatifs = []
    for sujet, tickets_sujet_verbatims in sujets_verbatims.items():
        if len(tickets_sujet_verbatims) >= SEUIL_VERBATIMS_GROUPE:
            sujets_verbatims_significatifs.append((sujet, tickets_sujet_verbatims))

    def obtenir_compte_verbatims(item):
        sujet, tickets_sujet = item
        return len(tickets_sujet)

    sujets_verbatims_tries = sorted(sujets_verbatims_significatifs, key=obtenir_compte_verbatims, reverse=True)

    def obtenir_date_ticket(ticket):
        return ticket["created_at"]

    sujets_traites = []
    for sujet, entree in suivi_suggestions.items():
        if entree["statut"] == "Fait" and entree["date_action"] is not None:
            sujets_traites.append((sujet, entree))

    lignes_suivi = []
    if len(sujets_traites) > 0:
        sujets_historique = grouper_par(tickets_historique_business, "subject_cluster")

        for sujet, entree in sujets_traites:
            tickets_sujet_historique = sujets_historique.get(sujet, [])
            impact = impact_avant_apres(tickets_sujet_historique, entree["date_action"])

            notes = entree["notes"]
            if notes is None:
                notes = ""

            lignes_suivi.append({
                "Sujet": sujet,
                "Date action": entree["date_action"].strftime("%d/%m/%Y"),
                "Tickets avant": impact["volume_avant"],
                "Tickets après": impact["volume_apres"],
                "CSAT avant": formater_csat(impact["csat_avant"]),
                "CSAT après": formater_csat(impact["csat_apres"]),
                "Utilisation macro avant (%)": formater_pourcentage(impact["macro_avant"]),
                "Utilisation macro après (%)": formater_pourcentage(impact["macro_apres"]),
                "Notes": notes,
            })

    lignes_macros_associees = []
    for sujet, entree in sujets_traites:
        code_macro = extraire_code_macro(entree["notes"])
        texte_macro = charger_texte_macro(code_macro, DOSSIER_MACROS)
        if texte_macro is not None:
            nom_fichier_faq = extraire_nom_fichier_faq(texte_macro)
            faq_associee = "—"
            if nom_fichier_faq is not None:
                texte_faq = charger_texte_faq(nom_fichier_faq, DOSSIER_FAQ)
                if texte_faq is not None:
                    faq_associee = nom_fichier_faq

            lignes_macros_associees.append({
                "Sujet": sujet,
                "Macro": code_macro,
                "FAQ associée": faq_associee,
            })

    # ------------------------------------------------------------------
    # Alertes prioritaires — jusqu'à SEUIL_TOP_ALERTES, classées par sévérité × impact,
    # à partir de tous les générateurs ci-dessus. Le reste (toujours calculé, jamais perdu)
    # est accessible dans "Voir plus" plus bas, pas supprimé.
    # ------------------------------------------------------------------

    candidats_alertes = (
        candidats_categorie
        + construire_candidats_macro(suggestions_creation, suggestions_amelioration)
        + construire_candidats_faq(suggestions_faq)
        + construire_candidats_verbatims(sujets_verbatims_tries)
    )
    candidats_alertes_tries = sorted(candidats_alertes, key=obtenir_score_insight, reverse=True)
    alertes_prioritaires = candidats_alertes_tries[:SEUIL_TOP_ALERTES]

    st.markdown(titre_section_principale("Alertes prioritaires"), unsafe_allow_html=True)
    st.caption(
        "Classées par sévérité et volume concerné, tous générateurs confondus (dégradation catégorie, "
        "macro/FAQ manquante, verbatims négatifs). Pas de liste exhaustive — le reste est dans "
        "\"Voir plus\" plus bas."
    )
    if len(alertes_prioritaires) > 0:
        for alerte in alertes_prioritaires:
            st.markdown(construire_carte_alerte(alerte), unsafe_allow_html=True)
    else:
        st.caption("Aucune alerte prioritaire sur cette période.")

    if len(candidats_alertes_tries) > SEUIL_TOP_ALERTES:
        st.caption(
            str(len(candidats_alertes_tries) - SEUIL_TOP_ALERTES) + " alerte(s) supplémentaire(s) de "
            "moindre priorité — voir \"Voir plus\" plus bas."
        )

    st.divider()
    st.markdown(titre_section_principale("Temps de résolution par catégorie"), unsafe_allow_html=True)
    st.caption(
        "Trié par temps de résolution moyen, du plus long au plus court — la vraie question n'est pas "
        "\"quel ticket a traîné\" mais \"quelle catégorie prend le plus de temps à l'équipe\"."
    )
    with st.container(border=True):
        st.dataframe(lignes_resolution_categorie_triees, hide_index=True, width="stretch")

    with st.expander("Voir plus d'alertes et de détails"):
        st.caption(
            "Détail complet de chaque générateur d'alerte, y compris ce qui n'a pas été jugé prioritaire "
            "ci-dessus — rien n'est supprimé, seulement démoté."
        )

        st.markdown("**Les 10 tickets les plus longs**")
        st.dataframe(lignes_longs, hide_index=True, width="stretch")

        st.markdown("**Dégradation par catégorie**")
        if not comparaison_disponible:
            st.caption("Active « Comparer à une autre période » dans la barre latérale pour voir ce signal.")
        elif len(candidats_categorie) == 0:
            st.caption("Aucune catégorie ne dégrade simultanément CSAT et temps de réponse sur cette période.")
        else:
            candidats_categorie_tries = sorted(candidats_categorie, key=obtenir_score_insight, reverse=True)
            for candidat in candidats_categorie_tries:
                st.write("- " + candidat["quoi"])

        st.markdown("**Suggestions - macro à créer**")
        st.caption(
            "Sujet avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets, CSAT < "
            + str(SEUIL_CSAT_INSATISFAISANT) + ", quasi aucune macro utilisée"
        )
        afficher_tableau_colore(suggestions_creation)

        st.markdown("**Suggestions - macro à renforcer (adoption partielle)**")
        st.caption(
            "Utilisation macro entre " + str(SEUIL_MACRO_BASSE) + " % et " + str(SEUIL_MACRO_HAUTE) + " % "
            "et CSAT insatisfaisant — la macro existe mais n'est pas assez systématiquement utilisée."
        )
        afficher_tableau_colore(suggestions_partielle)

        st.markdown("**Suggestions - macro / process à améliorer**")
        st.caption("Macro déjà bien utilisée mais CSAT insatisfaisant quand même.")
        afficher_tableau_colore(suggestions_amelioration)

        st.markdown("**Suggestions - FAQ à créer**")
        st.caption(
            "Sujet avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets et " + str(SEUIL_REPLIES_FAQ)
            + " échanges en moyenne ou plus."
        )
        afficher_tableau_colore(suggestions_faq)

        st.markdown("**Verbatims clients (CSAT bas)**")
        st.caption(
            "CSAT ≤ " + str(SEUIL_CSAT_VERBATIM) + ", un sujet n'est affiché qu'à partir de "
            + str(SEUIL_VERBATIMS_GROUPE) + " commentaires similaires. Les 3 commentaires les plus "
            "récents sont affichés par sujet."
        )
        if len(sujets_verbatims_tries) == 0:
            st.write(
                "Aucun sujet avec au moins " + str(SEUIL_VERBATIMS_GROUPE) + " commentaires similaires sur "
                "cette période."
            )
        else:
            for sujet, tickets_sujet_verbatims in sujets_verbatims_tries:
                tickets_recents = sorted(tickets_sujet_verbatims, key=obtenir_date_ticket, reverse=True)[:3]

                titre_expander = sujet + " (" + str(len(tickets_sujet_verbatims)) + " commentaire(s))"
                with st.expander(titre_expander):
                    lignes_verbatims_sujet = []
                    for ticket in tickets_recents:
                        lignes_verbatims_sujet.append({
                            "CSAT": ticket["csat"],
                            "Commentaire": ticket["csat_comment"],
                        })
                    st.dataframe(lignes_verbatims_sujet, hide_index=True, width="stretch")

        st.markdown("**Mots fréquents (sujets à faible CSAT)**")
        if len(suggestions_creation) == 0:
            st.write("Aucun sujet signalé à faible CSAT sur cette période.")
        else:
            for ligne_suggestion in suggestions_creation:
                sujet_signale = ligne_suggestion["Sujet"]
                tickets_sujet_signale = sujets_s2.get(sujet_signale, [])
                mots_top = mots_frequents(tickets_sujet_signale, "first_message", 5)

                if len(mots_top) == 0:
                    continue

                texte_mots = ""
                for i in range(len(mots_top)):
                    mot, compte = mots_top[i]
                    if i > 0:
                        texte_mots = texte_mots + ", "
                    texte_mots = texte_mots + mot + " (" + str(compte) + ")"

                st.write("**" + sujet_signale + "** : " + texte_mots)

        st.markdown("**Suivi des suggestions**")
        st.caption(
            "Sujets marqués « Fait » dans le fichier de suivi — impact mesuré avant/après la date "
            "d'action, sur tout l'historique disponible (pas seulement la période affichée)."
        )
        afficher_tableau_colore(lignes_suivi)

        if len(lignes_macros_associees) > 0:
            st.markdown("**Macros/FAQ associées**")
            st.caption("Texte complet dans le CRM, pas dupliqué ici.")
            st.dataframe(lignes_macros_associees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 5 : Couverture & réactivité
# ------------------------------------------------------------------

with onglet_creneaux:
    st.markdown(titre_section_principale("Couverture & réactivité"), unsafe_allow_html=True)
    st.caption("Sommes-nous disponibles aux bons moments et répondons-nous suffisamment vite ?")
    st.caption(DEFINITION_EN_CRENEAU)

    en_creneau, pause_dejeuner, hors_creneau = separer_creneau(tickets_s2, planning_s2)
    tickets_hors_tout = pause_dejeuner + hors_creneau
    volume_total_creneaux = len(tickets_s2)
    pct_en_creneau = len(en_creneau) / volume_total_creneaux * 100

    en_creneau_s1 = []
    tickets_hors_tout_s1 = []
    part_hors_couverture_s1 = None
    if comparaison_disponible:
        en_creneau_s1, pause_dejeuner_s1, hors_creneau_s1 = separer_creneau(tickets_s1, planning_s1)
        tickets_hors_tout_s1 = pause_dejeuner_s1 + hors_creneau_s1
        if len(tickets_s1) > 0:
            part_hors_couverture_s1 = len(tickets_hors_tout_s1) / len(tickets_s1) * 100

    # ------------------------------------------------------------------
    # Données de couverture partagées par plusieurs sections plus bas (grille heure x jour,
    # taux SLA, répartition par canal, volume hors couverture) — calculées une seule fois ici.
    # ------------------------------------------------------------------

    agents_grille = construire_agents_grille(tickets_s2, planning_s2_dernier)
    horaires_standard = planning_s2_dernier.get(NOM_AGENT_DEFAUT, {})
    grille_creneaux = construire_grille_creneaux(tickets_s2, planning_s2_dernier, agents_grille, horaires_standard)

    totaux_jour = {}
    for nom_jour, numero_jour in JOURS_ORDRE:
        totaux_jour[nom_jour] = 0
    for entree in grille_creneaux:
        totaux_jour[entree["jour"]] = totaux_jour[entree["jour"]] + entree["demandes"]

    jour_le_plus_charge = None
    volume_max_jour = -1
    for nom_jour, numero_jour in JOURS_ORDRE:
        if totaux_jour[nom_jour] > volume_max_jour:
            volume_max_jour = totaux_jour[nom_jour]
            jour_le_plus_charge = nom_jour

    creneau_le_plus_charge = None
    ratio_max = -1
    for entree in grille_creneaux:
        if entree["ratio"] is not None and entree["ratio"] > ratio_max:
            ratio_max = entree["ratio"]
            creneau_le_plus_charge = entree

    situations_tension = []
    for entree in grille_creneaux:
        if entree["niveau"] == "HOTSPOT":
            situations_tension.append(entree)

    def obtenir_ratio_tri_situation(entree):
        if entree["ratio"] is None:
            return float("inf")
        return entree["ratio"]

    situations_tension_triees = sorted(situations_tension, key=obtenir_ratio_tri_situation, reverse=True)

    taux_sla_global = taux_sla(tickets_s2, planning_s2)
    taux_sla_s1 = None
    nb_tensions_s1 = None
    if comparaison_disponible:
        taux_sla_s1 = taux_sla(tickets_s1, planning_s1)
        agents_grille_s1 = construire_agents_grille(tickets_s1, planning_s1_dernier)
        horaires_standard_s1 = planning_s1_dernier.get(NOM_AGENT_DEFAUT, {})
        grille_creneaux_s1 = construire_grille_creneaux(
            tickets_s1, planning_s1_dernier, agents_grille_s1, horaires_standard_s1
        )
        nb_tensions_s1 = 0
        for entree in grille_creneaux_s1:
            if entree["niveau"] == "HOTSPOT":
                nb_tensions_s1 = nb_tensions_s1 + 1

    par_canal_en = grouper_par(en_creneau, "via_channel")
    par_canal_en_s1 = grouper_par(en_creneau_s1, "via_channel")

    def formater_delta_duree_min(delta_minutes):
        if delta_minutes >= 0:
            fleche = "↑ +"
        else:
            fleche = "↓ "
            delta_minutes = -delta_minutes
        return fleche + formater_duree(round(delta_minutes))

    lignes_canal_en_avec_niveaux = []
    for canal, tickets_canal in par_canal_en.items():
        frt_canal = moyenne(tickets_canal, "first_reply_time_min")
        ligne = {"Canal": canal, "Tickets": len(tickets_canal), "1re réponse moyenne": "N/A"}

        niveau_reponse_canal = ""
        if frt_canal is not None:
            ligne["1re réponse moyenne"] = formater_duree(frt_canal)
            niveau_reponse_canal = niveau_reponse_ouvree(frt_canal)

        if comparaison_disponible:
            tickets_canal_s1 = par_canal_en_s1.get(canal, [])
            frt_canal_s1 = moyenne(tickets_canal_s1, "first_reply_time_min")
            if frt_canal is not None and frt_canal_s1 is not None:
                ligne["Évolution"] = formater_delta_duree_min(frt_canal - frt_canal_s1)
            else:
                ligne["Évolution"] = "N/A"

        lignes_canal_en_avec_niveaux.append((ligne, niveau_reponse_canal))

    def obtenir_tickets_canal_avec_niveau(item):
        ligne_canal, niveau_reponse_item = item
        return ligne_canal["Tickets"]

    lignes_canal_en_avec_niveaux_triees = sorted(
        lignes_canal_en_avec_niveaux, key=obtenir_tickets_canal_avec_niveau, reverse=True
    )

    lignes_canal_en_triees = []
    niveaux_reponse_canal = []
    for ligne_canal, niveau_reponse_item in lignes_canal_en_avec_niveaux_triees:
        lignes_canal_en_triees.append(ligne_canal)
        niveaux_reponse_canal.append(niveau_reponse_item)

    pire_canal = canal_le_plus_problematique(lignes_canal_en_triees, niveaux_reponse_canal)

    volume_hors_couverture_actuel = len(tickets_hors_tout)
    part_hors_couverture = volume_hors_couverture_actuel / volume_total_creneaux * 100

    volumes_baseline_hors_couverture = calculer_baseline_hors_couverture(
        exports_disponibles, date_a_debut, NB_SEMAINES_BASELINE_HORS_COUVERTURE
    )
    if len(volumes_baseline_hors_couverture) > 0:
        moyenne_baseline_hors_couverture = (
            sum(volumes_baseline_hors_couverture) / len(volumes_baseline_hors_couverture)
        )
    else:
        moyenne_baseline_hors_couverture = None

    hors_couverture_significatif = hors_couverture_est_significatif(
        volume_hors_couverture_actuel, moyenne_baseline_hors_couverture
    )

    # ------------------------------------------------------------------
    # Synthèse de la période — 4 chiffres, la question directrice de tout l'onglet.
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Synthèse de la période"), unsafe_allow_html=True)

    colonne_s1, colonne_s2, colonne_s3, colonne_s4 = st.columns(4)

    if comparaison_disponible:
        colonne_s1.markdown(
            construire_carte_kpi(
                "Demandes reçues", formater_nombre_espace(volume_total_creneaux),
                delta=volume_total_creneaux - len(tickets_s1), delta_couleur="off",
            ),
            unsafe_allow_html=True,
        )
    else:
        colonne_s1.markdown(
            construire_carte_kpi("Demandes reçues", formater_nombre_espace(volume_total_creneaux)),
            unsafe_allow_html=True,
        )

    if taux_sla_global is not None:
        if comparaison_disponible and taux_sla_s1 is not None:
            colonne_s2.markdown(
                construire_carte_kpi(
                    "SLA respecté", formater_pourcentage(taux_sla_global),
                    delta=round(taux_sla_global - taux_sla_s1, 1),
                ),
                unsafe_allow_html=True,
            )
        else:
            colonne_s2.markdown(
                construire_carte_kpi("SLA respecté", formater_pourcentage(taux_sla_global)),
                unsafe_allow_html=True,
            )

    if jour_le_plus_charge is not None:
        if len(fichiers_actuels) > 1:
            volume_jour_affiche = round(volume_max_jour / len(fichiers_actuels))
            suffixe_jour = " demandes en moyenne"
        else:
            volume_jour_affiche = volume_max_jour
            suffixe_jour = " demandes"
        colonne_s3.markdown(
            construire_carte_kpi(
                "Jour le plus chargé", jour_le_plus_charge,
                sous_texte=formater_nombre_espace(volume_jour_affiche) + suffixe_jour,
            ),
            unsafe_allow_html=True,
        )

    if creneau_le_plus_charge is not None:
        texte_creneau_max = (
            creneau_le_plus_charge["jour"] + " " + str(creneau_le_plus_charge["heure"]) + "h-"
            + str(creneau_le_plus_charge["heure"] + 1) + "h"
        )
        if len(fichiers_actuels) > 1:
            ratio_affiche = ratio_max / len(fichiers_actuels)
            suffixe_ratio = " demandes/agent en moyenne"
        else:
            ratio_affiche = ratio_max
            suffixe_ratio = " demandes/agent"
        colonne_s4.markdown(
            construire_carte_kpi(
                "Créneau habituellement le plus chargé", texte_creneau_max,
                sous_texte=str(round(ratio_affiche, 1)) + suffixe_ratio,
            ),
            unsafe_allow_html=True,
        )

    pic_exceptionnel = None
    if creneau_le_plus_charge is not None:
        pic_exceptionnel = detecter_pic_exceptionnel(
            fichiers_actuels, agents_grille, creneau_le_plus_charge["ratio"],
            creneau_le_plus_charge["jour"], creneau_le_plus_charge["heure"],
        )
    if pic_exceptionnel is not None:
        st.caption(
            "Pic exceptionnel observé : " + pic_exceptionnel["jour"] + " " + str(pic_exceptionnel["heure"])
            + "h-" + str(pic_exceptionnel["heure"] + 1) + "h, " + str(round(pic_exceptionnel["ratio"], 1))
            + " demandes/agent — nettement au-dessus du rythme habituel."
        )

    # ------------------------------------------------------------------
    # Réactivité & SLA
    # ------------------------------------------------------------------

    st.divider()
    st.markdown(titre_section_principale("Réactivité & SLA"), unsafe_allow_html=True)
    st.caption(
        "SLA : en créneau ouvert, 1re réponse sous 1h. Hors créneau, réponse attendue au plus tard à la "
        "fin de la 1re plage horaire du prochain jour disponible — ex : message reçu vendredi 19h, "
        "réponse due lundi avant 12h (avant l'ouverture ou pendant la pause déjeuner : réponse due "
        "avant la fin du jour même)."
    )

    if taux_sla_global is not None:
        delta_sla = None
        if comparaison_disponible and taux_sla_s1 is not None:
            delta_sla = round(taux_sla_global - taux_sla_s1, 1)
        st.markdown(construire_carte_sla(taux_sla_global, SLA_OBJECTIF_PCT, delta=delta_sla), unsafe_allow_html=True)

        insight_sla = construire_insight_sla(taux_sla_global, SLA_OBJECTIF_PCT, pire_canal)
        if insight_sla is not None:
            st.caption(insight_sla)

    st.markdown("**Répartition des temps de réponse, tickets reçus en créneau**")

    compte_niveaux = {"OK": 0, "A SURVEILLER": 0, "CRITIQUE": 0, "DEBORDEMENT": 0}
    for ticket in en_creneau:
        frt_ticket = ticket["first_reply_time_min"]
        if frt_ticket is not None:
            niveau = niveau_reponse_ouvree(frt_ticket)
            compte_niveaux[niveau] = compte_niveaux[niveau] + 1

    st.markdown(construire_barre_empilee_reponse(compte_niveaux, len(en_creneau)), unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Performance par canal
    # ------------------------------------------------------------------

    st.divider()
    st.markdown(titre_section_principale("Performance par canal"), unsafe_allow_html=True)

    with st.container(border=True):
        afficher_tableau_colore(
            lignes_canal_en_triees,
            colonnes_couleur_bloc={"1re réponse moyenne": niveaux_reponse_canal},
        )

    insight_canal = construire_insight_canal(pire_canal)
    if insight_canal is not None:
        st.caption(insight_canal)

    # ------------------------------------------------------------------
    # Demande hors couverture
    # ------------------------------------------------------------------

    st.divider()
    st.markdown(titre_section_principale("Demande hors couverture"), unsafe_allow_html=True)
    st.caption("La demande reçue hors couverture justifie-t-elle une adaptation des horaires ?")

    frt_en_creneau_global = moyenne(en_creneau, "first_reply_time_min")
    frt_en_creneau_global_s1 = None
    if comparaison_disponible:
        frt_en_creneau_global_s1 = moyenne(en_creneau_s1, "first_reply_time_min")

    colonne_h1, colonne_h2, colonne_h3 = st.columns(3)
    colonne_h1.markdown(
        construire_carte_kpi(
            "Reçus pendant la couverture", formater_nombre_espace(len(en_creneau)),
            sous_texte=formater_pourcentage(pct_en_creneau) + " du volume",
        ),
        unsafe_allow_html=True,
    )

    delta_part_hors_couverture = None
    if part_hors_couverture_s1 is not None:
        delta_part_hors_couverture = round(part_hors_couverture - part_hors_couverture_s1, 1)

    if delta_part_hors_couverture is not None:
        html_carte_hors_couv = construire_carte_kpi(
            "Reçus hors couverture", formater_nombre_espace(volume_hors_couverture_actuel),
            delta=delta_part_hors_couverture, delta_couleur="inverse",
            sous_texte=formater_pourcentage(part_hors_couverture) + " du volume",
        )
    else:
        html_carte_hors_couv = construire_carte_kpi(
            "Reçus hors couverture", formater_nombre_espace(volume_hors_couverture_actuel),
            sous_texte=formater_pourcentage(part_hors_couverture) + " du volume",
        )
    colonne_h2.markdown(html_carte_hors_couv, unsafe_allow_html=True)

    if frt_en_creneau_global is not None:
        delta_frt_couverture = None
        if frt_en_creneau_global_s1 is not None:
            delta_frt_couverture = round(frt_en_creneau_global - frt_en_creneau_global_s1)

        if delta_frt_couverture is not None:
            html_carte_frt_couverture = construire_carte_kpi(
                "Délai moyen de 1re réponse en couverture", formater_duree(frt_en_creneau_global),
                delta=str(delta_frt_couverture) + " min", delta_couleur="inverse",
            )
        else:
            html_carte_frt_couverture = construire_carte_kpi(
                "Délai moyen de 1re réponse en couverture", formater_duree(frt_en_creneau_global),
            )
        colonne_h3.markdown(html_carte_frt_couverture, unsafe_allow_html=True)

    lignes_hors_couverture = construire_lignes_hors_couverture(tickets_hors_tout, planning_s2, volume_total_creneaux)
    with st.container(border=True):
        st.dataframe(lignes_hors_couverture, hide_index=True, width="stretch")

    if hors_couverture_significatif:
        type_signal = type_signal_hors_couverture(volumes_baseline_hors_couverture)
        st.markdown(
            construire_carte_hors_couverture(
                volume_hors_couverture_actuel, moyenne_baseline_hors_couverture,
                len(volumes_baseline_hors_couverture), type_signal, tickets_hors_tout,
            ),
            unsafe_allow_html=True,
        )
    else:
        st.caption(
            "Le volume hors couverture reste dans la norme historique — pas de signal justifiant une "
            "adaptation des horaires actuellement."
        )

    with st.expander("Détail : pourquoi et comment"):
        groupes_type_categorie = {}
        for ticket in tickets_hors_tout:
            type_detail = type_hors_creneau_detaille(ticket["created_at"], ticket["assignee"], planning_s2)
            cle = (type_detail, categoriser(ticket))
            if cle in groupes_type_categorie:
                groupes_type_categorie[cle].append(ticket)
            else:
                groupes_type_categorie[cle] = [ticket]

        lignes_type_categorie = []
        for cle, tickets_groupe in groupes_type_categorie.items():
            type_detail, categorie = cle
            frt_groupe = moyenne(tickets_groupe, "first_reply_time_min")
            csat_groupe = moyenne(tickets_groupe, "csat")

            ligne = {
                "Type": type_detail, "Catégorie": categorie, "Tickets": len(tickets_groupe),
                "Délai de rattrapage": "N/A", "CSAT": "N/A",
            }
            if frt_groupe is not None:
                ligne["Délai de rattrapage"] = formater_duree(frt_groupe)
            if csat_groupe is not None:
                ligne["CSAT"] = formater_csat(csat_groupe)
            lignes_type_categorie.append(ligne)

        st.write("Pourquoi (par catégorie de demande) :")
        lignes_type_categorie_triees = sorted(lignes_type_categorie, key=obtenir_tickets, reverse=True)
        st.dataframe(lignes_type_categorie_triees, hide_index=True, width="stretch")

        groupes_type_canal = {}
        for ticket in tickets_hors_tout:
            type_detail = type_hors_creneau_detaille(ticket["created_at"], ticket["assignee"], planning_s2)
            cle = (type_detail, ticket["via_channel"])
            if cle in groupes_type_canal:
                groupes_type_canal[cle].append(ticket)
            else:
                groupes_type_canal[cle] = [ticket]

        lignes_type_canal = []
        for cle, tickets_groupe in groupes_type_canal.items():
            type_detail, canal = cle
            frt_groupe = moyenne(tickets_groupe, "first_reply_time_min")
            csat_groupe = moyenne(tickets_groupe, "csat")

            ligne = {
                "Type": type_detail, "Canal": canal, "Tickets": len(tickets_groupe),
                "Délai de rattrapage": "N/A", "CSAT": "N/A",
            }
            if frt_groupe is not None:
                ligne["Délai de rattrapage"] = formater_duree(frt_groupe)
            if csat_groupe is not None:
                ligne["CSAT"] = formater_csat(csat_groupe)
            lignes_type_canal.append(ligne)

        st.write("Comment (par canal) :")
        lignes_type_canal_triees = sorted(lignes_type_canal, key=obtenir_tickets, reverse=True)
        st.dataframe(lignes_type_canal_triees, hide_index=True, width="stretch")

    st.divider()
    st.markdown(titre_section_principale("Couverture horaire"), unsafe_allow_html=True)
    st.caption(
        "Où la couverture est-elle sous tension par rapport au volume reçu, pendant les horaires "
        "ouverts ? 🟢 Confortable · 🟡 À surveiller · 🔴 Hotspot. Les créneaux fermés (horaire "
        "standard, pause, week-end) sont grisés — ce volume peut attendre la réouverture ; il est "
        "suivi à part, agrégé sur la période, dans la section \"Demande hors couverture\" plus haut."
    )

    html_heatmap = (
        "<style>"
        ".hm-grid { display: grid; grid-template-columns: 40px repeat(7, 1fr); gap: 3px; margin-bottom: 8px; }"
        ".hm-day-header, .hm-hour-label, .hm-corner { font-size: 10px; font-weight: 600; color: " + COULEUR_TEXTE_LABEL + "; "
        "display: flex; align-items: center; justify-content: center; padding: 2px; }"
        ".hm-cell { border-radius: 5px; padding: 3px 4px; text-align: center; line-height: 1.25; "
        "min-height: 40px; display: flex; flex-direction: column; justify-content: center; }"
        ".hm-cell-bande { min-height: 22px; }"
        ".hm-line-agents { font-weight: 600; font-size: 10px; color: " + COULEUR_TEXTE_VALEUR + "; }"
        ".hm-line-demandes { font-size: 9px; color: " + COULEUR_TEXTE_LABEL + "; }"
        ".hm-line-ratio { font-size: 10px; font-weight: 700; color: " + COULEUR_TEXTE_VALEUR + "; }"
        ".hm-muted { font-size: 9px; color: #B7AFA3; }"
        "</style>"
    )

    html_heatmap = html_heatmap + '<div class="hm-grid">' + '<div class="hm-corner"></div>'
    for nom_jour, numero_jour in JOURS_ORDRE:
        html_heatmap = html_heatmap + '<div class="hm-day-header">' + nom_jour[:3] + "</div>"

    grille_par_jour_heure = {}
    for entree in grille_creneaux:
        grille_par_jour_heure[(entree["jour"], entree["heure"])] = entree

    premiere_ouverture, derniere_fermeture = determiner_bornes_ouverture(horaires_standard)
    bandes_heatmap = construire_bandes_heatmap(premiere_ouverture, derniere_fermeture)

    for type_bande, heure_debut_bande, heure_fin_bande in bandes_heatmap:
        if type_bande == "HEURE":
            html_heatmap = html_heatmap + '<div class="hm-hour-label">' + str(heure_debut_bande) + "h</div>"
            for nom_jour, numero_jour in JOURS_ORDRE:
                entree = grille_par_jour_heure[(nom_jour, heure_debut_bande)]
                html_heatmap = html_heatmap + construire_cellule_heatmap(entree)
        else:
            if type_bande == "AVANT_OUVERTURE":
                label_bande = "<" + str(heure_fin_bande) + "h"
            else:
                label_bande = str(heure_debut_bande) + "h+"
            html_heatmap = html_heatmap + '<div class="hm-hour-label">' + label_bande + "</div>"
            for nom_jour, numero_jour in JOURS_ORDRE:
                demandes_bande = 0
                for heure_b in range(heure_debut_bande, heure_fin_bande):
                    demandes_bande = demandes_bande + grille_par_jour_heure[(nom_jour, heure_b)]["demandes"]
                html_heatmap = html_heatmap + construire_cellule_heatmap_bande(demandes_bande)

    html_heatmap = html_heatmap + "</div>"

    with st.container(border=True):
        st.markdown(html_heatmap, unsafe_allow_html=True)

    st.caption(
        "Survolez une cellule pour voir la liste complète des agents en poste sur ce créneau. Les "
        "heures avant l'ouverture et après la fermeture sont regroupées en un seul bloc — volume "
        "cumulé sur la plage, sans détail heure par heure (détail disponible dans la section "
        "\"Demande hors couverture\" plus haut)."
    )

    st.markdown("**Tensions de couverture**")
    if len(situations_tension_triees) > 0:
        for entree in situations_tension_triees[:5]:
            est_pic_semaine = creneau_le_plus_charge is not None and (
                entree["jour"] == creneau_le_plus_charge["jour"] and entree["heure"] == creneau_le_plus_charge["heure"]
            )
            st.markdown(construire_carte_situation(entree, est_pic_semaine), unsafe_allow_html=True)
        if comparaison_disponible and nb_tensions_s1 is not None:
            st.caption(
                str(len(situations_tension_triees)) + " tension(s) détectée(s), contre " + str(nb_tensions_s1)
                + " sur la période précédente."
            )
    else:
        if comparaison_disponible and nb_tensions_s1 is not None and nb_tensions_s1 > 0:
            st.caption(
                "Aucune tension de couverture significative sur cette période, contre " + str(nb_tensions_s1)
                + " sur la période précédente."
            )
        elif comparaison_disponible:
            st.caption(
                "Aucune tension de couverture significative sur cette période. Situation stable par "
                "rapport à la période précédente."
            )
        else:
            st.caption("Aucune tension de couverture significative sur cette période.")

    with st.expander("Voir le détail du planning"):
        lignes_planning = [
            construire_ligne_planning("Créneau standard (référence)", horaires_standard, "—")
        ]

        for agent in agents_grille:
            horaires = horaires_agent(planning_s2_dernier, agent)
            role = roles_periode.get(agent, "—")
            lignes_planning.append(construire_ligne_planning(agent, horaires, role))

        colonnes_jours_planning = []
        for nom_jour, numero_jour in JOURS_ORDRE:
            colonnes_jours_planning.append(nom_jour)

        tableau_planning = pd.DataFrame(lignes_planning)
        tableau_planning_stylise = tableau_planning.style.map(couleur_disponibilite_jour, subset=colonnes_jours_planning)

        st.dataframe(tableau_planning_stylise, hide_index=True, width="stretch")
        st.caption(
            "Tout est éditable dans l'onglet PLANNING du fichier Excel de l'export concerné (colonnes "
            "agent, jour, heure_debut, heure_fin, role) : les horaires et le rôle d'un agent, mais aussi "
            "le créneau standard lui-même (ligne \"DEFAUT\") — utile si un client passe à mi-temps, ferme "
            "un mois donné, ou ajoute des heures supplémentaires. Les arrivées/départs/absences se notent "
            "dans la colonne evenement_semaine de l'onglet RAW_TICKETS."
        )

    # ------------------------------------------------------------------
    # Conclusion
    # ------------------------------------------------------------------

    observations_conclusion = construire_conclusion_onglet(
        taux_sla_global, SLA_OBJECTIF_PCT, len(situations_tension_triees), pire_canal,
        part_hors_couverture, hors_couverture_significatif,
    )

    if len(observations_conclusion) > 0:
        st.divider()
        st.markdown(titre_section_principale("Conclusion"), unsafe_allow_html=True)
        for titre_observation, texte_observation in observations_conclusion:
            st.markdown(
                '<div style="margin-bottom:10px;"><span style="font-size:11px; font-weight:700; '
                'text-transform:uppercase; letter-spacing:0.04em; color:' + COULEUR_PRIMAIRE + ';">'
                + titre_observation + '</span><br><span style="font-size:14px; color:' + COULEUR_TEXTE_VALEUR + ';">'
                + texte_observation + "</span></div>",
                unsafe_allow_html=True,
            )


SEUIL_PART_COMPOSANT_DOMINANT = 35


def construire_insight_composant(lignes_composant_triees):
    if len(lignes_composant_triees) == 0:
        return None

    total = 0
    for ligne in lignes_composant_triees:
        total = total + ligne["Tickets"]
    if total == 0:
        return None

    plus_gros = lignes_composant_triees[0]
    part = plus_gros["Tickets"] / total * 100
    if part >= SEUIL_PART_COMPOSANT_DOMINANT:
        return (
            plus_gros["Composant"] + " concentre " + str(round(part)) + " % des tickets SAV produit "
            "de la période — la piste la plus probable pour un défaut structurel."
        )
    return None


def construire_insight_resolution(lignes_resolution_triees, total_sav):
    if len(lignes_resolution_triees) == 0 or total_sav == 0:
        return None

    plus_frequente = lignes_resolution_triees[0]
    part = plus_frequente["Tickets"] / total_sav * 100
    type_resolution = plus_frequente["Type de résolution"]

    if type_resolution == "Conseil à distance" and part >= 40:
        return (
            "« Conseil à distance » domine (" + str(round(part)) + " %) — plutôt un souci de "
            "compréhension d'usage qu'un vrai défaut matériel."
        )
    if "Remplacement" in str(type_resolution) and part >= 30:
        return (
            "« " + type_resolution + " » domine (" + str(round(part)) + " %) — signal de défaut "
            "matériel réel à corriger."
        )
    return None


def construire_insight_garantie(lignes_garantie, total_sav):
    if total_sav == 0:
        return None

    hors_garantie = 0
    for ligne in lignes_garantie:
        if ligne["Statut garantie"] != "Sous garantie":
            hors_garantie = hors_garantie + ligne["Tickets"]

    part = hors_garantie / total_sav * 100
    return (
        str(round(part)) + " % des SAV produit sont hors garantie — coût à la charge du client, sauf "
        "geste commercial (voir Impact & confiance)."
    )


# ------------------------------------------------------------------
# Onglet 6 : Produit
# ------------------------------------------------------------------

with onglet_produit:
    st.caption(
        "Cadence trimestrielle recommandée — élargis la Période A dans la barre latérale pour une vraie "
        "tendance produit. Les exports disponibles sont des semaines représentatives espacées dans le "
        "temps (pas un historique hebdomadaire continu) : élargir la période ajoute les exports compris "
        "dans la plage, sans combler les semaines entre deux exports."
    )

    tickets_sav_produit_s2 = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_sav_produit_s1 = categories_s1.get(CATEGORIE_SAV_PRODUIT, [])

    st.markdown(titre_section_principale("Composant en cause (SAV produit uniquement)"), unsafe_allow_html=True)

    par_composant_s2 = grouper_par(tickets_sav_produit_s2, "component")
    par_composant_s1 = grouper_par(tickets_sav_produit_s1, "component")

    schema_svg = construire_schema_composants(par_composant_s2, COULEUR_PRIMAIRE)
    if schema_svg is not None:
        st.caption(
            "Vue éclatée illustrative (produit générique, pas le vrai Emyria) — la taille et "
            "l'opacité des points suivent le nombre de tickets sur ce composant. Survole un point "
            "pour voir le détail."
        )
        st.markdown(schema_svg, unsafe_allow_html=True)

        if "Packaging / accessoire" in par_composant_s2:
            st.caption(
                str(len(par_composant_s2["Packaging / accessoire"]))
                + " tickets concernent le packaging/accessoires — hors schéma, pas un composant du produit lui-même."
            )

    lignes_composant = []

    if comparaison_disponible:
        composants_a_afficher = cles_combinees(par_composant_s2, par_composant_s1)
    else:
        composants_a_afficher = list(par_composant_s2.keys())

    for composant in composants_a_afficher:
        tickets_composant = par_composant_s2.get(composant, [])
        csat_composant = moyenne(tickets_composant, "csat")
        pct_composant = len(tickets_composant) / len(tickets_s2) * 100

        ligne = {
            "Composant": composant,
            "Tickets": len(tickets_composant),
            "% du volume global": formater_pourcentage(pct_composant),
            "CSAT": "N/A",
        }

        if csat_composant is not None:
            ligne["CSAT"] = formater_csat(csat_composant)

        if comparaison_disponible:
            tickets_composant_s1 = par_composant_s1.get(composant, [])
            volume_s1 = len(tickets_composant_s1)
            delta = len(tickets_composant) - volume_s1
            if delta >= 0:
                ligne["Évolution"] = "+" + str(delta)
            else:
                ligne["Évolution"] = str(delta)

            csat_composant_s1 = moyenne(tickets_composant_s1, "csat")
            if csat_composant is not None and csat_composant_s1 is not None:
                delta_csat = round(csat_composant - csat_composant_s1, 2)
                if delta_csat >= 0:
                    ligne["Évolution CSAT"] = "+" + str(delta_csat)
                else:
                    ligne["Évolution CSAT"] = str(delta_csat)

        lignes_composant.append(ligne)

    lignes_composant_triees = sorted(lignes_composant, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        afficher_tableau_colore(lignes_composant_triees)

    insight_composant = construire_insight_composant(lignes_composant_triees)
    if insight_composant is not None:
        st.caption(insight_composant)

    st.markdown(titre_section_principale("Par produit"), unsafe_allow_html=True)
    st.caption("Diffuseur (appareil) et Recharge sont distingués même pour un même parfum — un souci sur le matériel n'a pas la même gravité qu'un souci sur un consommable.")

    par_produit_s2 = {}
    for ticket in tickets_s2:
        cle_produit = (ticket["product_category"], ticket["product_name"])
        if cle_produit in par_produit_s2:
            par_produit_s2[cle_produit].append(ticket)
        else:
            par_produit_s2[cle_produit] = [ticket]

    par_produit_s1 = {}
    for ticket in tickets_s1:
        cle_produit = (ticket["product_category"], ticket["product_name"])
        if cle_produit in par_produit_s1:
            par_produit_s1[cle_produit].append(ticket)
        else:
            par_produit_s1[cle_produit] = [ticket]

    lignes_produit = []

    if comparaison_disponible:
        produits_a_afficher = cles_combinees(par_produit_s2, par_produit_s1)
    else:
        produits_a_afficher = list(par_produit_s2.keys())

    for produit in produits_a_afficher:
        tickets_produit = par_produit_s2.get(produit, [])
        csat_produit = moyenne(tickets_produit, "csat")
        pct_produit = len(tickets_produit) / len(tickets_s2) * 100

        ligne = {
            "Catégorie": produit[0],
            "Produit": produit[1],
            "Tickets": len(tickets_produit),
            "% du volume global": formater_pourcentage(pct_produit),
            "CSAT": "N/A",
        }

        if csat_produit is not None:
            ligne["CSAT"] = formater_csat(csat_produit)

        if comparaison_disponible:
            tickets_produit_s1 = par_produit_s1.get(produit, [])
            volume_s1 = len(tickets_produit_s1)
            delta = len(tickets_produit) - volume_s1
            if delta >= 0:
                ligne["Évolution"] = "+" + str(delta)
            else:
                ligne["Évolution"] = str(delta)

            csat_produit_s1 = moyenne(tickets_produit_s1, "csat")
            if csat_produit is not None and csat_produit_s1 is not None:
                delta_csat = round(csat_produit - csat_produit_s1, 2)
                if delta_csat >= 0:
                    ligne["Évolution CSAT"] = "+" + str(delta_csat)
                else:
                    ligne["Évolution CSAT"] = str(delta_csat)

        lignes_produit.append(ligne)

    lignes_produit_triees = sorted(lignes_produit, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        afficher_tableau_colore(lignes_produit_triees)

    st.markdown(titre_section_principale("Type de résolution des SAV produit"), unsafe_allow_html=True)

    par_resolution = grouper_par(tickets_sav_produit_s2, "resolution_type")
    lignes_resolution = []
    for resolution, tickets_resolution in par_resolution.items():
        lignes_resolution.append({"Type de résolution": resolution, "Tickets": len(tickets_resolution)})

    lignes_resolution_triees = sorted(lignes_resolution, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        st.dataframe(lignes_resolution_triees, hide_index=True, width="stretch")

    insight_resolution = construire_insight_resolution(lignes_resolution_triees, len(tickets_sav_produit_s2))
    if insight_resolution is not None:
        st.caption(insight_resolution)

    st.markdown(titre_section_principale("Nature du problème"), unsafe_allow_html=True)
    st.caption("component dit où le défaut se situe, issue_type dit ce qui est réellement cassé — les deux ensemble orientent vers le vrai correctif.")

    par_issue = grouper_par(tickets_sav_produit_s2, "issue_type")
    lignes_issue = []
    for issue, tickets_issue in par_issue.items():
        if issue is None:
            continue
        lignes_issue.append({"Nature du problème": issue, "Tickets": len(tickets_issue)})

    lignes_issue_triees = sorted(lignes_issue, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        st.dataframe(lignes_issue_triees, hide_index=True, width="stretch")

    par_composant_issue = {}
    for ticket in tickets_sav_produit_s2:
        composant = ticket["component"]
        issue = ticket["issue_type"]
        if composant is None or issue is None:
            continue
        cle = (composant, issue)
        if cle in par_composant_issue:
            par_composant_issue[cle] = par_composant_issue[cle] + 1
        else:
            par_composant_issue[cle] = 1

    lignes_composant_issue = []
    for cle, nombre in par_composant_issue.items():
        lignes_composant_issue.append({"Composant": cle[0], "Nature du problème": cle[1], "Tickets": nombre})

    lignes_composant_issue_triees = sorted(lignes_composant_issue, key=obtenir_tickets, reverse=True)

    lignes_composant_issue_significatives = []
    for ligne in lignes_composant_issue_triees:
        if ligne["Tickets"] >= SEUIL_MINIMUM_SUJET:
            lignes_composant_issue_significatives.append(ligne)

    st.markdown(titre_section_principale("Combinaisons composant × problème à investiguer"), unsafe_allow_html=True)
    st.caption(
        "Seules les combinaisons avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets sont montrées "
        "ici — le croisement complet reste disponible ci-dessous."
    )
    if len(lignes_composant_issue_significatives) > 0:
        st.dataframe(lignes_composant_issue_significatives, hide_index=True, width="stretch")
    else:
        st.caption("Aucune combinaison composant × problème assez récurrente sur cette période.")

    with st.expander("Voir le croisement complet composant × nature du problème"):
        st.dataframe(lignes_composant_issue_triees, hide_index=True, width="stretch")

    st.markdown(titre_section_principale("Garantie"), unsafe_allow_html=True)

    par_garantie = grouper_par(tickets_sav_produit_s2, "warranty_status")
    lignes_garantie = []
    for garantie, tickets_garantie in par_garantie.items():
        lignes_garantie.append({"Statut garantie": garantie, "Tickets": len(tickets_garantie)})

    with st.container(border=True):
        st.dataframe(lignes_garantie, hide_index=True, width="stretch")

    insight_garantie = construire_insight_garantie(lignes_garantie, len(tickets_sav_produit_s2))
    if insight_garantie is not None:
        st.caption(insight_garantie)

    with st.expander("Délai entre achat et signalement SAV"):
        st.caption("Un défaut précoce (moins de 30 jours après achat) évoque plutôt un défaut de fabrication ; un défaut tardif évoque plutôt de l'usure normale.")

        compte_anciennete = {}
        for ticket in tickets_sav_produit_s2:
            jours = delai_jours(ticket["order_date"], ticket["sav_reported_date"])
            if jours is None:
                continue
            niveau = niveau_anciennete_defaut(jours)
            if niveau in compte_anciennete:
                compte_anciennete[niveau] = compte_anciennete[niveau] + 1
            else:
                compte_anciennete[niveau] = 1

        lignes_anciennete = []
        for niveau, compte in compte_anciennete.items():
            lignes_anciennete.append({"Ancienneté du défaut": niveau, "Tickets": compte})

        st.dataframe(lignes_anciennete, hide_index=True, width="stretch")

    st.markdown(titre_section_principale("Clients avec SAV récurrents"), unsafe_allow_html=True)

    tickets_recurrents = []
    for ticket in tickets_sav_produit_s2:
        if ticket["prior_sav_count"] is not None and ticket["prior_sav_count"] >= 1:
            tickets_recurrents.append(ticket)

    if len(tickets_recurrents) == 0:
        st.caption("Aucun SAV récurrent sur cette période.")
    else:
        part_recurrents = len(tickets_recurrents) / len(tickets_sav_produit_s2) * 100

        par_produit_recurrent = grouper_par(tickets_recurrents, "product_name")
        lignes_produit_recurrent_triees = []
        for produit, tickets_produit_r in par_produit_recurrent.items():
            lignes_produit_recurrent_triees.append({"Produit": produit, "SAV récurrents": len(tickets_produit_r)})
        lignes_produit_recurrent_triees = sorted(lignes_produit_recurrent_triees, key=obtenir_sav_recurrents, reverse=True)

        par_composant_recurrent = grouper_par(tickets_recurrents, "component")
        lignes_composant_recurrent_triees = []
        for composant, tickets_composant_r in par_composant_recurrent.items():
            lignes_composant_recurrent_triees.append({"Composant": composant, "SAV récurrents": len(tickets_composant_r)})
        lignes_composant_recurrent_triees = sorted(lignes_composant_recurrent_triees, key=obtenir_sav_recurrents, reverse=True)

        produit_principal = lignes_produit_recurrent_triees[0]
        composant_principal = lignes_composant_recurrent_triees[0]

        st.write(
            str(len(tickets_recurrents)) + " tickets (" + str(round(part_recurrents)) + " % du SAV produit) "
            "concernent un client ayant déjà eu au moins un SAV avant celui-ci — signal de défaut structurel "
            "plutôt qu'un cas isolé. Concentré sur **" + produit_principal["Produit"] + "** ("
            + str(produit_principal["SAV récurrents"]) + " cas) et le composant **"
            + composant_principal["Composant"] + "** (" + str(composant_principal["SAV récurrents"]) + " cas)."
        )

        with st.expander("Détail par produit et composant"):
            colonne_rec_a, colonne_rec_b = st.columns(2)
            with colonne_rec_a:
                st.dataframe(lignes_produit_recurrent_triees, hide_index=True, width="stretch")
            with colonne_rec_b:
                st.dataframe(lignes_composant_recurrent_triees, hide_index=True, width="stretch")

    st.divider()
    st.markdown(titre_section_principale("Opportunités produit — demandes hors catalogue"), unsafe_allow_html=True)

    opportunites = detecter_opportunites_hors_catalogue(tickets_s2, SEUIL_MINIMUM_SUJET)

    if len(opportunites) == 0:
        st.caption(
            "Aucune demande hors catalogue récurrente (au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets) "
            "sur cette période."
        )
    else:
        st.caption(
            "Demandes récurrentes pour quelque chose qu'on ne vend pas (accessoire, personnalisation...), "
            "au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets — à remonter à l'équipe produit."
        )
        lignes_opportunites = []
        for sujet, tickets_sujet in opportunites:
            csat_opportunite = moyenne(tickets_sujet, "csat")
            ligne = {"Demande": sujet, "Tickets": len(tickets_sujet), "CSAT": "N/A"}
            if csat_opportunite is not None:
                ligne["CSAT"] = formater_csat(csat_opportunite)
            lignes_opportunites.append(ligne)

        lignes_opportunites_triees = sorted(lignes_opportunites, key=obtenir_tickets, reverse=True)[:10]
        with st.container(border=True):
            afficher_tableau_colore(lignes_opportunites_triees)


SEUIL_PART_SUJET_LIVRAISON_SIGNAL = 15
SEUIL_ECART_CSAT_LIVRAISON = 0.3
SEUIL_ECART_RESOLUTION_LIVRAISON_H = 4


# Un sujet ne mérite d'être mis en avant que s'il pèse assez dans le volume Livraison ET s'écarte
# vraiment de la moyenne de la catégorie (CSAT ou résolution) — pas juste parce qu'il existe.
def construire_signal_sujet_livraison(sujet, volume_s2, pct_sujet_livraison, csat_sujet, resolution_sujet, csat_moyen, resolution_moyenne):
    if pct_sujet_livraison < SEUIL_PART_SUJET_LIVRAISON_SIGNAL:
        return None

    ecart_csat = None
    if csat_sujet is not None and csat_moyen is not None:
        ecart_csat = csat_moyen - csat_sujet

    ecart_resolution = None
    if resolution_sujet is not None and resolution_moyenne is not None:
        ecart_resolution = resolution_sujet - resolution_moyenne

    csat_signal = ecart_csat is not None and ecart_csat >= SEUIL_ECART_CSAT_LIVRAISON
    resolution_signal = ecart_resolution is not None and ecart_resolution >= SEUIL_ECART_RESOLUTION_LIVRAISON_H
    if not csat_signal and not resolution_signal:
        return None

    morceaux = []
    if csat_signal:
        morceaux.append("CSAT " + formater_csat(csat_sujet) + " (moyenne Livraison " + formater_csat(csat_moyen) + ")")
    if resolution_signal:
        morceaux.append(
            "résolution " + formater_duree(resolution_sujet * 60) + " (moyenne Livraison "
            + formater_duree(resolution_moyenne * 60) + ")"
        )

    return {
        "sujet": sujet,
        "volume": volume_s2,
        "texte": (
            "« " + sujet + " » représente " + str(round(pct_sujet_livraison)) + " % du volume Livraison, "
            + " et ".join(morceaux) + " — nettement en retrait du reste de la catégorie."
        ),
    }


def obtenir_volume_signal(candidat):
    return candidat["volume"]


# ------------------------------------------------------------------
# Onglet 7 : Livraison
# ------------------------------------------------------------------

with onglet_livraison:
    st.caption(
        "Miroir mensuel de la catégorie Livraison, pensé pour un point avec le transporteur — voir "
        "l'onglet Vue d'ensemble pour la vue hebdomadaire toutes catégories confondues. Cadence mensuelle "
        "recommandée (élargis la Période A dans la barre latérale) — les exports disponibles restent des "
        "semaines représentatives isolées, pas un historique continu."
    )

    tickets_livraison_s2 = categories_s2.get("Livraison", [])
    tickets_livraison_s1 = categories_s1.get("Livraison", [])

    volume_livraison_s2 = len(tickets_livraison_s2)
    csat_livraison_s2 = moyenne(tickets_livraison_s2, "csat")
    resolution_livraison_s2 = moyenne(tickets_livraison_s2, "full_resolution_time_hours")
    pct_livraison_global = volume_livraison_s2 / len(tickets_s2) * 100

    with st.container(border=True):
        colonne_liv_a, colonne_liv_b, colonne_liv_c = st.columns(3)
        colonne_liv_a.markdown(
            construire_carte_kpi(
                "Tickets livraison", formater_nombre_espace(volume_livraison_s2),
                sous_texte=formater_pourcentage(pct_livraison_global) + " du volume global",
            ),
            unsafe_allow_html=True,
        )
        if csat_livraison_s2 is not None:
            colonne_liv_b.markdown(
                construire_carte_kpi("CSAT livraison", formater_csat(csat_livraison_s2)), unsafe_allow_html=True
            )
        if resolution_livraison_s2 is not None:
            colonne_liv_c.markdown(
                construire_carte_kpi("Résolution moyenne", formater_duree(resolution_livraison_s2 * 60)),
                unsafe_allow_html=True,
            )

    st.markdown(titre_section_principale("Sujets livraison"), unsafe_allow_html=True)

    sujets_livraison_s2 = grouper_par(tickets_livraison_s2, "subject_cluster")
    sujets_livraison_s1 = grouper_par(tickets_livraison_s1, "subject_cluster")

    if comparaison_disponible:
        sujets_livraison_a_afficher = cles_combinees(sujets_livraison_s2, sujets_livraison_s1)
    else:
        sujets_livraison_a_afficher = list(sujets_livraison_s2.keys())

    lignes_livraison = []
    signaux_sujets_livraison = []
    for sujet in sujets_livraison_a_afficher:
        tickets_sujet_s2 = sujets_livraison_s2.get(sujet, [])
        volume_s2 = len(tickets_sujet_s2)
        csat_sujet = moyenne(tickets_sujet_s2, "csat")
        resolution_sujet = moyenne(tickets_sujet_s2, "full_resolution_time_hours")
        pct_sujet_global = volume_s2 / len(tickets_s2) * 100
        pct_sujet_livraison = 0
        if volume_livraison_s2 > 0:
            pct_sujet_livraison = volume_s2 / volume_livraison_s2 * 100

        ligne = {
            "Sujet": sujet,
            "Tickets": volume_s2,
            "% du volume global": formater_pourcentage(pct_sujet_global),
            "CSAT": "N/A",
            "Résolution moyenne": "N/A",
        }

        if csat_sujet is not None:
            ligne["CSAT"] = formater_csat(csat_sujet)

        if resolution_sujet is not None:
            ligne["Résolution moyenne"] = formater_duree(resolution_sujet * 60)

        if comparaison_disponible:
            volume_s1 = len(sujets_livraison_s1.get(sujet, []))
            delta = volume_s2 - volume_s1
            if delta >= 0:
                ligne["Évolution"] = "+" + str(delta)
            else:
                ligne["Évolution"] = str(delta)

        lignes_livraison.append(ligne)

        signal = construire_signal_sujet_livraison(
            sujet, volume_s2, pct_sujet_livraison, csat_sujet, resolution_sujet,
            csat_livraison_s2, resolution_livraison_s2,
        )
        if signal is not None:
            signaux_sujets_livraison.append(signal)

    signaux_sujets_livraison_tries = sorted(signaux_sujets_livraison, key=obtenir_volume_signal, reverse=True)
    for signal in signaux_sujets_livraison_tries[:2]:
        st.caption(signal["texte"])

    lignes_livraison_triees = sorted(lignes_livraison, key=obtenir_tickets, reverse=True)
    with st.expander("Détail par sujet", expanded=(len(signaux_sujets_livraison_tries) == 0)):
        afficher_tableau_colore(lignes_livraison_triees)

    st.markdown(titre_section_principale("Par pays"), unsafe_allow_html=True)
    st.caption("Le transporteur est unique sur toute la zone de livraison — un écart marqué sur un pays isole un problème logistique local plutôt qu'un souci transporteur global.")

    par_pays_livraison = grouper_par(tickets_livraison_s2, "country")
    lignes_pays_livraison = []
    anomalies_pays = []
    for pays, tickets_pays in par_pays_livraison.items():
        csat_pays = moyenne(tickets_pays, "csat")
        resolution_pays = moyenne(tickets_pays, "full_resolution_time_hours")

        ligne = {
            "Pays": pays,
            "Tickets": len(tickets_pays),
            "CSAT": "N/A",
            "Résolution moyenne": "N/A",
        }
        if csat_pays is not None:
            ligne["CSAT"] = formater_csat(csat_pays)
        if resolution_pays is not None:
            ligne["Résolution moyenne"] = formater_duree(resolution_pays * 60)

        lignes_pays_livraison.append(ligne)

        if len(tickets_pays) >= SEUIL_MINIMUM_SUJET:
            ecart_csat_pays = None
            if csat_pays is not None and csat_livraison_s2 is not None:
                ecart_csat_pays = csat_livraison_s2 - csat_pays
            if ecart_csat_pays is not None and ecart_csat_pays >= SEUIL_ECART_CSAT_LIVRAISON:
                anomalies_pays.append(
                    pays + " : CSAT " + formater_csat(csat_pays) + " (moyenne Livraison "
                    + formater_csat(csat_livraison_s2) + ")"
                )

    if len(anomalies_pays) > 0:
        st.caption("Anomalie locale détectée : " + " · ".join(anomalies_pays))
    else:
        st.caption("Aucun pays ne s'écarte significativement de la moyenne Livraison sur cette période.")

    lignes_pays_livraison_triees = sorted(lignes_pays_livraison, key=obtenir_tickets, reverse=True)
    with st.expander("Détail par pays", expanded=(len(anomalies_pays) > 0)):
        afficher_tableau_colore(lignes_pays_livraison_triees)


SEUIL_ECART_CONVERSION_PCT = 15


# Écart d'un agent par rapport à la moyenne DE SON PAYS (pas un classement inter-agents) — un
# signal à comprendre (répartition des dossiers, typologie, formation), jamais un jugement de
# performance commerciale. Nécessite au moins 2 agents sur le pays pour qu'une moyenne ait un sens.
def construire_insight_agent_pays(lignes_agent_pays_triees):
    sommes_pays = {}
    comptes_pays = {}
    for ligne in lignes_agent_pays_triees:
        pays = ligne["pays"]
        sommes_pays[pays] = sommes_pays.get(pays, 0) + ligne["taux"]
        comptes_pays[pays] = comptes_pays.get(pays, 0) + 1

    moyennes_pays = {}
    for pays, somme in sommes_pays.items():
        moyennes_pays[pays] = somme / comptes_pays[pays]

    plus_gros_ecart_ligne = None
    plus_gros_ecart_valeur = 0
    for ligne in lignes_agent_pays_triees:
        if comptes_pays[ligne["pays"]] < 2:
            continue
        ecart = ligne["taux"] - moyennes_pays[ligne["pays"]]
        if abs(ecart) > abs(plus_gros_ecart_valeur):
            plus_gros_ecart_valeur = ecart
            plus_gros_ecart_ligne = ligne

    if plus_gros_ecart_ligne is None or abs(plus_gros_ecart_valeur) < SEUIL_ECART_CONVERSION_PCT:
        return None

    return (
        plus_gros_ecart_ligne["agent"] + " sur " + plus_gros_ecart_ligne["pays"] + " : taux de conversion "
        + str(round(plus_gros_ecart_ligne["taux"])) + " %, contre " + str(round(moyennes_pays[plus_gros_ecart_ligne["pays"]]))
        + " % en moyenne pour ce pays — écart à comprendre (répartition des dossiers, typologie de "
        "demandes, ou besoin de formation), pas un jugement de performance."
    )


# ------------------------------------------------------------------
# Onglet 8 : Avant-vente & conversion
# ------------------------------------------------------------------

with onglet_conversion:
    st.markdown(titre_section_principale("Conversion après contact avant-vente"), unsafe_allow_html=True)
    st.caption(
        "Fenêtre de " + str(FENETRE_CONVERSION_JOURS) + " jours glissants après le ticket. Rapproché par "
        "e-mail avec la commande la plus proche dans cette fenêtre (fichier Shopify fictif) — méthode "
        "réaliste, mais qui peut compter par coïncidence une commande sans lien réel avec le contact "
        "(client avec plusieurs tickets rapprochés dans le temps). À garder en tête en lisant les chiffres."
    )

    tickets_avant_vente = categories_s2.get("Avant-vente / conseil", [])
    index_commandes_email = commandes_par_email(commandes)

    resultats_conversion = []
    for ticket in tickets_avant_vente:
        commande = premiere_commande_apres(ticket, index_commandes_email, FENETRE_CONVERSION_JOURS)
        resultats_conversion.append((ticket, commande))

    nombre_convertis = 0
    delais = []
    for ticket, commande in resultats_conversion:
        if commande is not None:
            nombre_convertis = nombre_convertis + 1
            delais.append((commande["order_date"] - ticket["created_at"]).days)

    if len(tickets_avant_vente) > 0:
        taux_conversion = nombre_convertis / len(tickets_avant_vente) * 100

        with st.container(border=True):
            colonne_cv_a, colonne_cv_b = st.columns(2)
            colonne_cv_a.markdown(
                construire_carte_kpi(
                    "Taux de conversion (" + str(FENETRE_CONVERSION_JOURS) + "j)",
                    formater_pourcentage(taux_conversion),
                    sous_texte=formater_nombre_espace(len(tickets_avant_vente)) + " tickets avant-vente sur la période",
                ),
                unsafe_allow_html=True,
            )
            if len(delais) > 0:
                colonne_cv_b.markdown(
                    construire_carte_kpi(
                        "Délai moyen avant achat", str(round(sum(delais) / len(delais), 1)) + " j"
                    ),
                    unsafe_allow_html=True,
                )

    st.divider()
    st.markdown(titre_section_principale("Conversion par agent et par pays"), unsafe_allow_html=True)
    st.caption(
        "Pas un classement commercial : sert à repérer des écarts utiles pour la répartition des "
        "dossiers, la compréhension d'un marché ou un besoin de formation. Limité aux combinaisons "
        "agent/pays avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets avant-vente."
    )

    par_agent_pays = {}
    for ticket, commande in resultats_conversion:
        cle = (ticket["assignee"], ticket["country"])
        if cle not in par_agent_pays:
            par_agent_pays[cle] = {"total": 0, "convertis": 0, "montants": [], "quantites": []}
        par_agent_pays[cle]["total"] = par_agent_pays[cle]["total"] + 1
        if commande is not None:
            par_agent_pays[cle]["convertis"] = par_agent_pays[cle]["convertis"] + 1
            par_agent_pays[cle]["montants"].append(commande["montant_total"])
            par_agent_pays[cle]["quantites"].append(commande["quantite"])

    lignes_agent_pays = []
    for cle, stats in par_agent_pays.items():
        agent, pays = cle
        if stats["total"] < SEUIL_MINIMUM_SUJET:
            continue

        montant_moyen = None
        if len(stats["montants"]) > 0:
            montant_moyen = sum(stats["montants"]) / len(stats["montants"])

        quantite_moyenne = None
        if len(stats["quantites"]) > 0:
            quantite_moyenne = sum(stats["quantites"]) / len(stats["quantites"])

        lignes_agent_pays.append({
            "agent": agent,
            "pays": pays,
            "tickets": stats["total"],
            "convertis": stats["convertis"],
            "taux": stats["convertis"] / stats["total"] * 100,
            "montant_moyen": montant_moyen,
            "quantite_moyenne": quantite_moyenne,
        })

    def obtenir_tri_agent_pays(ligne):
        return ligne["tickets"]

    lignes_agent_pays_triees = sorted(lignes_agent_pays, key=obtenir_tri_agent_pays, reverse=True)

    insight_agent_pays = construire_insight_agent_pays(lignes_agent_pays_triees)
    if insight_agent_pays is not None:
        st.caption(insight_agent_pays)

    lignes_agent_pays_affichage = []
    for ligne in lignes_agent_pays_triees:
        montant_texte = "N/A"
        if ligne["montant_moyen"] is not None:
            montant_texte = formater_montant(ligne["montant_moyen"])

        quantite_texte = "N/A"
        if ligne["quantite_moyenne"] is not None:
            quantite_texte = str(round(ligne["quantite_moyenne"], 1))

        lignes_agent_pays_affichage.append({
            "Agent": ligne["agent"],
            "Pays": ligne["pays"],
            "Tickets avant-vente": ligne["tickets"],
            "Convertis": ligne["convertis"],
            "Taux de conversion": formater_pourcentage(ligne["taux"]),
            "Panier moyen": montant_texte,
            "Qté article moyenne": quantite_texte,
        })

    with st.container(border=True):
        st.dataframe(lignes_agent_pays_affichage, hide_index=True, width="stretch")


FENETRE_NPS_EXPERIENCE_JOURS = 60
SEUIL_RESOLUTION_RAPIDE_H = 24
SEUIL_MIN_REPONSES_NPS = 15


# Un ticket récurrent (le client a déjà eu au moins un SAV avant) pointe vers un défaut
# structurel qu'un correctif produit peut prévenir — "potentiellement évitable". Un incident
# isolé (accident de transport, mauvaise manipulation ponctuelle...) reste un "coût subi" : rien
# n'indique qu'une action corrective l'aurait empêché. Simplification assumée, pas une vérité
# absolue — documentée comme telle dans l'UI.
def est_cout_potentiellement_evitable(ticket):
    return ticket.get("prior_sav_count") is not None and ticket["prior_sav_count"] >= 1


# Rapproche une réponse NPS du dernier contact support plausible (fenêtre glissante avant la
# réponse) pour catégoriser par type d'expérience — approche associative, pas causale (aucun ID
# ticket n'est stocké dans les réponses NPS elles-mêmes, donc aucun lien démontré).
def obtenir_type_experience(reponse, index_tickets_email):
    ticket = dernier_ticket_avant(reponse, index_tickets_email, FENETRE_NPS_EXPERIENCE_JOURS)
    if ticket is None:
        return "Aucun contact"

    categorie = categoriser(ticket)
    if categorie == CATEGORIE_SAV_PRODUIT:
        if ticket["prior_sav_count"] is not None and ticket["prior_sav_count"] >= 1:
            return "SAV récurrent"
        return "SAV"
    if categorie == "Livraison":
        return "Problème livraison"

    resolution = ticket["resolution_type"]
    if resolution is not None and "Remplacement" in resolution:
        return "Remplacement"

    resolution_heures = ticket["full_resolution_time_hours"]
    if resolution_heures is not None:
        if resolution_heures < SEUIL_RESOLUTION_RAPIDE_H:
            return "Résolution rapide"
        return "Résolution longue"

    return "Autre contact"


# ------------------------------------------------------------------
# Onglet 9 : Impact & confiance
# ------------------------------------------------------------------

with onglet_impact:
    st.markdown(titre_section_principale("Coût direct estimé des incidents clients"), unsafe_allow_html=True)
    st.caption(
        "Remboursement = montant réellement remboursé. Remplacement et garantie = coût de revient "
        "produit + logistique associée (product_costs_fictif.xlsx), pas le prix de vente payé par le "
        "client. Geste commercial reste une fraction estimée du prix de vente : aucun montant "
        "réellement accordé n'est enregistré par ticket — seule ligne encore une estimation, "
        "marquée comme telle ci-dessous. Chaque commande n'est comptée qu'une seule fois même si "
        "plusieurs tickets s'y rattachent."
    )

    groupes_perte = {}
    for ticket in tickets_s2:
        type_perte = type_perte_financiere(ticket)
        if type_perte is None:
            continue
        if type_perte in groupes_perte:
            groupes_perte[type_perte].append(ticket)
        else:
            groupes_perte[type_perte] = [ticket]

    lignes_perte = []
    montant_total_pertes = 0
    montant_subi = 0
    montant_evitable = 0
    montants_par_composant = {}
    commandes_deja_comptees = set()

    for type_perte, tickets_perte in groupes_perte.items():
        pct_perte = len(tickets_perte) / len(tickets_s2) * 100

        montants = []
        for ticket in tickets_perte:
            order_id = ticket["order_id"]
            if order_id in commandes_deja_comptees:
                continue
            montant = montant_perte_estime(ticket, commandes, type_perte, couts_produits)
            if montant is None:
                continue

            montants.append(montant)
            commandes_deja_comptees.add(order_id)

            if est_cout_potentiellement_evitable(ticket):
                montant_evitable = montant_evitable + montant
            else:
                montant_subi = montant_subi + montant

            composant_ticket = ticket.get("component")
            if composant_ticket is not None:
                montants_par_composant[composant_ticket] = montants_par_composant.get(composant_ticket, 0) + montant

        methode = "Coût de revient réel"
        if type_perte == "Geste commercial":
            methode = "Estimé (fraction du prix de vente)"

        ligne = {
            "Type de perte": type_perte,
            "Tickets": len(tickets_perte),
            "% du volume global": formater_pourcentage(pct_perte),
            "Montant": "N/A",
            "Méthode": methode,
        }

        if len(montants) > 0:
            somme = sum(montants)
            ligne["Montant"] = formater_montant(somme)
            montant_total_pertes = montant_total_pertes + somme

        lignes_perte.append(ligne)

    lignes_perte_triees = sorted(lignes_perte, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        st.dataframe(lignes_perte_triees, hide_index=True, width="stretch")

    if montant_total_pertes > 0:
        colonne_cout_a, colonne_cout_b = st.columns(2)
        colonne_cout_a.markdown(
            construire_carte_kpi(
                "Coût direct estimé des incidents clients", formater_montant(montant_total_pertes)
            ),
            unsafe_allow_html=True,
        )
        colonne_cout_b.markdown(
            construire_carte_kpi(
                "Dont potentiellement évitable", formater_montant(montant_evitable),
                sous_texte=formater_pourcentage(montant_evitable / montant_total_pertes * 100) + " du coût — SAV récurrents",
            ),
            unsafe_allow_html=True,
        )

        if len(montants_par_composant) > 0:
            composant_principal = None
            montant_principal = 0
            for composant, montant in montants_par_composant.items():
                if montant > montant_principal:
                    montant_principal = montant
                    composant_principal = composant

            st.caption(
                "Principale cause du coût : " + composant_principal + " (" + formater_montant(montant_principal)
                + ", " + formater_pourcentage(montant_principal / montant_total_pertes * 100) + " du coût total)."
            )

    st.markdown(titre_section_principale("SAV sous garantie"), unsafe_allow_html=True)
    st.caption(
        "Impact économique du SAV pris en charge par l'entreprise — le détail produit/composant est "
        "dans l'onglet Produit, pas répété ici."
    )

    tickets_sav_produit_business = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_garantie = []
    for ticket in tickets_sav_produit_business:
        if ticket["warranty_status"] == "Sous garantie":
            tickets_garantie.append(ticket)

    if len(tickets_sav_produit_business) > 0 and len(tickets_garantie) > 0:
        pct_garantie_volume_sav = len(tickets_garantie) / len(tickets_sav_produit_business) * 100

        montants_garantie = []
        commandes_garantie_deja_comptees = set()
        for ticket in tickets_garantie:
            order_id = ticket["order_id"]
            if order_id in commandes_garantie_deja_comptees:
                continue
            montant = montant_cout_garantie(ticket, commandes, couts_produits)
            if montant is not None:
                montants_garantie.append(montant)
                commandes_garantie_deja_comptees.add(order_id)

        if len(montants_garantie) > 0:
            montant_garantie_total = sum(montants_garantie)

            colonne_gar_a, colonne_gar_b = st.columns(2)
            colonne_gar_a.markdown(
                construire_carte_kpi(
                    "Coût garantie estimé", formater_montant(montant_garantie_total),
                    sous_texte=str(len(tickets_garantie)) + " tickets sous garantie",
                ),
                unsafe_allow_html=True,
            )
            colonne_gar_b.markdown(
                construire_carte_kpi("Part du SAV produit concernée", formater_pourcentage(pct_garantie_volume_sav)),
                unsafe_allow_html=True,
            )

            # Comparaison en coût MOYEN par ticket, jamais en part d'un total combiné : une garantie
            # peut concerner un ticket déjà compté dans "Coût direct" (ex. Remplacement produit) —
            # additionner les deux totaux compterait ce ticket deux fois. Le coût moyen par ticket,
            # lui, reste valide même si les deux ensembles se recoupent partiellement.
            cout_moyen_garantie = None
            if len(tickets_garantie) > 0:
                cout_moyen_garantie = montant_garantie_total / len(tickets_garantie)

            cout_moyen_global = None
            if len(commandes_deja_comptees) > 0:
                cout_moyen_global = montant_total_pertes / len(commandes_deja_comptees)

            if cout_moyen_garantie is not None and cout_moyen_global is not None and cout_moyen_global > 0:
                ecart_cout_moyen_pct = (cout_moyen_garantie - cout_moyen_global) / cout_moyen_global * 100
                if ecart_cout_moyen_pct >= 50:
                    st.caption(
                        "Coût moyen par ticket sous garantie : " + formater_montant(cout_moyen_garantie)
                        + ", contre " + formater_montant(cout_moyen_global) + " en moyenne sur l'ensemble des "
                        "incidents chiffrés — un ticket garantie coûte structurellement plus cher (remplacement "
                        "complet à la charge de l'entreprise, pas de part payée par le client)."
                    )

            st.caption(
                "« Coût direct » et « Coût garantie » sont calculés indépendamment et peuvent se recouper "
                "partiellement (un remplacement sous garantie compte dans les deux) — ne pas additionner "
                "ces deux montants."
            )

    st.divider()
    st.markdown(titre_section_principale("Confiance mesurée (NPS)"), unsafe_allow_html=True)
    st.caption(
        "Fichier NPS FICTIF (nps_fictif.xlsx) — un score par client (0 à 10), pas filtré par période. "
        "NPS = % de promoteurs (9-10) moins % de détracteurs (0-6)."
    )

    reponses_nps = charger_nps(FICHIER_NPS)
    reponses_contactees = []
    reponses_non_contactees = []
    for reponse in reponses_nps:
        if reponse["a_contacte_support"] == "Oui":
            reponses_contactees.append(reponse)
        else:
            reponses_non_contactees.append(reponse)

    nps_global = calculer_nps(reponses_nps)
    nps_contactes = calculer_nps(reponses_contactees)
    nps_non_contactes = calculer_nps(reponses_non_contactees)

    with st.container(border=True):
        colonne_nps_a, colonne_nps_b, colonne_nps_c = st.columns(3)
        if nps_global is not None:
            colonne_nps_a.markdown(
                construire_carte_kpi(
                    "NPS global", round(nps_global, 1), sous_texte=str(len(reponses_nps)) + " répondants"
                ),
                unsafe_allow_html=True,
            )
        if nps_contactes is not None:
            colonne_nps_b.markdown(
                construire_carte_kpi(
                    "NPS - a contacté le support", round(nps_contactes, 1),
                    sous_texte=str(len(reponses_contactees)) + " répondants",
                ),
                unsafe_allow_html=True,
            )
        if nps_non_contactes is not None:
            colonne_nps_c.markdown(
                construire_carte_kpi(
                    "NPS - jamais contacté (référence)", round(nps_non_contactes, 1),
                    sous_texte=str(len(reponses_non_contactees)) + " répondants",
                ),
                unsafe_allow_html=True,
            )

    if nps_contactes is not None and nps_non_contactes is not None:
        ecart_nps = round(nps_contactes - nps_non_contactes, 1)
        if ecart_nps >= 0:
            texte_ecart = "supérieur de " + str(abs(ecart_nps))
        else:
            texte_ecart = "inférieur de " + str(abs(ecart_nps))
        st.write(
            "Les clients ayant contacté le support présentent un niveau de recommandation " + texte_ecart
            + " points par rapport à ceux n'ayant jamais contacté le support. Cet écart reflète "
            "l'expérience globale de ces clients et ne peut pas être attribué au support seul."
        )

    st.markdown("**Confiance par type d'expérience**")
    st.caption(
        "Rapproche chaque réponse du dernier ticket du même client dans les "
        + str(FENETRE_NPS_EXPERIENCE_JOURS) + " jours précédents — une association, pas un lien "
        "démontré (aucun ticket n'est référencé dans les réponses NPS elles-mêmes). Affiché "
        "seulement pour les groupes d'au moins " + str(SEUIL_MIN_REPONSES_NPS) + " répondants."
    )

    index_tickets_email = tickets_par_email(tickets_historique_business)
    reponses_par_experience = {}
    for reponse in reponses_nps:
        type_experience = obtenir_type_experience(reponse, index_tickets_email)
        if type_experience in reponses_par_experience:
            reponses_par_experience[type_experience].append(reponse)
        else:
            reponses_par_experience[type_experience] = [reponse]

    def obtenir_repondants(ligne):
        return ligne["Répondants"]

    lignes_experience = []
    for type_experience, reponses_experience in reponses_par_experience.items():
        if len(reponses_experience) < SEUIL_MIN_REPONSES_NPS:
            continue
        nps_experience = calculer_nps(reponses_experience)
        if nps_experience is None:
            continue
        lignes_experience.append({
            "Type d'expérience": type_experience,
            "NPS": round(nps_experience, 1),
            "Répondants": len(reponses_experience),
        })

    if len(lignes_experience) == 0:
        st.caption("Échantillon insuffisant par type d'expérience pour une comparaison robuste actuellement.")
    else:
        lignes_experience_triees = sorted(lignes_experience, key=obtenir_repondants, reverse=True)
        st.dataframe(lignes_experience_triees, hide_index=True, width="stretch")

    st.markdown("**Évolution du NPS dans le temps**")

    nps_par_mois = {}
    for reponse in reponses_nps:
        cle_mois = reponse["date_reponse"].strftime("%Y-%m")
        if cle_mois in nps_par_mois:
            nps_par_mois[cle_mois].append(reponse)
        else:
            nps_par_mois[cle_mois] = [reponse]

    lignes_nps_mois = []
    mois_echantillon_faible = []
    for cle_mois in sorted(nps_par_mois.keys()):
        nps_mois = calculer_nps(nps_par_mois[cle_mois])
        if nps_mois is None:
            continue
        nb_reponses_mois = len(nps_par_mois[cle_mois])
        lignes_nps_mois.append({"Mois": cle_mois, "NPS": nps_mois, "Réponses": nb_reponses_mois})
        if nb_reponses_mois < SEUIL_MIN_REPONSES_NPS:
            mois_echantillon_faible.append(cle_mois)

    tableau_nps_mois = pd.DataFrame(lignes_nps_mois)
    graphique_nps = alt.Chart(tableau_nps_mois).mark_line(point=True, color=COULEUR_SECONDAIRE).encode(
        x=alt.X("Mois:O", title=None),
        y=alt.Y("NPS:Q"),
        tooltip=["Mois:N", "NPS:Q", "Réponses:Q"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_nps, width="stretch")

    if len(mois_echantillon_faible) > 0:
        st.caption(
            "Échantillon faible (< " + str(SEUIL_MIN_REPONSES_NPS) + " répondants) sur : "
            + ", ".join(mois_echantillon_faible) + " — à lire avec prudence."
        )
