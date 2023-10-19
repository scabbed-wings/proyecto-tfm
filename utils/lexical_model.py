import pandas as pd
import random as rnd
import numpy as np

DICT_ENTS = pd.read_csv("csv/ent_atr.csv")
DICT_RELS = pd.read_csv("csv/rel_ent.csv")

def findValIndex(val, lista):
    for ind, elem in enumerate(lista):
        if val == elem[2]:
            return(ind)
    return -1

def take_card():
    card = ["0..N", "0..*", "1..1", "1..N", "1..*", "M..N"]
    card_1 = rnd.choice(card)
    card_2 = rnd.choice(card)
    return card_1, card_2

def take_atributes(ent, max_atr):
    atr = []
    num_atr = rnd.randint(0, max_atr)
    if num_atr > 0:
        df = DICT_ENTS[DICT_ENTS['Entidad'].str.contains(ent)].to_numpy().flatten()
        print("Ent", ent)
        atr = np.random.choice(df[1:], num_atr, replace=False)
        atr = atr.tolist()
    
    return atr

def create_lexical_model(max_ent= 5, max_atr= 5):
    ent_atr, rel, atr, i, act_id = [], [], [], 0, 0 
    nom_flag, init = False, True
    while not nom_flag:
        if init:
            df = DICT_ENTS.sample().to_numpy().flatten()
            ent_init = df[0]
        elif act_id != max_ent:
            ent_init = ent_atr[act_id][2]
            act_id += 1
                
        search1 = DICT_RELS[DICT_RELS['Entidad1'].str.contains(ent_init)].to_numpy()
        search2 = DICT_RELS[DICT_RELS['Entidad2'].str.contains(ent_init)].to_numpy()
        fy = []
        if len(ent_atr) == 0 and (search1.shape[0] >= 1 or search2.shape[0] >= 1):
            init = False
            atr = take_atributes(ent_init, max_atr)
            i += 1
            act_id = i
            ent_atr.append([f'''id{i}''', atr, ent_init])
            if search1.shape[0] >= 1:
                for j in range(search1.shape[0]):
                    if len(ent_atr) < 5:
                        if search1[j][1] != ent_init and not search1[j][1] in fy:
                            i += 1
                            ent = search1[j][1]
                            atr = take_atributes(ent, max_atr)
                            ent_atr.append([f'''id{i}''', atr, ent])
                            card_1, card_2 = take_card()
                            rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search1[j][2]])
                            fy.append(ent)
                    elif search1[j][1] == ent_init:
                        card_1, card_2 = take_card()
                        rel.append([f'''id{act_id}''', f'''id{act_id}''', card_1, card_2, search1[j][2]])

            if search2.shape[0] >= 1:
                for j in range(search2.shape[0]):
                    if len(ent_atr) < 5:
                        if search2[j][0] != ent_init and not search2[j][0] in fy:
                            i += 1
                            ent = search2[j][0]
                            atr = take_atributes(ent, max_atr)
                            ent_atr.append([f'''id{i}''', atr, ent])
                            card_1, card_2 = take_card()
                            rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search2[j][2]])
                            fy.append(ent)
                        elif search2[j][0] == ent_init:
                            card_1, card_2 = take_card()
                            rel.append([f'''id{act_id}''', f'''id{act_id}''', card_1, card_2, search2[j][2]])
        elif 1 < len(ent_atr) < max_ent  and (search1.shape[0] >= 1 or search2.shape[0] >= 1):
            if search1.shape[0] >= 1:
                for j in range(search1.shape[0]):
                        if search1[j][1] != ent_init and not search1[j][1] in fy:
                            ind = findValIndex(search1[j][1], ent_atr)
                            if ind == -1 and len(ent_atr) < max_ent:
                                i += 1
                                ent = search1[j][1]
                                atr = take_atributes(ent, max_atr)
                                ent_atr.append([f'''id{i}''', atr, ent])
                                card_1, card_2 = take_card()
                                rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search1[j][2]])
                                fy.append(ent)
                            elif act_id - 1 < ind:
                                card_1, card_2 = take_card()
                                rel.append([f'''id{act_id}''', f'''id{ind + 1}''', card_1, card_2, search1[j][2]])
                        elif search1[j][1] == ent_init:
                            card_1, card_2 = take_card()
                            rel.append([f'''id{act_id}''', f'''id{act_id}''', card_1, card_2, search1[j][2]])

            if search2.shape[0] >= 1:
                for j in range(search2.shape[0]):
                        if search2[j][0] != ent_init and not search2[j][0] in fy:
                            ind = findValIndex(search2[j][0], ent_atr)
                            if ind == -1 and len(ent_atr) < max_ent:
                                i += 1
                                ent = search2[j][0]
                                atr = take_atributes(ent, max_atr)
                                ent_atr.append([f'''id{i}''', atr, ent])
                                card_1, card_2 = take_card()
                                rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search2[j][2]])
                                fy.append(ent)
                            elif act_id - 1 < ind:
                                card_1, card_2 = take_card()
                                rel.append([f'''id{act_id}''', f'''id{ind + 1}''', card_1, card_2, search2[j][2]])
                        elif search2[j][0] == ent_init:
                            card_1, card_2 = take_card()
                            rel.append([f'''id{act_id}''', f'''id{act_id}''', card_1, card_2, search2[j][2]])
    
            if len(ent_atr) == act_id and search1.shape[0] + search2.shape[0] == 1:
                nom_flag = True
        elif len(ent_atr) == max_ent and act_id == max_ent:
            nom_flag = True

    print("Entidades: ", ent_atr)
    print("Relaciones: ", rel)

    return ent_atr, rel