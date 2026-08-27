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
    montant_ticket,
    formater_montant,
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
    charger_calendrier_evenements,
    evenements_dans_periode,
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
    niveau_csat,
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
    cible_perte_confiance,
    type_perte_financiere,
)


def obtenir_tickets(ligne):
    return ligne["Tickets"]


def obtenir_sav_recurrents(ligne):
    return ligne["SAV récurrents"]


DEFINITION_EN_CRENEAU = (
    "« En créneau » = uniquement les tickets arrivés pendant les horaires de travail définis "
    "dans l'onglet Planning. Ça isole la vraie performance de l'équipe, sans le délai dû aux "
    "horaires hors couverture (voir l'onglet Créneaux & délais pour le détail du hors créneau)."
)


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


def afficher_tableau_colore(lignes):
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
    st.dataframe(tableau_stylise, hide_index=True, width="stretch")


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


COULEUR_PRIMAIRE = "#CC5500"
COULEUR_SECONDAIRE = "#96234A"
COULEUR_ACCENT_FONCE = "#8B4513"

DOSSIER_EXPORTS = os.path.join(DOSSIER_PROJET, "exports_hebdomadaires")
FICHIER_SHOPIFY = os.path.join(DOSSIER_PROJET, "data_shopify", "commandes_shopify_fictif.xlsx")
FICHIER_NPS = os.path.join(DOSSIER_PROJET, "data_shopify", "nps_fictif.xlsx")
FICHIER_SUIVI_SUGGESTIONS = os.path.join(DOSSIER_PROJET, "data_suivi", "suivi_suggestions.xlsx")
DOSSIER_MACROS = os.path.join(DOSSIER_PROJET, "knowledge_base", "macros")
DOSSIER_FAQ = os.path.join(DOSSIER_PROJET, "knowledge_base", "faq")
FICHIER_CALENDRIER = os.path.join(DOSSIER_PROJET, "data_calendrier", "calendrier_evenements.xlsx")
FENETRE_CONVERSION_JOURS = 30

COUT_ACQUISITION_PAR_CANAL = {
    "Publicité Meta/Google": 20,
    "Email marketing": 5,
    "Recherche organique": 2,
    "Recommandation": 3,
    "Direct": 0,
}

SEUIL_MINIMUM_SUJET = 5
SEUIL_MACRO_BASSE = 20
SEUIL_MACRO_HAUTE = 50
SEUIL_CSAT_INSATISFAISANT = 4
SEUIL_HAUSSE_SUJET_SURVEILLER = 5
SEUIL_HAUSSE_SUJET_CRITIQUE = 10
SEUIL_REPLIES_FAQ = 3
SEUIL_CSAT_VERBATIM = 2

st.set_page_config(page_title="Dashboard Customer Care : Emyria", layout="wide")
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
st.sidebar.caption("Aujourd'hui : " + datetime.date.today().strftime("%d/%m/%Y"))
st.sidebar.button("Réinitialiser (dernières données)", on_click=reinitialiser_periode)

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
planning_s2_dernier = charger_planning(fichiers_actuels[-1])
planning_s2 = construire_plannings_periode(fichiers_actuels, exports_disponibles)

if comparaison_disponible:
    tickets_s1 = charger_periode(fichiers_precedents)
    planning_s1_dernier = charger_planning(fichiers_precedents[-1])
    agents_s1_liste = list(grouper_par(tickets_s1, "assignee").keys())
    agents_s2_liste = list(grouper_par(tickets_s2, "assignee").keys())
    changements_planning = detecter_changements_planning(agents_s1_liste, agents_s2_liste, planning_s1_dernier, planning_s2_dernier)

st.caption(periode_texte + " (" + str(len(fichiers_actuels)) + " export(s) — " + str(len(tickets_s2)) + " tickets)")
if comparer and not comparaison_disponible:
    st.caption("Aucun export disponible sur la période B choisie — pas de comparaison possible.")

with st.sidebar.expander("🎨 Comment lire les couleurs"):
    st.markdown(
        "🟢 **Vert** — OK / Correct / Excellent / Fort potentiel : rien à faire\n\n"
        "🟡 **Jaune** — À surveiller / Potentiel moyen : à garder à l'œil\n\n"
        "🔴 **Rouge** — Critique / Débordement / Risque de perte du prospect : action recommandée\n\n"
        "🔵 **Bleu** — Nouveau : sujet apparu depuis la période précédente\n\n"
        "⚪ **Gris** — Disparu : sujet qui n'apparaît plus sur la période actuelle"
    )

categories_s1 = grouper_par_categorie(tickets_s1)
categories_s2 = grouper_par_categorie(tickets_s2)

# Chargés une seule fois ici (au lieu de dans un onglet) car utilisés à la fois par
# "Conversion & acquisition" et "Impact & confiance" — éviter de recharger deux fois.
commandes = charger_commandes(FICHIER_SHOPIFY)

fichiers_tous_business = []
for date_export_hist, chemin_hist in exports_disponibles:
    fichiers_tous_business.append(chemin_hist)
tickets_historique_business = charger_periode(fichiers_tous_business)

(
    onglet_contexte, onglet_vue, onglet_tendances, onglet_categories, onglet_agents, onglet_alertes,
    onglet_creneaux, onglet_planning, onglet_produit, onglet_livraison, onglet_conversion, onglet_impact,
) = st.tabs(
    [
        "🏠 Contexte", "📊 Vue d'ensemble", "📈 Tendances", "🗂️ Catégories", "🧑‍💻 Agents",
        "🚨 Alertes & suggestions", "⏱️ Créneaux & délais", "📅 Planning", "🔧 Produit", "📦 Livraison",
        "💱 Conversion & acquisition", "🤝 Impact & confiance",
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

        st.info(
            "Ce tableau de bord est une démonstration construite sur des données 100 % fictives "
            "(tickets, commandes, avis) — pas l'audit d'une entreprise réelle. Il illustre un outil de "
            "pilotage du service client conçu pour ce type de scale-up e-commerce."
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
            "- **Équipe** : 38 personnes, dont 4 au service client\n"
            "- **Stade** : scale-up, post-Série A, forte croissance\n"
            "- **Fondée en** : 2021"
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
            "- **📊 Vue d'ensemble → 🚨 Alertes** : pilotage hebdomadaire de l'équipe\n"
            "- **⏱️ Créneaux & délais → 📅 Planning** : staffing et couverture horaire\n"
            "- **🔧 Produit** : cadence trimestrielle (usure, défauts récurrents)\n"
            "- **📦 Livraison** : cadence mensuelle, pensé pour un point avec le transporteur\n"
            "- **💱 Conversion & acquisition** : avant-vente, taux de conversion réel, canaux d'achat\n"
            "- **🤝 Impact & confiance** : coûts SAV, fidélisation, confiance client (NPS)\n\n"
            "🎨 Les tableaux utilisent un code couleur (vert/jaune/rouge/bleu/gris) — légende "
            "dans la barre latérale."
        )

    st.divider()
    st.caption(
        "Toutes les données (tickets, commandes, avis NPS) sont générées aléatoirement pour cette "
        "démonstration — les chiffres n'ont aucune valeur réelle."
    )


# ------------------------------------------------------------------
# Onglet 1 : Vue d'ensemble
# ------------------------------------------------------------------

with onglet_vue:
    nombre_s2 = len(tickets_s2)
    csat_s2 = moyenne(tickets_s2, "csat")
    frt_s2 = moyenne(tickets_s2, "first_reply_time_min")
    macro_s2 = taux_rempli(tickets_s2, "macro_applied")

    colonne1, colonne2, colonne3, colonne4 = st.columns(4)

    if comparaison_disponible:
        nombre_s1 = len(tickets_s1)
        csat_s1 = moyenne(tickets_s1, "csat")
        frt_s1 = moyenne(tickets_s1, "first_reply_time_min")
        macro_s1 = taux_rempli(tickets_s1, "macro_applied")

        colonne1.metric("Tickets reçus", nombre_s2, delta=nombre_s2 - nombre_s1, delta_color="off")

        if csat_s2 is not None and csat_s1 is not None:
            colonne2.metric("CSAT moyen", formater_csat(csat_s2), delta=round(csat_s2 - csat_s1, 2))
        else:
            colonne2.metric("CSAT moyen", formater_csat(csat_s2))

        if frt_s2 is not None and frt_s1 is not None:
            colonne3.metric(
                "1re réponse",
                formater_duree(frt_s2),
                delta=str(round(frt_s2 - frt_s1)) + " min",
                delta_color="inverse",
            )
        else:
            colonne3.metric("1re réponse", formater_duree(frt_s2))

        if macro_s2 is not None and macro_s1 is not None:
            colonne4.metric(
                "Utilisation macro",
                formater_pourcentage(macro_s2),
                delta=str(round(macro_s2 - macro_s1, 1)) + " pt",
            )
        else:
            colonne4.metric("Utilisation macro", formater_pourcentage(macro_s2))
    else:
        colonne1.metric("Tickets reçus", nombre_s2)
        colonne2.metric("CSAT moyen", formater_csat(csat_s2))
        colonne3.metric("1re réponse", formater_duree(frt_s2))
        colonne4.metric("Utilisation macro", formater_pourcentage(macro_s2))

    evenements_texte = construire_texte_evenements(exports_disponibles, date_a_debut, date_a_fin)
    for changement in changements_planning:
        evenements_texte = evenements_texte + "  \nChangement planning : " + changement

    st.info("Événement(s) de la période :  \n" + evenements_texte)

    st.subheader("Répartition par famille")
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
        st.altair_chart(graphique_categories, width="stretch")
    else:
        lignes_graphique_categories = []
        for ligne in lignes_categories_apercu_triees:
            lignes_graphique_categories.append(
                {"Catégorie": ligne["Catégorie"], "Période actuelle": ligne["Tickets"]}
            )
        tableau_graphique_categories = pd.DataFrame(lignes_graphique_categories).set_index("Catégorie")
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


# ------------------------------------------------------------------
# Onglet 1bis : Tendances
# ------------------------------------------------------------------

with onglet_tendances:
    st.caption(
        "Évolution sur les " + str(len(exports_disponibles)) + " exports disponibles (~1 an) — indépendant "
        "du filtre de période dans la barre latérale, pour voir une vraie tendance plutôt que comparer "
        "seulement deux instantanés."
    )

    lignes_tendance = []
    for date_export, chemin in exports_disponibles:
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

    st.subheader("Volume de tickets")
    graphique_volume = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Tickets:Q"),
        tooltip=["Date:T", "Tickets:Q", "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    st.altair_chart(graphique_volume, width="stretch")

    st.subheader("CSAT moyen")
    graphique_csat = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_SECONDAIRE).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("CSAT:Q", scale=alt.Scale(domain=[1, 5])),
        tooltip=["Date:T", alt.Tooltip("CSAT:Q", format=".2f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    st.altair_chart(graphique_csat, width="stretch")

    st.subheader("Temps de 1re réponse moyen")
    graphique_frt = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_ACCENT_FONCE).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("1re réponse (min):Q", title="Minutes"),
        tooltip=["Date:T", alt.Tooltip("1re réponse (min):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    st.altair_chart(graphique_frt, width="stretch")

    st.subheader("Utilisation macro")
    graphique_macro = alt.Chart(tableau_tendance).mark_line(point=True, color=COULEUR_PRIMAIRE).encode(
        x=alt.X("Date:T", title=None),
        y=alt.Y("Utilisation macro (%):Q", scale=alt.Scale(domain=[0, 100])),
        tooltip=["Date:T", alt.Tooltip("Utilisation macro (%):Q", format=".0f"), "Événement:N"],
    ).properties(height=260).configure_view(strokeWidth=0)
    st.altair_chart(graphique_macro, width="stretch")


# ------------------------------------------------------------------
# Onglet 2 : Catégories
# ------------------------------------------------------------------

with onglet_categories:
    st.caption(DEFINITION_EN_CRENEAU)

    lignes_categories = []

    if comparaison_disponible:
        categories_a_afficher = cles_combinees(categories_s2, categories_s1)
    else:
        categories_a_afficher = list(categories_s2.keys())

    for categorie in categories_a_afficher:
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
        ligne["Niveau CSAT"] = ""
        ligne["1re réponse (en créneau)"] = "N/A"
        ligne["Niveau réponse"] = ""
        ligne["% hors créneau"] = formater_pourcentage(pct_hors_creneau_cat)
        ligne["Utilisation macro (%)"] = formater_pourcentage(macro_cat_s2)
        ligne["Niveau utilisation macro"] = niveau_macro(macro_cat_s2)

        if csat_cat_s2 is not None:
            ligne["CSAT"] = formater_csat(csat_cat_s2)
            ligne["Niveau CSAT"] = niveau_csat(csat_cat_s2)

        if frt_en_creneau_cat is not None:
            ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_cat)
            ligne["Niveau réponse"] = niveau_reponse_ouvree(frt_en_creneau_cat)

        lignes_categories.append(ligne)

    afficher_tableau_colore(lignes_categories)


# ------------------------------------------------------------------
# Onglet 3 : Agents
# ------------------------------------------------------------------

with onglet_agents:
    st.caption(DEFINITION_EN_CRENEAU)

    par_agent = grouper_par(tickets_s2, "assignee")

    volumes = []
    csats_valides = []

    for agent, tickets_agent in par_agent.items():
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
            "Tickets": volume,
            "CSAT": formater_csat(csat_agent),
            "Niveau CSAT": niveau_csat(csat_agent),
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
            ligne["Réouvertures moyennes"] = round(reopens_agent, 2)

        if frt_en_creneau_agent is not None:
            ligne["1re réponse (en créneau)"] = formater_duree(frt_en_creneau_agent)
            ligne["Niveau réponse"] = niveau_reponse_ouvree(frt_en_creneau_agent)

        lignes_agents.append(ligne)

    lignes_agents_triees = sorted(lignes_agents, key=obtenir_tickets, reverse=True)
    afficher_tableau_colore(lignes_agents_triees)

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
                    ligne_sujet["Réouvertures moyennes"] = round(reopens_sujet, 2)

                lignes_sujets_agent.append(ligne_sujet)

            lignes_sujets_agent_triees = sorted(lignes_sujets_agent, key=obtenir_tickets, reverse=True)
            st.dataframe(lignes_sujets_agent_triees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 4 : Alertes & suggestions
# ------------------------------------------------------------------

with onglet_alertes:
    st.subheader("🚨 Alertes")

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
                    "Évolution CSAT": round(delta_csat, 2),
                    "1re réponse": formater_duree(frt_s1) + " → " + formater_duree(frt_s2),
                    "Évolution 1re réponse": "+" + str(round(delta_frt)) + " min",
                })

        if len(alertes) == 0:
            st.write("Aucune catégorie ne dégrade simultanément CSAT et temps de réponse sur cette période.")
        else:
            st.dataframe(alertes, hide_index=True, width="stretch")

    st.divider()
    st.caption("Détail complet par catégorie (CSAT, temps de réponse, macro) → onglet Catégories.")

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
            "Niveau CSAT": niveau_csat(csat_sujet),
            "Utilisation macro (%)": formater_pourcentage(macro_sujet),
        }

        if macro_sujet < SEUIL_MACRO_BASSE:
            suggestions_creation.append(ligne)
        elif macro_sujet >= SEUIL_MACRO_HAUTE:
            suggestions_amelioration.append(ligne)
        else:
            suggestions_partielle.append(ligne)

    afficher_tableau_colore(suggestions_creation)

    st.subheader("Suggestions - macro à renforcer (adoption partielle)")
    st.caption(
        "Utilisation macro entre " + str(SEUIL_MACRO_BASSE) + " % et " + str(SEUIL_MACRO_HAUTE) + " % "
        "et CSAT insatisfaisant — la macro existe mais n'est pas assez systématiquement utilisée : "
        "rappel à l'équipe, ou macro pas assez visible/facile à trouver."
    )

    afficher_tableau_colore(suggestions_partielle)

    st.subheader("Suggestions - macro / process à améliorer")
    st.caption("Macro déjà bien utilisée mais CSAT insatisfaisant quand même")

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
            "Échanges moyens": round(replies_moyen, 1),
        })

    afficher_tableau_colore(suggestions_faq)

    st.subheader("Verbatims clients (CSAT bas)")
    st.caption(
        "Lecture qualitative des tickets mal notés (CSAT ≤ " + str(SEUIL_CSAT_VERBATIM) + ") — pour "
        "repérer des irritants \"process\" que les champs structurés ne capturent pas."
    )

    def obtenir_csat_ticket(ticket):
        return ticket["csat"]

    tickets_verbatims = []
    for ticket in tickets_s2:
        csat_ticket = ticket["csat"]
        commentaire = ticket["csat_comment"]
        if csat_ticket is not None and csat_ticket <= SEUIL_CSAT_VERBATIM and commentaire:
            tickets_verbatims.append(ticket)

    tickets_verbatims_tries = sorted(tickets_verbatims, key=obtenir_csat_ticket)

    lignes_verbatims = []
    for ticket in tickets_verbatims_tries:
        lignes_verbatims.append({
            "Sujet": ticket["subject_cluster"],
            "CSAT": ticket["csat"],
            "Commentaire": ticket["csat_comment"],
        })

    if len(lignes_verbatims) == 0:
        st.write("Aucun commentaire sur les tickets mal notés de cette période.")
    else:
        st.dataframe(lignes_verbatims, hide_index=True, width="stretch")

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
        fichiers_tous = []
        for date_export_historique, chemin_historique in exports_disponibles:
            fichiers_tous.append(chemin_historique)
        tickets_historique = charger_periode(fichiers_tous)
        sujets_historique = grouper_par(tickets_historique, "subject_cluster")

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

    afficher_tableau_colore(lignes_suivi)

    for sujet, entree in sujets_traites:
        code_macro = extraire_code_macro(entree["notes"])
        texte_macro = charger_texte_macro(code_macro, DOSSIER_MACROS)
        if texte_macro is not None:
            with st.expander("Voir la macro " + code_macro + " (" + sujet + ")"):
                st.markdown(texte_macro)

            nom_fichier_faq = extraire_nom_fichier_faq(texte_macro)
            texte_faq = charger_texte_faq(nom_fichier_faq, DOSSIER_FAQ)
            if texte_faq is not None:
                with st.expander("Voir la FAQ associée (" + sujet + ")"):
                    st.markdown(texte_faq)

    st.divider()
    with st.expander("Réouvertures & tickets longs"):
        st.caption("Un ticket rouvert plusieurs fois signale une résolution bâclée ou incomplète, pas juste un chiffre de volume en plus")

        taux_reopens_global = moyenne(tickets_s2, "reopens")
        if taux_reopens_global is not None:
            st.metric("Réouvertures moyennes (toute la période)", round(taux_reopens_global, 2))

        st.write("Les 10 tickets les plus longs à résoudre :")

        def obtenir_resolution(ticket):
            return ticket["full_resolution_time_hours"]

        tickets_avec_resolution = []
        for ticket in tickets_s2:
            if ticket["full_resolution_time_hours"] is not None:
                tickets_avec_resolution.append(ticket)

        tickets_tries_par_resolution = sorted(tickets_avec_resolution, key=obtenir_resolution, reverse=True)

        lignes_longs = []
        for ticket in tickets_tries_par_resolution[:10]:
            if ticket["macro_applied"] is not None:
                macro_texte = "Oui"
            else:
                macro_texte = "Non"

            lignes_longs.append(
                {
                    "Ticket": ticket["ticket_id"],
                    "Agent": ticket["assignee"],
                    "Sujet": ticket["subject_cluster"],
                    "Résolution": formater_duree(ticket["full_resolution_time_hours"] * 60),
                    "Macro utilisée": macro_texte,
                    "Réouvertures": ticket["reopens"],
                }
            )

        st.dataframe(lignes_longs, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 5 : Créneaux & délais
# ------------------------------------------------------------------

with onglet_creneaux:
    st.caption("Horaires lus depuis l'onglet PLANNING du fichier Excel (un planning par agent est possible, avec un planning par défaut pour les autres)")

    en_creneau, pause_dejeuner, hors_creneau = separer_creneau(tickets_s2, planning_s2)
    tickets_hors_tout = pause_dejeuner + hors_creneau
    volume_total_creneaux = len(tickets_s2)

    # ------------------------------------------------------------------
    # Disponibilité des agents vs volume reçu
    # ------------------------------------------------------------------

    st.subheader("Les agents sont-ils disponibles aux bons horaires ?")
    st.caption("Sommes-nous assez staffés pour absorber le volume, aux bons horaires et aux bons jours ?")

    pct_en_creneau = len(en_creneau) / volume_total_creneaux * 100
    pct_hors_dispo = len(tickets_hors_tout) / volume_total_creneaux * 100
    frt_en_creneau_global = moyenne(en_creneau, "first_reply_time_min")

    colonne_a, colonne_b, colonne_c = st.columns(3)
    colonne_a.metric("Reçus en créneau ouvré", len(en_creneau), formater_pourcentage(pct_en_creneau) + " du volume")
    colonne_b.metric("Reçus hors dispo agents", len(tickets_hors_tout), formater_pourcentage(pct_hors_dispo) + " du volume")
    if frt_en_creneau_global is not None:
        colonne_c.metric("Traitement moyen en créneau", formater_duree(frt_en_creneau_global))

    st.subheader("Respect du SLA")
    st.caption(
        "SLA : en créneau ouvré, 1re réponse sous 1h. Hors créneau, réponse attendue au plus tard à la "
        "fin de la 1re plage horaire du prochain jour disponible — ex : message reçu vendredi 19h, "
        "réponse due lundi avant 12h (avant l'ouverture ou pendant la pause déjeuner : réponse due "
        "avant la fin du jour même)."
    )

    taux_sla_global = taux_sla(tickets_s2, planning_s2)
    if taux_sla_global is not None:
        st.metric("SLA respecté", formater_pourcentage(taux_sla_global))

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

    colonne_d, colonne_e, colonne_f, colonne_g = st.columns(4)
    colonne_d.metric("OK (< 1h30)", compte_niveaux["OK"])
    colonne_e.metric("À surveiller (1h30-2h)", compte_niveaux["A SURVEILLER"])
    colonne_f.metric("Critique (> 2h)", compte_niveaux["CRITIQUE"])
    colonne_g.metric("Débordement (> 8h)", compte_niveaux["DEBORDEMENT"])

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
    afficher_tableau_colore(lignes_canal_en_triees)

    # ------------------------------------------------------------------
    # Quand / pourquoi / comment les clients contactent hors créneau
    # ------------------------------------------------------------------

    st.divider()
    st.subheader("Quand les clients nous contactent hors créneau")
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

    tableau_type_graphique = pd.DataFrame(lignes_type_triees)[["Type", "Tickets"]].set_index("Type")
    st.bar_chart(tableau_type_graphique, horizontal=True, color=COULEUR_PRIMAIRE)

    st.dataframe(lignes_type_triees, hide_index=True, width="stretch")

    st.subheader("Pourquoi (par catégorie de demande)")

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

    lignes_type_categorie_triees = sorted(lignes_type_categorie, key=obtenir_tickets, reverse=True)
    st.dataframe(lignes_type_categorie_triees, hide_index=True, width="stretch")

    st.subheader("Comment (par canal)")

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

    lignes_type_canal_triees = sorted(lignes_type_canal, key=obtenir_tickets, reverse=True)
    st.dataframe(lignes_type_canal_triees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 6 : Planning
# ------------------------------------------------------------------

with onglet_planning:
    st.caption("Qui a travaillé sur cette période, avec quel rôle, et combien d'heures — lu depuis l'onglet PLANNING du dernier export de la période")

    roles_periode = charger_roles_planning(fichiers_actuels[-1])

    horaires_standard = planning_s2_dernier.get(NOM_AGENT_DEFAUT, {})
    lignes_planning = [
        construire_ligne_planning("Créneau standard (référence)", horaires_standard, "—")
    ]

    agents_de_la_periode = grouper_par(tickets_s2, "assignee")

    for agent in agents_de_la_periode:
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
# Onglet 7 : Produit
# ------------------------------------------------------------------

with onglet_produit:
    st.caption("Cadence trimestrielle recommandée — élargis la Période A dans la barre latérale pour une vraie tendance produit")

    tickets_sav_produit_s2 = categories_s2.get(CATEGORIE_SAV_PRODUIT, [])
    tickets_sav_produit_s1 = categories_s1.get(CATEGORIE_SAV_PRODUIT, [])

    st.subheader("Composant en cause (SAV produit uniquement)")

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

    lignes_composant_graphique = []
    for composant, tickets_composant in par_composant_s2.items():
        lignes_composant_graphique.append({"Composant": composant, "Tickets": len(tickets_composant)})
    lignes_composant_graphique_triees = sorted(lignes_composant_graphique, key=obtenir_tickets, reverse=True)
    tableau_composant_graphique = pd.DataFrame(lignes_composant_graphique_triees).set_index("Composant")
    st.bar_chart(tableau_composant_graphique, horizontal=True, color=COULEUR_PRIMAIRE)

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
    st.dataframe(lignes_composant_triees, hide_index=True, width="stretch")

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
    st.dataframe(lignes_produit_triees, hide_index=True, width="stretch")

    st.subheader("Type de résolution des SAV produit")
    st.caption("Beaucoup de \"conseil à distance\" = souci de compréhension d'usage plutôt qu'un vrai défaut. Beaucoup de remplacement = vrai défaut à corriger.")

    par_resolution = grouper_par(tickets_sav_produit_s2, "resolution_type")
    lignes_resolution = []
    for resolution, tickets_resolution in par_resolution.items():
        lignes_resolution.append({"Type de résolution": resolution, "Tickets": len(tickets_resolution)})

    lignes_resolution_triees = sorted(lignes_resolution, key=obtenir_tickets, reverse=True)
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
    st.dataframe(lignes_composant_issue_triees, hide_index=True, width="stretch")

    st.subheader("Garantie")

    par_garantie = grouper_par(tickets_sav_produit_s2, "warranty_status")
    lignes_garantie = []
    for garantie, tickets_garantie in par_garantie.items():
        lignes_garantie.append({"Statut garantie": garantie, "Tickets": len(tickets_garantie)})

    st.dataframe(lignes_garantie, hide_index=True, width="stretch")

    st.subheader("Délai entre achat et signalement SAV")
    st.caption("Un défaut précoce (moins de 30 jours après achat) évoque plutôt un défaut de fabrication ; un défaut tardif évoque plutôt de l'usure normale.")

    compte_anciennete = {}
    for ticket in tickets_sav_produit_s2:
        jours = delai_jours(ticket["order_date"], ticket["sav_reported_date"])
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

        colonne_rec_a, colonne_rec_b = st.columns(2)
        with colonne_rec_a:
            st.dataframe(lignes_produit_recurrent_triees, hide_index=True, width="stretch")
        with colonne_rec_b:
            st.dataframe(lignes_composant_recurrent_triees, hide_index=True, width="stretch")

        st.write("Clients à contacter en priorité (au moins 2 SAV avant celui-ci) :")

        recurrents_par_client = {}
        for ticket in tickets_recurrents:
            email_client = ticket["requester_email"]
            if email_client not in recurrents_par_client or ticket["created_at"] > recurrents_par_client[email_client]["created_at"]:
                recurrents_par_client[email_client] = ticket

        lignes_clients_recurrents = []
        for email_client, ticket_recent in recurrents_par_client.items():
            if ticket_recent["prior_sav_count"] < 2:
                continue

            lignes_clients_recurrents.append({
                "Client": email_client,
                "SAV au total": ticket_recent["prior_sav_count"] + 1,
                "Produit": ticket_recent["product_name"],
                "Composant": ticket_recent["component"],
                "Dernier ticket": ticket_recent["created_at"].strftime("%d/%m/%Y"),
            })

        if len(lignes_clients_recurrents) == 0:
            st.write("Aucun client avec 2 SAV ou plus avant celui-ci sur cette période.")
        else:
            def obtenir_sav_total(ligne):
                return ligne["SAV au total"]

            lignes_clients_recurrents_triees = sorted(lignes_clients_recurrents, key=obtenir_sav_total, reverse=True)
            st.dataframe(lignes_clients_recurrents_triees, hide_index=True, width="stretch")

    st.divider()
    st.subheader("Ventes par produit")
    st.caption(
        "Chiffre d'affaires par parfum (commandes, tout l'historique) croisé au volume de tickets sur "
        "la période affichée — pour repérer un parfum qui vend bien mais génère disproportionnellement "
        "du support. Montants € : données Shopify fictives (commandes_shopify_fictif.xlsx)."
    )

    ca_par_produit = {}
    for commande in commandes.values():
        produit_commande = commande["product_name"]
        if produit_commande in ca_par_produit:
            ca_par_produit[produit_commande] = ca_par_produit[produit_commande] + commande["montant_total"]
        else:
            ca_par_produit[produit_commande] = commande["montant_total"]

    tickets_par_produit_ventes = grouper_par(tickets_s2, "product_name")
    produits_ventes_a_afficher = cles_combinees(ca_par_produit, tickets_par_produit_ventes)

    lignes_produit_ventes = []
    for produit_nom in produits_ventes_a_afficher:
        lignes_produit_ventes.append({
            "produit": produit_nom,
            "ca": ca_par_produit.get(produit_nom, 0),
            "tickets": len(tickets_par_produit_ventes.get(produit_nom, [])),
        })

    def obtenir_ca(ligne):
        return ligne["ca"]

    lignes_produit_ventes_triees = sorted(lignes_produit_ventes, key=obtenir_ca, reverse=True)

    lignes_produit_ventes_affichage = []
    for ligne in lignes_produit_ventes_triees:
        lignes_produit_ventes_affichage.append({
            "Produit": ligne["produit"],
            "CA (historique)": formater_montant(ligne["ca"]),
            "Tickets (période)": ligne["tickets"],
        })

    st.dataframe(lignes_produit_ventes_affichage, hide_index=True, width="stretch")

    st.divider()
    st.subheader("Opportunités produit — demandes hors catalogue")
    st.caption(
        "Détecte automatiquement tout sujet marqué « (hors catalogue) » — une demande pour quelque chose "
        "qu'on ne vend pas (accessoire, personnalisation...). Élargis la Période A dans la barre latérale "
        "pour voir le seuil se déclencher sur des cadences plus longues."
    )

    seuil_opportunite = st.slider("Seuil de déclenchement (nombre de tickets sur la période)", 1, 20, 3)

    opportunites = detecter_opportunites_hors_catalogue(tickets_s2, seuil_opportunite)

    if len(opportunites) == 0:
        st.write("Aucune demande hors catalogue n'atteint le seuil sur cette période.")
    else:
        lignes_opportunites = []
        for sujet, tickets_sujet in opportunites:
            csat_opportunite = moyenne(tickets_sujet, "csat")
            ligne = {"Demande": sujet, "Tickets": len(tickets_sujet), "CSAT": "N/A"}
            if csat_opportunite is not None:
                ligne["CSAT"] = formater_csat(csat_opportunite)
            lignes_opportunites.append(ligne)

        lignes_opportunites_triees = sorted(lignes_opportunites, key=obtenir_tickets, reverse=True)
        st.dataframe(lignes_opportunites_triees, hide_index=True, width="stretch")
        st.write(
            "À remonter à l'équipe produit : ce sont des demandes récurrentes pour quelque chose qui "
            "n'existe pas encore au catalogue."
        )


# ------------------------------------------------------------------
# Onglet 8 : Livraison
# ------------------------------------------------------------------

with onglet_livraison:
    st.caption(
        "Miroir mensuel de la catégorie Livraison, pensé pour un point avec le transporteur — voir "
        "l'onglet Catégories pour la vue hebdomadaire toutes catégories confondues. Cadence mensuelle "
        "recommandée (élargis la Période A dans la barre latérale)."
    )

    tickets_livraison_s2 = categories_s2.get("Livraison", [])
    tickets_livraison_s1 = categories_s1.get("Livraison", [])

    volume_livraison_s2 = len(tickets_livraison_s2)
    csat_livraison_s2 = moyenne(tickets_livraison_s2, "csat")
    resolution_livraison_s2 = moyenne(tickets_livraison_s2, "full_resolution_time_hours")
    pct_livraison_global = volume_livraison_s2 / len(tickets_s2) * 100

    colonne_liv_a, colonne_liv_b, colonne_liv_c = st.columns(3)
    colonne_liv_a.metric("Tickets livraison", volume_livraison_s2, formater_pourcentage(pct_livraison_global) + " du volume global")
    if csat_livraison_s2 is not None:
        colonne_liv_b.metric("CSAT livraison", formater_csat(csat_livraison_s2))
    if resolution_livraison_s2 is not None:
        colonne_liv_c.metric("Résolution moyenne", formater_duree(resolution_livraison_s2 * 60))

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
    st.dataframe(lignes_livraison_triees, hide_index=True, width="stretch")

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
    st.dataframe(lignes_pays_livraison_triees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 10 : Conversion & acquisition
# ------------------------------------------------------------------

with onglet_conversion:
    st.caption(
        "Les montants € viennent d'un fichier Shopify FICTIF (commandes_shopify_fictif.xlsx), "
        "croisé aux tickets via order_id — Emyria est une marque fictive, ces chiffres sont des "
        "ordres de grandeur d'exemple pour la démonstration."
    )

    evenements_marketing = charger_calendrier_evenements(FICHIER_CALENDRIER)
    evenements_periode_actuelle = evenements_dans_periode(evenements_marketing, date_a_debut, date_a_fin)

    if len(evenements_periode_actuelle) > 0:
        st.subheader("Contexte marketing sur cette période")
        st.caption(
            "Campagnes et lancements en cours ou en chevauchement avec la période affichée — pour "
            "lire les chiffres de conversion et de volume avec ce contexte en tête."
        )

        lignes_evenements = []
        for evenement in evenements_periode_actuelle:
            reduction = evenement["reduction_pct"]
            if reduction is None:
                reduction_texte = "—"
            else:
                reduction_texte = "-" + str(reduction) + " %"

            lignes_evenements.append({
                "Événement": evenement["nom_evenement"],
                "Type": evenement["type"],
                "Dates": formater_plage(evenement["date_debut"], evenement["date_fin"]),
                "Canal": evenement["canal_diffusion"],
                "Réduction": reduction_texte,
                "Notes": evenement["notes"],
            })

        st.dataframe(lignes_evenements, hide_index=True, width="stretch")
        st.divider()

    st.subheader("Opportunités - avant-vente")
    st.caption("CSAT élevé = fort potentiel de conclure la vente ; CSAT bas = risque de perdre le prospect")

    tickets_avant_vente = categories_s2.get("Avant-vente / conseil", [])
    csat_avant_vente = moyenne(tickets_avant_vente, "csat")
    csat_global = moyenne(tickets_s2, "csat")
    pct_avant_vente = len(tickets_avant_vente) / len(tickets_s2) * 100

    index_commandes_email = commandes_par_email(commandes)

    resultats_conversion = []
    for ticket in tickets_avant_vente:
        commande = premiere_commande_apres(ticket, index_commandes_email, FENETRE_CONVERSION_JOURS)
        resultats_conversion.append((ticket, commande))

    conversion_par_sujet = {}
    for ticket, commande in resultats_conversion:
        sujet = ticket["subject_cluster"]
        if sujet not in conversion_par_sujet:
            conversion_par_sujet[sujet] = {"total": 0, "convertis": 0}
        conversion_par_sujet[sujet]["total"] = conversion_par_sujet[sujet]["total"] + 1
        if commande is not None:
            conversion_par_sujet[sujet]["convertis"] = conversion_par_sujet[sujet]["convertis"] + 1

    colonne_op_a, colonne_op_b = st.columns(2)
    colonne_op_a.metric("Tickets avant-vente", len(tickets_avant_vente), formater_pourcentage(pct_avant_vente) + " du volume global")

    if csat_avant_vente is not None and csat_global is not None:
        ecart_csat = round(csat_avant_vente - csat_global, 2)
        if ecart_csat >= 0:
            ecart_texte = "+" + str(ecart_csat) + " vs moyenne équipe"
        else:
            ecart_texte = str(ecart_csat) + " vs moyenne équipe"
        colonne_op_b.metric("CSAT avant-vente", formater_csat(csat_avant_vente), ecart_texte)

    sujets_av = grouper_par(tickets_avant_vente, "subject_cluster")
    lignes_av = []
    for sujet, tickets_sujet in sujets_av.items():
        csat_sujet = moyenne(tickets_sujet, "csat")
        ligne = {"Sujet": sujet, "Tickets": len(tickets_sujet), "CSAT": "N/A", "Taux de conversion": "N/A"}
        if csat_sujet is not None:
            ligne["CSAT"] = formater_csat(csat_sujet)

        compte_sujet = conversion_par_sujet.get(sujet)
        if compte_sujet is not None and compte_sujet["total"] > 0:
            taux_sujet = compte_sujet["convertis"] / compte_sujet["total"] * 100
            ligne["Taux de conversion"] = formater_pourcentage(taux_sujet)

        lignes_av.append(ligne)

    lignes_av_triees = sorted(lignes_av, key=obtenir_tickets, reverse=True)
    afficher_tableau_colore(lignes_av_triees)
    st.caption(
        "Taux de conversion réel par sujet (pas une estimation à partir du CSAT) — pour voir quelles "
        "demandes avant-vente convertissent le mieux, indépendamment de leur volume ou de leur note."
    )

    st.divider()
    st.subheader("Conversion / ré-achat après contact avant-vente")
    st.caption(
        "Fenêtre de " + str(FENETRE_CONVERSION_JOURS) + " jours glissants après le ticket. Rapproché par "
        "e-mail avec la commande la plus proche dans cette fenêtre (fichier Shopify fictif) — méthode "
        "réaliste, mais qui peut compter par coïncidence une commande sans lien réel avec le contact "
        "(client avec plusieurs tickets rapprochés dans le temps). À garder en tête en lisant les chiffres."
    )

    nombre_convertis = 0
    delais = []
    montants = []
    for ticket, commande in resultats_conversion:
        if commande is not None:
            nombre_convertis = nombre_convertis + 1
            delais.append((commande["order_date"] - ticket["created_at"]).days)
            montants.append(commande["montant_total"])

    if len(tickets_avant_vente) > 0:
        taux_conversion = nombre_convertis / len(tickets_avant_vente) * 100

        colonne_cv_a, colonne_cv_b, colonne_cv_c = st.columns(3)
        colonne_cv_a.metric("Taux de conversion (" + str(FENETRE_CONVERSION_JOURS) + "j)", formater_pourcentage(taux_conversion))
        if len(delais) > 0:
            colonne_cv_b.metric("Délai moyen avant achat", str(round(sum(delais) / len(delais), 1)) + " j")
        if len(montants) > 0:
            colonne_cv_c.metric("Panier moyen (converti)", formater_montant(sum(montants) / len(montants)))

    st.write("Par CSAT du ticket avant-vente :")

    par_csat_conversion = {}
    for ticket, commande in resultats_conversion:
        csat = ticket["csat"]
        if csat not in par_csat_conversion:
            par_csat_conversion[csat] = {"total": 0, "convertis": 0}
        par_csat_conversion[csat]["total"] = par_csat_conversion[csat]["total"] + 1
        if commande is not None:
            par_csat_conversion[csat]["convertis"] = par_csat_conversion[csat]["convertis"] + 1

    lignes_conversion_csat = []
    for csat, compte in par_csat_conversion.items():
        if csat is None:
            csat_texte = "Pas de note"
        else:
            csat_texte = str(csat)

        taux = compte["convertis"] / compte["total"] * 100

        lignes_conversion_csat.append(
            {
                "CSAT": csat_texte,
                "Tickets": compte["total"],
                "Convertis": compte["convertis"],
                "Taux de conversion": formater_pourcentage(taux),
                "Taux (valeur)": round(taux, 1),
            }
        )

    def obtenir_csat_pour_tri(ligne):
        if ligne["CSAT"] == "Pas de note":
            return -1
        return int(ligne["CSAT"])

    lignes_conversion_csat_triees = sorted(lignes_conversion_csat, key=obtenir_csat_pour_tri, reverse=True)

    lignes_conversion_csat_notees = []
    for ligne in lignes_conversion_csat_triees:
        if ligne["CSAT"] != "Pas de note":
            lignes_conversion_csat_notees.append(ligne)
    lignes_conversion_csat_croissant = sorted(lignes_conversion_csat_notees, key=obtenir_csat_pour_tri)

    tableau_conversion_csat_graphique = pd.DataFrame(lignes_conversion_csat_croissant)[["CSAT", "Taux (valeur)"]].set_index("CSAT")
    st.bar_chart(tableau_conversion_csat_graphique, color=COULEUR_PRIMAIRE, y_label="Taux de conversion (%)")

    lignes_conversion_csat_affichage = []
    for ligne in lignes_conversion_csat_triees:
        lignes_conversion_csat_affichage.append(
            {
                "CSAT": ligne["CSAT"],
                "Tickets": ligne["Tickets"],
                "Convertis": ligne["Convertis"],
                "Taux de conversion": ligne["Taux de conversion"],
            }
        )

    st.dataframe(lignes_conversion_csat_affichage, hide_index=True, width="stretch")
    st.caption("Échantillons parfois petits par note (ex : CSAT 1 ou 2) — à lire comme une tendance, pas un chiffre définitif.")

    st.write("Par agent :")
    st.caption("Clique sur l'en-tête d'une colonne pour trier par nombre de conversions ou par CA généré")

    par_agent_conversion = {}
    for ticket, commande in resultats_conversion:
        agent = ticket["assignee"]
        if agent not in par_agent_conversion:
            par_agent_conversion[agent] = {"total": 0, "convertis": 0, "montants": []}
        par_agent_conversion[agent]["total"] = par_agent_conversion[agent]["total"] + 1
        if commande is not None:
            par_agent_conversion[agent]["convertis"] = par_agent_conversion[agent]["convertis"] + 1
            par_agent_conversion[agent]["montants"].append(commande["montant_total"])

    lignes_agent_conversion = []
    for agent, stats in par_agent_conversion.items():
        taux_agent = stats["convertis"] / stats["total"] * 100
        ca_genere = sum(stats["montants"])

        lignes_agent_conversion.append(
            {
                "Agent": agent,
                "Tickets avant-vente": stats["total"],
                "Convertis": stats["convertis"],
                "Taux de conversion": formater_pourcentage(taux_agent),
                "CA généré": formater_montant(ca_genere),
            }
        )

    def obtenir_convertis(ligne):
        return ligne["Convertis"]

    lignes_agent_conversion_triees = sorted(lignes_agent_conversion, key=obtenir_convertis, reverse=True)
    st.dataframe(lignes_agent_conversion_triees, hide_index=True, width="stretch")

    montants_silencieux = []
    for order_id in commandes:
        commande = commandes[order_id]
        if commande["a_genere_ticket"] == "Non" and commande["ticket_conversion"] is None:
            montants_silencieux.append(commande["montant_total"])

    if len(montants_silencieux) > 0 and len(montants) > 0:
        st.write(
            "Panier moyen d'une commande sans aucun contact support : "
            + formater_montant(sum(montants_silencieux) / len(montants_silencieux))
            + " (vs " + formater_montant(sum(montants) / len(montants)) + " après contact avant-vente converti)"
        )

    st.divider()
    st.subheader("Par canal d'acquisition")
    st.caption(
        "Origine client (fichier Shopify) croisée avec le coût d'acquisition (CAC estimé, hypothèse "
        "fictive illustrative), le contact support et le CSAT — sur tout l'historique disponible, comme "
        "les commandes ci-dessus (pas filtré par la période affichée)."
    )

    tickets_par_id = {}
    for ticket in tickets_historique_business:
        tickets_par_id[ticket["ticket_id"]] = ticket

    par_canal = {}
    for commande in commandes.values():
        canal = commande["canal_acquisition"]
        if canal not in par_canal:
            par_canal[canal] = {"commandes": 0, "avec_contact": 0, "convertis_avant_vente": [], "montants": []}

        par_canal[canal]["commandes"] = par_canal[canal]["commandes"] + 1
        if commande["a_genere_ticket"] == "Oui":
            par_canal[canal]["avec_contact"] = par_canal[canal]["avec_contact"] + 1

        if commande["ticket_conversion"] is not None:
            ticket_lie = tickets_par_id.get(commande["ticket_conversion"])
            if ticket_lie is not None:
                par_canal[canal]["convertis_avant_vente"].append(ticket_lie)

        par_canal[canal]["montants"].append(commande["montant_total"])

    lignes_canal = []
    for canal, donnees in par_canal.items():
        taux_contact = donnees["avec_contact"] / donnees["commandes"] * 100
        csat_convertis = moyenne(donnees["convertis_avant_vente"], "csat")
        panier_moyen = sum(donnees["montants"]) / len(donnees["montants"])
        cac = COUT_ACQUISITION_PAR_CANAL.get(canal, 0)

        ligne = {
            "Canal": canal,
            "Commandes": donnees["commandes"],
            "CAC estimé": formater_montant(cac),
            "Panier moyen": formater_montant(panier_moyen),
            "Marge après CAC": formater_montant(panier_moyen - cac),
            "% avec contact support avant achat": formater_pourcentage(taux_contact),
            "Conversions avant-vente liées": len(donnees["convertis_avant_vente"]),
            "CSAT de ces conversions": "N/A",
        }
        if csat_convertis is not None:
            ligne["CSAT de ces conversions"] = formater_csat(csat_convertis)

        lignes_canal.append(ligne)

    def obtenir_commandes_canal(ligne):
        return ligne["Commandes"]

    lignes_canal_triees = sorted(lignes_canal, key=obtenir_commandes_canal, reverse=True)
    st.dataframe(lignes_canal_triees, hide_index=True, width="stretch")

    st.divider()
    st.subheader("Par pays (poids support vs poids commandes)")
    st.caption(
        "Tickets de la période affichée comparés aux commandes de tout l'historique (comme les autres "
        "sections ci-dessus) — un écart marqué signale que les clients d'un pays sollicitent le support "
        "disproportionnellement plus (ou moins) que leur poids réel dans les ventes."
    )

    tickets_par_pays = grouper_par(tickets_s2, "country")
    commandes_par_pays = {}
    for commande in commandes.values():
        pays = commande["pays"]
        if pays in commandes_par_pays:
            commandes_par_pays[pays] = commandes_par_pays[pays] + 1
        else:
            commandes_par_pays[pays] = 1

    pays_a_afficher = cles_combinees(tickets_par_pays, commandes_par_pays)

    lignes_pays_business = []
    for pays in pays_a_afficher:
        nb_tickets = len(tickets_par_pays.get(pays, []))
        nb_commandes = commandes_par_pays.get(pays, 0)
        pct_tickets = nb_tickets / len(tickets_s2) * 100
        pct_commandes = nb_commandes / len(commandes) * 100

        lignes_pays_business.append({
            "Pays": pays,
            "Tickets (période)": nb_tickets,
            "% des tickets": formater_pourcentage(pct_tickets),
            "Commandes (historique)": nb_commandes,
            "% des commandes": formater_pourcentage(pct_commandes),
            "Écart (points)": round(pct_tickets - pct_commandes, 1),
        })

    def obtenir_tickets_periode(ligne):
        return ligne["Tickets (période)"]

    lignes_pays_business_triees = sorted(lignes_pays_business, key=obtenir_tickets_periode, reverse=True)
    st.dataframe(lignes_pays_business_triees, hide_index=True, width="stretch")


# ------------------------------------------------------------------
# Onglet 11 : Impact & confiance
# ------------------------------------------------------------------

with onglet_impact:
    st.caption("Montants € : mêmes données Shopify fictives que l'onglet Conversion & acquisition.")

    st.subheader("Fidélisation & réachat")
    st.caption(
        "Sur tout l'historique des commandes (pas filtré par la période affichée) — pour voir si une "
        "bonne expérience support se traduit en réachat."
    )

    commandes_par_client = {}
    for commande in commandes.values():
        email = commande["email_client"]
        if email in commandes_par_client:
            commandes_par_client[email].append(commande)
        else:
            commandes_par_client[email] = [commande]

    nb_clients_total = len(commandes_par_client)
    nb_clients_repeat = 0
    for email, liste_client in commandes_par_client.items():
        if len(liste_client) >= 2:
            nb_clients_repeat = nb_clients_repeat + 1

    taux_reachat = nb_clients_repeat / nb_clients_total * 100

    colonne_fid_a, colonne_fid_b = st.columns(2)
    colonne_fid_a.metric("Clients avec au moins 2 commandes", nb_clients_repeat, formater_pourcentage(taux_reachat) + " des clients")
    colonne_fid_b.metric("Total clients (historique)", nb_clients_total)

    repartition_commandes = {}
    for email, liste_client in commandes_par_client.items():
        nb_commandes_client = len(liste_client)
        if nb_commandes_client >= 5:
            cle_repartition = "5+"
        else:
            cle_repartition = str(nb_commandes_client)

        if cle_repartition in repartition_commandes:
            repartition_commandes[cle_repartition] = repartition_commandes[cle_repartition] + 1
        else:
            repartition_commandes[cle_repartition] = 1

    ordre_cles_repartition = ["1", "2", "3", "4", "5+"]
    lignes_repartition = []
    for cle_repartition in ordre_cles_repartition:
        if cle_repartition in repartition_commandes:
            lignes_repartition.append({"Nombre de commandes": cle_repartition, "Clients": repartition_commandes[cle_repartition]})

    tableau_repartition = pd.DataFrame(lignes_repartition).set_index("Nombre de commandes")
    st.bar_chart(tableau_repartition, color=COULEUR_PRIMAIRE)

    st.write("CSAT support des clients ayant eu au moins un contact, par statut de fidélité :")

    csat_historique_par_email = {}
    for ticket in tickets_historique_business:
        email_ticket = ticket["requester_email"]
        csat_ticket = ticket["csat"]
        if csat_ticket is None:
            continue
        if email_ticket not in csat_historique_par_email:
            csat_historique_par_email[email_ticket] = []
        csat_historique_par_email[email_ticket].append(csat_ticket)

    csats_repeat = []
    csats_onetime = []
    for email, liste_client in commandes_par_client.items():
        csats_client = csat_historique_par_email.get(email)
        if csats_client is None or len(csats_client) == 0:
            continue
        csat_moyen_client = sum(csats_client) / len(csats_client)
        if len(liste_client) >= 2:
            csats_repeat.append(csat_moyen_client)
        else:
            csats_onetime.append(csat_moyen_client)

    lignes_fidelite_csat = []
    if len(csats_onetime) > 0:
        lignes_fidelite_csat.append({
            "Segment": "Client à commande unique",
            "Clients (avec contact support)": len(csats_onetime),
            "CSAT moyen": formater_csat(sum(csats_onetime) / len(csats_onetime)),
        })
    if len(csats_repeat) > 0:
        lignes_fidelite_csat.append({
            "Segment": "Client avec réachat (2+ commandes)",
            "Clients (avec contact support)": len(csats_repeat),
            "CSAT moyen": formater_csat(sum(csats_repeat) / len(csats_repeat)),
        })

    st.dataframe(lignes_fidelite_csat, hide_index=True, width="stretch")
    st.caption("Échantillon limité aux clients ayant eu au moins un contact support noté — les autres n'ont pas de point de comparaison.")

    st.divider()
    st.subheader("Pertes financières directes")
    st.caption("Basé sur le type de résolution du ticket, montant croisé avec la commande d'origine (fichier Shopify fictif)")

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
    for type_perte, tickets_perte in groupes_perte.items():
        pct_perte = len(tickets_perte) / len(tickets_s2) * 100

        montants = []
        for ticket in tickets_perte:
            montant = montant_ticket(ticket, commandes)
            if montant is not None:
                montants.append(montant)

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
    st.dataframe(lignes_perte_triees, hide_index=True, width="stretch")

    if montant_total_pertes > 0:
        st.metric("Total pertes financières directes estimées", formater_montant(montant_total_pertes))

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
        for ticket in tickets_garantie:
            montant = montant_ticket(ticket, commandes)
            if montant is not None:
                montants_garantie.append(montant)

        if len(montants_garantie) > 0:
            st.metric("Valeur des produits sous garantie concernés", formater_montant(sum(montants_garantie)))

    st.divider()
    st.subheader("Pertes de confiance")
    st.caption(
        "Un CSAT bas ne pèse pas pareil selon le sujet : sur un défaut produit, c'est le produit ET "
        "la marque qui trinquent ; sur une livraison, c'est la marque seule ; en avant-vente, c'est "
        "une conversion perdue."
    )

    lignes_confiance = []
    for categorie, tickets_cat in categories_s2.items():
        csat_cat = moyenne(tickets_cat, "csat")
        if csat_cat is None or csat_cat >= SEUIL_CSAT_INSATISFAISANT:
            continue

        lignes_confiance.append(
            {
                "Catégorie": categorie,
                "Tickets": len(tickets_cat),
                "CSAT": formater_csat(csat_cat),
                "Niveau CSAT": niveau_csat(csat_cat),
                "Ce qui est en jeu": cible_perte_confiance(categorie),
            }
        )

    lignes_confiance_triees = sorted(lignes_confiance, key=obtenir_tickets, reverse=True)
    afficher_tableau_colore(lignes_confiance_triees)

    st.divider()
    st.subheader("Confiance mesurée (NPS)")
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

    colonne_nps_a, colonne_nps_b, colonne_nps_c = st.columns(3)
    if nps_global is not None:
        colonne_nps_a.metric("NPS global", round(nps_global, 1))
    if nps_contactes is not None:
        colonne_nps_b.metric("NPS - a contacté le support", round(nps_contactes, 1))
    if nps_non_contactes is not None:
        colonne_nps_c.metric("NPS - jamais contacté (référence)", round(nps_non_contactes, 1))

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
    st.altair_chart(graphique_nps, width="stretch")
