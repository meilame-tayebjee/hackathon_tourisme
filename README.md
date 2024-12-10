# Hackathon DGE 9-10 Déc. 2024 - Groupe 8
## Rendre le tourisme accessible aux personnes en situation de handicap  

Bienvenue sur le repository de notre projet développé lors du Hackathon DGE des 9-10 décembre 2024.  
L'objectif : rendre le tourisme plus accessible aux personnes en situation de handicap, en proposant des parcours optimisés et personnalisés basés sur des lieux accessibles et de qualité.  

---

## Structure du projet  

Le repository contient deux principaux dossiers :  

1. **`src`**  
   Contient le code source de l'application, incluant les scripts pour :  
   - La gestion des points de départ et des rayons de recherche.  
   - Les appels à l'API Overpass et le traitement des données.  
   - L'optimisation des parcours.  

2. **`api`**  
   Contient les fichiers nécessaires au déploiement de l'API, qui expose les fonctionnalités clés de notre solution.  

---

## Principe de la solution  

Notre application suit les étapes suivantes :  

1. **Définition personnalisée du point de départ et du rayon de recherche**  
   L'utilisateur choisit un point de départ (adresse ou géolocalisation) et un rayon de recherche en kilomètres.  

2. **Filtrage des lieux accessibles avec l'API Overpass**  
   Nous interrogeons l'API Overpass pour obtenir une liste de lieux touristiques marqués comme accessibles en fauteuil roulant (`wheelchair=yes`).  

3. **Croisement des données avec une API de cartes**  
   Les lieux obtenus sont croisés avec des données supplémentaires pour ne garder que ceux ayant :  
   - Un nombre de reviews significatif.  
   - Une note moyenne élevée.  

4. **Génération d'un parcours optimisé**  
   Les lieux filtrés sont ordonnés pour minimiser le temps de marche entre chaque point, en utilisant un algorithme d'optimisation de parcours.  

---

## Installation  

Clonez ce repository :  
   ```bash
   git clone https://github.com/meilame-tayebjee/hackathon_tourisme.git
   cd hackathon_tourisme
   pip install -r requirements.txt
   ```

## Déploiement

L'API a été déployée ici: ```https://hackathon-tourisme.onrender.com/docs```.

