# Métriques à suivre — par cadence et par objectif

Référence pour construire le dashboard ([ROADMAP.md](ROADMAP.md)). Chaque métrique est reliée
à la colonne réelle de l'export (`RAW_TICKETS`) qui permet de la calculer.

## 1. Hebdomadaire — management & accompagnement de l'équipe

But : piloter la semaine, repérer qui a besoin d'aide, qui mérite d'être valorisé — jamais pour sanctionner.

- **Volume total de tickets** + % d'évolution vs semaine précédente — `ticket_id` (compte)
- **Volume par agent** (classement) — `assignee`
- **Sujets couverts par agent** — croiser `assignee` × `subject_cluster` (ou `ticket_reason`) :
  qui traite quoi, pour repérer un agent surchargé sur un sujet difficile, ou un agent jamais
  exposé à un type de demande (donc jamais formé dessus)
- **Vue détaillée agent × sujet** — pour chaque combinaison (assez de volume pour être fiable) :
  volume, CSAT, taux de macro, temps de 1re réponse. Objectif : localiser précisément *où* un
  client est déçu de la réponse reçue — pas juste "cet agent a un CSAT bas", mais "cet agent a un
  CSAT bas *sur ce sujet précis*", ce qui distingue un souci de formation (un sujet) d'un souci
  process (une macro à revoir, cf. section 3) ou d'un souci individuel (tous les sujets touchés)
- **CSAT global** + **CSAT par agent** — `csat`
- **Temps de 1re réponse** + **temps de résolution complet** (global et par agent) —
  `first_reply_time_min`, `full_resolution_time_hours`
- **Taux d'usage des macros**, global et par agent — `macro_applied`. Un agent très en dessous
  de la moyenne : creuser *pourquoi* (ne sait pas qu'elle existe ? macro mal indexée ? cas non
  couvert par les macros existantes ?) avant de conclure quoi que ce soit
- **Réouvertures** (`reopens`) — un ticket rouvert plusieurs fois signale une résolution bâclée
  ou incomplète, pas juste un chiffre de volume en plus
- **Respect SLA** (`sla_met`), global et par agent
- **Top irritants de la semaine** + nouveaux entrants vs la semaine précédente — `subject_cluster`
  (déjà en place dans `analyse_export_excel.py`)
- **Répartition par canal** — `via_channel` (mail/chat/WhatsApp/tél, dont créneaux de consultation
  téléphonique programmée pour l'avant-vente), pour équilibrer la charge
- **Avant-vente vs après-vente** — `is_sav`, première brique de la séparation en 3 catégories
  prévue au roadmap
- **Tickets les plus longs à résoudre** (outliers) — `full_resolution_time_hours`, les N tickets
  avec le temps le plus élevé. Une moyenne peut être bonne alors qu'un petit groupe de tickets
  traîne — ce sont ces cas-là qui ont besoin d'un regard, pas la moyenne
- **Répartition par jour / heure** — `created_at` : identifie les pics de charge dans la semaine,
  utile pour le planning des agents (pas seulement la charge globale)

## Mensuel — partenaire livraison

Un seul transporteur chez Emyria, pas besoin de le distinguer par nom dans les données. Le
suivi hebdomadaire n'est pas pertinent pour ce point (trop de bruit semaine à semaine) — cadence
**mensuelle** : agréger sur le mois les sujets de la catégorie Livraison (`Délai de livraison`,
`Colis annoncé livré non reçu`, dommages...) avec volume, CSAT et évolution, pour un point
factuel avec le transporteur.

## 2. Trimestriel — amélioration produit

But : remonter à l'équipe produit des signaux chiffrés, pas des impressions.

- **Irritants par produit** sur 3 mois — `product_name` / `product_category` × `subject_cluster`
  ou `issue_type` : quel produit génère quel type de souci, en volume et en tendance (pas juste
  un pic isolé)
- **Composant en cause** — `component` : localise le défaut (ex. "fixation capsule", "bouton /
  commande") pour orienter le produit vers un correctif précis
- **SAV récurrents par client** — `prior_sav_count` : un client à 2-3 SAV sur le même produit
  est un signal de défaut structurel, pas un cas isolé à traiter au coup par coup
- **Sous garantie vs hors garantie** — `warranty_status` : impact coût réel des défauts produit
- **Type de résolution** — `resolution_type` : ratio remplacement produit / réparation / conseil
  à distance. Si "conseil à distance" domine sur un `issue_type` donné → problème de
  compréhension d'usage (donc plutôt un sujet FAQ que produit) ; si "remplacement" domine →
  vrai défaut à corriger
- **CSAT moyen par produit/catégorie** sur la période
- **Délai entre achat et signalement SAV** — `order_date` → `sav_reported_date` : une panne à
  J+10 raconte une histoire de défaut de fabrication ; une panne à 8 mois raconte plutôt de
  l'usure normale. `prior_sav_count` capture la récurrence mais pas cette temporalité — les deux
  se complètent

## 3. Amélioration du service — macros, FAQ, base de connaissance

But : transformer un irritant récurrent en action concrète (créer/améliorer une macro, une FAQ,
une page process).

- **Sujets fréquents sans macro associée** — `subject_cluster` revient souvent alors que
  `macro_applied` est vide sur ces tickets → macro à **créer**
- **Sujets fréquents avec macro mais résultat décevant** — macro utilisée, mais temps de
  résolution long ou CSAT bas quand même → macro à **améliorer** (le texte existant ne répond
  pas bien au cas réel)
- **Usage de macro anormalement bas chez un agent** — signal à investiguer plutôt qu'à
  sanctionner (cf. section 1)
- **CSAT bas malgré un usage macro élevé chez un agent** — signal inverse et tout aussi
  important : si un agent utilise beaucoup les macros mais garde un CSAT bas, le problème n'est
  probablement pas l'agent, c'est le **texte de la macro** qui ne répond pas bien au client. À
  croiser avec la vue détaillée agent × sujet (section 1) pour savoir sur quel sujet précisément
- **Lecture qualitative de `csat_comment`** sur les tickets mal notés — pour repérer des
  irritants "process" non capturés par les champs structurés (ex. "j'ai dû réexpliquer trois
  fois" = souci de transfert d'info entre agents, pas un souci produit)
- **Nombre d'échanges par ticket** — `replies` élevé sur un même sujet → candidat naturel à une
  FAQ ou une page de base de connaissance, pour raccourcir la résolution la prochaine fois
- **Avant / après la création d'une macro ou d'une FAQ** — une fois une action validée
  (colonne "créé ou non" de la base de connaissance), comparer le CSAT et le temps de résolution
  sur ce sujet précis avant vs après sa mise en place. Sans ce suivi, impossible de savoir si une
  suggestion a réellement amélioré quelque chose — c'est ce qui transforme l'outil de "détecteur
  d'irritants" en outil qui prouve son impact

> **Note data** : `tags` et `ticket_reason` sont strictement redondants dans l'export actuel
> (mêmes 7 catégories, mêmes effectifs) — inutile de suivre les deux, n'en garder qu'un.

## Vue dédiée : Alertes de la semaine

Une catégorie (SAV produit / SAV usage / après-vente admin / livraison / avant-vente) est
**signalée** quand deux choses se dégradent **en même temps** d'une semaine à l'autre :
- le CSAT baisse, **et**
- le temps de 1re réponse augmente

Une seule des deux qui bouge n'est pas forcément un signal (le volume peut expliquer une hausse
de temps de réponse sans dégrader la satisfaction, par ex.) — c'est la combinaison des deux qui
rend le signal fiable. À lire toujours à côté de l'`evenement_semaine` des deux semaines
comparées : un événement identifié (campagne pub, tension transporteur...) peut expliquer la
dégradation sans qu'il y ait de vrai problème de service à corriger — mais l'outil ne tranche pas
ça tout seul, c'est une lecture humaine.

Implémenté dans [detecter_alertes.py](../mes-premiers-pas/detecter_alertes.py).

## 4. Événement de la semaine

Ce n'est pas une métrique calculée — c'est le **contexte** qui permet d'interpréter les autres.
Un pic sur "livraison" veut dire deux choses très différentes selon qu'il y a eu ou non une
campagne pub cette semaine-là. À archiver systématiquement à côté des chiffres de la semaine
(déjà fait : colonne `evenement_semaine` dans chaque export), pour :
- éviter de tirer une fausse conclusion sur un pic ponctuel expliqué par un facteur externe
- garder un historique exploitable plus tard pour chercher des corrélations automatiques (V2)
