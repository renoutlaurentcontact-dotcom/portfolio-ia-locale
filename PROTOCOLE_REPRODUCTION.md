# Préparer une reproduction et une comparaison

[Retour à la présentation](README.md)

Cette fiche décrit les informations à réunir pour reproduire le cas Qwen. Elle ne prétend pas fournir une commande prête à lancer sur une autre machine.

## 1. Identifier exactement l’environnement

- Confirmer l’identité fournisseur et la version du modèle.
- Relever le format, la quantification, la taille et l’empreinte des poids.
- Vérifier la licence et obtenir les poids depuis une source autorisée ; aucun poids n’est distribué ici.
- Identifier la source et la révision exactes du moteur adapté, les correctifs, les options de compilation et les dépendances.
- Relever le matériel réellement utilisé par le banc, la RAM disponible et le placement mémoire.

Les paramètres actuellement connus figurent dans [CONFIGURATION.md](CONFIGURATION.md). La signification et l’implémentation de split22 doivent être explicitées.

## 2. Fixer une charge comparable

Pour chaque essai, conserver :

- Une entrée redistribuable et sa longueur en tokens.
- La longueur de génération et les paramètres d’échantillonnage.
- Le contexte, le batch, le microbatch et la configuration du cache KV.
- Les GPU utilisés et le partage des opérations CPU / GPU.
- L’activation effective de MTP et ses réglages.
- La définition de la métrique et le périmètre du chronométrage.

Comparer séparément le traitement du contexte et la génération.

## 3. Mesurer et conserver les résultats

- Définir un point de référence.
- Décrire précisément la modification évaluée.
- Conserver les autres conditions identiques autant que possible.
- Prévoir une chauffe et plusieurs répétitions, en précisant le protocole.
- Rapporter la moyenne, la variabilité, les erreurs et les éventuelles régressions.
- Vérifier le comportement des réponses ; la vitesse seule ne suffit pas.
- Conserver des extraits nettoyés des sorties permettant de relier chaque chiffre à son essai.

Aucun nouveau benchmark n’a été exécuté pour préparer cette documentation.

## Tableau à renseigner

| Élément | Référence | Après modification |
|---|---|---|
| Modèle et quantification | À renseigner | À renseigner |
| Révision du moteur et correctifs | À renseigner | À renseigner |
| Charge d’entrée et longueur générée | À renseigner | À renseigner |
| Paramètres et placement mémoire | À renseigner | À renseigner |
| Nombre de répétitions | À renseigner | À renseigner |
| Débit moyen et variabilité | À renseigner | À renseigner |
| Vérifications fonctionnelles | À renseigner | À renseigner |
| Source des résultats nettoyés | À renseigner | À renseigner |

## Partager un retour

Décrire le matériel, le modèle, le moteur, la charge, les paramètres et les résultats obtenus. Retirer avant partage les clés, adresses réseau, noms de machines, chemins privés, données personnelles et entrées confidentielles.

[Mesures déjà rapportées et leurs limites](MESURES_ET_SOURCES.md)
