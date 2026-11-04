# Configuration, poids et paramètres Qwen

[Présentation](README.md) · [Mesures et sources](MESURES_ET_SOURCES.md) · [Reproduction](PROTOCOLE_REPRODUCTION.md) · [Provenance et licences](PROVENANCE_ET_LICENCES.md)

**Source des observations locales : audit du 4 novembre 2026, fourni le 5 novembre 2026.** Les caractéristiques du fichier local, de l’installation et des anciens essais ci-dessous sont rapportées par cet audit. Les références publiques et les calculs sur les valeurs transcrites ont été contrôlés séparément pour cette documentation ; le fichier local et les journaux originaux n’ont pas été relus ici.

## Station et système

| Composant | Observation rapportée le 4 novembre 2026 |
|---|---|
| Station | Lenovo ThinkStation P910 |
| CPU | 2 × Intel Xeon E5-2698 v4 |
| Topologie CPU | 40 cœurs physiques, 80 threads logiques, 2 nœuds NUMA, AVX2 |
| RAM vue par Linux | 168 852 533 248 octets, soit 157,256 Gio ou environ 168,853 Go |
| GPU texte | 2 × Tesla V100-PCIE-32GB, 32 768 Mio chacune |
| GPU complémentaire | NVIDIA RTX 4070 SUPER, 12 282 Mio rapportés par NVIDIA-SMI |
| Système | Ubuntu 24.04.5 LTS |
| Noyau lors de l’inventaire | 7.0.0-38-generic |
| Pilote NVIDIA | 580.178.04 |
| Toolkit CUDA | CUDA 12.9 ; nvcc 12.9.86 |

Cet inventaire ne doit pas être attribué rétroactivement à chaque ancien essai. Le noyau initial documenté le 5 octobre était 6.8.0-146-generic ; un inventaire complet n’a pas été retrouvé dans chaque journal individuel.

Les deux V100 exécutent le banc texte. La RTX sert au projecteur d’images à la demande dans le profil vision ; les mesures de génération présentées ne comportent aucune image. La mémoire des GPU reste distincte : additionner leurs capacités ne crée pas une mémoire unifiée.

## Fichier de poids identifié

| Élément | Valeur |
|---|---|
| Fichier | `Qwen3.8-Flash-Next-IQ3E-Q8D-MTP.gguf` |
| Assemblage public | `pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF` |
| Taille | **85 923 705 344 octets**, environ 80 Gio |
| Révision publique de référence | `75e6411f0157bb4b6d492a9868bc93c57d2b061c` |
| SHA-256 | `42506dd921d92af24f3666a6fc1d1c9ec77b998e16684b1d13bef2c77e3e50e8` |
| Licence des poids | **Qwen Community License 1.0** |
| Modèle source | Qwen/Qwen3.8-Flash-Next |

Références : [fichier public épinglé](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP.gguf), [métadonnées publiques à cette révision](https://huggingface.co/api/models/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/revision/75e6411f0157bb4b6d492a9868bc93c57d2b061c?blobs=true), [recette épinglée du fournisseur](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/README.md) et [licence des poids](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/LICENSE).

La taille et le SHA-256 des métadonnées publiques correspondent aux valeurs du rapport. L’audit indique avoir haché intégralement le fichier local le 4 novembre et obtenu la même empreinte. Cette lecture locale n’a pas été refaite pour la présente documentation. Le reçu initial de téléchargement et la révision effectivement utilisée à cette date n’ont pas été retrouvés ; l’identité des octets est établie dans l’audit par l’empreinte.

L’assemblage et les quantifications proviennent du fournisseur tiers. Sa recette cite la révision Unsloth `c8b5954a88c2775c546b92593eda40ea041d3176` et la révision Qwen `de4b8e4d43b917e7706784d8bb445c9af86a3540` pour les tenseurs MTP. Ce projet n’attribue pas leur création au travail d’optimisation P910.

## Architecture et quantification

La [carte officielle Qwen](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) décrit **125B de paramètres avec 6B activés, plus 51B d’embeddings n-gram et 4B MTP**. Ces composants représentent environ 180B de paramètres stockés ; ils ne sont pas tous activés à chaque token.

| Élément du fichier local | Valeur rapportée par l’audit |
|---|---|
| Format | GGUF version 3 |
| Architecture GGUF | `qwen4exp` |
| Nom enregistré | `Qwen3.8 Flash Next` |
| Tenseurs et métadonnées | 1 257 tenseurs ; 65 métadonnées |
| Couches | 48 principales + 1 bloc MTP intégré ; `block_count=49`, `nextn_predict_layers=1` |
| Experts routables | 512, dont 10 sélectionnés par token |
| Contexte déclaré | 262 144 tokens |
| Somme des éléments tensoriels stockés | 180 186 749 568 |

La documentation officielle précise également **un expert partagé** en complément des 10 experts routés. La somme exacte des dimensions des tenseurs provient de l’inspection locale décrite dans l’audit ; elle n’a pas été recalculée ici depuis le GGUF.

| Type de tenseur | Nombre rapporté |
|---|---:|
| F32 | 568 |
| Q8_0 | 516 |
| IQ2_S | 94 |
| IQ4_NL | 49 |
| BF16 | 26 |
| IQ3_S | 2 |
| Q6_K | 1 |
| Q4_0 | 1 |
| **Total** | **1 257** |

L’étiquette IQ3E ne désigne donc pas un format trois bits unique pour tous les tenseurs. Exemples relevés : tête cible `output.weight` en Q6_K, tête de sortie du brouillon MTP en Q4_0, projection MTP en Q8_0 et table PLE en IQ4_NL. Le format du cache KV, décrit plus bas, est distinct de la quantification des poids.

## Moteur et chaîne des adaptations

| Niveau | Provenance et rôle |
|---|---|
| Base | [llama.cpp v0.5.0](https://github.com/ggml-org/llama.cpp/tree/v0.5.0), commit `7fe450e19305b828c199d602c23a8337aaa1f03b` |
| Patch public | [V100 v3 à la révision épinglée](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/patches/llama-v0.5.0-v100-v3.patch) : architecture Qwen, MTP, code FreeToken et optimisations V100 préexistantes |
| Adaptation P910 du 9 octobre | Partage et restauration du cache, transport inter-GPU via la RAM hôte, protections et synchronisation |
| Colocation 22 | Placement cohérent des couches et de leurs experts |
| Argmax du 28 octobre | Variante locale conditionnelle SM70, activée par `LLAMA_V100_ARGMAX_SPLIT=1` |
| Intégration du projet | Lanceurs, contrôles d’empreintes, réglage MTP 64 et qualification, avec assistance d’agents IA |
| Moteur final conservé | Profil `colocate22-argmax-20261028` |

Le moteur final n’a **pas de commit unique disponible** : les copies de sources sont dépourvues de `.git` et signalent `LLAMA_COMMIT="unknown"`. Le seul commit amont ne reconstitue donc pas le résultat. Les patches locaux et leurs dépendances exactes restent nécessaires.

Le patch public v3 est identifié dans l’audit par le SHA-256 `21784053cabd828c5244a284af860e37c61f7d46f2799543fb6a79bb76febce9`. Les empreintes des modifications locales et de l’exécutable sont documentées dans la [provenance](PROVENANCE_ET_LICENCES.md). Une empreinte d’exécutable ne suffit pas à caractériser ses bibliothèques partagées, qui n’ont pas toutes été réhachées pendant l’audit.

Les licences du code sont distinctes de celles des poids : llama.cpp est sous MIT ; les composants FreeToken concernés sont sous Apache-2.0. Les adaptations locales ne permettent pas de revendiquer la création de l’ensemble du moteur.

## Placement et paramètres du profil final

| Paramètre | Réglage documenté |
|---|---|
| Mode de répartition | `--split-mode layer` ; colocation locale réglée à 22 |
| Première V100 | Couches 0–21 et bloc MTP 48 |
| Seconde V100 | Couches 22–47 et tête de sortie cible |
| RTX | Projecteur image F16 à la demande ; aucune couche texte dans cette recette |
| RAM / CPU | Poids mappés, table n-gram/PLE en lecture lazy, transport inter-V100 via la mémoire hôte |
| Cache d’experts | 512 places par banque, associées aux couches |
| Contexte | 200 000 tokens demandés ; **200 192 réservés**, un slot |
| CPU d’exécution | 48 threads de génération et 48 threads de batch ; NUMA distribute |
| Batch / microbatch principal | 2 048 / 512 |
| Cache KV cible | Q8_0 pour K et V |
| Cache KV brouillon | F16 |
| Spéculation | MTP profondeur 3 + `ngram-map-k4v` |
| Sous-lot MTP final | 64, imposé par le wrapper ; un JSON antérieur indique encore 32 |
| Graphes CUDA | Compilés, mais désactivés à l’exécution |

La construction rapportée cible SM70 avec CUDA 12.9, `GGML_NATIVE=ON`, NCCL compilé et des échanges entre les V100 via la RAM hôte. Le profil impose notamment `NCCL_P2P_DISABLE=1`, `GGML_CUDA_HOST_PEER_COPY=1` et `GGML_CUDA_DISABLE_GRAPHS=1`. La présence de NCCL à la compilation ne signifie donc pas que le banc utilise une interconnexion NVLink ou des copies P2P directes.

Un cache de 512 places ne signifie pas que les 85,92 Go du fichier résident intégralement en VRAM. Le contexte de 200 192 tokens est une capacité réservée, pas la longueur effectivement traitée par chaque requête.

## Différences entre les campagnes

| Élément | Colocation du 23 octobre | MTP du 28 octobre |
|---|---|---|
| Moteur | Binaire candidat de cette campagne | Moteur argmax final |
| Comparaison | Colocation absente / réglée à 22 | Sous-lot MTP 32 / 64, colocation 22 |
| Sous-lot MTP de la paire principale | 32 dans les deux bras | 64 pour la valeur finale de 99,148 TG |
| Entrée / génération du test court | 67 / 768 tokens | 73 / 384 tokens |
| Répétitions retenues | Médiane des 3 dernières sur 5 requêtes par variante | Moyenne des médianes de 2 passages de 3 requêtes UB64, après chauffe |
| Cache de prompt | Désactivé | Désactivé |
| RTX / image | RTX exclue | Aucune image dans les mesures |
| Particularités | Argmax récent absent ; pas de projecteur ni de `--no-warmup` | Profil final ; chauffe courte documentée |

Les deux campagnes utilisent des paramètres déterministes et l’effort de raisonnement medium. Les sorties de lecture PP et les sorties courtes TG constituent des mesures distinctes. Les configurations et les protocoles complets accompagnent les [mesures](MESURES_ET_SOURCES.md) et le [protocole de reproduction](PROTOCOLE_REPRODUCTION.md).
