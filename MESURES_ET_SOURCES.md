# Mesures, sources et limites

[Retour à la présentation](README.md)

## Source technique examinée

Document : **« DeepSeek sur le P910 — Rapport de passation et de comparaison pour une autre IA »**, daté du **31 octobre 2026**, version 1.0, 19 pages.

Le passage Qwen figure en **page 6**, dans la section « Moteur local et référence Qwen ». Il cite une **notice finale Qwen du 28 octobre**. Le document est une synthèse ; la notice et les journaux d’origine ne sont pas fournis dans ce dépôt.

## Mesures reprises de cette source

| Opération | Débit rapporté | Contexte indiqué |
|---|---:|---|
| Génération | 99,148 tokens/s | Banc synthétique direct |
| Traitement du contexte | 666,429 tokens/s | 4 103 tokens d’entrée |
| Traitement du contexte | 779,898 tokens/s | 16 391 tokens d’entrée |

Les anciens débits de 87–88 tokens/s mentionnés dans le passage proviennent d’autres demandes. Ils ne constituent pas une référence avant/après strictement comparable à ce banc.

Le passage ne donne pas le prompt complet, la longueur générée, le nombre de répétitions, la dispersion des mesures ni une commande complète de reproduction. La page 19 du rapport précise que les anciens débits ont été relus dans des notices et que tous les journaux bruts n’ont pas été recalculés.

## Autres informations, à conserver séparément

- **Progression globale déclarée par Laurent :** moins de 60 vers environ 90 tokens/s. Les conditions du point de départ et du point d’arrivée restent à rapprocher.
- **Campagne ponctuelle rapportée par la passation du 4 novembre :** 83,964 vers 95,608 tokens/s, avec un gain annoncé de 13,87 %. Le rapport du 31 octobre ne démontre pas cette comparaison ; ses traces propres restent à retrouver.

Ces deux éléments ne sont ni fusionnés avec le banc ci-dessus, ni additionnés. Aucun pourcentage global exact n’est déduit de valeurs approximatives.

## Ce que les éléments disponibles permettent d’évaluer

- Une recette de configuration rapportée pour deux V100.
- Une démarche de pilotage, d’expérimentation et de lecture critique des mesures.
- Des performances relatées avec une provenance identifiée.

Ils ne suffisent pas encore à établir une reproduction indépendante, l’origine de chaque gain, la qualité des réponses sur toutes les tâches, la stabilité générale ou une utilisation en production.

[Configuration](CONFIGURATION.md) · [Protocole à compléter](PROTOCOLE_REPRODUCTION.md)
