# CartonTracking

Par Fanny GOBBO, Simon SCHWAAR, Benoit VERDOT

## Principe

Le but de ce projet est de réaliser un tracker GPS en temps réel. Il faut pouvoir connecter 2 machines qui envoient leurs coordonnées à un serveur Kafka central, puis une 4ème machine qui reçoit les données et les affiche en temps réel.

## Adaptations

Au lieu de se déplacer dans une carte de notre monde, nous avons décidé de le faire sur la Terre du Milieu de l'Univers de J. R. R. Tolkien.

## Fonctionnement général

Le backend est en python et le front en angular, on sépare la partie producer de la partie consumer dans des fichiers distincts, et le front à part. Docker compose est utilisé pour séparer les environnements, qui pourraient être sur des machines différentes tant qu'elles partagent le même réseau.

#### Pour lancer le projet :

1. Lancer la commande à la racine du projet :  ./startBroker.sh
2. Lancer la commande à la racine du projet :  ./startConsumer.sh 'ip de la machine centrale'
3. Lancer la commande à la racine du projet :  ./startProducer.sh 'ip de la machine centrale' 'numéro du producer (1 ou 2)' 'nombre de points générés' 'nombre de secondes entre chaque génération'
4. Aller sur l'addresse

Si ces paramètres sont laissés vides, ils ont comme valeur par défaut respectivement 'localhost', '1', '60' et '1'.

À savoir que ces scripts lancent un docker compose en arrière plan, il faudra donc faire 'docker ps' puis docker 'docker stop' et 'docker rm' sur les containers à supprimer. Aussi, il faut laisser vacant le port 9092 (Kafka), 8000 (FastAPI) et 4200 (Angular).

## Fonctionnement du déplacement

Chaque machine va appliquer une fonction de déplacement aléatoire mais contrôlé :

1. Spawn de manière aléatoire sur la carte
2. Commence à se déplacer sur la carte
3. Chaque déplacement dépend du précédent (on prend en compte l'angle de déplacement pour éviter des angles trop erratiques)
4. L'emplitude de l'angle peut aller jusqu'à 360° dans les cas de blocages difficiles.

## Fonctionnement du Kafka

Le fonctionnement est très simple. Chaque producer et consumer sont liés au même topic 'coordinates' et se connectent au broker grâce à l'IP de l'hôte. C'est kafka-python qui permet ce lien ainsi que toutes les fonctionnalités liées aux modules.

Les producer doivent avoir un numéro 1 ou 2 différent entre eux pour être reconnu par le front à l'affichage. 

Le broker est lancé grâce à un docker compose classique, c'est l'image habituelle confluent où je n'ai laissé que le broker pour être plus efficace.

## Fonctionnement du front

Le frontend Angular est assez court par manque de temps mais il reste assez complexe. Nous avons fait le choix de ne pas utiliser de module comme Leaflet car ce n'était pas très bien adapté à notre carte fictive.

La gestion de la carte est donc fait par l'intermédiaire de ses pixels. On a l'image qu'on peut afficher plus ou moins grande selon un paramètre de scale, et on ramplace des blocs de pixels par certaines couleurs pour montrer le tracé des producers.

L'API utilise FastAPI et implémente une WebSocket directement reliée à Kafka. Les messages sont consommés et envoyés juste après dans la socket pour être passés dans un observable et mettre à jour la carte.
