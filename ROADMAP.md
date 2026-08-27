# Roadmap – Outil d'analyse des tickets (Emyria)

## Vision
Outil interne (pas l'agent IA du CRM) qui analyse les tickets, détecte les irritants récurrents,
suggère des macros/FAQ/pages Notion à créer ou améliorer, et facilite la vie des agents —
pas pour surveiller, mais pour accompagner et valoriser.

**V1 (cette phase)** : sans API, imports/exports manuels.
**V2 (plus tard)** : connecté en direct au CRM, à Shopify et à Notion, quasi automatique.

## 1. Ingestion hebdomadaire
- Dossier de dépôt : `exports_hebdomadaires/` — un export par semaine.
- Chaque export a une colonne manuelle **"Événement de la semaine"** (arrivée dans l'équipe,
  soldes, campagne pub, nouvelle FAQ...) pour donner du contexte aux variations observées.

## 2. Dashboard — vue d'ensemble
KPIs globaux avec **% d'évolution vs la semaine précédente** :
- nombre de tickets
- CSAT
- temps de réponse
- nombre de tickets traités via macro
- tickets les plus longs à résoudre

## 3. Dashboard — par agent
Pas pour "punir" : pour comprendre et accompagner.
- Qui prend le plus de temps → comprendre pourquoi, aider.
- Qui a les meilleurs résultats (volume + qualité) → valoriser.
- Un agent qui n'utilise pas les macros → savoir pourquoi (ex : ne sait simplement pas
  qu'elles existent) plutôt que de juste constater le chiffre.

## 4. Suggestions d'amélioration
- Macro à créer / à améliorer
- FAQ à créer / à améliorer
- Page Notion (process interne) à créer / à améliorer

## 5. Trois catégories suivies séparément
- **Avant-vente** : mail/chat/WhatsApp/tél + consultations téléphoniques programmées sur
  rendez-vous (cohérent avec un positionnement haut de gamme). Volume, satisfaction, taux de
  conversion (volume et CA) — croisé avec les données Shopify (import manuel en V1). Comparaison
  service client généraliste vs personne dédiée aux rendez-vous téléphoniques.
- **Après-vente – livraison** : retards, pertes, dommages.
- **Après-vente – SAV produit** (hors livraison) : casse, dysfonctionnement, incompréhension
  d'utilisation.

## 6. Onglet "To-do de la semaine"
Liste actionnable issue des suggestions : macros à créer, FAQ à créer, etc.

## 7. Base de connaissance
- Dossier `knowledge_base/` (sous-dossiers `macros/`, `faq/`, + ressources internes).
- Se met à jour au fil des suggestions validées.
- Colonne **"créé ou non"** : l'agent/l'admin valide (ou pas) le texte suggéré et l'état de
  création dans le CRM.
- Le texte final validé (macro ou FAQ) est archivé dans le dossier correspondant.

Détail des métriques par cadence : [METRIQUES.md](METRIQUES.md).

## Ordre de construction proposé
1. Lire un export hebdomadaire (**fait** — [analyse_export_excel.py](../mes-premiers-pas/analyse_export_excel.py))
2. Lire **plusieurs** exports dans `exports_hebdomadaires/` et calculer les KPIs de base + % d'évolution semaine vs semaine précédente (point 2)
3. Décliner les mêmes KPIs par agent (point 3)
4. Détecter les irritants sans macro associée → première version des suggestions (point 4)
5. Séparer l'analyse par catégorie avant-vente / livraison / SAV produit (point 5)
6. Colonne "événement de la semaine" + croisement Shopify (points 1 et 5)
7. To-do list + suivi knowledge base avec statut "créé ou non" (points 6 et 7)
8. V2 : API CRM / Shopify / Notion

## Note pour plus tard : filtre par mois / année

Idée retenue mais pas encore construite : pouvoir filtrer l'interface par mois ou par année une
fois qu'il y aura plusieurs mois d'exports réels dans `exports_hebdomadaires/`. Pas pertinent
tant qu'on n'a que 2 semaines de données (rien à filtrer) — à construire quand l'historique réel
existera : charger tous les fichiers du dossier plutôt que 2 chemins fixes, et laisser
choisir une période dans l'interface.
