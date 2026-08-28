import datetime
import unittest

from outils import (
    cles_combinees,
    delai_jours,
    dernier_ticket_avant,
    formater_csat,
    formater_duree,
    formater_pourcentage,
    moyenne,
    montant_cout_garantie,
    montant_perte_estime,
    niveau_charge_creneau,
    niveau_macro,
    niveau_reponse_ouvree,
    taux_rempli,
    tickets_par_email,
)


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
        self.assertEqual(formater_csat(4.567), "4.57")

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


class TestNiveauChargeCreneau(unittest.TestCase):
    def test_hors_couverture_si_statut_pas_couverture_requise(self):
        self.assertEqual(niveau_charge_creneau("Hors standard", 3, 50), "HORS_COUVERTURE")
        self.assertEqual(niveau_charge_creneau("Pause déjeuner", 0, 0), "HORS_COUVERTURE")

    def test_hors_couverture_ignore_le_volume(self):
        # Un statut hors "Couverture requise" reste muet même avec un volume élevé.
        self.assertEqual(niveau_charge_creneau("Hors standard", 0, None), "HORS_COUVERTURE")

    def test_zero_agent_en_couverture_requise_est_hotspot(self):
        # Anomalie reelle (personne en poste alors que le creneau devrait etre couvert),
        # distincte d'une fermeture assumee (HORS_COUVERTURE).
        self.assertEqual(niveau_charge_creneau("Couverture requise", 0, None), "HOTSPOT")

    def test_un_agent_charge_confortable_est_confortable(self):
        self.assertEqual(niveau_charge_creneau("Couverture requise", 1, 10), "CONFORTABLE")

    def test_charge_a_surveiller_reste_a_surveiller(self):
        self.assertEqual(niveau_charge_creneau("Couverture requise", 1, 20), "A_SURVEILLER")

    def test_un_agent_charge_critique_est_hotspot(self):
        self.assertEqual(niveau_charge_creneau("Couverture requise", 1, 35), "HOTSPOT")

    def test_deux_agents_charge_critique_est_hotspot(self):
        self.assertEqual(niveau_charge_creneau("Couverture requise", 2, 35), "HOTSPOT")

    def test_deux_agents_charge_confortable_est_confortable(self):
        self.assertEqual(niveau_charge_creneau("Couverture requise", 2, 12), "CONFORTABLE")


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


if __name__ == "__main__":
    unittest.main()
