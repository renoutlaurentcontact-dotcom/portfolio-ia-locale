# Examiner et reproduire les essais

[Accueil](README.md) · [Configuration](CONFIGURATION.md) · [Mesures](MESURES_ET_SOURCES.md)

Deux opérations sont proposées : contrôler les calculs avec les données du dépôt, puis préparer une reproduction du banc d’inférence avec les sources et dépendances exactes.

## 1. Vérifier les calculs disponibles immédiatement

Depuis la racine du dépôt, avec Python et sa bibliothèque standard :

    python recalculer_mesures.py

Le programme lit mesures_transcrites.json. Ces données sont transcrites du [rapport d’audit transmis](RAPPORT_AUDIT_2026-11-04.txt) ; elles ne sont pas les journaux originaux. Le programme ne lance pas Qwen, ne change aucun service et n’utilise pas le réseau.

Il permet de vérifier les médianes, le gain de colocation et la moyenne des médianes de la campagne finale. Cette vérification arithmétique est distincte d’une reproduction des performances.

## 2. Identifier les poids

Fichier : Qwen3.8-Flash-Next-IQ3E-Q8D-MTP.gguf.

- Taille : 85 923 705 344 octets.
- SHA-256 attendu : 42506dd921d92af24f3666a6fc1d1c9ec77b998e16684b1d13bef2c77e3e50e8.
- [Fichier public épinglé](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/blob/75e6411f0157bb4b6d492a9868bc93c57d2b061c/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP.gguf).
- [Recette du fournisseur](https://huggingface.co/pentacoxian-dev/Qwen3.8-Flash-Next-IQ3E-Q8D-MTP-GGUF/raw/75e6411f0157bb4b6d492a9868bc93c57d2b061c/README.md).

Le fournisseur décrit un moteur patché : un llama.cpp standard ne suffit pas à charger cet assemblage. Les licences des poids et du code figurent dans [la provenance](PROVENANCE_ET_LICENCES.md). Aucun téléchargement de poids n’a été lancé pour rédiger ce dépôt.

## 3. Reconstituer le moteur concerné

Le point de départ est llama.cpp v0.5.0, commit 7fe450e19305b828c199d602c23a8337aaa1f03b, avec le patch public V100 v3, puis les adaptations locales décrites dans le rapport.

Les sources finales, les trois correctifs locaux et toutes leurs dépendances ne sont pas encore joints au dépôt. Le commit amont et le patch public seuls ne reproduisent pas les résultats P910 présentés ici.

### Construction décrite par l’audit

Les commandes suivantes sont documentaires et n’ont pas été exécutées pour la préparation de ce dépôt. <ENGINE_DIR> et <MODEL_DIR> sont des chemins à adapter sur une installation d’essai.

    cmake -S '<ENGINE_DIR>/source' -B '<ENGINE_DIR>/build-gpu' \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.9/bin/nvcc \
      -DCMAKE_CUDA_ARCHITECTURES=70 \
      -DGGML_CUDA=ON -DGGML_CUDA_NCCL=ON \
      -DGGML_CUDA_CUB_3DOT2=OFF \
      -DGGML_CUDA_FORCE_MMQ=OFF -DGGML_CUDA_FORCE_CUBLAS=OFF \
      -DGGML_BACKEND_DL=OFF -DLLAMA_BUILD_TESTS=OFF \
      -DLLAMA_OPENSSL=ON \
      -DNCCL_INCLUDE_DIR='<ENGINE_DIR>/deps/nccl/include' \
      -DNCCL_LIBRARY='<ENGINE_DIR>/deps/nccl/lib/libnccl.so.2'

    cmake --build '<ENGINE_DIR>/build-gpu' --target llama-server -j8

Le cache décrit GGML_NATIVE=ON, et les commandes CPU comprennent -O3, -march=native et -fopenmp. Le paquet d’exécution comprend également ses bibliothèques partagées.

### Profil final décrit

Le [rapport transmis](RAPPORT_AUDIT_2026-11-04.txt), section 6, contient la commande serveur normalisée et les variables d’environnement. Les paramètres réseau, les authentifications et les identités GPU privées y ont été retirés. Cette transcription ne remplace pas le wrapper original et ses contrôles.

Les points essentiels sont :

| Réglage | Profil final |
|---|---|
| GPU texte | Deux V100 ; couches 0–21 et MTP 48 sur la première, couches 22–47 et tête cible sur la seconde |
| Image | Projecteur F16 sur la RTX à la demande ; aucune couche texte dans cette recette |
| Contexte | 200 000 demandé ; 200 192 réservé ; un slot |
| Threads / NUMA | 48 / 48 de batch ; distribute |
| Batch / microbatch | 2048 / 512 |
| Cache KV | Q8_0 cible ; F16 brouillon |
| Spéculation | MTP profondeur 3 et ngram-map-k4v |
| Sous-lot MTP | 64 dans le wrapper final ; un JSON antérieur contient encore 32 |
| Cache experts | 512 places par banque, associé aux couches |
| Graphes CUDA | Compilés, désactivés à l’exécution |

L’ordre logique des GPU doit correspondre aux deux V100 puis à la RTX pour le profil vision. Les chiffres de génération cités ont été obtenus sans image. La mémoire cumulée des GPU n’est pas une mémoire unique.

## 4. Reproduire la comparaison contrôlée du 23 octobre

Utiliser le binaire candidat de cette campagne et ses correctifs, avec MTP sous-lot 32. La variante argmax finale du 28 octobre et son projecteur ne doivent pas être substitués sans créer une autre expérience.

Comparer uniquement :

| Bras | Variable de colocation |
|---|---|
| OFF | LLAMA_V100_COLOCATE_SPLIT absente |
| split22 | LLAMA_V100_COLOCATE_SPLIT=22 |

Conserver les autres arguments identiques : deux V100, 67 tokens d’entrée mesurés, 768 générés, cache de prompt désactivé, batch 2048, microbatch 512, MTP profondeur 3, température 0 et seed 42. Les autres paramètres et la requête exacte sont transcrits dans le rapport, section 6.

Effectuer cinq requêtes par variante et prendre la médiane des trois dernières comme dans le protocole décrit. Conserver les réponses, les compteurs de tokens et les journaux expurgés ; vérifier l’identité du contenu et du raisonnement des sorties retenues.

Le débit est celui du moteur, avec raisonnement comptabilisé et premier token exclu de son calcul natif. Il doit être interprété avec ces conditions.

## 5. Reproduire la campagne MTP du 28 octobre

Utiliser le moteur colocate22-argmax et la colocation 22 ; comparer sous-lot MTP 32 et 64 à charge identique.

- 73 tokens d’entrée, 384 générés, aucune image et cache désactivé.
- Une chauffe de 32 tokens puis trois requêtes courtes par passage.
- Paramètres déterministes et effort medium décrits dans l’audit.
- Calculer chaque médiane B1/B2 puis leur moyenne, selon le protocole d’origine.
- Documenter l’ordre réellement exécuté : le rapport établit ABAB, pas ABBA.
- Traiter séparément les charges de lecture de 4 103 et 16 391 tokens.

Les scripts d’origine benchmark.py, compare_mtp.py et compare_mtp_ubatch.py gèrent aussi des arrêts/restaurations de services. Leur code complet reste à expurger et à joindre ; ces opérations ne doivent pas être transposées sur une installation en service sans examen préalable.

## 6. Décrire une nouvelle mesure

Préciser les poids et leur empreinte, les révisions et correctifs du moteur, le matériel, les dépendances, les paramètres, les longueurs réellement traitées, la chauffe, les répétitions et la métrique. Conserver les erreurs et régressions, ainsi qu’une vérification des réponses.

Une nouvelle expérience peut être utile même si elle ne reproduit pas exactement ce banc ; elle doit alors être présentée avec ses propres conditions.

[Résultats et limites](MESURES_ET_SOURCES.md) · [Contributions et licences](PROVENANCE_ET_LICENCES.md)
