from random import getrandbits, choice
import numpy as np
H_LINE, W_LET = 0.6, 0.3125
REL_TAG = [0] * 10

def size_object(word, obj_type):
    h_obj, w_obj = 0, 0
    min_w = 3 if obj_type == "rel" else 2
    min_h = 1 if obj_type == "atr" else 2
    add_h = 0.5 if obj_type == "rel" else 0.5
    words = word.split(" ")
    w_obj = (len(max(words, key=len)) * W_LET)
    h_obj = len(words) * H_LINE
    w_obj = min_w if w_obj < min_w else w_obj
    h_obj = min_h if h_obj < min_h else h_obj

    w_obj += add_h
    
    return h_obj/2, w_obj/2

def max_len_word(e):
    return len(max(e.split(" "), key=len))

def has_reflx_rel(id_ent, rel):
    for elem in rel:
        if elem[0] == elem[1] == id_ent:
            h, _ = size_object(elem[4], "rel")
            return h
    return 0

def get_pos_ent(id_ent, ent_atr):
    for ind, elem in enumerate(ent_atr):
        if elem[0] == id_ent:
            print("Id_ent: ", id_ent, " Numero de posicion: ", elem[3], " Numero de indice: ", ind)
            return elem[3], ind

def mod_pos_ent_atr(ind, max_mod=3, step=0.2):
    values = np.arange(0, max_mod, step).tolist()
    vert_mod, horz_mod = 0, 0
    if ind == 0 or ind == 2:
        if getrandbits(1):
            horz_mod = choice(values)
        if getrandbits(1):
            vert_mod = -choice(values) if ind == 2 else choice(values)
    elif ind == 1 or ind == 3:
        if getrandbits(1):
            horz_mod = -choice(values)
        if getrandbits(1):
            vert_mod = -choice(values) if ind == 3 else choice(values)
    # else:
    #     if getrandbits(1):
    #         horz_mod = -choice(values) if getrandbits(1) else choice(values)
    #     if getrandbits(1):
    #         vert_mod = -choice(values) if getrandbits(1) else choice(values)
    
    print("Posicion: ", ind, " horz_mod: ", horz_mod, " Vert_mod: ", vert_mod)
    
    return horz_mod, vert_mod

def box_intersection(obj1, obj2):
    l1 = np.array([obj1[0], obj1[1]])
    r1 = np.array([obj1[0] + obj1[2], obj1[1] + obj1[3]])
    l2 = np.array([obj2[0], obj2[1]])
    r2 = np.array([obj2[0] + obj2[2], obj2[1] + obj2[3]])
    # Rectangulo a la izquierda o la derecha
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return 0
    # Rectángulo arriba o abajo
    if r1[1] > l2[1] or r2[1] > l1[1]:
        return 0
 
    return True

def rel_by_pos(ent_atr, rel):
    ind = 0
    for elem in rel:
        num_id1, _ = get_pos_ent(elem[0], ent_atr)
        num_id2, _ = get_pos_ent(elem[1], ent_atr)
        if num_id1 > num_id2:
            cop = num_id2
            num_id2 = num_id1
            num_id1 = cop
        if num_id1 != num_id2:
            if num_id1 == 0:
                if num_id2 in [1,2]:
                    ind = 2 if num_id2 == 1 else 0
                else:
                    ind = 8 if num_id2 == 3 else 4
            elif num_id1 == 1:
                if num_id2 in [2, 3]:
                    ind = 9 if num_id2 == 2 else 1
                else: ind = 7
            elif num_id1 == 2:
                ind = 3 if num_id2 == 3 else 5
            elif num_id1 == 3:
                ind = 6

            REL_TAG[ind] = 1
        
def mod_pos_rel(id_pos1, id_pos2, rel_pos): # Modificador de posición por intersección
    mod_x, mod_y = 0, 0
    if id_pos1 == 0:
        if id_pos2 in [1,2]:
            mod_x = 0 if id_pos2 == 1 else -3
            mod_y = -2 if id_pos2 == 1 else 0
        else:
            ind = 8 if id_pos2 == 3 else 4
    elif id_pos1 == 1:
        if id_pos2 in [2, 3]:
            ind = 9 if id_pos2 == 2 else 1
        else: ind = 7
    elif id_pos1 == 2:
        ind = 3 if id_pos2 == 3 else 5
    elif id_pos1 == 3:
        ind = 6
    return mod_x, mod_y