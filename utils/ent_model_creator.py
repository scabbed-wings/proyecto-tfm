import random as rnd
from copy import copy
from re import findall

WIDTH, HEIGHT = 21, 29.70
W_ATR, H_ATR = 1, 0.5
W_ENT, H_ENT = 1.25, 1
W_REL, H_REL = 1.5, 1
OBJ_SPACE = 1

def num_ent_atr(max_ent, max_atr):
    l = []
    num_ent = rnd.randint(2, max_ent)
    for i in range(num_ent):
        id = f'''id{i+1}'''
        num_atr = rnd.randint(0, max_atr)
        l.append([id, num_atr])
    return l

def create_relations(ent_atr):
    rel = []
    card = ["0..N", "0..*", "1..1", "1..N", "1..*", "M..N"]
    for elem in ent_atr:
        rel_cr = False
        while rel_cr == False:
            id_rel = rnd.choice(ent_atr)[0]
            if elem[0] in id_rel:
                card_c = rnd.choice(card)
                rel.append([elem[0], id_rel, card_c])              
            elif not elem[0] in id_rel:
                rel_cr = True
                card_c = rnd.choice(card)
                rel.append([elem[0], id_rel, card_c])
    
    sub_filt = []
    for elem in rel:
        rev_cop = copy(elem)
        rev_cop.reverse()
        if not any(elem[:2] == sl[:2] or rev_cop[1:] == sl[:2] for sl in sub_filt):
            sub_filt.append(elem)

    return sub_filt

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
            if atr_pre: x += OBJ_SPACE + (W_ATR * 2)
            if ind == 2:
                y = HEIGHT - y
                y -= OBJ_SPACE + (H_ATR * 2)
            elif ind == 0:
                y += OBJ_SPACE + (H_ATR * 2)
        elif ind == 1 or ind == 3:
            x = WIDTH - x
            if atr_pre: x -= OBJ_SPACE + (W_ATR * 2)
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
    if num_id1 in [0, 2]:
        x_rel = pos[num_id1][0]
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        y_rel = HEIGHT - y_rel if num_id1 == 2 else y_rel
        conn_1[1] = pos[num_id1][1] + H_ENT if num_id1 == 2 else pos[num_id1][1] - H_ENT # Y entidad
        conn_1[3] = y_rel - H_REL if num_id1 == 2 else y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel + W_REL, pos[num_id1][0] + 0.5, y_rel
        conn_2[3] = conn_1[1]

    elif num_id1 in [1, 3]:
        x_rel = pos[num_id1][0] 
        y_rel = HEIGHT - y_rel if num_id1 == 3 else y_rel
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1] = pos[num_id1][1] + H_ENT if num_id1 == 3 else pos[num_id1][1] - H_ENT # Y entidad
        conn_1[3] = y_rel - H_REL if num_id1 == 3 else y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel - W_REL, pos[num_id1][0] - 0.5, y_rel
        conn_2[3] = conn_1[1]
    else:
        x_rel = WIDTH / 2
        y_rel = (HEIGHT / 2) - 2.5
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1], conn_1[3] = pos[num_id1][0] - 1, y_rel + H_REL
        conn_2[0], conn_2[2], conn_2[1] = x_rel - W_REL, pos[num_id1][0] + 0.5, y_rel
        conn_2[3] = conn_1[1]
    
    return x_rel, y_rel, conn_1, conn_2

def pos_rel_asoc(num_id1, num_id2, pos): # Posición para relaciones asociativas
    x_rel, y_rel = (pos[num_id1][0] + pos[num_id2][0]) / 2., (pos[num_id1][1] + pos[num_id2][1]) / 2.
    conn_1, conn_2  = [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    
    if (num_id1 in [0,1] and num_id2 in [1,0]) or (num_id1 in [2,3] and num_id2 in [3,2]):
        conn_1[0], conn_1[2] = pos[num_id1][0] + W_ENT, x_rel - W_REL
        conn_1[1], conn_1[3] = pos[num_id1][1], y_rel
        conn_2[0], conn_2[2] = pos[num_id2][0] - W_ENT, x_rel + W_REL
        conn_2[1], conn_2[3] = pos[num_id2][1], y_rel
    elif (num_id1 in [0,2] and num_id2 in [2,0]) or (num_id1 in [1,3] and num_id2 in [3,1]):
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel
        conn_1[1], conn_1[3] = pos[num_id1][1] + H_ENT, y_rel - H_REL
        conn_2[0], conn_2[2] = pos[num_id2][0], x_rel
        conn_2[1], conn_2[3] = pos[num_id2][1] - H_ENT, y_rel + H_REL
    elif num_id1 in [2,1] and num_id2 in [1,2]: # Conn1 entidad de arriba Conn2 entidad de abajo
        y_rel += 5 # Evitar colision con entidad numero 5
        conn_1[0], conn_1[2] = pos[num_id2][0], x_rel + W_REL
        conn_1[1], conn_1[3] = pos[num_id2][1] + H_ENT, y_rel
        conn_2[0], conn_2[2] = pos[num_id1][0], x_rel - W_REL
        conn_2[1], conn_2[3] = pos[num_id1][1] - H_ENT, y_rel
    elif num_id1 in [0,3] and num_id2 in [3,0]: # Conn1 entidad de arriba Conn2 entidad de abajo
        y_rel -= 5 # Evitar colision con entidad numero 5
        conn_1[0], conn_1[2] = pos[num_id1][0], x_rel - W_REL
        conn_1[1], conn_1[3] = pos[num_id1][1] + H_ENT, y_rel
        conn_2[0], conn_2[2] = pos[num_id2][0], x_rel + W_REL
        conn_2[1], conn_2[3] = pos[num_id2][1] - H_ENT, y_rel
    elif num_id1 == 4 or num_id2 == 4:
        non_centre = num_id1 if num_id2 == 4 else num_id2
        if non_centre in [0, 2]:
            conn_1[0], conn_1[2] = pos[4][0] - W_ENT, x_rel
            conn_1[1] = pos[4][1]
            conn_1[3] = y_rel + H_REL if non_centre == 0 else y_rel - H_REL
            conn_2[0], conn_2[2] = pos[non_centre][0] + 0.5, x_rel
            conn_2[1] = pos[non_centre][1] + H_ENT if non_centre == 0 else pos[non_centre] - H_ENT
            conn_2[3] = y_rel - H_REL if non_centre == 0 else y_rel + H_REL
        elif non_centre in [1, 3]:
            conn_1[0], conn_1[2] = pos[4][0] + W_ENT, x_rel
            conn_1[1] = pos[4][1]
            conn_1[3] = y_rel + H_REL if non_centre == 1 else y_rel - H_REL
            conn_2[0], conn_2[2] = pos[non_centre][0] - 0.5, x_rel
            conn_2[1] = pos[non_centre][1] + H_ENT if non_centre == 1 else pos[non_centre] - H_ENT
            conn_2[3] = y_rel - H_REL if non_centre == 0 else y_rel + H_REL

    return x_rel, y_rel, conn_1, conn_2

def pos_rel(num_id1, num_id2, pos):
    x_rel, y_rel, reflx_flag = 0, 0, False
    conn_1, conn_2 = [0] * 4, [0] * 4 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    if num_id1 == num_id2: # Relacion reflexiva
        x_rel, y_rel, conn_1, conn_2 = pos_rel_relx(num_id1, pos)
        reflx_flag = True
    else: # Relación asociativa
        x_rel, y_rel, conn_1, conn_2 = pos_rel_asoc(num_id1, num_id2, pos)
    
    return x_rel, y_rel, conn_1, conn_2, reflx_flag

def write_relations(l_rel, pos, num_id, num_comp):
    text_r, rel_num, first, second = "", 0, 0, 0
    for elem in l_rel:
        num_id1 = int(findall("\d+", elem[0])[0])
        num_id2 = int(findall("\d+", elem[1])[0])
        if num_id1 != 4 and num_id2 != 4:
            if num_id1 < num_id2:
                first, second = num_id1, num_id2
            else:
                first, second = num_id2, num_id1
        else:
            if num_id1 == 4:
                first = num_id1
                second = num_id2
            else:
                first = num_id2
                second = num_id1
        num_id += 1
        num_comp += 1
        rel_num += 1
        x_rel, y_rel, conn1, conn2, reflx = pos_rel(num_id1 - 1, num_id2 - 1, pos)
        rel_s = f'''\n<draw:custom-shape draw:name="Decision {rel_num}" draw:style-name="gr2" draw:text-style-name="P1" xml:id="id{num_id}" draw:id="id{num_id}" draw:layer="layout" svg:width="{W_REL * 2}cm" svg:height="{H_REL * 2}cm" svg:x="{x_rel}cm" svg:y="{y_rel}cm">
        <text:p text:style-name="P1"><text:span text:style-name="T1">id{num_id}</text:span></text:p>
        <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:mirror-horizontal="false" draw:mirror-vertical="false" draw:glue-points="10800 0 0 10800 10800 21600 21600 10800" draw:text-areas="5400 5400 16200 16200" draw:type="flowchart-decision" draw:enhanced-path="M 0 10800 L 10800 0 21600 10800 10800 21600 0 10800 Z N"/>
        </draw:custom-shape>'''
        num_comp += 1
        conn1_s = f'''\n  <draw:connector draw:style-name="gr5" draw:text-style-name="P3" draw:layer="layout" draw:type="line" svg:x1="{conn1[0]}cm" svg:y1="{conn1[1]}cm" svg:x2="{conn1[2]}cm" svg:y2="{conn1[3]}cm" draw:start-shape="id{first}" draw:end-shape="id{num_id}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                            </draw:connector>'''
        num_comp += 1
        if reflx:
            conn2_s = f'''\n  <draw:connector draw:style-name="gr5" draw:text-style-name="P3" draw:layer="layout" draw:type="line" svg:x1="{conn2[0]}cm" svg:y1="{conn2[1]}cm" svg:x2="{conn2[2]}cm" svg:y2="{conn2[3]}cm" draw:start-shape="id{second}" draw:end-shape="id{num_id}" draw:end-glue-point="1" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                            </draw:connector>'''
        else:
            conn2_s = f'''\n  <draw:connector draw:style-name="gr5" draw:text-style-name="P3" draw:layer="layout" draw:type="line" svg:x1="{conn2[0]}cm" svg:y1="{conn2[1]}cm" svg:x2="{conn2[2]}cm" svg:y2="{conn2[3]}cm" draw:start-shape="id{second}" draw:end-shape="id{num_id}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                            </draw:connector>'''
        text_r += rel_s + conn1_s + conn2_s
    return text_r

def write_ent_atr(ent_atr, pos):
    num_id = len(ent_atr)
    num_proc, num_comp = 0, 0
    text_w, text_c = "", ""
    for ind, elem in enumerate(ent_atr):
        num_comp += 1
        ent_s = f'''\n    <draw:custom-shape draw:name="Process {num_proc}" draw:style-name="gr5" draw:text-style-name="P1" xml:id="{elem[0]}" draw:id="{elem[0]}" draw:layer="layout" svg:width="{W_ENT * 2}cm" svg:height="{H_ENT * 2}cm" svg:x="{pos[ind][0]}cm" svg:y="{pos[ind][1]}cm">
        <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[0]}</text:span></text:p>
        <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:mirror-horizontal="false" draw:mirror-vertical="false" draw:glue-points="10800 0 0 10800 10800 21600 21600 10800" draw:type="flowchart-process" draw:enhanced-path="M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N"/>
        </draw:custom-shape>'''
        text_w += ent_s
        num_proc += 1
        if elem[1] > 0:
            for elem2 in pos[ind][2]:
                num_id += 1
                num_comp += 1
                atr_s =  f'''\n    <draw:custom-shape draw:style-name="gr5" draw:text-style-name="P1" xml:id="id{num_id}" draw:id="id{num_id}" draw:layer="layout" svg:width="{W_ATR * 2}cm" svg:height="{H_ATR * 2}cm" svg:x="{elem2[0]}cm" svg:y="{elem2[1]}cm">
                                <text:p text:style-name="P1"><text:span text:style-name="T1">id{num_id}</text:span></text:p>
                                <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:glue-points="10800 0 3163 3163 0 10800 3163 18437 10800 21600 18437 18437 21600 10800 18437 3163" draw:text-areas="3163 3163 18437 18437" draw:type="ellipse" draw:enhanced-path="U 10800 10800 10800 10800 0 360 Z N"/>
                                </draw:custom-shape>'''
                text_w += atr_s
                x_c = elem2[0] + 1.25 if ind in [0, 2, 4] else elem2[0] - 1.25 # Posicion X de Atributo
                x_e = pos[ind][0] - 1.25 if ind in [0, 2, 4] else pos[ind][0] + 1.25 # Posicion X de Entidad
                conn_s = f'''\n    <draw:connector draw:style-name="gr5" draw:text-style-name="P3" draw:layer="layout" draw:type="line" svg:x1="{x_e}cm" svg:y1="{pos[ind][1]}cm" svg:x2="{x_c}cm" svg:y2="{elem2[1]}cm" draw:start-shape="{elem[0]}" draw:end-shape="id{num_id}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                          </draw:connector>''' 
                text_c += conn_s

    return text_w + text_c, num_id, num_comp