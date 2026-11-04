# Qwen sur deux Tesla V100 — optimisation sur Lenovo P910

**Une comparaison contrôlée rapporte un passage de 83,964 à 95,608 tokens/s en génération, soit +13,87 %, sur deux Tesla V100 PCIe de 32 Go.**

Ce projet, piloté par **Laurent Renout avec l’assistance d’agents IA**, cherche à améliorer l’exécution de Qwen3.8-Flash-Next sur une station existante. Le travail porte sur le placement du calcul et des experts, les échanges entre GPU et les réglages du moteur, en tenant compte des contraintes de mémoire et de l’interconnexion du P910.

L’objectif : transformer un besoin en essais mesurables, sélectionner les adaptations utiles et documenter ce qui permet de comparer les résultats.

## Résultat principal : colocation des couches et des experts

La campagne du **23 octobre 2026** compare le même fichier de poids et le même binaire, avec la colocation désactivée puis activée à la séparation de couche 22. Les deux V100 assurent le calcul ; la RTX n’intervient pas dans ce banc texte.

| Génération courte | Colocation désactivée | Colocation 22 | Évolution |
|---|---:|---:|---:|
| Débit médian | 83,964 tokens/s | 95,608 tokens/s | **+13,87 %** |

Conditions rapportées : **67 tokens d’entrée, 768 générés**, cache de prompt désactivé, paramètres déterministes, MTP de profondeur 3. Chaque variante comporte cinq requêtes ; la médiane porte sur les trois dernières après exclusion des deux premières du score stable. Les six réponses retenues ont un contenu et un raisonnement identiques selon l’audit.

Un test distinct de traitement d’entrée, sur **37 475 tokens réellement lus**, rapporte **593,857 → 668,949 tokens/s**, soit **+12,64 %**. Ses générations diffèrent : cette mesure reste séparée de la comparaison courte à sorties identiques.

## Mesure finale distincte : 99,148 tokens/s

La campagne du **28 octobre** rapporte **99,148 tokens/s** avec le moteur final, un placement colocation 22 et un sous-lot MTP de 64. Il s’agit de la **moyenne des médianes de deux passages de trois requêtes**, avec 73 tokens d’entrée et 384 générés, après chauffe.

Cette valeur n’est pas un pic isolé. Elle ne mesure toutefois pas un gain causal depuis 95,608 : les deux campagnes ont des entrées, longueurs de sortie, moteurs et protocoles différents. Le seul passage MTP 32 → 64 laisse la génération pratiquement inchangée (**+0,035 %**) ; ses petits gains de lecture sont détaillés dans les [mesures et sources](MESURES_ET_SOURCES.md).

Les débits de génération incluent le raisonnement produit par le modèle. Ils ne garantissent ni le débit visible dans une application, ni une performance identique sur toute tâche. La progression historique « moins de 60 → environ 90 » ne dispose pas d’une paire avant/après comparable retrouvée.

## Matériel et poids identifiés

| Élément | Configuration du projet |
|---|---|
| Station | Lenovo ThinkStation P910 |
| CPU | 2 × Intel Xeon E5-2698 v4 — 40 cœurs physiques, 80 threads logiques |
| Mémoire vue par Linux | 157,256 Gio, soit environ 168,853 Go |
| GPU du banc texte | 2 × NVIDIA Tesla V100 PCIe de 32 Go chacune |
| GPU complémentaire | RTX 4070 SUPER pour le projecteur d’images à la demande, hors banc texte |
| Poids | `Qwen3.8-Flash-Next-IQ3E-Q8D-MTP.gguf` — 85 923 705 344 octets |
| Moteur | llama.cpp v0.5.0, patch public V100 v3 et adaptations locales P910 |

La fiche officielle décrit **125B de paramètres avec 6B activés, auxquels s’ajoutent 51B d’embeddings n-gram et 4B MTP**. Le modèle complet ne doit donc pas être résumé à « 125B de paramètres totaux ». La référence publique du GGUF, son empreinte et ses licences sont renseignées dans la [configuration détaillée](CONFIGURATION.md).

## Contribution et attribution

**Mon rôle :** définir les objectifs et les contraintes, rechercher et sélectionner les approches, coordonner les étapes et les agents, arbitrer les essais et contrôler les résultats.

**Rôle des agents IA :** produire l’essentiel du code, des adaptations, scripts, correctifs et contrôles techniques sous ma supervision.

Le modèle Qwen, l’assemblage et les quantifications du GGUF, llama.cpp et le patch public V100 sont des composants tiers. Les adaptations du projet P910 concernent notamment le transport inter-GPU via la mémoire hôte, la colocation des couches et de leurs experts, une variante argmax conditionnelle pour SM70, les lanceurs et la qualification des réglages. Le projet ne revendique ni la création de tout le moteur, ni le réentraînement des poids. Voir la [provenance et les licences](PROVENANCE_ET_LICENCES.md).

## Vérifier les chiffres et préparer un essai

- [Configuration, poids et paramètres](CONFIGURATION.md).
- [Mesures, conditions et sources](MESURES_ET_SOURCES.md).
- [Protocole de reproduction et éléments manquants](PROTOCOLE_REPRODUCTION.md).
- [Provenance des composants et licences](PROVENANCE_ET_LICENCES.md).
- [Valeurs transcrites](mesures_transcrites.json) et [outil de recalcul des statistiques](recalculer_mesures.py).

L’outil recalcule les statistiques depuis les valeurs transcrites ; il ne lance aucune inférence et ne remplace pas l’examen des résultats originaux. Pour reproduire l’environnement complet, il reste à verser les patches locaux, les scripts originaux et les dépendances exactes. Le moteur final n’a pas de commit unique permettant de le reconstituer à partir du seul amont.

**Provenance des observations locales : audit du 4 novembre 2026, fourni le 5 novembre 2026.** La présente documentation exploite cet audit ; ses auteurs ont vérifié les références publiques et les calculs à partir des valeurs transcrites, sans relire ici les journaux originaux ni recalculer le SHA-256 du fichier local. Les bancs utilisent des répétitions limitées et ne remplissent pas la fenêtre réservée de 200 192 tokens. Les limites complètes accompagnent les [mesures](MESURES_ET_SOURCES.md).

Les retours utiles portent sur le placement mémoire, la compatibilité V100, les protocoles de mesure et la reproductibilité. Le dépôt contient de la documentation et des données transcrites, sans poids de modèle, journaux bruts ni informations privées.
