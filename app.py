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
    montant_perte_estime,
    montant_cout_garantie,
    formater_montant,
    formater_nombre_espace,
    commandes_par_email,
    premiere_commande_apres,
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
    "(voir l'onglet Staffing & réactivité pour le détail du planning et du hors créneau)."
)

ROLE_RESPONSABLE_EQUIPE = "Responsable d'équipe"


def formater_plage(date_debut, date_fin):
    if date_debut == date_fin:
        return date_debut.strftime("%d/%m/%Y")
    return date_debut.strftime("%d/%m/%Y") + " → " + date_fin.strftime("%d/%m/%Y")


NOMS_MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def formater_mois_annee(annee, mois):
    return NOMS_MOIS[mois - 1] + " " + str(annee)


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


def afficher_tableau_colore(lignes, colonne_figee=None):
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


HEURE_DEBUT_GRILLE = 7
HEURE_FIN_GRILLE = 22


def construire_grille_couverture(planning, agents_grille):
    grille = {}
    for nom_jour, numero_jour in JOURS_ORDRE:
        ligne_jour = {}
        for heure in range(HEURE_DEBUT_GRILLE, HEURE_FIN_GRILLE):
            ligne_jour[heure] = 0
        grille[nom_jour] = ligne_jour

    for agent in agents_grille:
        horaires_grille = horaires_agent(planning, agent)
        for nom_jour, numero_jour in JOURS_ORDRE:
            plages = horaires_grille.get(numero_jour, [])
            for debut, fin in plages:
                for heure in range(HEURE_DEBUT_GRILLE, HEURE_FIN_GRILLE):
                    if debut <= heure < fin:
                        grille[nom_jour][heure] = grille[nom_jour][heure] + 1

    return grille


def couleur_fond_couverture(nombre_agents):
    if nombre_agents == 0:
        return "background-color: #f7c6c2"
    elif nombre_agents == 1:
        return "background-color: #ffe8a1"
    else:
        return "background-color: #c6f0d2"


def afficher_grille_couverture(grille):
    colonnes_heures = []
    for heure in range(HEURE_DEBUT_GRILLE, HEURE_FIN_GRILLE):
        colonnes_heures.append(str(heure) + "h")

    lignes_grille = []
    for nom_jour, numero_jour in JOURS_ORDRE:
        ligne = {"Jour": nom_jour}
        for heure in range(HEURE_DEBUT_GRILLE, HEURE_FIN_GRILLE):
            ligne[str(heure) + "h"] = grille[nom_jour][heure]
        lignes_grille.append(ligne)

    tableau_grille = pd.DataFrame(lignes_grille).set_index("Jour")
    tableau_grille_stylise = tableau_grille.style.map(couleur_fond_couverture, subset=colonnes_heures)
    st.dataframe(tableau_grille_stylise, width="stretch")


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
COULEUR_ACCENT_CRITIQUE = "#D1483B"
COULEUR_ACCENT_DEBORDEMENT = "#8B2E24"


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
        bordure_gauche = "border-left:3px solid " + accent + ";"

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


DOSSIER_EXPORTS = os.path.join(DOSSIER_PROJET, "exports_hebdomadaires")
FICHIER_SHOPIFY = os.path.join(DOSSIER_PROJET, "data_shopify", "commandes_shopify_fictif.xlsx")
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


st.sidebar.header("Période à afficher")
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

etendre_a = st.sidebar.checkbox("Étendre sur plusieurs semaines", value=False, key="etendre_a")

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
periode_texte = formater_plage(date_a_debut, date_a_fin)

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

    etendre_b = st.sidebar.checkbox("Étendre sur plusieurs semaines (B)", value=False, key="etendre_b")

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
    agents_s1_liste = list(grouper_par(tickets_s1, "assignee").keys())
    agents_s2_liste = list(grouper_par(tickets_s2, "assignee").keys())
    changements_planning = detecter_changements_planning(agents_s1_liste, agents_s2_liste, planning_s1_dernier, planning_s2_dernier)

st.caption(periode_texte)
if comparer and not comparaison_disponible:
    st.caption("Aucun export disponible sur la période B choisie — pas de comparaison possible.")

with st.sidebar.expander("🎨 Comment lire les couleurs", expanded=True):
    st.markdown(
        "🟢 **Vert** — OK / Correct / Excellent / Fort potentiel : rien à faire\n\n"
        "🟡 **Jaune** — À surveiller / Potentiel moyen : à garder à l'œil\n\n"
        "🔴 **Rouge** — Critique / Débordement / Risque de perte du prospect : action recommandée\n\n"
        "🔵 **Bleu** — Nouveau : sujet apparu depuis la période précédente\n\n"
        "⚪ **Gris** — Disparu : sujet qui n'apparaît plus sur la période actuelle"
    )
    st.caption("CSAT noté sur une échelle de 0 à 5.")

categories_s1 = grouper_par_categorie(tickets_s1)
categories_s2 = grouper_par_categorie(tickets_s2)

# Chargés une seule fois ici (au lieu de dans un onglet) car utilisés à la fois par
# "Conversion & acquisition" et "Impact & confiance" — éviter de recharger deux fois.
commandes = charger_commandes(FICHIER_SHOPIFY)

fichiers_tous_business = []
for date_export_hist, chemin_hist in exports_disponibles:
    fichiers_tous_business.append(chemin_hist)
tickets_historique_business = charger_periode(fichiers_tous_business)

# Chargé ici (au lieu de dans un onglet) car utilisé à la fois par "Agents" et "Staffing & réactivité".
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
        "Alertes & suggestions", "Staffing & réactivité", "Produit", "Livraison",
        "Conversion & acquisition", "Impact & confiance",
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
        st.subheader("L'entreprise (fictive)")
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
        st.subheader("Ce que fait cet outil")
        st.markdown(
            "- Suivi de la performance support à la semaine, au mois, au trimestre ou à l'année\n"
            "- Alertes automatiques : SLA, satisfaction, staffing par créneau horaire\n"
            "- Suggestions de macros/FAQ à créer, basées sur les irritants récurrents\n"
            "- Volet business : conversion avant-vente, coûts SAV, confiance client (NPS), "
            "opportunités produit hors catalogue"
        )

        st.subheader("Comment lire les onglets")
        st.markdown(
            "Les onglets suivent la cadence à laquelle chaque sujet se pilote réellement, "
            "pas un ordre arbitraire :\n"
            "- **Vue d'ensemble → Alertes** : pilotage hebdomadaire de l'équipe (catégories incluses)\n"
            "- **Staffing & réactivité** : couverture horaire, SLA, planning de l'équipe\n"
            "- **Produit** : cadence trimestrielle (usure, défauts récurrents)\n"
            "- **Livraison** : cadence mensuelle, pensé pour un point avec le transporteur\n"
            "- **Conversion & acquisition** : conversion réelle après contact avant-vente\n"
            "- **Impact & confiance** : coûts SAV, confiance client (NPS)\n\n"
            "Les tableaux utilisent un code couleur (vert/jaune/rouge/bleu/gris) — légende "
            "dans la barre latérale."
        )

    st.divider()
    st.caption(
        "Toutes les données (tickets, commandes, avis NPS) sont générées aléatoirement pour cette "
        "démonstration — les chiffres n'ont aucune valeur réelle."
    )

    with st.expander("Limites connues de cette démo"):
        st.markdown(
            "- **Pertes financières** : estimées via une fraction du prix de vente selon le type de "
            "résolution (remboursement intégral, remplacement/geste commercial à coût partiel) — une "
            "approximation illustrative, pas un chiffre comptable réel.\n"
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

    with st.container(border=True):
        colonne1, colonne2, colonne3, colonne4 = st.columns(4)

        if comparaison_disponible:
            nombre_s1 = len(tickets_s1)
            csat_s1 = moyenne(tickets_s1, "csat")
            frt_s1 = moyenne(tickets_s1, "first_reply_time_min")
            macro_s1 = taux_rempli(tickets_s1, "macro_applied")

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

    st.markdown(titre_section_principale("Répartition par famille"), unsafe_allow_html=True)
    if comparaison_disponible:
        st.caption("Barres groupées : volume par catégorie sur les deux périodes, avec l'évolution en %")

    if comparaison_disponible:
        categories_a_afficher = cles_combinees(categories_s2, categories_s1)
    else:
        categories_a_afficher = list(categories_s2.keys())

    lignes_categories_apercu = []
    for categorie in categories_a_afficher:
        tickets_cat = categories_s2.get(categorie, [])
        lignes_categories_apercu.append({"Catégorie": categorie, "Tickets": len(tickets_cat)})

    lignes_categories_apercu_triees = sorted(lignes_categories_apercu, key=obtenir_tickets, reverse=True)

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

    for ligne in lignes_categories_apercu_triees:
        categorie = ligne["Catégorie"]
        tickets_cat_s2 = categories_s2.get(categorie, [])
        tickets_cat_s1 = categories_s1.get(categorie, [])

        with st.expander(categorie + " — " + str(ligne["Tickets"]) + " tickets"):
            sujets_cat_s2 = grouper_par(tickets_cat_s2, "subject_cluster")
            sujets_cat_s1 = grouper_par(tickets_cat_s1, "subject_cluster")

            if comparaison_disponible:
                sujets_a_afficher = cles_combinees(sujets_cat_s2, sujets_cat_s1)
            else:
                sujets_a_afficher = list(sujets_cat_s2.keys())

            lignes_sujets_cat = []
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

                lignes_sujets_cat.append(ligne_sujet)

            lignes_sujets_cat_triees = sorted(lignes_sujets_cat, key=obtenir_tickets, reverse=True)
            afficher_tableau_colore(lignes_sujets_cat_triees)

    st.divider()
    st.markdown(titre_section_principale("Performance par catégorie"), unsafe_allow_html=True)
    st.caption(DEFINITION_EN_CRENEAU)

    lignes_categories = []

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
            en_creneau_cat, pause_cat, hors_cat = separer_creneau(tickets_cat_s2, planning_s2)
            frt_en_creneau_cat = moyenne(en_creneau_cat, "first_reply_time_min")
            pct_hors_creneau_cat = (len(pause_cat) + len(hors_cat)) / len(tickets_cat_s2) * 100
        else:
            frt_en_creneau_cat = None
            pct_hors_creneau_cat = None

        ligne = {"Catégorie": categorie}

        if comparaison_disponible:
            ligne["Volume période précédente"] = len(tickets_cat_s1)

        ligne["Volume période actuelle"] = len(tickets_cat_s2)
        ligne["CSAT"] = "N/A"
        ligne["1re réponse (en créneau)"] = "N/A"
        ligne["Niveau réponse"] = ""
        ligne["% hors créneau"] = formater_pourcentage(pct_hors_creneau_cat)
        ligne["Utilisation macro (%)"] = formater_pourcentage(macro_cat_s2)
        ligne["Niveau utilisation macro"] = niveau_macro(macro_cat_s2)

        if csat_cat_s2 is not None:
            ligne["CSAT"] = formater_csat(csat_cat_s2)

        if frt_en_creneau_cat is not None:
            ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_cat)
            ligne["Niveau réponse"] = niveau_reponse_ouvree(frt_en_creneau_cat)

        lignes_categories.append(ligne)

    with st.container(border=True):
        afficher_tableau_colore(lignes_categories)


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

    st.markdown(titre_section_principale("Volume de tickets"), unsafe_allow_html=True)
    graphique_volume = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Tickets:Q"),
        tooltip=["Date:T", "Tickets:Q", "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_volume, width="stretch")

    st.subheader("CSAT moyen")
    graphique_csat = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_SECONDAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("CSAT:Q", scale=alt.Scale(domain=[1, 5])),
        tooltip=["Date:T", alt.Tooltip("CSAT:Q", format=".2f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_csat, width="stretch")

    st.subheader("Temps de 1re réponse moyen")
    graphique_frt = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_ACCENT_FONCE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("1re réponse (min):Q", title="Minutes"),
        tooltip=["Date:T", alt.Tooltip("1re réponse (min):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_frt, width="stretch")

    st.subheader("Utilisation macro")
    graphique_macro = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE, strokeDash=[4, 4]).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Utilisation macro (%):Q", scale=alt.Scale(domain=[0, 100])),
        tooltip=["Date:T", alt.Tooltip("Utilisation macro (%):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_macro, width="stretch")


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

    lignes_agents = []

    for agent, tickets_agent in par_agent.items():
        volume = len(tickets_agent)
        csat_agent = moyenne(tickets_agent, "csat")
        macro_agent = taux_rempli(tickets_agent, "macro_applied")

        en_creneau_agent, pause_agent, hors_agent = separer_creneau(tickets_agent, planning_s2)
        frt_en_creneau_agent = moyenne(en_creneau_agent, "first_reply_time_min")

        resolution_agent = moyenne(tickets_agent, "full_resolution_time_hours")
        reopens_agent = moyenne(tickets_agent, "reopens")

        role_agent = roles_periode.get(agent, "—")

        if role_agent == ROLE_RESPONSABLE_EQUIPE:
            profil = "Management (volume non comparable aux conseillers)"
        else:
            volume_haut = volume > volume_moyen_equipe

            if csat_agent is not None and csat_moyen_equipe is not None:
                csat_haut = csat_agent > csat_moyen_equipe
            else:
                csat_haut = False

            if volume_haut and csat_haut:
                profil = "Référence"
            elif volume_haut and not csat_haut:
                profil = "Va vite, satisfaction en retrait"
            elif not volume_haut and csat_haut:
                profil = "Soigné, volume en retrait"
            else:
                profil = "À accompagner en priorité"

        ligne = {
            "Agent": agent,
            "Rôle": role_agent,
            "Tickets": volume,
            "CSAT": formater_csat(csat_agent),
            "1re réponse (en créneau)": "N/A",
            "Niveau réponse": "",
            "Résolution moyenne": "N/A",
            "Réouvertures moyennes": "N/A",
            "Utilisation macro (%)": formater_pourcentage(macro_agent),
            "Niveau utilisation macro": niveau_macro(macro_agent),
            "Profil": profil,
        }

        if resolution_agent is not None:
            ligne["Résolution moyenne"] = formater_duree(resolution_agent * 60)

        if reopens_agent is not None:
            ligne["Réouvertures moyennes"] = str(round(reopens_agent, 2))

        if frt_en_creneau_agent is not None:
            ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_agent)
            ligne["Niveau réponse"] = niveau_reponse_ouvree(frt_en_creneau_agent)

        lignes_agents.append(ligne)

    lignes_agents_triees = sorted(lignes_agents, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        afficher_tableau_colore(lignes_agents_triees, colonne_figee="Agent")

    st.subheader("Détail par agent")
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


# ------------------------------------------------------------------
# Onglet 4 : Alertes & suggestions
# ------------------------------------------------------------------

with onglet_alertes:
    st.markdown(titre_section_principale("Alertes"), unsafe_allow_html=True)

    if not comparaison_disponible:
        st.caption("Active « Comparer à une autre période » dans la barre latérale pour faire apparaître les alertes.")
    else:
        st.caption(
            "Une catégorie est signalée quand le CSAT baisse ET le temps de 1re réponse augmente en "
            "même temps par rapport à la période précédente — une seule des deux qui bouge n'est pas un "
            "signal fiable (le volume peut expliquer une hausse de temps de réponse sans dégrader la "
            "satisfaction). À lire à côté des événements des deux périodes (onglet Vue d'ensemble)."
        )

        alertes = []
        for categorie, tickets_cat_s2 in categories_s2.items():
            tickets_cat_s1 = categories_s1.get(categorie, [])
            if len(tickets_cat_s1) == 0:
                continue

            csat_s1 = moyenne(tickets_cat_s1, "csat")
            csat_s2 = moyenne(tickets_cat_s2, "csat")
            frt_s1 = moyenne(tickets_cat_s1, "first_reply_time_min")
            frt_s2 = moyenne(tickets_cat_s2, "first_reply_time_min")

            if csat_s1 is None or csat_s2 is None or frt_s1 is None or frt_s2 is None:
                continue

            delta_csat = csat_s2 - csat_s1
            delta_frt = frt_s2 - frt_s1

            if delta_csat < 0 and delta_frt > 0:
                alertes.append({
                    "Catégorie": categorie,
                    "CSAT": formater_csat(csat_s1) + " → " + formater_csat(csat_s2),
                    "Évolution CSAT": str(round(delta_csat, 2)),
                    "1re réponse": formater_duree(frt_s1) + " → " + formater_duree(frt_s2),
                    "Évolution 1re réponse": "+" + str(round(delta_frt)) + " min",
                })

        if len(alertes) == 0:
            st.write("Aucune catégorie ne dégrade simultanément CSAT et temps de réponse sur cette période.")
        else:
            with st.container(border=True):
                st.dataframe(alertes, hide_index=True, width="stretch")

    st.divider()
    st.caption("Détail complet par catégorie (CSAT, temps de réponse, macro) → onglet Vue d'ensemble.")

    st.markdown(titre_section_principale("Temps de résolution par catégorie"), unsafe_allow_html=True)
    st.caption(
        "Trié par temps de résolution moyen, du plus long au plus court — la vraie question n'est pas "
        "\"quel ticket a traîné\" mais \"quelle catégorie prend le plus de temps à l'équipe\"."
    )

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

    with st.container(border=True):
        st.dataframe(lignes_resolution_categorie_triees, hide_index=True, width="stretch")

    with st.expander("Détail : les 10 tickets les plus longs"):
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

        st.dataframe(lignes_longs, hide_index=True, width="stretch")

    st.subheader("Suggestions - macro à créer")
    st.caption(
        "Sujet avec au moins "
        + str(SEUIL_MINIMUM_SUJET)
        + " tickets, CSAT < "
        + str(SEUIL_CSAT_INSATISFAISANT)
        + ", quasi aucune macro utilisée"
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

    with st.container(border=True):
        afficher_tableau_colore(suggestions_creation)

    st.subheader("Suggestions - macro à renforcer (adoption partielle)")
    st.caption(
        "Utilisation macro entre " + str(SEUIL_MACRO_BASSE) + " % et " + str(SEUIL_MACRO_HAUTE) + " % "
        "et CSAT insatisfaisant — la macro existe mais n'est pas assez systématiquement utilisée : "
        "rappel à l'équipe, ou macro pas assez visible/facile à trouver."
    )

    with st.container(border=True):
        afficher_tableau_colore(suggestions_partielle)

    st.subheader("Suggestions - macro / process à améliorer")
    st.caption("Macro déjà bien utilisée mais CSAT insatisfaisant quand même")

    with st.container(border=True):
        afficher_tableau_colore(suggestions_amelioration)

    st.subheader("Suggestions - FAQ à créer")
    st.caption(
        "Sujet avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets et " + str(SEUIL_REPLIES_FAQ)
        + " échanges en moyenne ou plus — la résolution demande plusieurs allers-retours, signe qu'une "
        + "FAQ ou une page d'aide raccourcirait le traitement la prochaine fois"
    )

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

    with st.container(border=True):
        afficher_tableau_colore(suggestions_faq)

    st.subheader("Verbatims clients (CSAT bas)")
    st.caption(
        "Lecture qualitative des tickets mal notés (CSAT ≤ " + str(SEUIL_CSAT_VERBATIM) + ") — pour "
        "repérer des irritants \"process\" que les champs structurés ne capturent pas. Groupés par "
        "sujet, les 3 commentaires les plus récents par sujet."
    )

    tickets_verbatims = []
    for ticket in tickets_s2:
        csat_ticket = ticket["csat"]
        commentaire = ticket["csat_comment"]
        if csat_ticket is not None and csat_ticket <= SEUIL_CSAT_VERBATIM and commentaire:
            tickets_verbatims.append(ticket)

    if len(tickets_verbatims) == 0:
        st.write("Aucun commentaire sur les tickets mal notés de cette période.")
    else:
        sujets_verbatims = grouper_par(tickets_verbatims, "subject_cluster")

        def obtenir_compte_verbatims(item):
            sujet, tickets_sujet = item
            return len(tickets_sujet)

        sujets_verbatims_tries = sorted(sujets_verbatims.items(), key=obtenir_compte_verbatims, reverse=True)

        def obtenir_date_ticket(ticket):
            return ticket["created_at"]

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

    with st.expander("Mots fréquents (sujets à faible CSAT)"):
        st.caption(
            "Comptage simple des mots qui reviennent le plus dans les premiers messages des sujets déjà "
            "signalés ci-dessus — pour repérer un vocabulaire commun sans relire chaque ticket un par un."
        )

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

    st.subheader("Suivi des suggestions")
    st.caption(
        "Sujets marqués « Fait » dans le fichier de suivi (data_suivi/suivi_suggestions.xlsx) — "
        "impact mesuré en comparant le CSAT et l'utilisation macro avant/après la date d'action, "
        "sur tout l'historique disponible (pas seulement la période affichée)."
    )

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

    with st.container(border=True):
        afficher_tableau_colore(lignes_suivi)

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

    if len(lignes_macros_associees) > 0:
        st.caption("Macros/FAQ créées pour ces sujets — texte complet dans le CRM, pas dupliqué ici.")
        st.dataframe(lignes_macros_associees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 5 : Staffing & réactivité
# ------------------------------------------------------------------

with onglet_creneaux:
    st.caption(DEFINITION_EN_CRENEAU)

    en_creneau, pause_dejeuner, hors_creneau = separer_creneau(tickets_s2, planning_s2)
    tickets_hors_tout = pause_dejeuner + hors_creneau
    volume_total_creneaux = len(tickets_s2)

    # ------------------------------------------------------------------
    # Disponibilité des agents vs volume reçu
    # ------------------------------------------------------------------

    st.markdown(titre_section_principale("Couverture & respect du SLA"), unsafe_allow_html=True)
    st.caption("Sommes-nous assez staffés pour absorber le volume, aux bons horaires et aux bons jours ?")

    pct_en_creneau = len(en_creneau) / volume_total_creneaux * 100
    pct_hors_dispo = len(tickets_hors_tout) / volume_total_creneaux * 100
    frt_en_creneau_global = moyenne(en_creneau, "first_reply_time_min")

    with st.container(border=True):
        colonne_a, colonne_b, colonne_c = st.columns(3)
        colonne_a.markdown(
            construire_carte_kpi(
                "Reçus en créneau ouvré", formater_nombre_espace(len(en_creneau)),
                sous_texte=formater_pourcentage(pct_en_creneau) + " du volume",
            ),
            unsafe_allow_html=True,
        )
        colonne_b.markdown(
            construire_carte_kpi(
                "Reçus hors dispo agents", formater_nombre_espace(len(tickets_hors_tout)),
                sous_texte=formater_pourcentage(pct_hors_dispo) + " du volume",
            ),
            unsafe_allow_html=True,
        )
        if frt_en_creneau_global is not None:
            colonne_c.markdown(
                construire_carte_kpi("Traitement moyen en créneau", formater_duree(frt_en_creneau_global)),
                unsafe_allow_html=True,
            )

    st.subheader("Respect du SLA")
    st.caption(
        "SLA : en créneau ouvré, 1re réponse sous 1h. Hors créneau, réponse attendue au plus tard à la "
        "fin de la 1re plage horaire du prochain jour disponible — ex : message reçu vendredi 19h, "
        "réponse due lundi avant 12h (avant l'ouverture ou pendant la pause déjeuner : réponse due "
        "avant la fin du jour même)."
    )

    taux_sla_global = taux_sla(tickets_s2, planning_s2)
    if taux_sla_global is not None:
        st.markdown(
            construire_carte_kpi("SLA respecté", formater_pourcentage(taux_sla_global)), unsafe_allow_html=True
        )

    tickets_sla_connu = []
    for ticket in tickets_s2:
        if ticket["sla_met"] is not None:
            tickets_sla_connu.append(ticket)

    if len(tickets_sla_connu) > 0:
        respectes_bruts = 0
        for ticket in tickets_sla_connu:
            if ticket["sla_met"] == "Oui":
                respectes_bruts = respectes_bruts + 1
        taux_brut = respectes_bruts / len(tickets_sla_connu) * 100
        st.caption(
            "Le fichier source contient aussi son propre indicateur sla_met : "
            + formater_pourcentage(taux_brut) + ". L'écart avec le taux ci-dessus vient de la "
            + "définition de SLA détaillée plus haut, propre à cet outil — pas d'une erreur de données."
        )

    st.divider()
    st.subheader("Répartition des temps de réponse, tickets reçus en créneau")

    compte_niveaux = {"OK": 0, "A SURVEILLER": 0, "CRITIQUE": 0, "DEBORDEMENT": 0}
    for ticket in en_creneau:
        frt_ticket = ticket["first_reply_time_min"]
        if frt_ticket is not None:
            niveau = niveau_reponse_ouvree(frt_ticket)
            compte_niveaux[niveau] = compte_niveaux[niveau] + 1

    with st.container(border=True):
        colonne_d, colonne_e, colonne_f, colonne_g = st.columns(4)
        colonne_d.markdown(
            construire_carte_kpi("OK (< 1h30)", compte_niveaux["OK"], accent=COULEUR_ACCENT_OK),
            unsafe_allow_html=True,
        )
        colonne_e.markdown(
            construire_carte_kpi(
                "À surveiller (1h30-2h)", compte_niveaux["A SURVEILLER"], accent=COULEUR_ACCENT_SURVEILLER
            ),
            unsafe_allow_html=True,
        )
        colonne_f.markdown(
            construire_carte_kpi("Critique (> 2h)", compte_niveaux["CRITIQUE"], accent=COULEUR_ACCENT_CRITIQUE),
            unsafe_allow_html=True,
        )
        colonne_g.markdown(
            construire_carte_kpi(
                "Débordement (> 8h)", compte_niveaux["DEBORDEMENT"], accent=COULEUR_ACCENT_DEBORDEMENT
            ),
            unsafe_allow_html=True,
        )

    st.subheader("Par canal, en créneau")

    par_canal_en = grouper_par(en_creneau, "via_channel")
    lignes_canal_en = []
    for canal, tickets_canal in par_canal_en.items():
        frt_canal = moyenne(tickets_canal, "first_reply_time_min")
        ligne = {"Canal": canal, "Tickets": len(tickets_canal), "1re réponse moyenne": "N/A", "Niveau": ""}
        if frt_canal is not None:
            ligne["1re réponse moyenne"] = formater_duree(frt_canal)
            ligne["Niveau"] = niveau_reponse_ouvree(frt_canal)
        lignes_canal_en.append(ligne)

    lignes_canal_en_triees = sorted(lignes_canal_en, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        afficher_tableau_colore(lignes_canal_en_triees)

    # ------------------------------------------------------------------
    # Quand / pourquoi / comment les clients contactent hors créneau
    # ------------------------------------------------------------------

    st.divider()
    st.markdown(titre_section_principale("Volume hors créneau"), unsafe_allow_html=True)
    st.caption("Pour décider s'il faut élargir les horaires d'ouverture ou couvrir le week-end")

    groupes_type = {}
    for ticket in tickets_hors_tout:
        type_detail = type_hors_creneau_detaille(ticket["created_at"], ticket["assignee"], planning_s2)
        if type_detail in groupes_type:
            groupes_type[type_detail].append(ticket)
        else:
            groupes_type[type_detail] = [ticket]

    lignes_type = []
    for type_detail, tickets_type in groupes_type.items():
        frt_type = moyenne(tickets_type, "first_reply_time_min")
        csat_type = moyenne(tickets_type, "csat")
        pct_type = len(tickets_type) / volume_total_creneaux * 100

        ligne = {
            "Type": type_detail,
            "Tickets": len(tickets_type),
            "% du volume global": formater_pourcentage(pct_type),
            "Délai de rattrapage": "N/A",
            "CSAT": "N/A",
        }
        if frt_type is not None:
            ligne["Délai de rattrapage"] = formater_duree(frt_type)
        if csat_type is not None:
            ligne["CSAT"] = formater_csat(csat_type)

        lignes_type.append(ligne)

    lignes_type_triees = sorted(lignes_type, key=obtenir_tickets, reverse=True)

    with st.container(border=True):
        st.dataframe(lignes_type_triees, hide_index=True, width="stretch")

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
    st.markdown(titre_section_principale("Planning de l'équipe"), unsafe_allow_html=True)
    st.caption(
        "Nombre d'agents couvrant chaque créneau, lu depuis l'onglet PLANNING du dernier export de la "
        "période — pour voir d'un coup d'œil où la couverture est faible avant de modifier des horaires."
    )

    # Priorité au planning réellement déclaré (un agent programmé cette semaine mais qui
    # n'a clôturé aucun ticket ne doit pas disparaître de sa propre ligne de planning) ;
    # les assignees de tickets non présents dans le planning sont ajoutés en complément.
    agents_de_la_periode = grouper_par(tickets_s2, "assignee")
    agents_a_afficher = cles_combinees(planning_s2_dernier, agents_de_la_periode)

    agents_grille = []
    for agent in agents_a_afficher:
        if agent != NOM_AGENT_DEFAUT:
            agents_grille.append(agent)

    with st.container(border=True):
        grille_couverture = construire_grille_couverture(planning_s2_dernier, agents_grille)
        afficher_grille_couverture(grille_couverture)
        st.caption("Nombre d'agents planifiés sur ce créneau — 0 = rouge, 1 = jaune, 2+ = vert.")

    with st.expander("Détail horaires par agent"):
        horaires_standard = planning_s2_dernier.get(NOM_AGENT_DEFAUT, {})
        lignes_planning = [
            construire_ligne_planning("Créneau standard (référence)", horaires_standard, "—")
        ]

        for agent in agents_grille:
            horaires = horaires_agent(planning_s2_dernier, agent)
            role = roles_periode.get(agent, "—")
            lignes_planning.append(construire_ligne_planning(agent, horaires, role))

        st.dataframe(lignes_planning, hide_index=True, width="stretch")
        st.caption(
            "Tout est éditable dans l'onglet PLANNING du fichier Excel de l'export concerné (colonnes "
            "agent, jour, heure_debut, heure_fin, role) : les horaires et le rôle d'un agent, mais aussi "
            "le créneau standard lui-même (ligne \"DEFAUT\") — utile si un client passe à mi-temps, ferme "
            "un mois donné, ou ajoute des heures supplémentaires. Les arrivées/départs/absences se notent "
            "dans la colonne evenement_semaine de l'onglet RAW_TICKETS."
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

    st.subheader("Par produit")
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

    st.subheader("Type de résolution des SAV produit")
    st.caption("Beaucoup de \"conseil à distance\" = souci de compréhension d'usage plutôt qu'un vrai défaut. Beaucoup de remplacement = vrai défaut à corriger.")

    par_resolution = grouper_par(tickets_sav_produit_s2, "resolution_type")
    lignes_resolution = []
    for resolution, tickets_resolution in par_resolution.items():
        lignes_resolution.append({"Type de résolution": resolution, "Tickets": len(tickets_resolution)})

    lignes_resolution_triees = sorted(lignes_resolution, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        st.dataframe(lignes_resolution_triees, hide_index=True, width="stretch")

    st.subheader("Nature du problème")
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

    with st.expander("Détail croisé composant × nature du problème"):
        lignes_composant_issue_triees = sorted(lignes_composant_issue, key=obtenir_tickets, reverse=True)
        st.dataframe(lignes_composant_issue_triees, hide_index=True, width="stretch")

    st.subheader("Garantie")
    st.caption(
        "Part des tickets SAV produit sous garantie vs hors garantie — un hors-garantie coûte plus "
        "cher à l'entreprise (voir l'onglet Impact & confiance pour le chiffrage)."
    )

    par_garantie = grouper_par(tickets_sav_produit_s2, "warranty_status")
    lignes_garantie = []
    for garantie, tickets_garantie in par_garantie.items():
        lignes_garantie.append({"Statut garantie": garantie, "Tickets": len(tickets_garantie)})

    with st.container(border=True):
        st.dataframe(lignes_garantie, hide_index=True, width="stretch")

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

    st.subheader("Clients avec SAV récurrents")

    tickets_recurrents = []
    for ticket in tickets_sav_produit_s2:
        if ticket["prior_sav_count"] is not None and ticket["prior_sav_count"] >= 1:
            tickets_recurrents.append(ticket)

    st.write(
        str(len(tickets_recurrents)) + " tickets sur " + str(len(tickets_sav_produit_s2))
        + " concernent un client ayant déjà eu au moins un SAV avant celui-ci — signal de défaut structurel plutôt qu'un cas isolé."
    )

    if len(tickets_recurrents) > 0:
        st.write("Produit et composant les plus concernés par la récurrence :")

        par_produit_recurrent = grouper_par(tickets_recurrents, "product_name")
        lignes_produit_recurrent = []
        for produit, tickets_produit_r in par_produit_recurrent.items():
            lignes_produit_recurrent.append({"Produit": produit, "SAV récurrents": len(tickets_produit_r)})
        lignes_produit_recurrent_triees = sorted(lignes_produit_recurrent, key=obtenir_sav_recurrents, reverse=True)

        par_composant_recurrent = grouper_par(tickets_recurrents, "component")
        lignes_composant_recurrent = []
        for composant, tickets_composant_r in par_composant_recurrent.items():
            lignes_composant_recurrent.append({"Composant": composant, "SAV récurrents": len(tickets_composant_r)})
        lignes_composant_recurrent_triees = sorted(lignes_composant_recurrent, key=obtenir_sav_recurrents, reverse=True)

        with st.container(border=True):
            colonne_rec_a, colonne_rec_b = st.columns(2)
            with colonne_rec_a:
                st.dataframe(lignes_produit_recurrent_triees, hide_index=True, width="stretch")
            with colonne_rec_b:
                st.dataframe(lignes_composant_recurrent_triees, hide_index=True, width="stretch")

    st.divider()
    st.subheader("Opportunités produit — demandes hors catalogue")
    st.caption(
        "Top 10 des demandes récurrentes pour quelque chose qu'on ne vend pas (accessoire, "
        "personnalisation...), détectées via tout sujet marqué « (hors catalogue) » — à remonter à "
        "l'équipe produit."
    )

    opportunites = detecter_opportunites_hors_catalogue(tickets_s2, 1)

    if len(opportunites) == 0:
        st.write("Aucune demande hors catalogue sur cette période.")
    else:
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

    st.subheader("Sujets livraison")

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
            volume_s1 = len(sujets_livraison_s1.get(sujet, []))
            delta = volume_s2 - volume_s1
            if delta >= 0:
                ligne["Évolution"] = "+" + str(delta)
            else:
                ligne["Évolution"] = str(delta)

        lignes_livraison.append(ligne)

    lignes_livraison_triees = sorted(lignes_livraison, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        afficher_tableau_colore(lignes_livraison_triees)

    st.subheader("Par pays")
    st.caption("Le transporteur est unique sur toute la zone de livraison — un écart marqué sur un pays isole un problème logistique local plutôt qu'un souci transporteur global.")

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
    with st.container(border=True):
        afficher_tableau_colore(lignes_pays_livraison_triees)


# ------------------------------------------------------------------
# Onglet 8 : Conversion & acquisition
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
        "Pour repérer si un agent convertit mieux (ou moins bien) certains pays que d'autres — un signal "
        "utile pour la répartition des dossiers, pas un chiffre de performance commerciale. Limité aux "
        "combinaisons agent/pays avec au moins " + str(SEUIL_MINIMUM_SUJET) + " tickets avant-vente."
    )

    par_agent_pays = {}
    for ticket, commande in resultats_conversion:
        cle = (ticket["assignee"], ticket["country"])
        if cle not in par_agent_pays:
            par_agent_pays[cle] = {"total": 0, "convertis": 0}
        par_agent_pays[cle]["total"] = par_agent_pays[cle]["total"] + 1
        if commande is not None:
            par_agent_pays[cle]["convertis"] = par_agent_pays[cle]["convertis"] + 1

    lignes_agent_pays = []
    for cle, stats in par_agent_pays.items():
        agent, pays = cle
        if stats["total"] < SEUIL_MINIMUM_SUJET:
            continue
        lignes_agent_pays.append({
            "agent": agent,
            "pays": pays,
            "tickets": stats["total"],
            "convertis": stats["convertis"],
            "taux": stats["convertis"] / stats["total"] * 100,
        })

    def obtenir_tri_agent_pays(ligne):
        return (ligne["agent"], -ligne["taux"])

    lignes_agent_pays_triees = sorted(lignes_agent_pays, key=obtenir_tri_agent_pays)

    lignes_agent_pays_affichage = []
    for ligne in lignes_agent_pays_triees:
        lignes_agent_pays_affichage.append({
            "Agent": ligne["agent"],
            "Pays": ligne["pays"],
            "Tickets avant-vente": ligne["tickets"],
            "Convertis": ligne["convertis"],
            "Taux de conversion": formater_pourcentage(ligne["taux"]),
        })

    with st.container(border=True):
        st.dataframe(lignes_agent_pays_affichage, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 9 : Impact & confiance
# ------------------------------------------------------------------

with onglet_impact:
    st.markdown(titre_section_principale("Pertes financières directes"), unsafe_allow_html=True)
    st.caption(
        "Basé sur le type de résolution du ticket, montant estimé par une fraction réaliste du prix de "
        "la commande d'origine (fichier Shopify fictif) — remboursement intégral, remplacement ou geste "
        "commercial à coût partiel. Chaque commande n'est comptée qu'une seule fois même si plusieurs "
        "tickets s'y rattachent."
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
    commandes_deja_comptees = set()
    for type_perte, tickets_perte in groupes_perte.items():
        pct_perte = len(tickets_perte) / len(tickets_s2) * 100

        montants = []
        for ticket in tickets_perte:
            order_id = ticket["order_id"]
            if order_id in commandes_deja_comptees:
                continue
            montant = montant_perte_estime(ticket, commandes, type_perte)
            if montant is not None:
                montants.append(montant)
                commandes_deja_comptees.add(order_id)

        ligne = {
            "Type de perte": type_perte,
            "Tickets": len(tickets_perte),
            "% du volume global": formater_pourcentage(pct_perte),
            "Montant estimé": "N/A",
        }

        if len(montants) > 0:
            somme = sum(montants)
            ligne["Montant estimé"] = formater_montant(somme)
            montant_total_pertes = montant_total_pertes + somme

        lignes_perte.append(ligne)

    lignes_perte_triees = sorted(lignes_perte, key=obtenir_tickets, reverse=True)
    with st.container(border=True):
        st.dataframe(lignes_perte_triees, hide_index=True, width="stretch")

    if montant_total_pertes > 0:
        st.markdown(
            construire_carte_kpi(
                "Total pertes financières directes estimées", formater_montant(montant_total_pertes)
            ),
            unsafe_allow_html=True,
        )

    st.subheader("SAV sous garantie (coût absorbé par l'entreprise)")

    tickets_sav_produit_business = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_garantie = []
    for ticket in tickets_sav_produit_business:
        if ticket["warranty_status"] == "Sous garantie":
            tickets_garantie.append(ticket)

    if len(tickets_sav_produit_business) > 0:
        pct_garantie = len(tickets_garantie) / len(tickets_sav_produit_business) * 100

        st.write(
            str(len(tickets_garantie)) + " tickets sur " + str(len(tickets_sav_produit_business))
            + " tickets de SAV produit (soit " + formater_pourcentage(pct_garantie) + ") concernent un "
            + "appareil encore sous garantie — le coût de remplacement/réparation est à la charge de "
            + "l'entreprise, pas du client."
        )

        montants_garantie = []
        commandes_garantie_deja_comptees = set()
        for ticket in tickets_garantie:
            order_id = ticket["order_id"]
            if order_id in commandes_garantie_deja_comptees:
                continue
            montant = montant_cout_garantie(ticket, commandes)
            if montant is not None:
                montants_garantie.append(montant)
                commandes_garantie_deja_comptees.add(order_id)

        if len(montants_garantie) > 0:
            st.markdown(
                construire_carte_kpi(
                    "Coût de remplacement estimé (produits sous garantie)",
                    formater_montant(sum(montants_garantie)),
                ),
                unsafe_allow_html=True,
            )
            st.caption("Estimé à partir d'une fraction du prix de vente (coût matière/logistique), pas le prix payé par le client.")

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
            colonne_nps_a.markdown(construire_carte_kpi("NPS global", round(nps_global, 1)), unsafe_allow_html=True)
        if nps_contactes is not None:
            colonne_nps_b.markdown(
                construire_carte_kpi("NPS - a contacté le support", round(nps_contactes, 1)),
                unsafe_allow_html=True,
            )
        if nps_non_contactes is not None:
            colonne_nps_c.markdown(
                construire_carte_kpi("NPS - jamais contacté (référence)", round(nps_non_contactes, 1)),
                unsafe_allow_html=True,
            )

    if nps_contactes is not None and nps_non_contactes is not None:
        ecart_nps = round(nps_contactes - nps_non_contactes, 1)
        st.write(
            "Écart : les clients ayant contacté le support ont un NPS de " + str(ecart_nps)
            + " points par rapport à ceux qui n'ont jamais contacté — la mesure concrète de la "
            + "perte (ou du gain) de confiance liée à l'expérience de contact."
        )

    st.write("Évolution du NPS dans le temps :")

    nps_par_mois = {}
    for reponse in reponses_nps:
        cle_mois = reponse["date_reponse"].strftime("%Y-%m")
        if cle_mois in nps_par_mois:
            nps_par_mois[cle_mois].append(reponse)
        else:
            nps_par_mois[cle_mois] = [reponse]

    lignes_nps_mois = []
    for cle_mois in sorted(nps_par_mois.keys()):
        nps_mois = calculer_nps(nps_par_mois[cle_mois])
        if nps_mois is None:
            continue
        lignes_nps_mois.append({"Mois": cle_mois, "NPS": nps_mois, "Réponses": len(nps_par_mois[cle_mois])})

    tableau_nps_mois = pd.DataFrame(lignes_nps_mois)
    graphique_nps = alt.Chart(tableau_nps_mois).mark_line(point=True, color=COULEUR_SECONDAIRE).encode(
        x=alt.X("Mois:O", title=None),
        y=alt.Y("NPS:Q"),
        tooltip=["Mois:N", "NPS:Q", "Réponses:Q"],
    ).properties(height=260).configure_view(strokeWidth=0)
    with st.container(border=True):
        st.altair_chart(graphique_nps, width="stretch")
