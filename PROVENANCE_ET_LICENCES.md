# Provenance, contributions et licences

[Accueil](README.md) · [Configuration](CONFIGURATION.md) · [Mesures](MESURES_ET_SOURCES.md)

## Rôle de Laurent Renout

Laurent définit l’objectif et les contraintes, recherche les approches disponibles, sélectionne les pistes, organise les essais avec les agents IA, arbitre et vérifie les livrables.

Les agents produisent l’essentiel des scripts, adaptations et correctifs sous sa supervision. Le projet documente une intégration et une optimisation locales ; les composants tiers conservent leur attribution.

## Poids : un assemblage tiers identifié

- [Modèle source Qwen](https://huggingface.co/Qwen/Qwen3.8-Flash-Next).
- [Assemblage GGUF de pentacoxian-dev](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF).
- [Recette du fournisseur épinglée](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/raw/75e6411f0157bb4b6d492a9868bc93c57d2b061c/README.md).
- Révision GGUF consultée : 75e6411f0157bb4b6d492a9868bc93c57d2b061c.
- Source Unsloth annoncée par le fournisseur : c8b5954a88c2775c546b92593eda40ea041d3176.
- Source Qwen des tenseurs MTP annoncée : de4b8e4d43b917e7706784d8bb445c9af86a3540.

La recette publique décrit un mélange de tenseurs Unsloth et une tête MTP issue du checkpoint Qwen. La création de ces poids et leur quantification ne sont pas attribuées à Laurent. La correspondance entre le fichier public et le fichier local est attestée par l’audit transmis : même taille et même SHA-256. La révision utilisée lors du téléchargement local initial n’a pas été retrouvée.

## Chaîne du moteur

| Composant | Provenance et rôle |
|---|---|
| llama.cpp v0.5.0 | Base tierce, commit 7fe450e19305b828c199d602c23a8337aaa1f03b |
| Patch public V100 v3 | Architecture Qwen, MTP, composants FreeToken et optimisations V100 existantes |
| Adaptation locale du 9 octobre | Intégration P910 : partage/restauration du cache, transport inter-GPU via RAM, protections et synchronisation |
| Colocation22 | Placement cohérent des couches et de leurs experts ; comparaison contrôlée décrite dans les mesures |
| Argmax du 28 octobre | Variante locale conditionnelle SM70, activée par LLAMA_V100_ARGMAX_SPLIT |
| Lanceurs, qualification et réglage MTP64 | Intégration et essais du projet P910 réalisés avec assistance d’agents IA |

Sources publiques : [commit de base](https://github.com/ggml-org/llama.cpp/commit/7fe450e19305b828c199d602c23a8337aaa1f03b), [patch V100 v3](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/patches/llama-v0.5.0-v100-v3.patch).

Le moteur final conservé est désigné colocate22-argmax-20261028. Selon l’audit, les copies de sources finales ne disposent pas d’un historique Git complet et leur identifiant de construction est « unknown ». **Le commit amont seul ne reconstitue pas ce moteur final.** Les correctifs locaux et les dépendances restent à joindre pour une reproduction complète.

### Empreintes rapportées pour les artefacts locaux

Ces empreintes proviennent du recalcul décrit dans l’audit du 4 novembre ; les artefacts locaux ne sont pas distribués ici.

| Artefact | SHA-256 rapporté |
|---|---|
| Patch public v3 conservé | 21784053cabd828c5244a284af860e37c61f7d46f2799543fb6a79bb76febce9 |
| engine-changes.patch | e4448cee23d9c1501e18bb04108645fa0306a7aa5cf1f9ea60917dc20e04afc8 |
| colocate-split22.patch | ed2a8aeb345b985fb68eb1955a357d7903e0e79ee1142c7b17ffe7a8283402cd |
| argmax.patch | 224aaacd682208d0a4b34c2edccbe19f6b9fd77a7a7907fe53fca868562d6aaf |
| Exécutable llama-server final | c3601cdc5fc3eae061ffc29efface69bdbcafc456bc5cdde29c63b2ead4441b8 |

L’exécutable dépend de bibliothèques partagées ; son empreinte ne caractérise donc pas à elle seule l’ensemble du moteur. Toutes les bibliothèques n’ont pas été réhachées pendant l’audit.

## Licences à distinguer

| Élément | Licence indiquée par sa source |
|---|---|
| Poids Qwen et assemblage GGUF | [Qwen Community License 1.0](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/main/LICENSE) |
| llama.cpp | [MIT](https://github.com/ggml-org/llama.cpp/blob/v0.5.0/LICENSE) |
| Composants FreeToken repris | [Apache-2.0](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/raw/75e6411f0157bb4b6d492a9868bc93c57d2b061c/patches/LICENSE-freetoken) |

Ces licences ont des périmètres distincts. Le dépôt ne distribue pas les poids et ne les présente pas comme étant sous MIT ou Apache-2.0. Les conditions des sources doivent être conservées lors de toute utilisation ou redistribution.

L’outil de recalcul documentaire du dépôt a été préparé avec assistance d’agents IA sous supervision de Laurent ; il ne contient pas les correctifs du moteur d’inférence.

## Ce qui reste à publier pour une reproduction indépendante

- Les correctifs locaux exacts et leur ordre d’application, après relecture et vérification des droits.
- Les scripts de banc d’origine, débarrassés des paramètres privés et des opérations de gestion de services.
- Les résultats JSON et extraits de journaux expurgés permettant de vérifier la transcription.
- Un manifeste des dépendances, bibliothèques et inventaires système propres aux passages concernés.

[Rapport d’audit transmis](RAPPORT_AUDIT_2026-11-04.txt) · [Reproduction](PROTOCOLE_REPRODUCTION.md)
