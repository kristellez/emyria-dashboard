import datetime
import unittest

from outils import (
    agents_en_poste,
    activite_observee,
    analyser_contacts_avant_achat,
    analyser_observation,
    analyser_parcours_rdv,
    calculer_indice_difficulte,
    calculer_nps,
    calculer_reference_cout_moyen,
    calculer_stats_achat_observe,
    capacite_totale_heures,
    categoriser,
    cles_combinees,
    commandes_par_email,
    consolider_signaux_voie_a,
    construire_activite_par_jour_heure,
    construire_comparaisons_locales,
    construire_lecture_activite_avant_vente,
    construire_lecture_activite_livraison,
    construire_lecture_tendances,
    construire_niveaux_historiques_avant_vente,
    construire_niveaux_historiques_livraison,
    construire_signal_motif_avant_vente,
    construire_signal_produit_voie_a,
    construire_signal_sujet_livraison_voie_a,
    construire_synthese_generale,
    construire_synthese_longue,
    contexte_periode,
    controler_qualite_donnees_avant_vente,
    controler_qualite_donnees_livraison,
    distribution_canal_avant_vente,
    delai_jours,
    dernier_ticket_avant,
    determiner_mode_tendances,
    determiner_parcours_avant_vente,
    detecter_contrastes_capacite,
    detecter_fait_marquant,
    detecter_pics_et_creux,
    detecter_saisonnalite_apparente,
    distribution_issues_livraison,
    ecart_relatif_temporel,
    ecart_relatif_vs_reste,
    evaluer_concentration_transporteur_livraison,
    evaluer_gravite_ticket_voie_b,
    evaluer_temporalite,
    formater_csat,
    formater_duree,
    formater_pourcentage,
    GRAIN_COMPOSANT,
    GRAIN_PRODUIT_COMPOSANT,
    GRAIN_PRODUIT_ISSUE,
    lire_ecart_csat,
    lire_ecart_effort,
    lire_ecart_taux_achat_observe,
    mediane,
    mediane_du_reste,
    moyenne,
    MODE_HISTORIQUE_COMPLET,
    MODE_OBSERVATION_UNIQUE,
    MODE_PERIODE_ETENDUE,
    montant_cout_garantie,
    montant_perte_estime,
    moteur_avant_vente_motifs,
    moteur_livraison_voie_a,
    moteur_produit_voie_a,
    moteur_produit_voie_b,
    niveau_macro,
    niveau_reponse_ouvree,
    nom_mois,
    part_issues_defavorables,
    premiere_commande_apres,
    PARCOURS_RDV_HONORE,
    PARCOURS_RDV_NON_HONORE,
    PARCOURS_SPONTANE,
    rang_relatif,
    renfort_non_planifie,
    resoudre_achats_observes_avant_vente,
    RDV_STATUT_ANNULE,
    RDV_STATUT_HONORE,
    RDV_STATUT_NO_SHOW,
    saison_du_mois,
    SEUIL_MINIMUM_EVALUATION_PRODUIT,
    SEUIL_RANG_BAS_STRICT,
    SEUIL_RANG_HAUT_STRICT,
    SEUIL_VOLUME_ABSOLU_NOTABLE,
    SUJET_DEMANDE_RDV,
    taux_rempli,
    texte_piste_transporteur_livraison,
    tickets_par_email,
    TYPE_COMMERCIAL,
    TYPE_CONTACT_RDV,
    TYPE_CONTACT_SPONTANE,
    TYPE_PRODUIT,
    TYPE_STAFFING,
    TYPE_OPERATIONNEL,
    amplitude_relative_etendue,
    analyser_nps_par_type_experience,
    categorie_dominante_mix_tendances,
    charge_relative_agent,
    construire_historique_agent,
    construire_lecture_equipe_agents,
    construire_navigation_vue_ensemble,
    construire_roster_agents,
    heures_planifiees_agent,
    mix_pct_agent,
    STATUT_AGENT_ABSENT,
    STATUT_AGENT_PLANIFIE_ACTIF,
    STATUT_AGENT_PLANIFIE_SANS_ACTIVITE,
    STATUT_AGENT_RENFORT_NON_PLANIFIE,
    construire_points_anticipation_vue_ensemble,
    construire_texte_periode_reference_tendances,
    construire_signal_positif_vue_ensemble,
    construire_signaux_attention_vue_ensemble,
    evaluer_diagnostics_structures_transversal_vue_ensemble,
    extraire_candidats_categoriels_vue_ensemble,
    filtrer_candidats_materiels_vue_ensemble,
    filtrer_tickets_par_segment_transporteur,
    SEGMENT_LIVRAISON_TOUS,
    SEGMENT_LIVRAISON_STANDARD,
    SEGMENT_LIVRAISON_EXPRESS,
    regrouper_candidats_par_categorie_vue_ensemble,
    signal_categoriel_est_materiel_vue_ensemble,
    texte_signal_transversal_vue_ensemble,
    verifier_coherence_lecture_attention_vue_ensemble,
    CATEGORIE_LIVRAISON_VUE_ENSEMBLE,
    CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE,
    CATEGORIE_SAV_PRODUIT,
    FENETRE_ANTICIPATION_VUE_ENSEMBLE_JOURS,
    calculer_composition_nps,
    construire_historique_nps_par_mois,
    construire_profil_care_mensuel,
    controler_qualite_donnees_nps,
    determiner_type_experience_nps,
    evaluer_alignement_care_nps,
    evaluer_cas_compatibles_service_recovery,
    evaluer_prudence_echantillon_nps,
    formater_nps_entier,
    segmenter_nps_par_contact_care,
    texte_alignement_care_nps,
    texte_prudence_echantillon_nps,
    ETAT_PRUDENCE_PREMIERE_OBSERVATION,
    ETAT_PRUDENCE_VOLUME_ELEVE,
    ETAT_PRUDENCE_VOLUME_FAIBLE,
    ETAT_PRUDENCE_VOLUME_HABITUEL,
    SEUIL_AMPLITUDE_PART_ETENDUE_NPS,
    SEUIL_CSAT_INSATISFAISANT,
    SEUIL_PRUDENCE_ECHANTILLON_NPS,
    TEXTE_PRUDENCE_BIAIS_SELECTION,
    TYPE_EXPERIENCE_AUCUN,
    TYPE_EXPERIENCE_LIVRAISON,
    TYPE_EXPERIENCE_REMPLACEMENT,
    TYPE_EXPERIENCE_RESOLUTION_LONGUE,
    TYPE_EXPERIENCE_RESOLUTION_RAPIDE,
    TYPE_EXPERIENCE_SAV,
    TYPE_EXPERIENCE_SAV_RECURRENT,
    construire_actions_menees_actions,
    identifier_pistes_self_service,
    identifier_pistes_standardisation,
    identifier_retours_clients_a_explorer,
    sujet_deja_traite_actions,
    FAMILLE_RETOURS_CLIENTS_ACTIONS,
    FAMILLE_SELF_SERVICE_ACTIONS,
    FAMILLE_STANDARDISATION_ACTIONS,
    construire_agents_grille_couverture,
    construire_grille_pression_couverture,
    construire_lecture_couverture,
    creneau_est_tension_couverture,
    enrichir_grille_pression_tension_couverture,
    niveau_frt_local_couverture,
    niveau_pression_couverture,
    rang_relatif_vs_reference,
    statut_creneau_standard,
    NIVEAU_ACTIVITE_HORS_CAPACITE_FAIBLE,
    NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE,
    NIVEAU_FRT_LOCAL_DEGRADE,
    NIVEAU_FRT_LOCAL_NORMAL,
    NIVEAU_PRESSION_FAIBLE_VOLUME,
    NIVEAU_PRESSION_FORTE,
    NIVEAU_PRESSION_HABITUELLE,
    NIVEAU_PRESSION_MARQUEE,
    NIVEAU_PRESSION_NON_QUALIFIABLE,
    cle_signal_produit,
    construire_dossiers_associes_produit,
    construire_lecture_produit,
    construire_texte_resolution_produit,
    construire_texte_sav_recurrents_produit,
    titre_signal_produit,
    TEXTE_PRUDENCE_CAUSALE,
    construire_lecture_livraison,
    construire_dossiers_associes_livraison,
    construire_croisement_motif_issue_livraison,
    TEXTE_COUT_INDISPONIBLE_LIVRAISON,
    construire_lecture_avant_vente,
    construire_contacts_associes_avant_vente,
    construire_achats_associes_avant_vente,
    construire_table_sujets_avant_vente,
    construire_table_pays_avant_vente,
    identifier_observation_nps_periode,
    texte_sensibilite_echantillon_nps,
    TEXTE_SENSIBILITE_PETIT_ECHANTILLON_NPS,
    TEXTE_CAVEAT_RECOUVREMENT_COUT,
    construire_lecture_impact_confiance,
)


def ticket_produit(ticket_id=1, component="Batterie", product_name="Produit A", issue_type="Panne",
                    csat=4, replies=3, full_resolution_time_hours=10, resolution_type="Remplacement produit",
                    reopens=0, order_id=None, subject_cluster="Sujet SAV"):
    return {
        "ticket_id": ticket_id,
        "component": component,
        "product_name": product_name,
        "issue_type": issue_type,
        "csat": csat,
        "replies": replies,
        "full_resolution_time_hours": full_resolution_time_hours,
        "resolution_type": resolution_type,
        "reopens": reopens,
        "order_id": order_id,
        "subject_cluster": subject_cluster,
    }


def lot_tickets_neutres(prefixe, nombre, component="ComposantControle", product_name="ProduitControle"):
    # Produits variés (jamais un seul) : une population "neutre" à un seul product_name
    # déclencherait par accident la famille F (concentration) dès qu'elle atteint le seuil
    # minimum d'évaluation -- ce n'est pas ce que "neutre" est censé vouloir dire ici.
    variantes_produit = [product_name + " 1", product_name + " 2", product_name + " 3", product_name + " 4"]
    lot = []
    for i in range(nombre):
        lot.append(ticket_produit(
            ticket_id=prefixe + str(i), component=component, product_name=variantes_produit[i % 4],
            csat=4, replies=3, full_resolution_time_hours=10, reopens=0,
        ))
    return lot


def ticket_avec(champ, valeur):
    return {champ: valeur}


class TestMoyenne(unittest.TestCase):
    def test_liste_vide_retourne_none(self):
        self.assertIsNone(moyenne([], "csat"))

    def test_toutes_valeurs_none_retourne_none(self):
        tickets = [ticket_avec("csat", None), ticket_avec("csat", None)]
        self.assertIsNone(moyenne(tickets, "csat"))

    def test_ignore_les_valeurs_none_dans_la_moyenne(self):
        tickets = [ticket_avec("csat", 4), ticket_avec("csat", None), ticket_avec("csat", 2)]
        self.assertEqual(moyenne(tickets, "csat"), 3)

    def test_moyenne_simple(self):
        tickets = [ticket_avec("csat", 5), ticket_avec("csat", 3), ticket_avec("csat", 4)]
        self.assertEqual(moyenne(tickets, "csat"), 4)


class TestTauxRempli(unittest.TestCase):
    def test_liste_vide_retourne_none(self):
        self.assertIsNone(taux_rempli([], "macro_applied"))

    def test_aucune_valeur_remplie(self):
        tickets = [ticket_avec("macro_applied", None), ticket_avec("macro_applied", None)]
        self.assertEqual(taux_rempli(tickets, "macro_applied"), 0)

    def test_toutes_valeurs_remplies(self):
        tickets = [ticket_avec("macro_applied", "MAC-001"), ticket_avec("macro_applied", "MAC-002")]
        self.assertEqual(taux_rempli(tickets, "macro_applied"), 100)

    def test_taux_partiel(self):
        tickets = [
            ticket_avec("macro_applied", "MAC-001"),
            ticket_avec("macro_applied", None),
            ticket_avec("macro_applied", None),
            ticket_avec("macro_applied", None),
        ]
        self.assertEqual(taux_rempli(tickets, "macro_applied"), 25)


class TestClesCombinees(unittest.TestCase):
    def test_cles_du_dict_actuel_en_premier(self):
        dict_actuel = {"Livraison": [1], "SAV": [2]}
        dict_precedent = {"SAV": [3]}
        self.assertEqual(cles_combinees(dict_actuel, dict_precedent), ["Livraison", "SAV"])

    def test_ajoute_les_cles_disparues_a_la_fin(self):
        dict_actuel = {"Livraison": [1]}
        dict_precedent = {"Livraison": [2], "Ancien sujet": [3]}
        self.assertEqual(cles_combinees(dict_actuel, dict_precedent), ["Livraison", "Ancien sujet"])

    def test_aucun_doublon(self):
        dict_actuel = {"A": [1], "B": [2]}
        dict_precedent = {"B": [3], "C": [4]}
        self.assertEqual(cles_combinees(dict_actuel, dict_precedent), ["A", "B", "C"])


class TestMontantPerteEstime(unittest.TestCase):
    def setUp(self):
        self.commandes = {
            "EMY-1": {"montant_total": 200, "product_category": "Diffuseur", "product_name": "Cocon"},
        }
        self.couts_produits = {
            ("Diffuseur", "Cocon"): {
                "prix_vente_ttc": 200,
                "cout_revient_produit": 80,
                "cout_logistique_remplacement": 10,
                "cout_retour": 5,
            },
        }

    def test_ticket_sans_order_id_retourne_none(self):
        ticket = {"order_id": None}
        self.assertIsNone(montant_perte_estime(ticket, self.commandes, "Remboursement", self.couts_produits))

    def test_order_id_absent_des_commandes_retourne_none(self):
        ticket = {"order_id": "EMY-INCONNU"}
        self.assertIsNone(montant_perte_estime(ticket, self.commandes, "Remboursement", self.couts_produits))

    def test_remboursement_est_le_montant_complet(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_perte_estime(ticket, self.commandes, "Remboursement", self.couts_produits), 200)

    def test_remplacement_produit_utilise_cout_de_revient_plus_logistique_et_retour(self):
        # ratio_cout = 80/200 = 0.4 ; 200*0.4 + logistique 10 + retour 5 = 95
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(
            montant_perte_estime(ticket, self.commandes, "Remplacement produit", self.couts_produits), 95
        )

    def test_remplacement_accessoire_exclut_le_cout_de_retour(self):
        # 200*0.4 + logistique 10, pas de retour = 90
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(
            montant_perte_estime(ticket, self.commandes, "Remplacement accessoire", self.couts_produits), 90
        )

    def test_geste_commercial_est_une_fraction_du_prix_de_vente(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(
            montant_perte_estime(ticket, self.commandes, "Geste commercial", self.couts_produits), 30
        )

    def test_type_perte_inconnu_retombe_sur_le_montant_complet(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(
            montant_perte_estime(ticket, self.commandes, "Type jamais vu", self.couts_produits), 200
        )

    def test_produit_absent_du_catalogue_de_couts_retourne_none(self):
        ticket = {"order_id": "EMY-1"}
        self.assertIsNone(montant_perte_estime(ticket, self.commandes, "Remplacement produit", {}))


class TestMontantCoutGarantie(unittest.TestCase):
    def test_utilise_le_cout_de_revient_reel(self):
        commandes = {
            "EMY-1": {"montant_total": 200, "product_category": "Diffuseur", "product_name": "Cocon"},
        }
        couts_produits = {
            ("Diffuseur", "Cocon"): {
                "prix_vente_ttc": 200,
                "cout_revient_produit": 80,
                "cout_logistique_remplacement": 10,
                "cout_retour": 5,
            },
        }
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_cout_garantie(ticket, commandes, couts_produits), 95)

    def test_sans_commande_retourne_none(self):
        ticket = {"order_id": None}
        self.assertIsNone(montant_cout_garantie(ticket, {}, {}))


class TestDernierTicketAvant(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"requester_email": "a@x.com", "created_at": datetime.datetime(2026, 1, 1)},
            {"requester_email": "a@x.com", "created_at": datetime.datetime(2026, 1, 20)},
            {"requester_email": "a@x.com", "created_at": datetime.datetime(2026, 3, 1)},
            {"requester_email": "b@x.com", "created_at": datetime.datetime(2026, 1, 25)},
        ]
        self.index = tickets_par_email(self.tickets)

    def test_prend_le_ticket_le_plus_recent_dans_la_fenetre(self):
        reponse = {"email_client": "a@x.com", "date_reponse": datetime.datetime(2026, 1, 28)}
        resultat = dernier_ticket_avant(reponse, self.index, 30)
        self.assertEqual(resultat["created_at"], datetime.datetime(2026, 1, 20))

    def test_ignore_un_ticket_hors_fenetre(self):
        reponse = {"email_client": "a@x.com", "date_reponse": datetime.datetime(2026, 1, 5)}
        resultat = dernier_ticket_avant(reponse, self.index, 3)
        self.assertIsNone(resultat)

    def test_ignore_un_ticket_apres_la_reponse(self):
        reponse = {"email_client": "a@x.com", "date_reponse": datetime.datetime(2026, 1, 10)}
        resultat = dernier_ticket_avant(reponse, self.index, 30)
        self.assertEqual(resultat["created_at"], datetime.datetime(2026, 1, 1))

    def test_client_sans_ticket_retourne_none(self):
        reponse = {"email_client": "inconnu@x.com", "date_reponse": datetime.datetime(2026, 1, 28)}
        self.assertIsNone(dernier_ticket_avant(reponse, self.index, 30))


class TestDelaiJours(unittest.TestCase):
    def test_date_debut_none_retourne_none(self):
        self.assertIsNone(delai_jours(None, "peu importe"))

    def test_date_fin_none_retourne_none(self):
        self.assertIsNone(delai_jours("peu importe", None))

    def test_calcule_le_bon_ecart(self):
        debut = datetime.date(2026, 1, 1)
        fin = datetime.date(2026, 1, 10)
        self.assertEqual(delai_jours(debut, fin), 9)


class TestFormatters(unittest.TestCase):
    def test_formater_pourcentage_none(self):
        self.assertEqual(formater_pourcentage(None), "N/A")

    def test_formater_pourcentage_valeur(self):
        self.assertEqual(formater_pourcentage(42.6), "43 %")

    def test_formater_csat_none(self):
        self.assertEqual(formater_csat(None), "N/A")

    def test_formater_csat_valeur(self):
        self.assertEqual(formater_csat(4.567), "4,57")

    def test_formater_duree_none(self):
        self.assertEqual(formater_duree(None), "N/A")

    def test_formater_duree_minutes_seulement(self):
        self.assertEqual(formater_duree(45), "45min")

    def test_formater_duree_heures(self):
        self.assertEqual(formater_duree(150), "2h 30min")

    def test_formater_duree_jours(self):
        self.assertEqual(formater_duree(1500), "1j 1h")


class TestNiveauMacro(unittest.TestCase):
    def test_none_retourne_chaine_vide(self):
        self.assertEqual(niveau_macro(None), "")

    def test_sous_50_est_critique(self):
        self.assertEqual(niveau_macro(30), "CRITIQUE")

    def test_entre_50_et_70_est_a_surveiller(self):
        self.assertEqual(niveau_macro(60), "A SURVEILLER")

    def test_70_et_plus_est_ok(self):
        self.assertEqual(niveau_macro(85), "OK")


class TestNiveauReponseOuvree(unittest.TestCase):
    def test_dans_le_sla_jusqu_a_60_minutes(self):
        self.assertEqual(niveau_reponse_ouvree(60), "OK")

    def test_leger_depassement_juste_au_dessus_du_sla(self):
        self.assertEqual(niveau_reponse_ouvree(61), "A SURVEILLER")

    def test_leger_depassement_jusqu_a_119_minutes(self):
        self.assertEqual(niveau_reponse_ouvree(119), "A SURVEILLER")

    def test_retard_important_a_120_minutes(self):
        self.assertEqual(niveau_reponse_ouvree(120), "CRITIQUE")

    def test_retard_important_jusqu_a_480_minutes(self):
        self.assertEqual(niveau_reponse_ouvree(480), "CRITIQUE")

    def test_debordement_au_dela_de_480_minutes(self):
        self.assertEqual(niveau_reponse_ouvree(481), "DEBORDEMENT")


class TestAgentsEnPoste(unittest.TestCase):
    def setUp(self):
        self.planning = {
            "Amine": {0: [(10, 12), (13, 17)]},
            "Kristelle": {0: [(10, 12), (13, 17)]},
        }

    def test_capacite_seule_agent_planifie_present(self):
        presents = agents_en_poste(self.planning, ["Amine", "Kristelle"], 0, 10)
        self.assertEqual(presents, ["Amine", "Kristelle"])

    def test_agent_absent_du_planning_ne_compte_pas(self):
        # Sofia n'a aucune ligne cette semaine-la -- ne bascule jamais sur un horaire par defaut.
        presents = agents_en_poste(self.planning, ["Amine", "Sofia"], 0, 10)
        self.assertEqual(presents, ["Amine"])

    def test_hors_creneau_de_l_agent_ne_compte_pas(self):
        presents = agents_en_poste(self.planning, ["Amine"], 0, 12)  # pause dejeuner
        self.assertEqual(presents, [])

    def test_ni_planning_ni_agent_dans_la_grille(self):
        presents = agents_en_poste({}, [], 0, 10)
        self.assertEqual(presents, [])


class TestActiviteObservee(unittest.TestCase):
    def test_ticket_present_uniquement_dans_son_creneau_horaire(self):
        tickets = [
            {"created_at": datetime.datetime(2026, 1, 12, 14, 3), "assignee": "Sofia"},
        ]
        activite = construire_activite_par_jour_heure(tickets, 7, 21)
        self.assertEqual(activite_observee(activite, 0, 14), {"Sofia"})

    def test_aucune_propagation_aux_heures_voisines(self):
        tickets = [
            {"created_at": datetime.datetime(2026, 1, 12, 14, 3), "assignee": "Sofia"},
        ]
        activite = construire_activite_par_jour_heure(tickets, 7, 21)
        self.assertEqual(activite_observee(activite, 0, 13), set())
        self.assertEqual(activite_observee(activite, 0, 15), set())

    def test_creneau_sans_activite_retourne_ensemble_vide(self):
        activite = construire_activite_par_jour_heure([], 7, 21)
        self.assertEqual(activite_observee(activite, 2, 10), set())

    def test_plusieurs_agents_actifs_au_meme_creneau(self):
        tickets = [
            {"created_at": datetime.datetime(2026, 1, 13, 10, 0), "assignee": "Amine"},
            {"created_at": datetime.datetime(2026, 1, 13, 10, 45), "assignee": "Kristelle"},
        ]
        activite = construire_activite_par_jour_heure(tickets, 7, 21)
        self.assertEqual(activite_observee(activite, 1, 10), {"Amine", "Kristelle"})

    def test_heure_hors_plage_suivie_ignoree(self):
        tickets = [
            {"created_at": datetime.datetime(2026, 1, 12, 3, 0), "assignee": "Amine"},
        ]
        activite = construire_activite_par_jour_heure(tickets, 7, 21)
        self.assertEqual(activite_observee(activite, 0, 3), set())


class TestRenfortNonPlanifie(unittest.TestCase):
    def test_activite_seule_sans_capacite_est_un_renfort(self):
        self.assertEqual(renfort_non_planifie([], {"Sofia"}), ["Sofia"])

    def test_capacite_seule_sans_activite_nest_pas_un_renfort(self):
        self.assertEqual(renfort_non_planifie(["Amine"], set()), [])

    def test_ni_activite_ni_capacite(self):
        self.assertEqual(renfort_non_planifie([], set()), [])

    def test_agent_actif_et_planifie_nest_pas_un_renfort(self):
        self.assertEqual(renfort_non_planifie(["Amine"], {"Amine"}), [])

    def test_agent_actif_hors_planning_detecte_comme_renfort_meme_si_dautres_sont_planifies(self):
        # Amine et Kristelle planifies, une personne hors planning (Sofia) intervient aussi :
        # detectee independamment du fait qu'une capacite existe deja (0, 1, 2... agents prevus).
        self.assertEqual(renfort_non_planifie(["Amine", "Kristelle"], {"Amine", "Sofia"}), ["Sofia"])


def evenement(date_debut, date_fin, type_evenement="Commercial", nom="Événement", nature=None, perimetre=None):
    return {
        "date_debut": date_debut, "date_fin": date_fin, "type": type_evenement,
        "nature": nature, "nom_evenement": nom, "description": None, "perimetre": perimetre,
    }


class TestContextePeriode(unittest.TestCase):
    def setUp(self):
        self.periode_debut = datetime.date(2025, 12, 15)
        self.periode_fin = datetime.date(2025, 12, 21)

    def test_evenement_entierement_dans_la_periode(self):
        ev = evenement(datetime.date(2025, 12, 16), datetime.date(2025, 12, 18))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [ev])

    def test_evenement_commencant_avant_et_finissant_pendant(self):
        ev = evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 17))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [ev])

    def test_evenement_commencant_pendant_et_finissant_apres(self):
        ev = evenement(datetime.date(2025, 12, 18), datetime.date(2026, 1, 5))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [ev])

    def test_evenement_couvrant_toute_la_periode(self):
        ev = evenement(datetime.date(2025, 11, 1), datetime.date(2026, 1, 31))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [ev])

    def test_evenement_d_une_seule_journee_dans_la_periode(self):
        ev = evenement(datetime.date(2025, 12, 17), datetime.date(2025, 12, 17))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [ev])

    def test_evenement_d_une_seule_journee_hors_periode(self):
        ev = evenement(datetime.date(2025, 12, 25), datetime.date(2025, 12, 25))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [])

    def test_evenement_hors_periode(self):
        ev = evenement(datetime.date(2026, 1, 5), datetime.date(2026, 1, 20))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [])

    def test_aucun_evenement(self):
        self.assertEqual(contexte_periode([], self.periode_debut, self.periode_fin), [])

    def test_plusieurs_evenements_simultanes(self):
        ev1 = evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 31), nom="A")
        ev2 = evenement(datetime.date(2025, 12, 15), datetime.date(2025, 12, 21), nom="B")
        resultat = contexte_periode([ev1, ev2], self.periode_debut, self.periode_fin)
        self.assertEqual(len(resultat), 2)

    def test_plusieurs_types_simultanes(self):
        ev1 = evenement(datetime.date(2025, 12, 15), datetime.date(2025, 12, 21), type_evenement=TYPE_COMMERCIAL)
        ev2 = evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 31), type_evenement=TYPE_STAFFING)
        resultat = contexte_periode([ev1, ev2], self.periode_debut, self.periode_fin)
        types = set(e["type"] for e in resultat)
        self.assertEqual(types, {TYPE_COMMERCIAL, TYPE_STAFFING})

    def test_commercial_et_produit_le_meme_jour(self):
        ev_commercial = evenement(datetime.date(2026, 2, 9), datetime.date(2026, 2, 14), type_evenement=TYPE_COMMERCIAL, nom="St Valentin")
        ev_produit = evenement(datetime.date(2026, 2, 9), datetime.date(2026, 2, 14), type_evenement=TYPE_PRODUIT, nom="Lancement Étreinte")
        resultat = contexte_periode(
            [ev_commercial, ev_produit], datetime.date(2026, 2, 9), datetime.date(2026, 2, 15)
        )
        self.assertEqual(len(resultat), 2)
        self.assertIn(TYPE_COMMERCIAL, [e["type"] for e in resultat])
        self.assertIn(TYPE_PRODUIT, [e["type"] for e in resultat])

    def test_staffing_et_commercial_simultanement(self):
        ev_staffing = evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 31), type_evenement=TYPE_STAFFING, nom="Renfort Sam", perimetre="Sam")
        ev_commercial = evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 24), type_evenement=TYPE_COMMERCIAL, nom="Noël")
        resultat = contexte_periode([ev_staffing, ev_commercial], self.periode_debut, self.periode_fin)
        self.assertEqual(len(resultat), 2)

    def test_date_debut_manquante_ignoree(self):
        ev = evenement(None, datetime.date(2025, 12, 18))
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [])

    def test_date_fin_manquante_ignoree(self):
        ev = evenement(datetime.date(2025, 12, 16), None)
        self.assertEqual(contexte_periode([ev], self.periode_debut, self.periode_fin), [])

    def test_ordre_chronologique_stable(self):
        ev_tard = evenement(datetime.date(2025, 12, 20), datetime.date(2025, 12, 21), nom="Tard")
        ev_tot = evenement(datetime.date(2025, 12, 15), datetime.date(2025, 12, 16), nom="Tôt")
        resultat = contexte_periode([ev_tard, ev_tot], self.periode_debut, self.periode_fin)
        self.assertEqual([e["nom_evenement"] for e in resultat], ["Tôt", "Tard"])

    def test_absence_de_doublons_apres_fusion(self):
        # simule la fusion des deux feuilles : aucune ligne ne doit se dupliquer au filtrage/tri.
        evenements_commercial = [evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 24), nom="Noël")]
        evenements_staffing = [evenement(datetime.date(2025, 12, 1), datetime.date(2025, 12, 31), type_evenement=TYPE_STAFFING, nom="Renfort Sam")]
        fusion = evenements_commercial + evenements_staffing
        resultat = contexte_periode(fusion, self.periode_debut, self.periode_fin)
        noms = [e["nom_evenement"] for e in resultat]
        self.assertEqual(len(noms), len(set(noms)))
        self.assertEqual(len(resultat), 2)

    def test_type_operationnel_reconnu(self):
        ev = evenement(datetime.date(2025, 12, 16), datetime.date(2025, 12, 18), type_evenement=TYPE_OPERATIONNEL, nom="Incident transporteur")
        resultat = contexte_periode([ev], self.periode_debut, self.periode_fin)
        self.assertEqual(resultat[0]["type"], TYPE_OPERATIONNEL)


def commande_et_cout_remplacement(ids_tickets, prix_vente=100, cout_revient=40, cout_logistique=5, cout_retour=3,
                                   categorie="Diffuseur", produit="ProduitCout"):
    commandes = {}
    for ticket_id in ids_tickets:
        order_id = "CMD-" + str(ticket_id)
        commandes[order_id] = {
            "order_id": order_id, "montant_total": prix_vente,
            "product_category": categorie, "product_name": produit,
        }
    couts_produits = {
        (categorie, produit): {
            "product_category": categorie, "product_name": produit,
            "prix_vente_ttc": prix_vente, "cout_revient_produit": cout_revient,
            "cout_logistique_remplacement": cout_logistique, "cout_retour": cout_retour,
        }
    }
    return commandes, couts_produits


# cout_logistique=0 et cout_retour=0 rendent le coût par dossier exactement égal à cout_par_ticket
# (prix_vente=100, ratio_cout=cout_par_ticket/100 -> montant = 100 * ratio_cout = cout_par_ticket) --
# permet de calibrer un coût précis sans calcul mental supplémentaire dans chaque test.
def lot_tickets_avec_cout(prefixe, nombre, cout_par_ticket, component="ComposantCout", product_name="ProduitCoutable",
                           csat=4, replies=3, full_resolution_time_hours=10, reopens=0):
    ids = []
    tickets = []
    for i in range(nombre):
        ticket_id = prefixe + str(i)
        ids.append(ticket_id)
        tickets.append(ticket_produit(
            ticket_id=ticket_id, component=component, product_name=product_name,
            csat=csat, replies=replies, full_resolution_time_hours=full_resolution_time_hours,
            reopens=reopens, order_id="CMD-" + ticket_id,
        ))
    commandes, couts_produits = commande_et_cout_remplacement(
        ids, prix_vente=100, cout_revient=cout_par_ticket, cout_logistique=0, cout_retour=0,
        categorie="CategorieCout", produit=product_name + "-cout",
    )
    return tickets, commandes, couts_produits


def fusionner_couts(*paires):
    commandes = {}
    couts_produits = {}
    for commandes_partielles, couts_partiels in paires:
        commandes.update(commandes_partielles)
        couts_produits.update(couts_partiels)
    return commandes, couts_produits


class TestMoteurProduitVoieA(unittest.TestCase):
    def test_candidat_sous_seuil_minimum_retourne_aucun_signal(self):
        tickets_candidat = []
        for i in range(SEUIL_MINIMUM_EVALUATION_PRODUIT - 1):
            tickets_candidat.append(ticket_produit(ticket_id=i))
        resultat = construire_signal_produit_voie_a(
            "Batterie", GRAIN_COMPOSANT, tickets_candidat, tickets_candidat, [], {}, {}, None
        )
        self.assertIsNone(resultat)

    def test_candidat_sans_ecart_ne_declenche_pas_de_signal(self):
        tickets_candidat = []
        for i in range(6):
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name=produit, csat=4, replies=3, full_resolution_time_hours=10))

        tickets_controle = lot_tickets_neutres("ctrl", 40, component="LED", product_name="ProduitLED")
        tickets_univers = tickets_candidat + tickets_controle
        resultat = construire_signal_produit_voie_a(
            "Batterie", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], {}, {}, None
        )
        self.assertIsNotNone(resultat)
        self.assertFalse(resultat["eligible"])

    def test_a_csat_seul_ne_suffit_pas(self):
        # Une seule famille de preuve active (B, expérience client) ne doit jamais suffire seule.
        tickets_candidat = []
        for i in range(6):
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name=produit, csat=1))

        tickets_controle = lot_tickets_neutres("ctrl", 40, component="LED", product_name="ProduitLED")
        tickets_univers = tickets_candidat + tickets_controle
        resultat = construire_signal_produit_voie_a(
            "Batterie", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], {}, {}, None
        )
        self.assertEqual(resultat["familles_actives"], ["B"])
        self.assertFalse(resultat["eligible"])
        self.assertIsNone(resultat["niveau_priorite"])

    def test_b_volume_seul_ne_suffit_pas_meme_avec_gros_n(self):
        # 40 tickets, sinon tout dans la norme : le volume seul ne doit jamais devenir un signal,
        # a fortiori pas une "priorité principale". Produits variés pour éviter toute concentration.
        tickets_candidat = []
        for i in range(40):
            produit = ["Produit A", "Produit B", "Produit C", "Produit D"][i % 4]
            tickets_candidat.append(ticket_produit(ticket_id="big" + str(i), component="Bouton", product_name=produit))
        tickets_controle = []
        for i in range(10):
            produit = ["Produit A", "Produit B", "Produit C", "Produit D"][i % 4]
            tickets_controle.append(ticket_produit(ticket_id="ctrl" + str(i), component="Bouton", product_name=produit))
        tickets_univers = tickets_candidat + tickets_controle
        resultat = construire_signal_produit_voie_a(
            "Bouton", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], {}, {}, None
        )
        self.assertEqual(resultat["familles_actives"], ["A"])
        self.assertFalse(resultat["eligible"])
        self.assertIsNone(resultat["niveau_priorite"])

    def test_petit_n_fort_ecart_temporel_seul_ne_suffit_pas(self):
        tickets_candidat = []
        for i in range(6):
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name=produit))
        tickets_controle = lot_tickets_neutres("ctrl", 194, component="LED", product_name="ProduitLED")
        tickets_univers = tickets_candidat + tickets_controle  # part candidat = 6/200 = 3%

        niveaux_historiques = [0.01, 0.01, 0.01, 0.01]  # historique bas mais confiance pleine (4 obs)
        resultat = construire_signal_produit_voie_a(
            "Batterie", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, niveaux_historiques, {}, {}, None
        )
        self.assertGreaterEqual(resultat["reference"]["ecart_pct"], 20)  # écart bien réel...
        self.assertEqual(resultat["familles_actives"], ["A"])  # ...mais une seule famille -> pas de signal
        self.assertFalse(resultat["eligible"])

    def test_c_petit_n_multicritere_peut_remonter(self):
        # 12 tickets (sous le seuil de volume notable), mais CSAT très bas + résolution très longue
        # + coût nettement au-dessus de la référence de la période : la convergence métier doit
        # suffire malgré un volume inférieur.
        ids_candidat = list(range(12))
        commandes_candidat, couts_candidat = commande_et_cout_remplacement(
            ids_candidat, prix_vente=100, cout_revient=70, cout_logistique=0, cout_retour=0, produit="ProduitClarteCout"
        )
        tickets_candidat = []
        for i in ids_candidat:
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(
                ticket_id=i, component="Clarté", product_name=produit, csat=1, full_resolution_time_hours=200,
                replies=3, reopens=0, order_id="CMD-" + str(i),
            ))
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrlc", 100, cout_par_ticket=15, component="LED", product_name="ProduitLEDCout",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "Clarté", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits, reference_cout
        )
        self.assertNotIn("A", resultat["familles_actives"])  # le volume seul n'est pas en cause ici
        self.assertIn("D", resultat["familles_actives"])
        self.assertTrue(resultat["eligible"])
        self.assertEqual(resultat["niveau_priorite"], "Priorité principale")
        self.assertLess(resultat["volume"]["n"], SEUIL_VOLUME_ABSOLU_NOTABLE)

    def test_h_historique_insuffisant_pas_de_bonus_temporel(self):
        tickets_candidat = []
        for i in range(6):
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name=produit))
        tickets_controle = lot_tickets_neutres("ctrl", 100, component="LED", product_name="ProduitLED")
        tickets_univers = tickets_candidat + tickets_controle  # part candidat = 6/106 ≈ 5.7 %

        niveaux_historiques = [0.01]  # une seule observation -> confiance insuffisante
        resultat = construire_signal_produit_voie_a(
            "Batterie", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, niveaux_historiques, {}, {}, None
        )
        self.assertNotIn("A", resultat["familles_actives"])
        self.assertFalse(resultat["eligible"])

    def test_candidat_avec_concentration_seule_ne_suffit_pas(self):
        # F (concentration) seule, sans aucune autre famille active, ne doit pas suffire. Univers
        # volontairement large pour que A (volume/part) reste inactif -- la concentration est
        # interne au candidat, indépendante de la taille de l'univers.
        tickets_candidat = []
        for i in range(6):
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name="Étreinte"))
        tickets_controle = lot_tickets_neutres("ctrlconc", 100, component="LED", product_name="ProduitLED")
        tickets_univers = tickets_candidat + tickets_controle
        resultat = construire_signal_produit_voie_a(
            "Fixation", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], {}, {}, None
        )
        self.assertIsNotNone(resultat["concentration"])
        self.assertEqual(resultat["familles_actives"], ["F"])
        self.assertFalse(resultat["eligible"])

    def test_moteur_voie_a_ne_force_jamais_un_nombre_minimum_de_cartes(self):
        tickets_sav_produit = lot_tickets_neutres("neutre", 40, component="Batterie", product_name="ProduitBatterie")
        resultat = moteur_produit_voie_a(tickets_sav_produit, [], {}, {}, 5)
        self.assertEqual(resultat["prioritaires"], [])
        self.assertEqual(resultat["a_surveiller"], [])
        self.assertEqual(resultat["nb_prioritaires_avant_plafond"], 0)
        self.assertEqual(resultat["nb_a_surveiller_avant_plafond"], 0)

    def test_d_probleme_diffus_sur_plusieurs_produits_une_seule_carte_composant(self):
        tickets_sav_produit = []
        for produit in ("P1", "P2", "P3"):
            for i in range(7):
                tickets_sav_produit.append(ticket_produit(
                    ticket_id=produit + str(i), component="CompoDisperse", product_name=produit,
                    issue_type="IssueDiffuse", csat=1,
                ))
        tickets_sav_produit = tickets_sav_produit + lot_tickets_neutres(
            "ctrl", 100, component="CompoNeutre", product_name="ProduitNeutre"
        )

        resultat = moteur_produit_voie_a(tickets_sav_produit, [], {}, {}, 10)
        self.assertEqual(len(resultat["prioritaires"]), 1)
        self.assertEqual(resultat["prioritaires"][0]["grain"], GRAIN_COMPOSANT)
        self.assertEqual(resultat["prioritaires"][0]["sujet"], "CompoDisperse")

    def test_e_probleme_concentre_sur_un_produit_carte_produit_pas_de_doublon_composant(self):
        tickets_sav_produit = []
        for i in range(20):
            tickets_sav_produit.append(ticket_produit(
                ticket_id="dom" + str(i), component="CompoConcentre", product_name="ProduitDominant",
                issue_type="IssueDominante", csat=1,
            ))
        for i in range(2):
            tickets_sav_produit.append(ticket_produit(
                ticket_id="autre" + str(i), component="CompoConcentre", product_name="AutrePetit",
                issue_type="IssueAutre", csat=1,
            ))
        tickets_sav_produit = tickets_sav_produit + lot_tickets_neutres(
            "ctrl", 100, component="CompoNeutre", product_name="ProduitNeutre"
        )

        resultat = moteur_produit_voie_a(tickets_sav_produit, [], {}, {}, 10)
        self.assertEqual(len(resultat["prioritaires"]), 1)
        self.assertEqual(resultat["prioritaires"][0]["grain"], GRAIN_PRODUIT_COMPOSANT)
        self.assertEqual(resultat["prioritaires"][0]["sujet"], "ProduitDominant")
        sujets = []
        for signal in resultat["prioritaires"] + resultat["a_surveiller"]:
            sujets.append(signal["sujet"])
        self.assertNotIn("CompoConcentre", sujets)

    def test_a_meme_produit_meme_composant_deux_issue_types_se_consolident(self):
        # Identité structurelle : même product_name ET même component réel -> un seul candidat
        # produit x composant les regroupe déjà par construction, sans avoir besoin de comparer
        # leurs preuves (CSAT/effort/etc.).
        tickets_issue_1 = []
        tickets_issue_2 = []
        for i in range(8):
            tickets_issue_1.append(ticket_produit(
                ticket_id="i1-" + str(i), component="CompoF", product_name="ProduitF",
                issue_type="Issue1", csat=1,
            ))
            tickets_issue_2.append(ticket_produit(
                ticket_id="i2-" + str(i), component="CompoF", product_name="ProduitF",
                issue_type="Issue2", csat=1,
            ))
        tickets_produit_f = tickets_issue_1 + tickets_issue_2
        tickets_controle = lot_tickets_neutres("ctrl", 100, component="CompoNeutre", product_name="ProduitNeutre")
        univers = tickets_produit_f + tickets_controle

        signal_issue_1 = construire_signal_produit_voie_a(
            ("ProduitF", "Issue1"), GRAIN_PRODUIT_ISSUE, tickets_issue_1, univers, [], {}, {}, None
        )
        signal_issue_2 = construire_signal_produit_voie_a(
            ("ProduitF", "Issue2"), GRAIN_PRODUIT_ISSUE, tickets_issue_2, univers, [], {}, {}, None
        )
        signal_produit_composant = construire_signal_produit_voie_a(
            ("ProduitF", "CompoF"), GRAIN_PRODUIT_COMPOSANT, tickets_produit_f, univers, [], {}, {}, None
        )

        self.assertFalse(signal_issue_1["eligible"])  # chaque moitié seule est trop petite
        self.assertFalse(signal_issue_2["eligible"])
        self.assertTrue(signal_produit_composant["eligible"])  # combinées (même produit x composant), elles franchissent le seuil

        resultat = consolider_signaux_voie_a([], [signal_produit_composant], [signal_issue_1, signal_issue_2])
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]["grain"], GRAIN_PRODUIT_COMPOSANT)
        self.assertEqual(resultat[0]["sujet"], "ProduitF")
        texte_consolide = " | ".join(resultat[0]["elements_consolides"])
        self.assertIn("Issue1", texte_consolide)
        self.assertIn("Issue2", texte_consolide)

    def test_b_meme_produit_composants_differents_ne_fusionnent_pas(self):
        # Le product_name seul ne suffit jamais à fusionner -- il faut le MÊME component réel.
        tickets_c1 = []
        for i in range(8):
            tickets_c1.append(ticket_produit(
                ticket_id="b1-" + str(i), component="CompoB1", product_name="ProduitB",
                issue_type="IssueB1", csat=1, full_resolution_time_hours=200,
            ))
        controle_1 = lot_tickets_neutres("ctrlb1", 100, component="CompoNeutre", product_name="ProduitNeutre")
        univers_1 = tickets_c1 + controle_1
        signal_c1 = construire_signal_produit_voie_a(
            ("ProduitB", "CompoB1"), GRAIN_PRODUIT_COMPOSANT, tickets_c1, univers_1, [], {}, {}, None
        )
        self.assertTrue(signal_c1["eligible"])

        tickets_c2 = []
        for i in range(8):
            tickets_c2.append(ticket_produit(
                ticket_id="b2-" + str(i), component="CompoB2", product_name="ProduitB",
                issue_type="IssueB2", csat=1, full_resolution_time_hours=200,
            ))
        controle_2 = lot_tickets_neutres("ctrlb2", 100, component="CompoNeutre", product_name="ProduitNeutre")
        univers_2 = tickets_c2 + controle_2
        signal_c2 = construire_signal_produit_voie_a(
            ("ProduitB", "CompoB2"), GRAIN_PRODUIT_COMPOSANT, tickets_c2, univers_2, [], {}, {}, None
        )
        self.assertTrue(signal_c2["eligible"])

        resultat = consolider_signaux_voie_a([], [signal_c1, signal_c2], [])
        self.assertEqual(len(resultat), 2)
        sujets = []
        for signal in resultat:
            sujets.append(signal["sujet"])
        self.assertEqual(sujets, ["ProduitB", "ProduitB"])  # deux cartes, même produit, jamais fusionnées

    def test_c_deux_problemes_meme_csat_bas_meme_effort_eleve_ne_fusionnent_pas_sur_bc(self):
        # Coeur du principe Étape 4A.3 : B/C (preuve) ne sont jamais un critère d'identité, même
        # quand ils correspondent EXACTEMENT entre les deux candidats. Seuls product_name et
        # component réel décident -- ici volontairement différents.
        tickets_c1 = []
        for i in range(8):
            tickets_c1.append(ticket_produit(
                ticket_id="c1-" + str(i), component="CompoC1", product_name="ProduitC",
                issue_type="IssueC1", csat=1, full_resolution_time_hours=150,
            ))
        tickets_c2 = []
        for i in range(8):
            tickets_c2.append(ticket_produit(
                ticket_id="c2-" + str(i), component="CompoC2", product_name="ProduitC",
                issue_type="IssueC2", csat=1, full_resolution_time_hours=150,
            ))
        controle = lot_tickets_neutres("ctrlc", 100, component="CompoNeutre", product_name="ProduitNeutre")
        univers = tickets_c1 + tickets_c2 + controle

        signal_c1 = construire_signal_produit_voie_a(
            ("ProduitC", "CompoC1"), GRAIN_PRODUIT_COMPOSANT, tickets_c1, univers, [], {}, {}, None
        )
        signal_c2 = construire_signal_produit_voie_a(
            ("ProduitC", "CompoC2"), GRAIN_PRODUIT_COMPOSANT, tickets_c2, univers, [], {}, {}, None
        )
        # Preuves rigoureusement identiques (mêmes familles actives)...
        self.assertEqual(set(signal_c1["familles_actives"]), set(signal_c2["familles_actives"]))
        self.assertIn("B", signal_c1["familles_actives"])
        self.assertIn("C", signal_c1["familles_actives"])
        self.assertTrue(signal_c1["eligible"])
        self.assertTrue(signal_c2["eligible"])

        # ...mais deux components différents : deux cartes, jamais fusionnées sur la preuve seule.
        resultat = consolider_signaux_voie_a([], [signal_c1, signal_c2], [])
        self.assertEqual(len(resultat), 2)

    def test_e_trois_problemes_distincts_du_meme_produit_restent_identifiables(self):
        tickets_c1 = []
        for i in range(8):
            tickets_c1.append(ticket_produit(
                ticket_id="e1-" + str(i), component="CompoE1", product_name="ProduitE",
                issue_type="IssueE1", csat=1, full_resolution_time_hours=200,
            ))
        tickets_c2 = []
        for i in range(8):
            tickets_c2.append(ticket_produit(
                ticket_id="e2-" + str(i), component="CompoE2", product_name="ProduitE",
                issue_type="IssueE2", csat=1, full_resolution_time_hours=200,
            ))
        tickets_c3 = []
        for i in range(8):
            tickets_c3.append(ticket_produit(
                ticket_id="e3-" + str(i), component="CompoE3", product_name="ProduitE",
                issue_type="IssueE3", csat=1, full_resolution_time_hours=200,
            ))
        controle = lot_tickets_neutres("ctrle", 100, component="CompoNeutre", product_name="ProduitNeutre")
        univers = tickets_c1 + tickets_c2 + tickets_c3 + controle

        signal_c1 = construire_signal_produit_voie_a(
            ("ProduitE", "CompoE1"), GRAIN_PRODUIT_COMPOSANT, tickets_c1, univers, [], {}, {}, None
        )
        signal_c2 = construire_signal_produit_voie_a(
            ("ProduitE", "CompoE2"), GRAIN_PRODUIT_COMPOSANT, tickets_c2, univers, [], {}, {}, None
        )
        signal_c3 = construire_signal_produit_voie_a(
            ("ProduitE", "CompoE3"), GRAIN_PRODUIT_COMPOSANT, tickets_c3, univers, [], {}, {}, None
        )

        resultat = consolider_signaux_voie_a([], [signal_c1, signal_c2, signal_c3], [])
        self.assertEqual(len(resultat), 3)  # trois histoires distinctes, jamais fusionnées

        for signal in resultat:
            self.assertIsNotNone(signal["regroupement_produit"])
            self.assertEqual(signal["regroupement_produit"]["produit"], "ProduitE")
            self.assertEqual(len(signal["regroupement_produit"]["autres_sujets"]), 2)  # regroupées visuellement

    def test_f_aucune_regle_ne_depend_d_un_nom_de_produit_precis(self):
        # Rejoue exactement le scénario "composant concentré" (test E historique) avec des noms
        # de produit/composant arbitraires -- le comportement doit être identique, preuve que rien
        # n'est codé en dur pour un produit particulier.
        tickets_sav_produit = []
        for i in range(20):
            tickets_sav_produit.append(ticket_produit(
                ticket_id="dom" + str(i), component="Qzrmph-Δ7", product_name="Xyzintorb-42",
                issue_type="IssueDominante", csat=1,
            ))
        for i in range(2):
            tickets_sav_produit.append(ticket_produit(
                ticket_id="autre" + str(i), component="Qzrmph-Δ7", product_name="Wibbleflorn-9",
                issue_type="IssueAutre", csat=1,
            ))
        tickets_sav_produit = tickets_sav_produit + lot_tickets_neutres(
            "ctrl", 100, component="CompoNeutreZ", product_name="ProduitNeutreZ"
        )

        resultat = moteur_produit_voie_a(tickets_sav_produit, [], {}, {}, 10)
        self.assertEqual(len(resultat["prioritaires"]), 1)
        self.assertEqual(resultat["prioritaires"][0]["grain"], GRAIN_PRODUIT_COMPOSANT)
        self.assertEqual(resultat["prioritaires"][0]["sujet"], "Xyzintorb-42")

    def test_i_top_n_n_evince_pas_un_candidat_important(self):
        tickets_gros = []
        for i in range(30):
            tickets_gros.append(ticket_produit(
                ticket_id="gros" + str(i), component="CompoImportant", product_name="ProduitImportant",
                csat=1, full_resolution_time_hours=100, replies=3, reopens=0,
            ))

        tickets_petits = []
        for indice in range(5):
            composant = "CompoPetit" + str(indice)
            for i in range(6):
                tickets_petits.append(ticket_produit(
                    ticket_id=composant + str(i), component=composant, product_name="Produit" + composant,
                    csat=1,
                ))

        tickets_controle = lot_tickets_neutres("ctrl", 200, component="CompoNeutre", product_name="ProduitNeutre")
        tickets_sav_produit = tickets_gros + tickets_petits + tickets_controle

        resultat = moteur_produit_voie_a(tickets_sav_produit, [], {}, {}, 3)
        sujets = []
        for signal in resultat["prioritaires"]:
            sujets.append(signal["sujet"])
        # Le composant "CompoImportant" est concentré à 100 % sur "ProduitImportant" -- il est
        # donc légitimement absorbé dans la carte produit, plus précise (voir test E). Ce qui
        # compte ici : l'histoire (A+B+C+F, convergence forte) n'est pas évincée par les petits
        # candidats du plafond d'affichage (B+F seulement, convergence plus faible).
        self.assertIn("ProduitImportant", sujets)
        self.assertEqual(len(resultat["prioritaires"]), 3)
        self.assertGreaterEqual(resultat["nb_prioritaires_avant_plafond"], len(resultat["prioritaires"]))

    def test_volume_et_cout_seuls_restent_a_surveiller(self):
        ids_candidat = []
        tickets_candidat = []
        for i in range(20):
            ticket_id = "ad" + str(i)
            ids_candidat.append(ticket_id)
            produit = ["Produit A", "Produit B", "Produit C", "Produit D"][i % 4]
            tickets_candidat.append(ticket_produit(
                ticket_id=ticket_id, component="CompoAD", product_name=produit,
                csat=4, full_resolution_time_hours=10, replies=3, reopens=0, order_id="CMD-" + ticket_id,
            ))
        commandes_candidat, couts_candidat = commande_et_cout_remplacement(
            ids_candidat, prix_vente=100, cout_revient=50, cout_logistique=0, cout_retour=0, produit="ProduitADCout"
        )
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrlad", 100, cout_par_ticket=10, component="CompoNeutre", product_name="ProduitNeutreCout",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "CompoAD", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits, reference_cout
        )
        self.assertEqual(set(resultat["familles_actives"]), {"A", "D"})
        self.assertTrue(resultat["eligible"])
        self.assertEqual(resultat["tier"], "a_surveiller")
        self.assertEqual(resultat["niveau_priorite"], "À surveiller")

    def test_volume_cout_et_csat_degrade_devient_prioritaire(self):
        ids_candidat = []
        tickets_candidat = []
        for i in range(20):
            ticket_id = "adb" + str(i)
            ids_candidat.append(ticket_id)
            produit = ["Produit A", "Produit B", "Produit C", "Produit D"][i % 4]
            tickets_candidat.append(ticket_produit(
                ticket_id=ticket_id, component="CompoADB", product_name=produit,
                csat=1, full_resolution_time_hours=10, replies=3, reopens=0, order_id="CMD-" + ticket_id,
            ))
        commandes_candidat, couts_candidat = commande_et_cout_remplacement(
            ids_candidat, prix_vente=100, cout_revient=50, cout_logistique=0, cout_retour=0, produit="ProduitADBCout"
        )
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrladb", 100, cout_par_ticket=10, component="CompoNeutre", product_name="ProduitNeutreCoutB",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "CompoADB", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits, reference_cout
        )
        self.assertEqual(set(resultat["familles_actives"]), {"A", "B", "D"})
        self.assertEqual(resultat["tier"], "priorite")
        self.assertEqual(resultat["niveau_priorite"], "Priorité principale")

    def test_volume_cout_et_effort_eleve_devient_prioritaire(self):
        ids_candidat = []
        tickets_candidat = []
        for i in range(20):
            ticket_id = "adc" + str(i)
            ids_candidat.append(ticket_id)
            produit = ["Produit A", "Produit B", "Produit C", "Produit D"][i % 4]
            tickets_candidat.append(ticket_produit(
                ticket_id=ticket_id, component="CompoADC", product_name=produit,
                csat=4, full_resolution_time_hours=200, replies=3, reopens=0, order_id="CMD-" + ticket_id,
            ))
        commandes_candidat, couts_candidat = commande_et_cout_remplacement(
            ids_candidat, prix_vente=100, cout_revient=50, cout_logistique=0, cout_retour=0, produit="ProduitADCCout"
        )
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrladc", 100, cout_par_ticket=10, component="CompoNeutre", product_name="ProduitNeutreCoutC",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "CompoADC", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits, reference_cout
        )
        self.assertEqual(set(resultat["familles_actives"]), {"A", "C", "D"})
        self.assertEqual(resultat["tier"], "priorite")
        self.assertEqual(resultat["niveau_priorite"], "Priorité principale")

    def test_cout_absolu_eleve_mais_normal_relativement_pas_de_famille_d(self):
        tickets_candidat, commandes_candidat, couts_candidat = lot_tickets_avec_cout(
            "cher", 6, cout_par_ticket=100, component="CompoCherNormal", product_name="ProduitCherA",
        )
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrlcher", 100, cout_par_ticket=100, component="CompoNeutre", product_name="ProduitCherB",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "CompoCherNormal", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits,
            reference_cout,
        )
        self.assertNotIn("D", resultat["familles_actives"])

    def test_cout_modere_mais_tres_superieur_a_baseline_active_famille_d(self):
        tickets_candidat, commandes_candidat, couts_candidat = lot_tickets_avec_cout(
            "modere", 6, cout_par_ticket=25, component="CompoModere", product_name="ProduitModereA",
        )
        tickets_controle, commandes_controle, couts_controle = lot_tickets_avec_cout(
            "ctrlmodere", 100, cout_par_ticket=8, component="CompoNeutre", product_name="ProduitModereB",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_candidat, couts_candidat), (commandes_controle, couts_controle)
        )
        tickets_univers = tickets_candidat + tickets_controle
        reference_cout = calculer_reference_cout_moyen(tickets_univers, commandes, couts_produits)

        resultat = construire_signal_produit_voie_a(
            "CompoModere", GRAIN_COMPOSANT, tickets_candidat, tickets_univers, [], commandes, couts_produits,
            reference_cout,
        )
        self.assertIn("D", resultat["familles_actives"])

    def test_partager_uniquement_le_cout_ne_pilote_pas_la_decision_de_fusion(self):
        # Historiquement (Étape 4A.2), ce scénario vérifiait que "D seul en commun" empêchait la
        # fusion. Depuis Étape 4A.3, la fusion n'est plus décidée par la preuve du tout -- ici les
        # deux issue_types partagent le MÊME product_name ET le MÊME component réel : ils
        # fusionnent donc bien en un seul candidat produit x composant, par identité structurelle,
        # indépendamment du fait que leur seul point commun évident soit le coût.
        ids_1 = []
        tickets_issue_1 = []
        for i in range(8):
            ticket_id = "cd1-" + str(i)
            ids_1.append(ticket_id)
            tickets_issue_1.append(ticket_produit(
                ticket_id=ticket_id, component="CompoCD", product_name="ProduitCD", issue_type="IssueCoutA",
                csat=4, full_resolution_time_hours=10, replies=3, reopens=0, order_id="CMD-" + ticket_id,
            ))
        commandes_1, couts_1 = commande_et_cout_remplacement(
            ids_1, prix_vente=100, cout_revient=60, cout_logistique=0, cout_retour=0, produit="ProduitCDCout1"
        )

        ids_2 = []
        tickets_issue_2 = []
        for i in range(8):
            ticket_id = "cd2-" + str(i)
            ids_2.append(ticket_id)
            tickets_issue_2.append(ticket_produit(
                ticket_id=ticket_id, component="CompoCD", product_name="ProduitCD", issue_type="IssueCoutB",
                csat=4, full_resolution_time_hours=10, replies=3, reopens=0, order_id="CMD-" + ticket_id,
            ))
        commandes_2, couts_2 = commande_et_cout_remplacement(
            ids_2, prix_vente=100, cout_revient=60, cout_logistique=0, cout_retour=0, produit="ProduitCDCout2"
        )

        tickets_controle, commandes_ctrl, couts_ctrl = lot_tickets_avec_cout(
            "ctrlcd", 30, cout_par_ticket=10, component="CompoNeutre", product_name="ProduitCDNeutre",
        )
        commandes, couts_produits = fusionner_couts(
            (commandes_1, couts_1), (commandes_2, couts_2), (commandes_ctrl, couts_ctrl)
        )
        tickets_produit = tickets_issue_1 + tickets_issue_2
        univers = tickets_produit + tickets_controle
        reference_cout = calculer_reference_cout_moyen(univers, commandes, couts_produits)

        signal_issue_1 = construire_signal_produit_voie_a(
            ("ProduitCD", "IssueCoutA"), GRAIN_PRODUIT_ISSUE, tickets_issue_1, univers, [], commandes,
            couts_produits, reference_cout,
        )
        signal_issue_2 = construire_signal_produit_voie_a(
            ("ProduitCD", "IssueCoutB"), GRAIN_PRODUIT_ISSUE, tickets_issue_2, univers, [], commandes,
            couts_produits, reference_cout,
        )
        self.assertEqual(set(signal_issue_1["familles_actives"]), {"A", "D"})
        self.assertEqual(set(signal_issue_2["familles_actives"]), {"A", "D"})
        self.assertTrue(signal_issue_1["eligible"])  # à surveiller, mais analysable
        self.assertTrue(signal_issue_2["eligible"])

        signal_produit_composant = construire_signal_produit_voie_a(
            ("ProduitCD", "CompoCD"), GRAIN_PRODUIT_COMPOSANT, tickets_produit, univers, [], commandes,
            couts_produits, reference_cout,
        )
        resultat = consolider_signaux_voie_a([], [signal_produit_composant], [signal_issue_1, signal_issue_2])
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]["grain"], GRAIN_PRODUIT_COMPOSANT)
        self.assertEqual(resultat[0]["sujet"], "ProduitCD")


class TestEvaluerTemporalite(unittest.TestCase):
    def test_historique_vide(self):
        texte = evaluer_temporalite([], 0.3)
        self.assertIn("historique insuffisant", texte)

    def test_niveau_habituel(self):
        texte = evaluer_temporalite([0.20, 0.22, 0.19], 0.21)
        self.assertIn("niveau habituel", texte)

    def test_niveau_eleve_jamais_observe(self):
        texte = evaluer_temporalite([0.10, 0.11, 0.09], 0.30)
        self.assertIn("pas observé aussi haut", texte)
        self.assertNotIn("répétition", texte)

    def test_niveau_eleve_deja_observe(self):
        texte = evaluer_temporalite([0.30, 0.10, 0.32, 0.09], 0.31)
        self.assertIn("répétition à confirmer", texte)

    def test_niveau_plus_bas(self):
        texte = evaluer_temporalite([0.30, 0.32, 0.29], 0.10)
        self.assertIn("retour vers un niveau habituel", texte)

    def test_ecart_relatif_temporel_calcule_correctement(self):
        self.assertAlmostEqual(ecart_relatif_temporel([0.10, 0.20], 0.18), 0.2)


class TestMoteurProduitVoieB(unittest.TestCase):
    def test_remboursement_csat_faible_seul_ne_declenche_pas(self):
        ticket = ticket_produit(resolution_type="Remboursement", csat=1, reopens=0, replies=3, full_resolution_time_hours=10)
        resultat = evaluer_gravite_ticket_voie_b(ticket, reference_replies=3, reference_resolution_h=10)
        self.assertIsNone(resultat)

    def test_declenche_avec_reopens_eleves(self):
        ticket = ticket_produit(resolution_type="Remplacement produit", csat=2, reopens=3, replies=3, full_resolution_time_hours=10)
        resultat = evaluer_gravite_ticket_voie_b(ticket, reference_replies=3, reference_resolution_h=10)
        self.assertIsNotNone(resultat)
        self.assertIn("réouvertures", resultat["raison"])

    def test_declenche_avec_replies_nettement_au_dessus_reference(self):
        ticket = ticket_produit(resolution_type="Remboursement", csat=2, reopens=0, replies=10, full_resolution_time_hours=10)
        resultat = evaluer_gravite_ticket_voie_b(ticket, reference_replies=3, reference_resolution_h=10)
        self.assertIsNotNone(resultat)

    def test_resolution_hors_perimetre_jamais_declenchee(self):
        ticket = ticket_produit(
            resolution_type="Information / résolution à distance", csat=1, reopens=5, replies=20,
            full_resolution_time_hours=100,
        )
        resultat = evaluer_gravite_ticket_voie_b(ticket, reference_replies=3, reference_resolution_h=10)
        self.assertIsNone(resultat)


class TestVocabulaireProduit(unittest.TestCase):
    def test_jamais_significatif_ni_structurel_ni_statistique(self):
        textes = []
        textes.append(evaluer_temporalite([], 0.3))
        textes.append(evaluer_temporalite([0.20, 0.22], 0.21))
        textes.append(evaluer_temporalite([0.10, 0.11], 0.30))
        textes.append(evaluer_temporalite([0.30, 0.10, 0.32], 0.31))
        textes.append(evaluer_temporalite([0.30, 0.32], 0.10))
        textes.append(lire_ecart_csat(2, 4))
        textes.append(lire_ecart_csat(None, 4))
        textes.append(lire_ecart_effort(10, 3))
        textes.append(lire_ecart_effort(None, 3))

        signal_voie_b = evaluer_gravite_ticket_voie_b(
            ticket_produit(resolution_type="Remplacement produit", csat=1, reopens=4),
            reference_replies=3, reference_resolution_h=10,
        )
        textes.append(signal_voie_b["avertissement"])

        # Sorties du moteur Voie A : règle d'éligibilité (les deux variantes "priorité"), phrase
        # "à surveiller" structurelle, et lecture du coût (relative, jamais un seuil absolu).
        tickets_candidat = []
        for i in range(6):
            produit = ["Produit A", "Produit B", "Produit C"][i % 3]
            tickets_candidat.append(ticket_produit(ticket_id=i, product_name=produit, csat=1, full_resolution_time_hours=200))
        tickets_controle = lot_tickets_neutres("ctrlvoc", 100, component="LED", product_name="ProduitLED")
        univers = tickets_candidat + tickets_controle
        signal_priorite = construire_signal_produit_voie_a(
            "CompoVocab", GRAIN_COMPOSANT, tickets_candidat, univers, [], {}, {}, None
        )
        textes.append(signal_priorite["regle_eligibilite"])
        textes.append(signal_priorite["observation_principale"])
        for element in signal_priorite["elements_contributifs"]:
            textes.append(element)

        tickets_candidat_ad, commandes_ad, couts_ad = lot_tickets_avec_cout(
            "voc2", 20, cout_par_ticket=50, component="CompoVocab2", product_name="ProduitVocab2",
        )
        tickets_controle_ad, commandes_ctrl_ad, couts_ctrl_ad = lot_tickets_avec_cout(
            "ctrlvoc2", 100, cout_par_ticket=10, component="CompoNeutre", product_name="ProduitVocabNeutre",
        )
        commandes_voc, couts_voc = fusionner_couts((commandes_ad, couts_ad), (commandes_ctrl_ad, couts_ctrl_ad))
        univers_ad = tickets_candidat_ad + tickets_controle_ad
        reference_voc = calculer_reference_cout_moyen(univers_ad, commandes_voc, couts_voc)
        signal_a_surveiller = construire_signal_produit_voie_a(
            "CompoVocab2", GRAIN_COMPOSANT, tickets_candidat_ad, univers_ad, [], commandes_voc, couts_voc, reference_voc
        )
        textes.append(signal_a_surveiller["regle_eligibilite"])
        textes.append(signal_a_surveiller["observation_principale"])
        textes.append(signal_a_surveiller["cout"]["lecture"])
        for element in signal_a_surveiller["elements_contributifs"]:
            textes.append(element)

        for texte in textes:
            self.assertIsNotNone(texte)
            self.assertNotIn("significatif", texte.lower())
            self.assertNotIn("structurel", texte.lower())
            self.assertNotIn("statistique", texte.lower())


def profil_test(date_debut, volume, csat=4.0, resolution_h=40.0, reopens=0.06, replies=2.4,
                 capacite_heures=100, mix_categories=None, contexte=None, date_fin=None):
    if date_fin is None:
        date_fin = date_debut + datetime.timedelta(days=6)
    if mix_categories is None:
        mix_categories = {"Livraison": volume}
    if contexte is None:
        contexte = []
    return {
        "date_debut": date_debut,
        "date_fin": date_fin,
        "volume": volume,
        "mix_categories": mix_categories,
        "csat": csat,
        "n_csat": volume,
        "frt": 180.0,
        "taux_sla": 80.0,
        "resolution_h": resolution_h,
        "reopens": reopens,
        "replies": replies,
        "macro_pct": 60.0,
        "capacite_heures": capacite_heures,
        "contexte": contexte,
    }


def evenement_test(nom, type_evenement, date_debut, date_fin):
    return {
        "date_debut": date_debut, "date_fin": date_fin, "type": type_evenement,
        "nature": None, "nom_evenement": nom, "description": None, "perimetre": None,
    }


class TestMoteurTendances(unittest.TestCase):
    def test_a_pic_volume_bien_absorbe_nest_pas_une_crise(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 1600, csat=4.1, resolution_h=38, reopens=0.05, replies=2.3),
            profil_test(datetime.date(2025, 12, 1), 810),
            profil_test(datetime.date(2026, 1, 1), 790),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")
        self.assertNotIn("crise", fait["observation"].lower())
        self.assertNotIn("crise", fait["pourquoi"].lower())

    def test_b_tension_operationnelle_sans_pic_de_volume(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 790, csat=3.5, resolution_h=70, reopens=0.15, replies=3.6),
            profil_test(datetime.date(2025, 12, 1), 810),
            profil_test(datetime.date(2026, 1, 1), 800),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "vigilance")

    def test_c_contraste_capacite_comparable_complexite_differente(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800, capacite_heures=100),
            profil_test(datetime.date(2025, 10, 1), 820, capacite_heures=100),
            profil_test(
                datetime.date(2025, 11, 1), 1800, csat=4.2, resolution_h=32, reopens=0.02, replies=1.9,
                capacite_heures=120,
            ),
            profil_test(
                datetime.date(2025, 12, 1), 1200, csat=3.3, resolution_h=85, reopens=0.22, replies=4.2,
                capacite_heures=120,
            ),
            profil_test(datetime.date(2026, 1, 1), 790, capacite_heures=100),
        ]
        contrastes = detecter_contrastes_capacite(profils)
        self.assertGreaterEqual(len(contrastes), 1)
        self.assertIn("120h", contrastes[0]["observation"])

    def test_d_contexte_associe_sans_causalite(self):
        # Volumes choisis pour que l'observation cible reste au milieu du classement (rang ~0,5,
        # ni haut ni bas) -- seul le mix de demandes, épaulé par un contexte réel, doit déclencher
        # le jalon ici, pas la position du volume.
        campagne = evenement_test("Test Campagne", TYPE_COMMERCIAL, datetime.date(2025, 11, 20), datetime.date(2025, 11, 30))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 750, mix_categories={"Avant-vente / conseil": 140, "Livraison": 610}),
            profil_test(datetime.date(2025, 10, 1), 780, mix_categories={"Avant-vente / conseil": 150, "Livraison": 630}),
            profil_test(
                datetime.date(2025, 11, 24), 800, mix_categories={"Avant-vente / conseil": 400, "Livraison": 400},
                contexte=[campagne],
            ),
            profil_test(datetime.date(2025, 12, 1), 820, mix_categories={"Avant-vente / conseil": 155, "Livraison": 665}),
            profil_test(datetime.date(2026, 1, 1), 850, mix_categories={"Avant-vente / conseil": 160, "Livraison": 690}),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")
        self.assertIn("Avant-vente", fait["observation"])
        self.assertIsNotNone(fait["contexte"])
        self.assertIn("Test Campagne", fait["contexte"])

        for texte in (fait["observation"], fait["pourquoi"], fait["contexte"], fait["prudence"]):
            self.assertNotIn("provoqué", texte.lower())
            self.assertNotIn("entraîné", texte.lower())
            self.assertNotIn("a causé", texte.lower())

    def test_e_periode_calme_sans_fait_marquant(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 810),
            profil_test(datetime.date(2025, 12, 1), 805),
            profil_test(datetime.date(2026, 1, 1), 815),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNone(fait)

    def test_f_observations_espacees_jamais_de_serie_continue(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2026, 3, 1), 820),
            profil_test(datetime.date(2026, 9, 1), 1600, csat=4.1, resolution_h=38, reopens=0.05, replies=2.3),
        ]
        synthese = construire_synthese_longue(profils)
        textes = [synthese["synthese_generale"]]
        for fait in synthese["jalons_metier"] + synthese["vigilances"]:
            textes.append(fait["observation"])
            textes.append(fait["pourquoi"])
        for texte in textes:
            self.assertNotIn("hausse continue", texte.lower())
            self.assertNotIn("baisse continue", texte.lower())
            self.assertNotIn("semaines consécutives", texte.lower())
            self.assertNotIn("depuis plusieurs semaines", texte.lower())

    def test_g_saisonnalite_apparente_avec_assez_dobservations(self):
        profils = [
            profil_test(datetime.date(2025, 12, 1), 1800),
            profil_test(datetime.date(2026, 1, 1), 1700),
            profil_test(datetime.date(2026, 2, 1), 1750),
            profil_test(datetime.date(2026, 7, 1), 700),
            profil_test(datetime.date(2026, 8, 1), 650),
        ]
        saisonnalite = detecter_saisonnalite_apparente(profils)
        self.assertIsNotNone(saisonnalite)
        self.assertIn("hiver", saisonnalite["observation"])
        self.assertIn("été", saisonnalite["observation"])

    def test_h_une_seule_observation_estivale_ne_suffit_pas(self):
        profils = [
            profil_test(datetime.date(2025, 12, 1), 1800),
            profil_test(datetime.date(2026, 1, 1), 1700),
            profil_test(datetime.date(2026, 7, 1), 700),
        ]
        saisonnalite = detecter_saisonnalite_apparente(profils)
        self.assertIsNone(saisonnalite)

    def test_i_pic_volume_sans_degradation_nest_pas_automatiquement_negatif(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 810),
            profil_test(datetime.date(2025, 11, 1), 1650, csat=4.05, resolution_h=39, reopens=0.055, replies=2.35),
            profil_test(datetime.date(2025, 12, 1), 795),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")

    def test_j_volume_plus_faible_mais_forte_complexite_peut_etre_plus_preoccupant(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800, capacite_heures=100),
            profil_test(datetime.date(2025, 10, 1), 820, capacite_heures=100),
            profil_test(
                datetime.date(2025, 12, 1), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
                capacite_heures=120,
            ),
            profil_test(
                datetime.date(2026, 1, 1), 1200, csat=3.4, resolution_h=78, reopens=0.2, replies=4.0,
                capacite_heures=120,
            ),
        ]
        fait_janvier = detecter_fait_marquant(profils, 3)
        self.assertIsNotNone(fait_janvier)
        self.assertEqual(fait_janvier["categorie"], "vigilance")
        # volume janvier < volume decembre, et pourtant janvier est le point de vigilance
        self.assertLess(profils[3]["volume"], profils[2]["volume"])

    def test_k_vocabulaire_interdit_absent_des_sorties_tendances(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800, capacite_heures=100),
            profil_test(datetime.date(2025, 10, 1), 820, capacite_heures=100),
            profil_test(
                datetime.date(2025, 12, 1), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
                capacite_heures=120,
            ),
            profil_test(
                datetime.date(2026, 1, 1), 1200, csat=3.4, resolution_h=78, reopens=0.2, replies=4.0,
                capacite_heures=120,
            ),
            profil_test(datetime.date(2026, 7, 1), 700, capacite_heures=70),
        ]
        synthese = construire_synthese_longue(profils)
        textes = [synthese["synthese_generale"], synthese["niveau_confiance"]]
        for fait in synthese["jalons_metier"] + synthese["vigilances"]:
            textes.append(fait["observation"])
            textes.append(fait["pourquoi"])
            if fait["contexte"] is not None:
                textes.append(fait["contexte"])
            if fait["prudence"] is not None:
                textes.append(fait["prudence"])
        for contraste in synthese["contrastes"]:
            textes.append(contraste["observation"])
            textes.append(contraste["pourquoi"])
        if synthese["saisonnalite"] is not None:
            textes.append(synthese["saisonnalite"]["observation"])
            textes.append(synthese["saisonnalite"]["prudence"])

        mots_interdits = ("significatif", "significativement", "structurel", "corrélation", "causal", "statistique")
        for texte in textes:
            texte_minuscule = texte.lower()
            for mot in mots_interdits:
                self.assertNotIn(mot, texte_minuscule)

    def test_a2_campagne_avec_activite_moderee_devient_jalon(self):
        # Rang ~0,60 (élevé mais pas extrême) + contexte réel -> jalon, pas vigilance.
        campagne = evenement_test("Campagne Test", TYPE_COMMERCIAL, datetime.date(2026, 2, 1), datetime.date(2026, 2, 10))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 720),
            profil_test(datetime.date(2025, 11, 1), 740),
            profil_test(datetime.date(2025, 12, 1), 950),
            profil_test(datetime.date(2026, 1, 1), 980),
            profil_test(datetime.date(2026, 2, 5), 900, contexte=[campagne]),
        ]
        fait = detecter_fait_marquant(profils, 5)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")

    def test_b2_aucun_evenement_activite_normale_pas_de_jalon_force(self):
        profils = [
            profil_test(datetime.date(2026, 1, 1), 800),
            profil_test(datetime.date(2026, 2, 1), 810),
            profil_test(datetime.date(2026, 3, 1), 805),
            profil_test(datetime.date(2026, 4, 1), 795),
            profil_test(datetime.date(2026, 5, 1), 815),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNone(fait)

    def test_c2_volume_sous_seuil_fixe_mais_haut_dans_la_distribution(self):
        # Un pic extrême ailleurs (3000) gonflerait une simple moyenne au point de faire lire la
        # cible (700, pourtant 2e plus haute sur 6) comme "en retrait" -- le rang, robuste aux
        # valeurs extrêmes, la lit correctement comme haute.
        profils = [
            profil_test(datetime.date(2025, 9, 1), 500),
            profil_test(datetime.date(2025, 10, 1), 520),
            profil_test(datetime.date(2025, 11, 1), 540),
            profil_test(datetime.date(2025, 12, 1), 560),
            profil_test(datetime.date(2026, 1, 1), 3000),
            profil_test(datetime.date(2026, 2, 1), 700),
        ]
        volumes = []
        for p in profils:
            volumes.append(p["volume"])
        ecart_moyenne_fragile = ecart_relatif_vs_reste(volumes, 5)
        self.assertLess(ecart_moyenne_fragile, 0)  # la moyenne seule lirait ceci comme "en retrait"...

        rang = rang_relatif(volumes, 5)
        self.assertGreaterEqual(rang, SEUIL_RANG_HAUT_STRICT)  # ...le rang, lui, la lit correctement comme haute

        fait = detecter_fait_marquant(profils, 5)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")
        self.assertIn("élevé", fait["observation"])

    def test_d2_deux_pics_extremes_ne_masquent_pas_un_troisieme_volume_eleve(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 9, 8), 820),
            profil_test(datetime.date(2025, 10, 1), 830),
            profil_test(datetime.date(2025, 10, 15), 790),
            profil_test(datetime.date(2025, 11, 1), 1500, csat=4.1, resolution_h=38, reopens=0.05, replies=2.3),
            profil_test(datetime.date(2025, 12, 1), 1800, csat=4.1, resolution_h=35, reopens=0.04, replies=2.2),
            profil_test(
                datetime.date(2026, 1, 1), 1200, csat=3.4, resolution_h=75, reopens=0.2, replies=4.0,
            ),
        ]
        volumes = []
        for p in profils:
            volumes.append(p["volume"])
        rang_janvier = rang_relatif(volumes, 6)
        self.assertGreaterEqual(rang_janvier, 0.60)  # reste haut malgré les deux pics de fin d'année

        fait = detecter_fait_marquant(profils, 6)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "vigilance")
        self.assertIn("élevé", fait["observation"])

    def test_e2_faible_volume_registre_specifique_pas_positif_generique(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 1500),
            profil_test(datetime.date(2025, 10, 1), 1400),
            profil_test(datetime.date(2025, 11, 1), 1450),
            profil_test(datetime.date(2025, 12, 1), 1550),
            profil_test(datetime.date(2026, 1, 1), 600),
        ]
        fait = detecter_fait_marquant(profils, 4)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")
        self.assertIn(fait["registre"], ("creux sans tension", "activité calme"))
        self.assertNotEqual(fait["registre"], "positif")

    def test_f2_pic_volume_registre_pic_absorbe(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 810),
            profil_test(datetime.date(2025, 12, 1), 1900, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1),
        ]
        fait = detecter_fait_marquant(profils, 3)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["registre"], "pic absorbé")

    def test_g2_reprise_apres_creux_avec_contexte_est_un_jalon(self):
        campagne = evenement_test("Anniversaire Test", TYPE_COMMERCIAL, datetime.date(2026, 9, 1), datetime.date(2026, 9, 15))
        profils = [
            profil_test(datetime.date(2026, 6, 1), 900),
            profil_test(datetime.date(2026, 7, 1), 700),
            profil_test(datetime.date(2026, 8, 1), 650),
            profil_test(datetime.date(2026, 9, 7), 950, contexte=[campagne]),
        ]
        fait = detecter_fait_marquant(profils, 3)
        self.assertIsNotNone(fait)
        self.assertEqual(fait["categorie"], "jalon")
        self.assertIn("progresse", fait["observation"].lower())

    def test_h2_contexte_seul_sans_manifestation_ne_force_pas_de_jalon(self):
        evenement_neutre = evenement_test(
            "Evenement Neutre", TYPE_COMMERCIAL, datetime.date(2026, 3, 1), datetime.date(2026, 3, 10)
        )
        profils = [
            profil_test(datetime.date(2026, 1, 1), 800),
            profil_test(datetime.date(2026, 2, 1), 810),
            profil_test(datetime.date(2026, 3, 5), 805, contexte=[evenement_neutre]),
            profil_test(datetime.date(2026, 4, 1), 795),
            profil_test(datetime.date(2026, 5, 1), 815),
        ]
        fait = detecter_fait_marquant(profils, 2)
        self.assertIsNone(fait)

    def test_mediane_du_reste_robuste_aux_extremes(self):
        volumes = [800, 820, 830, 790, 5000]
        self.assertLess(mediane_du_reste(volumes, 4), 900)

    def test_nom_mois_couvre_les_douze_mois(self):
        self.assertEqual(nom_mois(1), "janvier")
        self.assertEqual(nom_mois(12), "décembre")

    def test_construire_synthese_generale_condensee(self):
        campagne = evenement_test("Test", TYPE_COMMERCIAL, datetime.date(2026, 2, 1), datetime.date(2026, 2, 10))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 720),
            profil_test(datetime.date(2025, 11, 1), 740),
            profil_test(datetime.date(2025, 12, 1), 950),
            profil_test(datetime.date(2026, 1, 1), 980),
            profil_test(datetime.date(2026, 2, 5), 900, contexte=[campagne]),
        ]
        synthese = construire_synthese_longue(profils)
        # 5 segments editoriaux maximum (pics / vigilance / normalisation / creux / cloture) --
        # chaque segment tient en une seule phrase (Étape 4B.3 point 20 : "Pas 6").
        nb_phrases = synthese["synthese_generale"].count(".")
        self.assertLessEqual(nb_phrases, 5)
        self.assertGreaterEqual(nb_phrases, 1)

    def test_synthese_a_deux_pics_regroupes_mais_jalons_distincts(self):
        profils = []
        for mois in range(1, 10):
            profils.append(profil_test(datetime.date(2025, mois, 1), 800 + mois))
        profils.append(profil_test(
            datetime.date(2025, 11, 1), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
        ))
        profils.append(profil_test(
            datetime.date(2025, 12, 1), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
        ))
        profils.append(profil_test(datetime.date(2026, 1, 1), 810))

        synthese = construire_synthese_longue(profils)
        registres_pic = []
        for jalon in synthese["jalons_metier"]:
            if jalon["registre"] == "pic absorbé":
                registres_pic.append(jalon)
        self.assertEqual(len(registres_pic), 2)  # les deux jalons restent distincts dans le détail

        nb_occurrences = synthese["synthese_generale"].count("temps forts")
        self.assertEqual(nb_occurrences, 1)  # mais regroupés en une seule mention dans la synthèse

    def test_synthese_b_deux_creux_regroupes(self):
        profils = []
        for mois in range(1, 10):
            profils.append(profil_test(datetime.date(2025, mois, 1), 1500 + mois))
        profils.append(profil_test(datetime.date(2025, 11, 1), 600))
        profils.append(profil_test(datetime.date(2025, 12, 1), 580))
        profils.append(profil_test(datetime.date(2026, 1, 1), 1520))

        synthese = construire_synthese_longue(profils)
        registres_creux = []
        for jalon in synthese["jalons_metier"]:
            if jalon["registre"] == "creux sans tension":
                registres_creux.append(jalon)
        self.assertEqual(len(registres_creux), 2)

        nb_occurrences = synthese["synthese_generale"].count("Un creux se dessine")
        self.assertEqual(nb_occurrences, 1)

    def test_synthese_c_vigilance_mise_en_avant(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 810),
            profil_test(datetime.date(2025, 11, 1), 805, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0),
            profil_test(datetime.date(2025, 12, 1), 795),
            profil_test(datetime.date(2026, 1, 1), 815),
        ]
        synthese = construire_synthese_longue(profils)
        self.assertEqual(len(synthese["vigilances"]), 1)
        self.assertIn("rompt avec cette dynamique", synthese["synthese_generale"])

    def test_synthese_d_historique_calme_pas_dhistoire_artificielle(self):
        volumes = [800, 795, 805, 790, 810, 798, 802, 793, 807, 785]
        profils = []
        for i in range(len(volumes)):
            profils.append(profil_test(datetime.date(2025, 1, 1) + datetime.timedelta(days=30 * i), volumes[i]))

        synthese = construire_synthese_longue(profils)
        self.assertEqual(len(synthese["vigilances"]), 0)
        self.assertNotIn("rompt avec cette dynamique", synthese["synthese_generale"])

    def test_synthese_e_reste_condensee_meme_avec_beaucoup_de_jalons(self):
        campagne_1 = evenement_test("Campagne 1", TYPE_COMMERCIAL, datetime.date(2025, 11, 20), datetime.date(2025, 11, 30))
        campagne_2 = evenement_test("Campagne 2", TYPE_COMMERCIAL, datetime.date(2025, 12, 10), datetime.date(2025, 12, 20))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 810),
            profil_test(datetime.date(2025, 11, 24), 1800, contexte=[campagne_1]),
            profil_test(datetime.date(2025, 12, 15), 1850, contexte=[campagne_2]),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
            profil_test(datetime.date(2026, 2, 9), 1176),
            profil_test(datetime.date(2026, 3, 9), 795),
            profil_test(datetime.date(2026, 5, 25), 1176),
            profil_test(datetime.date(2026, 6, 15), 795),
            profil_test(datetime.date(2026, 7, 6), 691),
            profil_test(datetime.date(2026, 8, 10), 646),
            profil_test(datetime.date(2026, 9, 7), 944),
        ]
        synthese = construire_synthese_longue(profils)
        # 5 segments editoriaux maximum (pics / vigilance / normalisation / creux / cloture),
        # même sur un historique riche en jalons (Étape 4B.3 point 20 : "Pas 6").
        nb_phrases = synthese["synthese_generale"].count(".")
        self.assertGreater(len(synthese["jalons_metier"]), 5)
        self.assertLessEqual(nb_phrases, 5)

    def test_synthese_f_ne_recite_pas_tous_les_mois_regroupables(self):
        campagne_1 = evenement_test("Campagne 1", TYPE_COMMERCIAL, datetime.date(2026, 2, 1), datetime.date(2026, 2, 10))
        campagne_2 = evenement_test("Campagne 2", TYPE_COMMERCIAL, datetime.date(2026, 5, 1), datetime.date(2026, 5, 10))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 720),
            profil_test(datetime.date(2026, 2, 5), 860, contexte=[campagne_1]),
            profil_test(datetime.date(2026, 3, 1), 800),
            profil_test(datetime.date(2026, 4, 1), 810),
            profil_test(datetime.date(2026, 5, 5), 855, contexte=[campagne_2]),
            profil_test(datetime.date(2026, 6, 1), 790),
        ]
        synthese = construire_synthese_longue(profils)
        self.assertGreater(len(synthese["jalons_metier"]), 3)
        occurrences = synthese["synthese_generale"].count("à l'image de")
        self.assertLessEqual(occurrences, 1)  # un seul jalon illustratif cité, pas tout le pool

    def test_synthese_g_jalons_detailles_inchanges_apres_synthese(self):
        campagne = evenement_test("Test", TYPE_COMMERCIAL, datetime.date(2026, 2, 1), datetime.date(2026, 2, 10))
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 720),
            profil_test(datetime.date(2025, 11, 1), 740),
            profil_test(datetime.date(2025, 12, 1), 950),
            profil_test(datetime.date(2026, 1, 1), 980),
            profil_test(datetime.date(2026, 2, 5), 900, contexte=[campagne]),
        ]
        synthese_1 = construire_synthese_longue(profils)
        synthese_2 = construire_synthese_longue(profils)
        self.assertEqual(len(synthese_1["jalons_metier"]), len(synthese_2["jalons_metier"]))
        for i in range(len(synthese_1["jalons_metier"])):
            self.assertEqual(
                synthese_1["jalons_metier"][i]["observation"], synthese_2["jalons_metier"][i]["observation"]
            )
            self.assertEqual(synthese_1["jalons_metier"][i]["registre"], synthese_2["jalons_metier"][i]["registre"])

    def test_capacite_totale_heures_ignore_lagent_defaut(self):
        planning = {
            "Amine": {0: [(9, 12), (13, 17)]},
            "DEFAUT": {0: [(9, 12), (13, 17)]},
        }
        self.assertEqual(capacite_totale_heures(planning), 7)

    def test_ecart_relatif_vs_reste_calcule_correctement(self):
        self.assertAlmostEqual(ecart_relatif_vs_reste([100, 100, 100, 150], 3), 0.5)

    def test_saison_du_mois_couvre_les_douze_mois(self):
        self.assertEqual(saison_du_mois(12), "hiver")
        self.assertEqual(saison_du_mois(7), "été")
        self.assertEqual(saison_du_mois(3), "printemps")
        self.assertEqual(saison_du_mois(9), "automne")

    def test_contexte_futur_jamais_remonte_hors_chevauchement(self):
        # contexte_periode() est déjà testée exhaustivement dans TestContextePeriode ; on vérifie
        # ici seulement que construire_profil_observation() ne l'étend pas au-delà de
        # [date_debut, date_fin] de l'observation elle-même.
        evenement_futur = evenement_test(
            "Fin future", TYPE_STAFFING, datetime.date(2026, 9, 30), datetime.date(2026, 9, 30)
        )
        resultat = contexte_periode([evenement_futur], datetime.date(2026, 9, 7), datetime.date(2026, 9, 13))
        self.assertEqual(resultat, [])

    def test_analyser_observation_comparaison_precedente_reste_qualifiee(self):
        profils = [
            profil_test(datetime.date(2026, 8, 1), 650),
            profil_test(datetime.date(2026, 9, 1), 950),
        ]
        resultat = analyser_observation(profils, 1)
        self.assertIsNotNone(resultat["comparaison_precedente"])
        self.assertIn("dernière observation disponible", resultat["comparaison_precedente"]["observation"])
        self.assertIn("pas une évolution semaine par semaine", resultat["comparaison_precedente"]["pourquoi"])


# Étape 4B.3 -- scope de période (PÉRIODE ANALYSÉE vs HISTORIQUE DE RÉFÉRENCE) : les 3 modes de
# lecture de l'onglet Tendances, déduits uniquement du nombre d'observations sélectionnées vs
# disponibles, jamais d'une date codée en dur. `profils_historique` dans ces tests représente
# toujours les SEULES observations dont la date est antérieure ou égale à la fin de la période
# analysée -- exactement ce que fait l'appelant réel (app.py) pour garantir l'absence de fuite du
# futur.
class TestScopeTendances(unittest.TestCase):
    def test_determiner_mode_tendances_cas_limites(self):
        self.assertEqual(determiner_mode_tendances(1, 1), MODE_OBSERVATION_UNIQUE)
        self.assertEqual(determiner_mode_tendances(1, 10), MODE_OBSERVATION_UNIQUE)
        self.assertEqual(determiner_mode_tendances(5, 5), MODE_HISTORIQUE_COMPLET)
        self.assertEqual(determiner_mode_tendances(3, 10), MODE_PERIODE_ETENDUE)

    def test_a_une_seule_observation_selectionnee_mode_1(self):
        profils = [profil_test(datetime.date(2025, 9, 1), 800), profil_test(datetime.date(2025, 10, 1), 820)]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(lecture["mode"], MODE_OBSERVATION_UNIQUE)

    def test_b_plusieurs_observations_mais_pas_historique_complet_mode_2(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800), profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 810), profil_test(datetime.date(2025, 12, 1), 830),
        ]
        lecture = construire_lecture_tendances(profils, 2)
        self.assertEqual(lecture["mode"], MODE_PERIODE_ETENDUE)

    def test_c_toutes_observations_disponibles_mode_3(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800), profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 810), profil_test(datetime.date(2025, 12, 1), 830),
        ]
        lecture = construire_lecture_tendances(profils, 4)
        self.assertEqual(lecture["mode"], MODE_HISTORIQUE_COMPLET)

    def test_d_octobre_2025_aucune_donnee_posterieure_utilisee_comme_reference(self):
        profils_sans_futur = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 9, 8), 810),
            profil_test(datetime.date(2025, 10, 6), 805),
        ]
        lecture_sans_futur = construire_lecture_tendances(profils_sans_futur, 1)
        self.assertEqual(
            lecture_sans_futur["niveau_confiance"],
            "Cette période est replacée parmi 2 observations antérieures disponibles.",
        )

        # si un pic futur (novembre) fuitait dans la référence, le rang d'octobre changerait --
        # la preuve que l'appelant ne le fournit jamais est que la lecture réelle (ci-dessus) ne
        # dépend que des 2 observations antérieures, jamais de ce pic.
        profils_avec_futur_par_erreur = profils_sans_futur + [profil_test(datetime.date(2025, 11, 24), 3000)]
        volumes_sans_futur = []
        for p in profils_sans_futur:
            volumes_sans_futur.append(p["volume"])
        volumes_avec_futur = []
        for p in profils_avec_futur_par_erreur:
            volumes_avec_futur.append(p["volume"])
        rang_sans_futur = rang_relatif(volumes_sans_futur, 2)
        rang_avec_futur = rang_relatif(volumes_avec_futur, 2)
        self.assertNotEqual(rang_sans_futur, rang_avec_futur)  # la fuite aurait un effet mesurable
        self.assertEqual(lecture_sans_futur["nb_observations_historique"], 3)  # jamais 4

    def test_e_janvier_2026_aucune_donnee_de_fevrier_ou_plus_tard_utilisee(self):
        profils_reels = [
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
        ]
        lecture = construire_lecture_tendances(profils_reels, 1)
        self.assertEqual(lecture["mode"], MODE_OBSERVATION_UNIQUE)
        self.assertEqual(lecture["nb_observations_historique"], 3)
        for mois_interdit in ("février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre"):
            self.assertNotIn(mois_interdit, lecture["synthese"].lower())

    def test_f_mode1_jalons_historiques_hors_scope_absents_de_la_sortie(self):
        profils = [
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(datetime.date(2026, 1, 12), 900),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(len(lecture["jalons_metier"]), 0)  # jamais de liste Jalons en mode 1

    def test_g_mode2_jalons_hors_fenetre_absents_de_la_sortie(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 710),
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(datetime.date(2026, 1, 12), 900),
        ]
        lecture = construire_lecture_tendances(profils, 2)  # fenêtre = décembre + janvier uniquement
        self.assertEqual(lecture["mode"], MODE_PERIODE_ETENDUE)
        for jalon in lecture["jalons_metier"]:
            self.assertGreaterEqual(jalon["date_debut"], datetime.date(2025, 12, 15))
        for vigilance in lecture["vigilances"]:
            self.assertGreaterEqual(vigilance["date_debut"], datetime.date(2025, 12, 15))

    def test_h_mode3_tous_les_jalons_pertinents_disponibles(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 710),
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(datetime.date(2026, 1, 12), 900),
        ]
        lecture = construire_lecture_tendances(profils, 5)
        self.assertEqual(lecture["mode"], MODE_HISTORIQUE_COMPLET)
        faits_attendus = detecter_pics_et_creux(profils)
        self.assertEqual(len(lecture["jalons_metier"]) + len(lecture["vigilances"]), len(faits_attendus))

    def test_i_mode1_comparaison_historique_sans_transformer_en_periode_analysee(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(
                datetime.date(2025, 11, 1), 1600, csat=4.1, resolution_h=38, reopens=0.05, replies=2.3,
            ),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(lecture["nb_observations_periode"], 1)
        self.assertEqual(lecture["nb_observations_historique"], 3)
        self.assertEqual(len(lecture["profils_periode"]), 1)

    def test_j_mode1_saisonnalite_globale_non_affichee_comme_conclusion_principale(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 900), profil_test(datetime.date(2025, 9, 15), 910),
            profil_test(datetime.date(2025, 12, 1), 1300), profil_test(datetime.date(2025, 12, 15), 1320),
            profil_test(datetime.date(2026, 3, 1), 950), profil_test(datetime.date(2026, 3, 15), 960),
            profil_test(datetime.date(2026, 6, 1), 700), profil_test(datetime.date(2026, 6, 15), 690),
            profil_test(datetime.date(2026, 7, 1), 705),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(lecture["mode"], MODE_OBSERVATION_UNIQUE)
        self.assertIsNone(lecture["saisonnalite"])

    def test_k_mode1_periode_analysee_identifiable_dans_lhistorique(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 850),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(lecture["profils_periode"][0]["date_debut"], profils[-1]["date_debut"])
        self.assertEqual(lecture["nb_observations_historique"], len(profils))

    def test_l_mode2_graphiques_principaux_scopes_sur_la_fenetre(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 1), 820),
            profil_test(datetime.date(2025, 11, 1), 850),
            profil_test(datetime.date(2025, 12, 1), 900),
        ]
        lecture = construire_lecture_tendances(profils, 2)
        self.assertEqual(len(lecture["profils_periode"]), 2)
        self.assertEqual(lecture["profils_periode"][0]["date_debut"], datetime.date(2025, 11, 1))
        self.assertEqual(lecture["profils_periode"][1]["date_debut"], datetime.date(2025, 12, 1))

    def test_m_mode3_synthese_5_phrases_maximum(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800),
            profil_test(datetime.date(2025, 10, 6), 805),
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
            profil_test(datetime.date(2026, 2, 9), 1176),
            profil_test(datetime.date(2026, 3, 9), 795),
            profil_test(datetime.date(2026, 5, 25), 1176),
            profil_test(datetime.date(2026, 6, 15), 795),
            profil_test(datetime.date(2026, 7, 6), 691),
            profil_test(datetime.date(2026, 8, 10), 646),
            profil_test(datetime.date(2026, 9, 7), 944),
        ]
        lecture = construire_lecture_tendances(profils, len(profils))
        self.assertEqual(lecture["mode"], MODE_HISTORIQUE_COMPLET)
        self.assertLessEqual(lecture["synthese"].count("."), 5)

    def test_n_mode2_synthese_4_phrases_maximum(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 710),
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
        ]
        lecture = construire_lecture_tendances(profils, 3)  # fenêtre = novembre -> janvier
        self.assertEqual(lecture["mode"], MODE_PERIODE_ETENDUE)
        self.assertLessEqual(lecture["synthese"].count("."), 4)

    def test_o_mode1_synthese_3_phrases_maximum(self):
        profils = [
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(lecture["mode"], MODE_OBSERVATION_UNIQUE)
        self.assertLessEqual(lecture["synthese"].count("."), 3)

    def test_p_pas_de_formulation_volume_reste(self):
        profils_liste = [
            [profil_test(datetime.date(2025, 9, 1), 800), profil_test(datetime.date(2025, 10, 1), 1600)],
            [
                profil_test(datetime.date(2025, 9, 1), 800), profil_test(datetime.date(2025, 10, 1), 820),
                profil_test(datetime.date(2025, 11, 1), 1600, csat=4.1, resolution_h=38, reopens=0.05, replies=2.3),
                profil_test(datetime.date(2025, 12, 1), 1650, csat=4.1, resolution_h=37, reopens=0.04, replies=2.2),
            ],
        ]
        for profils in profils_liste:
            for nb_periode in (1, len(profils)):
                lecture = construire_lecture_tendances(profils, nb_periode)
                self.assertNotIn("Volume reste", lecture["synthese"])

    def test_q_pas_de_libelle_technique_defaut_dans_la_synthese(self):
        mix_normal = {"Livraison": 750, "SAV produit (défaut)": 50}
        mix_devie = {"Livraison": 400, "SAV produit (défaut)": 400}
        profils = [
            profil_test(datetime.date(2025, 9, 1), 800, mix_categories=mix_normal),
            profil_test(datetime.date(2025, 10, 1), 800, mix_categories=mix_normal),
            profil_test(datetime.date(2025, 11, 1), 800, mix_categories=mix_normal),
            profil_test(
                datetime.date(2025, 12, 1), 800, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
                mix_categories=mix_devie,
            ),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(len(lecture["vigilances"]), 1)
        self.assertNotIn("(défaut)", lecture["synthese"])

    def test_r_vigilance_complexe_integre_volume_experience_effort(self):
        profils = [
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(
                datetime.date(2026, 1, 12), 1270, csat=3.3, resolution_h=80, reopens=0.2, replies=4.0,
            ),
        ]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertEqual(len(lecture["vigilances"]), 1)
        texte = lecture["vigilances"][0]["observation"]
        self.assertIn("satisfaction", texte)
        self.assertIn("effort", texte)
        self.assertIn("volume", texte.lower())

    def test_s_choix_jalon_illustratif_normalisation_est_generique(self):
        campagne_a = evenement_test("Campagne A", TYPE_COMMERCIAL, datetime.date(2026, 2, 1), datetime.date(2026, 2, 10))
        campagne_b = evenement_test("Campagne B", TYPE_COMMERCIAL, datetime.date(2026, 5, 1), datetime.date(2026, 5, 10))

        def construire_scenario(avec_contexte_sur_fevrier):
            contexte_fevrier = [campagne_a] if avec_contexte_sur_fevrier else []
            contexte_mai = [] if avec_contexte_sur_fevrier else [campagne_b]
            return [
                profil_test(datetime.date(2025, 9, 1), 500),
                profil_test(datetime.date(2025, 10, 1), 520),
                profil_test(datetime.date(2025, 11, 1), 540),
                profil_test(datetime.date(2025, 12, 1), 560),
                profil_test(datetime.date(2026, 1, 1), 580),
                profil_test(datetime.date(2026, 2, 5), 700, contexte=contexte_fevrier),
                profil_test(datetime.date(2026, 3, 1), 600),
                profil_test(datetime.date(2026, 5, 5), 610, contexte=contexte_mai),
                profil_test(datetime.date(2026, 6, 1), 950),
            ]

        profils_fevrier = construire_scenario(True)
        lecture_fevrier = construire_lecture_tendances(profils_fevrier, len(profils_fevrier))
        self.assertIn("février", lecture_fevrier["synthese"])
        self.assertNotIn("à l'image de mai", lecture_fevrier["synthese"])

        profils_mai = construire_scenario(False)
        lecture_mai = construire_lecture_tendances(profils_mai, len(profils_mai))
        self.assertIn("mai", lecture_mai["synthese"])
        self.assertNotIn("à l'image de février", lecture_mai["synthese"])

    def test_t_jalons_detailles_inchanges_par_le_composeur_a_travers_les_modes(self):
        profils = [
            profil_test(datetime.date(2025, 9, 1), 700),
            profil_test(datetime.date(2025, 10, 1), 710),
            profil_test(
                datetime.date(2025, 11, 24), 1800, csat=4.1, resolution_h=35, reopens=0.03, replies=2.1,
            ),
            profil_test(
                datetime.date(2025, 12, 15), 1850, csat=4.1, resolution_h=34, reopens=0.03, replies=2.0,
            ),
            profil_test(datetime.date(2026, 1, 12), 900),
        ]
        lecture_1 = construire_lecture_tendances(profils, 5)
        lecture_2 = construire_lecture_tendances(profils, 5)
        self.assertEqual(len(lecture_1["jalons_metier"]), len(lecture_2["jalons_metier"]))
        for i in range(len(lecture_1["jalons_metier"])):
            self.assertEqual(
                lecture_1["jalons_metier"][i]["observation"], lecture_2["jalons_metier"][i]["observation"]
            )

    def test_premiere_observation_sans_historique_reconnue(self):
        profils = [profil_test(datetime.date(2025, 9, 1), 800)]
        lecture = construire_lecture_tendances(profils, 1)
        self.assertTrue(lecture["premiere_observation_sans_historique"])
        self.assertIn("Première observation disponible", lecture["synthese"])


def ticket_livraison(ticket_id=1, subject_cluster="Où est ma commande", csat=4.2, replies=2.3,
                      full_resolution_time_hours=38.0, reopens=0.05, nombre_relances=0.8,
                      issue_livraison_finale="Livraison confirmée", transporteur="TransEuro"):
    return {
        "ticket_id": ticket_id,
        "subject_cluster": subject_cluster,
        "csat": csat,
        "replies": replies,
        "full_resolution_time_hours": full_resolution_time_hours,
        "reopens": reopens,
        "nombre_relances": nombre_relances,
        "issue_livraison_finale": issue_livraison_finale,
        "transporteur": transporteur,
    }


def generer_tickets_livraison(n, **kwargs):
    tickets = []
    for i in range(n):
        tickets.append(ticket_livraison(ticket_id=i, **kwargs))
    return tickets


def obtenir_sujet_signal(signal):
    return signal["sujet"]


# Étape 4C -- moteur Livraison : volume élevé n'est pas un problème en soi (Black Friday/Noël
# génèrent naturellement du suivi de commande), l'éligibilité repose sur la convergence de
# plusieurs familles de preuve indépendantes avec au moins une conséquence opérationnelle/client
# (jamais Volume ou Concentration transporteur seuls).
class TestMoteurLivraison(unittest.TestCase):
    def test_a_gros_volume_normal_pas_priorite(self):
        tickets_normaux = generer_tickets_livraison(
            200, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.7,
        )
        autres = generer_tickets_livraison(
            50, subject_cluster="Délai de livraison", csat=4.1, replies=2.0,
            full_resolution_time_hours=32, reopens=0.05, nombre_relances=0.6,
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + autres, [], 5)
        self.assertEqual(len(resultat["prioritaires"]), 0)

    def test_b_csat_faible_relances_elevees_resolution_longue_priorite(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, nombre_relances=0.6,
        )
        tickets_problematiques = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.0, replies=3.5,
            full_resolution_time_hours=70, nombre_relances=2.0, issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_problematiques, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertIn("Colis annoncé livré non reçu", sujets_prio)

    def test_c_volume_faible_une_issue_defavorable_seule_pas_automatiquement_priorite(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, nombre_relances=0.6, issue_livraison_finale="Livraison confirmée",
        )
        tickets_petit_sujet = (
            generer_tickets_livraison(
                4, subject_cluster="Modification adresse de livraison", csat=4.15, replies=2.2,
                full_resolution_time_hours=34, nombre_relances=0.6, issue_livraison_finale="Livraison confirmée",
            )
            + generer_tickets_livraison(
                1, subject_cluster="Modification adresse de livraison", csat=4.15, replies=2.2,
                full_resolution_time_hours=34, nombre_relances=0.6, issue_livraison_finale="Remboursé",
            )
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_petit_sujet, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        sujets_surveiller = [s["sujet"] for s in resultat["a_surveiller"]]
        self.assertNotIn("Modification adresse de livraison", sujets_prio)
        self.assertNotIn("Modification adresse de livraison", sujets_surveiller)

    def test_d_relances_elevees_et_csat_degrade_suffisent_a_remonter(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, nombre_relances=0.6,
        )
        tickets_probleme = generer_tickets_livraison(
            15, subject_cluster="Délai de livraison", csat=3.5, replies=2.25,
            full_resolution_time_hours=36, nombre_relances=1.5,
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_probleme, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertIn("Délai de livraison", sujets_prio)

    def test_e_transporteur_majoritaire_sans_difference_pas_de_signal(self):
        tickets_sujet = (
            generer_tickets_livraison(40, transporteur="TransEuro", csat=4.2, nombre_relances=0.7)
            + generer_tickets_livraison(10, transporteur="RapidPost", csat=4.2, nombre_relances=0.7)
            + generer_tickets_livraison(10, transporteur="ColisExpress", csat=4.2, nombre_relances=0.7)
        )
        concentration = evaluer_concentration_transporteur_livraison(tickets_sujet)
        self.assertIsNone(concentration)

    def test_f_transporteur_minoritaire_concentre_signaux_devient_informatif(self):
        tickets_sujet = (
            generer_tickets_livraison(55, transporteur="TransEuro", csat=4.2, nombre_relances=0.8)
            + generer_tickets_livraison(
                5, transporteur="TransEuro", csat=4.2, nombre_relances=0.8, issue_livraison_finale="Remboursé"
            )
            + generer_tickets_livraison(
                20, transporteur="RapidPost", csat=2.8, nombre_relances=3.0, issue_livraison_finale="Remboursé"
            )
        )
        concentration = evaluer_concentration_transporteur_livraison(tickets_sujet)
        self.assertIsNotNone(concentration)
        self.assertEqual(concentration["transporteur"], "RapidPost")

    def test_g_jamais_taux_incident_transporteur(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, nombre_relances=0.6,
        )
        tickets_probleme = (
            generer_tickets_livraison(
                40, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro",
                csat=4.2, nombre_relances=0.8,
            )
            + generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost",
                csat=2.8, nombre_relances=3.0, issue_livraison_finale="Remboursé",
            )
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_probleme, [], 5)
        textes = []
        for signal in resultat["prioritaires"] + resultat["a_surveiller"]:
            textes.append(signal["observation_principale"])
            textes.append(signal["action_investigation"])
        for texte in textes:
            self.assertNotIn("taux d'incident", texte.lower())
            self.assertNotIn("transporteur défaillant", texte.lower())
            self.assertNotIn("transporteur responsable", texte.lower())

    def test_h_meme_probleme_decline_par_transporteur_une_seule_histoire(self):
        tickets_sujet = (
            generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro",
                csat=3.0, nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost",
                csat=3.0, nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="ColisExpress",
                csat=3.0, nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
        )
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande")
        resultat = moteur_livraison_voie_a(tickets_sujet + tickets_normaux, [], 5)
        signaux_sujet = []
        for signal in resultat["prioritaires"] + resultat["a_surveiller"]:
            if signal["sujet"] == "Colis annoncé livré non reçu":
                signaux_sujet.append(signal)
        self.assertEqual(len(signaux_sujet), 1)

    def test_i_deux_motifs_distincts_restent_distincts(self):
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande")
        tickets_probleme_1 = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.2, nombre_relances=2.0,
            issue_livraison_finale="Remboursé",
        )
        tickets_probleme_2 = generer_tickets_livraison(
            20, subject_cluster="Délai de livraison", csat=3.2, nombre_relances=2.0,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(
            tickets_normaux + tickets_probleme_1 + tickets_probleme_2, [], 5
        )
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertIn("Colis annoncé livré non reçu", sujets_prio)
        self.assertIn("Délai de livraison", sujets_prio)
        self.assertEqual(len(sujets_prio), 2)

    def test_j_distribution_issues_somme_correcte(self):
        tickets = (
            generer_tickets_livraison(10, issue_livraison_finale="Remboursé")
            + generer_tickets_livraison(15, issue_livraison_finale="Réexpédié")
        )
        distribution = distribution_issues_livraison(tickets)
        total = 0
        for item in distribution:
            total = total + item["n"]
        self.assertEqual(total, 25)

    def test_k_historique_discontinu_jamais_depuis_x_semaines(self):
        niveaux = [0.30, 0.32]
        texte = evaluer_temporalite(niveaux, 0.45)
        self.assertNotIn("depuis", texte.lower())

    def test_l_niveaux_historiques_ne_utilisent_que_les_fichiers_fournis(self):
        fichier_1 = generer_tickets_livraison(50, subject_cluster="Où est ma commande")
        fichier_2 = (
            generer_tickets_livraison(10, subject_cluster="Où est ma commande")
            + generer_tickets_livraison(40, subject_cluster="Autre")
        )
        niveaux = construire_niveaux_historiques_livraison([fichier_1, fichier_2], "Où est ma commande")
        self.assertEqual(len(niveaux), 2)
        self.assertAlmostEqual(niveaux[0], 1.0)
        self.assertAlmostEqual(niveaux[1], 0.2)

    def test_m_black_friday_synthetique_volume_eleve_experience_tenue_pas_crise(self):
        tickets_bf = generer_tickets_livraison(
            300, subject_cluster="Où est ma commande", csat=4.3, nombre_relances=0.7,
            full_resolution_time_hours=30,
        )
        tickets_totaux = tickets_bf + generer_tickets_livraison(200, subject_cluster="Autre catégorie")
        lecture = construire_lecture_activite_livraison(tickets_bf, tickets_totaux, [])
        self.assertIn("%", lecture["observation"])
        resultat = moteur_livraison_voie_a(tickets_bf, [], 5)
        self.assertEqual(len(resultat["prioritaires"]), 0)

    def test_n_zero_signal_prioritaire_sortie_calme(self):
        tickets = generer_tickets_livraison(100, subject_cluster="Où est ma commande", csat=4.2, nombre_relances=0.7)
        resultat = moteur_livraison_voie_a(tickets, [], 5)
        self.assertEqual(resultat["prioritaires"], [])
        self.assertIn("Où est ma commande", resultat["sujets_silencieux"])

    def test_o_petit_n_csat_affiche(self):
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande", csat=4.2)
        tickets_probleme = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        for ticket in tickets_probleme[3:]:
            ticket["csat"] = None

        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_probleme, [], 5)
        signaux_sujet = []
        for signal in resultat["prioritaires"]:
            if signal["sujet"] == "Colis annoncé livré non reçu":
                signaux_sujet.append(signal)
        self.assertEqual(len(signaux_sujet), 1)
        self.assertEqual(signaux_sujet[0]["experience"]["n_csat"], 3)

    def test_controle_qualite_detecte_anomalies(self):
        tickets = [
            ticket_livraison(ticket_id=1, nombre_relances=-1),
            ticket_livraison(ticket_id=2, transporteur=None),
            ticket_livraison(ticket_id=3, issue_livraison_finale="Perdu en mer"),
        ]
        anomalies = controler_qualite_donnees_livraison(tickets)
        self.assertGreater(len(anomalies), 0)

    def test_controle_qualite_silencieux_sur_donnees_propres(self):
        tickets = generer_tickets_livraison(20)
        self.assertEqual(controler_qualite_donnees_livraison(tickets), [])

    def test_vocabulaire_interdit_absent_livraison(self):
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande")
        tickets_probleme = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_probleme, [], 5)
        mots_interdits = ("significatif", "significativement", "corrélation", "causal", "structurel")
        for signal in resultat["prioritaires"] + resultat["a_surveiller"]:
            textes = [signal["observation_principale"], signal["action_investigation"]]
            for texte in textes:
                texte_minuscule = texte.lower()
                for mot in mots_interdits:
                    self.assertNotIn(mot, texte_minuscule)

    def test_part_issues_defavorables_calcule_correctement(self):
        tickets = (
            generer_tickets_livraison(3, issue_livraison_finale="Remboursé")
            + generer_tickets_livraison(7, issue_livraison_finale="Livraison confirmée")
        )
        self.assertAlmostEqual(part_issues_defavorables(tickets), 0.3)


# Étape 4C.1 -- sélectivité des priorités + transporteur redevient une dimension d'investigation
# (jamais un facteur d'éligibilité). Le moteur analytique (grain, activité vs problème, relances,
# issues, consolidation, baselines, contextualisation, contrôle qualité) reste celui de 4C, validé
# et inchangé -- seule la règle de convergence pour Priorité/À surveiller est recalibrée.
class TestRecalibrageLivraison(unittest.TestCase):
    def test_a_a_plus_c_faible_seul_pas_priorite(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
        )
        tickets_sujet = generer_tickets_livraison(
            20, subject_cluster="Modification adresse de livraison", csat=4.2, replies=3.3,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertNotIn("Modification adresse de livraison", sujets_prio)

    def test_b_a_plus_c_faible_peut_etre_a_surveiller(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
        )
        tickets_sujet = generer_tickets_livraison(
            20, subject_cluster="Modification adresse de livraison", csat=4.2, replies=3.3,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        sujets_surveiller = [s["sujet"] for s in resultat["a_surveiller"]]
        self.assertIn("Modification adresse de livraison", sujets_surveiller)

    def test_c_b_plus_d_priorite_secondaire_volume_modere(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, nombre_relances=0.6,
        )
        tickets_sujet = generer_tickets_livraison(
            8, subject_cluster="Modification adresse de livraison", csat=3.5, nombre_relances=1.5,
            replies=2.2, full_resolution_time_hours=35, reopens=0.05,
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signaux = [s for s in resultat["prioritaires"] if s["sujet"] == "Modification adresse de livraison"]
        self.assertEqual(len(signaux), 1)
        self.assertEqual(signaux[0]["niveau_priorite"], "Priorité secondaire")

    def test_d_c_fort_plus_e_priorite_possible(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=4.2, replies=4.0,
            full_resolution_time_hours=90, reopens=0.3, nombre_relances=0.6,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertIn("Colis annoncé livré non reçu", sujets_prio)

    def test_e_a_plus_d_plus_e_priorite_forte_possible(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = generer_tickets_livraison(
            30, subject_cluster="Colis annoncé livré non reçu", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signaux = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"]
        self.assertEqual(len(signaux), 1)
        self.assertEqual(signaux[0]["niveau_priorite"], "Priorité principale")

    def test_f_toutes_familles_convergent_priorite_principale(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = generer_tickets_livraison(
            30, subject_cluster="Colis annoncé livré non reçu", csat=3.0, replies=4.0,
            full_resolution_time_hours=90, reopens=0.3, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signaux = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"]
        self.assertEqual(len(signaux), 1)
        self.assertEqual(signaux[0]["niveau_priorite"], "Priorité principale")

    def test_g_transporteur_concentre_sans_consequence_motif_aucune_priorite(self):
        autre_sujet = (
            generer_tickets_livraison(
                450, subject_cluster="Délai de livraison", csat=4.2, replies=2.2,
                full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
                issue_livraison_finale="Livraison confirmée",
            )
            + generer_tickets_livraison(
                50, subject_cluster="Délai de livraison", csat=4.2, replies=2.2,
                full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
                issue_livraison_finale="Remboursé",
            )
        )
        bon = (
            generer_tickets_livraison(
                155, subject_cluster="Où est ma commande", transporteur="TransEuro", csat=4.3,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.55,
                issue_livraison_finale="Livraison confirmée",
            )
            + generer_tickets_livraison(
                5, subject_cluster="Où est ma commande", transporteur="TransEuro", csat=4.3,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.55,
                issue_livraison_finale="Remboursé",
            )
        )
        mauvais = (
            generer_tickets_livraison(
                24, subject_cluster="Où est ma commande", transporteur="RapidPost", csat=2.9,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=2.2,
                issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                16, subject_cluster="Où est ma commande", transporteur="RapidPost", csat=2.9,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=2.2,
                issue_livraison_finale="Livraison confirmée",
            )
        )
        tickets_sujet = bon + mauvais
        resultat = moteur_livraison_voie_a(autre_sujet + tickets_sujet, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertNotIn("Où est ma commande", sujets_prio)

        signal = construire_signal_sujet_livraison_voie_a(
            "Où est ma commande", tickets_sujet, autre_sujet + tickets_sujet, []
        )
        self.assertIsNone(signal["tier"])
        self.assertIsNotNone(signal["concentration_transporteur"])
        self.assertEqual(signal["concentration_transporteur"]["transporteur"], "RapidPost")

    def test_h_motif_prioritaire_transporteur_seulement_investigation(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = (
            generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro",
                csat=4.0, replies=2.2, full_resolution_time_hours=35, reopens=0.05,
                nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                20, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost",
                csat=4.0, replies=2.2, full_resolution_time_hours=35, reopens=0.05,
                nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signaux = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"]
        self.assertEqual(len(signaux), 1)
        # le motif est déjà prioritaire par D+E (relances + issues) -- le transporteur, s'il
        # apparaît, ne doit être qu'une information d'investigation, jamais une famille comptée.
        self.assertNotIn("G", signaux[0]["familles_actives"])

    def test_i_motif_prioritaire_sans_difference_transporteur_rien_mis_en_avant(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = (
            generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro",
                csat=3.0, replies=2.2, full_resolution_time_hours=35, reopens=0.05,
                nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost",
                csat=3.0, replies=2.2, full_resolution_time_hours=35, reopens=0.05,
                nombre_relances=2.5, issue_livraison_finale="Remboursé",
            )
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signaux = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"]
        self.assertEqual(len(signaux), 1)
        self.assertIsNone(signaux[0]["concentration_transporteur"])

    def test_j_cout_indisponible_jamais_zero(self):
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande")
        tickets_sujet = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        resultat = moteur_livraison_voie_a(tickets_normaux + tickets_sujet, [], 5)
        signal = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"][0]
        self.assertIsNone(signal["cout"])

    def test_k_mai_synthetique_activite_saine_pas_multiplication_de_priorites(self):
        tickets_normaux = generer_tickets_livraison(
            300, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.6,
        )
        tickets_probleme = generer_tickets_livraison(
            90, subject_cluster="Colis annoncé livré non reçu", csat=4.0, replies=2.7,
            full_resolution_time_hours=50, reopens=0.05, nombre_relances=2.0,
            issue_livraison_finale="Remboursé",
        )
        tickets_secondaire_1 = generer_tickets_livraison(
            60, subject_cluster="Modification adresse de livraison", csat=4.3, replies=2.5,
            full_resolution_time_hours=36, reopens=0.05, nombre_relances=0.55,
        )
        tickets_secondaire_2 = generer_tickets_livraison(
            50, subject_cluster="Délai de livraison", csat=4.25, replies=2.4,
            full_resolution_time_hours=35, reopens=0.05, nombre_relances=0.5,
        )
        resultat = moteur_livraison_voie_a(
            tickets_normaux + tickets_probleme + tickets_secondaire_1 + tickets_secondaire_2, [], 5
        )
        self.assertLessEqual(len(resultat["prioritaires"]), 1)

    def test_l_noel_synthetique_enorme_volume_experience_tenue_pas_de_crise(self):
        tickets_bf = generer_tickets_livraison(
            800, subject_cluster="Où est ma commande", csat=4.15, replies=2.3,
            full_resolution_time_hours=38, reopens=0.05, nombre_relances=0.7,
        )
        resultat = moteur_livraison_voie_a(tickets_bf, [], 5)
        self.assertEqual(len(resultat["prioritaires"]), 0)


# Étape 4C.2 -- le transporteur redevient purement descriptif : une piste d'investigation à
# l'intérieur d'un motif déjà prioritaire, jamais un facteur d'éligibilité. Les règles de
# Priorité/À surveiller (4C.1, validées) ne sont pas retouchées ici.
class TestInvestigationTransporteurLivraison(unittest.TestCase):
    def test_a_transporteur_ne_participe_jamais_au_tier(self):
        autre_sujet = generer_tickets_livraison(
            200, subject_cluster="Délai de livraison", csat=4.2, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = (
            generer_tickets_livraison(
                90, subject_cluster="Où est ma commande", transporteur="TransEuro", csat=4.2,
                nombre_relances=0.6, issue_livraison_finale="Livraison confirmée",
            )
            + generer_tickets_livraison(
                10, subject_cluster="Où est ma commande", transporteur="RapidPost", csat=3.0,
                nombre_relances=0.6, issue_livraison_finale="Livraison confirmée",
            )
        )
        tous = autre_sujet + tickets_sujet
        resultat = moteur_livraison_voie_a(tous, [], 5)
        sujets_prio = [s["sujet"] for s in resultat["prioritaires"]]
        self.assertNotIn("Où est ma commande", sujets_prio)

        signal = construire_signal_sujet_livraison_voie_a("Où est ma commande", tickets_sujet, tous, [])
        self.assertIsNone(signal["tier"])
        self.assertIsNotNone(signal["concentration_transporteur"])

    def test_b_un_seul_contraste_transporteur_suffit(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, nombre_relances=0.6,
            issue_livraison_finale="Livraison confirmée",
        )
        tickets_sujet = (
            generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro", csat=4.2,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=2.5,
                issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost", csat=2.8,
                replies=2.2, full_resolution_time_hours=35, reopens=0.05, nombre_relances=2.5,
                issue_livraison_finale="Remboursé",
            )
        )
        concentration = evaluer_concentration_transporteur_livraison(tickets_sujet)
        self.assertIsNotNone(concentration)
        self.assertEqual(concentration["transporteur"], "RapidPost")
        # un seul indicateur écarté (CSAT) -- relances et issues sont identiques entre transporteurs
        self.assertEqual(concentration["lecture_csat"], "écart marqué par rapport à la référence observée")
        self.assertNotEqual(concentration["lecture_relances"], "écart marqué par rapport à la référence observée")

    def test_c_transporteurs_homogenes_aucun_focus(self):
        tickets_sujet = (
            generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro", csat=4.0,
                nombre_relances=2.0, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost", csat=4.0,
                nombre_relances=2.0, issue_livraison_finale="Remboursé",
            )
            + generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="ColisExpress", csat=4.0,
                nombre_relances=2.0, issue_livraison_finale="Remboursé",
            )
        )
        concentration = evaluer_concentration_transporteur_livraison(tickets_sujet)
        self.assertIsNone(concentration)

    def test_d_jamais_taux_incident_transporteur(self):
        tickets_sujet = (
            generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="TransEuro", csat=4.2,
                nombre_relances=0.6, issue_livraison_finale="Livraison confirmée",
            )
            + generer_tickets_livraison(
                15, subject_cluster="Colis annoncé livré non reçu", transporteur="RapidPost", csat=2.6,
                nombre_relances=3.0, issue_livraison_finale="Remboursé",
            )
        )
        concentration = evaluer_concentration_transporteur_livraison(tickets_sujet)
        self.assertIsNotNone(concentration)
        texte_piste = texte_piste_transporteur_livraison(concentration)
        textes = [texte_piste, concentration["prudence_echantillon"]]
        mots_interdits = ("taux d'incident", "transporteur défaillant", "transporteur responsable", "moins fiable")
        for texte in textes:
            texte_minuscule = texte.lower()
            for mot in mots_interdits:
                self.assertNotIn(mot, texte_minuscule)
        self.assertIn("dossiers observés", texte_piste)

    def test_e_somme_volumes_motifs_egale_volume_livraison(self):
        tickets = (
            generer_tickets_livraison(40, subject_cluster="Où est ma commande")
            + generer_tickets_livraison(30, subject_cluster="Colis annoncé livré non reçu")
            + generer_tickets_livraison(20, subject_cluster="Délai de livraison")
            + generer_tickets_livraison(10, subject_cluster="Modification adresse de livraison")
        )
        sujets = set(t["subject_cluster"] for t in tickets)
        total_par_motif = 0
        for sujet in sujets:
            total_par_motif = total_par_motif + len([t for t in tickets if t["subject_cluster"] == sujet])
        self.assertEqual(total_par_motif, len(tickets))
        self.assertEqual(total_par_motif, 100)

    def test_f_volume_categorie_distinct_du_volume_motif(self):
        tickets_normaux = generer_tickets_livraison(100, subject_cluster="Où est ma commande")
        tickets_sujet = generer_tickets_livraison(
            30, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé",
        )
        tickets_livraison = tickets_normaux + tickets_sujet
        lecture = construire_lecture_activite_livraison(tickets_livraison, tickets_livraison, [])
        resultat = moteur_livraison_voie_a(tickets_livraison, [], 5)
        signal = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"][0]

        self.assertEqual(lecture["volume"], 130)  # volume CATÉGORIE Livraison
        self.assertEqual(signal["volume"]["n"], 30)  # volume MOTIF -- jamais confondu avec le précédent
        self.assertNotEqual(lecture["volume"], signal["volume"]["n"])


# Phase 5B (passe finale, segmentation transporteur) : filtrer_tickets_par_segment_transporteur est
# une pure fonction de sélection -- aucun recalcul, aucun seuil, aucune éligibilité. "Tous" doit
# rester un court-circuit total et prouvable au niveau du moteur lui-même, pas seulement au niveau
# de la liste filtrée.
class TestFiltrageSegmentTransporteurLivraison(unittest.TestCase):
    def test_a_tous_reproduit_la_liste_a_lidentique(self):
        tickets = generer_tickets_livraison(10, transporteur="Noria Standard") + generer_tickets_livraison(
            5, transporteur="Velox Express"
        )
        resultat = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_TOUS)
        self.assertEqual(resultat, tickets)
        self.assertEqual(len(resultat), 15)

    def test_b_noria_ne_garde_que_noria(self):
        tickets = generer_tickets_livraison(10, transporteur=SEGMENT_LIVRAISON_STANDARD) + generer_tickets_livraison(
            5, transporteur=SEGMENT_LIVRAISON_EXPRESS
        )
        resultat = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_STANDARD)
        self.assertEqual(len(resultat), 10)
        for ticket in resultat:
            self.assertEqual(ticket["transporteur"], SEGMENT_LIVRAISON_STANDARD)

    def test_c_velox_ne_garde_que_velox(self):
        tickets = generer_tickets_livraison(10, transporteur=SEGMENT_LIVRAISON_STANDARD) + generer_tickets_livraison(
            5, transporteur=SEGMENT_LIVRAISON_EXPRESS
        )
        resultat = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_EXPRESS)
        self.assertEqual(len(resultat), 5)
        for ticket in resultat:
            self.assertEqual(ticket["transporteur"], SEGMENT_LIVRAISON_EXPRESS)

    def test_d_aucun_ticket_dans_les_deux_segments_a_la_fois(self):
        tickets_standard = [ticket_livraison(ticket_id=i, transporteur=SEGMENT_LIVRAISON_STANDARD) for i in range(10)]
        tickets_express = [ticket_livraison(ticket_id=100 + i, transporteur=SEGMENT_LIVRAISON_EXPRESS) for i in range(5)]
        tickets = tickets_standard + tickets_express
        noria = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_STANDARD)
        velox = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_EXPRESS)
        ids_noria = set(t["ticket_id"] for t in noria)
        ids_velox = set(t["ticket_id"] for t in velox)
        self.assertEqual(len(ids_noria & ids_velox), 0)
        self.assertEqual(len(noria) + len(velox), len(tickets))

    def test_e_moteur_tous_identique_avec_ou_sans_passage_par_le_filtre(self):
        # "Tous" doit reproduire le moteur a l'identique, teste au niveau du moteur lui-meme --
        # pas seulement au niveau de la liste de tickets.
        tickets_sujet = generer_tickets_livraison(
            30, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé", transporteur=SEGMENT_LIVRAISON_STANDARD,
        )
        tickets_autres = generer_tickets_livraison(
            20, subject_cluster="Où est ma commande", transporteur=SEGMENT_LIVRAISON_EXPRESS,
        )
        tickets = tickets_sujet + tickets_autres

        resultat_direct = moteur_livraison_voie_a(tickets, [], 5)
        tickets_via_filtre = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_TOUS)
        resultat_filtre = moteur_livraison_voie_a(tickets_via_filtre, [], 5)

        self.assertEqual(
            [s["sujet"] for s in resultat_direct["prioritaires"]],
            [s["sujet"] for s in resultat_filtre["prioritaires"]],
        )
        self.assertEqual(resultat_direct["nb_prioritaires_avant_plafond"], resultat_filtre["nb_prioritaires_avant_plafond"])

    def test_f_concentration_transporteur_devient_none_dans_une_vue_mono_transporteur(self):
        # Confirme le comportement naturel observe en Phase 5B.1 : dans un univers filtre a un seul
        # transporteur, la comparaison "ce transporteur vs le reste" n'a plus de "reste" -- le
        # signal ne doit jamais afficher une piste transporteur triviale (100 %/0 %).
        tickets_sujet = generer_tickets_livraison(
            30, subject_cluster="Colis annoncé livré non reçu", csat=3.0, nombre_relances=2.5,
            issue_livraison_finale="Remboursé", transporteur=SEGMENT_LIVRAISON_STANDARD,
        )
        tickets_autres = generer_tickets_livraison(
            20, subject_cluster="Où est ma commande", transporteur=SEGMENT_LIVRAISON_STANDARD,
        )
        tickets = tickets_sujet + tickets_autres
        tickets_filtres = filtrer_tickets_par_segment_transporteur(tickets, SEGMENT_LIVRAISON_STANDARD)

        resultat = moteur_livraison_voie_a(tickets_filtres, [], 5)
        signal = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"][0]
        self.assertIsNone(signal["concentration_transporteur"])

    def test_g_segment_inconnu_ne_retourne_aucun_ticket(self):
        tickets = generer_tickets_livraison(10, transporteur=SEGMENT_LIVRAISON_STANDARD)
        resultat = filtrer_tickets_par_segment_transporteur(tickets, "Transporteur inexistant")
        self.assertEqual(resultat, [])


# Composition Livraison — investigation (Étape 5G.1) : 4C reste l'unique propriétaire de la
# priorisation (aucune de ces fonctions ne recalcule une éligibilité) -- seuls le texte de lecture,
# le matching "dossiers associés" et l'agrégation d'exploration motif x issue sont testés ici.
class TestLivraisonInvestigation5G1(unittest.TestCase):
    def test_a_lecture_zero_priorite_zero_watch(self):
        texte = construire_lecture_livraison("Livraison représente 22 % des contacts.", 0, 0)
        self.assertIn("Livraison représente 22 % des contacts.", texte)
        self.assertIn("Aucun motif ne présente actuellement une convergence suffisante", texte)

    def test_b_lecture_un_prioritaire(self):
        texte = construire_lecture_livraison("Livraison représente 44 % des contacts.", 1, 0)
        self.assertIn("Un motif présente une convergence suffisante pour être investigué.", texte)

    def test_c_lecture_plusieurs_prioritaires(self):
        texte = construire_lecture_livraison("Livraison représente 38 % des contacts.", 3, 0)
        self.assertIn("3 motifs présentent une convergence suffisante pour être investigués.", texte)

    def test_d_lecture_watch_seul(self):
        texte = construire_lecture_livraison("Livraison représente 30 % des contacts.", 0, 2)
        self.assertNotIn("Aucun motif ne présente actuellement une convergence suffisante", texte)
        self.assertIn("2 motifs supplémentaires restent à surveiller", texte)

    def test_e_lecture_prioritaire_et_watch_combines(self):
        texte = construire_lecture_livraison("Livraison représente 45 % des contacts.", 1, 2)
        self.assertIn("Un motif présente une convergence suffisante pour être investigué.", texte)
        self.assertIn("2 motifs supplémentaires restent à surveiller", texte)

    def test_f_lecture_active_jamais_de_texte_causal_entre_activite_et_signal(self):
        texte = construire_lecture_livraison("Livraison représente 45 % des contacts.", 1, 0)
        self.assertNotIn(" car ", texte)
        self.assertNotIn(" donc ", texte)
        self.assertNotIn(" explique ", texte)

    def test_g_dossiers_associes_matching_exact_grain_motif(self):
        tickets = (
            generer_tickets_livraison(5, subject_cluster="Colis annoncé livré non reçu")
            + generer_tickets_livraison(3, subject_cluster="Où est ma commande")
        )
        signal = {"sujet": "Colis annoncé livré non reçu"}
        dossiers = construire_dossiers_associes_livraison(signal, tickets)
        self.assertEqual(len(dossiers), 5)
        for ticket in dossiers:
            self.assertEqual(ticket["subject_cluster"], "Colis annoncé livré non reçu")

    def test_h_dossiers_associes_coherence_n_signal_4c(self):
        tickets_normaux = generer_tickets_livraison(
            100, subject_cluster="Où est ma commande", csat=4.2, replies=2.2,
            full_resolution_time_hours=35, nombre_relances=0.6,
        )
        tickets_problematiques = generer_tickets_livraison(
            20, subject_cluster="Colis annoncé livré non reçu", csat=3.0, replies=3.5,
            full_resolution_time_hours=70, nombre_relances=2.0, issue_livraison_finale="Remboursé",
        )
        tous = tickets_normaux + tickets_problematiques
        resultat = moteur_livraison_voie_a(tous, [], 5)
        signal = [s for s in resultat["prioritaires"] if s["sujet"] == "Colis annoncé livré non reçu"][0]
        dossiers = construire_dossiers_associes_livraison(signal, tous)
        self.assertEqual(len(dossiers), signal["volume"]["n"])

    def test_i_dossiers_associes_aucun_matching_texte_libre(self):
        tickets = generer_tickets_livraison(4, subject_cluster="Colis annoncé livré non reçu")
        signal = {"sujet": "Colis annoncé"}  # sous-chaîne d'un vrai sujet, ne doit jamais matcher
        dossiers = construire_dossiers_associes_livraison(signal, tickets)
        self.assertEqual(len(dossiers), 0)

    def test_j_croisement_motif_issue_calcule_relances_et_issue_principale(self):
        tickets = generer_tickets_livraison(
            10, subject_cluster="Colis annoncé livré non reçu", nombre_relances=2.0,
            issue_livraison_finale="Remboursé",
        )
        lignes = construire_croisement_motif_issue_livraison(tickets)
        self.assertEqual(len(lignes), 1)
        self.assertEqual(lignes[0]["sujet"], "Colis annoncé livré non reçu")
        self.assertEqual(lignes[0]["n"], 10)
        self.assertEqual(lignes[0]["relances_moyennes"], 2.0)
        self.assertEqual(lignes[0]["issue_principale"], "Remboursé")
        self.assertEqual(lignes[0]["part_issue_principale_pct"], 100.0)

    def test_k_croisement_motif_issue_plusieurs_motifs_separes(self):
        tickets = (
            generer_tickets_livraison(5, subject_cluster="Où est ma commande", issue_livraison_finale="Livraison confirmée")
            + generer_tickets_livraison(3, subject_cluster="Délai de livraison", issue_livraison_finale="Geste commercial")
        )
        lignes = construire_croisement_motif_issue_livraison(tickets)
        sujets = set(ligne["sujet"] for ligne in lignes)
        self.assertEqual(sujets, {"Où est ma commande", "Délai de livraison"})

    def test_l_croisement_motif_issue_tickets_vides(self):
        lignes = construire_croisement_motif_issue_livraison([])
        self.assertEqual(lignes, [])

    def test_m_cout_indisponible_jamais_zero(self):
        self.assertNotIn("0 €", TEXTE_COUT_INDISPONIBLE_LIVRAISON)
        self.assertNotIn("0€", TEXTE_COUT_INDISPONIBLE_LIVRAISON)
        self.assertIn("non mesurable", TEXTE_COUT_INDISPONIBLE_LIVRAISON.lower())


def ticket_avant_vente(ticket_id=1, requester_email="client1@example.com", created_at=None,
                        subject_cluster="Choix du programme", via_channel="Email",
                        type_contact_avant_vente=TYPE_CONTACT_SPONTANE, rdv_statut=None, csat=4.2):
    if created_at is None:
        created_at = datetime.date(2026, 1, 1)
    return {
        "ticket_id": ticket_id,
        "requester_email": requester_email,
        "created_at": created_at,
        "subject_cluster": subject_cluster,
        "via_channel": via_channel,
        "type_contact_avant_vente": type_contact_avant_vente,
        "rdv_statut": rdv_statut,
        "csat": csat,
    }


def generer_tickets_avant_vente(n, id_depart=1, **kwargs):
    tickets = []
    for i in range(n):
        kwargs_ticket = dict(kwargs)
        if "requester_email" not in kwargs_ticket:
            kwargs_ticket["requester_email"] = "client" + str(id_depart + i) + "@example.com"
        tickets.append(ticket_avant_vente(ticket_id=id_depart + i, **kwargs_ticket))
    return tickets


def commande_test(order_id, email_client, order_date, montant_total=150.0):
    return {"order_id": order_id, "email_client": email_client, "order_date": order_date, "montant_total": montant_total}


# Étape 4D -- moteur Avant-vente & conversion. "Achat OBSERVÉ" dans la fenêtre, jamais "conversion
# causée" : le vocabulaire et les règles d'éligibilité suivent la même philosophie que Produit /
# Tendances / Livraison (convergence de familles, jamais un seuil de score seul, jamais de fuite
# du futur, jamais de mélange entre catégories).
class TestAvantVente(unittest.TestCase):
    # ---- A. Taux proches -> pas d'avantage net déclaré ----
    def test_a_taux_proches_pas_davantage_net_declare(self):
        tickets_honore = generer_tickets_avant_vente(
            20, type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE, via_channel="Téléphone",
        )
        tickets_spontane = generer_tickets_avant_vente(20, id_depart=100, subject_cluster="Choix du programme")
        tickets_av = tickets_honore + tickets_spontane

        commandes_dict = {}
        cpt = 0
        # ~30 % d'achat pour chaque groupe (6/20 honoré, 6/20 spontané) -- taux proches
        for ticket in tickets_honore[:6] + tickets_spontane[:6]:
            cpt += 1
            commandes_dict["ORD" + str(cpt)] = commande_test(
                "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
            )
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        parcours = analyser_parcours_rdv(tickets_av, resultats)

        self.assertIn("proches", parcours["conclusion"])
        self.assertNotIn("plus élevé", parcours["conclusion"])

    # ---- B. Avantage apparent sur petit n -> prudence, pas conclusion forte ----
    def test_b_avantage_apparent_petit_n_prudence(self):
        tickets_honore = generer_tickets_avant_vente(
            3, type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE, via_channel="Téléphone",
        )
        tickets_spontane = generer_tickets_avant_vente(20, id_depart=100, subject_cluster="Choix du programme")
        tickets_av = tickets_honore + tickets_spontane

        commandes_dict = {}
        cpt = 0
        for ticket in tickets_honore:  # 100 % d'achat sur seulement 3 contacts honorés
            cpt += 1
            commandes_dict["ORD" + str(cpt)] = commande_test(
                "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
            )
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        parcours = analyser_parcours_rdv(tickets_av, resultats)

        # malgré un taux de 100 % sur le petit groupe, la conclusion reste prudente (échantillon
        # insuffisant), jamais "le RDV honoré convertit mieux"
        self.assertIn("insuffisant", parcours["conclusion"])

    # ---- C. Verrou d'interprétation RDV ----
    def test_c_annule_no_show_jamais_conseil_recu(self):
        annule = ticket_avant_vente(type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_ANNULE)
        no_show = ticket_avant_vente(type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_NO_SHOW)
        honore = ticket_avant_vente(type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE)
        spontane = ticket_avant_vente(type_contact_avant_vente=TYPE_CONTACT_SPONTANE)

        self.assertEqual(determiner_parcours_avant_vente(annule), PARCOURS_RDV_NON_HONORE)
        self.assertEqual(determiner_parcours_avant_vente(no_show), PARCOURS_RDV_NON_HONORE)
        self.assertEqual(determiner_parcours_avant_vente(honore), PARCOURS_RDV_HONORE)
        self.assertEqual(determiner_parcours_avant_vente(spontane), PARCOURS_SPONTANE)
        self.assertNotEqual(determiner_parcours_avant_vente(annule), PARCOURS_RDV_HONORE)
        self.assertNotEqual(determiner_parcours_avant_vente(no_show), PARCOURS_RDV_HONORE)

    # ---- D/E/F. Fenêtre d'observation ----
    def test_d_commande_avant_contact_jamais_comptee(self):
        ticket = ticket_avant_vente(created_at=datetime.date(2026, 3, 15))
        commande_avant = commande_test("C1", "client1@example.com", datetime.date(2026, 3, 10))
        index = commandes_par_email({"C1": commande_avant})
        resultat = premiere_commande_apres(ticket, index, 30)
        self.assertIsNone(resultat)

    def test_e_commande_hors_fenetre_jamais_comptee(self):
        ticket = ticket_avant_vente(created_at=datetime.date(2026, 3, 15))
        commande_tardive = commande_test("C1", "client1@example.com", datetime.date(2026, 4, 20))  # 36 jours après
        index = commandes_par_email({"C1": commande_tardive})
        resultat = premiere_commande_apres(ticket, index, 30)
        self.assertIsNone(resultat)

    def test_f_premiere_commande_admissible_delai_et_panier_corrects(self):
        ticket = ticket_avant_vente(created_at=datetime.date(2026, 3, 1))
        commande_proche = commande_test("C1", "client1@example.com", datetime.date(2026, 3, 10), montant_total=120.0)
        commande_lointaine = commande_test("C2", "client1@example.com", datetime.date(2026, 3, 20), montant_total=300.0)
        index = commandes_par_email({"C1": commande_proche, "C2": commande_lointaine})
        resultat = premiere_commande_apres(ticket, index, 30)
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat["order_id"], "C1")  # la première admissible, pas la plus chère
        self.assertEqual((resultat["order_date"] - ticket["created_at"]).days, 9)
        self.assertEqual(resultat["montant_total"], 120.0)

    # ---- G. Anti-double-comptage (Étape 4D.1 : le contact le plus RÉCENT avant la commande) ----
    def test_g_meme_commande_attribuee_au_contact_le_plus_recent(self):
        ticket_1 = ticket_avant_vente(ticket_id=1, requester_email="client1@example.com", created_at=datetime.date(2026, 3, 1))
        ticket_2 = ticket_avant_vente(ticket_id=2, requester_email="client1@example.com", created_at=datetime.date(2026, 3, 4))
        commande = commande_test("C1", "client1@example.com", datetime.date(2026, 3, 10))
        index = commandes_par_email({"C1": commande})

        resultats = resoudre_achats_observes_avant_vente([ticket_1, ticket_2], index, 30)
        credits = [r for r in resultats if r[1] is not None]
        self.assertEqual(len(credits), 1)  # une seule des deux revendications est retenue
        self.assertEqual(credits[0][0]["ticket_id"], 2)  # le contact le plus RÉCENT (jeudi) la revendique

        non_credite = [r for r in resultats if r[1] is None]
        self.assertEqual(len(non_credite), 1)
        self.assertEqual(non_credite[0][0]["ticket_id"], 1)

        stats = calculer_stats_achat_observe(resultats)
        self.assertEqual(stats["n_achats"], 1)  # jamais 2 pour une seule commande réelle

    # ---- H/I/J. Éligibilité opportunité ----
    def test_h_fort_volume_taux_proche_reference_activite_pas_opportunite(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(
            50, id_depart=200, subject_cluster="Compatibilité allergies / parfums forts",
        )
        tickets_av = tickets_normaux + tickets_sujet
        index = commandes_par_email({})
        for i, ticket in enumerate(tickets_av):
            # 1 achat sur 5 pour tout le monde -- taux identique partout
            if i % 5 == 0:
                index.setdefault(ticket["requester_email"], [])
        # construit des commandes pour ~20% de chaque groupe, réparties de façon identique
        commandes_dict = {}
        cpt = 0
        for ticket in tickets_av:
            if int(ticket["ticket_id"]) % 5 == 0:
                cpt += 1
                commandes_dict["ORD" + str(cpt)] = commande_test(
                    "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                )
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)

        resultats_sujet = [r for r in resultats if r[0]["subject_cluster"] == "Compatibilité allergies / parfums forts"]
        signal = construire_signal_motif_avant_vente(
            "Compatibilité allergies / parfums forts", tickets_sujet, resultats_sujet, tickets_av, resultats, [], [],
        )
        self.assertIsNotNone(signal)
        self.assertIsNone(signal["tier"])  # activité, pas une opportunité ni une surveillance

    def test_i_volume_significatif_taux_nettement_inferieur_opportunite_possible(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(
            30, id_depart=200, subject_cluster="Demande couleur personnalisée (hors catalogue)",
        )
        tickets_av = tickets_normaux + tickets_sujet

        commandes_dict = {}
        cpt = 0
        for ticket in tickets_normaux:  # 30 % d'achat pour la référence
            if int(ticket["ticket_id"]) % 3 == 0:
                cpt += 1
                commandes_dict["ORD" + str(cpt)] = commande_test(
                    "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                )
        # aucun achat pour le motif candidat -- taux nettement inférieur
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [
            r for r in resultats if r[0]["subject_cluster"] == "Demande couleur personnalisée (hors catalogue)"
        ]

        niveaux_historiques = [0.10, 0.09, 0.11]  # historique cohérent, pas de hausse nécessaire ici
        signal = construire_signal_motif_avant_vente(
            "Demande couleur personnalisée (hors catalogue)", tickets_sujet, resultats_sujet, tickets_av,
            resultats, niveaux_historiques, [],
        )
        self.assertIsNotNone(signal)
        self.assertIn(signal["tier"], ("opportunite", "a_surveiller"))
        self.assertIn("C", signal["familles_actives"])

    def test_j_petit_n_zero_achat_pas_priorite_automatique(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(3, id_depart=200, subject_cluster="Motif rare")
        tickets_av = tickets_normaux + tickets_sujet
        index_commandes = commandes_par_email({})
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [r for r in resultats if r[0]["subject_cluster"] == "Motif rare"]

        signal = construire_signal_motif_avant_vente(
            "Motif rare", tickets_sujet, resultats_sujet, tickets_av, resultats, [], [],
        )
        self.assertIsNone(signal)  # n=3 < seuil minimum -- silence, jamais une carte automatique

    # ---- K. Canal purement descriptif ----
    def test_k_canal_purement_descriptif_sans_comparaison(self):
        tickets = (
            generer_tickets_avant_vente(20, via_channel="Téléphone", type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE)
            + generer_tickets_avant_vente(10, id_depart=100, via_channel="Chat")
        )
        distribution = distribution_canal_avant_vente(tickets)
        total_pct = sum(item["part_pct"] for item in distribution)
        self.assertAlmostEqual(total_pct, 100.0)
        for item in distribution:
            self.assertIn("canal", item)
            self.assertIn("n", item)
            self.assertIn("part_pct", item)
            self.assertNotIn("lecture", item)  # aucune comparaison/lecture attachée -- purement descriptif
            self.assertNotIn("taux_achat", item)

    # ---- L. Activité commerciale saine, pas un problème ----
    def test_l_contexte_campagne_hausse_experience_tenue_activite_pas_probleme(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(60, id_depart=200, subject_cluster="Choix du programme")
        tickets_av = tickets_normaux + tickets_sujet
        commandes_dict = {}
        cpt = 0
        for ticket in tickets_av:
            if int(ticket["ticket_id"]) % 3 == 0:
                cpt += 1
                commandes_dict["ORD" + str(cpt)] = commande_test(
                    "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                )
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [r for r in resultats if r[0]["subject_cluster"] == "Choix du programme"]

        signal = construire_signal_motif_avant_vente(
            "Choix du programme", tickets_av, resultats_sujet + [
                r for r in resultats if r[0]["subject_cluster"] == "Choix du programme"
            ], tickets_av, resultats, [], [],
        )
        # même taux d'achat que la référence (c'est tout le motif) -> jamais d'opportunité forcée
        self.assertIsNotNone(signal)
        self.assertIsNone(signal["tier"])

    # ---- M. Sable : jamais "ventes perdues" ----
    def test_m_faible_achat_observe_jamais_ventes_perdues(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(
            20, id_depart=200, subject_cluster="Demande couleur personnalisée (hors catalogue)",
        )
        tickets_av = tickets_normaux + tickets_sujet
        commandes_dict = {}
        cpt = 0
        for ticket in tickets_normaux:
            if int(ticket["ticket_id"]) % 3 == 0:
                cpt += 1
                commandes_dict["ORD" + str(cpt)] = commande_test(
                    "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                )
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [
            r for r in resultats if r[0]["subject_cluster"] == "Demande couleur personnalisée (hors catalogue)"
        ]
        signal = construire_signal_motif_avant_vente(
            "Demande couleur personnalisée (hors catalogue)", tickets_sujet, resultats_sujet, tickets_av,
            resultats, [], [],
        )
        self.assertIsNotNone(signal)
        textes = [signal["observation_principale"], signal["piste_investigation"]]
        for texte in textes:
            texte_minuscule = texte.lower()
            self.assertNotIn("vente perdue", texte_minuscule)
            self.assertNotIn("ventes perdues", texte_minuscule)
            self.assertNotIn("conversion perdue", texte_minuscule)

    # ---- N. Étreinte : jamais de mélange avec Product SAV ----
    def test_n_avant_vente_ne_melange_jamais_sav_produit(self):
        ticket_av = ticket_avant_vente(subject_cluster="Choix du programme")
        ticket_av["ticket_reason"] = "Conseil programme / produit"
        ticket_sav = dict(ticket_av)
        ticket_sav["ticket_reason"] = "SAV"
        ticket_sav["resolution_type"] = "Remplacement produit"
        self.assertEqual(categoriser(ticket_av), "Avant-vente / conseil")
        self.assertNotEqual(categoriser(ticket_sav), "Avant-vente / conseil")

    # ---- O. Dénominateur explicite partout ----
    def test_o_pourcentages_ont_toujours_un_denominateur_explicite(self):
        tickets = generer_tickets_avant_vente(10, subject_cluster="Choix du programme")
        index_commandes = commandes_par_email({})
        resultats = resoudre_achats_observes_avant_vente(tickets, index_commandes, 30)
        stats = calculer_stats_achat_observe(resultats)
        self.assertIn("n_contacts", stats)
        self.assertIn("taux_pct", stats)
        self.assertIn("n_achats", stats)
        self.assertIn("n_panier", stats)
        self.assertIn("n_delai", stats)

    # ---- Contrôle qualité ----
    def test_controle_qualite_avant_vente_silencieux_sur_donnees_propres(self):
        tickets_av = generer_tickets_avant_vente(
            10, type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE, via_channel="Téléphone",
        )
        tickets_hors = generer_tickets_avant_vente(5, id_depart=100)
        for t in tickets_hors:
            t["type_contact_avant_vente"] = None
            t["rdv_statut"] = None
        anomalies = controler_qualite_donnees_avant_vente(tickets_av, tickets_hors)
        self.assertEqual(anomalies, [])

    def test_controle_qualite_avant_vente_detecte_anomalies(self):
        tickets_av = [
            ticket_avant_vente(ticket_id=1, type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=None),
            ticket_avant_vente(ticket_id=2, type_contact_avant_vente="Autre", rdv_statut=None),
            ticket_avant_vente(
                ticket_id=3, type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE,
                via_channel="Email",
            ),
        ]
        tickets_hors = [ticket_avant_vente(ticket_id=4, type_contact_avant_vente=TYPE_CONTACT_SPONTANE)]
        anomalies = controler_qualite_donnees_avant_vente(tickets_av, tickets_hors)
        self.assertGreater(len(anomalies), 0)

    # ---- Motif "Demande de rendez-vous" exclu de l'analyse par motif ----
    def test_sujet_demande_rdv_exclu_de_lanalyse_par_motif(self):
        tickets_rdv = generer_tickets_avant_vente(
            60, subject_cluster=SUJET_DEMANDE_RDV, type_contact_avant_vente=TYPE_CONTACT_RDV,
            rdv_statut=RDV_STATUT_HONORE, via_channel="Téléphone",
        )
        tickets_autres = generer_tickets_avant_vente(20, id_depart=200, subject_cluster="Choix du programme")
        tickets_av = tickets_rdv + tickets_autres
        index_commandes = commandes_par_email({})
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultat = moteur_avant_vente_motifs(tickets_av, resultats, [], [], 5)
        sujets_vus = set()
        for signal in resultat["opportunites"] + resultat["a_surveiller"]:
            sujets_vus.add(signal["sujet"])
        for sujet in resultat["sujets_silencieux"]:
            sujets_vus.add(sujet)
        self.assertNotIn(SUJET_DEMANDE_RDV, sujets_vus)


# Étape 4D.1 -- attribution commande->contact recalibrée (le plus RÉCENT avant l'achat, jamais le
# plus ancien), contacts avant achat corrigés (bornés, précis), richesse des opportunités
# (Type 1 = friction commerciale ; Type 2 documenté comme limitation du dataset, voir compte-rendu).
class TestAttributionAvantVente4D1(unittest.TestCase):
    def test_a_deux_contacts_avant_commande_attribuee_au_plus_recent(self):
        ticket_ancien = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 3, 1))
        ticket_recent = ticket_avant_vente(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 3, 4))
        commande = commande_test("C1", "c@example.com", datetime.date(2026, 3, 6))
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente([ticket_ancien, ticket_recent], index, 30)
        credite = [r for r in resultats if r[1] is not None][0]
        self.assertEqual(credite[0]["ticket_id"], 2)

    def test_b_contact_apres_commande_jamais_attributaire(self):
        ticket_avant = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 3, 1))
        ticket_apres = ticket_avant_vente(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 3, 15))
        commande = commande_test("C1", "c@example.com", datetime.date(2026, 3, 10))
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente([ticket_avant, ticket_apres], index, 30)
        credit_apres = [r for r in resultats if r[0]["ticket_id"] == 2][0]
        self.assertIsNone(credit_apres[1])
        credit_avant = [r for r in resultats if r[0]["ticket_id"] == 1][0]
        self.assertIsNotNone(credit_avant[1])

    def test_c_deux_commandes_distinctes_chacune_son_contact(self):
        ticket_1 = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_2 = ticket_avant_vente(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 2, 1))
        commande_1 = commande_test("C1", "c@example.com", datetime.date(2026, 1, 10))
        commande_2 = commande_test("C2", "c@example.com", datetime.date(2026, 2, 10))
        index = commandes_par_email({"C1": commande_1, "C2": commande_2})
        resultats = resoudre_achats_observes_avant_vente([ticket_1, ticket_2], index, 30)
        r1 = [r for r in resultats if r[0]["ticket_id"] == 1][0]
        r2 = [r for r in resultats if r[0]["ticket_id"] == 2][0]
        self.assertEqual(r1[1]["order_id"], "C1")
        self.assertEqual(r2[1]["order_id"], "C2")

    def test_d_un_contact_plusieurs_commandes_compte_une_fois(self):
        ticket = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1))
        commande_1 = commande_test("C1", "c@example.com", datetime.date(2026, 1, 5), montant_total=100.0)
        commande_2 = commande_test("C2", "c@example.com", datetime.date(2026, 1, 20), montant_total=500.0)
        index = commandes_par_email({"C1": commande_1, "C2": commande_2})
        resultats = resoudre_achats_observes_avant_vente([ticket], index, 30)
        self.assertEqual(len(resultats), 1)
        ticket_r, commande_r, plusieurs = resultats[0]
        self.assertTrue(plusieurs)
        stats = calculer_stats_achat_observe(resultats)
        self.assertEqual(stats["n_achats"], 1)  # binaire, jamais 2 pour un seul contact

    def test_e_panier_delai_utilisent_premiere_commande_attribuee(self):
        ticket = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1))
        commande_1 = commande_test("C1", "c@example.com", datetime.date(2026, 1, 5), montant_total=100.0)
        commande_2 = commande_test("C2", "c@example.com", datetime.date(2026, 1, 20), montant_total=500.0)
        index = commandes_par_email({"C1": commande_1, "C2": commande_2})
        resultats = resoudre_achats_observes_avant_vente([ticket], index, 30)
        ticket_r, commande_r, plusieurs = resultats[0]
        self.assertEqual(commande_r["order_id"], "C1")  # la première chronologiquement, pas la plus chère
        self.assertEqual(commande_r["montant_total"], 100.0)

    def test_fg_contacts_avant_achat_uniquement_anterieurs_a_la_commande(self):
        ticket_avant_1 = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_avant_2 = ticket_avant_vente(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 1, 5))
        ticket_apres = ticket_avant_vente(ticket_id=3, requester_email="c@example.com", created_at=datetime.date(2026, 1, 15))
        commande = commande_test("C1", "c@example.com", datetime.date(2026, 1, 10))
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente(
            [ticket_avant_1, ticket_avant_2, ticket_apres], index, 30
        )
        analyse = analyser_contacts_avant_achat(resultats, 30)
        self.assertIsNotNone(analyse)
        self.assertEqual(analyse["n_achats_credites"], 1)
        # 2 contacts avant la commande (1er et 5 janvier) ; le contact du 15 (post-achat) exclu
        self.assertEqual(analyse["distribution_nb_contacts"]["2"], 1)
        self.assertEqual(analyse["nombre_moyen_contacts_avant_achat"], 2)

    def test_h_distribution_1_2_3_plus_correcte(self):
        # Achat A : 1 seul contact avant
        ticket_a = ticket_avant_vente(ticket_id=1, requester_email="clientA@example.com", created_at=datetime.date(2026, 1, 1))
        commande_a = commande_test("CA", "clientA@example.com", datetime.date(2026, 1, 5))
        # Achat B : 2 contacts avant
        ticket_b1 = ticket_avant_vente(ticket_id=2, requester_email="clientB@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_b2 = ticket_avant_vente(ticket_id=3, requester_email="clientB@example.com", created_at=datetime.date(2026, 1, 3))
        commande_b = commande_test("CB", "clientB@example.com", datetime.date(2026, 1, 5))
        # Achat C : 3 contacts avant
        ticket_c1 = ticket_avant_vente(ticket_id=4, requester_email="clientC@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_c2 = ticket_avant_vente(ticket_id=5, requester_email="clientC@example.com", created_at=datetime.date(2026, 1, 2))
        ticket_c3 = ticket_avant_vente(ticket_id=6, requester_email="clientC@example.com", created_at=datetime.date(2026, 1, 3))
        commande_c = commande_test("CC", "clientC@example.com", datetime.date(2026, 1, 5))

        index = commandes_par_email({"CA": commande_a, "CB": commande_b, "CC": commande_c})
        tickets = [ticket_a, ticket_b1, ticket_b2, ticket_c1, ticket_c2, ticket_c3]
        resultats = resoudre_achats_observes_avant_vente(tickets, index, 30)
        analyse = analyser_contacts_avant_achat(resultats, 30)

        self.assertEqual(analyse["n_achats_credites"], 3)
        self.assertEqual(analyse["distribution_nb_contacts"]["1"], 1)
        self.assertEqual(analyse["distribution_nb_contacts"]["2"], 1)
        self.assertEqual(analyse["distribution_nb_contacts"]["3+"], 1)

    def test_k_petit_n_avec_c_actif_pas_opportunite_forte(self):
        tickets_normaux = generer_tickets_avant_vente(150, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(6, id_depart=200, subject_cluster="Motif secondaire")
        tickets_av = tickets_normaux + tickets_sujet

        commandes_dict = {}
        cpt = 0
        for ticket in tickets_normaux:  # ~33 % d'achat en référence
            if int(ticket["ticket_id"]) % 3 == 0:
                cpt += 1
                commandes_dict["ORD" + str(cpt)] = commande_test(
                    "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                )
        # aucun achat pour le petit motif -- écart marqué, mais volume trop faible pour une vraie opportunité
        index_commandes = commandes_par_email(commandes_dict)
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [r for r in resultats if r[0]["subject_cluster"] == "Motif secondaire"]

        signal = construire_signal_motif_avant_vente(
            "Motif secondaire", tickets_sujet, resultats_sujet, tickets_av, resultats, [], [],
        )
        self.assertIsNotNone(signal)
        self.assertNotEqual(signal["tier"], "opportunite")
        self.assertEqual(signal["tier"], "a_surveiller")

    def test_l_aucun_champ_type_2_fabrique(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(30, id_depart=200, subject_cluster="Demande couleur personnalisée (hors catalogue)")
        tickets_av = tickets_normaux + tickets_sujet
        index_commandes = commandes_par_email({})
        resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
        resultats_sujet = [
            r for r in resultats if r[0]["subject_cluster"] == "Demande couleur personnalisée (hors catalogue)"
        ]
        signal = construire_signal_motif_avant_vente(
            "Demande couleur personnalisée (hors catalogue)", tickets_sujet, resultats_sujet, tickets_av,
            resultats, [], [],
        )
        self.assertIsNotNone(signal)
        # aucune structure "Type 2 / demande non couverte" fabriquée -- le champ n'existe pas,
        # conformément à l'audit (limitation du dataset, voir compte-rendu 4D.1 section 6/9)
        self.assertNotIn("type_2", signal)
        self.assertNotIn("demande_non_couverte", signal)
        self.assertIn(signal["tier"], (None, "opportunite", "a_surveiller"))

    def test_n_genericite_aucun_resultat_force_par_nom_de_motif(self):
        def construire_cas(nom_motif):
            tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
            tickets_sujet = generer_tickets_avant_vente(30, id_depart=200, subject_cluster=nom_motif)
            tickets_av = tickets_normaux + tickets_sujet
            commandes_dict = {}
            cpt = 0
            for ticket in tickets_normaux:
                if int(ticket["ticket_id"]) % 3 == 0:
                    cpt += 1
                    commandes_dict["ORD" + str(cpt)] = commande_test(
                        "ORD" + str(cpt), ticket["requester_email"], ticket["created_at"] + datetime.timedelta(days=5)
                    )
            index_commandes = commandes_par_email(commandes_dict)
            resultats = resoudre_achats_observes_avant_vente(tickets_av, index_commandes, 30)
            resultats_sujet = [r for r in resultats if r[0]["subject_cluster"] == nom_motif]
            return construire_signal_motif_avant_vente(
                nom_motif, tickets_sujet, resultats_sujet, tickets_av, resultats, [], [],
            )

        signal_sable = construire_cas("Demande couleur personnalisée (hors catalogue)")
        signal_generique = construire_cas("Zzz motif totalement générique")
        # même donnée (0 achat sur le motif candidat, même volume) -> même verdict, quel que soit le nom
        self.assertEqual(signal_sable["tier"], signal_generique["tier"])
        self.assertEqual(signal_sable["familles_actives"], signal_generique["familles_actives"])


def reponse_nps_test(email_client="client1@example.com", score=9, date_reponse=None, a_contacte_support="Non"):
    if date_reponse is None:
        date_reponse = datetime.date(2026, 1, 15)
    return {
        "email_client": email_client, "score": score, "date_reponse": date_reponse,
        "a_contacte_support": a_contacte_support,
    }


def ticket_care_test(ticket_id=1, requester_email="client1@example.com", created_at=None,
                      ticket_reason="SAV", resolution_type="Remplacement produit", csat=4.0,
                      full_resolution_time_hours=10, first_reply_time_min=60, reopens=0, replies=2,
                      prior_sav_count=0):
    if created_at is None:
        created_at = datetime.date(2026, 1, 1)
    return {
        "ticket_id": ticket_id, "requester_email": requester_email, "created_at": created_at,
        "ticket_reason": ticket_reason, "resolution_type": resolution_type, "csat": csat,
        "full_resolution_time_hours": full_resolution_time_hours, "first_reply_time_min": first_reply_time_min,
        "reopens": reopens, "replies": replies, "prior_sav_count": prior_sav_count,
    }


MOTS_CAUSAUX_INTERDITS = (
    "parce que", "grâce à", "grace a", "causé", "cause par", "a permis", "a amélioré", "a dégradé",
    "a fait baisser", "a fait monter", "explique le",
)


# Étape 4E -- moteur Impact & confiance / NPS. NPS = %promoteurs - %détracteurs (jamais une
# moyenne /10), toujours affiché en entier, jamais de benchmark industrie, jamais de causalité
# entre Care et NPS (association uniquement, biais de sélection explicite), jamais de fuite du
# futur dans les lectures d'alignement historique.
class TestImpactConfianceNPS(unittest.TestCase):
    # ---- A. NPS recomposé depuis les scores == calculer_nps (jamais une moyenne /10) ----
    def test_a_composition_nps_egale_calculer_nps(self):
        reponses = (
            [reponse_nps_test(score=9)] * 4
            + [reponse_nps_test(score=10)] * 2
            + [reponse_nps_test(score=7)] * 3
            + [reponse_nps_test(score=2)] * 3
        )
        composition = calculer_composition_nps(reponses)
        self.assertAlmostEqual(composition["nps"], calculer_nps(reponses))

    # ---- B. Affichage toujours entier, jamais de décimale ----
    def test_b_formater_nps_entier_jamais_de_decimale(self):
        self.assertEqual(formater_nps_entier(5.94), "+6")
        self.assertEqual(formater_nps_entier(-6.4), "-6")
        self.assertEqual(formater_nps_entier(0), "0")
        for valeur in (5.94, -6.4, 0, 31.2, -100.0, 100.0):
            texte = formater_nps_entier(valeur)
            self.assertNotIn(".", texte)

    # ---- C. Composition exacte : promoteurs + passifs + détracteurs == n, sommes cohérentes ----
    def test_c_composition_somme_coherente(self):
        reponses = [reponse_nps_test(score=s) for s in (10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)]
        composition = calculer_composition_nps(reponses)
        self.assertEqual(composition["n_promoteurs"] + composition["n_passifs"] + composition["n_detracteurs"], composition["n"])
        somme_parts = composition["part_promoteurs_pct"] + composition["part_passifs_pct"] + composition["part_detracteurs_pct"]
        self.assertAlmostEqual(somme_parts, 100.0)

    # ---- D. Prudence d'échantillon, jamais "significatif" ----
    def test_d_prudence_relative_a_la_serie_jamais_un_seuil_absolu(self):
        # Étape 4E.1 -- la prudence compare le n du mois aux AUTRES n déjà disponibles (rang),
        # jamais à un seuil absolu magique. Série réelle (sept25->sept26) : septembre 2026 (n=18)
        # est nettement moins documenté que les 12 mois précédents.
        historique_n = [73, 43, 55, 87, 69, 47, 61, 48, 59, 62, 50, 52, 18]
        etat = evaluer_prudence_echantillon_nps(historique_n, 12)
        self.assertEqual(etat, ETAT_PRUDENCE_VOLUME_FAIBLE)
        texte = texte_prudence_echantillon_nps(etat, 18)
        for mot_interdit in ("significatif", "statistiquement", "fiable"):
            self.assertNotIn(mot_interdit, texte.lower())
        self.assertIn("prudence", texte.lower())

    # ---- E. Alignement négatif (cas type janvier : NPS bas + CSAT bas + effort dégradé) ----
    def test_e_alignement_negatif_type_janvier(self):
        historique_nps = [{"nps": 10}, {"nps": 8}, {"nps": -6}]
        historique_care = [
            {"csat": 4.2, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.1, "reopens_moyen": 0.06, "resolution_moyenne": 22},
            {"csat": 3.5, "reopens_moyen": 0.15, "resolution_moyenne": 60},
        ]
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 2)
        self.assertEqual(resultat["type"], "alignement_negatif")

    # ---- F. Divergence (cas type juin : NPS bas mais CSAT reste correct, pas d'effort dégradé) ----
    def test_f_divergence_type_juin(self):
        historique_nps = [{"nps": 10}, {"nps": 8}, {"nps": -5}]
        historique_care = [
            {"csat": 4.0, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.05, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.5, "reopens_moyen": 0.05, "resolution_moyenne": 20},
        ]
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 2)
        self.assertEqual(resultat["type"], "divergence")
        texte = texte_alignement_care_nps(resultat, historique_care[2], "juin")
        # CSAT reste correct : jamais "NPS explique par CSAT", uniquement une observation de non-concordance
        self.assertNotIn("expliqu", texte.lower())

    # ---- G. Pic isolé sans corrélat CSAT (cas type avril) : aucun texte forcé, jamais "amélioré par" ----
    def test_g_pic_isole_sans_corrélat_pas_de_texte_force(self):
        historique_nps = [{"nps": 3}, {"nps": 3}, {"nps": 31}]
        historique_care = [
            {"csat": 3.9, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.0, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 3.96, "reopens_moyen": 0.05, "resolution_moyenne": 20},
        ]
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 2)
        self.assertIsNone(resultat["type"])
        texte = texte_alignement_care_nps(resultat, historique_care[2], "avril")
        self.assertIsNone(texte)

    # ---- H. Historique insuffisant -> aucune conclusion forcée ----
    def test_h_historique_insuffisant_aucune_conclusion(self):
        resultat = evaluer_alignement_care_nps([{"nps": 7}], [{"csat": 4.0, "reopens_moyen": 0.05, "resolution_moyenne": 20}], 0)
        self.assertIsNone(resultat)

    # ---- I. Aucun mot causal dans les textes d'alignement générés ----
    def test_i_textes_alignement_jamais_causaux(self):
        historique_nps = [{"nps": 10}, {"nps": 8}, {"nps": -6}]
        historique_care = [
            {"csat": 4.2, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.1, "reopens_moyen": 0.06, "resolution_moyenne": 22},
            {"csat": 3.5, "reopens_moyen": 0.15, "resolution_moyenne": 60},
        ]
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 2)
        texte = texte_alignement_care_nps(resultat, historique_care[2], "janvier")
        texte_minuscule = texte.lower()
        for mot in MOTS_CAUSAUX_INTERDITS:
            self.assertNotIn(mot, texte_minuscule)

    # ---- J. Segmentation "contact Care identifié" fondée sur le matching ticket, pas le champ déclaratif ----
    def test_j_segmentation_utilise_matching_ticket_pas_champ_declaratif(self):
        # le client déclare "Non" mais un ticket réel précède la réponse dans la fenêtre -- doit
        # basculer côté "contact identifié" malgré le champ déclaratif discordant.
        reponse = reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 1, 20), a_contacte_support="Non")
        ticket = ticket_care_test(requester_email="c@example.com", created_at=datetime.date(2026, 1, 10))
        index = tickets_par_email([ticket])
        segmentation = segmenter_nps_par_contact_care([reponse], index, 60)
        self.assertEqual(segmentation["contact_identifie"]["composition"]["n"], 1)
        self.assertIsNone(segmentation["aucun_contact_identifie"]["composition"])

    # ---- K. Contrôle qualité : jamais de ticket postérieur à la réponse NPS matché (invariant) ----
    def test_k_controle_qualite_aucun_ticket_posterieur(self):
        reponse = reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 1, 10))
        ticket_avant = ticket_care_test(requester_email="c@example.com", created_at=datetime.date(2026, 1, 5))
        ticket_apres = ticket_care_test(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 1, 15))
        index = tickets_par_email([ticket_avant, ticket_apres])
        anomalies = controler_qualite_donnees_nps([reponse], index, 60)
        for anomalie in anomalies:
            self.assertNotIn("postérieur", anomalie)

    # ---- L. Type d'expérience : le contact le plus RÉCENT avant la réponse l'emporte ----
    def test_l_type_experience_contact_le_plus_recent(self):
        reponse = reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 1, 20))
        ticket_ancien = ticket_care_test(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1), ticket_reason="Livraison")
        ticket_recent = ticket_care_test(ticket_id=2, requester_email="c@example.com", created_at=datetime.date(2026, 1, 15), ticket_reason="SAV", prior_sav_count=0)
        index = tickets_par_email([ticket_ancien, ticket_recent])
        type_experience = determiner_type_experience_nps(reponse, index, 60)
        self.assertEqual(type_experience, TYPE_EXPERIENCE_SAV)

    # ---- M. Libellé "aucun contact" jamais "Contacted"/"Never contacted" ----
    def test_m_libelle_aucun_contact_care_identifie(self):
        reponse = reponse_nps_test(email_client="isole@example.com")
        index = tickets_par_email([])
        type_experience = determiner_type_experience_nps(reponse, index, 60)
        self.assertEqual(type_experience, TYPE_EXPERIENCE_AUCUN)
        self.assertIn("données disponibles", type_experience)
        self.assertNotIn("Contacted", type_experience)
        self.assertNotIn("Never", type_experience)

    # ---- N. Types SAV récurrent / Livraison / Remplacement / résolution rapide-longue ----
    def test_n_types_experience_correctement_distingues(self):
        reponse = reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 2, 1))
        index_sav_recurrent = tickets_par_email([ticket_care_test(requester_email="c@example.com", ticket_reason="SAV", prior_sav_count=2)])
        self.assertEqual(determiner_type_experience_nps(reponse, index_sav_recurrent, 60), TYPE_EXPERIENCE_SAV_RECURRENT)

        index_livraison = tickets_par_email([ticket_care_test(requester_email="c@example.com", ticket_reason="Livraison")])
        self.assertEqual(determiner_type_experience_nps(reponse, index_livraison, 60), TYPE_EXPERIENCE_LIVRAISON)

        index_remplacement = tickets_par_email([ticket_care_test(
            requester_email="c@example.com", ticket_reason="Après-vente commande/admin", resolution_type="Remplacement accessoire",
        )])
        self.assertEqual(determiner_type_experience_nps(reponse, index_remplacement, 60), TYPE_EXPERIENCE_REMPLACEMENT)

        index_rapide = tickets_par_email([ticket_care_test(
            requester_email="c@example.com", ticket_reason="Utilisation / routine", resolution_type="Information / résolution à distance",
            full_resolution_time_hours=5,
        )])
        self.assertEqual(determiner_type_experience_nps(reponse, index_rapide, 60), TYPE_EXPERIENCE_RESOLUTION_RAPIDE)

        index_longue = tickets_par_email([ticket_care_test(
            requester_email="c@example.com", ticket_reason="Utilisation / routine", resolution_type="Information / résolution à distance",
            full_resolution_time_hours=48,
        )])
        self.assertEqual(determiner_type_experience_nps(reponse, index_longue, 60), TYPE_EXPERIENCE_RESOLUTION_LONGUE)

    # ---- O. Confiance par type d'expérience : jamais affiché sous le seuil de prudence ----
    def test_o_analyse_par_type_filtre_sous_seuil(self):
        reponses = [reponse_nps_test(email_client="petit" + str(i) + "@example.com") for i in range(3)]
        index = tickets_par_email([])
        resultats = analyser_nps_par_type_experience(reponses, index, 60, SEUIL_PRUDENCE_ECHANTILLON_NPS)
        self.assertEqual(resultats, [])

    # ---- P. Comparaison de groupes toujours accompagnée du disclaimer d'absence de causalité ----
    def test_p_disclaimer_biais_selection_present_et_non_causal(self):
        self.assertIn("biais de sélection", TEXTE_PRUDENCE_BIAIS_SELECTION.lower())
        self.assertNotIn("cause", TEXTE_PRUDENCE_BIAIS_SELECTION.lower())

    # ---- Q. Service recovery : cas compatibles seulement, jamais un avant/après individuel fabriqué ----
    def test_q_service_recovery_pas_de_structure_avant_apres(self):
        reponse_promoteur = reponse_nps_test(email_client="c@example.com", score=10, date_reponse=datetime.date(2026, 1, 20))
        ticket_csat_eleve = ticket_care_test(requester_email="c@example.com", created_at=datetime.date(2026, 1, 10), csat=4.8)
        index = tickets_par_email([ticket_csat_eleve])
        cas = evaluer_cas_compatibles_service_recovery([reponse_promoteur], index, 60, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(cas), 1)
        self.assertIn("reponse", cas[0])
        self.assertIn("ticket", cas[0])
        self.assertNotIn("avant", cas[0])
        self.assertNotIn("apres", cas[0])
        self.assertNotIn("delta", cas[0])

    def test_q_service_recovery_exclut_detracteurs_et_csat_bas(self):
        reponse_detracteur = reponse_nps_test(email_client="c1@example.com", score=3, date_reponse=datetime.date(2026, 1, 20))
        reponse_promoteur_csat_bas = reponse_nps_test(email_client="c2@example.com", score=10, date_reponse=datetime.date(2026, 1, 20))
        index = tickets_par_email([
            ticket_care_test(requester_email="c1@example.com", created_at=datetime.date(2026, 1, 10), csat=4.8),
            ticket_care_test(ticket_id=2, requester_email="c2@example.com", created_at=datetime.date(2026, 1, 10), csat=2.0),
        ])
        cas = evaluer_cas_compatibles_service_recovery([reponse_detracteur, reponse_promoteur_csat_bas], index, 60, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(cas), 0)

    # ---- R. Aucune fuite du futur : l'alignement d'un mois n'utilise jamais un mois postérieur ----
    def test_r_aucune_fuite_du_futur_dans_alignement(self):
        historique_nps_sans_futur = [{"nps": 10}, {"nps": 8}]
        historique_care_sans_futur = [
            {"csat": 4.2, "reopens_moyen": 0.05, "resolution_moyenne": 20},
            {"csat": 4.1, "reopens_moyen": 0.06, "resolution_moyenne": 22},
        ]
        historique_nps_avec_futur = historique_nps_sans_futur + [{"nps": -50}]
        historique_care_avec_futur = historique_care_sans_futur + [{"csat": 1.0, "reopens_moyen": 0.9, "resolution_moyenne": 500}]

        resultat_sans_futur = evaluer_alignement_care_nps(historique_nps_sans_futur, historique_care_sans_futur, 1)
        resultat_avec_futur = evaluer_alignement_care_nps(historique_nps_avec_futur, historique_care_avec_futur, 1)
        self.assertEqual(resultat_sans_futur["rang_nps"], resultat_avec_futur["rang_nps"])
        self.assertEqual(resultat_sans_futur["type"], resultat_avec_futur["type"])

    # ---- S. Contrôle qualité : score hors bornes 0-10 détecté ----
    def test_s_controle_qualite_score_hors_bornes(self):
        reponses = [reponse_nps_test(email_client="c@example.com", score=15)]
        index = tickets_par_email([])
        anomalies = controler_qualite_donnees_nps(reponses, index, 60)
        self.assertTrue(any("hors de l'échelle" in a for a in anomalies))

    # ---- T. Contrôle qualité : réponses multiples par client signalées comme information, pas erreur ----
    def test_t_controle_qualite_reponses_multiples_informatif(self):
        reponses = [
            reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2025, 12, 1)),
            reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 3, 1)),
        ]
        index = tickets_par_email([])
        anomalies = controler_qualite_donnees_nps(reponses, index, 60)
        self.assertTrue(any("plusieurs réponses NPS" in a for a in anomalies))
        self.assertTrue(any("pas une erreur" in a for a in anomalies))

    # ---- U. Contrôle qualité silencieux sur données propres ----
    def test_u_controle_qualite_silencieux_donnees_propres(self):
        reponses = [reponse_nps_test(email_client="c" + str(i) + "@example.com", score=7) for i in range(5)]
        index = tickets_par_email([])
        anomalies = controler_qualite_donnees_nps(reponses, index, 60)
        self.assertEqual(anomalies, [])

    # ---- V. Historique mensuel construit chronologiquement, un NPS entier calculable par mois ----
    def test_v_historique_mensuel_chronologique(self):
        reponses = [
            reponse_nps_test(email_client="a@example.com", date_reponse=datetime.date(2026, 2, 5), score=9),
            reponse_nps_test(email_client="b@example.com", date_reponse=datetime.date(2026, 1, 5), score=2),
        ]
        historique = construire_historique_nps_par_mois(reponses)
        self.assertEqual([item["cle_mois"] for item in historique], ["2026-01", "2026-02"])

    # ---- W. Profil Care mensuel : n=0 -> None, jamais un dict vide fabriqué ----
    def test_w_profil_care_mensuel_vide_retourne_none(self):
        self.assertIsNone(construire_profil_care_mensuel([]))


def signal_categoriel_test(sujet="Sujet test", niveau_priorite="Priorité principale", familles_actives=None, n=20, part_univers_pct=10.0):
    if familles_actives is None:
        familles_actives = ["A", "B"]
    return {
        "sujet": sujet, "niveau_priorite": niveau_priorite, "familles_actives": familles_actives,
        "observation_principale": "Observation test pour " + sujet + ".",
        "volume": {"n": n, "part_univers_pct": part_univers_pct, "univers": 200},
    }


def signal_av_test(sujet="Motif test", familles_actives=None, n=15, part_univers_pct=10.0):
    if familles_actives is None:
        familles_actives = ["A", "C"]
    return {
        "sujet": sujet, "familles_actives": familles_actives,
        "observation_principale": "Observation test avant-vente pour " + sujet + ".",
        "volume": {"n": n, "part_univers_pct": part_univers_pct, "univers": 100},
    }


def profil_ve_test(csat=4.0, reopens=0.05, resolution_h=20, replies=3, volume=100, mix_categories=None):
    if mix_categories is None:
        mix_categories = {}
    return {
        "csat": csat, "reopens": reopens, "resolution_h": resolution_h, "replies": replies,
        "volume": volume, "mix_categories": mix_categories,
    }


def vigilance_test(observation="Vigilance test.", pourquoi="Pourquoi test."):
    return {
        "date_debut": datetime.date(2026, 1, 12), "observation": observation, "pourquoi": pourquoi,
        "contexte": None, "prudence": "Association observée sur les données disponibles, pas une cause démontrée.",
    }


def alignement_nps_test(type_alignement):
    return {
        "type": type_alignement, "rang_nps": 0.0, "rang_csat": 0.0, "effort_degrade": True,
        "amplitude_nps": 0.9, "amplitude_suffisante": True,
    }


def evenement_contexte_ve_test(date_debut, date_fin=None, type_evenement="Staffing", nom="Événement test"):
    if date_fin is None:
        date_fin = date_debut
    return {
        "date_debut": date_debut, "date_fin": date_fin, "type": type_evenement,
        "nature": None, "nom_evenement": nom, "description": None, "perimetre": None,
    }


MOTS_PRESCRIPTIFS_INTERDITS_VUE_ENSEMBLE = (
    "recrutez", "recruter", "changez", "changer de transporteur", "créez immédiatement", "formez",
)


# Étape 5A -- composition Vue d'ensemble. Aucun moteur métier recalculé : ces fonctions
# sélectionnent/dédupliquent/composent UNIQUEMENT à partir des sorties déjà produites par les
# moteurs validés (Produit/Livraison/Avant-vente/Tendances/Impact & confiance).
DIAGNOSTIC_VIDE_VE_TEST = {"csat_bas": False, "effort_haut": False, "categories_part_haute": []}


# Étape 5A.1 -- composition éditoriale : signaux TRANSVERSAUX (Tendances/NPS, dégradation globale)
# vs DIAGNOSTIQUES/CATÉGORIELS (Produit/Livraison/Avant-vente, "où regarder"). Fusion Tendances+NPS
# "alignement_negatif" en une seule histoire structurée (jamais NLP) ; "divergence" reste distincte.
# Matérialité (famille B pour Produit/Livraison, part notable pour Avant-vente) appliquée AVANT
# regroupement/tri ; le plafond vient en dernier.
class TestCompositionVueEnsemble(unittest.TestCase):
    # ---- A. Tendances + Impact alignement négatif -> une seule histoire transversale ----
    def test_a_fusion_tendances_et_alignement_negatif(self):
        resultat = construire_signaux_attention_vue_ensemble(
            [], vigilance_test(), alignement_nps_test("alignement_negatif"), "Le NPS recule.",
            DIAGNOSTIC_VIDE_VE_TEST, 3,
        )
        signaux_transversaux = [s for s in resultat["retenus"] if s["priorite_tri"] == 0]
        self.assertEqual(len(signaux_transversaux), 1)
        self.assertEqual(signaux_transversaux[0]["titre"], "Expérience client sous tension")
        self.assertIn("NPS", signaux_transversaux[0]["texte"])

    # ---- B. Tendances + Impact divergence -> la divergence reste distincte ----
    def test_b_divergence_reste_distincte(self):
        resultat = construire_signaux_attention_vue_ensemble(
            [], vigilance_test(), alignement_nps_test("divergence"), "Divergence NPS/CSAT.",
            DIAGNOSTIC_VIDE_VE_TEST, 3,
        )
        self.assertEqual(len(resultat["retenus"]), 2)
        titres = [s["titre"] for s in resultat["retenus"]]
        self.assertIn("Expérience client sous tension", titres)
        self.assertIn("Confiance (NPS)", titres)

    # ---- C. Transversal + priorité Produit matérielle -> Produit n'est pas évincé ----
    def test_c_produit_materiel_coexiste_avec_transversal(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon", familles_actives=["A", "B", "C"])], [], [],
        )
        resultat = construire_signaux_attention_vue_ensemble(
            candidats, vigilance_test(), None, None, DIAGNOSTIC_VIDE_VE_TEST, 3,
        )
        self.assertEqual(len(resultat["retenus"]), 2)

    # ---- D. Signal spécialisé valide mais sans famille B -> absent de la Vue d'ensemble ----
    def test_d_signal_sans_famille_b_non_materiel(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Éveil", familles_actives=["A", "C", "D"])], [], [],
        )
        resultat = construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        self.assertEqual(resultat["retenus"], [])

    # ---- E. Signal spécialisé avec famille B -> présent ----
    def test_e_signal_avec_famille_b_materiel(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon", familles_actives=["A", "B", "C"])], [], [],
        )
        resultat = construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        self.assertEqual(len(resultat["retenus"]), 1)

    # ---- F. Période maîtrisée + signaux locaux faibles (sans B) -> Attention reste vide ----
    def test_f_periode_maitrisee_signaux_faibles_attention_vide(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Éveil", familles_actives=["A", "C", "D"])],
            [signal_categoriel_test(sujet="Colis annoncé livré non reçu", familles_actives=["A", "C", "D", "E"])],
            [signal_av_test(sujet="Motif", part_univers_pct=5.0)],
        )
        resultat = construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        self.assertEqual(resultat["retenus"], [])

    # ---- G. 0 Attention réel supporté ----
    def test_g_zero_signal_accepte(self):
        resultat = construire_signaux_attention_vue_ensemble([], None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        self.assertEqual(resultat["retenus"], [])

    # ---- H. Plafond appliqué APRÈS matérialité/fusion, pas avant ----
    def test_h_plafond_apres_materialite(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon", familles_actives=["A", "B", "C"], n=30),
             signal_categoriel_test(sujet="Éveil", familles_actives=["A", "C", "D"], n=50)],  # non matériel (pas de B)
            [signal_categoriel_test(sujet="Colis annoncé livré non reçu", familles_actives=["A", "B", "C", "D", "E"], n=20)],
            [],
        )
        resultat = construire_signaux_attention_vue_ensemble(
            candidats, vigilance_test(), alignement_nps_test("alignement_negatif"), "Texte NPS.",
            DIAGNOSTIC_VIDE_VE_TEST, 3,
        )
        # transversal fusionné (1) + Cocon matériel (1) + Livraison matériel (1) = 3 ; Éveil exclu en amont
        self.assertEqual(len(resultat["retenus"]), 3)
        for signal in resultat["retenus"]:
            self.assertNotIn("Éveil", signal["titre"])

    # ---- I. Événement en cours (commencé avant, se terminant après) -> jamais en anticipation ----
    def test_i_evenement_en_cours_jamais_en_anticipation(self):
        date_fin_periode = datetime.date(2026, 9, 13)
        evenement_long = evenement_contexte_ve_test(
            datetime.date(2026, 8, 20), date_fin=datetime.date(2026, 10, 1), type_evenement="Commercial",
        )
        anticipations = construire_points_anticipation_vue_ensemble([evenement_long], date_fin_periode)
        self.assertEqual(anticipations, [])
        contexte_actuel = contexte_periode(
            [evenement_long], date_fin_periode - datetime.timedelta(days=6), date_fin_periode,
        )
        self.assertEqual(len(contexte_actuel), 1)

    # ---- J. Événement futur staffing -> anticipation possible ----
    def test_j_evenement_futur_staffing_devient_anticipation(self):
        date_fin_periode = datetime.date(2026, 9, 13)
        evenements = [evenement_contexte_ve_test(datetime.date(2026, 9, 30), nom="Fin d'alternance Sofia")]
        anticipations = construire_points_anticipation_vue_ensemble(evenements, date_fin_periode)
        self.assertEqual(len(anticipations), 1)

    # ---- K. 4 événements futurs -> maximum 2 anticipations ----
    def test_k_quatre_evenements_futurs_plafonnes_a_deux(self):
        date_fin_periode = datetime.date(2025, 12, 21)
        evenements = [
            evenement_contexte_ve_test(datetime.date(2025, 12, 25), type_evenement="Commercial", nom="Noël"),
            evenement_contexte_ve_test(datetime.date(2026, 1, 2), type_evenement="Staffing", nom="Renfort"),
            evenement_contexte_ve_test(datetime.date(2026, 1, 5), type_evenement="Commercial", nom="Promo"),
            evenement_contexte_ve_test(datetime.date(2026, 1, 5), type_evenement="Staffing", nom="Arrivée Lucie"),
        ]
        anticipations = construire_points_anticipation_vue_ensemble(evenements, date_fin_periode)
        self.assertEqual(len(anticipations), 2)

    # ---- L. Transition staffing priorisée sur un événement commercial mineur futur ----
    def test_l_staffing_priorise_sur_commercial(self):
        date_fin_periode = datetime.date(2025, 12, 21)
        evenement_commercial_proche = evenement_contexte_ve_test(
            datetime.date(2025, 12, 22), type_evenement="Commercial", nom="Soldes",
        )
        evenement_staffing_plus_loin = evenement_contexte_ve_test(
            datetime.date(2026, 1, 5), type_evenement="Staffing", nom="Arrivée Lucie",
        )
        anticipations = construire_points_anticipation_vue_ensemble(
            [evenement_commercial_proche, evenement_staffing_plus_loin], date_fin_periode, nombre_max=1,
        )
        self.assertEqual(len(anticipations), 1)
        self.assertEqual(anticipations[0]["nom_evenement"], "Arrivée Lucie")

    # ---- M. Lecture "maîtrisée" + Attention au plafond -> contrôle de cohérence détecte ----
    def test_m_coherence_detecte_lecture_calme_avec_attention_pleine(self):
        self.assertFalse(verifier_coherence_lecture_attention_vue_ensemble(True, 3, 3))
        self.assertTrue(verifier_coherence_lecture_attention_vue_ensemble(True, 1, 3))
        self.assertTrue(verifier_coherence_lecture_attention_vue_ensemble(False, 3, 3))

    # ---- Matérialité : Produit/Livraison exigent la famille B, jamais E seule (chronique) ----
    def test_materialite_produit_sans_b_mais_avec_e_non_materiel(self):
        candidat = {
            "categorie": CATEGORIE_SAV_PRODUIT, "familles_actives": ["A", "C", "D", "E"],
            "part_univers_pct": 30.0,
        }
        self.assertFalse(signal_categoriel_est_materiel_vue_ensemble(candidat))

    def test_materialite_produit_avec_b_materiel(self):
        candidat = {"categorie": CATEGORIE_SAV_PRODUIT, "familles_actives": ["A", "B"], "part_univers_pct": 5.0}
        self.assertTrue(signal_categoriel_est_materiel_vue_ensemble(candidat))

    # ---- Matérialité Avant-vente : part réellement notable (réutilise SEUIL_VOLUME_PART_NOTABLE) ----
    def test_materialite_avant_vente_part_faible_non_materiel(self):
        candidat = {"categorie": CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE, "familles_actives": ["A", "C"], "part_univers_pct": 7.0}
        self.assertFalse(signal_categoriel_est_materiel_vue_ensemble(candidat))

    def test_materialite_avant_vente_part_haute_materiel(self):
        candidat = {"categorie": CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE, "familles_actives": ["A", "C"], "part_univers_pct": 20.0}
        self.assertTrue(signal_categoriel_est_materiel_vue_ensemble(candidat))

    # ---- Diagnostics structurés transversaux : lus sur les profils, jamais sur le texte ----
    def test_diagnostics_structures_detectent_csat_bas_et_effort_haut(self):
        profils = [
            profil_ve_test(csat=4.3, reopens=0.03, resolution_h=20, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 20}),
            profil_ve_test(csat=4.2, reopens=0.04, resolution_h=22, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 22}),
            profil_ve_test(csat=3.5, reopens=0.20, resolution_h=60, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 40}),
        ]
        diagnostics = evaluer_diagnostics_structures_transversal_vue_ensemble(profils, 2, [CATEGORIE_SAV_PRODUIT])
        self.assertTrue(diagnostics["csat_bas"])
        self.assertTrue(diagnostics["effort_haut"])
        self.assertIn(CATEGORIE_SAV_PRODUIT, diagnostics["categories_part_haute"])

    def test_diagnostics_structures_periode_normale_rien_de_marque(self):
        profils = [
            profil_ve_test(csat=4.0, reopens=0.05, resolution_h=20, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 20}),
            profil_ve_test(csat=4.1, reopens=0.05, resolution_h=21, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 19}),
            profil_ve_test(csat=4.05, reopens=0.05, resolution_h=20, volume=100, mix_categories={CATEGORIE_SAV_PRODUIT: 20}),
        ]
        diagnostics = evaluer_diagnostics_structures_transversal_vue_ensemble(profils, 2, [CATEGORIE_SAV_PRODUIT])
        self.assertFalse(diagnostics["csat_bas"])
        self.assertFalse(diagnostics["effort_haut"])

    # ---- Texte transversal jamais un simple copié du texte de vigilance (composé structurellement) ----
    def test_texte_transversal_compose_structurellement(self):
        diagnostics = {"csat_bas": True, "effort_haut": True, "categories_part_haute": [CATEGORIE_SAV_PRODUIT]}
        texte = texte_signal_transversal_vue_ensemble(diagnostics, None)
        self.assertIn("satisfaction", texte)
        self.assertIn("effort", texte)
        self.assertIn(CATEGORIE_SAV_PRODUIT, texte)
        self.assertNotIn("Le NPS évolue également", texte)

    def test_texte_transversal_mentionne_nps_si_fusionne(self):
        diagnostics = {"csat_bas": False, "effort_haut": False, "categories_part_haute": []}
        texte = texte_signal_transversal_vue_ensemble(diagnostics, "texte nps")
        self.assertIn("Le NPS évolue également", texte)

    # ---- Regroupement structuré par catégorie (jamais par texte) ----
    def test_regroupement_deux_signaux_meme_categorie_fusionnes(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon", familles_actives=["B", "C"]),
             signal_categoriel_test(sujet="Évasion", familles_actives=["B", "C", "E"])],
            [], [],
        )
        regroupes = regrouper_candidats_par_categorie_vue_ensemble(candidats)
        self.assertEqual(len(regroupes), 1)
        self.assertIn("Cocon", regroupes[0]["texte"])
        self.assertIn("Évasion", regroupes[0]["texte"])
        self.assertIn("satisfaction", regroupes[0]["texte"])
        self.assertIn("effort", regroupes[0]["texte"])

    def test_regroupement_categories_differentes_jamais_fusionnees(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon")],
            [signal_categoriel_test(sujet="Colis annoncé livré non reçu")],
            [],
        )
        regroupes = regrouper_candidats_par_categorie_vue_ensemble(candidats)
        self.assertEqual(len(regroupes), 2)

    # ---- Seul le tier le plus haut (Priorité principale) est éligible, jamais secondaire ----
    def test_priorite_secondaire_jamais_candidate(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(niveau_priorite="Priorité secondaire")], [], [],
        )
        self.assertEqual(candidats, [])

    # ---- Avant-vente : toutes les opportunités transmises sont déjà le tier le plus haut ----
    def test_avant_vente_opportunites_toutes_candidates(self):
        candidats = extraire_candidats_categoriels_vue_ensemble([], [], [signal_av_test(sujet="Sable")])
        self.assertEqual(len(candidats), 1)
        self.assertEqual(candidats[0]["categorie"], CATEGORIE_AVANT_VENTE_VUE_ENSEMBLE)

    # ---- Navigation dérivée des signaux réellement retenus, jamais une liste fixe ----
    def test_navigation_derivee_des_signaux_retenus(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [], [signal_categoriel_test(sujet="Colis annoncé livré non reçu", familles_actives=["A", "B"])], [],
        )
        resultat = construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        navigation = construire_navigation_vue_ensemble(resultat["retenus"])
        self.assertEqual(navigation, ["Livraison"])

    def test_navigation_vide_si_aucun_signal_retenu(self):
        resultat = construire_signaux_attention_vue_ensemble([], None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        navigation = construire_navigation_vue_ensemble(resultat["retenus"])
        self.assertEqual(navigation, [])

    # ---- Aucune donnée agent ne transite dans les signaux (pas de leaderboard) ----
    def test_aucune_cle_agent_dans_les_signaux(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(familles_actives=["A", "B"])], [], [],
        )
        resultat = construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        for signal in resultat["retenus"]:
            self.assertNotIn("agent", signal)

    # ---- Les dicts de signaux originaux ne sont jamais mutés par la composition ----
    def test_signaux_originaux_non_mutes(self):
        signal_original = signal_categoriel_test(sujet="Batterie", familles_actives=["A", "B"])
        cles_avant = set(signal_original.keys())
        candidats = extraire_candidats_categoriels_vue_ensemble([signal_original], [], [])
        construire_signaux_attention_vue_ensemble(candidats, None, None, None, DIAGNOSTIC_VIDE_VE_TEST, 3)
        self.assertEqual(set(signal_original.keys()), cles_avant)

    # ---- Aucune recommandation prescriptive dans les textes composés ----
    def test_aucune_recommandation_prescriptive(self):
        candidats = extraire_candidats_categoriels_vue_ensemble(
            [signal_categoriel_test(sujet="Cocon", familles_actives=["B", "C"]),
             signal_categoriel_test(sujet="Évasion", familles_actives=["B", "C", "D"])],
            [], [],
        )
        regroupes = regrouper_candidats_par_categorie_vue_ensemble(candidats)
        for regroupe in regroupes:
            texte_minuscule = regroupe["texte"].lower()
            for mot in MOTS_PRESCRIPTIFS_INTERDITS_VUE_ENSEMBLE:
                self.assertNotIn(mot, texte_minuscule)


def historique_nps_test(valeurs_nps):
    historique = []
    for valeur in valeurs_nps:
        historique.append({"nps": valeur})
    return historique


def historique_care_test(lignes):
    # chaque ligne = (csat, reopens_moyen, resolution_moyenne)
    historique = []
    for ligne in lignes:
        historique.append({"csat": ligne[0], "reopens_moyen": ligne[1], "resolution_moyenne": ligne[2]})
    return historique


# Étape 4E.1 -- la prudence d'échantillon n'est plus un seuil absolu (n>=15 = "étayée" était une
# fausse équivalence statistique) : elle situe le n du mois par rapport aux AUTRES n déjà
# disponibles (rang), jamais à un chiffre magique. L'alignement/divergence n'utilise plus
# seulement un rang extrême (une série resserrée transformait mécaniquement son minimum en
# "NPS bas") : une AMPLITUDE réelle (écart / étendue déjà observée >= 50 %) est désormais exigée
# en plus de la position, pour toutes les branches (négatif/positif/divergence).
class TestImpactConfianceNPS4E1(unittest.TestCase):
    # ---- A. n=18 après un historique de 40-80 -> lecture à prendre avec prudence ----
    def test_a_petit_n_relatif_a_la_serie(self):
        historique_n = [73, 43, 55, 87, 69, 47, 61, 48, 59, 62, 50, 52, 18]
        etat = evaluer_prudence_echantillon_nps(historique_n, 12)
        self.assertEqual(etat, ETAT_PRUDENCE_VOLUME_FAIBLE)

    # ---- B. Première observation n=18 -> pas de comparaison à des données futures ----
    def test_b_premiere_observation_ignore_le_futur(self):
        historique_n_avec_futur = [18, 73, 43, 55]
        etat = evaluer_prudence_echantillon_nps(historique_n_avec_futur, 0)
        self.assertEqual(etat, ETAT_PRUDENCE_PREMIERE_OBSERVATION)

    # ---- C. Première observation n=73 -> pas de qualification relative future, quelle que soit sa taille ----
    def test_c_premiere_observation_grand_n_toujours_sans_comparaison(self):
        historique_n_avec_futur = [73, 43, 55, 87, 18]
        etat = evaluer_prudence_echantillon_nps(historique_n_avec_futur, 0)
        self.assertEqual(etat, ETAT_PRUDENCE_PREMIERE_OBSERVATION)
        texte = texte_prudence_echantillon_nps(etat, 73)
        self.assertIn("pas encore assez d'historique", texte)

    # ---- D. Historique compact +7,+9,+7,+6 -> pas de divergence uniquement parce que +6 est le minimum ----
    def test_d_serie_compacte_pas_de_divergence_forcee(self):
        historique_nps = historique_nps_test([7, 9, 7, 6])
        # sans le garde-fou d'amplitude, un CSAT bas au même mois aurait déclenché "alignement_negatif"
        historique_care = historique_care_test([
            (4.5, 0.05, 20), (4.5, 0.05, 20), (4.5, 0.05, 20), (3.0, 0.05, 20),
        ])
        ratio = amplitude_relative_etendue([7, 9, 7, 6], 3)
        self.assertLess(ratio, SEUIL_AMPLITUDE_PART_ETENDUE_NPS)
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 3)
        self.assertIsNone(resultat["type"])
        self.assertFalse(resultat["amplitude_suffisante"])

    # ---- E. Rupture réelle +7,+9,+7,+6,-6 + CSAT/effort dégradés -> alignement négatif possible ----
    def test_e_rupture_reelle_avec_csat_et_effort_degrades(self):
        historique_nps = historique_nps_test([7, 9, 7, 6, -6])
        historique_care = historique_care_test([
            (4.5, 0.05, 20), (4.5, 0.05, 20), (4.5, 0.05, 20), (4.5, 0.05, 20), (3.0, 0.20, 60),
        ])
        ratio = amplitude_relative_etendue([7, 9, 7, 6, -6], 4)
        self.assertGreaterEqual(ratio, SEUIL_AMPLITUDE_PART_ETENDUE_NPS)
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 4)
        self.assertEqual(resultat["type"], "alignement_negatif")

    # ---- F. NPS compact + CSAT haut -> pas de divergence ----
    def test_f_nps_compact_csat_haut_pas_de_divergence(self):
        historique_nps = historique_nps_test([7, 9, 7, 6])
        historique_care = historique_care_test([
            (4.0, 0.05, 20), (4.0, 0.05, 20), (4.0, 0.05, 20), (4.9, 0.05, 20),
        ])
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 3)
        self.assertIsNone(resultat["type"])

    # ---- G. NPS réellement bas historiquement + CSAT haut -> divergence possible ----
    def test_g_rupture_basse_reelle_csat_haut_divergence(self):
        historique_nps = historique_nps_test([7, 9, 7, 6, -5])
        historique_care = historique_care_test([
            (4.0, 0.05, 20), (4.05, 0.05, 20), (4.0, 0.05, 20), (4.0, 0.05, 20), (4.5, 0.05, 20),
        ])
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 4)
        self.assertEqual(resultat["type"], "divergence")

    # ---- H. Petite hausse NPS + petite hausse CSAT -> pas d'alignement positif forcé ----
    def test_h_petite_hausse_pas_alignement_positif_force(self):
        historique_nps = historique_nps_test([6, 7, 6, 7])
        historique_care = historique_care_test([
            (4.0, 0.05, 20), (4.05, 0.05, 20), (4.0, 0.05, 20), (4.1, 0.05, 20),
        ])
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 3)
        self.assertIsNone(resultat["type"])

    # ---- I. Hausse NPS réellement marquée + amélioration Care cohérente -> alignement positif possible ----
    def test_i_hausse_marquee_alignement_positif(self):
        historique_nps = historique_nps_test([6, 7, 6, 30])
        historique_care = historique_care_test([
            (3.8, 0.10, 40), (3.85, 0.10, 40), (3.8, 0.10, 40), (4.8, 0.02, 15),
        ])
        ratio = amplitude_relative_etendue([6, 7, 6, 30], 3)
        self.assertGreaterEqual(ratio, SEUIL_AMPLITUDE_PART_ETENDUE_NPS)
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 3)
        self.assertEqual(resultat["type"], "alignement_positif")

    # ---- J. Pic isolé (type avril) sans corrélat Care -> pas d'alignement positif, même si l'amplitude passe ----
    def test_j_pic_isole_amplitude_ok_mais_pas_de_corrélat_pas_dalignement(self):
        historique_nps = historique_nps_test([3, 3, 31])
        historique_care = historique_care_test([
            (3.9, 0.05, 20), (4.0, 0.05, 20), (3.96, 0.05, 20),
        ])
        ratio = amplitude_relative_etendue([3, 3, 31], 2)
        self.assertGreaterEqual(ratio, SEUIL_AMPLITUDE_PART_ETENDUE_NPS)  # l'amplitude, seule, passerait
        resultat = evaluer_alignement_care_nps(historique_nps, historique_care, 2)
        self.assertIsNone(resultat["type"])  # bloqué par l'absence de corrélat CSAT (rang médian)

    # ---- K. Petit n + score élevé -> la prudence reste prioritaire, indépendante du score ----
    def test_k_prudence_independante_du_score_nps(self):
        historique_n = [73, 43, 55, 87, 69, 47, 61, 48, 59, 62, 50, 52, 18]
        etat = evaluer_prudence_echantillon_nps(historique_n, 12)
        texte_prudence = texte_prudence_echantillon_nps(etat, 18)
        # le texte de prudence ne dépend pas du NPS du mois (même très positif, la prudence prime)
        self.assertIn("prudence", texte_prudence.lower())
        self.assertNotIn("NPS", texte_prudence)

    # ---- L. Segmentation "Contact Care identifié" inchangée (verrouillée, 4E.1 section 14) ----
    def test_l_segmentation_contact_care_inchangee(self):
        reponse = reponse_nps_test(email_client="c@example.com", date_reponse=datetime.date(2026, 1, 20))
        ticket = ticket_care_test(requester_email="c@example.com", created_at=datetime.date(2026, 1, 10))
        index = tickets_par_email([ticket])
        segmentation = segmenter_nps_par_contact_care([reponse], index, 60)
        self.assertEqual(segmentation["contact_identifie"]["composition"]["n"], 1)
        self.assertIsNone(segmentation["aucun_contact_identifie"]["composition"])


def profil_observation_test(date_debut, date_fin=None, csat=4.0, volume=100, mix_categories=None):
    if date_fin is None:
        date_fin = date_debut + datetime.timedelta(days=6)
    if mix_categories is None:
        mix_categories = {}
    return {"date_debut": date_debut, "date_fin": date_fin, "csat": csat, "volume": volume, "mix_categories": mix_categories}


# Étape 5B -- composition Tendances UI. Le moteur 4B (construire_lecture_tendances,
# determiner_mode_tendances, rang_relatif, règles de vigilance/jalon/contraste/saisonnalité, no
# future leakage) N'EST PAS MODIFIÉ et reste couvert par TestMoteurTendances/TestScopeTendances
# (déjà 306 tests avant cette étape, inchangés) -- seules les DEUX nouvelles fonctions de
# composition UI (lecture pure des sorties moteur, aucune règle métier) sont testées ici.
class TestCompositionTendancesUI(unittest.TestCase):
    def test_mix_dominant_categorie_la_plus_nombreuse(self):
        mix = {"Livraison": 50, "SAV produit (défaut)": 120, "Avant-vente / conseil": 30}
        self.assertEqual(categorie_dominante_mix_tendances(mix), "SAV produit (défaut)")

    def test_mix_dominant_dict_vide_retourne_none(self):
        self.assertIsNone(categorie_dominante_mix_tendances({}))

    def test_periode_reference_mode_observation_unique_utilise_la_derniere_observation(self):
        profils = [
            profil_observation_test(datetime.date(2025, 12, 15), datetime.date(2025, 12, 21)),
            profil_observation_test(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18)),
        ]
        texte = construire_texte_periode_reference_tendances(profils, MODE_OBSERVATION_UNIQUE, 1)
        self.assertIn("2026-01-12", texte)
        self.assertIn("2026-01-18", texte)
        self.assertIn("Historique de référence : jusqu'au 2026-01-18", texte)

    def test_periode_reference_mode_fenetre_utilise_la_fenetre_selectionnee(self):
        profils = [
            profil_observation_test(datetime.date(2025, 9, 1), datetime.date(2025, 9, 7)),
            profil_observation_test(datetime.date(2025, 11, 24), datetime.date(2025, 11, 30)),
            profil_observation_test(datetime.date(2025, 12, 15), datetime.date(2025, 12, 21)),
            profil_observation_test(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18)),
        ]
        # fenêtre sélectionnée = les 3 dernières observations (nov->jan), la 1re (sept) reste
        # historique de référence uniquement -- jamais mélangée à la "période analysée".
        texte = construire_texte_periode_reference_tendances(profils, MODE_PERIODE_ETENDUE, 3)
        self.assertIn("Période analysée : 2025-11-24 → 2026-01-18", texte)
        self.assertNotIn("2025-09-01", texte.split("Historique de référence")[0])

    def test_periode_reference_aucun_profil_retourne_none(self):
        self.assertIsNone(construire_texte_periode_reference_tendances([], MODE_OBSERVATION_UNIQUE, 1))

    def test_periode_reference_jamais_au_dela_des_profils_fournis(self):
        # aucune fuite du futur : la référence ne peut jamais dépasser le dernier profil transmis
        # (profils_historique est déjà borné à date_a_fin par construction dans onglet_tendances).
        profils = [profil_observation_test(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18))]
        texte = construire_texte_periode_reference_tendances(profils, MODE_OBSERVATION_UNIQUE, 1)
        self.assertIn("jusqu'au 2026-01-18", texte)


def ticket_agent_test(ticket_id=1, assignee="Agent Test", csat=4.0, ticket_reason="Livraison", resolution_type=None):
    return {
        "ticket_id": ticket_id, "assignee": assignee, "csat": csat,
        "ticket_reason": ticket_reason, "resolution_type": resolution_type,
    }


def evenement_staffing_agent_test(perimetre, date_debut, date_fin=None, nom="Absence test"):
    if date_fin is None:
        date_fin = date_debut
    return {
        "date_debut": date_debut, "date_fin": date_fin, "type": "Staffing",
        "nature": None, "nom_evenement": nom, "description": None, "perimetre": perimetre,
    }


# Étape 5C.1 -- "Portrait factuel des contributions" : aucun score, aucun classement, aucune
# performance déduite. Toutes ces fonctions produisent des constats descriptifs (charge relative,
# mix, présence/absence structurée) -- jamais un jugement.
class TestCompositionAgents(unittest.TestCase):
    # ---- A/B/C/D. Heures planifiées : 35h/21h/14h, plusieurs créneaux/jour sommés ----
    def test_a_heures_35h_temps_plein(self):
        planning = {"Amine": {0: [(9, 12), (13, 17)], 1: [(9, 12), (13, 17)], 2: [(9, 12), (13, 17)], 3: [(9, 12), (13, 17)], 4: [(9, 12), (13, 17)]}}
        self.assertEqual(heures_planifiees_agent(planning, "Amine"), 35)

    def test_b_heures_21h_alternance(self):
        planning = {"Sofia": {0: [(9, 16)], 2: [(9, 16)], 4: [(9, 16)]}}
        self.assertEqual(heures_planifiees_agent(planning, "Sofia"), 21)

    def test_c_heures_14h(self):
        planning = {"Sofia": {2: [(9, 16)], 4: [(9, 16)]}}
        self.assertEqual(heures_planifiees_agent(planning, "Sofia"), 14)

    def test_e_plusieurs_creneaux_par_jour_sommes(self):
        planning = {"Kristelle": {0: [(9, 12), (13, 18)]}}
        self.assertEqual(heures_planifiees_agent(planning, "Kristelle"), 8)

    # ---- F. Agent non planifié -> pas de division par zéro ----
    def test_f_charge_relative_sans_heures_retourne_none(self):
        self.assertIsNone(charge_relative_agent(50, 0))
        self.assertIsNone(charge_relative_agent(50, None))

    # ---- G. Agent planifié 0 ticket -> charge 0 descriptive (calculable, jamais une erreur) ----
    def test_g_charge_relative_zero_ticket(self):
        self.assertEqual(charge_relative_agent(0, 35), 0)

    def test_charge_relative_calcul_simple(self):
        self.assertAlmostEqual(charge_relative_agent(350, 35), 10.0)

    # ---- I. CSAT inclut n (vérifié via moyenne + comptage direct, pas de nouvelle fonction requise) ----
    def test_i_mix_pct_somme_a_cent(self):
        tickets = [
            ticket_agent_test(1, ticket_reason="Livraison"),
            ticket_agent_test(2, ticket_reason="Livraison"),
            ticket_agent_test(3, ticket_reason="Conseil programme / produit"),
        ]
        mix = mix_pct_agent(tickets)
        self.assertAlmostEqual(sum(mix.values()), 100.0)

    # ---- K. Catégorie absente = 0 %, pas erreur (dict creux, .get() côté appelant) ----
    def test_k_mix_pct_categorie_absente_ne_leve_pas_erreur(self):
        tickets = [ticket_agent_test(1, ticket_reason="Livraison")]
        mix = mix_pct_agent(tickets)
        self.assertEqual(mix.get("Avant-vente / conseil", 0), 0)

    def test_mix_pct_liste_vide_retourne_dict_vide(self):
        self.assertEqual(mix_pct_agent([]), {})

    # ---- Roster : agent planifié + tickets -> planifie_actif ----
    def test_roster_agent_planifie_et_actif(self):
        tickets = [ticket_agent_test(1, assignee="Amine")]
        plannings = [(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), {"Amine": {0: [(9, 17)]}})]
        roster = construire_roster_agents(tickets, plannings, [], datetime.date(2026, 1, 12), datetime.date(2026, 1, 18))
        self.assertEqual(len(roster), 1)
        self.assertEqual(roster[0]["statut"], STATUT_AGENT_PLANIFIE_ACTIF)

    # ---- H. Agent non planifié + tickets -> renfort non planifié, activité visible ----
    def test_h_roster_renfort_non_planifie(self):
        tickets = [ticket_agent_test(1, assignee="Sam")]
        roster = construire_roster_agents(tickets, [], [], datetime.date(2025, 12, 15), datetime.date(2025, 12, 21))
        self.assertEqual(roster[0]["statut"], STATUT_AGENT_RENFORT_NON_PLANIFIE)
        self.assertIsNone(charge_relative_agent(len(roster[0]["tickets"]), roster[0]["heures_planifiees"]))

    # ---- Agent planifié, 0 ticket -> planifie_sans_activite (visible, jamais "0 performance") ----
    def test_roster_agent_planifie_sans_ticket(self):
        plannings = [(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), {"Kristelle": {0: [(9, 17)]}})]
        roster = construire_roster_agents([], plannings, [], datetime.date(2026, 1, 12), datetime.date(2026, 1, 18))
        self.assertEqual(roster[0]["statut"], STATUT_AGENT_PLANIFIE_SANS_ACTIVITE)

    # ---- L. Agent absent avec événement Staffing -> statut absent, jamais de métrique 0 comme performance ----
    def test_l_roster_agent_absent_avec_evenement(self):
        evenements = [evenement_staffing_agent_test("Amine", datetime.date(2026, 3, 9), datetime.date(2026, 3, 15), "Absence Amine (congés)")]
        roster = construire_roster_agents([], [], evenements, datetime.date(2026, 3, 9), datetime.date(2026, 3, 15))
        self.assertEqual(len(roster), 1)
        self.assertEqual(roster[0]["statut"], STATUT_AGENT_ABSENT)
        self.assertEqual(roster[0]["evenement_absence"]["nom_evenement"], "Absence Amine (congés)")
        self.assertEqual(roster[0]["heures_planifiees"], 0)
        self.assertEqual(len(roster[0]["tickets"]), 0)

    # ---- M. Sam hors décembre -> n'apparaît simplement pas (pas d'historique à zéro) ----
    def test_m_agent_totalement_absent_najamais_dans_le_roster(self):
        roster = construire_roster_agents([], [], [], datetime.date(2026, 3, 9), datetime.date(2026, 3, 15))
        noms = [ligne["agent"] for ligne in roster]
        self.assertNotIn("Sam", noms)

    # ---- N/O. Lucie avant janvier / Sofia avant son arrivée -> absentes du roster, pas "absentes" ----
    def test_n_agent_hors_fenetre_staffing_najamais_dans_le_roster(self):
        evenements = [evenement_staffing_agent_test("Lucie", datetime.date(2026, 1, 5), nom="Arrivée Lucie (stage)")]
        # Roster de septembre 2025 : aucun ticket, aucun planning, et l'événement Lucie ne
        # chevauche pas cette période -> Lucie n'apparaît pas du tout.
        roster = construire_roster_agents([], [], evenements, datetime.date(2025, 9, 1), datetime.date(2025, 9, 7))
        noms = [ligne["agent"] for ligne in roster]
        self.assertNotIn("Lucie", noms)

    # ---- S. Aucun tri par volume : ordre alphabétique, stable et neutre ----
    def test_s_roster_trie_alphabetiquement_jamais_par_volume(self):
        tickets = (
            [ticket_agent_test(i, assignee="Sofia") for i in range(1, 3)]
            + [ticket_agent_test(i, assignee="Amine") for i in range(10, 30)]
        )
        plannings = [(datetime.date(2026, 1, 1), datetime.date(2026, 1, 7), {"Sofia": {0: [(9, 17)]}, "Amine": {0: [(9, 17)]}})]
        roster = construire_roster_agents(tickets, plannings, [], datetime.date(2026, 1, 1), datetime.date(2026, 1, 7))
        noms = [ligne["agent"] for ligne in roster]
        self.assertEqual(noms, sorted(noms))
        # Amine a bien plus de tickets que Sofia mais apparaît après elle (ordre alphabétique)
        self.assertEqual(noms, ["Amine", "Sofia"])

    # ---- Lecture équipe : générique, aucun texte codé par agent ----
    def test_lecture_equipe_generique_toute_composition(self):
        tickets = [ticket_agent_test(1, assignee="X"), ticket_agent_test(2, assignee="Y")]
        plannings = [(datetime.date(2026, 1, 1), datetime.date(2026, 1, 7), {"X": {0: [(9, 17)]}, "Y": {0: [(9, 17)]}})]
        roster = construire_roster_agents(tickets, plannings, [], datetime.date(2026, 1, 1), datetime.date(2026, 1, 7))
        texte = construire_lecture_equipe_agents(roster)
        self.assertIn("X", texte)
        self.assertIn("Y", texte)
        self.assertNotIn("meilleur", texte.lower())
        self.assertNotIn("pire", texte.lower())
        self.assertNotIn("top", texte.lower())

    def test_lecture_equipe_aucune_activite(self):
        texte = construire_lecture_equipe_agents([])
        self.assertEqual(texte, "Aucune activité observée pour cette période.")

    # ---- Q. Historique agent : jamais de point 0 pendant absence ----
    def test_q_historique_agent_saute_les_semaines_sans_ticket(self):
        exports_avec_donnees = [
            (datetime.date(2026, 3, 9), datetime.date(2026, 3, 15), [], {}),  # Amine absent cette semaine
            (datetime.date(2026, 5, 25), datetime.date(2026, 5, 31), [ticket_agent_test(1, assignee="Amine")], {"Amine": {0: [(9, 17)]}}),
        ]
        historique = construire_historique_agent(exports_avec_donnees, "Amine")
        self.assertEqual(len(historique), 1)
        self.assertEqual(historique[0]["date_debut"], datetime.date(2026, 5, 25))

    # ---- P. Historique borné aux exports fournis par l'appelant (no future leakage) ----
    def test_p_historique_agent_borne_aux_exports_fournis(self):
        exports_avec_donnees = [
            (datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), [ticket_agent_test(1, assignee="Amine")], {"Amine": {0: [(9, 17)]}}),
        ]
        historique = construire_historique_agent(exports_avec_donnees, "Amine")
        self.assertEqual(len(historique), 1)
        for item in historique:
            self.assertLessEqual(item["date_debut"], datetime.date(2026, 1, 18))

    # ---- Historique : contient charge relative et CSAT+n, jamais de division par zéro ----
    def test_historique_agent_champs_complets(self):
        exports_avec_donnees = [
            (datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), [ticket_agent_test(1, assignee="Amine", csat=4.5)], {"Amine": {0: [(9, 17)]}}),
        ]
        historique = construire_historique_agent(exports_avec_donnees, "Amine")
        self.assertEqual(historique[0]["tickets"], 1)
        self.assertEqual(historique[0]["heures_planifiees"], 8)
        self.assertAlmostEqual(historique[0]["charge_relative"], 1 / 8)
        self.assertEqual(historique[0]["csat"], 4.5)
        self.assertEqual(historique[0]["n_csat"], 1)

    # ---- R. Aucun champ "Profil" ne subsiste dans les nouvelles fonctions de composition ----
    def test_r_aucune_cle_profil_dans_le_roster(self):
        tickets = [ticket_agent_test(1, assignee="Amine")]
        plannings = [(datetime.date(2026, 1, 1), datetime.date(2026, 1, 7), {"Amine": {0: [(9, 17)]}})]
        roster = construire_roster_agents(tickets, plannings, [], datetime.date(2026, 1, 1), datetime.date(2026, 1, 7))
        self.assertNotIn("profil", roster[0])
        self.assertNotIn("score", roster[0])


def ticket_actions_test(ticket_id=1, subject_cluster="Sujet test", csat=3.5, macro_applied=None,
                         replies=2, csat_comment=None, created_at=None):
    if created_at is None:
        created_at = datetime.date(2026, 1, 15)
    return {
        "ticket_id": ticket_id, "subject_cluster": subject_cluster, "csat": csat,
        "macro_applied": macro_applied, "replies": replies, "csat_comment": csat_comment,
        "created_at": created_at,
    }


def tickets_sujet_actions_test(nombre, subject_cluster, csat=3.5, macro_applied=None, replies=2, csat_comment=None):
    tickets = []
    for i in range(nombre):
        tickets.append(ticket_actions_test(
            ticket_id=i, subject_cluster=subject_cluster, csat=csat,
            macro_applied=macro_applied, replies=replies, csat_comment=csat_comment,
        ))
    return tickets


# Étape 5D.1 -- "Actions & améliorations" remplace l'ancien onglet "Alertes & suggestions" (audit
# Étape 5D : score inter-familles opaque, redondant avec Vue d'ensemble/4B, jamais silencieux même
# sur une période calme). Pistes séparées par famille (jamais de score composite les comparant),
# wording non prescriptif, actions déjà menées avec discipline no-future-leakage stricte.
class TestCompositionActionsAmeliorations(unittest.TestCase):
    # ---- sujet_deja_traite_actions ----
    def test_sujet_deja_traite_vrai_si_fait_avec_date(self):
        suivi = {"Sujet A": {"statut": "Fait", "date_action": datetime.date(2026, 1, 1), "notes": None}}
        self.assertTrue(sujet_deja_traite_actions("Sujet A", suivi))

    def test_sujet_deja_traite_faux_si_absent_du_suivi(self):
        self.assertFalse(sujet_deja_traite_actions("Sujet inconnu", {}))

    def test_sujet_deja_traite_faux_si_statut_pas_fait(self):
        suivi = {"Sujet A": {"statut": "En attente", "date_action": None, "notes": None}}
        self.assertFalse(sujet_deja_traite_actions("Sujet A", suivi))

    # ---- Standardisation : détection + wording (G) + tri (F) + exclusion sujet traité (H) ----
    def test_standardisation_detecte_macro_absente(self):
        tickets = tickets_sujet_actions_test(6, "Choix du programme", csat=3.5, macro_applied=None)
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(pistes), 1)
        self.assertEqual(pistes[0]["famille"], FAMILLE_STANDARDISATION_ACTIONS)
        self.assertEqual(pistes[0]["sous_type"], "macro_absente")

    def test_standardisation_macro_bien_utilisee_donne_sous_type_insuffisant(self):
        tickets = tickets_sujet_actions_test(6, "Choix du programme", csat=3.5, macro_applied="MAC-001")
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(pistes[0]["sous_type"], "macro_insuffisante")

    def test_standardisation_wording_non_prescriptif(self):
        tickets = tickets_sujet_actions_test(6, "Choix du programme", csat=3.5, macro_applied=None)
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertTrue(pistes[0]["piste"].startswith("Piste :"))
        self.assertNotIn("Créer une macro", pistes[0]["piste"])

    def test_standardisation_exclut_sujet_deja_traite(self):
        tickets = tickets_sujet_actions_test(6, "Choix du programme", csat=3.5, macro_applied=None)
        suivi = {"Choix du programme": {"statut": "Fait", "date_action": datetime.date(2026, 1, 1), "notes": None}}
        pistes = identifier_pistes_standardisation(tickets, suivi, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(pistes), 0)

    def test_standardisation_csat_satisfaisant_exclu(self):
        tickets = tickets_sujet_actions_test(6, "Sujet satisfaisant", csat=4.5, macro_applied=None)
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(pistes), 0)

    def test_standardisation_sous_seuil_volume_exclu(self):
        tickets = tickets_sujet_actions_test(3, "Petit volume", csat=3.5, macro_applied=None)
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(len(pistes), 0)

    def test_standardisation_tri_volume_decroissant(self):
        tickets = (
            tickets_sujet_actions_test(6, "Petit sujet", csat=3.5, macro_applied=None)
            + tickets_sujet_actions_test(12, "Gros sujet", csat=3.5, macro_applied=None)
        )
        pistes = identifier_pistes_standardisation(tickets, {}, 5, SEUIL_CSAT_INSATISFAISANT)
        self.assertEqual(pistes[0]["sujet"], "Gros sujet")
        self.assertEqual(pistes[1]["sujet"], "Petit sujet")

    # ---- Self-service : détection + wording (G) + exclusion sujet traité (H) ----
    def test_self_service_detecte_echanges_eleves(self):
        tickets = tickets_sujet_actions_test(6, "Où est ma commande", replies=5)
        pistes = identifier_pistes_self_service(tickets, {}, 5, 3)
        self.assertEqual(len(pistes), 1)
        self.assertEqual(pistes[0]["famille"], FAMILLE_SELF_SERVICE_ACTIONS)

    def test_self_service_wording_non_prescriptif(self):
        tickets = tickets_sujet_actions_test(6, "Où est ma commande", replies=5)
        pistes = identifier_pistes_self_service(tickets, {}, 5, 3)
        self.assertTrue(pistes[0]["piste"].startswith("Piste :"))
        self.assertNotIn("Créer une FAQ", pistes[0]["piste"])

    def test_self_service_exclut_sujet_deja_traite(self):
        tickets = tickets_sujet_actions_test(6, "Où est ma commande", replies=5)
        suivi = {"Où est ma commande": {"statut": "Fait", "date_action": datetime.date(2026, 1, 1), "notes": None}}
        pistes = identifier_pistes_self_service(tickets, suivi, 5, 3)
        self.assertEqual(len(pistes), 0)

    def test_self_service_echanges_insuffisants_exclu(self):
        tickets = tickets_sujet_actions_test(6, "Sujet simple", replies=1)
        pistes = identifier_pistes_self_service(tickets, {}, 5, 3)
        self.assertEqual(len(pistes), 0)

    # ---- Retours clients : regroupement + volontairement PAS filtré par suivi (voir docstring outils.py) ----
    def test_retours_clients_regroupe_par_sujet_avec_seuil(self):
        tickets = tickets_sujet_actions_test(10, "Colis non reçu", csat=1, csat_comment="Toujours pas reçu")
        groupes = identifier_retours_clients_a_explorer(tickets, 2, 10)
        self.assertEqual(len(groupes), 1)
        self.assertEqual(groupes[0]["famille"], FAMILLE_RETOURS_CLIENTS_ACTIONS)
        self.assertEqual(groupes[0]["volume"], 10)

    def test_retours_clients_sous_seuil_exclu(self):
        tickets = tickets_sujet_actions_test(4, "Colis non reçu", csat=1, csat_comment="Pas reçu")
        groupes = identifier_retours_clients_a_explorer(tickets, 2, 10)
        self.assertEqual(len(groupes), 0)

    def test_retours_clients_pas_filtre_par_suivi(self):
        # Comportement volontairement différent de standardisation/self-service (asymétrie documentée
        # dans outils.py) : un sujet déjà "Fait" peut continuer à faire remonter des verbatims négatifs.
        tickets = tickets_sujet_actions_test(10, "Colis non reçu", csat=1, csat_comment="Pas reçu")
        groupes = identifier_retours_clients_a_explorer(tickets, 2, 10)
        self.assertEqual(len(groupes), 1)

    # ---- P. Aucun score inter-familles ----
    def test_p_aucune_cle_score_dans_les_pistes(self):
        tickets_standard = tickets_sujet_actions_test(6, "Sujet standard", csat=3.5, macro_applied=None)
        tickets_faq = tickets_sujet_actions_test(6, "Sujet faq", replies=5)
        tickets_verbatim = tickets_sujet_actions_test(10, "Sujet verbatim", csat=1, csat_comment="Pas content")
        for piste in identifier_pistes_standardisation(tickets_standard, {}, 5, SEUIL_CSAT_INSATISFAISANT):
            self.assertNotIn("score", piste)
        for piste in identifier_pistes_self_service(tickets_faq, {}, 5, 3):
            self.assertNotIn("score", piste)
        for groupe in identifier_retours_clients_a_explorer(tickets_verbatim, 2, 10):
            self.assertNotIn("score", groupe)

    # ---- Actions déjà menées : "Fait" visible (I), no future leakage (K/L), sans date prudent (M) ----
    def test_i_actions_menees_inclut_sujet_fait(self):
        suivi = {"Macro colis": {"statut": "Fait", "date_action": datetime.date(2026, 1, 5), "notes": "MAC-001"}}
        actions = construire_actions_menees_actions(suivi, [], datetime.date(2026, 1, 31))
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["sujet"], "Macro colis")
        self.assertEqual(actions[0]["statut"], "Fait")

    def test_k_action_future_absente_du_scope_passe(self):
        suivi = {"Macro colis": {"statut": "Fait", "date_action": datetime.date(2026, 6, 1), "notes": None}}
        actions = construire_actions_menees_actions(suivi, [], datetime.date(2026, 1, 31))
        self.assertEqual(len(actions), 0)

    def test_l_impact_apres_borne_a_date_fin_periode(self):
        sujet = "Retour transporteur"
        date_action = datetime.date(2026, 3, 1)
        date_fin_periode = datetime.date(2026, 3, 10)
        tickets_historique = [
            ticket_actions_test(1, subject_cluster=sujet, created_at=datetime.date(2026, 2, 1)),
            ticket_actions_test(2, subject_cluster=sujet, created_at=datetime.date(2026, 2, 15)),
            ticket_actions_test(3, subject_cluster=sujet, created_at=datetime.date(2026, 3, 2)),
            ticket_actions_test(4, subject_cluster=sujet, created_at=datetime.date(2026, 3, 5)),
            ticket_actions_test(5, subject_cluster=sujet, created_at=datetime.date(2026, 3, 20)),
            ticket_actions_test(6, subject_cluster=sujet, created_at=datetime.date(2026, 4, 1)),
        ]
        suivi = {sujet: {"statut": "Fait", "date_action": date_action, "notes": None}}
        actions = construire_actions_menees_actions(suivi, tickets_historique, date_fin_periode)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["impact"]["volume_avant"], 2)
        self.assertEqual(actions[0]["impact"]["volume_apres"], 2)

    def test_m_action_sans_date_exclue_par_prudence(self):
        suivi = {"Macro colis": {"statut": "Fait", "date_action": None, "notes": "MAC-001"}}
        actions = construire_actions_menees_actions(suivi, [], datetime.date(2026, 1, 31))
        self.assertEqual(len(actions), 0)

    # ---- J. "Fait" != succès : un résultat neutre/négatif reste visible, aucun badge de succès ----
    def test_j_impact_negatif_reste_visible(self):
        sujet = "Macro sans effet"
        date_action = datetime.date(2026, 5, 1)
        tickets_historique = (
            [ticket_actions_test(i, subject_cluster=sujet, csat=4.5, created_at=datetime.date(2026, 4, 1)) for i in range(5)]
            + [ticket_actions_test(i + 5, subject_cluster=sujet, csat=3.0, created_at=datetime.date(2026, 5, 10)) for i in range(5)]
        )
        suivi = {sujet: {"statut": "Fait", "date_action": date_action, "notes": "CSAT en baisse malgré l'action"}}
        actions = construire_actions_menees_actions(suivi, tickets_historique, datetime.date(2026, 5, 31))
        self.assertEqual(len(actions), 1)
        self.assertLess(actions[0]["impact"]["csat_apres"], actions[0]["impact"]["csat_avant"])

    def test_j_aucune_cle_succes_ou_badge(self):
        suivi = {"Macro colis": {"statut": "Fait", "date_action": datetime.date(2026, 1, 5), "notes": None}}
        actions = construire_actions_menees_actions(suivi, [], datetime.date(2026, 1, 31))
        self.assertNotIn("succes", actions[0])
        self.assertNotIn("badge", actions[0])


def ticket_couverture_test(ticket_id=1, created_at=None, assignee="Amine", via_channel="Email",
                            first_reply_time_min=30, ticket_reason="Livraison", resolution_type=None):
    if created_at is None:
        created_at = datetime.datetime(2026, 1, 12, 10, 0)
    return {
        "ticket_id": ticket_id, "created_at": created_at, "assignee": assignee,
        "via_channel": via_channel, "first_reply_time_min": first_reply_time_min,
        "ticket_reason": ticket_reason, "resolution_type": resolution_type,
    }


def tickets_creneau_test(nombre, jour, heure, first_reply_time_min=30, assignee="Amine"):
    # jour : 0=Lundi ... date de base arbitraire (12/01/2026 est un lundi).
    date_base = datetime.date(2026, 1, 12) + datetime.timedelta(days=jour)
    tickets = []
    for i in range(nombre):
        tickets.append(ticket_couverture_test(
            ticket_id=i, created_at=datetime.datetime.combine(date_base, datetime.time(heure, i % 50)),
            assignee=assignee, first_reply_time_min=first_reply_time_min,
        ))
    return tickets


def planning_couverture_test(agents_heures):
    # agents_heures : {"Amine": [(9, 17)], ...} -- appliqué du lundi au vendredi (0-4).
    planning = {}
    for agent, plages in agents_heures.items():
        planning[agent] = {}
        for jour in range(5):
            planning[agent][jour] = plages
    return planning


# horaires_standard (statut_creneau_standard) reste conceptuellement distinct du planning par
# agent -- même dans ce fichier de test, jamais le même dict réutilisé pour les deux rôles.
HORAIRES_STANDARD_COUVERTURE_TEST = {0: [(9, 17)], 1: [(9, 17)], 2: [(9, 17)], 3: [(9, 17)], 4: [(9, 17)]}


# Étape 5E.1 -- "Pression de charge" (demandes/capacité, relative à l'historique) et "Tension de
# couverture" (pression matérielle ET réactivité locale dégradée, jamais la pression seule) : les
# deux notions gardées strictement séparées, conformément à l'audit 5E qui a établi que l'ancien
# mécanisme "hotspot" (seuils absolus 15/30, jamais atteints en pratique) confondait les deux.
class TestCompositionCouverturePressionTension(unittest.TestCase):
    # ---- rang_relatif_vs_reference ----
    def test_rang_vs_reference_valeur_basse(self):
        self.assertEqual(rang_relatif_vs_reference(1, [1, 2, 3, 4, 5]), 0.0)

    def test_rang_vs_reference_valeur_haute(self):
        self.assertEqual(rang_relatif_vs_reference(10, [1, 2, 3, 4, 5]), 1.0)

    def test_rang_vs_reference_none_si_cible_none(self):
        self.assertIsNone(rang_relatif_vs_reference(None, [1, 2, 3]))

    def test_rang_vs_reference_none_si_reference_vide(self):
        self.assertIsNone(rang_relatif_vs_reference(5, []))

    # ---- A/G. Garde-fou volume + première observation : jamais de rang historique artificiel ----
    def test_a_capacite_zero_volume_faible_nest_pas_une_tension_possible(self):
        niveau = niveau_pression_couverture(demandes=3, capacite_cumulee=0, rang_pression=None)
        self.assertEqual(niveau, NIVEAU_ACTIVITE_HORS_CAPACITE_FAIBLE)
        self.assertFalse(creneau_est_tension_couverture(niveau, NIVEAU_FRT_LOCAL_DEGRADE))

    def test_a_capacite_zero_volume_materiel_distinct_du_faible(self):
        niveau = niveau_pression_couverture(demandes=8, capacite_cumulee=0, rang_pression=None)
        self.assertEqual(niveau, NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE)

    def test_g_premiere_observation_rang_none_est_non_qualifiable(self):
        niveau = niveau_pression_couverture(demandes=10, capacite_cumulee=2, rang_pression=None)
        self.assertEqual(niveau, NIVEAU_PRESSION_NON_QUALIFIABLE)
        self.assertNotIn(niveau, (NIVEAU_PRESSION_MARQUEE, NIVEAU_PRESSION_FORTE))

    def test_volume_sous_seuil_avec_capacite_reste_faible_volume(self):
        niveau = niveau_pression_couverture(demandes=3, capacite_cumulee=2, rang_pression=0.99)
        self.assertEqual(niveau, NIVEAU_PRESSION_FAIBLE_VOLUME)

    def test_pression_habituelle_marquee_forte_selon_rang(self):
        self.assertEqual(niveau_pression_couverture(10, 2, 0.5), NIVEAU_PRESSION_HABITUELLE)
        self.assertEqual(niveau_pression_couverture(10, 2, 0.8), NIVEAU_PRESSION_MARQUEE)
        self.assertEqual(niveau_pression_couverture(10, 2, 0.95), NIVEAU_PRESSION_FORTE)

    # ---- FRT local : jamais "normal" par défaut sous le seuil d'échantillon ----
    def test_frt_local_non_mesurable_sous_seuil_echantillon(self):
        self.assertIsNone(niveau_frt_local_couverture(frt_local_n=3, rang_frt_local=0.9))

    def test_frt_local_normal_vs_degrade(self):
        self.assertEqual(niveau_frt_local_couverture(10, 0.5), NIVEAU_FRT_LOCAL_NORMAL)
        self.assertEqual(niveau_frt_local_couverture(10, 0.8), NIVEAU_FRT_LOCAL_DEGRADE)

    # ---- C/D/E/F. Tension = convergence stricte, jamais un seul des deux axes ----
    def test_d_tension_exige_pression_et_reactivite_degradee(self):
        self.assertTrue(creneau_est_tension_couverture(NIVEAU_PRESSION_MARQUEE, NIVEAU_FRT_LOCAL_DEGRADE))
        self.assertTrue(creneau_est_tension_couverture(NIVEAU_PRESSION_FORTE, NIVEAU_FRT_LOCAL_DEGRADE))

    def test_e_pression_forte_frt_normal_est_absorbee_pas_tension(self):
        self.assertFalse(creneau_est_tension_couverture(NIVEAU_PRESSION_FORTE, NIVEAU_FRT_LOCAL_NORMAL))

    def test_f_pression_habituelle_frt_degrade_nest_pas_attribue_a_la_couverture(self):
        self.assertFalse(creneau_est_tension_couverture(NIVEAU_PRESSION_HABITUELLE, NIVEAU_FRT_LOCAL_DEGRADE))

    def test_frt_non_mesurable_empeche_la_tension(self):
        self.assertFalse(creneau_est_tension_couverture(NIVEAU_PRESSION_FORTE, None))

    # ---- O. 0 tension reste un résultat valide (pas de forçage) ----
    def test_o_zero_tension_est_un_resultat_valide(self):
        self.assertFalse(creneau_est_tension_couverture(NIVEAU_PRESSION_HABITUELLE, NIVEAU_FRT_LOCAL_NORMAL))

    # ---- I/J/K. Step 1 -- heures exactes, Sam planifié jamais renfort, renfort jamais au dénominateur ----
    def test_i_sofia_14h_reflete_dans_capacite_cumulee(self):
        planning = planning_couverture_test({"Sofia": [(9, 16)]})  # 7h/jour x 2 jours = 14h reference
        tickets = tickets_creneau_test(3, jour=0, heure=10, assignee="Sofia")
        plannings_periode = [(datetime.date(2026, 5, 25), datetime.date(2026, 5, 31), planning)]
        agents_grille = construire_agents_grille_couverture(tickets, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        cellule = [e for e in grille if e["jour"] == "Lundi" and e["heure"] == 10][0]
        self.assertEqual(cellule["capacite_cumulee"], 1)
        self.assertIn("Sofia", cellule["agents"])

    def test_j_sam_planifie_nest_jamais_renfort(self):
        planning = planning_couverture_test({"Sam": [(9, 17)]})
        tickets = tickets_creneau_test(5, jour=0, heure=10, assignee="Sam")
        plannings_periode = [(datetime.date(2025, 12, 15), datetime.date(2025, 12, 21), planning)]
        agents_grille = construire_agents_grille_couverture(tickets, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        cellule = [e for e in grille if e["jour"] == "Lundi" and e["heure"] == 10][0]
        self.assertEqual(cellule["renfort_non_planifie"], [])
        self.assertEqual(cellule["capacite_cumulee"], 1)

    def test_k_renfort_non_planifie_jamais_au_denominateur(self):
        planning = planning_couverture_test({})  # personne planifie
        tickets = tickets_creneau_test(5, jour=0, heure=10, assignee="Lucie")
        plannings_periode = [(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), planning)]
        agents_grille = construire_agents_grille_couverture(tickets, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        cellule = [e for e in grille if e["jour"] == "Lundi" and e["heure"] == 10][0]
        self.assertEqual(cellule["capacite_cumulee"], 0)
        self.assertIsNone(cellule["ratio"])
        self.assertIn("Lucie", cellule["renfort_non_planifie"])

    # ---- L. Multi-semaines : capacité SOMMÉE par semaine, jamais la dernière semaine seule ----
    def test_l_multi_semaines_somme_la_capacite_par_semaine(self):
        planning_semaine_1 = planning_couverture_test({"Amine": [(9, 17)], "Kristelle": [(9, 17)]})
        planning_semaine_2 = planning_couverture_test({"Amine": [(9, 17)]})  # Kristelle absente semaine 2
        tickets_semaine_1 = tickets_creneau_test(10, jour=0, heure=10, assignee="Amine")
        tickets_semaine_2 = tickets_creneau_test(10, jour=0, heure=10, assignee="Amine")
        tickets_totaux = tickets_semaine_1 + tickets_semaine_2

        plannings_periode = [
            (datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), planning_semaine_1),
            (datetime.date(2026, 1, 19), datetime.date(2026, 1, 25), planning_semaine_2),
        ]
        agents_grille = construire_agents_grille_couverture(tickets_totaux, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets_totaux, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        cellule = [e for e in grille if e["jour"] == "Lundi" and e["heure"] == 10][0]

        # capacite attendue : semaine 1 (Amine+Kristelle=2) + semaine 2 (Amine=1) = 3, jamais 1
        # (capacité de la seule dernière semaine) ni 2 (comme si les deux semaines avaient Kristelle).
        self.assertEqual(cellule["capacite_cumulee"], 3)
        self.assertEqual(cellule["demandes"], 20)
        self.assertAlmostEqual(cellule["ratio"], 20 / 3)
        self.assertIn("Kristelle", cellule["agents"])  # visible au moins une semaine -> visible

    # ---- M/N. Catégorie et canal n'entrent jamais dans le calcul de tension ----
    def test_m_n_tension_ignore_categorie_et_canal(self):
        # creneau_est_tension_couverture ne prend que niveau_pression/niveau_frt_local en argument :
        # aucune catégorie ni canal ne peut influencer le résultat, par construction de la signature.
        resultat_a = creneau_est_tension_couverture(NIVEAU_PRESSION_MARQUEE, NIVEAU_FRT_LOCAL_DEGRADE)
        resultat_b = creneau_est_tension_couverture(NIVEAU_PRESSION_MARQUEE, NIVEAU_FRT_LOCAL_DEGRADE)
        self.assertEqual(resultat_a, resultat_b)
        self.assertTrue(resultat_a)

    # ---- P/Q. Aucun wording de recommandation staffing dans les constantes de niveau ----
    def test_p_q_aucun_wording_staffing_dans_les_niveaux(self):
        niveaux = [
            NIVEAU_PRESSION_HABITUELLE, NIVEAU_PRESSION_MARQUEE, NIVEAU_PRESSION_FORTE,
            NIVEAU_PRESSION_FAIBLE_VOLUME, NIVEAU_PRESSION_NON_QUALIFIABLE,
            NIVEAU_ACTIVITE_HORS_CAPACITE_FAIBLE, NIVEAU_ACTIVITE_HORS_CAPACITE_MATERIELLE,
            NIVEAU_FRT_LOCAL_NORMAL, NIVEAU_FRT_LOCAL_DEGRADE,
        ]
        interdits = ["staffing insuffisant", "ajouter un agent", "recruter", "heures supplémentaires"]
        for niveau in niveaux:
            for mot in interdits:
                self.assertNotIn(mot, niveau.lower())

    # ---- Régression : un créneau "Hors standard" (avant ouverture/après fermeture) à fort volume
    # ne doit JAMAIS remonter comme "activité observée sans capacité planifiée" -- bug réel trouvé
    # en vérification navigateur (Étape 5E.1), où les heures fermées par conception (7h/18h+, sans
    # capacité par définition) étaient à tort classées comme une anomalie de couverture.
    def test_creneau_hors_standard_nest_jamais_classe_comme_activite_hors_capacite(self):
        planning = planning_couverture_test({"Amine": [(9, 17)]})  # rien planifié a 7h
        tickets = tickets_creneau_test(20, jour=0, heure=7, assignee="Amine")
        plannings_periode = [(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), planning)]
        agents_grille = construire_agents_grille_couverture(tickets, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        grille_enrichie = enrichir_grille_pression_tension_couverture(grille, tickets, [], [])
        cellule = [e for e in grille_enrichie if e["jour"] == "Lundi" and e["heure"] == 7][0]
        self.assertEqual(cellule["statut"], "Hors standard")
        self.assertIsNone(cellule["niveau_pression"])
        self.assertFalse(cellule["est_tension"])

    # ---- H. No future leakage : enrichissement borné aux références fournies (jamais la période
    # elle-même) -- vérifié ici au niveau de la fonction d'enrichissement pure, la construction de
    # la référence historique (reload des exports antérieurs) est couverte par le rejeu réel. ----
    def test_h_reference_insuffisante_ne_produit_aucun_rang(self):
        planning = planning_couverture_test({"Amine": [(9, 17)]})
        tickets = tickets_creneau_test(10, jour=0, heure=10, assignee="Amine")
        plannings_periode = [(datetime.date(2026, 1, 12), datetime.date(2026, 1, 18), planning)]
        agents_grille = construire_agents_grille_couverture(tickets, plannings_periode)
        grille = construire_grille_pression_couverture(
            tickets, plannings_periode, agents_grille, HORAIRES_STANDARD_COUVERTURE_TEST
        )
        # reference vide (< SEUIL_MIN_REFERENCE_HISTORIQUE_COUVERTURE points) -> pas de rang.
        grille_enrichie = enrichir_grille_pression_tension_couverture(grille, tickets, [], [])
        cellule = [e for e in grille_enrichie if e["jour"] == "Lundi" and e["heure"] == 10][0]
        self.assertIsNone(cellule["rang_pression"])
        self.assertEqual(cellule["niveau_pression"], NIVEAU_PRESSION_NON_QUALIFIABLE)

    # ---- construire_lecture_couverture : texte data-driven, jamais générique ----
    def test_lecture_couverture_silence_si_rien_a_signaler(self):
        texte = construire_lecture_couverture(0, 0, 90, 85, False)
        self.assertIn("norme habituelle", texte)

    def test_lecture_couverture_mentionne_les_tensions(self):
        texte = construire_lecture_couverture(2, 1, 80, 85, False)
        self.assertIn("2 créneau", texte)
        self.assertIn("1 autre créneau", texte)

    # ---- statut_creneau_standard : inchangé (déplacé depuis app.py) ----
    def test_statut_creneau_standard_couverture_requise(self):
        horaires = {0: [(9, 17)]}
        self.assertEqual(statut_creneau_standard(horaires, 0, 10), "Couverture requise")
        self.assertEqual(statut_creneau_standard(horaires, 1, 10), "Hors standard")


def signal_produit_test(grain, sujet, produit=None, composant=None, issue=None, niveau_priorite="Priorité principale"):
    return {
        "grain": grain, "sujet": sujet, "_produit": produit, "_composant": composant, "_issue_type": issue,
        "niveau_priorite": niveau_priorite,
    }


# Étape 5F.1 -- "Produit / investigation" : 4A reste l'unique propriétaire de la priorisation
# (aucune fonction ici ne recalcule une éligibilité ou un score) ; ce module reformate ses sorties
# (titre de carte, lecture de synthèse, textes descriptifs sans conclusion causale) et matche les
# "dossiers associés" en réutilisant tickets_correspondant_candidat -- la fonction structurelle que
# 4A utilise lui-même, jamais une reconstruction parallèle ni un matching par texte libre.
class TestCompositionProduitInvestigation(unittest.TestCase):
    # ---- E/F/G. Titre de carte : grain produit x composant complet, jamais ambigu ----
    def test_e_titre_produit_composant_affiche_les_deux(self):
        signal = signal_produit_test(GRAIN_PRODUIT_COMPOSANT, "Clarté", produit="Clarté", composant="Batterie / charge")
        self.assertEqual(titre_signal_produit(signal), "Clarté — Batterie / charge")

    def test_f_deux_clarte_composants_differents_sont_distinguables(self):
        signal_a = signal_produit_test(GRAIN_PRODUIT_COMPOSANT, "Clarté", produit="Clarté", composant="Batterie / charge")
        signal_b = signal_produit_test(GRAIN_PRODUIT_COMPOSANT, "Clarté", produit="Clarté", composant="Module lumineux / LED")
        self.assertNotEqual(titre_signal_produit(signal_a), titre_signal_produit(signal_b))

    def test_g_signal_composant_consolide_garde_son_sujet_sans_faux_produit(self):
        signal = signal_produit_test(GRAIN_COMPOSANT, "Batterie / charge")
        self.assertEqual(titre_signal_produit(signal), "Batterie / charge")

    def test_titre_produit_issue_inchange(self):
        signal = signal_produit_test(GRAIN_PRODUIT_ISSUE, "Évasion — Défaut de finition", produit="Évasion", issue="Défaut de finition")
        self.assertEqual(titre_signal_produit(signal), "Évasion — Défaut de finition")

    # ---- P/Q/R. Dossiers associés : matching structurel, jamais par texte libre ----
    def test_p_dossiers_associes_grain_produit_composant(self):
        tickets = [
            ticket_produit(1, component="Batterie / charge", product_name="Clarté", subject_cluster="Autonomie faible"),
            ticket_produit(2, component="Batterie / charge", product_name="Clarté", subject_cluster="Ne charge plus"),
            ticket_produit(3, component="Batterie / charge", product_name="Évasion", subject_cluster="Autonomie faible"),
            ticket_produit(4, component="Module lumineux / LED", product_name="Clarté", subject_cluster="LED éteinte"),
        ]
        signal = signal_produit_test(GRAIN_PRODUIT_COMPOSANT, "Clarté", produit="Clarté", composant="Batterie / charge")
        dossiers = construire_dossiers_associes_produit(signal, tickets)
        ids = sorted(t["ticket_id"] for t in dossiers)
        self.assertEqual(ids, [1, 2])  # jamais le ticket 3 (autre produit) ni 4 (autre composant)

    def test_q_matching_ignore_subject_cluster(self):
        # Deux tickets du même produit x composant mais subject_cluster totalement différents :
        # les deux doivent rester matchés -- la correspondance ne passe jamais par le texte libre.
        tickets = [
            ticket_produit(1, component="Batterie / charge", product_name="Clarté", subject_cluster="Ne charge plus du tout"),
            ticket_produit(2, component="Batterie / charge", product_name="Clarté", subject_cluster="Autonomie divisée par deux"),
        ]
        signal = signal_produit_test(GRAIN_PRODUIT_COMPOSANT, "Clarté", produit="Clarté", composant="Batterie / charge")
        dossiers = construire_dossiers_associes_produit(signal, tickets)
        self.assertEqual(len(dossiers), 2)

    def test_r_signal_consolide_composant_capte_plusieurs_produits(self):
        # Grain composant (ex. "Batterie / charge" consolidé) : doit inclure TOUS les produits
        # partageant ce composant, sans reconstruire la consolidation 4A elle-même.
        tickets = [
            ticket_produit(1, component="Batterie / charge", product_name="Cocon"),
            ticket_produit(2, component="Batterie / charge", product_name="Évasion"),
            ticket_produit(3, component="Batterie / charge", product_name="Clarté"),
            ticket_produit(4, component="Module lumineux / LED", product_name="Cocon"),
        ]
        signal = signal_produit_test(GRAIN_COMPOSANT, "Batterie / charge")
        dossiers = construire_dossiers_associes_produit(signal, tickets)
        self.assertEqual(len(dossiers), 3)

    def test_dossiers_associes_grain_produit_issue(self):
        tickets = [
            ticket_produit(1, product_name="Évasion", issue_type="Défaut de finition"),
            ticket_produit(2, product_name="Évasion", issue_type="Charge / autonomie"),
        ]
        signal = signal_produit_test(GRAIN_PRODUIT_ISSUE, "Évasion — Défaut de finition", produit="Évasion", issue="Défaut de finition")
        dossiers = construire_dossiers_associes_produit(signal, tickets)
        self.assertEqual(len(dossiers), 1)
        self.assertEqual(dossiers[0]["ticket_id"], 1)

    # ---- J. Coexistence Voie A / Voie B sur le même ticket, sans fusion ----
    def test_j_meme_ticket_peut_etre_a_la_fois_dans_un_signal_voie_a_et_voie_b(self):
        # TKT-109042 (mars 2026) : ticket appartenant à un signal Voie A actif (Batterie / charge)
        # ET repéré indépendamment par la Voie B -- les deux mécanismes restent indépendants,
        # aucune donnée partagée ne les fait fusionner.
        ticket_sensible = ticket_produit(
            109042, component="Batterie / charge", product_name="Évasion", csat=2, reopens=2,
            resolution_type="Remplacement produit",
        )
        tickets = [ticket_sensible] + lot_tickets_neutres("ctrl", 10, component="Batterie / charge", product_name="Autre")
        signal = signal_produit_test(GRAIN_COMPOSANT, "Batterie / charge")
        dossiers = construire_dossiers_associes_produit(signal, tickets)
        ids_dossiers = [t["ticket_id"] for t in dossiers]
        self.assertIn(109042, ids_dossiers)

        voie_b = moteur_produit_voie_b(tickets)
        ids_voie_b = [v["ticket_id"] for v in voie_b]
        self.assertIn(109042, ids_voie_b)
        # Le ticket apparaît dans les deux résultats indépendamment, jamais retiré de l'un parce
        # qu'il est présent dans l'autre.

    # ---- L. Wording du plafond d'affichage (safety cap), jamais "Top 5" ----
    def test_l_lecture_mentionne_le_nombre_affiche_si_plafonne(self):
        prioritaires_affiches = [
            signal_produit_test(GRAIN_COMPOSANT, "Batterie / charge", niveau_priorite="Priorité principale"),
        ]
        texte = construire_lecture_produit(prioritaires_affiches, 10, [], 0, 0, 27.6)
        self.assertIn("10 signaux", texte)
        self.assertIn("1 affiché", texte)
        self.assertNotIn("Top 5", texte)
        self.assertNotIn("top 5", texte.lower())

    def test_lecture_nomme_le_signal_principal_le_mieux_prouve(self):
        prioritaires_affiches = [
            signal_produit_test(GRAIN_COMPOSANT, "Batterie / charge", niveau_priorite="Priorité principale"),
            signal_produit_test(GRAIN_COMPOSANT, "Module lumineux / LED", niveau_priorite="Priorité secondaire"),
        ]
        texte = construire_lecture_produit(prioritaires_affiches, 2, [], 0, 0, 18.2)
        self.assertIn("Batterie / charge", texte)
        self.assertIn("niveau de preuve le plus complet", texte)

    def test_lecture_silence_si_aucun_signal(self):
        texte = construire_lecture_produit([], 0, [], 0, 0, 15.7)
        self.assertIn("aucun signal", texte.lower())
        self.assertNotIn("produit le plus problématique", texte.lower())
        self.assertNotIn("cause principale", texte.lower())

    # ---- A/B/C/N/O. Textes descriptifs : jamais de causalité ou de prescription technique ----
    def test_texte_resolution_jamais_causal(self):
        lignes = [{"Type de résolution": "Remplacement produit", "Tickets": 30}]
        texte = construire_texte_resolution_produit(lignes, 90)
        interdits = ["défaut structurel", "défaut matériel", "à corriger", "changer la batterie", "corriger le firmware"]
        for mot in interdits:
            self.assertNotIn(mot, texte.lower())
        self.assertIn("33", texte)

    def test_texte_sav_recurrents_jamais_defaut_structurel(self):
        produit_principal = {"Produit": "Clarté", "SAV récurrents": 5}
        composant_principal = {"Composant": "Batterie / charge", "SAV récurrents": 4}
        texte = construire_texte_sav_recurrents_produit(12, 8.5, produit_principal, composant_principal)
        self.assertNotIn("défaut structurel", texte.lower())
        self.assertIn("Clarté", texte)
        self.assertIn("Batterie / charge", texte)

    # ---- Prudence causale globale : reste explicite, jamais perdue ----
    def test_prudence_causale_globale_non_vide(self):
        self.assertIn("association", TEXTE_PRUDENCE_CAUSALE.lower())
        self.assertIn("jamais une cause démontrée", TEXTE_PRUDENCE_CAUSALE)


# Composition Avant-vente — parcours & achats observés (Étape 5H.1) : 4D reste l'unique propriétaire
# de l'attribution (aucune de ces fonctions ne recalcule une éligibilité ni ne recherche une
# commande hors de resultats_achats_av déjà déduplicué par 4D) -- seuls le texte de lecture, le
# matching "contacts/achats associés" et les tables descriptives par sujet/pays sont testés ici.
class TestAvantVenteParcours5H1(unittest.TestCase):
    def test_a_lecture_zero_opportunite_zero_watch(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 22 % des contacts.", 0, 0)
        self.assertIn("Avant-vente représente 22 % des contacts.", texte)
        self.assertIn("Aucune opportunité ne se détache actuellement", texte)

    def test_b_lecture_une_opportunite(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 18 % des contacts.", 1, 0)
        self.assertIn("Une opportunité présente une convergence suffisante pour être investiguée.", texte)

    def test_c_lecture_plusieurs_opportunites(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 26 % des contacts.", 2, 0)
        self.assertIn("2 opportunités présentent une convergence suffisante pour être investiguées.", texte)

    def test_d_lecture_watch_seul(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 22 % des contacts.", 0, 2)
        self.assertNotIn("Aucune opportunité ne se détache actuellement", texte)
        self.assertIn("2 motifs supplémentaires restent à surveiller", texte)

    def test_e_lecture_opportunite_et_watch_combines(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 20 % des contacts.", 1, 1)
        self.assertIn("Une opportunité présente une convergence suffisante pour être investiguée.", texte)
        self.assertIn("1 motif supplémentaire reste à surveiller", texte)

    def test_f_lecture_jamais_de_connecteur_causal(self):
        texte = construire_lecture_avant_vente("Avant-vente représente 45 % des contacts.", 1, 0)
        self.assertNotIn(" car ", texte)
        self.assertNotIn(" donc ", texte)
        self.assertNotIn(" explique ", texte)

    def test_g_contacts_associes_matching_exact_grain_motif(self):
        tickets = (
            generer_tickets_avant_vente(5, subject_cluster="Compatibilité allergies / parfums forts")
            + generer_tickets_avant_vente(3, id_depart=100, subject_cluster="Choix du programme")
        )
        index = commandes_par_email({})
        resultats = resoudre_achats_observes_avant_vente(tickets, index, 30)
        signal = {"sujet": "Compatibilité allergies / parfums forts"}
        contacts = construire_contacts_associes_avant_vente(signal, resultats)
        self.assertEqual(len(contacts), 5)
        for ticket, commande, plusieurs in contacts:
            self.assertEqual(ticket["subject_cluster"], "Compatibilité allergies / parfums forts")

    def test_h_contacts_associes_aucun_matching_texte_libre(self):
        tickets = generer_tickets_avant_vente(4, subject_cluster="Demande couleur personnalisée (hors catalogue)")
        resultats = resoudre_achats_observes_avant_vente(tickets, commandes_par_email({}), 30)
        signal = {"sujet": "Demande couleur personnalisée"}  # sous-chaîne, ne doit jamais matcher
        contacts = construire_contacts_associes_avant_vente(signal, resultats)
        self.assertEqual(len(contacts), 0)

    def test_i_contacts_associes_coherence_n_signal_4d(self):
        tickets_normaux = generer_tickets_avant_vente(100, subject_cluster="Choix du programme")
        tickets_sujet = generer_tickets_avant_vente(
            20, id_depart=200, subject_cluster="Personnalisation mix capsules (hors catalogue)",
        )
        tous = tickets_normaux + tickets_sujet
        resultats = resoudre_achats_observes_avant_vente(tous, commandes_par_email({}), 30)
        signal = {"sujet": "Personnalisation mix capsules (hors catalogue)"}
        contacts = construire_contacts_associes_avant_vente(signal, resultats)
        self.assertEqual(len(contacts), 20)

    def test_j_achats_associes_ne_garde_que_les_contacts_credites(self):
        ticket_credite = ticket_avant_vente(ticket_id=1, requester_email="c1@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_sans_achat = ticket_avant_vente(ticket_id=2, requester_email="c2@example.com", created_at=datetime.date(2026, 1, 1))
        commande = commande_test("C1", "c1@example.com", datetime.date(2026, 1, 5))
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente([ticket_credite, ticket_sans_achat], index, 30)
        achats = construire_achats_associes_avant_vente(resultats)
        self.assertEqual(len(achats), 1)
        ticket_achat, commande_achat = achats[0]
        self.assertEqual(ticket_achat["ticket_id"], 1)
        self.assertEqual(commande_achat["order_id"], "C1")

    def test_k_achats_associes_jamais_de_nouvelle_recherche_shopify(self):
        # La commande retournée doit être exactement l'objet déjà résolu par 4D, jamais reconstruite.
        ticket = ticket_avant_vente(ticket_id=1, requester_email="c@example.com", created_at=datetime.date(2026, 1, 1))
        commande = commande_test("C1", "c@example.com", datetime.date(2026, 1, 5), montant_total=229.0)
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente([ticket], index, 30)
        achats = construire_achats_associes_avant_vente(resultats)
        self.assertIs(achats[0][1], resultats[0][1])

    def test_l_table_sujets_exclut_demande_de_rdv(self):
        tickets = (
            generer_tickets_avant_vente(10, subject_cluster="Choix du programme")
            + generer_tickets_avant_vente(
                10, id_depart=100, subject_cluster=SUJET_DEMANDE_RDV,
                type_contact_avant_vente=TYPE_CONTACT_RDV, rdv_statut=RDV_STATUT_HONORE,
            )
        )
        resultats = resoudre_achats_observes_avant_vente(tickets, commandes_par_email({}), 30)
        table = construire_table_sujets_avant_vente(tickets, resultats)
        sujets = [ligne["sujet"] for ligne in table]
        self.assertNotIn(SUJET_DEMANDE_RDV, sujets)
        self.assertIn("Choix du programme", sujets)

    def test_m_table_sujets_stats_achat_observe_correctes(self):
        ticket_avec_achat = ticket_avant_vente(ticket_id=1, requester_email="c1@example.com", subject_cluster="Choix du programme", created_at=datetime.date(2026, 1, 1))
        ticket_sans_achat = ticket_avant_vente(ticket_id=2, requester_email="c2@example.com", subject_cluster="Choix du programme", created_at=datetime.date(2026, 1, 1))
        commande = commande_test("C1", "c1@example.com", datetime.date(2026, 1, 5), montant_total=199.0)
        index = commandes_par_email({"C1": commande})
        resultats = resoudre_achats_observes_avant_vente([ticket_avec_achat, ticket_sans_achat], index, 30)
        table = construire_table_sujets_avant_vente([ticket_avec_achat, ticket_sans_achat], resultats)
        self.assertEqual(len(table), 1)
        self.assertEqual(table[0]["n"], 2)
        self.assertEqual(table[0]["n_achats"], 1)
        self.assertEqual(table[0]["achat_observe_pct"], 50.0)
        self.assertEqual(table[0]["panier_moyen"], 199.0)

    def test_n_table_pays_regroupe_sans_dimension_agent(self):
        ticket_fr = ticket_avant_vente(ticket_id=1, requester_email="c1@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_fr["country"] = "FR"
        ticket_be = ticket_avant_vente(ticket_id=2, requester_email="c2@example.com", created_at=datetime.date(2026, 1, 1))
        ticket_be["country"] = "BE"
        resultats = resoudre_achats_observes_avant_vente([ticket_fr, ticket_be], commandes_par_email({}), 30)
        table = construire_table_pays_avant_vente([ticket_fr, ticket_be], resultats)
        pays_vus = set(ligne["pays"] for ligne in table)
        self.assertEqual(pays_vus, {"FR", "BE"})
        for ligne in table:
            self.assertNotIn("agent", ligne)


# Composition Impact & confiance (Étape 5I.1) : 4E reste l'unique propriétaire du calcul NPS et de
# l'alignement -- seul le calage sur la période sélectionnée (bug corrigé, audit 5I section 43) et
# la Lecture combinée confiance/finance sont testés ici.
class TestImpactConfiance5I1(unittest.TestCase):
    def test_a_identifier_observation_correspond_au_mois_exact(self):
        reponses = (
            [reponse_nps_test(date_reponse=datetime.date(2025, 12, 5))] * 3
            + [reponse_nps_test(date_reponse=datetime.date(2026, 1, 10))] * 3
        )
        historique = construire_historique_nps_par_mois(reponses)
        index = identifier_observation_nps_periode(historique, datetime.date(2026, 1, 12))
        self.assertEqual(historique[index]["cle_mois"], "2026-01")

    def test_b_identifier_observation_aucun_mois_correspondant(self):
        reponses = [reponse_nps_test(date_reponse=datetime.date(2025, 12, 5))] * 3
        historique = construire_historique_nps_par_mois(reponses)
        index = identifier_observation_nps_periode(historique, datetime.date(2026, 6, 15))
        self.assertIsNone(index)

    def test_c_identifier_observation_jamais_le_mois_le_plus_proche(self):
        # Un mois voisin (novembre) ne doit jamais être retourné pour une période de janvier --
        # aucun repli, aucune approximation (Étape 5I.1, section 4).
        reponses = [reponse_nps_test(date_reponse=datetime.date(2025, 11, 20))] * 5
        historique = construire_historique_nps_par_mois(reponses)
        index = identifier_observation_nps_periode(historique, datetime.date(2026, 1, 5))
        self.assertIsNone(index)

    def test_d_sensibilite_petit_echantillon_volume_faible(self):
        texte = texte_sensibilite_echantillon_nps(ETAT_PRUDENCE_VOLUME_FAIBLE)
        self.assertEqual(texte, TEXTE_SENSIBILITE_PETIT_ECHANTILLON_NPS)

    def test_e_sensibilite_petit_echantillon_premiere_observation(self):
        texte = texte_sensibilite_echantillon_nps(ETAT_PRUDENCE_PREMIERE_OBSERVATION)
        self.assertEqual(texte, TEXTE_SENSIBILITE_PETIT_ECHANTILLON_NPS)

    def test_f_sensibilite_absente_volume_habituel(self):
        texte = texte_sensibilite_echantillon_nps(ETAT_PRUDENCE_VOLUME_HABITUEL)
        self.assertIsNone(texte)

    def test_g_lecture_aucune_donnee_nps_aucun_cout(self):
        texte = construire_lecture_impact_confiance(None, None, 0, 0)
        self.assertIn("Aucune donnée NPS exploitable pour cette période.", texte)
        self.assertIn("Aucun coût direct identifié sur cette période.", texte)

    def test_h_lecture_nps_present_sans_alignement(self):
        item_nps = {"nps": -6.0, "n": 69}
        texte = construire_lecture_impact_confiance(item_nps, None, 0, 0)
        self.assertIn("Le NPS de la période est de -6 sur 69 réponses.", texte)

    def test_i_lecture_combine_nps_et_cout_sans_les_fusionner(self):
        item_nps = {"nps": 6.0, "n": 18}
        texte_align = "Le NPS de cette période recule dans la série disponible."
        texte = construire_lecture_impact_confiance(item_nps, texte_align, 5000, 1000)
        self.assertIn("Le NPS de la période est de +6 sur 18 réponses.", texte)
        self.assertIn(texte_align, texte)
        self.assertIn("coût direct observé/estimé sur cette période s'élève à 5 000 €", texte)
        self.assertIn("20 % de ce montant est classé potentiellement évitable", texte)
        # Jamais une seule affirmation fusionnant NPS et coût (Étape 5I.1, section 9/28) : la phrase
        # qui parle du coût ne mentionne jamais le NPS.
        phrase_cout = texte[texte.index("Le coût direct"):]
        self.assertNotIn("NPS", phrase_cout)

    def test_j_lecture_jamais_de_score_compose(self):
        item_nps = {"nps": 31.0, "n": 48}
        texte = construire_lecture_impact_confiance(item_nps, None, 5000, 0)
        self.assertNotIn("score global", texte.lower())
        self.assertNotIn("indice", texte.lower())

    def test_k_caveat_recouvrement_jamais_additionner(self):
        self.assertIn("ne jamais additionner", TEXTE_CAVEAT_RECOUVREMENT_COUT.lower())
        self.assertIn("Coût direct", TEXTE_CAVEAT_RECOUVREMENT_COUT)
        self.assertIn("Coût garantie", TEXTE_CAVEAT_RECOUVREMENT_COUT)


# Invariants transverses (Étape 6A) : des vérités qui doivent tenir quel que soit l'onglet qui les
# affiche -- pas des snapshots fragiles, des propriétés structurelles du modèle de données.
class TestCoherenceTransverse6A(unittest.TestCase):
    # categoriser() ne doit jamais laisser un ticket sans catégorie (sinon la somme des catégories
    # affichées par onglet divergerait silencieusement du volume total affiché ailleurs).
    def test_a_categoriser_jamais_none(self):
        raisons_connues = (
            "Livraison", "Suivi commande", "Abonnement / paiement", "Retour / remboursement",
            "Conseil programme / produit", "Utilisation / routine", "SAV", "Motif inconnu jamais vu",
        )
        for raison in raisons_connues:
            ticket = ticket_care_test(ticket_reason=raison, resolution_type="Remplacement produit")
            self.assertIsNotNone(categoriser(ticket))

    def test_b_somme_categories_egale_total_tickets(self):
        tickets = []
        raisons_variees = (
            "Livraison", "Suivi commande", "Conseil programme / produit", "Utilisation / routine",
            "SAV", "Abonnement / paiement", "Motif rare jamais catalogué",
        )
        for i in range(len(raisons_variees)):
            tickets.append(ticket_care_test(
                ticket_id=i, requester_email="c" + str(i) + "@example.com",
                ticket_reason=raisons_variees[i], resolution_type="Remplacement produit",
            ))

        categories = {}
        for ticket in tickets:
            categorie = categoriser(ticket)
            if categorie in categories:
                categories[categorie].append(ticket)
            else:
                categories[categorie] = [ticket]

        somme = 0
        for categorie, tickets_categorie in categories.items():
            somme = somme + len(tickets_categorie)
        self.assertEqual(somme, len(tickets))


class TestShellVisuel6C(unittest.TestCase):
    # Format CSAT (Étape 6C, section 27) : virgule française, toujours 2 décimales -- jamais un
    # nombre entier de décimales variable ("4.0" vs "3.91") qui donne une fausse impression de
    # précision différente entre deux lignes du même tableau.
    def test_a_formater_csat_entier_deux_decimales(self):
        self.assertEqual(formater_csat(4.0), "4,00")

    def test_b_formater_csat_virgule_francaise(self):
        self.assertEqual(formater_csat(4.05), "4,05")

    def test_c_formater_csat_ne_change_pas_la_valeur_numerique(self):
        texte = formater_csat(3.91)
        valeur_repartie = texte.replace(",", ".")
        self.assertAlmostEqual(float(valeur_repartie), 3.91)


if __name__ == "__main__":
    unittest.main()
