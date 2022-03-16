# D&N DIG
Day&Night Dataset Image Generator utilise [le simulateur CARLA](https://carla.org/) pour générer des paires d'images jour/nuit.

## Dossier sources:
	config.py        configuration des paramètres
	evaluation_DB.py score de ressemblance pour les paires d'une DB
	daynightdl.py    bibliothèque générale pour le projet
	step0.py         vérifie que l'on puisse initialiser une voiture
	step1.py         vérifie la synchronisation des capteurs (image jour uniquement)
	step2A.py        enregistrement des images jours puis rejoue la même simulation en nuit
	step2B.py        enregistrement des images jours et nuit en même temps
	step2C.py	 joue des simulations déterministes
