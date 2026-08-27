# Dashboard Customer Care — Emyria

Tableau de bord d'analyse du service client pour **Emyria**, une marque fictive de diffuseurs
d'ambiance connectés. Projet portfolio en Python (Streamlit) : ingestion de tickets support,
détection automatique d'irritants récurrents, suivi d'impact avant/après action, et volet
business (conversion, coûts SAV, fidélisation).

> Toutes les données (tickets, commandes, avis clients) sont **100 % fictives**, générées pour la démonstration.

## Démo en ligne

👉 [Voir le dashboard](LIEN_A_COMPLETER_APRES_DEPLOIEMENT)

## Ce que fait l'outil

- **Suivi de la performance support** à la semaine, sur plusieurs semaines, ou en tendance sur ~1 an
- **Alertes automatiques** : détecte une catégorie qui se dégrade sur deux signaux à la fois (CSAT en baisse ET temps de réponse en hausse) — pas sur un seul, pour limiter les faux positifs
- **Suggestions de macros/FAQ à créer**, basées sur les irritants récurrents (CSAT bas, adoption macro faible, volume d'échanges élevé)
- **Suivi d'impact** : une fois une macro créée, compare le CSAT et l'usage macro avant/après sa mise en place
- **Volet business** : conversion avant-vente réelle (pas estimée), coûts SAV, confiance client (NPS), fidélisation/réachat, coût d'acquisition par canal

## Stack technique

- [Streamlit](https://streamlit.io/) pour le dashboard
- [Pandas](https://pandas.pydata.org/) et [openpyxl](https://openpyxl.readthedocs.io/) pour le traitement des données (fichiers Excel)
- [Altair](https://altair-viz.github.io/) pour les graphiques

## Lancer en local

```bash
git clone <URL_DU_REPO>
cd emyria-outil-tickets
pip install -r requirements.txt
streamlit run app.py
```

## Structure du projet

- `app.py` — le dashboard Streamlit
- `outils.py` — logique métier et fonctions de traitement des données
- `exports_hebdomadaires/` — exports tickets fictifs (un par mois, ~1 an)
- `data_shopify/` — commandes et avis NPS fictifs
- `data_calendrier/` — calendrier marketing/saisonnier fictif
- `data_suivi/` — suivi manuel des macros/FAQ créées (édité à la main)
- `knowledge_base/` — textes des macros et FAQ créées
- `ROADMAP.md` / `METRIQUES.md` — notes de conception du projet

## Contexte du projet

Ce projet a été construit pour apprendre Python en partant d'un besoin concret (service client),
puis développé comme pièce de portfolio. Le produit et l'entreprise (Emyria) sont entièrement
fictifs — voir l'onglet "Contexte" du dashboard pour le détail.
