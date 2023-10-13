WIDTH, HEIGHT = 25, 32.70
W_ATR, H_ATR = 1, 0.5
W_ENT, H_ENT = 1.25, 1
W_REL, H_REL = 1.5, 1
OBJ_SPACE, CARD_WS, CARD_HS = 1.5, 1.5, 0.2

def pos_atr(ind, num_atr):
    atr_pos, x, y = [], 0, 0
    if ind == 0 or ind  == 2:
        x = OBJ_SPACE + W_ATR
        y = OBJ_SPACE + H_ATR if ind == 0 else HEIGHT - (OBJ_SPACE + H_ATR)
    elif ind == 1 or ind == 3:
        x = WIDTH - (OBJ_SPACE + W_ATR)
        y = OBJ_SPACE + H_ATR if ind == 1 else HEIGHT - (OBJ_SPACE + H_ATR)
    elif ind == 4:
        x = (WIDTH / 2) - (OBJ_SPACE + H_ATR)
        y = (HEIGHT / 2) - (OBJ_SPACE + H_ATR)
    for num in range(num_atr):
        if ind == 0 or ind == 1 or ind == 5:
            y += OBJ_SPACE + H_ATR
        else:
            y -= OBJ_SPACE + H_ATR
        atr_pos.append([x,y])
    return atr_pos

def pos_ent(ent_atr):
    ent_pos = []
    for ind, elem in enumerate(ent_atr):
        x, y = OBJ_SPACE + W_ENT, OBJ_SPACE + H_ENT
        atr_pre = True if elem[1] > 0 else False
        if ind == 0 or ind == 2:
            #if atr_pre: x += OBJ_SPACE + (W_ATR * 2)
            x += OBJ_SPACE + (W_ATR * 2)
            if ind == 2:
                y = HEIGHT - y
                y -= OBJ_SPACE + (H_ATR * 2)
            elif ind == 0:
                y += OBJ_SPACE + (H_ATR * 2)
        elif ind == 1 or ind == 3:
            x = WIDTH - x
            #if atr_pre: x -= OBJ_SPACE + (W_ATR * 2)
            x -= OBJ_SPACE + (W_ATR * 2)
            if ind == 3:
                y = HEIGHT - y
                y -= OBJ_SPACE + (H_ATR * 2)
            elif ind == 1:
                y += OBJ_SPACE + (H_ATR * 2)
        elif ind == 4:
            x, y = WIDTH/2, HEIGHT/2
        
        if atr_pre:
            atr_pos = pos_atr(ind, elem[1])
            ent_pos.append([x, y, atr_pos])
        else:
            ent_pos.append([x,y])
    return ent_pos

def pos_rel_relx(num_id1, pos): #Posición para relaciones reflexivas
    x_rel, y_rel = 2, 1.5
    conn_1, conn_2  = [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2

    if num_id1 in [0, 2]:
        x_rel = pos[num_id1][0]
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        y_rel = HEIGHT - y_rel if num_id1 == 2 else y_rel
        conn_1[1] = pos[num_id1][1] + H_ENT if num_id1 == 2 else pos[num_id1][1] - H_ENT # Y entidad
        conn_1[3] = y_rel - H_REL if num_id1 == 2 else y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel + W_REL, pos[num_id1][0] + 0.5, y_rel
        conn_2[3] = conn_1[1]
        pos_card_1[0], pos_card_2[0] = x_rel - (W_REL + CARD_WS), x_rel + W_REL + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - CARD_HS if num_id1 == 0 else y_rel + CARD_HS
    elif num_id1 in [1, 3]:
        x_rel = pos[num_id1][0] 
        y_rel = HEIGHT - y_rel if num_id1 == 3 else y_rel
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1] = pos[num_id1][1] + H_ENT if num_id1 == 3 else pos[num_id1][1] - H_ENT # Y entidad
        conn_1[3] = y_rel - H_REL if num_id1 == 3 else y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel - W_REL, pos[num_id1][0] - 0.5, y_rel
        conn_2[3] = conn_1[1]
        pos_card_1[0], pos_card_2[0] = x_rel - (W_REL + CARD_WS), x_rel + W_REL + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - CARD_HS if num_id1 == 1 else y_rel + CARD_HS
    else:
        x_rel = WIDTH / 2
        y_rel = (HEIGHT / 2) - 2.5
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1], conn_1[3] = pos[num_id1][0] - 1, y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel - W_REL, pos[num_id1][0] + 0.5, y_rel
        conn_2[3] = conn_1[1]
        pos_card_1[0], pos_card_2[0] = x_rel - (W_REL + CARD_WS), x_rel + W_REL + CARD_WS
        pos_card_1[1] = pos_card_2[1] = y_rel - CARD_HS
    
    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2

def pos_rel_asoc(num_id1, num_id2, pos): # Posición para relaciones asociativas
    x_rel, y_rel = (pos[num_id1][0] + pos[num_id2][0]) / 2., (pos[num_id1][1] + pos[num_id2][1]) / 2.
    conn_1, conn_2  = [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    pos_card_1, pos_card_2 = [0] * 2, [0] * 2
    if num_id1 > num_id2:
        cop = num_id1
        num_id1 = num_id2
        num_id2 = cop
    
    if (num_id1 == 0 and num_id2 == 1) or (num_id1 == 2 and num_id2 == 3): # Relaciones horizontales id mas bajo a la izquierda
        conn_1[0], conn_1[2] = pos[num_id1][0] + W_ENT, x_rel - W_REL
        conn_1[1], conn_1[3] = pos[num_id1][1], y_rel
        conn_2[0], conn_2[2] = pos[num_id2][0] - W_ENT, x_rel + W_REL
        conn_2[1], conn_2[3] = pos[num_id2][1], y_rel
        pos_card_1[0], pos_card_2[0] = pos[num_id1][0] + W_ENT + CARD_WS, pos[num_id2][0] - (W_ENT + CARD_WS)
        pos_card_1[1] = pos[num_id1][1] - CARD_HS if num_id2 == 1 else pos[num_id1][1] + CARD_HS
        pos_card_2[1] = pos[num_id2][1] - CARD_HS if num_id2 == 1 else pos[num_id2][1] + CARD_HS
    elif (num_id1 == 0 and num_id2 == 2) or (num_id1 == 1 and num_id2 == 3): # Relaciones verticales id mas bajo arriba
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1], conn_1[3] = pos[num_id1][1] + H_ENT, y_rel - H_REL
        conn_2[0], conn_2[2] = pos[num_id2][0], x_rel
        conn_2[1], conn_2[3] = pos[num_id2][1] - H_ENT, y_rel + H_REL
        pos_card_1[1], pos_card_2[1] = pos[num_id1][1] + (H_ENT + CARD_HS), pos[num_id2][1] - (H_ENT + CARD_HS)
        pos_card_1[0] = pos[num_id1][0] - CARD_WS if num_id1 == 0 else pos[num_id1][0] + CARD_WS 
        pos_card_2[0] = pos[num_id2][0] - CARD_WS if num_id2 == 2 else pos[num_id2][0] + CARD_WS 
    elif num_id1 == 1 and num_id2 == 2: # Conn1 entidad de arriba Conn2 entidad de abajo
        y_rel += 5 # Evitar colision con entidad numero 5
        conn_1[0], conn_1[2] = pos[num_id2][0], x_rel + W_REL
        conn_1[1], conn_1[3] = pos[num_id2][1] + H_ENT, y_rel
        conn_2[0], conn_2[2] = pos[num_id1][0], x_rel - W_REL
        conn_2[1], conn_2[3] = pos[num_id1][1] - H_ENT, y_rel
        pos_card_1[0], pos_card_2[0] = x_rel - (W_REL + CARD_WS), x_rel + W_REL + CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel - CARD_HS, y_rel + CARD_HS      
    elif num_id1 == 0 and num_id2 == 3: # Conn1 entidad de arriba Conn2 entidad de abajo
        y_rel -= 5 # Evitar colision con entidad numero 5
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel - W_REL
        conn_1[1], conn_1[3] = pos[num_id1][1] + H_ENT, y_rel
        conn_2[0], conn_2[2] = pos[num_id2][0], x_rel + W_REL
        conn_2[1], conn_2[3] = pos[num_id2][1] - H_ENT, y_rel
        pos_card_1[0], pos_card_2[0] = x_rel - (W_REL + CARD_WS), x_rel + W_REL + CARD_WS
        pos_card_1[1], pos_card_2[1] = y_rel + CARD_HS, y_rel - CARD_HS 
    elif num_id2 == 4:
        if num_id1 in [0, 2]:
            conn_1[0], conn_1[2] = pos[4][0] - W_ENT, x_rel
            conn_1[1] = pos[4][1]
            conn_1[3] = y_rel + H_REL if num_id1 == 0 else y_rel - H_REL
            conn_2[0], conn_2[2] = pos[num_id1][0] + 0.5, x_rel
            conn_2[1] = pos[num_id1][1] + H_ENT if num_id1 == 0 else pos[num_id1][1] - H_ENT
            conn_2[3] = y_rel - H_REL if num_id1 == 0 else y_rel + H_REL
            pos_card_1[0] = pos_card_2[0] = x_rel + CARD_WS
            pos_card_1[1], pos_card_2[1] = y_rel - (H_REL + CARD_HS), y_rel + (H_REL + CARD_HS)
        elif num_id1 in [1, 3]:
            conn_1[0], conn_1[2] = pos[4][0] + W_ENT, x_rel
            conn_1[1] = pos[4][1]
            conn_1[3] = y_rel + H_REL if num_id1 == 1 else y_rel - H_REL
            conn_2[0], conn_2[2] = pos[num_id1][0] - 0.5, x_rel
            conn_2[1] = pos[num_id1][1] + H_ENT if num_id1 == 1 else pos[num_id1][1] - H_ENT
            conn_2[3] = y_rel - H_REL if num_id1 == 0 else y_rel + H_REL
            pos_card_1[0] = pos_card_2[0] = x_rel - CARD_WS
            pos_card_1[1], pos_card_2[1] = y_rel - (H_REL + CARD_HS), y_rel + (H_REL + CARD_HS)

    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2