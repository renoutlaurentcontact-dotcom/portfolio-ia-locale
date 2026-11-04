# Configuration et paramètres Qwen

[Retour à la présentation](README.md)

## Matériel et système décrits pour le projet

- Lenovo ThinkStation P910.
- Deux Intel Xeon E5-2698 v4 : 40 cœurs et 80 threads au total.
- Environ 170 Go de RAM DDR4 ECC installée.
- Deux NVIDIA Tesla V100 PCIe, 32 Go de VRAM chacune.
- Une RTX 4070 SUPER de 12 Go, utilisée séparément selon les tâches ; sa participation aux mesures Qwen n’est pas établie.
- Ubuntu 24.04 LTS.

Ces données proviennent des informations de projet et doivent être rapprochées des relevés du banc au moment des essais. La VRAM cumulée des GPU ne doit pas être assimilée à une mémoire unique.

## Modèle : informations de projet à confirmer

La désignation fournie est **Qwen3.8-Flash-Next**, annoncé autour de **125 milliards de paramètres totaux**. La passation mentionne un GGUF à quantification mixte IQ3E / Q8D avec MTP.

L’identité fournisseur, la fiche du modèle, la quantification effective, l’empreinte du fichier et sa licence restent à confirmer. Un nom de fichier ne suffit pas à établir ces informations.

## Paramètres explicitement repris du rapport du 31 octobre

La page 6 cite une notice Qwen du 28 octobre :

| Paramètre | Valeur rapportée |
|---|---|
| Désignation dans ce passage | Qwen Flash-Next |
| Répartition | split22 sur les deux V100 |
| Slot configuré | 200 192 tokens |
| Batch | 2 048 |
| Microbatch | 512 |
| Cache KV | Q8 |
| Profondeur MTP | 3 |
| Sous-lot de rattrapage MTP retenu | 64 |
| Taille du GGUF évoqué | 85 923 705 344 octets, environ 80 Gio |

Le slot représente une capacité configurée, pas la longueur de chaque entrée mesurée. Les détails exacts de split22 et les options du moteur adapté doivent être explicités avant reproduction.

Les versions de moteur et de CUDA évoquées pour DeepSeek dans le rapport ne sont pas attribuées à Qwen.

[Sources et mesures](MESURES_ET_SOURCES.md) · [Préparer un essai comparable](PROTOCOLE_REPRODUCTION.md)
