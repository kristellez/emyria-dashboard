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
    tickets_par_email,
    charger_nps,
    charger_suivi_suggestions,
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
    accorder,
    grouper_par,
    grouper_par_categorie,
    cles_combinees,
    evolution_pourcentage,
    categoriser,
    CATEGORIE_SAV_PRODUIT,
    couleur_texte_csat,
    niveau_macro,
    niveau_reponse_ouvree,
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
    moteur_produit_voie_a,
    moteur_produit_voie_b,
    charger_evenements_calendrier,
    construire_profil_observation,
    construire_lecture_tendances,
    MODE_OBSERVATION_UNIQUE,
    contexte_periode,
    moteur_livraison_voie_a,
    construire_lecture_activite_livraison,
    controler_qualite_donnees_livraison,
    texte_piste_transporteur_livraison,
    distribution_issues_livraison,
    TEXTE_COUT_INDISPONIBLE_LIVRAISON,
    construire_lecture_livraison,
    filtrer_tickets_par_segment_transporteur,
    SEGMENTS_LIVRAISON,
    SEGMENT_LIVRAISON_TOUS,
    construire_dossiers_associes_livraison,
    construire_croisement_motif_issue_livraison,
    FENETRE_CONVERSION_JOURS,
    resoudre_achats_observes_avant_vente,
    analyser_parcours_rdv,
    moteur_avant_vente_motifs,
    construire_lecture_activite_avant_vente,
    controler_qualite_donnees_avant_vente,
    distribution_canal_avant_vente,
    construire_lecture_avant_vente,
    construire_contacts_associes_avant_vente,
    construire_achats_associes_avant_vente,
    construire_table_sujets_avant_vente,
    construire_table_pays_avant_vente,
    SEUIL_CSAT_INSATISFAISANT,
    FENETRE_NPS_EXPERIENCE_JOURS,
    SEUIL_PRUDENCE_ECHANTILLON_NPS,
    TEXTE_PRUDENCE_BIAIS_SELECTION,
    formater_nps_entier,
    calculer_composition_nps,
    evaluer_prudence_echantillon_nps,
    texte_prudence_echantillon_nps,
    ETAT_PRUDENCE_VOLUME_FAIBLE,
    construire_historique_nps_par_mois,
    construire_profil_care_mensuel,
    evaluer_alignement_care_nps,
    texte_alignement_care_nps,
    segmenter_nps_par_contact_care,
    analyser_nps_par_type_experience,
    identifier_observation_nps_periode,
    texte_sensibilite_echantillon_nps,
    TEXTE_SENSIBILITE_PETIT_ECHANTILLON_NPS,
    TEXTE_CAVEAT_RECOUVREMENT_COUT,
    construire_lecture_impact_confiance,
    rang_relatif,
    extraire_candidats_categoriels_vue_ensemble,
    construire_signaux_attention_vue_ensemble,
    construire_signal_positif_vue_ensemble,
    construire_points_anticipation_vue_ensemble,
    construire_navigation_vue_ensemble,
    categorie_dominante_mix_tendances,
    construire_texte_periode_reference_tendances,
    charge_relative_agent,
    construire_historique_agent,
    construire_lecture_equipe_agents,
    construire_roster_agents,
    heures_planifiees_agent,
    mix_pct_agent,
    STATUT_AGENT_ABSENT,
    STATUT_AGENT_RENFORT_NON_PLANIFIE,
    evaluer_diagnostics_structures_transversal_vue_ensemble,
    CATEGORIE_LIVRAISON_VUE_ENSEMBLE,
    CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE,
    SEUIL_MAX_SIGNAUX_ATTENTION_VUE_ENSEMBLE,
    FENETRE_ANTICIPATION_VUE_ENSEMBLE_JOURS,
    SEUIL_REPLIES_FAQ_ACTIONS,
    SEUIL_CSAT_VERBATIM_ACTIONS,
    SEUIL_VERBATIMS_GROUPE_ACTIONS,
    TEXTE_PRUDENCE_AVANT_APRES_ACTIONS,
    identifier_pistes_standardisation,
    identifier_pistes_self_service,
    identifier_retours_clients_a_explorer,
    construire_actions_menees_actions,
    construire_agents_grille_couverture,
    construire_grille_pression_couverture,
    construire_reference_historique_couverture,
    enrichir_grille_pression_tension_couverture,
    construire_lecture_couverture,
    NIVEAU_PRESSION_HABITUELLE,
    NIVEAU_PRESSION_MARQUEE,
    NIVEAU_PRESSION_FORTE,
    NIVEAU_PRESSION_NON_QUALIFIABLE,
    NIVEAU_PRESSION_FAIBLE_VOLUME,
    NIVEAU_ACTIVITE_HORS_CAPACITE_FAIBLE,
    NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE,
    titre_signal_produit,
    titre_signal_produit_parties,
    construire_lecture_produit,
    construire_dossiers_associes_produit,
    cle_signal_produit,
    periodes_comparables_en_duree,
    formater_delta_nombre,
    formater_delta_points,
    formater_delta_duree,
    evaluer_evolution_signal_vs_b,
    texte_evolution_signal_vs_b,
    RANG_NIVEAU_PRIORITE,
    PLAFOND_SIGNAUX_COMPARAISON_B,
    construire_texte_resolution_produit,
    construire_texte_sav_recurrents_produit,
    TEXTE_PRUDENCE_CAUSALE,
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


# agents_en_poste, construire_activite_par_jour_heure, activite_observee et
# renfort_non_planifie vivent désormais dans outils.py (logique métier testable,
# indépendante de la couche d'affichage) — voir l'import en tête de fichier.
# statut_creneau_standard, construire_agents_grille, construire_grille_creneaux (Étape 5E.1 :
# devenue construire_grille_pression_couverture, corrigée pour le multi-semaines) vivent
# désormais dans outils.py également, section "Composition Couverture -- pression / tension".


# ------------------------------------------------------------------
# Design tokens (Étape 6C) -- source unique de la palette, de l'espacement et des rayons. La
# couleur représente un RÔLE (identité / surface / texte / attention / watch / positif / critique),
# jamais une source analytique ni un onglet : aucun token n'est ajouté "pour Produit" ou "pour
# Livraison" spécifiquement (Étape 6B, section 6-7). Toute nouvelle couleur doit venir de cette
# section -- pas de nouveau hex ajouté directement dans un onglet.
# ------------------------------------------------------------------

# --- Identité ---
COULEUR_PRIMAIRE = "#CC5500"        # Accent -- marque, période courante/A, liseré priorité
COULEUR_SECONDAIRE = "#96234A"      # 2e série de graphique UNIQUEMENT -- jamais une référence
                                     # temporelle B (Étape 6B, section 24 ; verrouillé section 15).
COULEUR_ACCENT_FONCE = "#8B4513"    # 3e série de graphique

# --- Surfaces ---
COULEUR_FOND_CARTE = "#FAFAF9"          # Surface 1
COULEUR_BORDURE_CARTE = "#E8E3DD"       # Border
COULEUR_FOND_BANDEAU = "#FBF3EC"        # Surface 2
COULEUR_BORDURE_BANDEAU = "#EAD9C4"

# --- Texte -- Text secondary et Text muted assombris (Étape 6C, section 3). Contraste mesuré par
# la formule de luminance relative WCAG (fond blanc/surface 1, texte 11-13px) :
#   Text secondary sur Surface 1 : #8A7F73 -> ~3,75:1 (sous le seuil AA texte normal 4,5:1)
#                                   #7A6F62 -> ~4,69:1 (conforme AA)
#   Text muted sur blanc         : #B7AFA3 -> ~2,17:1 (très insuffisant)
#                                   #857D70 -> ~4,07:1 (nettement amélioré, reste sous 4,5:1)
# Text muted reste volontairement réservé à un texte strictement secondaire/décoratif (jamais la
# seule porteuse d'une information nécessaire) -- si un jour elle porte une info fonctionnelle non
# dupliquée ailleurs, la remonter en Text secondary plutôt que de la laisser telle quelle.
COULEUR_TEXTE_VALEUR = "#2B2620"    # Text primary
COULEUR_TEXTE_LABEL = "#7A6F62"     # Text secondary (assombri depuis #8A7F73)
COULEUR_TEXTE_MUTED = "#857D70"     # Text muted (assombri depuis #B7AFA3)

# --- Rôles fonctionnels (couleur = rôle, jamais un jugement de performance -- Étape 6B, section 7)
COULEUR_ATTENTION = "#D9822E"       # Priorité à investiguer -- jamais rouge par défaut
COULEUR_WATCH = "#E0A72E"           # À surveiller / prudence -- ambre unique, réutilisé partout
COULEUR_POSITIVE = "#3FA76B"        # Tenue / absorption -- jamais "bon agent"
COULEUR_CRITIQUE = "#D1483B"        # Réservé aux cas réellement critiques (débordement, dossier
                                     # individuel sensible) -- jamais une priorité ordinaire

COULEUR_HAUSSE_FOND = "#DCF3E4"
COULEUR_HAUSSE_TEXTE = "#1E7A42"
COULEUR_BAISSE_FOND = "#FBDFDC"
COULEUR_BAISSE_TEXTE = "#B23A2E"
COULEUR_NEUTRE_FOND = "#EFECE8"
COULEUR_NEUTRE_TEXTE = "#6A6258"

# --- Espacement (Étape 6C, section 7) ---
ESPACE_XS = "4px"
ESPACE_S = "8px"
ESPACE_M = "16px"
ESPACE_L = "24px"
ESPACE_XL = "40px"

# --- Rayon (Étape 6C, section 8) ---
RADIUS_CARTE = "10px"
RADIUS_COMPACT = "8px"

# --- Catégories métier -- mapping fixe, jamais recyclé (Étape 6C, section 16). Utilisé partout où
# une composition par catégorie est affichée (Vue d'ensemble, Tendances) -- jamais laissé au hasard
# de la palette par défaut d'Altair (bug identifié en 6B, section 25).
# Étape 6J, section 33 : nommée (au lieu d'un hex local dans PLAGE_COULEURS_CATEGORIES) pour rester
# cohérente avec les 5 autres entrées du tableau, toutes déjà des tokens nommés.
COULEUR_CATEGORIE_SAV_USAGE = "#B7935F"

DOMAINE_CATEGORIES = [
    "Livraison", CATEGORIE_SAV_PRODUIT, "Avant-vente / conseil",
    "Après-vente commande/admin", "SAV usage (besoin d'aide)", "Autre",
]
PLAGE_COULEURS_CATEGORIES = [
    COULEUR_PRIMAIRE, COULEUR_SECONDAIRE, COULEUR_POSITIVE,
    COULEUR_ACCENT_FONCE, COULEUR_CATEGORIE_SAV_USAGE, COULEUR_TEXTE_LABEL,
]

# --- Couverture (accents de carte + heatmap) -- non modifiés ce tour, Étape 6G leur est dédiée
# (Étape 6C, section 34). Variantes plus saturées de couleur_niveau() (outils.py), pensées pour un
# liseré de carte plutôt qu'un fond de cellule de tableau — même langage de statut, contexte
# différent.
COULEUR_ACCENT_OK = "#3FA76B"
COULEUR_ACCENT_SURVEILLER = "#E0A72E"
# Distinct du rouge (tension pendant l'ouverture) : la question "hors couverture" est d'une
# autre nature — pas un débordement de l'équipe en poste, une question de capacité/horaires.
COULEUR_ACCENT_HORS_COUVERTURE = "#D9822E"
COULEUR_ACCENT_CRITIQUE = "#D1483B"
COULEUR_ACCENT_DEBORDEMENT = "#A6291E"

# Fonds de cellule pour la heatmap de couverture (onglet Couverture & réactivité). Étape 6G,
# section 11 : re-palette -- l'ancienne échelle vert/jaune/rose lisait comme un score de qualité
# (vert = bon, rose = mauvais), alors que la pression n'est PAS un jugement de performance (une
# forte pression bien absorbée reste neutre). Nouvelle échelle chromatique autour de la marque,
# monotone du neutre vers l'orange marqué -- jamais de vert (retirerait toute lecture "bonne
# note"), jamais de rouge (réservé à COULEUR_ACCENT_CRITIQUE, un vrai jugement, ailleurs dans
# l'app). COULEUR_HEATMAP_HORS_COUVERTURE (gris neutre, créneaux fermés) reste inchangée : ce
# n'est pas une valeur de pression, seulement "fermé par conception".
COULEUR_HEATMAP_CONFORTABLE = "#F5EFE6"
COULEUR_HEATMAP_SURVEILLER = "#EACB9C"
COULEUR_HEATMAP_HOTSPOT = "#CC8347"
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
        + "border-radius:" + RADIUS_CARTE + "; padding:" + ESPACE_M + " 18px 14px; margin-bottom:" + ESPACE_S + "; "
        'min-height:104px;">'
        '<div style="font-size:12px; text-transform:uppercase; letter-spacing:0.04em; color:' + COULEUR_TEXTE_LABEL + "; "
        'font-weight:600; line-height:1.3; margin-bottom:6px;">' + label + "</div>"
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
            '<div style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + '; line-height:1.4; margin-top:6px;">'
            + sous_texte + "</div>"
        )

    html = html + "</div>"
    return html


def construire_bandeau_info(texte_html):
    return (
        '<div style="background-color:' + COULEUR_FOND_BANDEAU + "; border:1px solid " + COULEUR_BORDURE_BANDEAU + "; "
        "border-radius:" + RADIUS_COMPACT + "; padding:14px " + ESPACE_M + "; color:" + COULEUR_TEXTE_VALEUR + '; '
        # max-width : contenu éditorial (texte de lecture), jamais appliqué à un tableau/heatmap/
        # graphique -- ceux-ci gardent la pleine largeur du layout "wide" (Étape 6C, section 6).
        'font-size:14px; line-height:1.5; max-width:1400px;">'
        + texte_html + "</div>"
    )


# Phase 2 (passe finale, section méthodologie) : note méthodologique partagée -- pour une
# précaution qui s'applique identiquement à plusieurs cartes/éléments d'une même section, affichée
# UNE fois au niveau section (juste sous le titre) plutôt que répétée sur chaque carte. Réduit le
# bruit visuel au niveau de lecture principal sans perdre l'information : detail_html optionnel
# reste disponible via un <details> natif replié, pour un complément plus long que la phrase
# courte n'a pas besoin de porter en permanence.
def construire_note_methodologique(texte, detail_html=None):
    html = (
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + "; line-height:1.5; margin:2px 0 "
        + ESPACE_S + ';">' + texte
    )
    if detail_html is not None:
        html = html + (
            '<details style="display:inline; margin-left:6px;">'
            '<summary style="display:inline; cursor:pointer; color:' + COULEUR_PRIMAIRE + ';">'
            "détail</summary>"
            '<div style="margin-top:4px;">' + detail_html + "</div>"
            "</details>"
        )
    html = html + "</div>"
    return html


# Style distinct pour LE titre principal de chaque onglet (un seul par onglet, celui qui
# introduit le sujet central) — les st.subheader() suivants restent la hiérarchie "normale"
# (déjà assagie par la règle CSS globale h2/h3), pour donner un vrai repère visuel de premier
# niveau sans devoir reclasser individuellement chaque sous-titre de l'app.
def titre_section_principale(texte):
    return (
        '<div style="border-left:4px solid ' + COULEUR_PRIMAIRE + "; padding-left:14px; margin:10px 0 6px;\">"
        '<span style="font-size:21px; font-weight:700; line-height:1.2; color:' + COULEUR_TEXTE_VALEUR + ';">'
        + texte + "</span>"
        "</div>"
    )


ROLES_STATUT_CARTE_SIGNAL = {
    "attention": COULEUR_ATTENTION,
    "watch": COULEUR_WATCH,
    "positive": COULEUR_POSITIVE,
    "critique": COULEUR_CRITIQUE,
}


# Fondation Étape 6C (section 20), câblée et validée en Étape 6D sur Vue d'ensemble (signaux
# "Ce qui mérite votre attention" et, en variante allégée sans titre, "Ce qui tient") : socle
# commun pour les 3-4 traitements visuels distincts jusque-là dispersés (Produit/Livraison/
# Avant-vente ont chacun leur propre mise en page de carte -- migration de leur contenu réel
# repoussée à 6E/6F, hors périmètre 6D). statut doit être une clé de ROLES_STATUT_CARTE_SIGNAL, ou
# None pour un signal neutre (bordure standard, pas d'accent de couleur). titre=None omet
# entièrement la ligne d'en-tête (et le badge) -- variante allégée pour un signal secondaire qui
# n'a pas de titre propre dans les données (Étape 6D, section 11 : partage radius/border/typo/
# espacements avec la carte "attention", mais une hiérarchie visuelle plus légère).
def construire_carte_signal(titre, statut, corps_html, badge=None, lien_croise=None):
    if statut is None:
        bordure_gauche = "border-left:1px solid " + COULEUR_BORDURE_CARTE + ";"
    else:
        bordure_gauche = "border-left:6px solid " + ROLES_STATUT_CARTE_SIGNAL[statut] + ";"

    html = (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        + bordure_gauche
        + "border-radius:" + RADIUS_CARTE + "; padding:" + ESPACE_M + "; margin-bottom:" + ESPACE_S + ';">'
    )

    if titre is not None:
        html = html + (
            '<div style="display:flex; justify-content:space-between; align-items:baseline; gap:' + ESPACE_S + ';">'
            '<span style="font-size:15px; font-weight:700; line-height:1.3; color:' + COULEUR_TEXTE_VALEUR + ';">'
            + titre + "</span>"
        )

        if badge is not None:
            html = html + (
                '<span style="font-size:12px; font-weight:600; color:' + COULEUR_TEXTE_MUTED + ';">' + badge + "</span>"
            )

        html = html + "</div>"

    if titre is not None:
        marge_haut_corps = ESPACE_XS
    else:
        marge_haut_corps = "0px"

    html = html + (
        '<div style="font-size:14px; line-height:1.5; color:' + COULEUR_TEXTE_VALEUR + "; margin-top:" + marge_haut_corps + ';">'
        + corps_html + "</div>"
    )

    # Phase 5 (passe finale, liens contextuels) : pointeur secondaire vers un autre onglet, distinct
    # du badge (réservé à la sévérité) et de corps_html (le contenu du signal) -- jamais une
    # nouvelle carte, juste une ligne de renvoi discrète en pied de carte. None par défaut : la
    # grande majorité des cartes n'en ont pas besoin.
    if lien_croise is not None:
        html = html + (
            '<div style="font-size:12px; font-weight:600; color:' + COULEUR_PRIMAIRE + "; margin-top:" + ESPACE_XS + ';">'
            + lien_croise + "</div>"
        )

    html = html + "</div>"
    return html


# Fondation Étape 6C (section 9, posée mais non appliquée), câblée pour la première fois en
# Étape 6E sur les graphiques Tendances/Agents : apparence commune (fond transparent, gridlines
# discrètes, police et couleurs alignées sur les tokens texte) plutôt qu'un thème Altair par
# défaut différent d'un graphique à l'autre. Ne change ni le type de graphique, ni les données,
# ni l'échelle -- appelé sur un chart déjà encodé (après .encode()/.properties()), remplace le
# .configure_view(strokeWidth=0) répété partout par un unique point de configuration partagé.
def configurer_apparence_graphique(graphique):
    return (
        graphique
        .properties(background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(
            gridColor=COULEUR_BORDURE_CARTE, gridOpacity=0.6,
            domainColor=COULEUR_BORDURE_CARTE, tickColor=COULEUR_BORDURE_CARTE,
            labelColor=COULEUR_TEXTE_LABEL, titleColor=COULEUR_TEXTE_LABEL,
            labelFont="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            titleFont="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            labelFontSize=11, titleFontSize=12,
        )
        .configure_legend(
            labelColor=COULEUR_TEXTE_LABEL,
            labelFont="Inter, -apple-system, BlinkMacSystemFont, sans-serif", labelFontSize=11,
        )
    )


# Étape 5E.1 : la couleur de cellule encode désormais une PRESSION DE CHARGE relative à
# l'historique disponible, jamais une qualité de service jugée dans l'absolu -- voir
# construire_cellule_pression_couverture plus bas. "Parmi les plus fortes observées" reste un
# ton chaud (jamais le rouge "critique" réservé ailleurs à un vrai jugement de performance) --
# valeur mise à jour en Étape 6G (section 11) avec le reste de l'échelle, voir COULEUR_HEATMAP_*.
COULEUR_HEATMAP_PRESSION_FORTE = "#DFA463"

# Étape 6G, section 34 : dette identifiée en 6A -- ces clés recopiaient les libellés de niveau en
# dur au lieu de référencer les constantes moteur (outils.py). Corrigé ici (comparaison sur les
# constantes partagées, jamais leur chaîne recopiée) ; aucune valeur de couleur ni logique changée.
COULEUR_FOND_HEATMAP_PRESSION = {
    NIVEAU_PRESSION_HABITUELLE: COULEUR_HEATMAP_CONFORTABLE,
    NIVEAU_PRESSION_MARQUEE: COULEUR_HEATMAP_SURVEILLER,
    NIVEAU_PRESSION_FORTE: COULEUR_HEATMAP_PRESSION_FORTE,
    NIVEAU_PRESSION_FAIBLE_VOLUME: COULEUR_HEATMAP_HORS_COUVERTURE,
    NIVEAU_PRESSION_NON_QUALIFIABLE: COULEUR_HEATMAP_HORS_COUVERTURE,
    NIVEAU_ACTIVITE_HORS_CAPACITE_FAIBLE: COULEUR_HEATMAP_HORS_COUVERTURE,
    NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE: COULEUR_HEATMAP_HOTSPOT,
    None: COULEUR_HEATMAP_HORS_COUVERTURE,
}


# Au-delà de 3 prénoms, la cellule tronque ("+N") pour rester compacte — la liste
# complète reste disponible via l'attribut title (tooltip au survol).
def construire_texte_agents_cellule(agents):
    if len(agents) == 0:
        return ""
    if len(agents) <= 3:
        return " · ".join(agents)
    return " · ".join(agents[:3]) + " +" + str(len(agents) - 3)


# Remplace construire_cellule_heatmap (Étape 5E.1) : le contenu et la couleur reflètent la
# PRESSION relative, jamais une conclusion de tension (celle-ci vit dans le bloc "Créneaux à
# examiner", pas dans la heatmap elle-même). Un badge "⚠ Tension" discret signale les cellules
# où pression ET réactivité locale convergent, sans changer la couleur de fond (qui reste celle
# de la pression seule).
def construire_cellule_pression_couverture(entree):
    titre_tooltip = ""
    if len(entree["agents"]) > 0:
        titre_tooltip = ", ".join(entree["agents"])

    if entree["statut"] != "Couverture requise":
        # Fermé par conception (horaire standard, pause, week-end) : le volume peut
        # attendre la réouverture, pas de couleur de pression ni de mention d'effectif.
        if entree["demandes"] > 0:
            contenu = '<div class="hm-muted">' + str(entree["demandes"]) + " demandes</div>"
        else:
            contenu = '<div class="hm-muted">—</div>'
        return (
            '<div class="hm-cell" style="background-color:' + COULEUR_HEATMAP_HORS_COUVERTURE + ';" '
            'title="' + titre_tooltip + '">' + contenu + "</div>"
        )

    couleur_fond = COULEUR_FOND_HEATMAP_PRESSION.get(entree["niveau_pression"], COULEUR_HEATMAP_HORS_COUVERTURE)

    if entree["capacite_cumulee"] > 0:
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
        if entree["est_tension"]:
            contenu = contenu + '<div class="hm-line-tension">⚠ Tension</div>'
    elif len(entree["renfort_non_planifie"]) > 0:
        # Personne planifié, mais une activité réelle a été observée sur ce créneau précis —
        # distinct d'une vraie absence de couverture : ne pas mélanger à la pression (capacité
        # cumulée reste 0), seulement l'afficher.
        texte_renfort = construire_texte_agents_cellule(entree["renfort_non_planifie"])
        contenu = (
            '<div class="hm-line-agents">Aucun agent planifié — renfort non planifié : ' + texte_renfort + "</div>"
            '<div class="hm-line-demandes">' + str(entree["demandes"]) + " demandes</div>"
        )
    else:
        # Créneau censé être couvert mais personne en poste — jamais une "pression infinie" :
        # aucun ratio, un simple constat factuel (Étape 5E.1, section 10).
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
# Synthèse légère, séparée de la heatmap (qui reste lisible cellule par cellule) : agrège tous
# les créneaux où une activité a été observée sans capacité prévue correspondante, quel que soit
# le nombre d'agents déjà planifiés sur ces créneaux — la détection (renfort_non_planifie, dans
# la grille) fonctionne partout, seul l'affichage choisit de rester synthétique.
def construire_synthese_renfort(grille_creneaux):
    par_agent = {}
    for entree in grille_creneaux:
        for agent in entree["renfort_non_planifie"]:
            if agent not in par_agent:
                par_agent[agent] = {"heures": 0, "demandes": 0}
            par_agent[agent]["heures"] = par_agent[agent]["heures"] + 1
            par_agent[agent]["demandes"] = par_agent[agent]["demandes"] + entree["demandes"]
    return par_agent


# Remplace construire_carte_situation (Étape 5E.1) : une "Tension à examiner" est toujours la
# convergence pression + réactivité locale dégradée (jamais la pression seule) -- bordure ambre
# (COULEUR_ACCENT_SURVEILLER), jamais le rouge critique. Catégorie/canal restent des éléments qui
# EXPLIQUENT la tension, jamais des critères qui la déclenchent (sections 17-18).
def construire_carte_tension_couverture(entree):
    titre = entree["jour"] + " · " + str(entree["heure"]) + "h-" + str(entree["heure"] + 1) + "h"

    texte_agents = construire_texte_agents_cellule(entree["agents"])
    if texte_agents == "":
        texte_agents = "Aucun agent en poste"

    ligne_pression = (
        str(entree["demandes"]) + " demandes · " + str(round(entree["ratio"], 1)) + " / agent — "
        + entree["niveau_pression"]
    )
    ligne_frt = (
        "1re réponse locale (médiane) : " + formater_duree(entree["frt_local_median"]) + " — "
        + entree["niveau_frt_local"]
    )

    ligne_categorie = ""
    if entree.get("categorie_dominante") is not None:
        ligne_categorie = (
            '<div style="font-size:11px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;">'
            "Dont " + str(round(entree["part_categorie_dominante"])) + " % " + entree["categorie_dominante"] + "</div>"
        )

    ligne_canal = ""
    if entree.get("canal_dominant") == "Téléphone" and entree.get("part_canal_dominant", 0) >= SEUIL_PART_TELEPHONE_SIGNAL:
        ligne_canal = (
            '<div style="font-size:11px; color:' + COULEUR_ACCENT_HORS_COUVERTURE + '; margin-top:2px;">'
            "Dont " + str(round(entree["part_canal_dominant"])) + " % téléphone — implique une attente "
            "synchrone.</div>"
        )

    return (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        "border-left:6px solid " + COULEUR_ACCENT_SURVEILLER + "; border-radius:" + RADIUS_CARTE
        + "; padding:12px " + ESPACE_M + "; margin-bottom:" + ESPACE_S + ';">'
        '<div style="font-size:13px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">' + titre + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:2px;">' + texte_agents + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + ligne_pression + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + ';">' + ligne_frt + "</div>"
        + ligne_categorie + ligne_canal
        + "</div>"
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

# construire_agents_grille, construire_grille_creneaux (Étape 5E.1 : construire_grille_pression_
# couverture, corrigée multi-semaines) vivent désormais dans outils.py. detecter_pic_exceptionnel
# est retiré (Étape 5E.1) : il recalculait un second pic "exceptionnel" à partir du même ratio
# brut que l'ancien hotspot -- la nouvelle taxonomie pression/tension (rang relatif à l'historique,
# déjà par-créneau) couvre ce besoin sans un second mécanisme parallèle.

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


# construire_carte_sla / construire_barre_progression_sla (grande carte SLA dédiée, avec barre de
# progression) supprimées Étape 5E.1 : le SLA reste premier niveau (carte KPI compacte, section B)
# mais ne justifie plus une section indépendante à côté du FRT -- les deux racontent la même
# dimension de réactivité (audit 5E.1, section 16).
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
# construire_conclusion_onglet supprimée Étape 5E.1 : son rôle de synthèse est repris par
# construire_lecture_couverture (outils.py), affichée en tête d'onglet (bloc A) plutôt qu'en pied
# de page -- une seule synthèse data-driven, pas deux mécanismes parallèles.


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
    "Actions & améliorations": [ROLE_TEAM_LEAD, ROLE_HEAD_CX, ROLE_ADMIN],
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
FICHIER_CALENDRIER_EVENEMENTS = os.path.join(DOSSIER_PROJET, "data_calendrier", "calendrier_evenements.xlsx")
DOSSIER_MACROS = os.path.join(DOSSIER_PROJET, "knowledge_base", "macros")
DOSSIER_FAQ = os.path.join(DOSSIER_PROJET, "knowledge_base", "faq")
# FENETRE_CONVERSION_JOURS vit désormais dans outils.py (source unique, Étape 4D) -- importée ci-dessus.
# SEUIL_CSAT_INSATISFAISANT vit désormais dans outils.py (source unique, Étape 4E) -- importée ci-dessus.

SEUIL_MINIMUM_SUJET = 5

# Étape 5A -- construire_lignes_sujets / obtenir_sujets_notables / construire_insights_vue_ensemble
# (ex-moteur d'alerte local à la Vue d'ensemble, recalculant des deltas bruts indépendamment des
# moteurs 4A-4E validés) supprimées : la Vue d'ensemble consomme désormais directement les sorties
# des moteurs Produit/Livraison/Avant-vente/Tendances/Impact & confiance (voir onglet_vue plus bas
# et les fonctions de composition dans outils.py, section "Composition Vue d'ensemble").
# Étape 5D.1 -- obtenir_score_insight, construire_candidats_categorie et le score inter-familles
# hétérogène qui les utilisait sont supprimés (voir compte-rendu Étape 5D, section 4 : le score
# mélangeait des unités incomparables entre familles). SEUIL_MACRO_BASSE/HAUTE, SEUIL_REPLIES_FAQ,
# SEUIL_CSAT_VERBATIM, SEUIL_VERBATIMS_GROUPE ont déménagé dans outils.py (section "Composition
# Actions & améliorations, Étape 5D.1") avec les fonctions qui les utilisent.

st.set_page_config(page_title="Dashboard Customer Care : Emyria", layout="wide")

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');"
    "html, body, [class*='css'] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }"
    "h1 { letter-spacing: -0.02em; }"
    # Étape 6J, section 33 : référence le token Text primary au lieu d'un hex local proche mais
    # distinct (#3A342C) -- même teinte partout, plus de doublon de "texte principal".
    "h2, h3 { letter-spacing: -0.01em; font-weight: 600; color: " + COULEUR_TEXTE_VALEUR + "; }"
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
    str(len(semaines_disponibles)) + " semaines représentatives disponibles (pas un historique continu)."
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

# Spinner local (Étape 6C, section 32) : le chargement (lecture fichiers + mise en cache, voir
# functools.lru_cache sur charger_tickets/charger_planning depuis l'Étape 6A) reste sensible sur un
# premier chargement à froid ou un changement de période -- un repère visuel discret suffit, pas de
# restructuration de l'ordre de chargement.
with st.spinner("Chargement des données de la période..."):
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
evenements_calendrier = charger_evenements_calendrier(FICHIER_CALENDRIER_EVENEMENTS)

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

# Contexte en dernier onglet (Étape 6C, section 12-13) : l'app s'ouvre sur le pilotage, pas sur
# la documentation -- Contexte reste disponible mais n'est plus le premier réflexe. Libellés de la
# barre raccourcis pour résoudre le débordement identifié en 6B (section 20) ; le nom complet
# ("Actions & améliorations", "Couverture & réactivité", "Avant-vente & parcours d'achat", "Impact
# & confiance") reste utilisé dans le texte de contenu (ex. Contexte, "Comment lire les onglets").
(
    onglet_vue, onglet_tendances, onglet_agents, onglet_alertes, onglet_creneaux,
    onglet_produit, onglet_livraison, onglet_conversion, onglet_impact, onglet_contexte,
) = st.tabs(
    [
        "Vue d'ensemble", "Tendances", "Agents", "Actions", "Couverture",
        "Produit", "Livraison", "Avant-vente", "Impact", "Contexte",
    ]
)


# ------------------------------------------------------------------
# Onglet 0 : Contexte
# ------------------------------------------------------------------

with onglet_contexte:
    # Étape 6I, section 4 : patron page title validé -- remplace l'ancien hero (bloc plein orange +
    # h1 "Emyria") qui était le seul vestige pré-6C de l'app. L'identité produit ("Emyria, diffuseur
    # d'ambiance connecté...") n'est pas supprimée : elle est reprise mot pour mot dans le panneau
    # "Ce que vous regardez" ci-dessous, avec le disclaimer données fictives déjà existant (section 6-7
    # : un seul panneau éditorial, jamais plusieurs grandes cartes pour expliquer le produit).
    st.subheader("Contexte")
    st.caption("Comprendre le périmètre, les données et les règles de lecture du dashboard.")

    colonne_ctx_texte, colonne_ctx_image = st.columns([2, 1])

    with colonne_ctx_texte:
        st.markdown(titre_section_principale("Ce que vous regardez"), unsafe_allow_html=True)
        st.markdown(
            construire_bandeau_info(
                "Emyria (fictif) — diffuseur d'ambiance connecté, lumière LED &amp; capsules de parfum "
                "interchangeables. Ce tableau de bord est une démonstration construite sur des données "
                "100 % fictives (tickets, commandes, avis) — pas l'audit d'une entreprise réelle. Il "
                "illustre un outil de pilotage du service client conçu pour ce type de scale-up e-commerce."
            ),
            unsafe_allow_html=True,
        )

    with colonne_ctx_image:
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
            "- Relier l'activité Care aux enjeux produit, logistiques, commerciaux et financiers : "
            "signaux SAV produit, motifs logistiques, parcours avant-vente, coûts et confiance "
            "client (NPS)"
        )

    # ------------------------------------------------------------------
    # Étape 6I, section 8-10 : nouvelle section -- cette distinction Période A / période de
    # comparaison / historique n'était auparavant condensée qu'en une phrase dans "Comment lire les
    # onglets" (ci-dessous). Contenu directement dérivé de la mécanique déjà en place dans la barre
    # latérale (Étape 6A/6C, jamais "dernière période"/"période précédente" -- toujours "période de
    # comparaison"), aucune règle de calcul nouvelle.
    # ------------------------------------------------------------------

    # Étape 7A -- grammaire temporelle réécrite pour documenter le rôle de B une fois la comparaison
    # A/B étendue à l'ensemble du dashboard (B enrichit A, ne crée jamais une deuxième lecture
    # parallèle) ; contenu toujours dérivé de la mécanique déjà en place dans la barre latérale,
    # aucune règle de calcul nouvelle ici.
    st.markdown(titre_section_principale("Période & comparaison"), unsafe_allow_html=True)
    st.markdown(
        "- **Période A** : la période analysée. Elle constitue toujours la lecture principale du "
        "dashboard.\n"
        "- **Période B** (optionnelle) : une période de référence utilisée pour comprendre ce qui a "
        "changé par rapport à A. Lorsqu'elle est activée, elle enrichit les indicateurs de A par des "
        "écarts, évolutions ou changements significatifs. Elle ne crée pas une seconde lecture "
        "parallèle du dashboard.\n"
        "- **Historique** : les observations disponibles antérieures à A, utilisées lorsque "
        "nécessaire pour déterminer si un niveau ou une évolution est habituel, récent ou "
        "exceptionnel. L'historique est distinct de la comparaison explicite entre A et B."
    )
    st.markdown(
        construire_bandeau_info(
            "<strong>Principe de lecture :</strong> A montre la situation à piloter. B aide à "
            "comprendre son évolution. L'historique aide à la replacer dans le temps."
        ),
        unsafe_allow_html=True,
    )

    st.markdown(titre_section_principale("Sources de données"), unsafe_allow_html=True)
    lignes_sources_contexte = [
        {"Source": "Tickets support", "Ce qu'elle apporte": "Canal, catégorie, agent, délais, CSAT"},
        {"Source": "Planning des agents", "Ce qu'elle apporte": "Horaires, rôles, présence par créneau"},
        {
            "Source": "Calendrier commercial / événements",
            "Ce qu'elle apporte": "Campagnes, lancements, absences prévues -- contexte de la période",
        },
        {"Source": "Commandes", "Ce qu'elle apporte": "Produit, montant, pays, date (fichier Shopify)"},
        {
            "Source": "Coûts produit",
            "Ce qu'elle apporte": "Coût de revient et coûts logistiques associés, utilisés pour le coût "
            "direct et le coût garantie (onglet Impact)",
        },
        {
            "Source": "Réponses NPS",
            "Ce qu'elle apporte": "Score de recommandation, date et client, exploités selon les analyses "
            "à l'échelle de la période sélectionnée ou de l'historique disponible",
        },
        {"Source": "Suivi des suggestions", "Ce qu'elle apporte": "Macros/FAQ créées et leur effet mesuré"},
    ]
    st.dataframe(lignes_sources_contexte, hide_index=True, width="stretch")
    st.caption("CSAT noté sur une échelle de 0 à 5.")
    st.caption(
        "Toutes les données présentées sont fictives et ont été conçues exclusivement pour cette "
        "démonstration. Elles reproduisent des situations plausibles de pilotage Customer Care et "
        "n'ont aucune valeur réelle."
    )

    with st.expander("Limites connues de cette démo"):
        st.markdown(
            "- **Coût des incidents clients** : remboursement et remplacement/garantie utilisent un vrai "
            "coût de revient produit ; seul le geste commercial reste une fraction estimée du prix de "
            "vente, faute d'un montant réellement accordé enregistré par ticket — voir l'onglet Impact "
            "pour le détail par ligne.\n"
            "- **Exports disponibles** : semaines représentatives espacées dans le temps, pas un "
            "historique continu — voir l'onglet Tendances pour le détail des écarts.\n"
            "- **Volume support en période de pic** : les semaines Black Friday/Noël dépassent le "
            "rythme soutenable d'un fonctionnement normal — volontaire, pensé comme un mode « surge » "
            "temporaire plutôt qu'un défaut de modélisation.\n"
            "- **Suivi des actions** (onglet Actions) : inclut volontairement un cas "
            "(MAC-018) où la macro créée a bien été adoptée par l'équipe mais n'a pas amélioré le CSAT — "
            "un vrai outil de pilotage doit pouvoir montrer un échec, pas seulement des réussites."
        )


# ------------------------------------------------------------------
# Onglet 1 : Vue d'ensemble
# ------------------------------------------------------------------

with onglet_vue:
    # Titre de page (Étape 6D, section 4) : reprend la règle CSS globale h2/h3 (Étape 6C) plutôt
    # qu'un nouveau bloc HTML -- pas de hero, la période reste affichée dans le bandeau global
    # au-dessus des onglets, jamais dupliquée ici en plus grand.
    st.subheader("Vue d'ensemble")
    st.caption("Ce qui s'est passé sur la période, ce qui mérite attention, ce qui tient.")

    nombre_s2 = len(tickets_s2)
    csat_s2 = moyenne(tickets_s2, "csat")
    frt_s2 = moyenne(tickets_s2, "first_reply_time_min")
    macro_s2 = taux_rempli(tickets_s2, "macro_applied")
    # Étape 5A.1 -- audit KPI (macro vs résolution, 5 périodes réelles Dec/Jan/Mai/Jul/Sep) :
    # l'utilisation macro reste dans une bande étroite (22-38 %), toujours loin de l'objectif de
    # 70 % quelle que soit la difficulté réelle de la période -- peu discriminante. La résolution
    # moyenne, elle, varie de 36h à 62h et signale précisément janvier (la période la plus dure
    # des 5 testées) -- bien plus informative en KPI principal. Macro reste visible dans le détail
    # "Performance par catégorie" (accordéon), simplement retirée des 4 indicateurs essentiels.
    resolution_s2 = moyenne(tickets_s2, "full_resolution_time_hours")

    nombre_s1 = len(tickets_s1)
    csat_s1 = moyenne(tickets_s1, "csat")
    frt_s1 = moyenne(tickets_s1, "first_reply_time_min")
    macro_s1 = taux_rempli(tickets_s1, "macro_applied")
    resolution_s1 = moyenne(tickets_s1, "full_resolution_time_hours")

    # ------------------------------------------------------------------
    # Étape 5A -- la Vue d'ensemble consomme les moteurs validés (Tendances/Produit/Livraison/
    # Avant-vente/Impact & confiance), jamais une seconde vérité recalculée localement. Chaque
    # moteur est réinvoqué ici avec les mêmes entrées que dans son propre onglet (l'onglet Vue
    # d'ensemble s'exécute avant les onglets spécialisés dans le script -- leurs résultats ne sont
    # pas encore disponibles à ce stade) : duplication de calcul assumée et documentée (voir
    # compte-rendu Étape 5A, limites), jamais de logique métier réécrite.
    # ------------------------------------------------------------------

    exports_jusqu_a_periode_ve = []
    for date_export_ve, chemin_ve in exports_disponibles:
        if date_export_ve <= date_a_fin:
            exports_jusqu_a_periode_ve.append((date_export_ve, chemin_ve))

    profils_historique_ve = []
    for date_export_ve, chemin_ve in exports_jusqu_a_periode_ve:
        tickets_fichier_ve = charger_tickets(chemin_ve)
        if len(tickets_fichier_ve) == 0:
            continue
        planning_fichier_ve = charger_planning(chemin_ve)
        date_fin_fichier_ve = date_export_ve + datetime.timedelta(days=6)
        profils_historique_ve.append(construire_profil_observation(
            tickets_fichier_ve, planning_fichier_ve, evenements_calendrier, date_export_ve, date_fin_fichier_ve,
        ))

    lecture_tendance_ve = construire_lecture_tendances(profils_historique_ve, len(fichiers_actuels))

    vigilance_derniere_ve = None
    if len(lecture_tendance_ve["vigilances"]) > 0:
        vigilance_derniere_ve = lecture_tendance_ve["vigilances"][-1]

    index_dernier_profil_ve = len(profils_historique_ve) - 1
    rang_capacite_ve = None
    rang_volume_ve = None
    if index_dernier_profil_ve >= 0:
        capacites_ve = []
        volumes_profils_ve = []
        for profil_ve in profils_historique_ve:
            capacites_ve.append(profil_ve["capacite_heures"])
            volumes_profils_ve.append(profil_ve["volume"])
        rang_capacite_ve = rang_relatif(capacites_ve, index_dernier_profil_ve)
        rang_volume_ve = rang_relatif(volumes_profils_ve, index_dernier_profil_ve)

    historique_sav_produit_par_fichier_ve = []
    historique_livraison_par_fichier_ve = []
    historique_av_par_fichier_ve = []
    for date_export_hist_ve, chemin_hist_ve in exports_disponibles:
        if date_export_hist_ve < date_a_debut:
            tickets_fichier_hist_ve = charger_tickets(chemin_hist_ve)
            tickets_sav_hist_ve = []
            tickets_liv_hist_ve = []
            tickets_av_hist_ve = []
            for ticket_hist_ve in tickets_fichier_hist_ve:
                categorie_hist_ve = categoriser(ticket_hist_ve)
                if categorie_hist_ve == CATEGORIE_SAV_PRODUIT:
                    tickets_sav_hist_ve.append(ticket_hist_ve)
                elif categorie_hist_ve == "Livraison":
                    tickets_liv_hist_ve.append(ticket_hist_ve)
                elif categorie_hist_ve == "Avant-vente / conseil":
                    tickets_av_hist_ve.append(ticket_hist_ve)
            historique_sav_produit_par_fichier_ve.append(tickets_sav_hist_ve)
            historique_livraison_par_fichier_ve.append(tickets_liv_hist_ve)
            historique_av_par_fichier_ve.append(tickets_av_hist_ve)

    tickets_sav_produit_ve = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_livraison_ve = categories_s2.get("Livraison", [])
    tickets_av_ve = categories_s2.get("Avant-vente / conseil", [])

    resultats_produit_ve = moteur_produit_voie_a(
        tickets_sav_produit_ve, historique_sav_produit_par_fichier_ve, commandes, couts_produits, 5,
    )
    resultats_livraison_ve = moteur_livraison_voie_a(tickets_livraison_ve, historique_livraison_par_fichier_ve, 5)

    contexte_periode_ve = contexte_periode(evenements_calendrier, date_a_debut, date_a_fin)
    index_commandes_email_ve = commandes_par_email(commandes)
    resultats_achats_av_ve = resoudre_achats_observes_avant_vente(
        tickets_av_ve, index_commandes_email_ve, FENETRE_CONVERSION_JOURS,
    )
    resultats_motifs_av_ve = moteur_avant_vente_motifs(
        tickets_av_ve, resultats_achats_av_ve, historique_av_par_fichier_ve, contexte_periode_ve, 5,
    )

    reponses_nps_ve = charger_nps(FICHIER_NPS)
    historique_nps_mensuel_ve = construire_historique_nps_par_mois(reponses_nps_ve)
    cle_mois_periode_ve = date_a_debut.strftime("%Y-%m")
    index_mois_nps_ve = None
    for i_mois_ve in range(len(historique_nps_mensuel_ve)):
        if historique_nps_mensuel_ve[i_mois_ve]["cle_mois"] == cle_mois_periode_ve:
            index_mois_nps_ve = i_mois_ve

    alignement_nps_ve = None
    texte_alignement_nps_ve = None
    item_nps_ve = None
    if index_mois_nps_ve is not None:
        item_nps_ve = historique_nps_mensuel_ve[index_mois_nps_ve]
        tickets_par_mois_care_ve = {}
        for ticket_care_ve in tickets_historique_business:
            cle_mois_ticket_ve = ticket_care_ve["created_at"].strftime("%Y-%m")
            if cle_mois_ticket_ve in tickets_par_mois_care_ve:
                tickets_par_mois_care_ve[cle_mois_ticket_ve].append(ticket_care_ve)
            else:
                tickets_par_mois_care_ve[cle_mois_ticket_ve] = [ticket_care_ve]
        historique_care_mensuel_ve = []
        for item_mois_ve in historique_nps_mensuel_ve:
            historique_care_mensuel_ve.append(
                construire_profil_care_mensuel(tickets_par_mois_care_ve.get(item_mois_ve["cle_mois"], []))
            )
        alignement_nps_ve = evaluer_alignement_care_nps(
            historique_nps_mensuel_ve, historique_care_mensuel_ve, index_mois_nps_ve,
        )
        if alignement_nps_ve is not None:
            texte_alignement_nps_ve = texte_alignement_care_nps(
                alignement_nps_ve, historique_care_mensuel_ve[index_mois_nps_ve], "cette période",
            )

    candidats_categoriels_ve = extraire_candidats_categoriels_vue_ensemble(
        resultats_produit_ve["prioritaires"], resultats_livraison_ve["prioritaires"], resultats_motifs_av_ve["opportunites"],
    )
    diagnostics_transversaux_ve = evaluer_diagnostics_structures_transversal_vue_ensemble(
        profils_historique_ve, index_dernier_profil_ve,
        [CATEGORIE_SAV_PRODUIT, CATEGORIE_LIVRAISON_VUE_ENSEMBLE, CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE],
    )
    resultat_attention_ve = construire_signaux_attention_vue_ensemble(
        candidats_categoriels_ve, vigilance_derniere_ve, alignement_nps_ve, texte_alignement_nps_ve,
        diagnostics_transversaux_ve, SEUIL_MAX_SIGNAUX_ATTENTION_VUE_ENSEMBLE,
    )
    signaux_positifs_ve = construire_signal_positif_vue_ensemble(
        rang_capacite_ve, rang_volume_ve, alignement_nps_ve, texte_alignement_nps_ve,
    )
    anticipations_ve = construire_points_anticipation_vue_ensemble(evenements_calendrier, date_a_fin)
    navigation_ve = construire_navigation_vue_ensemble(resultat_attention_ve["retenus"])

    # ---- A. Lecture de la période ----
    # Étape 6D, section 5 : bloc éditorial distinct d'une simple caption -- réutilise l'info panel
    # 6C (construire_bandeau_info), texte inchangé (même synthèse, même phrase NPS, jamais réécrite).
    st.markdown(titre_section_principale(lecture_tendance_ve["titre"]), unsafe_allow_html=True)
    texte_lecture_ve_html = lecture_tendance_ve["synthese"]
    if item_nps_ve is not None:
        texte_lecture_ve_html = texte_lecture_ve_html + (
            '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">NPS '
            + formater_nps_entier(item_nps_ve["nps"]) + " (n=" + str(item_nps_ve["n"])
            + ") sur le mois correspondant -- voir Impact & confiance pour le détail et la prudence "
            "d'échantillon.</span>"
        )
    st.markdown(construire_bandeau_info(texte_lecture_ve_html), unsafe_allow_html=True)

    # ---- B. Indicateurs essentiels ----
    with st.container(border=True):
        if item_nps_ve is not None:
            colonnes_kpi_ve = st.columns(5)
        else:
            colonnes_kpi_ve = st.columns(4)

        if comparaison_disponible:
            colonnes_kpi_ve[0].markdown(
                construire_carte_kpi(
                    "Tickets reçus", formater_nombre_espace(nombre_s2),
                    delta=nombre_s2 - nombre_s1, delta_couleur="off",
                    sous_texte="vs période de comparaison",
                ),
                unsafe_allow_html=True,
            )
            if csat_s2 is not None and csat_s1 is not None:
                colonnes_kpi_ve[1].markdown(
                    construire_carte_kpi("CSAT moyen", formater_csat(csat_s2), delta=round(csat_s2 - csat_s1, 2)),
                    unsafe_allow_html=True,
                )
            else:
                colonnes_kpi_ve[1].markdown(construire_carte_kpi("CSAT moyen", formater_csat(csat_s2)), unsafe_allow_html=True)
            if frt_s2 is not None and frt_s1 is not None:
                colonnes_kpi_ve[2].markdown(
                    construire_carte_kpi(
                        "1re réponse", formater_duree(frt_s2),
                        delta=str(round(frt_s2 - frt_s1)) + " min", delta_couleur="inverse",
                    ),
                    unsafe_allow_html=True,
                )
            else:
                colonnes_kpi_ve[2].markdown(construire_carte_kpi("1re réponse", formater_duree(frt_s2)), unsafe_allow_html=True)
            if resolution_s2 is not None and resolution_s1 is not None:
                colonnes_kpi_ve[3].markdown(
                    construire_carte_kpi(
                        "Résolution moyenne", formater_duree(resolution_s2 * 60),
                        delta=str(round((resolution_s2 - resolution_s1) * 60)) + " min", delta_couleur="inverse",
                    ),
                    unsafe_allow_html=True,
                )
            elif resolution_s2 is not None:
                colonnes_kpi_ve[3].markdown(
                    construire_carte_kpi("Résolution moyenne", formater_duree(resolution_s2 * 60)), unsafe_allow_html=True
                )
        else:
            colonnes_kpi_ve[0].markdown(
                construire_carte_kpi("Tickets reçus", formater_nombre_espace(nombre_s2)), unsafe_allow_html=True
            )
            colonnes_kpi_ve[1].markdown(construire_carte_kpi("CSAT moyen", formater_csat(csat_s2)), unsafe_allow_html=True)
            colonnes_kpi_ve[2].markdown(construire_carte_kpi("1re réponse", formater_duree(frt_s2)), unsafe_allow_html=True)
            if resolution_s2 is not None:
                colonnes_kpi_ve[3].markdown(
                    construire_carte_kpi("Résolution moyenne", formater_duree(resolution_s2 * 60)), unsafe_allow_html=True
                )

        if item_nps_ve is not None:
            colonnes_kpi_ve[4].markdown(
                construire_carte_kpi(
                    "NPS", formater_nps_entier(item_nps_ve["nps"]), sous_texte="n=" + str(item_nps_ve["n"]),
                ),
                unsafe_allow_html=True,
            )

    # ---- C. Ce qui mérite votre attention ----
    # Étape 6D, section 8-9 : première migration vers construire_carte_signal (Étape 6C). Statut
    # "attention" uniforme -- rien dans la structure de ces signaux (titre/texte/onglet_cible) ne
    # distingue aujourd'hui un niveau de gravité, donc jamais "critique" ici (réservé à un signal
    # réellement produit comme tel par la logique métier, absent de cette liste). "Approfondir
    # dans" devient le badge -- même contenu, seulement la mise en forme change.
    st.markdown(titre_section_principale("Ce qui mérite votre attention"), unsafe_allow_html=True)
    if len(resultat_attention_ve["retenus"]) == 0:
        st.caption("Aucun signal prioritaire ne se détache sur cette période avec les critères actuels.")
    else:
        # Phase 4 (passe finale, mini-histoires) : conclusion transversale + jusqu'à 2 preuves
        # (volume, part de l'univers) quand elles existent déjà -- les signaux transversaux
        # (Tendances/NPS) n'en portent pas à ce niveau de composition, leur conclusion reste seule,
        # déjà porteuse du "pourquoi". Renvoi vers l'onglet concerné : badge existant, inchangé.
        for signal_ve in resultat_attention_ve["retenus"]:
            corps_ve_html = signal_ve["texte"]
            if signal_ve["volume_n"] is not None:
                texte_volume_ve = str(signal_ve["volume_n"]) + " " + accorder(signal_ve["volume_n"], "ticket", "tickets")
                if signal_ve.get("part_univers_pct") is not None:
                    texte_volume_ve = texte_volume_ve + " (" + formater_pourcentage(signal_ve["part_univers_pct"]) + " de la catégorie)"
                corps_ve_html = corps_ve_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">' + texte_volume_ve + "</span>"
                )
            st.markdown(
                construire_carte_signal(
                    signal_ve["titre"], "attention", corps_ve_html,
                    badge="Approfondir dans : " + signal_ve["onglet_cible"],
                ),
                unsafe_allow_html=True,
            )

    # ---- D. Ce qui tient ----
    # Étape 6D, section 10-11 : contrepartie visuelle de "Ce qui mérite votre attention", même
    # socle (radius/border/typo/espacements de construire_carte_signal) mais hiérarchie plus
    # légère -- statut "positive" en accent discret, pas de titre par carte (la donnée n'en fournit
    # pas), pas de badge. Jamais présenté comme un "succès" : wording métier (signaux_positifs_ve)
    # inchangé.
    if len(signaux_positifs_ve) > 0:
        st.markdown(titre_section_principale("Ce qui tient"), unsafe_allow_html=True)
        for texte_positif_ve in signaux_positifs_ve:
            st.markdown(
                construire_carte_signal(None, "positive", texte_positif_ve), unsafe_allow_html=True
            )

    # ---- E. Contexte de la période ----
    st.markdown(titre_section_principale("Contexte de la période"), unsafe_allow_html=True)
    evenements_texte = construire_texte_evenements(exports_disponibles, date_a_debut, date_a_fin)
    for changement in changements_planning:
        evenements_texte = evenements_texte + "  \nChangement planning : " + changement
    evenements_html = "Événements de la période :<br>" + evenements_texte.replace("  \n", "<br>")
    st.markdown(construire_bandeau_info(evenements_html), unsafe_allow_html=True)

    if len(anticipations_ve) > 0:
        st.markdown("**" + accorder(len(anticipations_ve), "Point d'anticipation", "Points d'anticipation") + "**")
        st.caption(
            "Événements à venir dans les " + str(FENETRE_ANTICIPATION_VUE_ENSEMBLE_JOURS) + " jours suivant "
            "cette période -- un repère, pas une dégradation actuelle."
        )
        for anticipation_ve in anticipations_ve:
            st.caption(str(anticipation_ve["date_debut"]) + " — " + anticipation_ve["type"] + " : " + anticipation_ve["nom_evenement"])

    # ---- F. Pour aller plus loin ----
    if len(navigation_ve) > 0:
        st.markdown("**Pour aller plus loin**")
        st.caption("Approfondir dans : " + ", ".join(navigation_ve))

    # ------------------------------------------------------------------
    # Détail (accordéons fermés, jamais affiché en avant -- section 36) : sujets par catégorie
    # (calculés une seule fois ici) pour le graphique de répartition et la performance détaillée.
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

    with st.expander("Répartition par famille (détail)"):
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
                    # Période précédente = une référence temporelle, pas une 2e série de données au
                    # même titre que la période actuelle -- gris neutre, jamais l'Accent secondaire
                    # (Étape 6C, section 15 ; Étape 6B, section 24).
                    scale=alt.Scale(
                        domain=["Période actuelle", "Période précédente"],
                        range=[COULEUR_PRIMAIRE, COULEUR_NEUTRE_TEXTE],
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

            # Étape 6J, section 19 : seul graphique de l'app encore hors configurer_apparence_graphique
            # (Vue d'ensemble, verrouillée depuis 6D, mais ce token manquant est un P1 visuel évident --
            # migration triviale, aucun changement de type/données). configure_axisX reste ensuite pour
            # la rotation des labels, compatible avec le config.axis déjà posé par le helper.
            graphique_categories = configurer_apparence_graphique(
                (barres_categories + etiquettes_evolution).properties(height=340)
            ).configure_axisX(labelAngle=-30)
            st.altair_chart(graphique_categories, width="stretch")
        else:
            lignes_graphique_categories = []
            for ligne in lignes_categories_apercu_triees:
                lignes_graphique_categories.append(
                    {"Catégorie": ligne["Catégorie"], "Période actuelle": ligne["Tickets"]}
                )
            tableau_graphique_categories = pd.DataFrame(lignes_graphique_categories).set_index("Catégorie")
            st.bar_chart(tableau_graphique_categories, color=COULEUR_PRIMAIRE)

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


# ------------------------------------------------------------------
# Onglet 2 : Tendances
# ------------------------------------------------------------------

with onglet_tendances:
    st.subheader("Tendances")
    st.caption("Ce que racontent les observations disponibles dans le temps : jalons, vigilances, contrastes.")

    exports_jusqu_a_periode = []
    for date_export, chemin in exports_disponibles:
        if date_export <= date_a_fin:
            exports_jusqu_a_periode.append((date_export, chemin))

    st.caption(
        "⚠️ Chaque point est une semaine représentative isolée, pas un suivi hebdomadaire continu — certains "
        "écarts entre observations vont jusqu'à 6-7 semaines. Les comparaisons ci-dessous se font contre "
        "l'ensemble des observations disponibles, jamais entre deux points voisins traités comme des semaines "
        "consécutives."
    )

    # profils_historique = TOUTES les observations disponibles jusqu'à la fin de la Période A
    # (aucune fuite du futur, par construction : exports_jusqu_a_periode ne contient jamais un
    # export postérieur à date_a_fin). nb_observations_periode = celles qui appartiennent
    # effectivement à la sélection de l'utilisatrice (fichiers_actuels) -- le reste, en tête de
    # liste, ne sert que d'historique de référence (Étape 4B.3).
    profils_historique = []
    lignes_tendance = []
    for date_export, chemin in exports_jusqu_a_periode:
        tickets_fichier = charger_tickets(chemin)
        if len(tickets_fichier) == 0:
            continue

        planning_fichier = charger_planning(chemin)
        date_fin_fichier = date_export + datetime.timedelta(days=6)
        profils_historique.append(construire_profil_observation(
            tickets_fichier, planning_fichier, evenements_calendrier, date_export, date_fin_fichier,
        ))
        profil_courant_tendance = profils_historique[-1]

        lignes_tendance.append({
            "Date": date_export,
            "Date fin": date_fin_fichier,
            "Tickets": len(tickets_fichier),
            "CSAT": moyenne(tickets_fichier, "csat"),
            "1re réponse (min)": moyenne(tickets_fichier, "first_reply_time_min"),
            "Resolution (h)": profil_courant_tendance["resolution_h"],
            "Utilisation macro (%)": taux_rempli(tickets_fichier, "macro_applied"),
            "Événement": evenements_periode(tickets_fichier),
            "Mix": profil_courant_tendance["mix_categories"],
        })

    lecture_tendance = construire_lecture_tendances(profils_historique, len(fichiers_actuels))

    # Étape 5B -- "Période analysée" vs "Historique de référence" (section 8) : une ligne discrète,
    # dérivée des observations déjà chargées ci-dessus, jamais un nouveau calcul métier.
    texte_periode_reference_tendances = construire_texte_periode_reference_tendances(
        profils_historique, lecture_tendance["mode"], lecture_tendance["nb_observations_periode"],
    )
    if texte_periode_reference_tendances is not None:
        st.caption(texte_periode_reference_tendances)

    # Étape 6E, section 5 : migration vers le panneau éditorial 6D (même patron que Vue
    # d'ensemble) -- texte inchangé, mêmes séquences, seulement la mise en forme change.
    st.markdown(titre_section_principale(lecture_tendance["titre"]), unsafe_allow_html=True)
    texte_lecture_tendance_html = lecture_tendance["synthese"]
    lignes_lecture_tendance_secondaires = []
    for repere_tendance in lecture_tendance["reperes"]:
        lignes_lecture_tendance_secondaires.append(repere_tendance)
    if lecture_tendance["contexte"] is not None:
        lignes_lecture_tendance_secondaires.append(lecture_tendance["contexte"])
    lignes_lecture_tendance_secondaires.append(lecture_tendance["niveau_confiance"])
    if lecture_tendance["saisonnalite"] is not None:
        lignes_lecture_tendance_secondaires.append(lecture_tendance["saisonnalite"]["observation"])
        lignes_lecture_tendance_secondaires.append(lecture_tendance["saisonnalite"]["prudence"])
    if len(lecture_tendance["jalons_metier"]) == 0 and len(lecture_tendance["vigilances"]) == 0:
        if lecture_tendance["mode"] != MODE_OBSERVATION_UNIQUE:
            lignes_lecture_tendance_secondaires.append("Aucun changement majeur ne se détache sur cette période.")
    for ligne_lecture_secondaire in lignes_lecture_tendance_secondaires:
        texte_lecture_tendance_html = texte_lecture_tendance_html + (
            '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
            + ligne_lecture_secondaire + "</span>"
        )
    st.markdown(construire_bandeau_info(texte_lecture_tendance_html), unsafe_allow_html=True)

    # Jalons : registre léger (une ligne), pas de grosses cartes -- ce ne sont pas des alertes.
    # Jamais affichés en mode "observation unique" (le sujet est la semaine sélectionnée, pas
    # l'historique -- si elle est elle-même un jalon, c'est déjà dit dans la synthèse ci-dessus).
    if len(lecture_tendance["jalons_metier"]) > 0:
        st.markdown(titre_section_principale("Jalons"), unsafe_allow_html=True)
        for jalon_tendance in lecture_tendance["jalons_metier"]:
            texte_jalon = (
                "**" + str(jalon_tendance["date_debut"]) + "** — " + jalon_tendance["registre"] + " : "
                + jalon_tendance["observation"]
            )
            if jalon_tendance["contexte"] is not None:
                texte_jalon = texte_jalon + " (" + jalon_tendance["contexte"] + ")"
            st.markdown(texte_jalon)

    # Vigilances : seule catégorie encore présentée en carte marquée -- réservée aux dégradations
    # réelles, jamais utilisée pour un simple écart de volume. Statut "watch" (Étape 6E, section 6) :
    # une vigilance de tendance, pas un signal métier matériel comme "attention" en Vue d'ensemble --
    # doit attirer l'œil sans transformer l'observation en crise, donc jamais "critique" ici.
    if len(lecture_tendance["vigilances"]) > 0:
        st.markdown(titre_section_principale("Vigilances"), unsafe_allow_html=True)
        st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_CAUSALE), unsafe_allow_html=True)
        for vigilance_tendance in lecture_tendance["vigilances"]:
            corps_vigilance_html = vigilance_tendance["observation"]
            lignes_meta_vigilance = [vigilance_tendance["pourquoi"]]
            if vigilance_tendance["contexte"] is not None:
                lignes_meta_vigilance.append(vigilance_tendance["contexte"])
            for ligne_meta_vigilance in lignes_meta_vigilance:
                corps_vigilance_html = corps_vigilance_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                    + ligne_meta_vigilance + "</span>"
                )
            st.markdown(
                construire_carte_signal("⚠️ " + str(vigilance_tendance["date_debut"]), "watch", corps_vigilance_html),
                unsafe_allow_html=True,
            )

    # Contrastes : information analytique riche mais pas une vigilance -- carte neutre (statut
    # None), aucune couleur d'alerte (Étape 6E, section 8). Wording inchangé.
    if len(lecture_tendance["contrastes"]) > 0:
        st.markdown(titre_section_principale("Contrastes entre observations comparables"), unsafe_allow_html=True)
        st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_CAUSALE), unsafe_allow_html=True)
        for contraste_tendance in lecture_tendance["contrastes"]:
            corps_contraste_html = contraste_tendance["observation"]
            lignes_meta_contraste = [contraste_tendance["pourquoi"]]
            for ligne_meta_contraste in lignes_meta_contraste:
                corps_contraste_html = corps_contraste_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                    + ligne_meta_contraste + "</span>"
                )
            st.markdown(construire_carte_signal(None, None, corps_contraste_html), unsafe_allow_html=True)

    # Graphiques : scope selon le mode -- mode 1 affiche l'historique complet en repère (avec la
    # période analysée distinguée visuellement), mode 2 se limite aux observations de la fenêtre
    # sélectionnée, mode 3 conserve le comportement d'origine (tout l'historique).
    date_semaine_analysee = None
    if lecture_tendance["mode"] == MODE_OBSERVATION_UNIQUE:
        titre_expander_tendance = "Replacer cette période dans l'historique"
        lignes_graphique = lignes_tendance
        if len(profils_historique) > 0:
            date_semaine_analysee = profils_historique[-1]["date_debut"]
    else:
        titre_expander_tendance = "Détail métrique par observation"
        nb_lignes_periode = lecture_tendance["nb_observations_periode"]
        lignes_graphique = lignes_tendance[len(lignes_tendance) - nb_lignes_periode:]

    tableau_tendance = pd.DataFrame(lignes_graphique)

    encodage_couleur_volume = alt.value(COULEUR_PRIMAIRE)
    encodage_couleur_csat = alt.value(COULEUR_SECONDAIRE)
    encodage_couleur_effort = alt.value(COULEUR_ACCENT_FONCE)
    colonnes_tooltip_supplementaires = []

    if date_semaine_analysee is not None and len(tableau_tendance) > 0:
        valeurs_selection = []
        for date_valeur in tableau_tendance["Date"]:
            if date_valeur == date_semaine_analysee:
                valeurs_selection.append("Période analysée")
            else:
                valeurs_selection.append("Historique")
        tableau_tendance["Sélection"] = valeurs_selection
        echelle_selection = alt.Scale(
            domain=["Historique", "Période analysée"], range=[COULEUR_TEXTE_LABEL, COULEUR_PRIMAIRE],
        )
        encodage_couleur_volume = alt.Color("Sélection:N", scale=echelle_selection, legend=alt.Legend(title=None))
        encodage_couleur_csat = encodage_couleur_volume
        encodage_couleur_effort = encodage_couleur_volume
        colonnes_tooltip_supplementaires = ["Sélection:N"]

    # Étape 5B -- 4 graphiques principaux maximum, chacun répondant à une question distincte
    # (section 34/40) : Activité (volume), Expérience (CSAT), Effort/complexité (résolution --
    # remplace macro/FRT ici, tous deux peu discriminants entre périodes, voir compte-rendu),
    # Composition de la demande (mix catégories, jamais montré avant faute de graphique dédié).
    # FRT et Utilisation macro restent accessibles dans le détail chiffré ci-dessous, jamais
    # supprimés.
    with st.expander(titre_expander_tendance):
        st.markdown(titre_section_principale("Activité"), unsafe_allow_html=True)
        st.caption("Comment le niveau d'activité évolue-t-il entre les observations disponibles ?")
        graphique_volume = configurer_apparence_graphique(
            alt.Chart(tableau_tendance).mark_line(point=True, strokeDash=[4, 4]).encode(
                x=alt.X("Date:T", title=None),
                y=alt.Y("Tickets:Q"),
                color=encodage_couleur_volume,
                tooltip=["Date:T", "Tickets:Q", "Événement:N"] + colonnes_tooltip_supplementaires,
            ).properties(height=260)
        )
        with st.container(border=True):
            st.altair_chart(graphique_volume, width="stretch")

        st.markdown(titre_section_principale("Expérience (CSAT)"), unsafe_allow_html=True)
        st.caption("La satisfaction se dégrade-t-elle ou se maintient-elle entre les observations ?")
        graphique_csat = configurer_apparence_graphique(
            alt.Chart(tableau_tendance).mark_line(point=True, strokeDash=[4, 4]).encode(
                x=alt.X("Date:T", title=None),
                y=alt.Y("CSAT:Q", scale=alt.Scale(domain=[1, 5])),
                color=encodage_couleur_csat,
                tooltip=["Date:T", alt.Tooltip("CSAT:Q", format=".2f"), "Événement:N"] + colonnes_tooltip_supplementaires,
            ).properties(height=260)
        )
        with st.container(border=True):
            st.altair_chart(graphique_csat, width="stretch")

        st.markdown(titre_section_principale("Effort / complexité (résolution)"), unsafe_allow_html=True)
        st.caption("Les dossiers demandent-ils plus de temps à clôturer d'une observation à l'autre ?")
        graphique_resolution = configurer_apparence_graphique(
            alt.Chart(tableau_tendance).mark_line(point=True, strokeDash=[4, 4]).encode(
                x=alt.X("Date:T", title=None),
                y=alt.Y("Resolution (h):Q", title="Heures"),
                color=encodage_couleur_effort,
                tooltip=["Date:T", alt.Tooltip("Resolution (h):Q", format=".1f"), "Événement:N"] + colonnes_tooltip_supplementaires,
            ).properties(height=260)
        )
        with st.container(border=True):
            st.altair_chart(graphique_resolution, width="stretch")

        st.markdown(titre_section_principale("Composition de la demande"), unsafe_allow_html=True)
        st.caption("La nature des demandes change-t-elle d'une observation à l'autre (ex. Livraison en pic saisonnier, SAV en janvier) ?")
        lignes_mix_long = []
        for ligne_mix in lignes_graphique:
            for categorie_mix, n_categorie_mix in ligne_mix["Mix"].items():
                lignes_mix_long.append({"Date": ligne_mix["Date"], "Catégorie": categorie_mix, "Tickets": n_categorie_mix})
        tableau_mix = pd.DataFrame(lignes_mix_long)
        graphique_mix = configurer_apparence_graphique(
            alt.Chart(tableau_mix).mark_bar().encode(
                x=alt.X("Date:T", title=None),
                y=alt.Y("Tickets:Q", stack="normalize", axis=alt.Axis(format="%"), title="Part de la demande"),
                # Mapping fixe (jamais la palette par défaut d'Altair, qui recycle des teintes selon
                # l'ordre d'apparition et change de sens d'une période à l'autre -- Étape 6C, section 16).
                color=alt.Color(
                    "Catégorie:N",
                    scale=alt.Scale(domain=DOMAINE_CATEGORIES, range=PLAGE_COULEURS_CATEGORIES),
                    legend=alt.Legend(title=None),
                ),
                tooltip=["Date:T", "Catégorie:N", "Tickets:Q"],
            ).properties(height=260)
        )
        with st.container(border=True):
            st.altair_chart(graphique_mix, width="stretch")
        st.caption("Répartition en %, pas en volume — voir « Activité » ci-dessus pour le volume total.")

        with st.expander("Détail chiffré par observation"):
            lignes_detail_tendance = []
            for ligne_detail in lignes_graphique:
                lignes_detail_tendance.append({
                    "Observation": str(ligne_detail["Date"]) + " → " + str(ligne_detail["Date fin"]),
                    "Volume": ligne_detail["Tickets"],
                    "CSAT": formater_csat(ligne_detail["CSAT"]) if ligne_detail["CSAT"] is not None else "N/A",
                    "1re réponse": formater_duree(ligne_detail["1re réponse (min)"]) if ligne_detail["1re réponse (min)"] is not None else "N/A",
                    "Résolution (h)": str(round(ligne_detail["Resolution (h)"], 1)) if ligne_detail["Resolution (h)"] is not None else "N/A",
                    "Utilisation macro (%)": formater_pourcentage(ligne_detail["Utilisation macro (%)"]),
                    "Mix principal": categorie_dominante_mix_tendances(ligne_detail["Mix"]),
                    "Contexte": ligne_detail["Événement"],
                })
            st.dataframe(lignes_detail_tendance, hide_index=True, width="stretch")


# Étape 5C.1 -- construire_profil_agent (quadrant volume/CSAT non normalisé par les heures ni le
# mix -- audité et jugé non défendable, voir compte-rendu Étape 5C) et obtenir_categorie_dominante
# (remplacée par categorie_dominante_mix_tendances, déjà réutilisée depuis 5B, qui accepte aussi
# bien des comptes que des %) supprimées. Aucun autre usage dans l'application (vérifié).


# ------------------------------------------------------------------
# Onglet 3 : Agents
# ------------------------------------------------------------------

with onglet_agents:
    st.subheader("Agents")
    st.caption("Qui compose l'équipe sur la période, comment la charge se répartit -- sans classement.")

    st.caption(DEFINITION_EN_CRENEAU)
    st.caption(
        "Le volume rapporté aux heures planifiées décrit la charge observée ; il ne constitue pas une "
        "mesure de performance. Le type de dossiers traité peut fortement modifier le rythme de "
        "traitement -- voir la répartition par catégorie ci-dessous et le détail par agent."
    )

    roster_agents = construire_roster_agents(tickets_s2, planning_s2, evenements_calendrier, date_a_debut, date_a_fin)

    n_tickets_non_assignes = 0
    for ticket_verif_assignee in tickets_s2:
        if ticket_verif_assignee["assignee"] is None:
            n_tickets_non_assignes = n_tickets_non_assignes + 1
    if n_tickets_non_assignes > 0:
        st.caption(
            str(n_tickets_non_assignes) + " " + accorder(n_tickets_non_assignes, "ticket non assigné", "tickets non assignés")
            + " cette période (non inclus ci-dessous)."
        )

    # ---- Lecture de l'équipe (factuelle, jamais un classement -- Étape 5C.1) ----
    # Étape 6E, section 15 : panneau éditorial 6D, texte inchangé, aucun jugement ajouté.
    st.markdown(titre_section_principale("Lecture de l'équipe"), unsafe_allow_html=True)
    st.markdown(construire_bandeau_info(construire_lecture_equipe_agents(roster_agents)), unsafe_allow_html=True)

    # ---- Table principale : 6 colonnes, ordre alphabétique (jamais par volume/CSAT), aucune
    # couleur bon/mauvais -- la charge relative et le CSAT+n remplacent le champ "Profil" supprimé.
    lignes_table_agents = []
    for ligne_roster in roster_agents:
        agent_ligne = ligne_roster["agent"]
        tickets_agent_ligne = ligne_roster["tickets"]
        heures_ligne = ligne_roster["heures_planifiees"]
        statut_ligne = ligne_roster["statut"]
        nb_tickets_ligne = len(tickets_agent_ligne)

        if statut_ligne == STATUT_AGENT_ABSENT:
            if ligne_roster["evenement_absence"] is not None:
                texte_presence = ligne_roster["evenement_absence"]["nom_evenement"]
            else:
                texte_presence = "Non planifié cette période"
        elif statut_ligne == STATUT_AGENT_RENFORT_NON_PLANIFIE:
            texte_presence = "Non planifié (activité observée)"
        else:
            texte_presence = str(heures_ligne) + "h planifiées"

        charge_ligne = charge_relative_agent(nb_tickets_ligne, heures_ligne)
        if charge_ligne is not None:
            texte_charge = str(round(charge_ligne, 1))
        else:
            texte_charge = "N/A"

        mix_ligne = mix_pct_agent(tickets_agent_ligne)
        if len(mix_ligne) > 0:
            mix_principal_ligne = categorie_dominante_mix_tendances(mix_ligne)
        else:
            mix_principal_ligne = "N/A"

        csat_agent_ligne = moyenne(tickets_agent_ligne, "csat")
        n_csat_agent_ligne = 0
        for ticket_csat_ligne in tickets_agent_ligne:
            if ticket_csat_ligne["csat"] is not None:
                n_csat_agent_ligne = n_csat_agent_ligne + 1
        if csat_agent_ligne is not None:
            texte_csat_ligne = formater_csat(csat_agent_ligne) + " (n=" + str(n_csat_agent_ligne) + ")"
        else:
            texte_csat_ligne = "N/A"

        lignes_table_agents.append({
            "Agent": agent_ligne,
            "Présence": texte_presence,
            "Tickets": nb_tickets_ligne,
            "Tickets / h planifiée": texte_charge,
            "Mix principal": mix_principal_ligne,
            "CSAT (n)": texte_csat_ligne,
        })

    with st.container(border=True):
        afficher_tableau_colore(lignes_table_agents, colonne_figee="Agent")

    # ---- Détail par agent : résumé factuel, puis catégorie -> sujet (architecture existante) ----
    st.markdown(titre_section_principale("Détail par agent"), unsafe_allow_html=True)
    st.caption("D'abord un résumé et la répartition par catégorie, puis choisis une catégorie pour voir le détail par sujet.")

    for ligne_roster in roster_agents:
        agent_detail = ligne_roster["agent"]
        tickets_agent_detail = ligne_roster["tickets"]

        if len(tickets_agent_detail) == 0:
            continue  # rien à détailler pour un agent sans activité observée cette période

        with st.expander(agent_detail):
            heures_detail = ligne_roster["heures_planifiees"]
            charge_detail = charge_relative_agent(len(tickets_agent_detail), heures_detail)
            csat_detail = moyenne(tickets_agent_detail, "csat")
            n_csat_detail = 0
            for ticket_csat_detail in tickets_agent_detail:
                if ticket_csat_detail["csat"] is not None:
                    n_csat_detail = n_csat_detail + 1
            resolution_detail = moyenne(tickets_agent_detail, "full_resolution_time_hours")
            macro_detail = taux_rempli(tickets_agent_detail, "macro_applied")
            role_detail = roles_periode.get(agent_detail, "—")

            texte_resume_detail = role_detail + " · " + str(len(tickets_agent_detail)) + " tickets"
            if charge_detail is not None:
                texte_resume_detail = texte_resume_detail + " · " + str(round(charge_detail, 1)) + " tickets/h planifiée"
            if csat_detail is not None:
                texte_resume_detail = texte_resume_detail + " · CSAT " + formater_csat(csat_detail) + " (n=" + str(n_csat_detail) + ")"
            if resolution_detail is not None:
                texte_resume_detail = texte_resume_detail + " · résolution moyenne " + formater_duree(resolution_detail * 60)
            if macro_detail is not None:
                texte_resume_detail = texte_resume_detail + " · macro " + formater_pourcentage(macro_detail)
            st.caption(texte_resume_detail)
            st.caption(
                "Les temps de résolution dépendent fortement du type de demande : SAV et dossiers "
                "impliquant des tiers peuvent rester ouverts plusieurs jours."
            )

            categories_agent = grouper_par_categorie(tickets_agent_detail)

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
                "Détail par sujet pour :", noms_categories_agent, key="categorie_" + agent_detail
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

    # ---- Évolution d'un agent (Étape 5C.1, section 26-31) : uniquement les observations où
    # l'agent a une activité réelle, jamais un point fabriqué pendant une absence ou avant son
    # arrivée. Aucune fuite du futur (exports bornés à date_a_fin, même discipline que 4B/5B).
    st.markdown(titre_section_principale("Évolution d'un agent"), unsafe_allow_html=True)
    st.caption(
        "Observations disponibles où l'agent a une activité réelle uniquement -- jamais un point "
        "artificiel pendant une absence ou avant son arrivée dans l'équipe."
    )

    agents_pour_historique = []
    for ligne_roster in roster_agents:
        if len(ligne_roster["tickets"]) > 0:
            agents_pour_historique.append(ligne_roster["agent"])

    if len(agents_pour_historique) == 0:
        st.caption("Aucun agent actif sur cette période.")
    else:
        agent_choisi_historique = st.selectbox("Voir l'évolution de :", agents_pour_historique, key="agent_historique_selectbox")

        exports_avec_donnees_historique_agent = []
        for date_export_hist_agent, chemin_hist_agent in exports_disponibles:
            if date_export_hist_agent <= date_a_fin:
                tickets_fichier_hist_agent = charger_tickets(chemin_hist_agent)
                planning_fichier_hist_agent = charger_planning(chemin_hist_agent)
                exports_avec_donnees_historique_agent.append((
                    date_export_hist_agent, date_export_hist_agent + datetime.timedelta(days=6),
                    tickets_fichier_hist_agent, planning_fichier_hist_agent,
                ))

        historique_agent_choisi = construire_historique_agent(exports_avec_donnees_historique_agent, agent_choisi_historique)

        if len(historique_agent_choisi) <= 1:
            st.caption("Pas encore assez d'observations disponibles pour cet agent pour tracer une évolution.")
        else:
            lignes_historique_agent_choisi = []
            for item_historique_agent in historique_agent_choisi:
                lignes_historique_agent_choisi.append({
                    "Date": item_historique_agent["date_debut"],
                    "Charge (tickets/h)": item_historique_agent["charge_relative"],
                    "CSAT": item_historique_agent["csat"],
                    "n (CSAT)": item_historique_agent["n_csat"],
                })
            tableau_historique_agent_choisi = pd.DataFrame(lignes_historique_agent_choisi)

            st.markdown("**Charge observée (tickets / heure planifiée)**")
            graphique_charge_agent_choisi = configurer_apparence_graphique(
                alt.Chart(tableau_historique_agent_choisi).mark_line(point=True, strokeDash=[4, 4]).encode(
                    x=alt.X("Date:T", title=None),
                    y=alt.Y("Charge (tickets/h):Q"),
                    color=alt.value(COULEUR_PRIMAIRE),
                    tooltip=["Date:T", alt.Tooltip("Charge (tickets/h):Q", format=".1f")],
                ).properties(height=220)
            )
            with st.container(border=True):
                st.altair_chart(graphique_charge_agent_choisi, width="stretch")

            st.markdown("**CSAT**")
            graphique_csat_agent_choisi = configurer_apparence_graphique(
                alt.Chart(tableau_historique_agent_choisi).mark_line(point=True, strokeDash=[4, 4]).encode(
                    x=alt.X("Date:T", title=None),
                    y=alt.Y("CSAT:Q", scale=alt.Scale(domain=[1, 5])),
                    color=alt.value(COULEUR_SECONDAIRE),
                    tooltip=["Date:T", alt.Tooltip("CSAT:Q", format=".2f"), "n (CSAT):Q"],
                ).properties(height=220)
            )
            with st.container(border=True):
                st.altair_chart(graphique_csat_agent_choisi, width="stretch")



# Carte neutre pour une piste d'amélioration -- pas d'accent coloré (bordure fine standard, comme
# construire_carte_kpi sans accent), volontairement pas l'esthétique "alerte critique" de l'ancien
# onglet (Étape 5D.1, section 39). QUOI / POURQUOI / PISTE seulement, jamais "cause" ni "action"
# prescriptive (section 27). Une piste n'est pas un signal -- jamais construire_carte_signal avec
# un statut coloré ici (Étape 6E, section 23) ; tokens 6C alignés sur RADIUS_CARTE/ESPACE_M/ESPACE_S
# en 6E, sans changer le langage visuel déjà validé en 5D.1.
def construire_carte_piste_actions(piste, quoi, pourquoi):
    return (
        '<div style="background-color:' + COULEUR_FOND_CARTE + "; border:1px solid " + COULEUR_BORDURE_CARTE + "; "
        "border-radius:" + RADIUS_CARTE + "; padding:14px " + ESPACE_M + "; margin-bottom:" + ESPACE_S + ';">'
        '<div style="font-size:13px; font-weight:700; color:' + COULEUR_TEXTE_VALEUR + ';">' + quoi + "</div>"
        '<div style="font-size:12px; color:' + COULEUR_TEXTE_LABEL + '; margin-top:5px;"><b>Observé</b> : '
        + pourquoi + "</div>"
        '<div style="font-size:12px; font-weight:600; color:' + COULEUR_PRIMAIRE + '; margin-top:5px;">'
        + piste["piste"] + "</div>"
        "</div>"
    )


# Étape 6E, section 24 : évite le "top arbitraire" identifié comme problème UX en 5D.1 (une
# famille peut compter 14-17 pistes) sans jamais supprimer une piste -- aperçu des premières
# (déjà triées par volume décroissant), le reste reste accessible dans un expander, jamais caché
# sans accès.
def afficher_cartes_avec_apercu(cartes_html, nombre_apercu, libelle_singulier, libelle_pluriel=None):
    cartes_apercu = cartes_html[:nombre_apercu]
    cartes_restantes = cartes_html[nombre_apercu:]
    for carte_html in cartes_apercu:
        st.markdown(carte_html, unsafe_allow_html=True)
    if len(cartes_restantes) > 0:
        n_restantes = len(cartes_restantes)
        if n_restantes == 1:
            titre_expander_apercu = "Voir l'autre " + libelle_singulier
        else:
            titre_expander_apercu = "Voir les " + str(n_restantes) + " autres " + accorder(n_restantes, libelle_singulier, libelle_pluriel)
        with st.expander(titre_expander_apercu):
            for carte_html in cartes_restantes:
                st.markdown(carte_html, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Onglet 4 : Actions & améliorations (ex "Alertes & suggestions", refondu Étape 5D.1)
# ------------------------------------------------------------------

with onglet_alertes:
    st.subheader("Actions & améliorations")
    st.caption(
        "À partir des irritants et opportunités observés, quelles améliorations concrètes peut-on "
        "explorer, qu'a-t-on déjà essayé, et qu'est-ce que cela semble avoir changé ?"
    )

    NOMBRE_PISTES_APERCU_ACTIONS = 5

    suivi_suggestions = charger_suivi_suggestions(FICHIER_SUIVI_SUGGESTIONS)

    # ------------------------------------------------------------------
    # A. Pistes d'amélioration -- 3 familles indépendantes (Standardisation / Self-service /
    # Retours clients), jamais comparées entre elles par un score : chacune a son propre critère
    # de tri explicable (volume décroissant), affiché dans l'accordéon méthodologique ci-dessous.
    # ------------------------------------------------------------------

    pistes_standardisation = identifier_pistes_standardisation(
        tickets_s2, suivi_suggestions, SEUIL_MINIMUM_SUJET, SEUIL_CSAT_INSATISFAISANT
    )
    pistes_self_service = identifier_pistes_self_service(
        tickets_s2, suivi_suggestions, SEUIL_MINIMUM_SUJET, SEUIL_REPLIES_FAQ_ACTIONS
    )
    retours_clients_a_explorer = identifier_retours_clients_a_explorer(
        tickets_s2, SEUIL_CSAT_VERBATIM_ACTIONS, SEUIL_VERBATIMS_GROUPE_ACTIONS
    )

    st.markdown(titre_section_principale("Pistes d'amélioration"), unsafe_allow_html=True)

    with st.expander("Comment les pistes sont identifiées"):
        st.markdown(
            "- **Standardisation** : sujet avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets sur la "
            "période, une satisfaction moyenne insuffisante, et une macro absente ou peu utilisée.\n"
            "- **Self-service** : sujet avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets et "
            + str(SEUIL_REPLIES_FAQ_ACTIONS) + " échanges en moyenne ou plus pour être résolu.\n"
            "- **Retours clients à explorer** : au moins " + str(SEUIL_VERBATIMS_GROUPE_ACTIONS) + " "
            "commentaires clients à note très basse (" + str(SEUIL_CSAT_VERBATIM_ACTIONS) + "/5 ou moins) "
            "portant sur le même sujet.\n"
            "- Un sujet déjà marqué « Fait » dans le suivi des actions n'est pas reproposé comme "
            "nouvelle piste de standardisation ou de self-service.\n"
            "- Chaque famille est triée par volume décroissant, jamais comparée aux autres familles."
        )

    # Étape 6E, section 23-25 : les 3 familles restent distinguables par leur libellé (typo/label),
    # pas par 3 couleurs -- toutes en carte neutre (construire_carte_piste_actions / carte_signal
    # statut None), jamais Signal card "attention". Aperçu + expander (afficher_cartes_avec_apercu,
    # section 24) évite qu'une famille à fort volume (ex. 14-17 pistes en janvier) écrase la page,
    # sans jamais supprimer une piste.
    total_pistes = len(pistes_standardisation) + len(pistes_self_service) + len(retours_clients_a_explorer)
    if total_pistes == 0:
        st.caption("Aucune nouvelle piste d'amélioration ne ressort sur cette observation.")
    else:
        if len(pistes_standardisation) > 0:
            st.markdown(
                "**Standardisation** — " + str(len(pistes_standardisation))
                + " " + accorder(len(pistes_standardisation), "piste", "pistes")
            )
            cartes_standardisation = []
            for piste in pistes_standardisation:
                quoi = piste["sujet"] + " — " + str(piste["volume"]) + " tickets"
                pourquoi = (
                    "CSAT " + formater_csat(piste["csat"]) + ", usage macro "
                    + formater_pourcentage(piste["usage_macro_pct"])
                )
                cartes_standardisation.append(construire_carte_piste_actions(piste, quoi, pourquoi))
            afficher_cartes_avec_apercu(
                cartes_standardisation, NOMBRE_PISTES_APERCU_ACTIONS,
                "piste de standardisation", "pistes de standardisation",
            )

        if len(pistes_self_service) > 0:
            st.markdown(
                "**Self-service** — " + str(len(pistes_self_service))
                + " " + accorder(len(pistes_self_service), "piste", "pistes")
            )
            cartes_self_service = []
            for piste in pistes_self_service:
                quoi = piste["sujet"] + " — " + str(piste["volume"]) + " tickets"
                pourquoi = str(round(piste["echanges_moyens"], 1)) + " échanges en moyenne"
                if piste["csat"] is not None:
                    pourquoi = pourquoi + ", CSAT " + formater_csat(piste["csat"])
                cartes_self_service.append(construire_carte_piste_actions(piste, quoi, pourquoi))
            afficher_cartes_avec_apercu(
                cartes_self_service, NOMBRE_PISTES_APERCU_ACTIONS,
                "piste de self-service", "pistes de self-service",
            )

        if len(retours_clients_a_explorer) > 0:
            st.markdown(
                "**Retours clients à explorer** — " + str(len(retours_clients_a_explorer))
                + " " + accorder(len(retours_clients_a_explorer), "sujet", "sujets")
            )
            st.caption("Voix client à investiguer, pas une conclusion causale — détail dans l'accordéon plus bas.")
            cartes_retours_clients = []
            for groupe in retours_clients_a_explorer:
                titre_retour = (
                    groupe["sujet"] + " — " + str(groupe["volume"])
                    + " " + accorder(groupe["volume"], "commentaire", "commentaires")
                )
                corps_retour = "CSAT moyen sur ces retours : " + formater_csat(groupe["csat"])
                cartes_retours_clients.append(construire_carte_signal(titre_retour, None, corps_retour))
            afficher_cartes_avec_apercu(
                cartes_retours_clients, NOMBRE_PISTES_APERCU_ACTIONS,
                "sujet de retours clients", "sujets de retours clients",
            )

    # ------------------------------------------------------------------
    # B. Actions déjà menées -- suivi_suggestions.xlsx. "Fait" = action réalisée, pas succès garanti :
    # aucun badge de couleur, l'écart avant/après (quand disponible) reste au conditionnel.
    # ------------------------------------------------------------------

    # Étape 6E, section 30 : divider retiré -- titre_section_principale (liseré + marge) sépare déjà
    # suffisamment les sections, cohérent avec Vue d'ensemble/Tendances/Agents (0 divider).
    st.markdown(titre_section_principale("Actions déjà menées"), unsafe_allow_html=True)
    st.caption(
        "À partir du suivi manuel des actions. « Fait » signifie que l'action a été réalisée — pas que "
        "le problème est résolu."
    )

    actions_menees = construire_actions_menees_actions(suivi_suggestions, tickets_historique_business, date_a_fin)

    if len(actions_menees) == 0:
        st.caption("Aucune action déjà menée n'est visible sur cette période.")
    else:
        # Étape 6E, section 26-28 : statut "positive" en accent léger (jamais "vert triomphant" --
        # pas de grande surface colorée, juste un liseré) signale que l'action a été RÉALISÉE, pas
        # qu'elle a réussi -- le texte d'impact reste neutre (aucune flèche colorée), donc aucune
        # contradiction possible avec un résultat neutre ou non amélioré.
        au_moins_une_comparaison_chiffree = False
        for action in actions_menees:
            if action["mesure_avant_disponible"] and action["mesure_apres_disponible"]:
                au_moins_une_comparaison_chiffree = True
                break
        if au_moins_une_comparaison_chiffree:
            st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_AVANT_APRES_ACTIONS), unsafe_allow_html=True)

        for action in actions_menees:
            corps_action_html = ""
            if action["notes"]:
                corps_action_html = action["notes"]

            impact = action["impact"]
            if action["mesure_avant_disponible"] and action["mesure_apres_disponible"]:
                texte_impact_action = (
                    "Après la mise en place, le CSAT observé passe de " + formater_csat(impact["csat_avant"])
                    + " à " + formater_csat(impact["csat_apres"]) + " (" + str(impact["volume_avant"])
                    + " tickets avant, " + str(impact["volume_apres"]) + " après)."
                )
                # Précaution causale déjà affichée une fois au niveau section (voir
                # au_moins_une_comparaison_chiffree ci-dessus) -- jamais répétée par carte.
                texte_secondaire_action = None
            else:
                texte_impact_action = None
                texte_secondaire_action = (
                    "Pas assez de données avant et/ou après cette action, sur cette période, pour "
                    "donner une lecture chiffrée."
                )

            # Phase 4 (passe finale, mini-histoires) : constat (notes, poids normal de la carte) ->
            # preuve (impact chiffré, en retrait muted comme partout ailleurs -- avant/après n'avait
            # jusqu'ici pas la même hiérarchie visuelle que les autres onglets).
            if texte_impact_action is not None:
                if corps_action_html != "":
                    corps_action_html = corps_action_html + "<br>"
                corps_action_html = corps_action_html + (
                    '<span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">' + texte_impact_action + "</span>"
                )

            if texte_secondaire_action is not None:
                if corps_action_html != "":
                    corps_action_html = corps_action_html + "<br>"
                corps_action_html = corps_action_html + (
                    '<span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">' + texte_secondaire_action + "</span>"
                )

            badge_action = action["statut"] + " · " + action["date_action"].strftime("%d/%m/%Y")
            st.markdown(
                construire_carte_signal(action["sujet"], "positive", corps_action_html, badge=badge_action),
                unsafe_allow_html=True,
            )

    # ------------------------------------------------------------------
    # C/D. Détail et éléments d'investigation -- verbatims complets par sujet, tickets les plus longs
    # à résoudre, macros/FAQ associées aux actions déjà menées. Rien de prescriptif, tout en retrait.
    # ------------------------------------------------------------------

    def obtenir_date_ticket(ticket):
        return ticket["created_at"]

    def obtenir_resolution(ticket):
        return ticket["full_resolution_time_hours"]

    tickets_avec_resolution = []
    for ticket in tickets_s2:
        if ticket["full_resolution_time_hours"] is not None:
            tickets_avec_resolution.append(ticket)

    tickets_tries_par_resolution = sorted(tickets_avec_resolution, key=obtenir_resolution, reverse=True)

    lignes_longs = []
    for ticket in tickets_tries_par_resolution[:10]:
        lignes_longs.append({
            "Ticket": ticket["ticket_id"],
            "Agent": ticket["assignee"],
            "Catégorie": categoriser(ticket),
            "Résolution": formater_duree(ticket["full_resolution_time_hours"] * 60),
            "Résolu par": ticket["resolution_type"],
        })

    lignes_macros_associees = []
    for action in actions_menees:
        code_macro = extraire_code_macro(action["notes"])
        texte_macro = charger_texte_macro(code_macro, DOSSIER_MACROS)
        if texte_macro is not None:
            nom_fichier_faq = extraire_nom_fichier_faq(texte_macro)
            faq_associee = "—"
            if nom_fichier_faq is not None:
                texte_faq = charger_texte_faq(nom_fichier_faq, DOSSIER_FAQ)
                if texte_faq is not None:
                    faq_associee = nom_fichier_faq

            lignes_macros_associees.append({
                "Sujet": action["sujet"],
                "Macro": code_macro,
                "FAQ associée": faq_associee,
            })

    with st.expander("Détail et éléments d'investigation"):
        st.markdown("**Retours clients — commentaires détaillés**")
        if len(retours_clients_a_explorer) == 0:
            st.write("Aucun retour client à détailler sur cette période.")
        else:
            for groupe in retours_clients_a_explorer:
                tickets_recents = sorted(groupe["tickets"], key=obtenir_date_ticket, reverse=True)[:3]
                titre_expander = (
                    groupe["sujet"] + " (" + str(groupe["volume"])
                    + " " + accorder(groupe["volume"], "commentaire", "commentaires") + ")"
                )
                with st.expander(titre_expander):
                    lignes_verbatims_sujet = []
                    for ticket in tickets_recents:
                        lignes_verbatims_sujet.append({
                            # Étape 6J, section 12 : dette connue -- affichait la valeur numérique
                            # brute au lieu de passer par formater_csat (convention "4,05" partout
                            # ailleurs). Purement présentationnel, aucune donnée changée.
                            "CSAT": formater_csat(ticket["csat"]) if ticket["csat"] is not None else "N/A",
                            "Commentaire": ticket["csat_comment"],
                        })
                    st.dataframe(lignes_verbatims_sujet, hide_index=True, width="stretch")

        st.markdown("**Les 10 tickets les plus longs à résoudre**")
        st.dataframe(lignes_longs, hide_index=True, width="stretch")

        if len(lignes_macros_associees) > 0:
            st.markdown("**Macros/FAQ créées lors d'actions déjà menées**")
            st.caption("Texte complet dans le CRM, pas dupliqué ici.")
            st.dataframe(lignes_macros_associees, hide_index=True, width="stretch")


# La référence historique (Étape 5E.1) recharge et reconstruit une grille de pression pour
# CHAQUE export antérieur disponible (jusqu'à 13 pour la période la plus récente) -- environ 15s
# sans cache, systématiquement payé à CHAQUE rerun Streamlit (tous les onglets s'exécutent, visible
# ou non). Mise en cache par (exports_disponibles, date_limite) : les fichiers ne changent pas
# pendant l'exécution, donc un même couple ne peut produire qu'un seul résultat valide.
@st.cache_data
def _reference_historique_couverture_cache(exports_disponibles, date_limite):
    return construire_reference_historique_couverture(exports_disponibles, date_limite)


# ------------------------------------------------------------------
# Onglet 5 : Couverture & réactivité
# ------------------------------------------------------------------

with onglet_creneaux:
    st.subheader("Couverture")
    # Étape 6G, section 4 : intro déjà existante et équivalente, reprise telle quelle -- pas de
    # nouveau wording métier.
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
    # Données de couverture partagées -- grille de PRESSION (jour x heure), corrigée
    # multi-semaines (Étape 5E.1 : la capacité est désormais sommée semaine par semaine, jamais
    # la capacité de la seule dernière semaine appliquée à un volume cumulé), enrichie de la
    # classification pression/tension relative à l'historique STRICTEMENT ANTÉRIEUR (no future
    # leakage, même discipline que Tendances 4B). Step 1 (agents_en_poste, activite_observee,
    # renfort_non_planifie) reste inchangé, appelé depuis outils.py.
    # ------------------------------------------------------------------

    agents_grille = construire_agents_grille_couverture(tickets_s2, planning_s2)
    horaires_standard = planning_s2_dernier.get(NOM_AGENT_DEFAUT, {})
    grille_pression = construire_grille_pression_couverture(tickets_s2, planning_s2, agents_grille, horaires_standard)

    ratios_reference, frt_medians_reference = _reference_historique_couverture_cache(
        exports_disponibles, date_a_debut
    )
    grille_enrichie = enrichir_grille_pression_tension_couverture(
        grille_pression, en_creneau, ratios_reference, frt_medians_reference
    )

    tensions = []
    pressions_marquees_absorbees = []
    activite_hors_capacite_materielle = []
    for entree in grille_enrichie:
        if entree["est_tension"]:
            tensions.append(entree)
        elif entree["niveau_pression"] in (NIVEAU_PRESSION_MARQUEE, NIVEAU_PRESSION_FORTE):
            pressions_marquees_absorbees.append(entree)
        if entree["niveau_pression"] == NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE:
            activite_hors_capacite_materielle.append(entree)

    def obtenir_rang_pression_tri(entree):
        rang = entree["rang_pression"]
        if rang is None:
            return -1
        return rang

    tensions_triees = sorted(tensions, key=obtenir_rang_pression_tri, reverse=True)
    pressions_marquees_absorbees_triees = sorted(pressions_marquees_absorbees, key=obtenir_rang_pression_tri, reverse=True)

    taux_sla_global = taux_sla(tickets_s2, planning_s2)
    taux_sla_s1 = None
    if comparaison_disponible:
        taux_sla_s1 = taux_sla(tickets_s1, planning_s1)

    capacite_planifiee_heures = 0
    for date_debut_semaine, date_fin_semaine, planning_semaine in planning_s2:
        for agent in agents_grille:
            capacite_planifiee_heures = capacite_planifiee_heures + heures_planifiees_agent(planning_semaine, agent)

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
    # A. Lecture de couverture -- 2-4 phrases data-driven, aucun nouveau calcul (Étape 5E.1).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Lecture de couverture"), unsafe_allow_html=True)
    st.markdown(
        construire_bandeau_info(
            construire_lecture_couverture(
                len(tensions), len(pressions_marquees_absorbees), taux_sla_global, SLA_OBJECTIF_PCT,
                hors_couverture_significatif,
            )
        ),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # B. KPI compacts -- Demandes / Capacité planifiée / FRT en couverture / SLA. Étape 6G, section
    # 36 : divider retiré, le bandeau ci-dessus sépare déjà suffisamment.
    # ------------------------------------------------------------------

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

    colonne_s2.markdown(
        construire_carte_kpi("Capacité planifiée", formater_nombre_espace(round(capacite_planifiee_heures)) + " h"),
        unsafe_allow_html=True,
    )

    frt_en_creneau_global = moyenne(en_creneau, "first_reply_time_min")
    frt_en_creneau_global_s1 = None
    if comparaison_disponible:
        frt_en_creneau_global_s1 = moyenne(en_creneau_s1, "first_reply_time_min")

    if frt_en_creneau_global is not None:
        delta_frt_couverture = None
        if frt_en_creneau_global_s1 is not None:
            delta_frt_couverture = round(frt_en_creneau_global - frt_en_creneau_global_s1)

        if delta_frt_couverture is not None:
            colonne_s3.markdown(
                construire_carte_kpi(
                    "1re réponse (en créneau)", formater_duree(frt_en_creneau_global),
                    delta=str(delta_frt_couverture) + " min", delta_couleur="inverse",
                ),
                unsafe_allow_html=True,
            )
        else:
            colonne_s3.markdown(
                construire_carte_kpi("1re réponse (en créneau)", formater_duree(frt_en_creneau_global)),
                unsafe_allow_html=True,
            )

    if taux_sla_global is not None:
        if comparaison_disponible and taux_sla_s1 is not None:
            colonne_s4.markdown(
                construire_carte_kpi(
                    "SLA respecté", formater_pourcentage(taux_sla_global),
                    delta=round(taux_sla_global - taux_sla_s1, 1),
                ),
                unsafe_allow_html=True,
            )
        else:
            colonne_s4.markdown(
                construire_carte_kpi("SLA respecté", formater_pourcentage(taux_sla_global)),
                unsafe_allow_html=True,
            )

    # ------------------------------------------------------------------
    # C. Heatmap -- PRESSION demande / capacité (Étape 5E.1 : couleur = pression relative à
    # l'historique, jamais une qualité de service jugée dans l'absolu).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Pression de charge (demande / capacité planifiée)"), unsafe_allow_html=True)
    st.caption(
        "Cette heatmap représente une PRESSION DE CHARGE relative à l'historique disponible — pas "
        "une mesure de qualité de service : un créneau très sollicité peut rester bien absorbé (voir "
        "« Créneaux à examiner » ci-dessous pour la distinction, légende détaillée sous la grille). "
        "Les créneaux fermés (horaire standard, pause, week-end) sont grisés — ce volume est suivi à "
        "part, agrégé sur la période, dans la section « Demande hors couverture » plus bas."
    )

    # Étape 6G, section 9 : typographie fonctionnelle relevée à 10px minimum (9px identifié en 6B) --
    # tailles/couleurs seules changent, aucune donnée/logique de cellule touchée. hm-muted référençait
    # encore un hex pré-6C (#B7AFA3, ancienne valeur de COULEUR_TEXTE_MUTED avant son assombrissement
    # en 6C) au lieu du token courant -- corrigé (Étape 6G, section 33/36).
    html_heatmap = (
        "<style>"
        ".hm-grid { display: grid; grid-template-columns: 40px repeat(7, 1fr); gap: 3px; margin-bottom: 8px; }"
        ".hm-day-header, .hm-hour-label, .hm-corner { font-size: 10px; font-weight: 600; color: " + COULEUR_TEXTE_LABEL + "; "
        "display: flex; align-items: center; justify-content: center; padding: 2px; }"
        ".hm-cell { border-radius: 5px; padding: 3px 4px; text-align: center; line-height: 1.25; "
        "min-height: 40px; display: flex; flex-direction: column; justify-content: center; }"
        ".hm-cell-bande { min-height: 22px; }"
        ".hm-line-agents { font-weight: 600; font-size: 10px; color: " + COULEUR_TEXTE_VALEUR + "; }"
        ".hm-line-demandes { font-size: 10px; color: " + COULEUR_TEXTE_LABEL + "; }"
        ".hm-line-ratio { font-size: 10px; font-weight: 700; color: " + COULEUR_TEXTE_VALEUR + "; }"
        ".hm-line-tension { font-size: 10px; font-weight: 700; color: " + COULEUR_ACCENT_SURVEILLER + "; margin-top: 1px; }"
        ".hm-muted { font-size: 10px; color: " + COULEUR_TEXTE_MUTED + "; }"
        "</style>"
    )

    html_heatmap = html_heatmap + '<div class="hm-grid">' + '<div class="hm-corner"></div>'
    for nom_jour, numero_jour in JOURS_ORDRE:
        html_heatmap = html_heatmap + '<div class="hm-day-header">' + nom_jour[:3] + "</div>"

    grille_par_jour_heure = {}
    for entree in grille_enrichie:
        grille_par_jour_heure[(entree["jour"], entree["heure"])] = entree

    premiere_ouverture, derniere_fermeture = determiner_bornes_ouverture(horaires_standard)
    bandes_heatmap = construire_bandes_heatmap(premiere_ouverture, derniere_fermeture)

    for type_bande, heure_debut_bande, heure_fin_bande in bandes_heatmap:
        if type_bande == "HEURE":
            html_heatmap = html_heatmap + '<div class="hm-hour-label">' + str(heure_debut_bande) + "h</div>"
            for nom_jour, numero_jour in JOURS_ORDRE:
                entree = grille_par_jour_heure[(nom_jour, heure_debut_bande)]
                html_heatmap = html_heatmap + construire_cellule_pression_couverture(entree)
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

    # Étape 6G, section 15 : légende explicite, PRESSION et TENSION documentées séparément -- le
    # lecteur ne doit jamais lire la couleur de fond comme une performance d'agent (section 16 :
    # aucune couleur individuelle par agent non plus, les prénoms restent du texte simple partout).
    html_legende_pression = (
        '<div style="display:flex; flex-wrap:wrap; gap:14px; align-items:center; font-size:12px; '
        "color:" + COULEUR_TEXTE_LABEL + '; margin:8px 0 4px;">'
        '<span style="font-weight:600;">Fond = pression :</span>'
    )
    # Étape 6J, section 32 : "libelle_niveau" évitée comme nom de boucle -- collision avec la
    # fonction globale libelle_niveau() (outils.py), qui écrasait la référence pour tout le reste
    # du script et faisait planter afficher_tableau_colore() plus loin ("'str' object is not
    # callable"). P0 visuel trouvé et corrigé pendant cette étape.
    for libelle_niveau_legende, couleur_niveau_legende in (
        (NIVEAU_PRESSION_HABITUELLE, COULEUR_HEATMAP_CONFORTABLE),
        (NIVEAU_PRESSION_MARQUEE, COULEUR_HEATMAP_SURVEILLER),
        (NIVEAU_PRESSION_FORTE, COULEUR_HEATMAP_PRESSION_FORTE),
        (NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE, COULEUR_HEATMAP_HOTSPOT),
        ("Fermé / hors couverture", COULEUR_HEATMAP_HORS_COUVERTURE),
    ):
        html_legende_pression = html_legende_pression + (
            '<span><span style="display:inline-block; width:10px; height:10px; border-radius:2px; '
            "background-color:" + couleur_niveau_legende + "; margin-right:5px; vertical-align:middle; "
            'border:1px solid ' + COULEUR_BORDURE_CARTE + ';"></span>' + libelle_niveau_legende + "</span>"
        )
    html_legende_pression = html_legende_pression + (
        '<span style="color:' + COULEUR_ACCENT_SURVEILLER + '; font-weight:700;">⚠ Tension : réactivité '
        "locale dégradée — indépendant de la couleur de fond, voir « Tensions à examiner » ci-dessous.</span>"
        "</div>"
    )
    st.markdown(html_legende_pression, unsafe_allow_html=True)

    st.caption(
        "Survolez une cellule pour voir la liste complète des agents en poste sur ce créneau. Les "
        "heures avant l'ouverture et après la fermeture sont regroupées en un seul bloc — volume "
        "cumulé sur la plage, sans détail heure par heure."
    )

    # ------------------------------------------------------------------
    # D. Créneaux à examiner -- séparation explicite pression-seule (absorbée) / tension réelle
    # (pression + réactivité locale dégradée). Jamais un plafond forcé (Étape 5E.1, section 28) :
    # 0 tension reste un résultat valide, pas un vide à combler.
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Créneaux à examiner"), unsafe_allow_html=True)
    st.markdown("**Tensions à examiner**")
    st.caption("Pression de charge marquée ET réactivité locale dégradée — jamais la pression seule.")
    if len(tensions_triees) > 0:
        cartes_tensions = []
        for entree in tensions_triees:
            cartes_tensions.append(construire_carte_tension_couverture(entree))
        afficher_cartes_avec_apercu(cartes_tensions, 5, "tension")
    else:
        st.caption("Aucune tension à examiner sur cette observation.")

    if len(pressions_marquees_absorbees_triees) > 0:
        morceaux_pression = []
        for entree in pressions_marquees_absorbees_triees:
            morceaux_pression.append(entree["jour"] + " " + str(entree["heure"]) + "h")
        n_pressions_marquees_absorbees = len(pressions_marquees_absorbees_triees)
        st.caption(
            str(n_pressions_marquees_absorbees) + " " + accorder(n_pressions_marquees_absorbees, "créneau", "créneaux")
            + " à pression marquée, " + accorder(n_pressions_marquees_absorbees, "absorbé", "absorbés") + " "
            "(réactivité locale non dégradée, ou non mesurable localement) : "
            + " · ".join(morceaux_pression) + "."
        )

    if len(activite_hors_capacite_materielle) > 0:
        morceaux_hc = []
        for entree in activite_hors_capacite_materielle:
            morceaux_hc.append(
                entree["jour"] + " " + str(entree["heure"]) + "h (" + str(entree["demandes"]) + " demandes)"
            )
        st.caption(
            "Activité observée sans capacité planifiée, hors renfort identifié : "
            + " · ".join(morceaux_hc) + "."
        )

    # ------------------------------------------------------------------
    # E. Réactivité par canal -- explique la réactivité globale, ne déclenche jamais la pression.
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Réactivité par canal"), unsafe_allow_html=True)
    st.caption(
        "SLA : en créneau ouvert, 1re réponse sous 1h. Hors créneau, réponse attendue au plus tard à la "
        "fin de la 1re plage horaire du prochain jour disponible — ex : message reçu vendredi 19h, "
        "réponse due lundi avant 12h (avant l'ouverture ou pendant la pause déjeuner : réponse due "
        "avant la fin du jour même)."
    )

    st.markdown("**Répartition des temps de réponse, tickets reçus en créneau**")
    compte_niveaux = {"OK": 0, "A SURVEILLER": 0, "CRITIQUE": 0, "DEBORDEMENT": 0}
    for ticket in en_creneau:
        frt_ticket = ticket["first_reply_time_min"]
        if frt_ticket is not None:
            niveau = niveau_reponse_ouvree(frt_ticket)
            compte_niveaux[niveau] = compte_niveaux[niveau] + 1
    st.markdown(construire_barre_empilee_reponse(compte_niveaux, len(en_creneau)), unsafe_allow_html=True)

    insight_sla = construire_insight_sla(taux_sla_global, SLA_OBJECTIF_PCT, pire_canal)
    if insight_sla is not None:
        st.caption(insight_sla)

    with st.container(border=True):
        afficher_tableau_colore(
            lignes_canal_en_triees,
            colonnes_couleur_bloc={"1re réponse moyenne": niveaux_reponse_canal},
        )

    insight_canal = construire_insight_canal(pire_canal)
    if insight_canal is not None:
        st.caption(insight_canal)

    # ------------------------------------------------------------------
    # F. Demande hors couverture
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Demande hors couverture"), unsafe_allow_html=True)
    st.caption("La demande reçue hors couverture justifie-t-elle une adaptation des horaires ?")

    colonne_h1, colonne_h2 = st.columns(2)
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

    # ------------------------------------------------------------------
    # G. Renforts non planifiés -- Step 1 (renfort_non_planifie), inchangé.
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Renforts non planifiés"), unsafe_allow_html=True)
    synthese_renfort = construire_synthese_renfort(grille_enrichie)
    if len(synthese_renfort) > 0:
        morceaux_renfort = []
        for agent, stats in synthese_renfort.items():
            morceaux_renfort.append(
                agent + " (" + str(stats["heures"]) + "h, " + str(stats["demandes"]) + " demandes)"
            )
        st.caption(
            "Activité observée sans capacité prévue correspondante, pendant les horaires standard — "
            "à ne jamais confondre avec de la capacité planifiée : " + " · ".join(morceaux_renfort) + "."
        )
    else:
        st.caption("Aucun renfort ponctuel non planifié détecté sur cette période.")

    # ------------------------------------------------------------------
    # H. Planning détaillé (accordéon)
    # ------------------------------------------------------------------

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
            "Les horaires et le rôle d'un agent, ainsi que le créneau standard de l'équipe, sont mis à "
            "jour en amont à partir des exports fournis — utile si un agent passe à mi-temps, ferme un "
            "mois donné, ou ajoute des heures supplémentaires. Les arrivées/départs/absences ponctuelles "
            "sont également pris en compte de cette façon."
        )


# construire_insight_composant / construire_insight_resolution supprimées (Étape 5F.1, sections
# 4-5) : recréaient une conclusion analytique locale ("défaut structurel"/"défaut matériel réel à
# corriger") à partir du seul volume ou du seul type de résolution dominant, sans passer par 4A --
# concurrentes de 4A, verdict plus fort que ce que 4A autoriserait sur les mêmes données. Les
# tables descriptives (Contacts SAV par composant, Type de résolution) restent, sans conclusion
# analytique attachée ; construire_texte_resolution_produit (outils.py) les remplace en version
# strictement descriptive quand le texte apporte une vraie valeur de transmission.
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
    st.subheader("Produit")
    st.caption("Signaux produit, composants concernés, dossiers associés.")

    st.caption(
        "Cadence trimestrielle recommandée — élargis la Période A dans la barre latérale pour une vraie "
        "tendance produit. Les exports disponibles sont des semaines représentatives espacées dans le "
        "temps, pas un historique continu : élargir la période ajoute les exports compris "
        "dans la plage, sans combler les semaines entre deux exports."
    )

    tickets_sav_produit_s2 = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_sav_produit_s1 = categories_s1.get(CATEGORIE_SAV_PRODUIT, [])

    NOMBRE_MAX_SIGNAUX_VOIE_A = 5

    historique_sav_produit_par_fichier = []
    for date_export_historique, chemin_historique in exports_disponibles:
        if date_export_historique < date_a_debut:
            tickets_fichier_historique = charger_tickets(chemin_historique)
            tickets_sav_produit_fichier = []
            for ticket_historique in tickets_fichier_historique:
                if categoriser(ticket_historique) == CATEGORIE_SAV_PRODUIT:
                    tickets_sav_produit_fichier.append(ticket_historique)
            historique_sav_produit_par_fichier.append(tickets_sav_produit_fichier)

    resultats_voie_a = moteur_produit_voie_a(
        tickets_sav_produit_s2, historique_sav_produit_par_fichier, commandes, couts_produits,
        NOMBRE_MAX_SIGNAUX_VOIE_A,
    )
    signaux_prioritaires = resultats_voie_a["prioritaires"]
    signaux_a_surveiller = resultats_voie_a["a_surveiller"]
    signaux_voie_b = moteur_produit_voie_b(tickets_sav_produit_s2)

    part_sav_pct = None
    if len(tickets_s2) > 0:
        part_sav_pct = len(tickets_sav_produit_s2) / len(tickets_s2) * 100

    # ------------------------------------------------------------------
    # Étape 7B -- comparaison A/B Produit. B est évalué avec exactement les mêmes règles métier
    # que A (même moteur, même historique symétrique construit sur date_b_debut) -- seul le
    # plafond d'affichage est retiré (PLAFOND_SIGNAUX_COMPARAISON_B), jamais un critère du moteur.
    # Sert uniquement de table de correspondance (clé structurelle -> niveau_priorite), jamais
    # affiché comme une seconde liste de signaux.
    # ------------------------------------------------------------------

    signaux_prioritaires_b_produit = []
    signaux_a_surveiller_b_produit = []
    part_sav_pct_s1 = None
    csat_sav_global_s1 = None
    n_csat_sav_global_s1 = 0
    resolution_sav_global_s1 = None
    produit_duree_comparable = False

    if comparaison_disponible:
        produit_duree_comparable = periodes_comparables_en_duree(date_a_debut, date_a_fin, date_b_debut, date_b_fin)

        if len(tickets_s1) > 0:
            part_sav_pct_s1 = len(tickets_sav_produit_s1) / len(tickets_s1) * 100
        csat_sav_global_s1 = moyenne(tickets_sav_produit_s1, "csat")
        for ticket_sav_ctx_s1 in tickets_sav_produit_s1:
            if ticket_sav_ctx_s1["csat"] is not None:
                n_csat_sav_global_s1 = n_csat_sav_global_s1 + 1
        resolution_sav_global_s1 = moyenne(tickets_sav_produit_s1, "full_resolution_time_hours")

        historique_sav_produit_par_fichier_b = []
        for date_export_historique_b, chemin_historique_b in exports_disponibles:
            if date_export_historique_b < date_b_debut:
                tickets_fichier_historique_b = charger_tickets(chemin_historique_b)
                tickets_sav_produit_fichier_b = []
                for ticket_historique_b in tickets_fichier_historique_b:
                    if categoriser(ticket_historique_b) == CATEGORIE_SAV_PRODUIT:
                        tickets_sav_produit_fichier_b.append(ticket_historique_b)
                historique_sav_produit_par_fichier_b.append(tickets_sav_produit_fichier_b)

        resultats_voie_a_b_produit = moteur_produit_voie_a(
            tickets_sav_produit_s1, historique_sav_produit_par_fichier_b, commandes, couts_produits,
            PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        signaux_prioritaires_b_produit = resultats_voie_a_b_produit["prioritaires"]
        signaux_a_surveiller_b_produit = resultats_voie_a_b_produit["a_surveiller"]

    niveau_priorite_par_cle_b_produit = {}
    for signal_b_produit in signaux_prioritaires_b_produit + signaux_a_surveiller_b_produit:
        cle_b_produit, grain_b_produit = cle_signal_produit(signal_b_produit)
        if cle_b_produit is not None:
            niveau_priorite_par_cle_b_produit[(cle_b_produit, grain_b_produit)] = signal_b_produit["niveau_priorite"]

    def _evolution_signal_produit_vs_b(signal):
        cle_produit_ab, grain_produit_ab = cle_signal_produit(signal)
        if cle_produit_ab is None:
            return None
        niveau_b_produit = niveau_priorite_par_cle_b_produit.get((cle_produit_ab, grain_produit_ab))
        qualification_produit = evaluer_evolution_signal_vs_b(signal["niveau_priorite"], niveau_b_produit)
        return texte_evolution_signal_vs_b(qualification_produit)

    # "Ne ressort plus parmi les signaux de A" -- jamais "résolu" (formulation imposée). Limité aux
    # 2 signaux B les mieux étayés (niveau de priorité le plus haut) pour rester une mention dans la
    # synthèse, pas une seconde liste.
    texte_signaux_disparus_produit = None
    if comparaison_disponible:
        # Le set d'exclusion doit couvrir TOUS les signaux qualifiés de A, pas seulement les
        # signaux_prioritaires/signaux_a_surveiller déjà plafonnés à l'affichage (NOMBRE_MAX_SIGNAUX_
        # VOIE_A) -- sinon un signal réellement qualifié sur A mais non affiché serait signalé à tort
        # comme "ne ressort plus". Même plafond purement UI que côté B, mêmes règles métier.
        resultats_voie_a_complet_produit = moteur_produit_voie_a(
            tickets_sav_produit_s2, historique_sav_produit_par_fichier, commandes, couts_produits,
            PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        cles_a_produit = set()
        for signal_a_produit in (
            resultats_voie_a_complet_produit["prioritaires"] + resultats_voie_a_complet_produit["a_surveiller"]
        ):
            cle_a_produit, grain_a_produit = cle_signal_produit(signal_a_produit)
            if cle_a_produit is not None:
                cles_a_produit.add((cle_a_produit, grain_a_produit))

        signaux_disparus_produit = []
        for signal_b_produit in signaux_prioritaires_b_produit + signaux_a_surveiller_b_produit:
            cle_b_produit, grain_b_produit = cle_signal_produit(signal_b_produit)
            if cle_b_produit is not None and (cle_b_produit, grain_b_produit) not in cles_a_produit:
                signaux_disparus_produit.append(signal_b_produit)

        if len(signaux_disparus_produit) > 0:
            def _rang_disparu_produit(signal):
                return -RANG_NIVEAU_PRIORITE.get(signal["niveau_priorite"], 0)

            signaux_disparus_produit_tries = sorted(signaux_disparus_produit, key=_rang_disparu_produit)
            noms_disparus_produit = []
            for signal_disparu_produit in signaux_disparus_produit_tries[:2]:
                noms_disparus_produit.append(titre_signal_produit(signal_disparu_produit))
            verbe_disparu_produit = accorder(len(noms_disparus_produit), "ne ressort plus", "ne ressortent plus")
            texte_signaux_disparus_produit = (
                " · ".join(noms_disparus_produit) + " " + verbe_disparu_produit + " parmi les signaux de A."
            )

    # ------------------------------------------------------------------
    # A. Lecture Produit -- dérivée uniquement des sorties déjà produites par 4A (Étape 5F.1).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Lecture Produit"), unsafe_allow_html=True)
    texte_lecture_produit = construire_lecture_produit(
        signaux_prioritaires, resultats_voie_a["nb_prioritaires_avant_plafond"],
        signaux_a_surveiller, resultats_voie_a["nb_a_surveiller_avant_plafond"],
        len(signaux_voie_b), part_sav_pct,
    )
    if texte_signaux_disparus_produit is not None:
        texte_lecture_produit = texte_lecture_produit + " " + texte_signaux_disparus_produit
    st.markdown(construire_bandeau_info(texte_lecture_produit), unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # B. Contexte SAV compact -- 4 informations, jamais un coût global (Étape 5F.1, section 11).
    # Étape 6F, section 36 : divider retiré -- le bandeau ci-dessus sépare déjà suffisamment.
    # ------------------------------------------------------------------

    colonne_ctx1, colonne_ctx2, colonne_ctx3, colonne_ctx4 = st.columns(4)

    delta_dossiers_produit = None
    sous_texte_dossiers_produit = None
    if comparaison_disponible:
        if produit_duree_comparable:
            delta_dossiers_produit = formater_delta_nombre(len(tickets_sav_produit_s2) - len(tickets_sav_produit_s1))
        else:
            sous_texte_dossiers_produit = (
                "B : " + formater_nombre_espace(len(tickets_sav_produit_s1)) + " (durées non comparables)"
            )
    colonne_ctx1.markdown(
        construire_carte_kpi(
            "Dossiers SAV Produit", formater_nombre_espace(len(tickets_sav_produit_s2)),
            delta=delta_dossiers_produit, delta_couleur="off", sous_texte=sous_texte_dossiers_produit,
        ),
        unsafe_allow_html=True,
    )

    if part_sav_pct is not None:
        delta_part_sav_produit = None
        if comparaison_disponible and part_sav_pct_s1 is not None:
            delta_part_sav_produit = formater_delta_points(part_sav_pct - part_sav_pct_s1)
        colonne_ctx2.markdown(
            construire_carte_kpi(
                "Part du total", formater_pourcentage(part_sav_pct),
                delta=delta_part_sav_produit, delta_couleur="off",
            ),
            unsafe_allow_html=True,
        )

    csat_sav_global = moyenne(tickets_sav_produit_s2, "csat")
    n_csat_sav_global = 0
    for ticket_sav_ctx in tickets_sav_produit_s2:
        if ticket_sav_ctx["csat"] is not None:
            n_csat_sav_global = n_csat_sav_global + 1
    if csat_sav_global is not None:
        sous_texte_csat_produit = "n=" + str(n_csat_sav_global)
        delta_csat_produit = None
        if comparaison_disponible:
            if csat_sav_global_s1 is not None:
                delta_csat_produit = formater_delta_nombre(csat_sav_global - csat_sav_global_s1, decimales=2)
                sous_texte_csat_produit = (
                    sous_texte_csat_produit + " · B : " + formater_csat(csat_sav_global_s1)
                    + " (n=" + str(n_csat_sav_global_s1) + ")"
                )
            else:
                sous_texte_csat_produit = sous_texte_csat_produit + " · B : N/A"
        colonne_ctx3.markdown(
            construire_carte_kpi(
                "CSAT SAV Produit", formater_csat(csat_sav_global), sous_texte=sous_texte_csat_produit,
                delta=delta_csat_produit, delta_couleur="normal",
            ),
            unsafe_allow_html=True,
        )

    resolution_sav_global = moyenne(tickets_sav_produit_s2, "full_resolution_time_hours")
    if resolution_sav_global is not None:
        delta_resolution_produit = None
        if comparaison_disponible and resolution_sav_global_s1 is not None:
            delta_resolution_produit = formater_delta_duree((resolution_sav_global - resolution_sav_global_s1) * 60)
        colonne_ctx4.markdown(
            construire_carte_kpi(
                "Résolution moyenne", formater_duree(resolution_sav_global * 60),
                delta=delta_resolution_produit, delta_couleur="inverse",
            ),
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------
    # C. Priorités à investiguer -- 4A seul propriétaire, aucun recalcul (Étape 5F.1, section 12).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Priorités à investiguer"), unsafe_allow_html=True)
    st.markdown(
        construire_note_methodologique(
            "« Priorité principale »/« secondaire » décrit le niveau de convergence des preuves, pas une "
            "gravité absolue. " + TEXTE_PRUDENCE_CAUSALE
        ),
        unsafe_allow_html=True,
    )

    if len(signaux_prioritaires) == 0 and len(signaux_a_surveiller) == 0 and len(signaux_voie_b) == 0:
        st.caption("Aucun signal Produit ne présente actuellement une convergence suffisante pour être investigué.")
    else:
        # Étape 6F, section 6-7-10 : même Signal card pour principal et secondaire -- seule la
        # force de l'accent change (statut "attention" uniquement pour la priorité principale,
        # jamais de rouge/critique ici). Le badge porte toujours le niveau ("Priorité principale"/
        # "secondaire"), donc la distinction reste lisible même en traitement neutre. Le titre
        # sépare visuellement le préfixe produit (plus discret) du composant/sujet (poids plein) --
        # deux signaux sur le même produit restent distinguables sans nouvelle couleur.
        for signal_produit in signaux_prioritaires:
            prefixe_titre_produit, principal_titre_produit = titre_signal_produit_parties(signal_produit)
            if prefixe_titre_produit is not None:
                titre_html_produit = (
                    '<span style="font-weight:400; color:' + COULEUR_TEXTE_MUTED + ';">'
                    + prefixe_titre_produit + " — </span>" + principal_titre_produit
                )
            else:
                titre_html_produit = principal_titre_produit

            if signal_produit["niveau_priorite"] == "Priorité principale":
                statut_signal_produit = "attention"
            else:
                statut_signal_produit = None

            corps_produit_html = signal_produit["observation_principale"]

            # Étape 7B -- tag de comparaison A/B, ajouté hors du plafond des 2-3 preuves (Phase 4) :
            # c'est un repère d'identité/évolution, pas une preuve du signal lui-même.
            if comparaison_disponible:
                texte_evolution_produit = _evolution_signal_produit_vs_b(signal_produit)
                if texte_evolution_produit is not None:
                    corps_produit_html = corps_produit_html + (
                        '<br><span style="font-size:12px; font-weight:600; color:' + COULEUR_TEXTE_MUTED + ';">'
                        + texte_evolution_produit + "</span>"
                    )

            # Phase 4 (passe finale, mini-histoires) : constat -> 2-3 preuves principales
            # sélectionnées pour CE signal (jamais le même trio imposé partout) -> détail/
            # méthodologie relégué dans un expander. Volume toujours en premier (établit
            # l'échelle) ; puis CSAT et impact financier priorisés s'ils existent (ce sont eux qui
            # disent "pourquoi ça compte" -- expérience client, conséquence business), sinon
            # concentration puis temporalité comblent les 2-3 preuves. Rien n'est supprimé : tout
            # champ non promu en preuve principale reste visible dans le détail, avec sa référence/
            # son n intacts.
            texte_volume_produit = (
                str(signal_produit["volume"]["n"]) + " tickets ("
                + formater_pourcentage(signal_produit["volume"]["part_univers_pct"])
                + " du SAV produit de la période, univers " + str(signal_produit["volume"]["univers"]) + ")"
            )
            texte_temporalite_produit = "Temporalité : " + signal_produit["temporalite"]

            texte_csat_produit = None
            if signal_produit["experience"]["csat"] is not None:
                texte_csat_produit = (
                    "CSAT : " + formater_csat(signal_produit["experience"]["csat"])
                    + " (n=" + str(signal_produit["experience"]["n_csat"]) + ") vs "
                    + formater_csat(signal_produit["experience"]["csat_reference"])
                    + " pour le SAV Produit sur cette observation — " + signal_produit["experience"]["lecture"]
                )

            texte_cout_produit = None
            if signal_produit["cout"] is not None:
                texte_cout_produit = (
                    "Impact financier associé : " + formater_montant(signal_produit["cout"]["montant"])
                    + " (méthodologie détaillée dans l'onglet Impact & confiance)"
                )

            texte_concentration_produit = None
            if signal_produit["concentration"] is not None:
                texte_concentration_produit = (
                    "Concentré sur " + str(signal_produit["concentration"]["produit_dominant"]) + " ("
                    + formater_pourcentage(signal_produit["concentration"]["part"] * 100)
                    + " des tickets de ce composant, n=" + str(signal_produit["concentration"]["n"]) + ")"
                )

            texte_elements_consolides_produit = None
            if len(signal_produit["elements_consolides"]) > 0:
                texte_elements_consolides_produit = signal_produit["elements_consolides"][0]
                for element_consolide in signal_produit["elements_consolides"][1:]:
                    texte_elements_consolides_produit = texte_elements_consolides_produit + " · " + element_consolide
                texte_elements_consolides_produit = "Concerne notamment : " + texte_elements_consolides_produit

            texte_regroupement_produit = None
            if signal_produit["regroupement_produit"] is not None:
                n_autres_sujets = len(signal_produit["regroupement_produit"]["autres_sujets"])
                texte_regroupement_produit = (
                    "Voir aussi sur " + signal_produit["regroupement_produit"]["produit"] + " — "
                    + accorder(n_autres_sujets, "autre sujet distinct", "autres sujets distincts")
                    + " cette période : " + " · ".join(signal_produit["regroupement_produit"]["autres_sujets"])
                )

            lignes_meta_produit_principales = [texte_volume_produit]
            candidats_preuve_produit = [texte_csat_produit, texte_cout_produit, texte_concentration_produit]
            for candidat_preuve_produit in candidats_preuve_produit:
                if candidat_preuve_produit is not None and len(lignes_meta_produit_principales) < 3:
                    lignes_meta_produit_principales.append(candidat_preuve_produit)
            if len(lignes_meta_produit_principales) < 3:
                lignes_meta_produit_principales.append(texte_temporalite_produit)

            lignes_meta_produit_detail = []
            for texte_champ_produit in (
                texte_temporalite_produit, texte_csat_produit, texte_cout_produit,
                texte_concentration_produit, texte_elements_consolides_produit, texte_regroupement_produit,
            ):
                if texte_champ_produit is not None and texte_champ_produit not in lignes_meta_produit_principales:
                    lignes_meta_produit_detail.append(texte_champ_produit)

            for ligne_meta_produit in lignes_meta_produit_principales:
                corps_produit_html = corps_produit_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                    + ligne_meta_produit + "</span>"
                )

            # Phase 5 (passe finale, liens contextuels) : "Voir l'impact" uniquement quand un coût a
            # déjà été calculé pour CE signal (signal["cout"], moteur Produit inchangé) -- jamais un
            # lien systématique. Réutilise le même nom d'onglet que la navigation Vue d'ensemble
            # déjà en place ("Impact & confiance"), pas un second mécanisme.
            lien_croise_produit = None
            if signal_produit["cout"] is not None:
                lien_croise_produit = "Voir l'impact →"

            st.markdown(
                construire_carte_signal(
                    titre_html_produit, statut_signal_produit, corps_produit_html,
                    badge=signal_produit["niveau_priorite"], lien_croise=lien_croise_produit,
                ),
                unsafe_allow_html=True,
            )

            if len(lignes_meta_produit_detail) > 0:
                with st.expander("Détail et méthodologie"):
                    for ligne_detail_produit in lignes_meta_produit_detail:
                        st.caption(ligne_detail_produit)

            # ---- F (au niveau carte) : dossiers associés, matchés structurellement (5F.1, section 28-30) ----
            dossiers_associes = construire_dossiers_associes_produit(signal_produit, tickets_sav_produit_s2)
            with st.expander("Dossiers associés (" + str(len(dossiers_associes)) + ")"):
                lignes_dossiers = []
                for ticket_dossier in dossiers_associes:
                    cout_dossier = None
                    type_perte_dossier = type_perte_financiere(ticket_dossier)
                    if type_perte_dossier is not None:
                        cout_dossier = montant_perte_estime(ticket_dossier, commandes, type_perte_dossier, couts_produits)
                    ligne_dossier = {
                        "Ticket": ticket_dossier["ticket_id"],
                        "Produit": ticket_dossier["product_name"],
                        "Composant": ticket_dossier["component"],
                        "Nature du problème": ticket_dossier["issue_type"],
                        "CSAT": formater_csat(ticket_dossier["csat"]) if ticket_dossier["csat"] is not None else "N/A",
                        "Résolution": ticket_dossier["resolution_type"],
                        "Réouvertures": str(ticket_dossier["reopens"]) if ticket_dossier["reopens"] is not None else "N/A",
                        "Coût associé": formater_montant(cout_dossier) if cout_dossier is not None else "Non disponible",
                    }
                    lignes_dossiers.append(ligne_dossier)
                st.dataframe(lignes_dossiers, hide_index=True, width="stretch")

        # Étape 6F, section 8 : Watch déjà en compact row (texte joint, pas de carte) -- ne rivalise
        # pas visuellement avec les priorités ci-dessus. Aucune migration structurelle nécessaire.
        if len(signaux_a_surveiller) > 0:
            texte_a_surveiller = []
            for signal_surveillance in signaux_a_surveiller:
                texte_tag_surveillance_produit = ""
                if comparaison_disponible:
                    texte_evolution_surveillance_produit = _evolution_signal_produit_vs_b(signal_surveillance)
                    if texte_evolution_surveillance_produit is not None:
                        texte_tag_surveillance_produit = " — " + texte_evolution_surveillance_produit
                texte_a_surveiller.append(
                    titre_signal_produit(signal_surveillance) + " (" + str(signal_surveillance["volume"]["n"])
                    + " tickets — " + signal_surveillance["observation_principale"].rstrip(".") + ")"
                    + texte_tag_surveillance_produit
                )
            st.markdown("**À surveiller**")
            st.caption(
                "Convergence encore partielle : ces sujets ne remplissent pas les critères d'une priorité "
                "Produit. " + " · ".join(texte_a_surveiller)
            )

    # ------------------------------------------------------------------
    # E. Dossiers individuels à examiner -- Voie B, toujours séparée de la Voie A (Étape 5F.1,
    # section 27 : même si son produit×composant est aussi une priorité analytique, TKT-109042 reste
    # sa propre carte, jamais fusionné).
    # ------------------------------------------------------------------

    if len(signaux_voie_b) > 0:
        st.markdown(titre_section_principale("Dossiers individuels à examiner"), unsafe_allow_html=True)
        # Étape 6F, section 14 : statut "critique" (liseré, jamais un fond rouge) -- réservé aux cas
        # individuels réellement sensibles, jamais une priorité analytique ordinaire. Le badge
        # "Dossier individuel" rend explicite que ceci n'est PAS un pattern agrégé comme ci-dessus.
        for signal_grave in signaux_voie_b:
            corps_grave_html = str(signal_grave["sujet"]) + " (" + str(signal_grave["produit"]) + ")"
            corps_grave_html = corps_grave_html + (
                '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                "Résolution : " + str(signal_grave["resolution_type"]) + " — CSAT "
                + formater_csat(signal_grave["csat"]) + " — " + signal_grave["raison"] + "</span>"
                '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                + signal_grave["avertissement"] + "</span>"
            )
            st.markdown(
                construire_carte_signal(
                    "Ticket " + str(signal_grave["ticket_id"]), "critique", corps_grave_html,
                    badge="Dossier individuel",
                ),
                unsafe_allow_html=True,
            )

    # ------------------------------------------------------------------
    # Données descriptives partagées par F et G ci-dessous.
    # ------------------------------------------------------------------

    par_composant_s2 = grouper_par(tickets_sav_produit_s2, "component")
    par_composant_s1 = grouper_par(tickets_sav_produit_s1, "component")

    par_issue = grouper_par(tickets_sav_produit_s2, "issue_type")
    par_issue_s1 = grouper_par(tickets_sav_produit_s1, "issue_type")
    issues_produit_evolution_active = comparaison_disponible and produit_duree_comparable

    issues_a_afficher_produit = list(par_issue.keys())
    if issues_produit_evolution_active:
        issues_a_afficher_produit = cles_combinees(par_issue, par_issue_s1)

    lignes_issue = []
    for issue in issues_a_afficher_produit:
        if issue is None:
            continue
        tickets_issue = par_issue.get(issue, [])
        ligne_issue = {"Nature du problème": issue, "Tickets": len(tickets_issue)}
        if issues_produit_evolution_active:
            tickets_issue_s1 = par_issue_s1.get(issue, [])
            ligne_issue["Évolution"] = formater_delta_nombre(len(tickets_issue) - len(tickets_issue_s1))
        lignes_issue.append(ligne_issue)
    lignes_issue_triees = sorted(lignes_issue, key=obtenir_tickets, reverse=True)

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

    par_composant_issue_s1 = {}
    for ticket in tickets_sav_produit_s1:
        composant = ticket["component"]
        issue = ticket["issue_type"]
        if composant is None or issue is None:
            continue
        cle = (composant, issue)
        if cle in par_composant_issue_s1:
            par_composant_issue_s1[cle] = par_composant_issue_s1[cle] + 1
        else:
            par_composant_issue_s1[cle] = 1

    cles_composant_issue_a_afficher = list(par_composant_issue.keys())
    if issues_produit_evolution_active:
        cles_composant_issue_a_afficher = cles_combinees(par_composant_issue, par_composant_issue_s1)

    lignes_composant_issue = []
    for cle in cles_composant_issue_a_afficher:
        nombre = par_composant_issue.get(cle, 0)
        ligne_composant_issue = {"Composant": cle[0], "Nature du problème": cle[1], "Tickets": nombre}
        if issues_produit_evolution_active:
            nombre_s1 = par_composant_issue_s1.get(cle, 0)
            ligne_composant_issue["Évolution"] = formater_delta_nombre(nombre - nombre_s1)
        lignes_composant_issue.append(ligne_composant_issue)
    lignes_composant_issue_triees = sorted(lignes_composant_issue, key=obtenir_tickets, reverse=True)

    lignes_composant_issue_significatives = []
    for ligne in lignes_composant_issue_triees:
        if ligne["Tickets"] >= SEUIL_MINIMUM_SUJET:
            lignes_composant_issue_significatives.append(ligne)

    # ------------------------------------------------------------------
    # F. Explorer les preuves -- nature du problème + combinaisons composant×problème (Étape 5F.1,
    # section 39 : remonté hors du descriptif générique, ce sont des outils d'investigation).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Explorer les preuves"), unsafe_allow_html=True)
    st.caption("component dit où le défaut se situe, issue_type dit ce qui est réellement cassé — les deux ensemble orientent vers le vrai correctif.")

    with st.container(border=True):
        st.dataframe(lignes_issue_triees, hide_index=True, width="stretch")

    st.markdown("**Combinaisons composant × problème à investiguer**")
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

    # ------------------------------------------------------------------
    # G. Vue descriptive Produit -- niveau secondaire, accordéons (Étape 5F.1, section 33).
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Vue descriptive Produit"), unsafe_allow_html=True)
    st.caption("Informations descriptives — ne remplacent pas les priorités ci-dessus.")

    with st.expander("Contacts SAV par composant"):
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
        afficher_tableau_colore(lignes_composant_triees)

    with st.expander("Contacts SAV par produit"):
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
        afficher_tableau_colore(lignes_produit_triees)

    with st.expander("Type de résolution des SAV produit"):
        par_resolution = grouper_par(tickets_sav_produit_s2, "resolution_type")
        lignes_resolution = []
        for resolution, tickets_resolution in par_resolution.items():
            lignes_resolution.append({"Type de résolution": resolution, "Tickets": len(tickets_resolution)})
        lignes_resolution_triees = sorted(lignes_resolution, key=obtenir_tickets, reverse=True)
        st.dataframe(lignes_resolution_triees, hide_index=True, width="stretch")

        texte_resolution = construire_texte_resolution_produit(lignes_resolution_triees, len(tickets_sav_produit_s2))
        if texte_resolution is not None:
            st.caption(texte_resolution)

    with st.expander("Garantie"):
        par_garantie = grouper_par(tickets_sav_produit_s2, "warranty_status")
        lignes_garantie = []
        for garantie, tickets_garantie in par_garantie.items():
            lignes_garantie.append({"Statut garantie": garantie, "Tickets": len(tickets_garantie)})
        st.dataframe(lignes_garantie, hide_index=True, width="stretch")

        insight_garantie = construire_insight_garantie(lignes_garantie, len(tickets_sav_produit_s2))
        if insight_garantie is not None:
            st.caption(insight_garantie)

        st.markdown("**Délai entre achat et signalement SAV**")
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

    with st.expander("Clients avec SAV récurrents"):
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
                construire_texte_sav_recurrents_produit(
                    len(tickets_recurrents), part_recurrents, produit_principal, composant_principal,
                )
            )

            colonne_rec_a, colonne_rec_b = st.columns(2)
            with colonne_rec_a:
                st.dataframe(lignes_produit_recurrent_triees, hide_index=True, width="stretch")
            with colonne_rec_b:
                st.dataframe(lignes_composant_recurrent_triees, hide_index=True, width="stretch")

    with st.expander("Opportunités produit — demandes hors catalogue"):
        st.caption(
            "Demande non satisfaite / opportunité de gamme — pas un défaut SAV, à traiter séparément des "
            "problèmes Produit ci-dessus."
        )
        opportunites = detecter_opportunites_hors_catalogue(tickets_s2, SEUIL_MINIMUM_SUJET)

        if len(opportunites) == 0:
            st.caption(
                "Aucune demande hors catalogue récurrente (au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets) "
                "sur cette période."
            )
        else:
            lignes_opportunites = []
            for sujet, tickets_sujet in opportunites:
                csat_opportunite = moyenne(tickets_sujet, "csat")
                ligne = {"Demande": sujet, "Tickets": len(tickets_sujet), "CSAT": "N/A"}
                if csat_opportunite is not None:
                    ligne["CSAT"] = formater_csat(csat_opportunite)
                lignes_opportunites.append(ligne)

            lignes_opportunites_triees = sorted(lignes_opportunites, key=obtenir_tickets, reverse=True)[:10]
            afficher_tableau_colore(lignes_opportunites_triees)


# ------------------------------------------------------------------
# Onglet 7 : Livraison
# ------------------------------------------------------------------
# Étape 5G.1 : 4C (moteur_livraison_voie_a) est l'unique propriétaire de la priorisation
# analytique Livraison. Les anciens mécanismes locaux concurrents (construire_signal_sujet_
# livraison au grain motif, anomalies_pays au grain pays -- trouvés en audit 5G, section 4 et 6,
# tous deux sur des seuils non alignés avec la convergence 4C) ont été supprimés : les tables
# "Sujets livraison" et "Par pays" ci-dessous restent purement descriptives, elles ne produisent
# plus de caption "signal"/"anomalie"/"à investiguer".

with onglet_livraison:
    st.subheader("Livraison")
    st.caption("Motifs logistiques, conséquences observées, dossiers associés.")

    st.caption(
        "Miroir mensuel de la catégorie Livraison, pensé pour un point avec le transporteur — voir "
        "l'onglet Vue d'ensemble pour la vue hebdomadaire toutes catégories confondues. Cadence mensuelle "
        "recommandée (élargis la Période A dans la barre latérale) — les exports disponibles sont des "
        "semaines représentatives espacées dans le temps, pas un historique continu."
    )

    # Phase 5B (passe finale, segmentation transporteur) : "Tous" reproduit exactement le
    # fonctionnement déjà validé (court-circuit total, aucun filtre appliqué). Noria Standard/Velox
    # Express filtrent le même moteur, sur le même champ transporteur -- jamais un second moteur.
    segment_livraison = st.radio(
        "Transporteur", SEGMENTS_LIVRAISON, horizontal=True, key="segment_livraison",
    )

    tickets_livraison_s2 = filtrer_tickets_par_segment_transporteur(
        categories_s2.get("Livraison", []), segment_livraison
    )
    tickets_livraison_s1 = filtrer_tickets_par_segment_transporteur(
        categories_s1.get("Livraison", []), segment_livraison
    )

    # ---- Moteur Livraison (Étape 4C) : convergence de familles de preuve (demande, expérience,
    # effort, relances, issues, concentration transporteur, persistance) -- jamais le volume seul.
    # Historique = exports STRICTEMENT antérieurs à la Période A, jamais de fuite du futur (même
    # principe que le moteur Produit ci-dessous). Le filtre transporteur est appliqué ICI, au même
    # niveau que le filtre catégoriel Livraison -- jamais seulement sur la période courante, sinon
    # la temporalité comparerait un univers filtré à un historique non filtré (risque identifié en
    # Phase 5B.1).
    NOMBRE_MAX_SIGNAUX_LIVRAISON = 5

    historique_livraison_par_fichier = []
    for date_export_historique_liv, chemin_historique_liv in exports_disponibles:
        if date_export_historique_liv < date_a_debut:
            tickets_fichier_historique_liv = charger_tickets(chemin_historique_liv)
            tickets_livraison_fichier_historique = []
            for ticket_historique_liv in tickets_fichier_historique_liv:
                if categoriser(ticket_historique_liv) == "Livraison":
                    tickets_livraison_fichier_historique.append(ticket_historique_liv)
            historique_livraison_par_fichier.append(
                filtrer_tickets_par_segment_transporteur(tickets_livraison_fichier_historique, segment_livraison)
            )

    contexte_livraison_periode = contexte_periode(evenements_calendrier, date_a_debut, date_a_fin)
    lecture_activite_livraison = construire_lecture_activite_livraison(
        tickets_livraison_s2, tickets_s2, contexte_livraison_periode
    )

    resultats_livraison = moteur_livraison_voie_a(
        tickets_livraison_s2, historique_livraison_par_fichier, NOMBRE_MAX_SIGNAUX_LIVRAISON
    )
    signaux_prioritaires_livraison = resultats_livraison["prioritaires"]
    signaux_a_surveiller_livraison = resultats_livraison["a_surveiller"]

    # ------------------------------------------------------------------
    # Étape 7C -- comparaison A/B Livraison. Réutilise exactement la grammaire Produit (Étape 7B) :
    # RANG_NIVEAU_PRIORITE / evaluer_evolution_signal_vs_b / texte_evolution_signal_vs_b, aucune
    # nouvelle logique de tier. La clé d'identité est directement signal["sujet"] -- Livraison n'a
    # qu'un seul grain (subject_cluster), pas besoin d'un équivalent à cle_signal_produit. B hérite
    # automatiquement du segment transporteur actif : tickets_livraison_s1 est déjà filtré par
    # segment_livraison plus haut, donc Tous/Noria/Velox sont respectés sans logique spéciale ici.
    # ------------------------------------------------------------------

    livraison_duree_comparable = False
    csat_livraison_s1 = None
    n_csat_livraison_s1 = 0
    resolution_livraison_s1 = None
    signaux_prioritaires_b_livraison = []
    signaux_a_surveiller_b_livraison = []

    if comparaison_disponible:
        livraison_duree_comparable = periodes_comparables_en_duree(date_a_debut, date_a_fin, date_b_debut, date_b_fin)

        csat_livraison_s1 = moyenne(tickets_livraison_s1, "csat")
        for ticket_liv_ctx_s1 in tickets_livraison_s1:
            if ticket_liv_ctx_s1["csat"] is not None:
                n_csat_livraison_s1 = n_csat_livraison_s1 + 1
        resolution_livraison_s1 = moyenne(tickets_livraison_s1, "full_resolution_time_hours")

        historique_livraison_par_fichier_b = []
        for date_export_historique_liv_b, chemin_historique_liv_b in exports_disponibles:
            if date_export_historique_liv_b < date_b_debut:
                tickets_fichier_historique_liv_b = charger_tickets(chemin_historique_liv_b)
                tickets_livraison_fichier_historique_b = []
                for ticket_historique_liv_b in tickets_fichier_historique_liv_b:
                    if categoriser(ticket_historique_liv_b) == "Livraison":
                        tickets_livraison_fichier_historique_b.append(ticket_historique_liv_b)
                historique_livraison_par_fichier_b.append(
                    filtrer_tickets_par_segment_transporteur(tickets_livraison_fichier_historique_b, segment_livraison)
                )

        resultats_livraison_b = moteur_livraison_voie_a(
            tickets_livraison_s1, historique_livraison_par_fichier_b, PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        signaux_prioritaires_b_livraison = resultats_livraison_b["prioritaires"]
        signaux_a_surveiller_b_livraison = resultats_livraison_b["a_surveiller"]

    niveau_priorite_par_sujet_b_livraison = {}
    concentration_par_sujet_b_livraison = {}
    for signal_b_livraison in signaux_prioritaires_b_livraison + signaux_a_surveiller_b_livraison:
        niveau_priorite_par_sujet_b_livraison[signal_b_livraison["sujet"]] = signal_b_livraison["niveau_priorite"]
        concentration_par_sujet_b_livraison[signal_b_livraison["sujet"]] = signal_b_livraison["concentration_transporteur"]

    def _evolution_signal_livraison_vs_b(signal):
        niveau_b_livraison = niveau_priorite_par_sujet_b_livraison.get(signal["sujet"])
        qualification_livraison = evaluer_evolution_signal_vs_b(signal["niveau_priorite"], niveau_b_livraison)
        return texte_evolution_signal_vs_b(qualification_livraison)

    # "Ne ressort plus parmi les signaux de A" -- même règle que Produit : le set d'exclusion
    # utilise TOUS les signaux qualifiés de A (plafond retiré), jamais la liste plafonnée à
    # l'affichage, pour ne jamais signaler à tort un motif encore qualifié mais non affiché.
    texte_signaux_disparus_livraison = None
    if comparaison_disponible:
        resultats_livraison_complet = moteur_livraison_voie_a(
            tickets_livraison_s2, historique_livraison_par_fichier, PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        sujets_a_livraison = set()
        for signal_a_livraison in (
            resultats_livraison_complet["prioritaires"] + resultats_livraison_complet["a_surveiller"]
        ):
            sujets_a_livraison.add(signal_a_livraison["sujet"])

        signaux_disparus_livraison = []
        for signal_b_livraison in signaux_prioritaires_b_livraison + signaux_a_surveiller_b_livraison:
            if signal_b_livraison["sujet"] not in sujets_a_livraison:
                signaux_disparus_livraison.append(signal_b_livraison)

        if len(signaux_disparus_livraison) > 0:
            def _rang_disparu_livraison(signal):
                return -RANG_NIVEAU_PRIORITE.get(signal["niveau_priorite"], 0)

            signaux_disparus_livraison_tries = sorted(signaux_disparus_livraison, key=_rang_disparu_livraison)
            noms_disparus_livraison = []
            for signal_disparu_livraison in signaux_disparus_livraison_tries[:2]:
                noms_disparus_livraison.append(signal_disparu_livraison["sujet"])
            verbe_disparu_livraison = accorder(len(noms_disparus_livraison), "ne ressort plus", "ne ressortent plus")
            texte_signaux_disparus_livraison = (
                " · ".join(noms_disparus_livraison) + " " + verbe_disparu_livraison + " parmi les signaux de A."
            )

    # ---- A. Lecture Livraison : juxtapose ACTIVITÉ (poids de Livraison sur la période) et SIGNAL
    # (compteurs 4C), sans jamais fusionner les deux en une seule affirmation causale. ----
    st.markdown(titre_section_principale("Lecture Livraison"), unsafe_allow_html=True)
    texte_lecture_livraison = construire_lecture_livraison(
        lecture_activite_livraison["observation"],
        resultats_livraison["nb_prioritaires_avant_plafond"],
        resultats_livraison["nb_a_surveiller_avant_plafond"],
    )
    if texte_signaux_disparus_livraison is not None:
        texte_lecture_livraison = texte_lecture_livraison + " " + texte_signaux_disparus_livraison
    if lecture_activite_livraison["contexte"] is not None:
        texte_lecture_livraison_html = texte_lecture_livraison + (
            '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
            + lecture_activite_livraison["contexte"] + "</span>"
        )
    else:
        texte_lecture_livraison_html = texte_lecture_livraison
    st.markdown(construire_bandeau_info(texte_lecture_livraison_html), unsafe_allow_html=True)

    # ---- B. Contexte Livraison compact ----
    volume_livraison_s2 = len(tickets_livraison_s2)
    csat_livraison_s2 = moyenne(tickets_livraison_s2, "csat")
    resolution_livraison_s2 = moyenne(tickets_livraison_s2, "full_resolution_time_hours")
    pct_livraison_global = volume_livraison_s2 / len(tickets_s2) * 100

    with st.container(border=True):
        colonne_liv_a, colonne_liv_b, colonne_liv_c = st.columns(3)

        delta_volume_livraison = None
        sous_texte_volume_livraison = formater_pourcentage(pct_livraison_global) + " du volume global"
        if comparaison_disponible:
            if livraison_duree_comparable:
                delta_volume_livraison = formater_delta_nombre(volume_livraison_s2 - len(tickets_livraison_s1))
            else:
                sous_texte_volume_livraison = (
                    sous_texte_volume_livraison + " · B : " + formater_nombre_espace(len(tickets_livraison_s1))
                    + " (durées non comparables)"
                )
        colonne_liv_a.markdown(
            construire_carte_kpi(
                "Tickets livraison", formater_nombre_espace(volume_livraison_s2),
                delta=delta_volume_livraison, delta_couleur="off", sous_texte=sous_texte_volume_livraison,
            ),
            unsafe_allow_html=True,
        )

        if csat_livraison_s2 is not None:
            n_csat_livraison_s2 = 0
            for ticket_liv_ctx_s2 in tickets_livraison_s2:
                if ticket_liv_ctx_s2["csat"] is not None:
                    n_csat_livraison_s2 = n_csat_livraison_s2 + 1
            sous_texte_csat_livraison = "n=" + str(n_csat_livraison_s2)
            delta_csat_livraison = None
            if comparaison_disponible:
                if csat_livraison_s1 is not None:
                    delta_csat_livraison = formater_delta_nombre(csat_livraison_s2 - csat_livraison_s1, decimales=2)
                    sous_texte_csat_livraison = (
                        sous_texte_csat_livraison + " · B : " + formater_csat(csat_livraison_s1)
                        + " (n=" + str(n_csat_livraison_s1) + ")"
                    )
                else:
                    sous_texte_csat_livraison = sous_texte_csat_livraison + " · B : N/A"
            colonne_liv_b.markdown(
                construire_carte_kpi(
                    "CSAT livraison", formater_csat(csat_livraison_s2), sous_texte=sous_texte_csat_livraison,
                    delta=delta_csat_livraison, delta_couleur="normal",
                ),
                unsafe_allow_html=True,
            )

        if resolution_livraison_s2 is not None:
            delta_resolution_livraison = None
            if comparaison_disponible and resolution_livraison_s1 is not None:
                delta_resolution_livraison = formater_delta_duree(
                    (resolution_livraison_s2 - resolution_livraison_s1) * 60
                )
            colonne_liv_c.markdown(
                construire_carte_kpi(
                    "Résolution moyenne", formater_duree(resolution_livraison_s2 * 60),
                    delta=delta_resolution_livraison, delta_couleur="inverse",
                ),
                unsafe_allow_html=True,
            )
    st.caption(TEXTE_COUT_INDISPONIBLE_LIVRAISON)

    # ---- C. Motifs à investiguer (4C, réutilisé sans recalcul) ----
    st.markdown(titre_section_principale("Motifs à investiguer"), unsafe_allow_html=True)
    if len(signaux_prioritaires_livraison) == 0:
        st.caption("Aucun motif ne présente actuellement une convergence suffisante pour être investigué.")
    else:
        st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_CAUSALE), unsafe_allow_html=True)
        # Étape 6F, section 17-18 : même fondation que Produit -- statut "attention" uniquement pour
        # la priorité principale, badge = niveau. Les relances restent en corps principal (taille
        # normale, jamais reléguées en petite légende muted) : c'est la métrique distinctive de
        # Livraison, elle doit rester très lisible. "Piste transporteur" reste secondaire (meta
        # muted), jamais un badge d'alerte -- le badge est réservé au niveau de priorité.
        for signal_livraison in signaux_prioritaires_livraison:
            if signal_livraison["niveau_priorite"] == "Priorité principale":
                statut_signal_livraison = "attention"
            else:
                statut_signal_livraison = None

            corps_livraison_html = signal_livraison["observation_principale"]

            # Étape 7C -- tag de comparaison A/B, même grammaire que Produit, jamais reformulé en
            # termes de transporteur (le motif est comparé, pas le transporteur).
            if comparaison_disponible:
                texte_evolution_livraison = _evolution_signal_livraison_vs_b(signal_livraison)
                if texte_evolution_livraison is not None:
                    corps_livraison_html = corps_livraison_html + (
                        '<br><span style="font-size:12px; font-weight:600; color:' + COULEUR_TEXTE_MUTED + ';">'
                        + texte_evolution_livraison + "</span>"
                    )

            if signal_livraison["relances"]["moyen"] is not None:
                corps_livraison_html = corps_livraison_html + (
                    '<br><span style="font-weight:600;">Relances moyennes : '
                    + str(round(signal_livraison["relances"]["moyen"], 2))
                    + " (référence Livraison " + str(round(signal_livraison["relances"]["reference"], 2)) + ")</span>"
                )

            # Phase 4 (passe finale, mini-histoires) : constat -> relances (déjà en évidence,
            # inchangé, métrique distinctive de Livraison) -> 2 preuves principales choisies pour CE
            # signal (volume toujours, puis résolution priorisée sur CSAT -- cf. consigne, "résolution
            # peut être plus parlant que temporalité") -> investigation (toujours visible, jamais
            # reléguée) -> détail/méthodologie en expander. Rien n'est supprimé : n/références
            # intacts partout où ils existent déjà.
            texte_volume_livraison = (
                str(signal_livraison["volume"]["n"]) + " tickets ("
                + formater_pourcentage(signal_livraison["volume"]["part_univers_pct"])
                + " de Livraison sur la période, univers " + str(signal_livraison["volume"]["univers"]) + ")"
            )
            texte_temporalite_livraison = "Temporalité : " + signal_livraison["temporalite"]

            texte_csat_livraison = None
            if signal_livraison["experience"]["csat"] is not None:
                texte_csat_livraison = (
                    "CSAT : " + formater_csat(signal_livraison["experience"]["csat"])
                    + " (n=" + str(signal_livraison["experience"]["n_csat"]) + ") — "
                    + signal_livraison["experience"]["lecture"]
                )

            texte_resolution_livraison = None
            if signal_livraison["effort"]["resolution_h_moyenne"] is not None:
                texte_resolution_livraison = (
                    "Résolution moyenne : " + formater_duree(signal_livraison["effort"]["resolution_h_moyenne"] * 60)
                    + " (référence " + formater_duree(signal_livraison["effort"]["resolution_h_reference"] * 60) + ")"
                )

            texte_issues_livraison = None
            distribution_livraison = signal_livraison["issues"]["distribution"]
            if len(distribution_livraison) > 0:
                textes_issues = []
                for item_issue in distribution_livraison:
                    textes_issues.append(
                        item_issue["issue"] + " " + formater_pourcentage(item_issue["part_pct"])
                        + " (n=" + str(item_issue["n"]) + ")"
                    )
                texte_issues_livraison = "Issues finales : " + " · ".join(textes_issues)

            texte_transporteur_livraison = None
            texte_prudence_transporteur_livraison = None
            if signal_livraison["concentration_transporteur"] is not None:
                texte_transporteur_livraison = (
                    "Piste transporteur : "
                    + texte_piste_transporteur_livraison(signal_livraison["concentration_transporteur"])
                )
                texte_prudence_transporteur_livraison = signal_livraison["concentration_transporteur"]["prudence_echantillon"]

            # Étape 7C -- comparaison A/B FACTUELLE de la piste transporteur, uniquement en vue
            # "Tous" et uniquement dans le détail (jamais dans le corps principal de la carte,
            # jamais un badge). Purement descriptive (transporteur + part + n de chaque côté) --
            # aucun verdict "renforcé/atténué/dégradé" n'est appliqué à la piste transporteur, cette
            # grammaire reste réservée à l'évolution du signal/motif lui-même. En vue mono-
            # transporteur, concentration_transporteur est déjà None par construction (rien à faire).
            texte_transporteur_ab_livraison = None
            if (
                comparaison_disponible and segment_livraison == SEGMENT_LIVRAISON_TOUS
                and signal_livraison["concentration_transporteur"] is not None
            ):
                concentration_a_livraison = signal_livraison["concentration_transporteur"]
                concentration_b_livraison = concentration_par_sujet_b_livraison.get(signal_livraison["sujet"])
                ligne_transporteur_a_livraison = (
                    "Piste transporteur sur A : " + concentration_a_livraison["transporteur"] + ", "
                    + formater_pourcentage(concentration_a_livraison["part_du_motif_pct"])
                    + " (n=" + str(concentration_a_livraison["n"]) + ")."
                )
                if concentration_b_livraison is not None:
                    ligne_transporteur_b_livraison = (
                        "B : " + concentration_b_livraison["transporteur"] + ", "
                        + formater_pourcentage(concentration_b_livraison["part_du_motif_pct"])
                        + " (n=" + str(concentration_b_livraison["n"]) + ")."
                    )
                else:
                    ligne_transporteur_b_livraison = "Aucune concentration transporteur comparable ne ressort sur B."
                texte_transporteur_ab_livraison = ligne_transporteur_a_livraison + " " + ligne_transporteur_b_livraison

            lignes_meta_livraison_principales = [texte_volume_livraison]
            candidats_preuve_livraison = [texte_resolution_livraison, texte_csat_livraison]
            for candidat_preuve_livraison in candidats_preuve_livraison:
                if candidat_preuve_livraison is not None and len(lignes_meta_livraison_principales) < 2:
                    lignes_meta_livraison_principales.append(candidat_preuve_livraison)

            lignes_meta_livraison_detail = []
            for texte_champ_livraison in (
                texte_temporalite_livraison, texte_resolution_livraison, texte_csat_livraison,
                texte_issues_livraison, texte_transporteur_livraison, texte_prudence_transporteur_livraison,
                texte_transporteur_ab_livraison,
            ):
                if texte_champ_livraison is not None and texte_champ_livraison not in lignes_meta_livraison_principales:
                    lignes_meta_livraison_detail.append(texte_champ_livraison)

            for ligne_meta_livraison in lignes_meta_livraison_principales:
                corps_livraison_html = corps_livraison_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                    + ligne_meta_livraison + "</span>"
                )

            corps_livraison_html = corps_livraison_html + (
                '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                + signal_livraison["action_investigation"] + "</span>"
            )

            # Phase 5 (passe finale, liens contextuels) : pas de "Voir l'impact" ici -- signal_livraison
            # ["cout"] est toujours None (outils.py, moteur Livraison : "jamais calculable actuellement
            # -- aucun order_id sur les tickets Livraison"). Documenté plutôt que forcé : un lien vers
            # Impact & confiance ne serait pas fiable tant que cette limite structurelle existe.
            st.markdown(
                construire_carte_signal(
                    signal_livraison["sujet"], statut_signal_livraison, corps_livraison_html,
                    badge=signal_livraison["niveau_priorite"],
                ),
                unsafe_allow_html=True,
            )

            if len(lignes_meta_livraison_detail) > 0:
                with st.expander("Détail et méthodologie"):
                    for ligne_detail_livraison in lignes_meta_livraison_detail:
                        st.caption(ligne_detail_livraison)

            # ---- Dossiers associés : matching structurel exact sur le grain motif (subject_cluster) ----
            dossiers_associes_livraison = construire_dossiers_associes_livraison(signal_livraison, tickets_livraison_s2)
            with st.expander("Dossiers associés (" + str(len(dossiers_associes_livraison)) + ")"):
                lignes_dossiers_livraison = []
                for ticket_dossier_livraison in dossiers_associes_livraison:
                    resolution_dossier_livraison = ticket_dossier_livraison["full_resolution_time_hours"]
                    ligne_dossier_livraison = {
                        "Ticket": ticket_dossier_livraison["ticket_id"],
                        "Transporteur": (
                            ticket_dossier_livraison["transporteur"]
                            if ticket_dossier_livraison["transporteur"] else "N/A"
                        ),
                        "Pays": ticket_dossier_livraison["country"],
                        "Relances": (
                            str(ticket_dossier_livraison["nombre_relances"])
                            if ticket_dossier_livraison["nombre_relances"] is not None else "N/A"
                        ),
                        "CSAT": (
                            formater_csat(ticket_dossier_livraison["csat"])
                            if ticket_dossier_livraison["csat"] is not None else "N/A"
                        ),
                        "Résolution": (
                            formater_duree(resolution_dossier_livraison * 60)
                            if resolution_dossier_livraison is not None else "N/A"
                        ),
                        "Issue finale": (
                            ticket_dossier_livraison["issue_livraison_finale"]
                            if ticket_dossier_livraison["issue_livraison_finale"] else "N/A"
                        ),
                    }
                    lignes_dossiers_livraison.append(ligne_dossier_livraison)
                st.dataframe(lignes_dossiers_livraison, hide_index=True, width="stretch")

    # ---- D. À surveiller (compact, indépendant du nombre de priorités) ----
    if len(signaux_a_surveiller_livraison) > 0:
        texte_a_surveiller_livraison = []
        for signal_surveillance_livraison in signaux_a_surveiller_livraison:
            texte_tag_surveillance_livraison = ""
            if comparaison_disponible:
                texte_evolution_surveillance_livraison = _evolution_signal_livraison_vs_b(signal_surveillance_livraison)
                if texte_evolution_surveillance_livraison is not None:
                    texte_tag_surveillance_livraison = " — " + texte_evolution_surveillance_livraison
            texte_a_surveiller_livraison.append(
                signal_surveillance_livraison["sujet"] + " (" + str(signal_surveillance_livraison["volume"]["n"])
                + " tickets — " + signal_surveillance_livraison["observation_principale"].rstrip(".") + ")"
                + texte_tag_surveillance_livraison
            )
        st.caption("À surveiller (preuve encore partielle) : " + " · ".join(texte_a_surveiller_livraison))

    # ---- E. Sujets sans signal particulier ----
    if len(resultats_livraison["sujets_silencieux"]) > 0:
        st.caption(
            "Sujets sans signal particulier cette période : " + " · ".join(resultats_livraison["sujets_silencieux"])
        )

    anomalies_qualite_livraison = controler_qualite_donnees_livraison(tickets_livraison_s2)
    if len(anomalies_qualite_livraison) > 0:
        with st.expander("Anomalies de qualité de données détectées"):
            for anomalie in anomalies_qualite_livraison:
                st.caption(anomalie)

    # ---- F. Explorer les conséquences : distribution globale des issues + croisement motif x issue
    # (relances incluses) -- réutilise distribution_issues_livraison (verrouillé 4C) et une simple
    # agrégation par motif, jamais un nouveau moteur, jamais utilisé pour trancher une priorité. ----
    st.markdown(titre_section_principale("Explorer les conséquences"), unsafe_allow_html=True)

    distribution_globale_livraison = distribution_issues_livraison(tickets_livraison_s2)
    if len(distribution_globale_livraison) > 0:
        texte_issues_globales = []
        for item_issue_globale in distribution_globale_livraison:
            texte_issues_globales.append(
                item_issue_globale["issue"] + " " + formater_pourcentage(item_issue_globale["part_pct"])
                + " (n=" + str(item_issue_globale["n"]) + ")"
            )
        st.caption("Issues finales sur l'ensemble de Livraison : " + " · ".join(texte_issues_globales))

    croisement_motif_issue_livraison = construire_croisement_motif_issue_livraison(tickets_livraison_s2)
    dict_croisement_a_livraison = {}
    for ligne_a_croisement in croisement_motif_issue_livraison:
        dict_croisement_a_livraison[ligne_a_croisement["sujet"]] = ligne_a_croisement

    croisement_evolution_active_livraison = comparaison_disponible and livraison_duree_comparable
    dict_croisement_b_livraison = {}
    if croisement_evolution_active_livraison:
        for ligne_b_croisement in construire_croisement_motif_issue_livraison(tickets_livraison_s1):
            dict_croisement_b_livraison[ligne_b_croisement["sujet"]] = ligne_b_croisement

    sujets_croisement_a_afficher = list(dict_croisement_a_livraison.keys())
    if croisement_evolution_active_livraison:
        sujets_croisement_a_afficher = cles_combinees(dict_croisement_a_livraison, dict_croisement_b_livraison)

    lignes_croisement_livraison = []
    for sujet_croisement in sujets_croisement_a_afficher:
        ligne_croisement = dict_croisement_a_livraison.get(sujet_croisement)
        n_a_croisement = ligne_croisement["n"] if ligne_croisement is not None else 0
        ligne_croisement_affichee = {
            "Sujet": sujet_croisement,
            "Tickets": n_a_croisement,
            "Relances moyennes": "N/A",
            "Issue principale": "N/A",
        }
        if ligne_croisement is not None:
            if ligne_croisement["relances_moyennes"] is not None:
                ligne_croisement_affichee["Relances moyennes"] = str(round(ligne_croisement["relances_moyennes"], 2))
            if ligne_croisement["issue_principale"] is not None:
                ligne_croisement_affichee["Issue principale"] = (
                    ligne_croisement["issue_principale"]
                    + " (" + formater_pourcentage(ligne_croisement["part_issue_principale_pct"]) + ")"
                )
        if croisement_evolution_active_livraison:
            ligne_b_croisement = dict_croisement_b_livraison.get(sujet_croisement)
            n_b_croisement = ligne_b_croisement["n"] if ligne_b_croisement is not None else 0
            ligne_croisement_affichee["Évolution"] = formater_delta_nombre(n_a_croisement - n_b_croisement)
        lignes_croisement_livraison.append(ligne_croisement_affichee)

    lignes_croisement_livraison_triees = sorted(lignes_croisement_livraison, key=obtenir_tickets, reverse=True)
    with st.expander("Détail par motif : relances et issue principale", expanded=False):
        afficher_tableau_colore(lignes_croisement_livraison_triees)

    # ---- G. Vue descriptive secondaire : tables purement descriptives, jamais de caption
    # "signal"/"anomalie" (mécanismes locaux concurrents supprimés en 5G.1, voir audit 5G section 4/6) ----
    st.markdown(titre_section_principale("Vue descriptive secondaire"), unsafe_allow_html=True)

    sujets_livraison_s2 = grouper_par(tickets_livraison_s2, "subject_cluster")
    sujets_livraison_s1 = grouper_par(tickets_livraison_s1, "subject_cluster")

    if comparaison_disponible:
        sujets_livraison_a_afficher = cles_combinees(sujets_livraison_s2, sujets_livraison_s1)
    else:
        sujets_livraison_a_afficher = list(sujets_livraison_s2.keys())

    lignes_livraison = []
    for sujet in sujets_livraison_a_afficher:
        tickets_sujet_s2 = sujets_livraison_s2.get(sujet, [])
        volume_s2 = len(tickets_sujet_s2)
        csat_sujet = moyenne(tickets_sujet_s2, "csat")
        resolution_sujet = moyenne(tickets_sujet_s2, "full_resolution_time_hours")
        pct_sujet_global = volume_s2 / len(tickets_s2) * 100

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
            if livraison_duree_comparable:
                volume_s1 = len(sujets_livraison_s1.get(sujet, []))
                ligne["Évolution"] = formater_delta_nombre(volume_s2 - volume_s1)
            else:
                ligne["Évolution"] = "Non comparable"

        lignes_livraison.append(ligne)

    lignes_livraison_triees = sorted(lignes_livraison, key=obtenir_tickets, reverse=True)
    with st.expander("Sujets livraison — détail", expanded=False):
        afficher_tableau_colore(lignes_livraison_triees)

    par_pays_livraison = grouper_par(tickets_livraison_s2, "country")
    lignes_pays_livraison = []
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

    lignes_pays_livraison_triees = sorted(lignes_pays_livraison, key=obtenir_tickets, reverse=True)
    with st.expander("Par pays — détail", expanded=False):
        st.caption(
            "Le transporteur est unique sur toute la zone de livraison — un écart marqué sur un pays isole un "
            "problème logistique local plutôt qu'un souci transporteur global."
        )
        afficher_tableau_colore(lignes_pays_livraison_triees)


# ------------------------------------------------------------------
# Onglet 8 : Avant-vente & conversion
# ------------------------------------------------------------------

with onglet_conversion:
    st.subheader("Avant-vente")
    # Étape 6F, section 3 : "parcours d'achat observés", jamais le vocabulaire causal de conversion
    # (déjà tranché en 5H.1 -- le renommage d'onglet et ce libellé restent cohérents).
    st.caption("Parcours de contact, opportunités à investiguer, achats observés après contact.")

    tickets_avant_vente = categories_s2.get("Avant-vente / conseil", [])
    index_commandes_email = commandes_par_email(commandes)

    # ---- Moteur Avant-vente (Étape 4D) : parcours de contact, opportunités par motif, achats
    # observés. Historique = exports STRICTEMENT antérieurs à la Période A, jamais de fuite du futur
    # (même principe que Produit/Livraison ci-dessus). Achats résolus une seule fois par commande
    # réelle (resoudre_achats_observes_avant_vente) -- jamais la même commande recréditée à plusieurs
    # contacts rapprochés du même client. Étape 5H.1 : 4D devient l'unique propriétaire de
    # l'attribution -- l'ancienne logique locale non déduplicuée (premiere_commande_apres) a été
    # retirée de cet onglet (audit 5H, section 4 et 34 : elle alimentait un KPI "Taux de conversion"
    # et une table "Conversion par agent et par pays" tous deux fondés sur une base non robuste).
    historique_avant_vente_par_fichier = []
    for date_export_historique_av, chemin_historique_av in exports_disponibles:
        if date_export_historique_av < date_a_debut:
            tickets_fichier_historique_av = charger_tickets(chemin_historique_av)
            tickets_av_fichier_historique = []
            for ticket_historique_av in tickets_fichier_historique_av:
                if categoriser(ticket_historique_av) == "Avant-vente / conseil":
                    tickets_av_fichier_historique.append(ticket_historique_av)
            historique_avant_vente_par_fichier.append(tickets_av_fichier_historique)

    contexte_avant_vente_periode = contexte_periode(evenements_calendrier, date_a_debut, date_a_fin)
    lecture_activite_av = construire_lecture_activite_avant_vente(
        tickets_avant_vente, tickets_s2, contexte_avant_vente_periode
    )

    resultats_achats_av = resoudre_achats_observes_avant_vente(
        tickets_avant_vente, index_commandes_email, FENETRE_CONVERSION_JOURS
    )
    parcours_av = analyser_parcours_rdv(tickets_avant_vente, resultats_achats_av)

    NOMBRE_MAX_SIGNAUX_AVANT_VENTE = 5
    resultats_motifs_av = moteur_avant_vente_motifs(
        tickets_avant_vente, resultats_achats_av, historique_avant_vente_par_fichier,
        contexte_avant_vente_periode, NOMBRE_MAX_SIGNAUX_AVANT_VENTE,
    )

    # ------------------------------------------------------------------
    # Étape 7D -- comparaison A/B Avant-vente. Réutilise strictement la grammaire Produit/Livraison
    # (RANG_NIVEAU_PRIORITE étendu avec "Opportunité à investiguer", voir outils.py -- aucune
    # nouvelle logique de tier). Clé d'identité = signal["sujet"] (grain unique, comme Livraison).
    # Taux d'achat observé / panier / délai sont des RATIOS (dénominateur contact ou achat, jamais
    # un volume brut) -- pas de gate de comparabilité de durée pour ces trois-là, contrairement aux
    # volumes bruts (Contacts Avant-vente, RDV conseil) qui la respectent comme Produit/Livraison.
    # ------------------------------------------------------------------

    tickets_avant_vente_s1 = categories_s1.get("Avant-vente / conseil", [])
    av_duree_comparable = False
    parcours_av_b = None
    resultats_opportunites_b_av = []
    resultats_a_surveiller_b_av = []

    if comparaison_disponible:
        av_duree_comparable = periodes_comparables_en_duree(date_a_debut, date_a_fin, date_b_debut, date_b_fin)

        resultats_achats_av_b = resoudre_achats_observes_avant_vente(
            tickets_avant_vente_s1, index_commandes_email, FENETRE_CONVERSION_JOURS
        )
        parcours_av_b = analyser_parcours_rdv(tickets_avant_vente_s1, resultats_achats_av_b)

        contexte_avant_vente_periode_b = contexte_periode(evenements_calendrier, date_b_debut, date_b_fin)

        historique_avant_vente_par_fichier_b = []
        for date_export_historique_av_b, chemin_historique_av_b in exports_disponibles:
            if date_export_historique_av_b < date_b_debut:
                tickets_fichier_historique_av_b = charger_tickets(chemin_historique_av_b)
                tickets_av_fichier_historique_b = []
                for ticket_historique_av_b in tickets_fichier_historique_av_b:
                    if categoriser(ticket_historique_av_b) == "Avant-vente / conseil":
                        tickets_av_fichier_historique_b.append(ticket_historique_av_b)
                historique_avant_vente_par_fichier_b.append(tickets_av_fichier_historique_b)

        resultats_motifs_av_b = moteur_avant_vente_motifs(
            tickets_avant_vente_s1, resultats_achats_av_b, historique_avant_vente_par_fichier_b,
            contexte_avant_vente_periode_b, PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        resultats_opportunites_b_av = resultats_motifs_av_b["opportunites"]
        resultats_a_surveiller_b_av = resultats_motifs_av_b["a_surveiller"]

    niveau_par_sujet_b_av = {}
    for signal_b_av in resultats_opportunites_b_av + resultats_a_surveiller_b_av:
        niveau_par_sujet_b_av[signal_b_av["sujet"]] = signal_b_av["niveau"]

    def _evolution_signal_av_vs_b(signal):
        niveau_b_av = niveau_par_sujet_b_av.get(signal["sujet"])
        qualification_av = evaluer_evolution_signal_vs_b(signal["niveau"], niveau_b_av)
        return texte_evolution_signal_vs_b(qualification_av)

    # "Ne ressort plus parmi les signaux de A" -- même mécanique uncapped que Produit/Livraison :
    # le set d'exclusion de A utilise TOUS les signaux qualifiés (plafond retiré), jamais la liste
    # plafonnée à l'affichage.
    texte_signaux_disparus_av = None
    if comparaison_disponible:
        resultats_motifs_av_complet = moteur_avant_vente_motifs(
            tickets_avant_vente, resultats_achats_av, historique_avant_vente_par_fichier,
            contexte_avant_vente_periode, PLAFOND_SIGNAUX_COMPARAISON_B,
        )
        sujets_a_av = set()
        for signal_a_av in resultats_motifs_av_complet["opportunites"] + resultats_motifs_av_complet["a_surveiller"]:
            sujets_a_av.add(signal_a_av["sujet"])

        signaux_disparus_av = []
        for signal_b_av in resultats_opportunites_b_av + resultats_a_surveiller_b_av:
            if signal_b_av["sujet"] not in sujets_a_av:
                signaux_disparus_av.append(signal_b_av)

        if len(signaux_disparus_av) > 0:
            def _rang_disparu_av(signal):
                return -RANG_NIVEAU_PRIORITE.get(signal["niveau"], 0)

            signaux_disparus_av_tries = sorted(signaux_disparus_av, key=_rang_disparu_av)
            noms_disparus_av = []
            for signal_disparu_av in signaux_disparus_av_tries[:2]:
                noms_disparus_av.append(signal_disparu_av["sujet"])
            verbe_disparu_av = accorder(len(noms_disparus_av), "ne ressort plus", "ne ressortent plus")
            texte_signaux_disparus_av = (
                " · ".join(noms_disparus_av) + " " + verbe_disparu_av + " parmi les signaux de A."
            )

    # ---- A. Lecture Avant-vente : juxtapose ACTIVITÉ et SIGNAL, sans les fusionner. ----
    st.markdown(titre_section_principale("Lecture Avant-vente"), unsafe_allow_html=True)
    texte_lecture_av = construire_lecture_avant_vente(
        lecture_activite_av["observation"],
        resultats_motifs_av["nb_opportunites_avant_plafond"],
        resultats_motifs_av["nb_a_surveiller_avant_plafond"],
    )
    if texte_signaux_disparus_av is not None:
        texte_lecture_av = texte_lecture_av + " " + texte_signaux_disparus_av
    if lecture_activite_av["contexte"] is not None:
        texte_lecture_av_html = texte_lecture_av + (
            '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
            + lecture_activite_av["contexte"] + "</span>"
        )
    else:
        texte_lecture_av_html = texte_lecture_av
    st.markdown(construire_bandeau_info(texte_lecture_av_html), unsafe_allow_html=True)

    # ---- B. Contexte compact (2 KPI -- volume brut, jamais "conversion") ----
    volume_av_total = len(tickets_avant_vente)
    pct_av_global = 0
    if len(tickets_s2) > 0:
        pct_av_global = volume_av_total / len(tickets_s2) * 100

    with st.container(border=True):
        colonne_ctx_a, colonne_ctx_b = st.columns(2)

        delta_volume_av = None
        sous_texte_volume_av = formater_pourcentage(pct_av_global) + " du volume global"
        if comparaison_disponible:
            if av_duree_comparable:
                delta_volume_av = formater_delta_nombre(volume_av_total - len(tickets_avant_vente_s1))
            else:
                sous_texte_volume_av = (
                    sous_texte_volume_av + " · B : " + formater_nombre_espace(len(tickets_avant_vente_s1))
                    + " (durées non comparables)"
                )
        colonne_ctx_a.markdown(
            construire_carte_kpi(
                "Contacts Avant-vente", formater_nombre_espace(volume_av_total),
                delta=delta_volume_av, delta_couleur="off", sous_texte=sous_texte_volume_av,
            ),
            unsafe_allow_html=True,
        )
        sous_texte_rdv_av = (
            formater_pourcentage(parcours_av["rdv_demandes"] / volume_av_total * 100) + " de l'Avant-vente"
            if volume_av_total > 0 else None
        )
        delta_rdv_av = None
        if comparaison_disponible and parcours_av_b is not None:
            if av_duree_comparable:
                delta_rdv_av = formater_delta_nombre(parcours_av["rdv_demandes"] - parcours_av_b["rdv_demandes"])
            else:
                note_rdv_av = "B : " + formater_nombre_espace(parcours_av_b["rdv_demandes"]) + " (durées non comparables)"
                if sous_texte_rdv_av is not None:
                    sous_texte_rdv_av = sous_texte_rdv_av + " · " + note_rdv_av
                else:
                    sous_texte_rdv_av = note_rdv_av
        colonne_ctx_b.markdown(
            construire_carte_kpi(
                "RDV conseil", formater_nombre_espace(parcours_av["rdv_demandes"]),
                delta=delta_rdv_av, delta_couleur="off", sous_texte=sous_texte_rdv_av,
            ),
            unsafe_allow_html=True,
        )

    # ---- C. Parcours observés (RDV honoré / annulé-no-show / spontané) ----
    # Étape 6F, section 23-24 : présentation comparative neutre -- 3 mini metric cards (même
    # construire_carte_kpi que partout ailleurs, jamais d'accent), pas des Signal cards. Aucune
    # couleur gagnant/perdant : "RDV annulé / no-show" à 31,9 % ne doit pas paraître plus "gagnant"
    # que "RDV honoré" à 28,7 % -- les 3 cartes partagent rigoureusement le même traitement visuel.
    st.markdown(titre_section_principale("Parcours observés"), unsafe_allow_html=True)

    # Étape 7D -- B référencé en une seule ligne de sous-texte compacte (taux uniquement, jamais
    # panier/délai qui alourdiraient les 3 cartes déjà denses). delta_couleur="off" partout : le
    # principe "aucune couleur gagnant/perdant" déjà en place sur ces 3 cartes s'applique aussi à B.
    stats_b_par_nom_parcours_av = {}
    if parcours_av_b is not None:
        stats_b_par_nom_parcours_av = {
            "RDV honoré": parcours_av_b["stats_rdv_honore"],
            "RDV annulé / no-show": parcours_av_b["stats_rdv_non_honore"],
            "Contact spontané": parcours_av_b["stats_spontane"],
        }

    with st.container(border=True):
        colonnes_parcours_av = st.columns(3)
        index_colonne_parcours_av = 0
        for nom_parcours_av, stats_parcours_av in (
            ("RDV honoré", parcours_av["stats_rdv_honore"]),
            ("RDV annulé / no-show", parcours_av["stats_rdv_non_honore"]),
            ("Contact spontané", parcours_av["stats_spontane"]),
        ):
            if stats_parcours_av["n_contacts"] > 0:
                delta_parcours_av = None
                if stats_parcours_av["taux_pct"] is not None:
                    valeur_parcours_av = formater_pourcentage(stats_parcours_av["taux_pct"])
                    sous_texte_parcours_av = "achat observé, n=" + str(stats_parcours_av["n_contacts"]) + " contacts"
                    if comparaison_disponible:
                        stats_b_parcours_av = stats_b_par_nom_parcours_av.get(nom_parcours_av)
                        if stats_b_parcours_av is not None and stats_b_parcours_av["taux_pct"] is not None:
                            delta_parcours_av = formater_delta_points(
                                stats_parcours_av["taux_pct"] - stats_b_parcours_av["taux_pct"]
                            )
                            sous_texte_parcours_av = sous_texte_parcours_av + (
                                " · B : " + formater_pourcentage(stats_b_parcours_av["taux_pct"])
                                + " (n=" + str(stats_b_parcours_av["n_contacts"]) + ")"
                            )
                else:
                    valeur_parcours_av = str(stats_parcours_av["n_contacts"])
                    sous_texte_parcours_av = accorder(stats_parcours_av["n_contacts"], "contact", "contacts")

                if stats_parcours_av["panier_moyen"] is not None:
                    sous_texte_parcours_av = sous_texte_parcours_av + (
                        " · panier " + formater_montant(stats_parcours_av["panier_moyen"])
                        + " (n=" + str(stats_parcours_av["n_panier"]) + ") · délai "
                        + str(round(stats_parcours_av["delai_moyen"], 1)) + " j"
                    )

                colonnes_parcours_av[index_colonne_parcours_av].markdown(
                    construire_carte_kpi(
                        nom_parcours_av, valeur_parcours_av, delta=delta_parcours_av, delta_couleur="off",
                        sous_texte=sous_texte_parcours_av,
                    ),
                    unsafe_allow_html=True,
                )
            index_colonne_parcours_av = index_colonne_parcours_av + 1

        st.caption(parcours_av["conclusion"])
        st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_CAUSALE), unsafe_allow_html=True)

        contacts_avant_achat_av = parcours_av["contacts_avant_achat"]
        if contacts_avant_achat_av is not None:
            st.caption(
                "Contacts Avant-vente avant l'achat (mêmes " + str(FENETRE_CONVERSION_JOURS) + " jours que "
                "l'attribution) : en moyenne " + str(round(contacts_avant_achat_av["nombre_moyen_contacts_avant_achat"], 2))
                + " (médiane " + str(round(contacts_avant_achat_av["nombre_median_contacts_avant_achat"], 1)) + "), "
                + formater_pourcentage(contacts_avant_achat_av["part_plusieurs_contacts_pct"])
                + " des achats observés avaient plusieurs contacts avant l'achat (n="
                + str(contacts_avant_achat_av["n_achats_credites"]) + " achats observés)."
            )

    # ---- D. Opportunités à investiguer (4C, réutilisé sans recalcul) + Contacts/Achats associés ----
    st.markdown(titre_section_principale("Opportunités à investiguer"), unsafe_allow_html=True)
    if len(resultats_motifs_av["opportunites"]) == 0:
        st.caption("Aucune opportunité ne se détache sur cette période avec les critères actuels.")
    else:
        # Étape 6F, section 6-25 : même fondation Signal card. Un seul niveau existe ici ("Opportunité
        # à investiguer", tier unique -- pas de principal/secondaire comme Produit/Livraison), donc
        # statut "attention" uniforme et badge = signal_av["niveau"] tel quel.
        st.markdown(construire_note_methodologique(TEXTE_PRUDENCE_CAUSALE), unsafe_allow_html=True)
        for signal_av in resultats_motifs_av["opportunites"]:
            corps_av_html = signal_av["observation_principale"]

            # Étape 7D -- tag de comparaison A/B, même grammaire que Produit/Livraison. Décrit
            # uniquement le passage entre niveaux produits par LE MOTEUR (jamais inféré d'un taux
            # d'achat, panier, volume ou CSAT).
            if comparaison_disponible:
                texte_evolution_av = _evolution_signal_av_vs_b(signal_av)
                if texte_evolution_av is not None:
                    corps_av_html = corps_av_html + (
                        '<br><span style="font-size:12px; font-weight:600; color:' + COULEUR_TEXTE_MUTED + ';">'
                        + texte_evolution_av + "</span>"
                    )

            # Phase 4 (passe finale, mini-histoires) : constat -> 2-3 preuves principales pour CE
            # signal (volume et achat observé -- avec sa référence -- toujours présents car ce sont
            # les deux faits qui font qu'un motif Avant-vente mérite l'attention ; panier ou CSAT
            # complète selon ce qui existe) -> investigation (piste_investigation, toujours visible)
            # -> détail/méthodologie en expander.
            texte_volume_av = (
                str(signal_av["volume"]["n"]) + " tickets ("
                + formater_pourcentage(signal_av["volume"]["part_univers_pct"])
                + " d'Avant-vente sur la période, univers " + str(signal_av["volume"]["univers"]) + ")"
            )
            texte_temporalite_av = "Temporalité : " + signal_av["temporalite"]
            texte_achat_observe_av = (
                "Achat observé : " + formater_pourcentage(signal_av["achat_observe"]["taux_pct"])
                + " des contacts (n=" + str(signal_av["achat_observe"]["n_contacts"]) + "), contre "
                + formater_pourcentage(signal_av["achat_observe_reference_pct"]) + " en référence Avant-vente"
            )

            texte_panier_av = None
            if signal_av["achat_observe"]["panier_moyen"] is not None:
                texte_panier_av = (
                    "Panier observé moyen : " + formater_montant(signal_av["achat_observe"]["panier_moyen"])
                    + " (n=" + str(signal_av["achat_observe"]["n_panier"]) + ")"
                )

            texte_csat_av = None
            if signal_av["experience"]["csat"] is not None:
                texte_csat_av = (
                    "CSAT : " + formater_csat(signal_av["experience"]["csat"])
                    + " (n=" + str(signal_av["experience"]["n_csat"]) + ")"
                )

            texte_contexte_av = signal_av["contexte"]

            lignes_meta_av_principales = [texte_volume_av, texte_achat_observe_av]
            candidats_preuve_av = [texte_panier_av, texte_csat_av]
            for candidat_preuve_av in candidats_preuve_av:
                if candidat_preuve_av is not None and len(lignes_meta_av_principales) < 3:
                    lignes_meta_av_principales.append(candidat_preuve_av)

            lignes_meta_av_detail = []
            for texte_champ_av in (texte_temporalite_av, texte_panier_av, texte_csat_av, texte_contexte_av):
                if texte_champ_av is not None and texte_champ_av not in lignes_meta_av_principales:
                    lignes_meta_av_detail.append(texte_champ_av)

            for ligne_meta_av in lignes_meta_av_principales:
                corps_av_html = corps_av_html + (
                    '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">' + ligne_meta_av + "</span>"
                )

            corps_av_html = corps_av_html + (
                '<br><span style="font-size:12px; color:' + COULEUR_TEXTE_MUTED + ';">'
                + signal_av["piste_investigation"] + "</span>"
            )

            st.markdown(
                construire_carte_signal(signal_av["sujet"], "attention", corps_av_html, badge=signal_av["niveau"]),
                unsafe_allow_html=True,
            )

            if len(lignes_meta_av_detail) > 0:
                with st.expander("Détail et méthodologie"):
                    for ligne_detail_av in lignes_meta_av_detail:
                        st.caption(ligne_detail_av)

            # ---- G (au niveau carte) : contacts associés + achats associés, matchés
            # structurellement (grain subject_cluster), source unique = resultats_achats_av ----
            contacts_associes_av = construire_contacts_associes_avant_vente(signal_av, resultats_achats_av)
            achats_associes_av = construire_achats_associes_avant_vente(contacts_associes_av)

            with st.expander("Contacts associés (" + str(len(contacts_associes_av)) + ")"):
                lignes_contacts_av = []
                for ticket_contact_av, commande_contact_av, plusieurs_contact_av in contacts_associes_av:
                    parcours_ticket_av = "Contact spontané"
                    if ticket_contact_av["type_contact_avant_vente"] == "RDV conseil":
                        parcours_ticket_av = "RDV " + str(ticket_contact_av["rdv_statut"]).lower()
                    achat_observe_texte = "Non"
                    delai_texte_av = "N/A"
                    if commande_contact_av is not None:
                        achat_observe_texte = "Oui"
                        delai_texte_av = str(
                            (commande_contact_av["order_date"] - ticket_contact_av["created_at"]).days
                        ) + " j"
                    lignes_contacts_av.append({
                        "Ticket": ticket_contact_av["ticket_id"],
                        "Date contact": ticket_contact_av["created_at"],
                        "Parcours": parcours_ticket_av,
                        "Canal": ticket_contact_av["via_channel"],
                        "Achat observé": achat_observe_texte,
                        "Délai commande": delai_texte_av,
                    })
                st.dataframe(lignes_contacts_av, hide_index=True, width="stretch")

            # Étape 6F, section 27 : "Commandes attribuées (n)" si disponible -- même logique
            # visuelle que Produit/Livraison, contenu différent. Montant reste descriptif (aucune
            # couleur suggérant une vente "réussie", section 28).
            if len(achats_associes_av) > 0:
                with st.expander("Commandes attribuées (" + str(len(achats_associes_av)) + ")"):
                    lignes_achats_av = []
                    for ticket_achat_av, commande_achat_av in achats_associes_av:
                        lignes_achats_av.append({
                            "Commande": commande_achat_av["order_id"],
                            "Date": commande_achat_av["order_date"],
                            "Contact attribué": ticket_achat_av["ticket_id"],
                            "Produit": commande_achat_av["product_name"],
                            "Montant": formater_montant(commande_achat_av["montant_total"]),
                            "Délai depuis contact": str(
                                (commande_achat_av["order_date"] - ticket_achat_av["created_at"]).days
                            ) + " j",
                        })
                    st.dataframe(lignes_achats_av, hide_index=True, width="stretch")

    # ---- E. À surveiller (compact, indépendant du nombre d'opportunités) ----
    if len(resultats_motifs_av["a_surveiller"]) > 0:
        texte_a_surveiller_av = []
        for signal_surveillance_av in resultats_motifs_av["a_surveiller"]:
            texte_tag_surveillance_av = ""
            if comparaison_disponible:
                texte_evolution_surveillance_av = _evolution_signal_av_vs_b(signal_surveillance_av)
                if texte_evolution_surveillance_av is not None:
                    texte_tag_surveillance_av = " — " + texte_evolution_surveillance_av
            texte_a_surveiller_av.append(
                signal_surveillance_av["sujet"] + " (" + str(signal_surveillance_av["volume"]["n"]) + " tickets — "
                + signal_surveillance_av["observation_principale"].rstrip(".") + ")"
                + texte_tag_surveillance_av
            )
        st.caption("À surveiller (preuve encore partielle) : " + " · ".join(texte_a_surveiller_av))

    # ---- F. Sujets sans signal particulier ----
    if len(resultats_motifs_av["sujets_silencieux"]) > 0:
        st.caption(
            "Motifs sans signal particulier cette période : " + " · ".join(resultats_motifs_av["sujets_silencieux"])
        )

    anomalies_qualite_av = controler_qualite_donnees_avant_vente(
        tickets_avant_vente, [t for t in tickets_s2 if categoriser(t) != "Avant-vente / conseil"]
    )
    if len(anomalies_qualite_av) > 0:
        with st.expander("Anomalies de qualité de données détectées"):
            for anomalie_av in anomalies_qualite_av:
                st.caption(anomalie_av)

    st.caption(
        "Les achats sont attribués uniquement lorsqu'ils surviennent dans les " + str(FENETRE_CONVERSION_JOURS)
        + " jours après un contact Avant-vente éligible — un achat en dehors de cette fenêtre reste hors "
        "périmètre d'attribution, sans être compté comme un contact sans achat."
    )

    # ---- H. Vue descriptive secondaire : canaux (descriptif uniquement -- jamais de comparaison
    # d'achat observé par canal, le téléphone étant confondu avec le parcours RDV), sujets, pays.
    # Jamais de croisement agent x pays (retiré en 5H.1, voir audit 5H section 34). ----
    st.markdown(titre_section_principale("Vue descriptive secondaire"), unsafe_allow_html=True)

    distribution_canal_av = distribution_canal_avant_vente(tickets_avant_vente)
    with st.expander("Par canal", expanded=False):
        lignes_canal_av = []
        for item_canal_av in distribution_canal_av:
            lignes_canal_av.append({
                "Canal": item_canal_av["canal"],
                "Tickets": item_canal_av["n"],
                "% de l'Avant-vente": formater_pourcentage(item_canal_av["part_pct"]),
            })
        afficher_tableau_colore(lignes_canal_av)

    table_sujets_av = construire_table_sujets_avant_vente(tickets_avant_vente, resultats_achats_av)
    lignes_sujets_av = []
    for ligne_sujet_av in table_sujets_av:
        achat_texte_sujet = "N/A"
        if ligne_sujet_av["achat_observe_pct"] is not None:
            achat_texte_sujet = formater_pourcentage(ligne_sujet_av["achat_observe_pct"])
        panier_texte_sujet = "N/A"
        if ligne_sujet_av["panier_moyen"] is not None:
            panier_texte_sujet = formater_montant(ligne_sujet_av["panier_moyen"])
        lignes_sujets_av.append({
            "Sujet": ligne_sujet_av["sujet"],
            "Tickets": ligne_sujet_av["n"],
            "Achat observé": achat_texte_sujet,
            "Panier moyen observé": panier_texte_sujet,
        })
    lignes_sujets_av_triees = sorted(lignes_sujets_av, key=obtenir_tickets, reverse=True)
    with st.expander("Par sujet", expanded=False):
        afficher_tableau_colore(lignes_sujets_av_triees)

    table_pays_av = construire_table_pays_avant_vente(tickets_avant_vente, resultats_achats_av)
    lignes_pays_av = []
    for ligne_pays_av in table_pays_av:
        achat_texte_pays = "N/A"
        if ligne_pays_av["achat_observe_pct"] is not None:
            achat_texte_pays = formater_pourcentage(ligne_pays_av["achat_observe_pct"])
        lignes_pays_av.append({
            "Pays": ligne_pays_av["pays"],
            "Tickets": ligne_pays_av["n"],
            "Achat observé": achat_texte_pays,
        })
    lignes_pays_av_triees = sorted(lignes_pays_av, key=obtenir_tickets, reverse=True)
    with st.expander("Par pays", expanded=False):
        afficher_tableau_colore(lignes_pays_av_triees)


# FENETRE_NPS_EXPERIENCE_JOURS / SEUIL_RESOLUTION_RAPIDE_H / SEUIL_PRUDENCE_ECHANTILLON_NPS vivent
# désormais dans outils.py (source unique, Étape 4E) -- importées ci-dessus.


def _texte_composition_nps(composition):
    return (
        "n=" + str(composition["n"]) + " · Promoteurs " + str(round(composition["part_promoteurs_pct"]))
        + "% / Passifs " + str(round(composition["part_passifs_pct"])) + "% / Détracteurs "
        + str(round(composition["part_detracteurs_pct"])) + "%"
    )


# Un ticket récurrent (le client a déjà eu au moins un SAV avant) pointe vers un défaut
# structurel qu'un correctif produit peut prévenir — "potentiellement évitable". Un incident
# isolé (accident de transport, mauvaise manipulation ponctuelle...) reste un "coût subi" : rien
# n'indique qu'une action corrective l'aurait empêché. Simplification assumée, pas une vérité
# absolue — documentée comme telle dans l'UI.
def est_cout_potentiellement_evitable(ticket):
    return ticket.get("prior_sav_count") is not None and ticket["prior_sav_count"] >= 1


# ------------------------------------------------------------------
# Onglet 9 : Impact & confiance
# ------------------------------------------------------------------

with onglet_impact:
    st.subheader("Impact & confiance")
    st.caption("Ce que disent réellement les données disponibles sur la confiance client et l'impact financier -- avec quel niveau de prudence.")

    # ---- Calculs : coût direct (moteur de coût inchangé, Étape 5I : sain) ----
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

    # ---- Calculs : SAV sous garantie ----
    tickets_sav_produit_business = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_garantie = []
    for ticket in tickets_sav_produit_business:
        if ticket["warranty_status"] == "Sous garantie":
            tickets_garantie.append(ticket)

    pct_garantie_volume_sav = None
    montants_garantie = []
    montant_garantie_total = 0
    if len(tickets_sav_produit_business) > 0 and len(tickets_garantie) > 0:
        pct_garantie_volume_sav = len(tickets_garantie) / len(tickets_sav_produit_business) * 100

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

    # ---- Calculs : NPS calé sur la PÉRIODE SÉLECTIONNÉE (Étape 5I.1 -- corrige le bug identifié en
    # 5I : l'ancienne "Lecture de confiance" utilisait toujours index_dernier_mois = len(historique)-1,
    # indépendamment de la période choisie dans la barre latérale. Même principe de calage que Vue
    # d'ensemble (5A, verrouillé, non modifié ici) : identifier_observation_nps_periode ne renvoie
    # jamais un mois approximatif -- absent si aucune correspondance exacte, jamais de repli. ----
    reponses_nps = charger_nps(FICHIER_NPS)
    index_tickets_email = tickets_par_email(tickets_historique_business)
    composition_globale_nps = calculer_composition_nps(reponses_nps)

    item_nps = None
    texte_alignement_periode = None
    texte_prudence_periode = None
    texte_sensibilite_periode = None
    historique_nps_mensuel = []
    historique_nps_borne = []

    if composition_globale_nps is not None:
        historique_nps_mensuel = construire_historique_nps_par_mois(reponses_nps)

        tickets_par_mois_care = {}
        for ticket in tickets_historique_business:
            cle_mois_ticket = ticket["created_at"].strftime("%Y-%m")
            if cle_mois_ticket in tickets_par_mois_care:
                tickets_par_mois_care[cle_mois_ticket].append(ticket)
            else:
                tickets_par_mois_care[cle_mois_ticket] = [ticket]

        historique_care_mensuel = []
        for item_mois in historique_nps_mensuel:
            historique_care_mensuel.append(
                construire_profil_care_mensuel(tickets_par_mois_care.get(item_mois["cle_mois"], []))
            )

        historique_n_mensuel = []
        for item_mois in historique_nps_mensuel:
            historique_n_mensuel.append(item_mois["n"])

        index_mois_nps = identifier_observation_nps_periode(historique_nps_mensuel, date_a_debut)

        if index_mois_nps is not None:
            item_nps = historique_nps_mensuel[index_mois_nps]
            historique_nps_borne = historique_nps_mensuel[:index_mois_nps + 1]

            alignement_periode = evaluer_alignement_care_nps(
                historique_nps_mensuel, historique_care_mensuel, index_mois_nps
            )
            if alignement_periode is not None:
                texte_alignement_periode = texte_alignement_care_nps(
                    alignement_periode, historique_care_mensuel[index_mois_nps], "cette période",
                )

            etat_prudence_periode = evaluer_prudence_echantillon_nps(historique_n_mensuel, index_mois_nps)
            texte_prudence_periode = texte_prudence_echantillon_nps(etat_prudence_periode, item_nps["n"])
            texte_sensibilite_periode = texte_sensibilite_echantillon_nps(etat_prudence_periode)

    # ---- A. Lecture Impact & confiance ----
    # L'alignement n'est jamais passé ici : la section D ci-dessous en est l'unique affichage
    # (Étape 5I.1, section 15/16 -- corrige la duplication identifiée en 5I entre "Lecture de
    # confiance" et "Alignement avec les autres signaux Care", qui répétaient le même texte).
    st.markdown(titre_section_principale("Lecture Impact & confiance"), unsafe_allow_html=True)
    st.markdown(
        construire_bandeau_info(
            construire_lecture_impact_confiance(item_nps, None, montant_total_pertes, montant_evitable)
        ),
        unsafe_allow_html=True,
    )

    # ---- B. Contexte compact (max 3 KPI -- jamais un total combiné Coût direct + Garantie) ----
    kpis_contexte_impact = []
    if item_nps is not None:
        kpis_contexte_impact.append((
            "NPS de la période", formater_nps_entier(item_nps["nps"]),
            str(item_nps["n"]) + " " + accorder(item_nps["n"], "réponse", "réponses"),
        ))
    if montant_total_pertes > 0:
        kpis_contexte_impact.append(("Coût direct observé / estimé", formater_montant(montant_total_pertes), None))
    if montant_garantie_total > 0:
        kpis_contexte_impact.append(("Coût garantie estimé", formater_montant(montant_garantie_total), None))

    if len(kpis_contexte_impact) == 0:
        st.caption("Aucune donnée exploitable pour cette période.")
    else:
        with st.container(border=True):
            colonnes_contexte_impact = st.columns(len(kpis_contexte_impact))
            for index_kpi_impact in range(len(kpis_contexte_impact)):
                label_kpi_impact, valeur_kpi_impact, sous_texte_kpi_impact = kpis_contexte_impact[index_kpi_impact]
                colonnes_contexte_impact[index_kpi_impact].markdown(
                    construire_carte_kpi(label_kpi_impact, valeur_kpi_impact, sous_texte=sous_texte_kpi_impact),
                    unsafe_allow_html=True,
                )
        if montant_total_pertes > 0 and montant_garantie_total > 0:
            st.caption(TEXTE_CAVEAT_RECOUVREMENT_COUT)

    # ---- C. Confiance client ----
    st.markdown(titre_section_principale("Confiance client"), unsafe_allow_html=True)
    if composition_globale_nps is None:
        st.caption("Aucune réponse NPS disponible dans le fichier.")
    elif item_nps is None:
        st.caption("Aucune donnée NPS exploitable pour cette période.")
    else:
        # La prudence d'échantillon est toujours énoncée avant/avec le NPS lui-même (Étape 4E.1).
        st.write(texte_prudence_periode)
        if texte_sensibilite_periode is not None:
            st.caption(texte_sensibilite_periode)
        st.markdown(
            construire_carte_kpi(
                "NPS", formater_nps_entier(item_nps["nps"]),
                sous_texte=str(item_nps["n"]) + " " + accorder(item_nps["n"], "réponse", "réponses"),
            ),
            unsafe_allow_html=True,
        )
        st.write(
            "Promoteurs " + str(item_nps["composition"]["n_promoteurs"]) + " / Passifs "
            + str(item_nps["composition"]["n_passifs"]) + " / Détracteurs "
            + str(item_nps["composition"]["n_detracteurs"])
        )

    # ---- D. Alignement / divergence 4E (affiché UNE SEULE FOIS -- Étape 5I.1, section 15) ----
    if composition_globale_nps is not None and item_nps is not None:
        st.markdown(titre_section_principale("Alignement avec les autres signaux Care"), unsafe_allow_html=True)
        st.caption(
            "Compare la position du NPS de la période dans l'historique disponible à celle du CSAT et des "
            "indicateurs d'effort (relances, résolution) du même mois — une coïncidence temporelle "
            "observée, jamais une explication démontrée."
        )
        if texte_alignement_periode is not None:
            # Étape 6H, section 11-12 : statut selon le TYPE produit par 4E (jamais recalculé) --
            # alignement négatif = "attention" (signal à investiguer), positif = "positive" (accent
            # léger, jamais une grande carte verte), divergence = neutre (information analytique,
            # pas une anomalie -- même traitement que "Contrastes" en Tendances, Étape 6E).
            if alignement_periode["type"] == "alignement_negatif":
                statut_alignement_periode = "attention"
            elif alignement_periode["type"] == "alignement_positif":
                statut_alignement_periode = "positive"
            else:
                statut_alignement_periode = None
            st.markdown(
                construire_carte_signal(None, statut_alignement_periode, texte_alignement_periode),
                unsafe_allow_html=True,
            )
        else:
            st.caption("Aucun signal d'alignement ou de divergence notable pour cette période.")

    # ---- E. Impact financier ----
    st.markdown(titre_section_principale("Impact financier"), unsafe_allow_html=True)
    st.caption(
        "Remboursement = montant réellement remboursé. Remplacement et garantie = coût de revient "
        "produit + logistique associée, pas le prix de vente payé par le client. Geste commercial "
        "reste une fraction estimée du prix de vente — seule ligne encore une estimation, marquée "
        "comme telle ci-dessous. Chaque commande n'est comptée qu'une seule fois même si plusieurs "
        "tickets s'y rattachent."
    )
    with st.container(border=True):
        st.dataframe(lignes_perte_triees, hide_index=True, width="stretch")

    if montant_total_pertes > 0 and montant_evitable > 0:
        st.caption(
            "Dont potentiellement évitable : " + formater_montant(montant_evitable) + " ("
            + formater_pourcentage(montant_evitable / montant_total_pertes * 100) + " du coût — SAV récurrents)."
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

    if len(montants_garantie) > 0:
        st.markdown("**SAV sous garantie**")
        st.caption(
            "Impact économique du SAV pris en charge par l'entreprise — le détail produit/composant est "
            "dans l'onglet Produit, pas répété ici."
        )
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
        cout_moyen_garantie = montant_garantie_total / len(tickets_garantie)
        cout_moyen_global = None
        if len(commandes_deja_comptees) > 0:
            cout_moyen_global = montant_total_pertes / len(commandes_deja_comptees)

        if cout_moyen_global is not None and cout_moyen_global > 0:
            ecart_cout_moyen_pct = (cout_moyen_garantie - cout_moyen_global) / cout_moyen_global * 100
            if ecart_cout_moyen_pct >= 50:
                st.caption(
                    "Coût moyen par ticket sous garantie : " + formater_montant(cout_moyen_garantie)
                    + ", contre " + formater_montant(cout_moyen_global) + " en moyenne sur l'ensemble des "
                    "incidents chiffrés — un ticket garantie coûte structurellement plus cher (remplacement "
                    "complet à la charge de l'entreprise, pas de part payée par le client)."
                )

        st.caption(TEXTE_CAVEAT_RECOUVREMENT_COUT)

    # ---- F. Méthodologie / couverture ----
    with st.expander("Comment lire ces données"):
        st.markdown(
            "- **NPS** : toujours accompagné du nombre de répondants (n) — un score sans n peut être "
            "trompeur, surtout sur un petit échantillon.\n"
            "- **Petit échantillon** : " + TEXTE_SENSIBILITE_PETIT_ECHANTILLON_NPS + "\n"
            "- **Association ≠ causalité** : tout rapprochement entre NPS et expérience Care reste une "
            "coïncidence temporelle observée, jamais une explication démontrée.\n"
            "- **Réel vs estimé** : remboursement et remplacement/garantie sont des coûts réels (coût de "
            "revient produit + logistique) ; le geste commercial reste une fraction estimée du prix de "
            "vente, faute de montant réellement accordé enregistré par ticket.\n"
            "- **« Potentiellement évitable »** : approximation basée sur l'existence d'un SAV antérieur "
            "chez le même client (`prior_sav_count`) — une heuristique documentée, pas une preuve.\n"
            "- **Commande manquante** : les montants nécessitant une commande ne sont calculés que "
            "lorsqu'un identifiant commande exploitable est disponible — une commande manquante n'est "
            "jamais comptée comme un coût nul, et n'est jamais comptée deux fois si plusieurs tickets "
            "s'y rattachent.\n"
            "- **" + TEXTE_CAVEAT_RECOUVREMENT_COUT + "**"
        )

    # ---- G. Vue descriptive secondaire (NPS toutes périodes disponibles, pas limité à la période
    # sélectionnée -- contexte méthodologique, jamais la lecture principale de la page) ----
    st.markdown(titre_section_principale("Vue descriptive secondaire"), unsafe_allow_html=True)

    if composition_globale_nps is not None:
        with st.expander("NPS par contact Care identifié", expanded=False):
            st.caption(
                "Toutes les réponses NPS disponibles (pas limité à la période sélectionnée). « Contact "
                "Care identifié » = un ticket du même client a été retrouvé dans les "
                + str(FENETRE_NPS_EXPERIENCE_JOURS) + " jours précédant la réponse NPS (rapprochement par "
                "email et fenêtre temporelle, avec le ticket le plus récent avant la réponse)."
            )
            segmentation_care_nps = segmenter_nps_par_contact_care(
                reponses_nps, index_tickets_email, FENETRE_NPS_EXPERIENCE_JOURS
            )
            composition_avec_contact = segmentation_care_nps["contact_identifie"]["composition"]
            composition_sans_contact = segmentation_care_nps["aucun_contact_identifie"]["composition"]

            colonne_nps_a, colonne_nps_b, colonne_nps_c = st.columns(3)
            colonne_nps_a.markdown(
                construire_carte_kpi(
                    "NPS global (toutes périodes)", formater_nps_entier(composition_globale_nps["nps"]),
                    sous_texte=_texte_composition_nps(composition_globale_nps),
                ),
                unsafe_allow_html=True,
            )
            if composition_avec_contact is not None:
                colonne_nps_b.markdown(
                    construire_carte_kpi(
                        "NPS - contact Care identifié", formater_nps_entier(composition_avec_contact["nps"]),
                        sous_texte=_texte_composition_nps(composition_avec_contact),
                    ),
                    unsafe_allow_html=True,
                )
            if composition_sans_contact is not None:
                colonne_nps_c.markdown(
                    construire_carte_kpi(
                        "NPS - aucun contact Care identifié", formater_nps_entier(composition_sans_contact["nps"]),
                        sous_texte=_texte_composition_nps(composition_sans_contact),
                    ),
                    unsafe_allow_html=True,
                )
            st.caption(TEXTE_PRUDENCE_BIAIS_SELECTION)

        with st.expander("Confiance par type d'expérience", expanded=False):
            st.caption("Toutes les réponses NPS disponibles (pas limité à la période sélectionnée).")
            resultats_type_experience = analyser_nps_par_type_experience(
                reponses_nps, index_tickets_email, FENETRE_NPS_EXPERIENCE_JOURS, SEUIL_PRUDENCE_ECHANTILLON_NPS
            )

            def obtenir_repondants_type_experience(ligne):
                return ligne["Répondants"]

            lignes_experience = []
            for resultat_type in resultats_type_experience:
                lignes_experience.append({
                    "Type d'expérience": resultat_type["type_experience"],
                    "NPS": formater_nps_entier(resultat_type["composition"]["nps"]),
                    "Répondants": resultat_type["composition"]["n"],
                })

            if len(lignes_experience) == 0:
                st.caption(
                    "Échantillon insuffisant par type d'expérience (seuil de prudence : "
                    + str(SEUIL_PRUDENCE_ECHANTILLON_NPS) + " répondants) pour une comparaison robuste actuellement."
                )
            else:
                lignes_experience_triees = sorted(lignes_experience, key=obtenir_repondants_type_experience, reverse=True)
                st.dataframe(lignes_experience_triees, hide_index=True, width="stretch")
                st.caption(
                    "Lecture contextuelle uniquement — ces populations sont structurellement différentes "
                    "(un client SAV n'a pas la même expérience de base qu'un client jamais recontacté) : "
                    "pas un classement des catégories de contact."
                )

        with st.expander("Historique NPS", expanded=False):
            if len(historique_nps_borne) == 0:
                st.caption("Aucune observation NPS disponible jusqu'à cette période.")
            else:
                lignes_nps_mois = []
                for item_mois in historique_nps_borne:
                    lignes_nps_mois.append({
                        "Mois": item_mois["cle_mois"], "NPS": round(item_mois["nps"]), "Réponses": item_mois["n"],
                    })
                tableau_nps_mois = pd.DataFrame(lignes_nps_mois)
                ligne_zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
                    color=COULEUR_NEUTRE_TEXTE, strokeDash=[3, 3]
                ).encode(y=alt.Y("y:Q", title=None))
                graphique_nps = alt.Chart(tableau_nps_mois).mark_line(point=True, color=COULEUR_SECONDAIRE).encode(
                    x=alt.X("Mois:O", title=None),
                    y=alt.Y("NPS:Q", scale=alt.Scale(domain=[-100, 100])),
                    tooltip=["Mois:N", "NPS:Q", "Réponses:Q"],
                ).properties(height=260)
                st.altair_chart(
                    configurer_apparence_graphique(ligne_zero + graphique_nps), width="stretch"
                )

                # n rendu directement lisible (pas seulement au survol) -- Étape 5I.1, section 30.
                textes_n_mois = []
                for ligne_n_mois in lignes_nps_mois:
                    textes_n_mois.append(str(ligne_n_mois["Mois"]) + " n=" + str(ligne_n_mois["Réponses"]))
                st.caption("Réponses par mois : " + " · ".join(textes_n_mois))

                historique_n_borne = []
                for item_mois in historique_nps_borne:
                    historique_n_borne.append(item_mois["n"])
                mois_prudence = []
                for index_mois in range(len(historique_nps_borne)):
                    etat_mois = evaluer_prudence_echantillon_nps(historique_n_borne, index_mois)
                    if etat_mois == ETAT_PRUDENCE_VOLUME_FAIBLE:
                        mois_prudence.append(historique_nps_borne[index_mois]["cle_mois"])
                if len(mois_prudence) > 0:
                    st.caption(
                        "Volume de réponses nettement inférieur aux observations environnantes (à l'époque) sur : "
                        + ", ".join(mois_prudence) + " — à lire avec prudence avant toute lecture positive ou négative."
                    )

        with st.expander("Verbatims et limites des données NPS", expanded=False):
            st.caption(
                "Le fichier NPS ne contient aucun champ de texte libre (verbatim) — seulement un score, une "
                "date, un email et l'indicateur déclaratif « a contacté le support ». Aucun verbatim n'est "
                "donc affiché ici : limitation du dataset, pas un choix de présentation. Pour la même raison, "
                "aucun comparatif NPS « avant/après contact » individuel n'est possible (le fichier ne "
                "contient qu'une seule mesure par réponse, pas une paire avant/après) — la section "
                "« NPS par contact Care identifié » ci-dessus reste une comparaison de groupes, jamais un "
                "effet individuel démontré."
            )
