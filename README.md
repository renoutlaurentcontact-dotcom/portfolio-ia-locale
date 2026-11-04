# Qwen sur deux Tesla V100 — optimisation et expérimentation locale

**Projet personnel piloté par Laurent Renout, avec l’assistance d’agents IA.**

Ce dépôt documente une démarche pour améliorer l’exécution d’un modèle de langage local sur une station Lenovo ThinkStation P910 existante : comprendre les contraintes de mémoire, rechercher des approches compatibles, faire adapter l’environnement et examiner les résultats.

Il rassemble la configuration décrite, les paramètres retrouvés dans un rapport technique et les informations nécessaires pour préparer des essais comparables.

## Configuration de travail

| Composant | Configuration décrite |
|---|---|
| Station | Lenovo ThinkStation P910 |
| CPU | 2 × Intel Xeon E5-2698 v4 — 40 cœurs / 80 threads au total |
| RAM | Environ 170 Go de DDR4 ECC |
| GPU utilisés pour Qwen | 2 × NVIDIA Tesla V100 PCIe de 32 Go chacune |
| GPU complémentaire | NVIDIA RTX 4070 SUPER 12 Go, utilisée séparément selon les tâches |
| Système | Ubuntu 24.04 LTS |
| Moteur | Environnement fondé sur llama.cpp, avec adaptations réalisées par les agents |
| Désignation du modèle fournie dans le projet | Qwen3.8-Flash-Next, annoncé autour de 125 milliards de paramètres totaux |

La configuration est issue des informations de projet. Les relevés matériels et les métadonnées exactes du modèle restent à joindre. Les deux V100 possèdent des mémoires séparées ; 64 Go cumulés ne constituent pas automatiquement un espace mémoire unique.

[Voir la configuration et les paramètres](CONFIGURATION.md)

## Démarche

1. Définir le besoin et les contraintes du matériel.
2. Rechercher des méthodes existantes et choisir les pistes compatibles.
3. Organiser les adaptations et les essais avec les agents IA.
4. Examiner les mesures, les erreurs et les effets des réglages.
5. Documenter les décisions et les limites des résultats.

## Résultats rapportés et provenance

Le rapport technique du **31 octobre 2026, page 6**, cite une notice Qwen du **28 octobre** et rapporte :

| Mesure | Débit | Charge précisée dans le rapport |
|---|---:|---|
| Génération de texte | **99,148 tokens/s** | Banc synthétique direct ; longueur générée non précisée |
| Traitement du contexte d’entrée | **666,429 tokens/s** | 4 103 tokens d’entrée |
| Traitement du contexte d’entrée | **779,898 tokens/s** | 16 391 tokens d’entrée |

Ce sont des mesures **rapportées dans une synthèse technique**, pas recalculées ici depuis les journaux bruts. Elles décrivent des opérations et charges différentes et ne sont pas additionnées.

Je décris également une progression globale de **moins de 60 à environ 90 tokens/s** au fil du projet. Cette évolution reste à reconstruire avec des journaux comparables avant d’en déduire un gain quantifié.

[Lire les sources, le statut des chiffres et les limites](MESURES_ET_SOURCES.md)

## Mon rôle et celui des agents

Je définis les objectifs, effectue la veille, sélectionne les pistes, organise les étapes, arbitre et contrôle les résultats.

Les agents logiciels produisent l’essentiel des scripts, adaptations et correctifs sous ma supervision. Le code de ces modifications n’est pas présenté comme un développement que j’aurais réalisé seul.

## Tester et comparer

Le dépôt propose une [fiche de préparation à la reproduction](PROTOCOLE_REPRODUCTION.md). Elle sépare les paramètres connus des informations encore manquantes.

**Cette première version documentaire ne contient pas encore un environnement prêt à lancer.** L’identité et la licence exactes des poids, la révision du moteur adapté, les correctifs et les entrées du banc doivent être établis pour reproduire le même essai.

Les retours utiles concernent la méthode de mesure, la répartition mémoire, la compatibilité matérielle et la clarté du protocole. Une comparaison doit préciser son modèle, sa quantification, son matériel, son moteur et sa charge.

## Portée du projet

Ces travaux sont des expérimentations personnelles. Les éléments disponibles documentent des paramètres et des performances rapportées ; ils ne prouvent pas à eux seuls un gain causal avant/après, une vitesse universelle, une innovation algorithmique ou un déploiement commercial.

Le dépôt ne distribue ni poids de modèles, ni journaux bruts, ni document d’origine, ni code tiers non vérifié. Les clés, adresses réseau, chemins privés et données personnelles sont exclus.
