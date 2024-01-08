from utils.tools import has_reflx_rel, size_object, mod_pos_ent_atr, max_len_word, check_intersection_rel, mod_pos_rel, control_pos
import random as rnd
import utils.globals as gb
from utils.position_rules import init_diag_vals

def pos_atr(ind, atr, w_ent, mod_h, mod_v):
    """
    Get the positions of the attributes related to an entity

    :param ind: Index position of the entity
    :param atr: Atribute list
    :param w_ent: Width of the entity
    :param mod_h: Horizontal position modifier of the entity
    :param mod_v: Vertical position modifier of the entity
    :return: list of position and dimension of the atribute and maximum width of the atributes
    """ 
    atr_pos, x, y = [], 0, 0
    h_atr, w_atr = size_object(atr[0], "atr")
    max_w, max_h4, h4_saved = w_atr, 0, 0
    if ind == 0 or ind  == 2:
        x = gb.OBJ_SPACE
        y = gb.OBJ_SPACE if ind == 0 else gb.HEIGHT - (gb.OBJ_SPACE + 2 * h_atr)
    elif ind == 1 or ind == 3:
        x = gb.WIDTH - (gb.OBJ_SPACE + 2 * w_atr)
        y = gb.OBJ_SPACE if ind == 1 else gb.HEIGHT - (gb.OBJ_SPACE + 2 * h_atr)
    elif ind == 4:
        x = (gb.WIDTH / 2) - (gb.OBJ_SPACE + 2 * w_atr + w_ent)
        y = (gb.HEIGHT / 2)
        max_h4 += (2 * h_atr) + gb.OBJ_SPACE
    x += mod_h
    y += mod_v
    atr_pos.append([x,y,w_atr,h_atr])
    for num, elem in enumerate(atr[1:]):
        prev_h = h_atr
        h_atr, w_atr = size_object(elem, "atr")
        max_w = w_atr if w_atr > max_w else max_w
        if ind == 0 or ind == 1:
            x = gb.WIDTH - (gb.OBJ_SPACE + 2 * w_atr) + mod_h if ind == 1 else gb.OBJ_SPACE + mod_h
            y += gb.OBJ_SPACE + 2 * prev_h
        elif ind == 2 or ind == 3:
            x = gb.WIDTH - (gb.OBJ_SPACE + 2 * w_atr) + mod_h if ind == 3 else gb.OBJ_SPACE + mod_h
            y -= gb.OBJ_SPACE + 2 * h_atr
        else:
            x = (gb.WIDTH / 2) - (gb.OBJ_SPACE + 2 * w_atr + w_ent) + mod_h
            if (num+1)%2 != 0:
                y += max_h4
                h4_saved = (2 * h_atr) + gb.OBJ_SPACE
            else:
                y -= max_h4 + (gb.OBJ_SPACE + 2 * h_atr)
                max_h4 += h4_saved + gb.OBJ_SPACE + 2 * h_atr

        atr_pos.append([x,y, w_atr, h_atr])
    return atr_pos, max_w

def pos_ent(ent_atr, rel):
    """
    Get the positions of the entities

    :param ent_atr: Iist of entities and its atributes
    :param rel: List of relations between entities
    :return: list of position and dimension of the entities and it's atributes
    """ 
    ent_pos = []
    inds = rnd.sample(range(0, 5), len(ent_atr))
    for elem in ent_atr:
        atr_pos, max_w, ind = [], 0, inds.pop()
        h_ent, w_ent = size_object(elem[2], "ent")
        h_rel = has_reflx_rel(elem[0], rel)
        mod_h, mod_v = mod_pos_ent_atr(ind)
        x,y = 0, 0
        if h_rel:
            x, y = gb.OBJ_SPACE, (2 * gb.OBJ_SPACE) + (2 * h_rel) + (2 * h_ent)
        else:
            x, y = gb.OBJ_SPACE, (2 * gb.OBJ_SPACE) + (2 * h_ent)

        atr_pre = True if len(elem[1]) > 0 else False
        if atr_pre:
            if ind == 0 or ind == 1:
                elem[1].sort(key=max_len_word, reverse=True)
            atr_pos, max_w = pos_atr(ind, elem[1], w_ent, mod_h, mod_v)
            if ind == 4: gb.CONTR_FLAG[10] = 1

        if ind == 0 or ind == 2:
            if atr_pre: x += gb.OBJ_SPACE + (max_w * 2)
            if ind == 2:
                y = gb.HEIGHT - y
        elif ind == 1 or ind == 3:
            x = gb.WIDTH - (x + 2 * w_ent)
            if atr_pre: x -= gb.OBJ_SPACE + (max_w * 2)
            if ind == 3:
                y = gb.HEIGHT - y
        elif ind == 4:
            x, y = (gb.WIDTH/2) - w_ent, (gb.HEIGHT/2) - h_ent
        
        x += mod_h
        y += mod_v
        ent_pos.append([x, y, atr_pos, w_ent, h_ent])
        elem.append(ind)
    
    print("Entidades: ", ent_atr)
    print("Posiciones: ", ent_pos)
    return ent_pos

def pos_rel_relx(num_id1, ind_pos1, pos, w_rel, h_rel): #Posición para relaciones reflexivas
    """
    Get the positions of the attributes related to an entity

    :param id1: Index position of the entity
    :param ind_pos1: Index position of the entity in the list
    :param pos: List of positions of atributes and entities
    :param w_rel: Width of the relation object
    :param h_rel: Height of the relation object
    :return: list of position and dimension of the atribute and maximum width of the atributes
    """ 
    x_rel, y_rel = gb.OBJ_SPACE, gb.OBJ_SPACE
    conn_1, conn_2, gp  = [0] * 4, [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2

    if num_id1 in [0, 2]:
        x_rel = pos[ind_pos1][0] + pos[ind_pos1][3]
        y_rel = gb.HEIGHT - (y_rel + 2 * h_rel) if num_id1 == 2 else y_rel
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel
        conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 2 else pos[ind_pos1][1] # Y entidad
        conn_1[3] = y_rel + h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel + 2 * w_rel, pos[ind_pos1][0] + 2 * pos[ind_pos1][3], y_rel + h_rel
        conn_2[3] = pos[ind_pos1][1] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - gb.W_CARD - gb.CARD_WS, x_rel + w_rel + gb.CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - gb.CARD_HS if num_id1 == 0 else y_rel  + 2 * h_rel
        gp[0] = 4 if num_id1 == 0 else 2
        gp[1], gp[2], gp[3]= 3, 1, 1
    elif num_id1 in [1, 3]:
        x_rel = pos[ind_pos1][0] - x_rel
        y_rel = gb.HEIGHT - (y_rel + 2 * h_rel) if num_id1 == 3 else y_rel
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + 2 * pos[ind_pos1][3]
        conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 3 else pos[ind_pos1][1]# Y entidad
        conn_1[3] = y_rel + h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel, pos[ind_pos1][0], y_rel + h_rel
        conn_2[3] = pos[ind_pos1][1] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - gb.W_CARD - gb.CARD_WS, x_rel + w_rel + gb.CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - gb.CARD_HS if num_id1 == 1 else y_rel + 2 * h_rel
        gp[0] = 4 if num_id1 == 1 else 2
        gp[1], gp[2], gp[3] = 1, 3, 3
    else:
        x_rel = pos[ind_pos1][0] + pos[ind_pos1][3]
        y_rel = pos[ind_pos1][1] - (gb.OBJ_SPACE + 2 * h_rel)
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + pos[ind_pos1][3]
        conn_1[1], conn_1[3] = pos[ind_pos1][0], y_rel + 2 * h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel + 2 * w_rel, pos[ind_pos1][0] + pos[ind_pos1][3] * 2, y_rel + h_rel
        conn_2[3] = pos[ind_pos1][0] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - gb.W_CARD - gb.CARD_WS, x_rel + w_rel + gb.CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel
        gp[0], gp[1], gp[2], gp[3] = 4, 3, 1, 1
    
    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp

def conn_and_gp_asoc(num_id1, num_id2, ind_pos1, ind_pos2, x_rel, y_rel, w_rel, h_rel, pos):
    conn_1, conn_2, gp  = [0] * 4, [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2

    if (num_id1 == 0 and num_id2 == 1) or (num_id1 == 2 and num_id2 == 3): # Relaciones horizontales id mas bajo a la izquierda
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + 2 * pos[ind_pos1][3], x_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0], x_rel + 2 * w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1] + pos[ind_pos2][4], y_rel + h_rel
        pos_card_1[0], pos_card_2[0] = pos[ind_pos1][0] + 2 * pos[ind_pos1][3] + gb.CARD_WS, pos[ind_pos2][0] - gb.W_CARD - gb.CARD_WS
        pos_card_1[1] = pos[ind_pos1][1] + (pos[ind_pos1][4]/2) - gb.CARD_HS if num_id2 == 1 else pos[ind_pos1][1] + pos[ind_pos1][4] + gb.CARD_HS
        pos_card_2[1] = pos[ind_pos2][1] + (pos[ind_pos2][4]/2) - gb.CARD_HS if num_id2 == 1 else pos[ind_pos2][1] + pos[ind_pos2][4] + gb.CARD_HS
        gp[0], gp[1], gp[2], gp[3] = 1, 3, 3, 1 # Der ENT, Izq REL, Izq ENT, Der REL
    elif (num_id1 == 0 and num_id2 == 2) or (num_id1 == 1 and num_id2 == 3): # Relaciones verticales id mas bajo arriba
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel +  w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + 2 * h_rel
        pos_card_1[1], pos_card_2[1] = pos[ind_pos1][1] + (pos[ind_pos1][4] * 2) + 2 * gb.CARD_HS, pos[ind_pos2][1] - gb.H_CARD - gb.CARD_HS
        pos_card_1[0] = pos[ind_pos1][0] + pos[ind_pos1][3] - gb.W_CARD if num_id1 == 0 else pos[ind_pos1][0] + pos[ind_pos1][3] 
        pos_card_2[0] = pos[ind_pos2][0] + pos[ind_pos2][3] - gb.W_CARD if num_id2 == 2 else pos[ind_pos2][0] + pos[ind_pos2][3]
        gp[0], gp[1], gp[2], gp[3] = 2, 4, 4, 2 # Abajo Ent, Arriba Rel, Arriba Ent, Abajo Rel
    elif num_id1 == 1 and num_id2 == 2: # Conn1 entidad de arriba Conn2 entidad de abajo
        _, DIAG9_UP = init_diag_vals()
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + 2 * w_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + h_rel
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - gb.W_CARD - gb.CARD_WS, x_rel + w_rel + gb.CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel + h_rel - gb.H_CARD - gb.CARD_HS, y_rel + h_rel + gb.CARD_HS
        if DIAG9_UP:
            print("Cambiando gluepoints diagonal 9")
            gp[0], gp[1], gp[2], gp[3] = 3, 1, 2, 3    # ABajo 1, Der Rel, Arriba 2, Izq Rel  
        else:
            gp[0], gp[1], gp[2], gp[3] = 2, 1, 1, 3    # ABajo 1, Der Rel, Arriba 2, Izq Rel  
    elif num_id1 == 0 and num_id2 == 3: # Conn1 entidad de arriba Conn2 entidad de abajo
        DIAG8_LOW, _ = init_diag_vals()
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel + 2 * w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + h_rel
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - gb.W_CARD - gb.CARD_WS, x_rel + w_rel + gb.CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel + h_rel + gb.CARD_HS, y_rel + h_rel - 2 * gb.CARD_HS - gb.H_CARD
        if DIAG8_LOW:
            print("Cambiando gluepoints diagonal 8")
            gp[0], gp[1], gp[2], gp[3] = 2, 3, 3, 1    # Der 1, Izq Rel, Arriba 2, Der Rel 
        else:
            gp[0], gp[1], gp[2], gp[3] = 2, 3, 4, 1    # Der 1, Izq Rel, Arriba 2, Der Rel 
    elif num_id2 == 4:
        if num_id1 in [0, 2]:
            conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
            conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 0 else pos[ind_pos1][1]
            conn_1[3] = y_rel if num_id1 == 0 else y_rel + 2 * h_rel
            conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel + w_rel
            conn_2[1] = pos[ind_pos2][1] if num_id1 == 0 else pos[ind_pos2][1] + 2 * pos[ind_pos2][4]
            conn_2[3] = y_rel + 2 * h_rel if num_id1 == 0 else y_rel
            pos_card_1[0] = pos_card_2[0] = x_rel + w_rel - (gb.W_CARD /2)
            pos_card_1[1], pos_card_2[1] = y_rel - gb.CARD_HS - gb.H_CARD, y_rel + (2 * h_rel + gb.CARD_HS)
            gp[0] = 2 if num_id1 == 0 else 4
            gp[2] = 4 if num_id1 == 0 else 2
            gp[1], gp[3] = 3, 1

        elif num_id1 in [1, 3]:
            conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
            conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 1 else pos[ind_pos1][1]
            conn_1[3] = y_rel if num_id1 == 1 else y_rel + 2 * h_rel
            conn_2[0], conn_2[2] = pos[ind_pos2][0] + 2 * pos[ind_pos2][3], x_rel + h_rel
            conn_2[1] = pos[ind_pos2][1] if num_id1 == 1 else pos[ind_pos2][1] + 2 * pos[ind_pos2][4]
            conn_2[3] = y_rel + 2 * h_rel if num_id1 == 1 else y_rel
            pos_card_1[0] = pos_card_2[0] = x_rel + w_rel - (gb.W_CARD /2)
            pos_card_1[1], pos_card_2[1] = y_rel - gb.H_CARD - gb.CARD_HS, y_rel + (2 * h_rel + gb.CARD_HS)
            gp[1], gp[2], gp[3] = 1, 1, 3
            gp[0] = 2 if num_id1 == 1 else 4

    return conn_1, conn_2, pos_card_1, pos_card_2, gp

def pos_rel_asoc(num_id1, num_id2, ind_pos1, ind_pos2, w_rel, h_rel, pos): # Posición para relaciones asociativas
    x_rel, y_rel = 0, 0
    
    if (num_id1 == 0 and num_id2 == 1) or (num_id1 == 2 and num_id2 == 3): # Relaciones horizontales id mas bajo a la izquierda
        x_rel = (((pos[ind_pos1][0] + 2 * pos[ind_pos1][3]) + (pos[ind_pos2][0])) / 2) - w_rel
        y_rel = ((pos[ind_pos1][1] + pos[ind_pos2][1]) / 2.) - h_rel

    elif (num_id1 == 0 and num_id2 == 2) or (num_id1 == 1 and num_id2 == 3): # Relaciones verticales id mas bajo arriba
        x_rel = ((pos[ind_pos1][0] + pos[ind_pos2][0]) / 2.) - w_rel
        y_rel = (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2.) - h_rel
    elif num_id1 == 1 and num_id2 == 2: # Conn1 entidad de arriba Conn2 entidad de abajo
        x_rel = ((pos[ind_pos1][0] + (pos[ind_pos2][0] + 2 * w_rel)) / 2.) - w_rel 
        y_rel = (((pos[ind_pos1][1] + 2 * h_rel) + pos[ind_pos2][1]) / 2.) - h_rel 
    elif num_id1 == 0 and num_id2 == 3: # Conn1 entidad de arriba Conn2 entidad de abajo
        x_rel = (((pos[ind_pos1][0] + 2 * w_rel) + pos[ind_pos2][0]) / 2.) - w_rel 
        y_rel = (((pos[ind_pos1][1] + 2 * h_rel) + pos[ind_pos2][1]) / 2.) - h_rel
    elif num_id2 == 4:
        x_rel = (((pos[ind_pos1][0] + 2 * pos[ind_pos1][3]) + pos[ind_pos2][0]) / 2.) - w_rel 
        if num_id1 in [0, 2]:
            if num_id1 == 0:
                y_rel = (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2.) - h_rel
            else:
                y_rel = ((pos[ind_pos1][1] + (pos[ind_pos2][1] + 2 * pos[ind_pos2][4])) / 2.) - h_rel

        elif num_id1 in [1, 3]:
            x_rel = ((pos[ind_pos1][0] + (pos[ind_pos2][0] + 2 * pos[ind_pos2][3])) / 2.) - w_rel
            if num_id1 == 1:
                y_rel = (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2.) - h_rel
            else:
                y_rel = ((pos[ind_pos1][1] + (pos[ind_pos2][1] + 2 * pos[ind_pos2][4])) / 2.) - h_rel
            
    if gb.CONTR_FLAG[10] or gb.CONTR_FLAG[9] or gb.CONTR_FLAG[8]:
        mod_x, mod_y = mod_pos_rel(num_id1, num_id2)
        x_rel, y_rel = control_pos(num_id1, num_id2, x_rel + mod_x, y_rel + mod_y, w_rel, h_rel)
    elif check_intersection_rel(pos, [x_rel, y_rel, w_rel, h_rel]):
        mod_x, mod_y = mod_pos_rel(num_id1, num_id2)
        x_rel, y_rel = control_pos(num_id1, num_id2, x_rel + mod_x, y_rel + mod_y, w_rel, h_rel)
    
    gb.ADDED_REL.append([x_rel, y_rel, w_rel, h_rel])
    conn_1, conn_2, pos_card_1, pos_card_2, gp = conn_and_gp_asoc(num_id1, num_id2, ind_pos1, ind_pos2, x_rel, y_rel, w_rel, h_rel, pos)

    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp