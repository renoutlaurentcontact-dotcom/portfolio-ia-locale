# Mesures et preuves

[Accueil](README.md) · [Configuration](CONFIGURATION.md) · [Reproduction](PROTOCOLE_REPRODUCTION.md)

## Source des observations

Les résultats locaux ci-dessous proviennent du [rapport d’audit du 4 novembre 2026, transmis le 5 novembre](RAPPORT_AUDIT_2026-11-04.txt). Ce rapport décrit la relecture de commandes, de résultats JSON et de journaux sur le P910, ainsi que des recalculs statistiques et un hachage intégral des poids.

Pour cette documentation, les références publiques et les calculs à partir des valeurs transcrites ont été contrôlés. Les journaux originaux et le fichier GGUF local n’ont pas été relus ou hachés à nouveau par les rédacteurs du dépôt. Le [fichier de données](mesures_transcrites.json) est une transcription du rapport, pas un export des journaux originaux.

## Résultat principal : colocation des couches et des experts

| Comparaison du 23 octobre | Génération, médiane stable |
|---|---:|
| Colocation désactivée | 83,964 tokens/s |
| Colocation split22 | 95,608 tokens/s |
| Gain relatif | **+13,87 %** |

Conditions décrites dans l’audit :

- Même fichier de poids et même binaire candidat ; arguments identiques.
- Différence isolée : variable LLAMA_V100_COLOCATE_SPLIT absente ou réglée à 22.
- Deux V100 PCIe de 32 Go ; RTX exclue.
- 67 tokens d’entrée et 768 générés ; cache de prompt désactivé.
- Cinq requêtes par variante ; score stable = médiane des trois dernières.
- Température 0, seed 42, top-k 1, top-p 1, min-p 0, repeat-penalty 1 ; effort de raisonnement medium.
- MTP profondeur 3, sous-lot MTP 32, batch 2048, microbatch 512.
- Contenu et raisonnement identiques pour les six réponses retenues, selon le rapport.

Valeurs stables transcrites :

| Variante | Mesure 1 | Mesure 2 | Mesure 3 | Médiane |
|---|---:|---:|---:|---:|
| OFF | 84,194 | 83,964 | 83,964 | 83,964 |
| split22 | 95,124 | 95,717 | 95,608 | 95,608 |

Les médianes plus précises données par l’audit sont 83,9643798360 et 95,6082291386. Le gain s’arrondit à +13,87 % avec ces valeurs comme avec les valeurs publiées arrondies. Le débit natif exclut le premier token du calcul ; il ne faut pas le remplacer mécaniquement par longueur générée / durée.

Preuves d’origine citées dans l’audit : dossier bench-confirmation-20261023, results.json, summary.json, commandes des deux variantes, benchmark.py, réponses et journaux associés. Ces originaux ne sont pas encore joints au dépôt.

### Traitement du contexte, opération distincte

Pour une entrée de 37 475 tokens réellement lus, sans cache : médiane de **593,857 à 668,949 tokens/s**, soit **+12,64 %**. Les générations associées différaient : ce résultat descriptif n’a pas le même contrôle de sorties identiques que le test court ci-dessus.

## Mesure finale distincte : 99,148 tokens/s

Le rapport décrit une campagne du 28 octobre sur le moteur colocate22-argmax, avec sous-lot MTP 64 :

- 73 tokens d’entrée, 384 générés, cache désactivé, aucune image.
- Deux passages ; chacun comporte une chauffe de 32 tokens puis trois requêtes courtes.
- Paramètres déterministes et effort medium ; sortie courte identique dans les contrôles.
- L’ordre réellement exécuté est A1–B1–A2–B2, malgré le libellé « ABBA » du script ; A1 est repris d’un passage précédent.

| Passage | Valeurs transcrites, tokens/s | Médiane |
|---|---|---:|
| B1 | 98,8887537667 ; 99,1269580809 ; 99,1597826563 | 99,1269580809 |
| B2 | 99,1690513846 ; 99,0728539863 ; 99,2404092436 | 99,1690513846 |

**99,14800473275 tokens/s est la moyenne de ces deux médianes.** Ce résultat n’est pas un pic isolé. Il ne permet pas de déduire un gain causal depuis 95,608 : les charges, le moteur et le protocole des deux campagnes diffèrent.

Preuves citées : mtp-ubatch-summary.json, compare_mtp.py, compare_mtp_ubatch.py, six réponses JSON des passages B1/B2 et journaux serveur correspondants. Originaux non joints.

### Effet du sous-lot MTP 32 vers 64, dans cette seule campagne

| Opération | Sous-lot 32 | Sous-lot 64 | Écart descriptif |
|---|---:|---:|---:|
| Génération | 99,1131973343 | 99,14800473275 | +0,035 % |
| Lecture de 4 103 tokens | 661,282373 | 666,429197 | +0,778 % |
| Lecture de 16 391 tokens | 772,249603 | 779,898211 | +0,990 % |

La génération est pratiquement inchangée. Les petits écarts observés ne constituent pas une promesse générale. Les tests de lecture ne demandent qu’une sortie ; leur champ predicted_per_second nul n’est pas un résultat de génération.

## Progression historique « moins de 60 vers environ 90 »

Des débits inférieurs à 60 et proches de 90 existent dans l’historique décrit, avec des GPU, requêtes ou longueurs différentes. **L’audit n’a pas retrouvé une paire comparable établissant un gain global de moins de 60 à environ 90.** Cette trajectoire n’est pas utilisée comme résultat contrôlé.

## Refaire les calculs

Depuis la racine du dépôt :

    python recalculer_mesures.py

L’outil utilise seulement la bibliothèque standard et les valeurs transcrites du rapport. Il ne lance ni modèle, ni service, ni requête réseau. Il permet de contrôler l’arithmétique ; une reproduction des benchmarks nécessite les artefacts d’origine.

## Limites d’interprétation

- Peu de répétitions, charges synthétiques et sorties courtes, parfois arrêtées à la limite demandée.
- Le débit de génération inclut le raisonnement ; il n’est pas le débit du seul texte visible dans une interface vocale ou Hermès.
- La fenêtre réservée de 200 192 tokens n’est pas entièrement remplie dans ces tests.
- Ces résultats ne constituent pas une évaluation générale de qualité, de stabilité ou de production.
- Les performances publiées par le fournisseur des poids sur son propre matériel ne sont pas des mesures de ce P910.

[Lire le rapport transmis](RAPPORT_AUDIT_2026-11-04.txt) · [Provenance et licences](PROVENANCE_ET_LICENCES.md)
