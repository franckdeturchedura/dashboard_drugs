# Mini Projet Python

Franck Deturche-Dura
Yasmine Djemame

Voici la notice d'utilisation du Dashboard final.

Nous avons utilisé deux datasets : un pour avoir les données sur les drogues et un pour avoir les coordonnées géographiques. Nous les regroupons en un seul dans le script pour pouvoir faire tout ce qu'on veut.

Sur le dashboard vous trouverez également un lien vers le CSV final utilisé (après modification dans le script de l'initial).

Voici le site sur lequel nous avons trouvé notre dataset brut : https://public.tableau.com/profile/umidjon.rahmonberdiev#!/vizhome/WDR2016-Useofdrugs/Full


Pour que le dashboard fonctionne, il faut :
    - Télécharger "Dash3.py" 
    - S'assurer que toutes les librairies sont installées sur la machine
    - Installer ChromeDriver (pour Chrome v78) et changer "l'executable_path", présent dans la variable "d", ligne 21, avec VOTRE path (où se trouve chromedriver sur votre ordinateur)
    - S'assurer d'avoir la version 78 de Google Chrome installée et effective
    - Télécharger dans le répertoire courant de "dash3.py" les fichiers dataset.xlsx (c'est normal, il est converti en csv dans le script) et countries.csv. Les autres sont créés via le script, ils sont disponibles sur le Repo au cas où.
    - Lancer le script avec Python 3.
    - Se connecter à "http://127.0.0.1:8050/" (le chemin est spécifié dans le terminal)

Au cas où il y a un problème lié à Selenium et ChromeDriver pour le scrapping over JS, il existe une version sans selenium. Voilà comment y accéder :
    - Télécharger "dash_without_dynamic.py" dans la branche du même nom et reprendre les étapes citées précédemment.


Nous avons utiisé bootstrap pour le design (via la librairie dash-bootstrap-components)
Dans la navbar :

Vous trouverez un onglet contact avec nos noms et les liens vers nos LinkedIn si existants.
Vous trouverez un bouton pour dowload le fichier csv comme expliqué précédemment.

Il y a un slider et un dropdown pour la map. Les Markers sur la Map vous indique le nom du pays et le rate.
Il y a un dropdown pour les deux graphes.
Vous pouvez également accéder au Git via le bouton 'View Git'.
Avec le bouton "Actualiser", vous pouvez connaître en temps réel la quantité d'argent dépensée dans les drogues illégales depuis le début de l'année dans le monde.


Description - Analyse (Check ReadMe to see more):
    Nous constatons que via la Map que les drogues douces (cannabis) sont bien plus présentes que les drogues dures (les autres). 
    Les pays développés sont globalement bien plus concernés que les pays pauvres ou en voie de développement. 
    Les drogues dures comme la cocaine sont bien présentes dans les pays en voie de développement comme le Brésil. 
    Concernant la Map, nous pouvons nuancé car les données sont clairement irrégulières d'année en année. 
    Pour observer correctement, il faut se placer dans le cas "all", où toutes les années sont prises en compte. 
    Nous constatons grâce au Scatter que le taux de consommation du cannabis est bien plus éparses (jusqu'à 15%) que pour les drogues dures où les % restent très faibles (plutôt entre 1 et 3%). 
    Nous constatons via la donnée dynamique que l'argent dépensé dans la drogue depuis le début de l'année représente une somme colossale, montrant que nous sommes loin de la fin de la guerre contre les drogues. 
    L'histogramme nous donne des renseignements concernant l'utilisation des drogues selon les années. 
    Comme spécifié précédemment, nous le dataset n'étant pas complet à la base, l'histogramme n'est pas aussi pertinent que prévu.
    Sur le dashboard R, nous avons opté pour un autre dataset permettant une observation via Histogramme bien plus pertinente.
    
    
    
    