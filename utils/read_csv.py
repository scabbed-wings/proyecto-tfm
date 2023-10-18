import pandas as pd
import random as rnd
import numpy as np
from copy import copy

DICT_ENTS = pd.read_csv("csv/ent_atr.csv")
DICT_RELS = pd.read_csv("csv/rel_ent.csv")

#    for elem in rel:
#        rev_cop = copy(elem)
#        rev_cop.reverse()
#        if not any(elem[:2] == sl[:2] or rev_cop[2:] == sl[:2] for sl in sub_filt):
#            sub_filt.append(elem)

def take_card():
    card = ["0..N", "0..*", "1..1", "1..N", "1..*", "M..N"]
    card_1 = rnd.choice(card)
    card_2 = rnd.choice(card)
    return card_1, card_2

def take_atributes(ent, max_atr):
    atr = []
    df = DICT_ENTS[DICT_ENTS['Entidad'].str.contains(ent)].to_numpy().flatten()
    num_atr = rnd.randint(0, max_atr)
    if num_atr > 0:
        atr = np.random.choice(df[1:], num_atr)
    
    return atr

def create_lexical_model(max_ent= 5, max_atr= 5):
    ent_atr, rel, atr, i = [], [], [], 0

    
    while len(rel) < 5:
        df = DICT_ENTS.sample().to_numpy().flatten()
        ent = df[0]
        num_atr = rnd.randint(0, max_atr)
        if num_atr > 0:
            atr = np.random.choice(df[1:], num_atr)
        i += 1
        act_id = i
        ent_atr.append([f'''id{i}''', atr, ent])
        search1 = DICT_RELS[DICT_RELS['Entidad1'].str.contains(ent)].to_numpy()
        search2 = DICT_RELS[DICT_RELS['Entidad2'].str.contains(ent)].to_numpy()
        print(search1)
        print(search2)
        if search1.shape[0] > 1:
            for j in range(search1.shape[0]):
                if len(ent_atr) < 5:
                    i += 1
                    ent = search1[j][1]
                    atr = take_atributes(ent, max_atr)
                    ent_atr.append([f'''id{i}''', atr, ent])
                    card_1, card_2 = take_card()
                    rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search1[j][2]])

        if search2.shape[0] > 1:
            for j in range(search2.shape[0]):
                if len(ent_atr) < 5:
                    i += 1
                    ent = search2[j][0]
                    atr = take_atributes(ent, max_atr)
                    ent_atr.append([f'''id{i}''', atr, ent])
                    card_1, card_2 = take_card()
                    rel.append([f'''id{act_id}''', f'''id{i}''', card_1, card_2, search1[j][2]])

if __name__ == "__main__":
    create_lexical_model(5)