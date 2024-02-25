import os
########################################
##     Projet INF402 : TAKUZU
##     Groupe : INM2
##     Version: 1.0
#######################################
from z3 import *
from itertools import combinations

# init(r"D:\z3-4.8.15-x64-win\bin\libz3.dll")

# regle 1
def genererClausesRegle1(taille):
    regle1 = []
    for row in range(1, taille + 1):
        for n in range(3, taille):  # plus de n cas identique
            for i in range(1, taille + 2 - n):  # commence par i
                row_item1 = []  # positif
                row_item2 = []  # negatif
                col_item1 = []  # positif
                col_item2 = []  # negatif
                for j in range(0, n):
                    # print("" + str(i+j) + "_" + str(row))
                    row_item1.append(((row - 1) * taille + (i + j)))
                    row_item2.append(-((row - 1) * taille + (i + j)))
                    col_item1.append(((i + j - 1) * taille + row))
                    col_item2.append(-((i + j - 1) * taille + row))
                regle1.append(row_item1)
                regle1.append(row_item2)
                regle1.append(col_item1)
                regle1.append(col_item2)
    return regle1


def combineList(list, k):
    result = []
    for c in combinations(list, k):
        result.append(c)
    return result


# k parmi n
def combine(k, n):
    list = [i for i in range(1, n + 1)]
    return combineList(list, k)


def combineTrois(n):
    result = []
    list = [i for i in range(1, n + 1)]
    for c in combinations(list, 3):
        if c[1] - c[0] == 1 and c[2] - c[1] == 1:
            continue
        result.append(c)
    return result


# regle 2
def genererClausesRegle2(taille):
    regle2 = []
    k = taille // 2 + 1
    arr = combine(k, taille)

    for row in range(taille):
        for i in range(len(arr)):
            item1 = []
            item2 = []
            regle2.append(item1)
            regle2.append(item2)
            for j in range(len(arr[i])):
                item1.append(arr[i][j] + row * taille)
                item2.append(-(arr[i][j] + row * taille))

    for col in range(taille):
        for i in range(len(arr)):
            item1 = []
            item2 = []
            regle2.append(item1)
            regle2.append(item2)
            for j in range(len(arr[i])):
                item1.append((arr[i][j] - 1) * taille + col + 1)
                item2.append(-((arr[i][j] - 1) * taille + col + 1))
    return regle2

# Regle3
def genererClausesRegle3(taille):
    #l_diff_pos = [[], [3], [2], [1], [1, 3], [1, 2], [2, 3], [1, 2, 3]]
    l_diff_pos = [()]
    for i in range(1, taille):
        l_cmb = combine(i, taille-1)
        for j in range(len(l_cmb)):
            l_diff_pos.append(l_cmb[j])
    #print("l_diff_pos:", l_diff_pos)

    #l_rows = [ [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4] ]
    l_groupe = combine(2, taille)
    #print("l_rows:",l_rows)

    regle3 = []
    # pour tous les deux rows
    for i in range(len(l_groupe)):
        # t_diff = remplaceRow(l_diff, l_rows[i][0], l_rows[i][1])
        for j in range(len(l_diff_pos)):
            r1_max = l_groupe[i][0] * taille
            r2_max = l_groupe[i][1] * taille
            clauses_1 = [-r1_max, -r2_max]
            clauses_2 = [r1_max, r2_max]
            regle3.append(clauses_1)
            regle3.append(clauses_2)
            for k in range(taille):
                id1 = (l_groupe[i][0] - 1) * taille + k + 1
                id2 = (l_groupe[i][1] - 1) * taille + k + 1
                if id1 == r1_max or id2 == r2_max:
                    continue
                if l_diff_pos[j].count(k + 1) > 0:
                    clauses_1.append(id1)
                    clauses_1.append(id2)
                    clauses_2.append(id1)
                    clauses_2.append(id2)
                else:
                    clauses_1.append(-id1)
                    clauses_1.append(-id2)
                    clauses_2.append(-id1)
                    clauses_2.append(-id2)
            if len(clauses_1)!=taille*2 or len(clauses_2)!=taille*2:
                print("Erreur:",i," ",j)

    # pour tous les deux cols
    for i in range(len(l_groupe)):
        # t_diff = remplaceRow(l_diff, l_rows[i][0], l_rows[i][1])
        for j in range(len(l_diff_pos)):
            index_s = taille*(taille-1)
            c1_max = l_groupe[i][0] + index_s
            c2_max = l_groupe[i][1] + index_s
            clauses_1 = [-c1_max, -c2_max]
            clauses_2 = [c1_max, c2_max]
            regle3.append(clauses_1)
            regle3.append(clauses_2)
            for k in range(taille):
                id1 = l_groupe[i][0] + (taille*k)
                id2 = l_groupe[i][1] + (taille*k)
                if id1 == c1_max or id2 == c2_max:
                    continue
                if l_diff_pos[j].count(k + 1) > 0:
                    clauses_1.append(id1)
                    clauses_1.append(id2)
                    clauses_2.append(id1)
                    clauses_2.append(id2)
                else:
                    clauses_1.append(-id1)
                    clauses_1.append(-id2)
                    clauses_2.append(-id1)
                    clauses_2.append(-id2)
            if len(clauses_1) != taille*2 or len(clauses_2) != taille*2:
                print("Erreur:", i, " ", j)
            #print(clauses_1)
            #print(clauses_2)

    return regle3


def printRegle(regle):
    print("len:", len(regle))
    for i in range(len(regle)):
        item = regle[i]
        print("(", end="")
        n = len(item)
        for j in range(n):
            print(item[j], end="")
            '''
            if item[j] < 0:
                print("-x"+str(-item[j]), end="")
            else:
                print("x"+str(item[j]), end="") '''
            if j < n - 1:
                print(" + ", end="")
        print(") . ", end="")
        if i + 1 % 4 == 0:
            print("\n")
    print("\n")


def printRegleFormCNF(regle, taille):
    print("p cnf ", str(taille * taille), len(regle))
    for i in range(len(regle)):
        item = regle[i]
        n = len(item)
        for j in range(n):
            print(item[j], end=" ")
        print("0")
    print("\n")


def printGrill(data, taille, enCouleur):
    for i in range(taille):
        print(" ", end="")
        for k in range(taille):
            print("------", end="")
        print("")
        for j in range(taille):
            n = data[i * taille + j]
            if j == 0:
                print("|  " if n >= 10 else "|  ", end="")
            else:
                print(" |  " if n > 10 else "  |  ", end="")
            if n == -1:
                print(" ", end="")
            else:
                print(str(n), end="")
            if j == taille - 1:
                print(" |" if n >= 10 else "  |")
    print(" ", end="")
    for k in range(taille):
        print("------", end="")
    print("\n")

# pour aider à saisir plus pratique
def printGrillAvecIndex(taille):
    data = range(1, taille*taille+1)
    printGrill(data, taille, False)

def saveCNFFile(regles, data, taille, filename):
    n = 0
    for i in range(len(regles)):
        n = n + len(regles[i])
    file = open(filename, "w")
    # c  takuzu.cnf
    # c
    # p cnf 16 39
    file.write("c takuzu.cnf\n")
    file.write("c \n")
    file.write("p cnf " + str(taille * taille) + " " + str(n) + "\n")
    for k in range(len(regles)):
        for i in range(len(regles[k])):
            for j in range(len(regles[k][i])):
                file.write(str(regles[k][i][j]) + " ")
            file.write("0\n")
    #for i in range(len(r2)):
    #    for j in range(len(r2[i])):
    #        file.write(str(r2[i][j]) + " ")
    #    file.write("0\n")
    for i in range(len(data)):
        if data[i]==0:
            file.write(str(-(i+1)) + " 0\n")
        elif data[i]==1:
            file.write(str(i+1) + " 0\n")
    file.close()

# lire un ficher .tkz
def loadJeuFile(filepath):
    file = open(filepath, "r")
    instance = []
    taille = eval(file.readline())
    print(" >> jeu loaded:" + str(taille) + "x" + str(taille))
    l = file.readline()
    while l != "":
        if len(l.strip()):
            instance.append(l.strip())
        l = file.readline()
    file.close()
    return taille, instance

# save les données dans un fichier au format .tkz
def saveJeuFile(data, taille, filepath):
    print(" >> jeu saved:" + str(taille) + "x" + str(taille))
    file = open(filepath, "w")
    file.write(str(taille)+"\n")
    for i in range(len(data)):
        if data[i] == 0:
            file.write(str(-(i+1))+"\n")
        elif data[i] == 1:
            file.write(str(i + 1) + "\n")
    file.close()

def genererCNF(taille, data, filename, regles_ck):
    '''
    :param taille: taille du jeu, comme 4 pour 4x4
    :param data: data d'une isntance à résoudre
    :param filename: path pour générer le fichier .cnf
    :param regles_ck: indiquer l'utilisation des trois règles, comme [True, True, True]
    :return:'''

    ################
    ### générer les clauses des règles
    ################
    r1 = [] if (regles_ck[0] == False) else genererClausesRegle1(taille)
    # printRegle(r1)
    r2 = [] if (regles_ck[1] == False) else genererClausesRegle2(taille)
    # printRegle(r2)
    r3 = [] if (regles_ck[2] == False) else genererClausesRegle3(taille)
    # printRegle(r3)

    ################
    ### écrire dans un fichier .cnf
    ################
    saveCNFFile([r1, r2, r3], data, taille, filename)

    # printRegleFormCNF(r1, 8)
    # printRegleFormCNF(r2, 8)

def solver(taille, filename):
    ################
    ### Solver Z3 lit le fichier et renvoie un résultat
    ################
    s = Solver()
    s.from_file(filename)
    # print(s)
    data = []
    if s.check() == sat:
        m = s.model()
        print("len:", str(len(m)))
        if len(m) == taille*taille:
            data = [-1] * (taille * taille)
            for i in range(taille * taille):
                # print(str(i), m[i].name().split("k!"))
                index = int(m[i].name().split("k!")[1])
                # print(index, end="")
                # print(" = ", end="")
                print(-index if m[m[i]] == False else index, end=", ")
                data[index - 1] = 0 if m[m[i]] == False else 1
            print()
    return data