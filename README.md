# D&N DIG

![alt text](https://github.com/Yaceee/dn-dig/blob/master/sources/gui/img/logo_dn_titre.png)

Day&Night Dataset Image Generator utilise [le simulateur CARLA](https://carla.org/) pour générer des paires d'images jour/nuit. Cet outil a été développé dans le cadre du projet DayNight DL, projet étudiant visant à modifier l'éclairage naturel d'une image (jour ou nuit) par le biais d'une intelligence artificielle.

## Installation

Le programme nécessite l'installation de Python ainsi que du module [Carla](https://carla.readthedocs.io/en/latest/start_quickstart/#install-client-library). Pour utiliser l'interface graphique, il est nécessaire d'installer npm, et de lancer la commande 
```bash
$ npm install
```
dans le répertoire sources.

## Lancement

Au préalable, vous devez lancer et configurer le simulateur Carla. Pour lancer l'interface graphique, placez vous dans le dossier sources et entrer la commande :

```bash
$ python gui.py
```

## Dossier sources:
	config.py        configuration des paramètres
	daynightdl.py    bibliothèque générale pour le projet
	evaluation_DB.py score de ressemblance pour les paires d'une DB
	gui.py           interface graphique de l'application
	simThread.py     lanceur de thread des simulations
	simulation.py    lancement de la simulation et génération des images
	
