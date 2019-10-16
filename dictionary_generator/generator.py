#!/usr/bin/env python
import random
names = ["ANTONI", "JAKUB", "JAN", "SZYMON", "ALEKSANDER", "FRANCISZEK", "FILIP", "WOJCIECH", "MIKOŁAJ", "KACPER", "ZUZANNA", "JULIA", "ZOFIA", "MAJA", "HANNA", "LENA", "ALICJA", "AMELIA", "MARIA", "OLIWIA"]
surenames = ["Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński", "Lewandowski", "Zieliński", "Szymański", "Woźniak"]


def get_random_name():
    return names[int(random.random()*len(names))]

def get_random_surename():
    return surenames[int(random.random()*len(surenames))]

def get_random_grade():
    return int(random.random()*6)+1
if __name__ == "__main__":

    file = open("dictionary","w")
    for i in range(1000000):
        file.write(get_random_name()+" "+get_random_surename() + " " + str(get_random_grade())+'\n')
