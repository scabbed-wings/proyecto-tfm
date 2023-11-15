from random import getrandbits, choice
import numpy as np
import utils.globals as gb
import utils.position_rules as pr

def size_object(word, obj_type):
    h_obj, w_obj = 0, 0
    min_w = 3.5 if obj_type == "rel" else 2
    min_h = 1 if obj_type == "atr" else 2
    add_h = 0.5 if obj_type == "rel" else 0.5
    words = word.split(" ")
    w_obj = (len(max(words, key=len)) * gb.W_LET)
    h_obj = len(words) * gb.H_LINE
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
            # print("Id_ent: ", id_ent, " Numero de posicion: ", elem[3], " Numero de indice: ", ind)
            return elem[3], ind

def mod_pos_ent_atr(ind, max_mod=2, step=0.2):
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
    
    # print("Posicion: ", ind, " horz_mod: ", horz_mod, " Vert_mod: ", vert_mod)
    
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
    return 1

def check_intersection_rel(ent_atr, rel_dim):
    for elem in ent_atr:
        #print("CHECK ELEM: ", elem)
        obj_ent = [elem[0], elem[1], elem[3], elem[4]]
        if box_intersection(rel_dim, obj_ent): return 1
        if len(elem[2]):
            for elem2 in elem[2]:
                if box_intersection(rel_dim, elem2): return 1
        
    if len(gb.ADDED_REL):
        for elem in gb.ADDED_REL:
            if box_intersection(rel_dim, elem): return 1
    
    return 0

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

            gb.CONTR_FLAG[ind] = 1
        
def mod_pos_rel(id_pos1, id_pos2): # Modify position by intersection
    mod_x, mod_y = 0, 0
    if id_pos1 == 0:
        mod_x, mod_y = pr.mod_rules_ent0(id_pos2)
    elif id_pos1 == 1:
        mod_x, mod_y = pr.mod_rules_ent1(id_pos2)
    elif id_pos1 == 2:
        mod_x, mod_y = pr.mod_rules_ent2(id_pos2)
    elif id_pos1 == 3: # ID pos 4
        mod_x, mod_y  = pr.mod_rules_ent3()
    return mod_x, mod_y

def control_pos(id_pos1, id_pos2, x, y, w, h):
    if (id_pos1 == 0 and id_pos2 == 2) or (id_pos1 == 1 and id_pos2 == 3):
        if id_pos1 == 0:
            x = x if x > 0 else gb.OBJ_SPACE
        else:
            x = x if x + (2 * w) + gb.OBJ_SPACE < gb.WIDTH else gb.WIDTH - (gb.OBJ_SPACE + 2 * w)
    elif (id_pos1 == 0 and id_pos2 == 1) or (id_pos1 == 2 and id_pos2 == 3):
        if id_pos1 == 0:
            y = y if y > 0 else gb.OBJ_SPACE
        else:
            y = y if y + (2 * h) + gb.OBJ_SPACE < gb.HEIGHT else gb.HEIGHT - (gb.OBJ_SPACE + 2 * h)
    
    return x, y

def init_control_flags():
    gb.CONTR_FLAG = [0] * 11