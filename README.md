# CartonTracking

Par Fanny GOBBO, Simon SCHWAAR, Benoit VERDOT

## Principe

Le but de ce projet est de réaliser un tracker GPS en temps réel. Il faut pouvoir connecter 2 machines qui envoient leurs coordonnées à un serveur Kafka central, puis une 4ème machine qui reçoit les données et les affiche en temps réel.

## Adaptations

Au lieu de se déplacer dans une carte de notre monde, nous avons décidé de le faire sur la Terre du Milieu de l'Univers de J. R. R. Tolkien. 

## Fonctionnement du déplacement

Chaque machine va appliquer une fonction de déplacement aléatoire mais contrôlé : 

1. Spawn de manière aléatoire sur la carte
1. Commence à se déplacer sur la carte
1. Chaque déplacement dépends du précédent (on prends en compte l'angle de déplacement pour éviter des angles trop erratiques)



