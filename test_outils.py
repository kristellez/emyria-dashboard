import datetime
import unittest

from outils import (
    cles_combinees,
    delai_jours,
    formater_csat,
    formater_duree,
    formater_pourcentage,
    moyenne,
    montant_cout_garantie,
    montant_perte_estime,
    niveau_macro,
    taux_rempli,
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
        self.commandes = {"EMY-1": {"montant_total": 200}}

    def test_ticket_sans_order_id_retourne_none(self):
        ticket = {"order_id": None}
        self.assertIsNone(montant_perte_estime(ticket, self.commandes, "Remboursement"))

    def test_order_id_absent_des_commandes_retourne_none(self):
        ticket = {"order_id": "EMY-INCONNU"}
        self.assertIsNone(montant_perte_estime(ticket, self.commandes, "Remboursement"))

    def test_remboursement_est_le_montant_complet(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_perte_estime(ticket, self.commandes, "Remboursement"), 200)

    def test_remplacement_produit_est_une_fraction(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_perte_estime(ticket, self.commandes, "Remplacement produit"), 70)

    def test_geste_commercial_est_une_fraction_plus_faible(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_perte_estime(ticket, self.commandes, "Geste commercial"), 30)

    def test_type_perte_inconnu_retombe_sur_le_montant_complet(self):
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_perte_estime(ticket, self.commandes, "Type jamais vu"), 200)


class TestMontantCoutGarantie(unittest.TestCase):
    def test_utilise_la_fraction_remplacement(self):
        commandes = {"EMY-1": {"montant_total": 200}}
        ticket = {"order_id": "EMY-1"}
        self.assertEqual(montant_cout_garantie(ticket, commandes), 70)

    def test_sans_commande_retourne_none(self):
        ticket = {"order_id": None}
        self.assertIsNone(montant_cout_garantie(ticket, {}))


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


if __name__ == "__main__":
    unittest.main()
