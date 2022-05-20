import numpy as np
import random
import argparse
import Parser
import time
import copy


def generate_first_solution_PPV(graphe, v_depart=None):
     # Faire une copie du graphe vu qu'il va subir des modification
    _graphe = graphe.copy()
    # La liste chemin garde trace de notre parcour
    chemin = []
    # Selection d'1 point de depart
    if v_depart is None:
        depart = v_depart = np.random.randint(0, len(graphe))
    depart = v_depart
    # Ajouter le point de depart au chamin de parcour
    chemin.append(v_depart)
    # Création de l'ensemble des noeuds non visités
    noeudsNonVisite = set(
        np.delete(np.arange(0, len(graphe)), v_depart).flatten())
    cout = 0
    while (len(noeudsNonVisite) != 0):
        # Retourne le plus proche voisin
        v_suivante = np.argmin(_graphe[v_depart, :])
        # màj du chemin
        chemin.append(v_suivante)
        # màj du cout
        cout += _graphe[v_depart, v_suivante]
        # Aller au prochain neoud
        noeudsNonVisite.remove(v_suivante)
        v_depart = v_suivante
        # De/vers les noeuds deja visité a l'infini
        _graphe[v_depart, chemin] = float("inf")
        _graphe[chemin, v_depart] = float("inf")

    # Ajouter le cout de retour
    cout += graphe[v_suivante, depart]

    return chemin, cout


def trouver_voisinage(solution, matrice):
    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[idx1+1 :-1]:
            idx2 = solution.index(kn)
            # Calcul du voisin
            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0
            for i in range(len(matrice)):
                #Calculer le cout du voisin 
                distance += matrice[_tmp[i - 1]][_tmp[i]]

            _tmp.append(distance)

            #Ajouter le resultat à la liste des voisins 
            neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1
    # Trier les voisins suivant leurs couts 
    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def recherche_tabou(matrice, iters, size, start_node=None):
    # Generation de la solution initiale
    solution, best_cost = generate_first_solution_PPV(matrice, start_node)
    # Initialisation de la liste tabou
    tabu_list = list() 
    best_solution_ever = solution
    # Repeter pour un nombre d'iterations predefinie
    for count in range(iters): 
        # Generation des voisins de la solution
        neighborhood = trouver_voisinage(solution, matrice)
        # commencer par le voisin avec le cout le plus minimal
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while found is False:
            
            if best_solution not in tabu_list:
                #si la solution n'existe pas a la liste tabou
                tabu_list.append(best_solution[1: -2])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = neighborhood[index_of_best_solution]

        if len(tabu_list) >= size:
            _ = tabu_list.pop(0)

    return best_solution_ever, best_cost


if __name__ == '__main__':
    # Préparation des données 
    parser = argparse.ArgumentParser()
    parser.add_argument("instance")
    parser.add_argument("--iterations",
                        help="Number of Iterations", )
    parser.add_argument("--size",
                        help="Size of Tabu List", )
    parser.add_argument("--start",
                        help="Starting Node", default=0)
    args = parser.parse_args()
    instance = Parser.TSPInstance(args.instance)
    instance.readData()
     # Lancer le chrono 
    start_time = time.time()
     # Debut
    tour, cost = recherche_tabou(np.array(instance.data), iters=int(
        args.iterations), size=int(args.size), start_node=int(args.start))
    end_time = time.time()
     # fin
    print(tour)
    print(cost)
    print(end_time - start_time)
