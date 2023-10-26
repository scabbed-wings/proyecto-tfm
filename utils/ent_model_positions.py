from utils.tools import has_reflx_rel, size_object, mod_pos_ent_atr
import random as rnd


WIDTH, HEIGHT = 25, 32.70
W_ATR, H_ATR = 1, 0.5
W_ENT, H_ENT = 1.25, 1
W_REL, H_REL = 1.5, 1
W_CARD, H_CARD = 1.5, 0.4
OBJ_SPACE, CARD_WS, CARD_HS = 0.7, 1, 0.2

def pos_atr(ind, atr, w_ent, mod_h, mod_v):
    atr_pos, x, y = [], 0, 0
    h_atr, w_atr = size_object(atr[0], "atr")
    max_w, max_h4 = w_atr, 0
    if ind == 0 or ind  == 2:
        x = OBJ_SPACE
        y = OBJ_SPACE if ind == 0 else HEIGHT - (OBJ_SPACE + 2 * h_atr)
    elif ind == 1 or ind == 3:
        x = WIDTH - (OBJ_SPACE + 2 * w_atr)
        y = OBJ_SPACE if ind == 1 else HEIGHT - (OBJ_SPACE + 2 * h_atr)
    elif ind == 4:
        x = (WIDTH / 2) - (OBJ_SPACE + 2 * w_atr + w_ent)
        y = (HEIGHT / 2)
        max_h4 += (2 * h_atr)
    x += mod_h
    y += mod_v
    atr_pos.append([x,y,w_atr,h_atr])
    for num, elem in enumerate(atr[1:]):
        h_atr, w_atr = size_object(elem, "atr")
        max_w = w_atr if w_atr > max_w else max_w
        if ind == 0 or ind == 1:
            x = WIDTH - (OBJ_SPACE + 2 * w_atr) + mod_h if ind == 1 else OBJ_SPACE + mod_h
            y += OBJ_SPACE + 2 * h_atr
        elif ind == 2 or ind == 3:
            x = WIDTH - (OBJ_SPACE + 2 * w_atr) + mod_h if ind == 3 else OBJ_SPACE + mod_h
            y -= OBJ_SPACE + 2 * h_atr
        else:
            x = (WIDTH / 2) - (OBJ_SPACE + 2 * w_atr + w_ent) + mod_h
            if (num+1)%2 != 0:
                y += max_h4 + (OBJ_SPACE + 2 * h_atr)
            else:
                y -= max_h4 + (OBJ_SPACE + 2 * h_atr)
            
            max_h4 += OBJ_SPACE + 2 * h_atr
        atr_pos.append([x,y, w_atr, h_atr])
    return atr_pos, max_w

def pos_ent(ent_atr, rel):
    ent_pos = []
    inds = rnd.sample(range(0, 5), len(ent_atr))
    for elem in ent_atr:
        atr_pos, max_w, ind = 0, 0, inds.pop()
        h_ent, w_ent = size_object(elem[2], "ent")
        h_rel = has_reflx_rel(elem[0], rel)
        mod_h, mod_v = mod_pos_ent_atr(ind)
        x,y = 0, 0
        if h_rel:
            x, y = OBJ_SPACE, (2 * OBJ_SPACE) + (2 * h_rel) + (2 * h_ent)
        else:
            x, y = OBJ_SPACE, (2 * OBJ_SPACE) + (2 * h_ent)

        atr_pre = True if len(elem[1]) > 0 else False
        if atr_pre:
            atr_pos, max_w = pos_atr(ind, elem[1], w_ent, mod_h, mod_v)

        if ind == 0 or ind == 2:
            if atr_pre: x += OBJ_SPACE + (max_w * 2)
            if ind == 2:
                y = HEIGHT - y
        elif ind == 1 or ind == 3:
            x = WIDTH - (x + 2 * w_ent)
            if atr_pre: x -= OBJ_SPACE + (max_w * 2)
            if ind == 3:
                y = HEIGHT - y
        elif ind == 4:
            x, y = (WIDTH/2) - w_ent, (HEIGHT/2) - h_ent
        
        x += mod_h
        y += mod_v
        ent_pos.append([x, y, atr_pos, w_ent, h_ent])
        elem.append(ind)
    
    print("Entidades: ", ent_atr)
    print("Posiciones: ", ent_pos)
    return ent_pos

def pos_rel_relx(num_id1, ind_pos1, pos, w_rel, h_rel): #Posición para relaciones reflexivas
    x_rel, y_rel = OBJ_SPACE, OBJ_SPACE
    conn_1, conn_2, gp  = [0] * 4, [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2

    if num_id1 in [0, 2]:
        x_rel = pos[ind_pos1][0] + pos[ind_pos1][3]
        y_rel = HEIGHT - (y_rel + 2 * h_rel) if num_id1 == 2 else y_rel
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel
        conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 2 else pos[ind_pos1][1] # Y entidad
        conn_1[3] = y_rel + h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel + 2 * w_rel, pos[ind_pos1][0] + 2 * pos[ind_pos1][3], y_rel + h_rel
        conn_2[3] = pos[ind_pos1][1] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - W_CARD - CARD_WS, x_rel + w_rel + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - CARD_HS if num_id1 == 0 else y_rel  + 2 * h_rel
        gp[0] = 4 if num_id1 == 0 else 2
        gp[1], gp[2], gp[3]= 3, 1, 1
    elif num_id1 in [1, 3]:
        x_rel = pos[ind_pos1][0] - x_rel
        y_rel = HEIGHT - (y_rel + 2 * h_rel) if num_id1 == 3 else y_rel
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + 2 * pos[ind_pos1][3]
        conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 3 else pos[ind_pos1][1]# Y entidad
        conn_1[3] = y_rel + h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel, pos[ind_pos1][0], y_rel + h_rel
        conn_2[3] = pos[ind_pos1][1] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - W_CARD - CARD_WS, x_rel + w_rel + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - CARD_HS if num_id1 == 1 else y_rel + 2 * h_rel
        gp[0] = 4 if num_id1 == 1 else 2
        gp[1], gp[2], gp[3] = 1, 3, 3
    else:
        x_rel = pos[ind_pos1][0] + pos[ind_pos1][3]
        y_rel = pos[ind_pos1][1] - (OBJ_SPACE + 2 * h_rel)
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + pos[ind_pos1][3]
        conn_1[1], conn_1[3] = pos[ind_pos1][0], y_rel + 2 * h_rel
        conn_2[0], conn_2[2], conn_2[1] = x_rel + 2 * w_rel, pos[ind_pos1][0] + pos[ind_pos1][3] * 2, y_rel + h_rel
        conn_2[3] = pos[ind_pos1][0] + pos[ind_pos1][4]
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - W_CARD - CARD_WS, x_rel + w_rel + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel
        gp[0], gp[1], gp[2], gp[3] = 4, 3, 1, 1
    
    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp

def pos_rel_asoc(num_id1, num_id2, ind_pos1, ind_pos2, pos, w_rel, h_rel): # Posición para relaciones asociativas
    x_rel, y_rel = 0, 0
    conn_1, conn_2, gp  = [0] * 4, [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2
    
    if (num_id1 == 0 and num_id2 == 1) or (num_id1 == 2 and num_id2 == 3): # Relaciones horizontales id mas bajo a la izquierda
        x_rel, y_rel = (((pos[ind_pos1][0] + 2 * pos[ind_pos1][3]) + (pos[ind_pos2][0])) / 2.) - w_rel, pos[ind_pos1][1]
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + 2 * pos[ind_pos1][3], x_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0], x_rel + 2 * w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1] + pos[ind_pos2][4], y_rel + h_rel 
        pos_card_1[0], pos_card_2[0] = pos[ind_pos1][0] + 2 * pos[ind_pos1][3] + CARD_WS, pos[ind_pos2][0] - W_CARD - CARD_WS
        pos_card_1[1] = pos[ind_pos1][1] + (pos[ind_pos1][4]/2) - CARD_HS if num_id2 == 1 else pos[ind_pos1][1] + pos[ind_pos1][4] + CARD_HS
        pos_card_2[1] = pos[ind_pos2][1] + (pos[ind_pos2][4]/2) - CARD_HS if num_id2 == 1 else pos[ind_pos2][1] + pos[ind_pos2][4] + CARD_HS
        gp[0], gp[1], gp[2], gp[3] = 1, 3, 3, 1 # Der ENT, Izq REL, Izq ENT, Der REL
    elif (num_id1 == 0 and num_id2 == 2) or (num_id1 == 1 and num_id2 == 3): # Relaciones verticales id mas bajo arriba
        x_rel, y_rel = pos[ind_pos1][0], (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2) - h_rel
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel +  w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + 2 * h_rel
        pos_card_1[1], pos_card_2[1] = pos[ind_pos1][1] + (pos[ind_pos1][4] * 2) + 2 * CARD_HS, pos[ind_pos2][1] - H_CARD - CARD_HS
        pos_card_1[0] = pos[ind_pos1][0] + pos[ind_pos1][3] - W_CARD if num_id1 == 0 else pos[ind_pos1][0] + pos[ind_pos1][3] 
        pos_card_2[0] = pos[ind_pos2][0] + pos[ind_pos2][3] - W_CARD if num_id2 == 2 else pos[ind_pos2][0] + pos[ind_pos2][3]
        gp[0], gp[1], gp[2], gp[3] = 2, 4, 4, 2 # Abajo Ent, Arriba Rel, Arriba Ent, Abajo Rel
    elif num_id1 == 1 and num_id2 == 2: # Conn1 entidad de arriba Conn2 entidad de abajo
        x_rel = ((pos[ind_pos1][0] + (pos[ind_pos2][0] + 2 * w_rel)) / 2.) - w_rel 
        y_rel = (((pos[ind_pos1][1] + 2 * h_rel) + pos[ind_pos2][1]) / 2.) - h_rel
        y_rel += 8 # Evitar colision con entidad numero 5
        x_rel -= 3
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + 2 * w_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + h_rel
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - W_CARD - CARD_WS, x_rel + w_rel + CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel + h_rel - H_CARD - CARD_HS, y_rel + h_rel + CARD_HS
        gp[0], gp[1], gp[2], gp[3] = 2, 1, 4, 3    # ABajo 1, Der Rel, Arriba 2, Izq Rel  
    elif num_id1 == 0 and num_id2 == 3: # Conn1 entidad de arriba Conn2 entidad de abajo
        x_rel = (((pos[ind_pos1][0] + 2 * w_rel) + pos[ind_pos2][0]) / 2.) - w_rel 
        y_rel = (((pos[ind_pos1][1] + 2 * h_rel) + pos[ind_pos2][1]) / 2.) - h_rel
        y_rel -= 7 # Evitar colision con entidad numero 5
        #x_rel +=  # Evitar colision con entidad numero 5
        conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel
        conn_1[1], conn_1[3] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4], y_rel + h_rel
        conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel + 2 * w_rel
        conn_2[1], conn_2[3] = pos[ind_pos2][1], y_rel + h_rel
        pos_card_1[0], pos_card_2[0] = x_rel + w_rel - W_CARD - CARD_WS, x_rel + w_rel + CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel + h_rel + CARD_HS, y_rel + h_rel - 2 * CARD_HS - H_CARD
        gp[0], gp[1], gp[2], gp[3] = 1, 3, 4, 1    # Der 1, Izq Rel, Arriba 2, Der Rel 
    elif num_id2 == 4:
        x_rel = (((pos[ind_pos1][0] + 2 * pos[ind_pos1][3]) + pos[ind_pos2][0]) / 2.) - w_rel 
        if num_id1 in [0, 2]:
            if num_id1 == 0:
                y_rel = (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2.) - h_rel
            else:
                y_rel = ((pos[ind_pos1][1] + (pos[ind_pos2][1] + 2 * pos[ind_pos2][4])) / 2.) - h_rel
            conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
            conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 0 else pos[ind_pos1][1]
            conn_1[3] = y_rel if num_id1 == 0 else y_rel + 2 * h_rel
            conn_2[0], conn_2[2] = pos[ind_pos2][0] + pos[ind_pos2][3], x_rel + w_rel
            conn_2[1] = pos[ind_pos2][1] if num_id1 == 0 else pos[ind_pos2][1] + 2 * pos[ind_pos2][4]
            conn_2[3] = y_rel + 2 * h_rel if num_id1 == 0 else y_rel
            pos_card_1[0] = pos_card_2[0] = x_rel + w_rel - (W_CARD /2)
            pos_card_1[1], pos_card_2[1] = y_rel - CARD_HS - H_CARD, y_rel + (2 * h_rel + CARD_HS)
            gp[0] = 2 if num_id1 == 0 else 4
            gp[2] = 4 if num_id1 == 0 else 2
            gp[1], gp[3] = 3, 1

        elif num_id1 in [1, 3]:
            x_rel = ((pos[ind_pos1][0] + (pos[ind_pos2][0] + 2 * pos[ind_pos2][3])) / 2.) - w_rel
            if num_id1 == 1:
                y_rel = (((pos[ind_pos1][1] + 2 * pos[ind_pos1][4]) + pos[ind_pos2][1]) / 2.) - h_rel
            else:
                y_rel = ((pos[ind_pos1][1] + (pos[ind_pos2][1] + 2 * pos[ind_pos2][4])) / 2.) - h_rel
            
            conn_1[0], conn_1[2] = pos[ind_pos1][0] + pos[ind_pos1][3], x_rel + w_rel
            conn_1[1] = pos[ind_pos1][1] + 2 * pos[ind_pos1][4] if num_id1 == 1 else pos[ind_pos1][1]
            conn_1[3] = y_rel if num_id1 == 1 else y_rel + 2 * h_rel
            conn_2[0], conn_2[2] = pos[ind_pos2][0] + 2 * pos[ind_pos2][3], x_rel + h_rel
            conn_2[1] = pos[ind_pos2][1] if num_id1 == 1 else pos[ind_pos2][1] + 2 * pos[ind_pos2][4]
            conn_2[3] = y_rel + 2 * h_rel if num_id1 == 1 else y_rel
            pos_card_1[0] = pos_card_2[0] = x_rel + w_rel - (W_CARD /2)
            pos_card_1[1], pos_card_2[1] = y_rel - H_CARD - CARD_HS, y_rel + (2 * h_rel + CARD_HS)
            gp[1], gp[2], gp[3] = 1, 1, 3
            gp[0] = 2 if num_id1 == 1 else 4

    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp