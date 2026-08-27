# Roadmap – Outil d'analyse des tickets (Emyria)

## Vision
Outil interne (pas l'agent IA du CRM) qui analyse les tickets, détecte les irritants récurrents,
suggère des macros/FAQ/pages Notion à créer ou améliorer, et facilite la vie des agents —
pas pour surveiller, mais pour accompagner et valoriser.

**V1 (cette phase)** : sans API, imports/exports manuels.
**V2 (plus tard)** : connecté en direct au CRM, à Shopify et à Notion, quasi automatique.

## 1. Ingestion hebdomadaire ✅ fait (adapté)
- Dossier de dépôt : `exports_hebdomadaires/` — en pratique un export mensuel représentatif
  (14 fichiers, sept. 2025 à sept. 2026) plutôt qu'un export par semaine, pour raconter une
  histoire sur un an sans générer 52 fichiers.
- Chaque export a une colonne manuelle **"Événement de la semaine"** (arrivée dans l'équipe,
  soldes, campagne pub, nouvelle FAQ...) pour donner du contexte aux variations observées.

## 2. Dashboard — vue d'ensemble ✅ fait
KPIs globaux avec **% d'évolution vs une période de comparaison** (voir "Note pour plus tard"
ci-dessous — le filtre par plage de dates libre remplace le "vs semaine précédente" fixe) :
- nombre de tickets
- CSAT
- temps de réponse
- nombre de tickets traités via macro
- tickets les plus longs à résoudre

## 3. Dashboard — par agent ✅ fait
Pas pour "punir" : pour comprendre et accompagner.
- Qui prend le plus de temps → comprendre pourquoi, aider.
- Qui a les meilleurs résultats (volume + qualité) → valoriser.
- Un agent qui n'utilise pas les macros → savoir pourquoi (ex : ne sait simplement pas
  qu'elles existent) plutôt que de juste constater le chiffre.

## 4. Suggestions d'amélioration ✅ fait
- Macro à créer / à améliorer
- FAQ à créer / à améliorer
- Page Notion (process interne) à créer / à améliorer

## 5. Trois catégories suivies séparément ✅ fait
- **Avant-vente** : mail/chat/WhatsApp/tél + consultations téléphoniques programmées sur
  rendez-vous (cohérent avec un positionnement haut de gamme). Volume, satisfaction, taux de
  conversion (volume et CA) — croisé avec les données Shopify (import manuel en V1). Comparaison
  service client généraliste vs personne dédiée aux rendez-vous téléphoniques.
- **Après-vente – livraison** : retards, pertes, dommages.
- **Après-vente – SAV produit** (hors livraison) : casse, dysfonctionnement, incompréhension
  d'utilisation.

## 6. Onglet "To-do de la semaine" ✅ fait (absorbé ailleurs)
Pas construit comme onglet séparé : la liste actionnable (macros à créer, FAQ à créer, etc.)
vit directement dans les tableaux de l'onglet "Alertes & suggestions", avec un tableau de suivi
d'impact avant/après (voir point 7) plutôt qu'une simple liste de tâches.

## 7. Base de connaissance ✅ fait
- Dossier `knowledge_base/` (sous-dossiers `macros/`, `faq/`, + ressources internes).
- Se met à jour au fil des suggestions validées.
- Colonne **"créé ou non"** : l'agent/l'admin valide (ou pas) le texte suggéré et l'état de
  création dans le CRM.
- Le texte final validé (macro ou FAQ) est archivé dans le dossier correspondant.

Détail des métriques par cadence : [METRIQUES.md](METRIQUES.md).

## Ordre de construction proposé
1. Lire un export hebdomadaire (**fait** — [analyse_export_excel.py](../mes-premiers-pas/analyse_export_excel.py))
2. Lire **plusieurs** exports dans `exports_hebdomadaires/` et calculer les KPIs de base + % d'évolution vs une période de comparaison (point 2) — **fait**
3. Décliner les mêmes KPIs par agent (point 3) — **fait**
4. Détecter les irritants sans macro associée → première version des suggestions (point 4) — **fait**
5. Séparer l'analyse par catégorie avant-vente / livraison / SAV produit (point 5) — **fait**
6. Colonne "événement de la semaine" + croisement Shopify (points 1 et 5) — **fait**
7. To-do list + suivi knowledge base avec statut "créé ou non" (points 6 et 7) — **fait**
8. V2 : API CRM / Shopify / Notion — **pas fait**, reste l'écart principal entre la démo et un
   vrai outil de pilotage au quotidien (ingestion manuelle en V1)

## Filtre par plage de dates ✅ fait

Construit différemment de l'idée initiale (filtre par mois/année) : un vrai sélecteur de plage de
dates libre dans la barre latérale (Période A + Période B optionnelle pour comparaison, "étendre
sur plusieurs semaines"), plus flexible qu'un simple mois/année et permettant de comparer
n'importe quelle période à n'importe quelle autre (avant/après l'arrivée d'un agent, pendant une
absence, etc.).
