import random as rnd
from copy import copy
import utils.ent_model_positions as EMP
from utils.tools import get_pos_ent, size_object
import utils.globals as gb

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
                card_1 = rnd.choice(card)
                card_2 = rnd.choice(card)
                rel.append([elem[0], id_rel, card_1, card_2])              
            elif not elem[0] in id_rel:
                rel_cr = True
                card_1 = rnd.choice(card)
                card_2 = rnd.choice(card)
                rel.append([elem[0], id_rel, card_1, card_2])  
    
    sub_filt = []
    for elem in rel:
        rev_cop = copy(elem)
        rev_cop.reverse()
        if not any(elem[:2] == sl[:2] or rev_cop[2:] == sl[:2] for sl in sub_filt):
            sub_filt.append(elem)

    return sub_filt

def pos_rel(num_id1, num_id2, ind_pos1, ind_pos2, pos, w_rel, h_rel):
    x_rel, y_rel, gp = 0, 0, [0] * 4
    conn_1, conn_2, pos_card_1, pos_card_2 = [0] * 4, [0] * 4, [0] * 2, [0] * 2 # 1: Conexion entidad relacion 2: Conexion relacion entidad
    if num_id1 == num_id2: # Relacion reflexiva
        x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp = EMP.pos_rel_relx(num_id1, ind_pos1, pos, w_rel, h_rel)
    else: # Relación asociativa
        x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp = EMP.pos_rel_asoc(num_id1, num_id2, ind_pos1, ind_pos2, w_rel, h_rel, pos)
    
    # print("X_rel: ", x_rel, " Y_rel: ", y_rel, " Card1:", pos_card_1, " Card2:", pos_card_2)
    return x_rel, y_rel, conn_1, conn_2, pos_card_1, pos_card_2, gp

def write_relations(l_rel, pos, num_id, num_comp, ent_atr, rel_style, line_style, line_type):
    text_r, rel_num, rel_pos = "", 0, []
    # Seleccion de estilos
    #rel_style = rnd.choice(gb.OBJ_STYLES)
    #line_style = rnd.choice(gb.LINE_STYLES)
    #line_type = rnd.choice(gb.REL_LINE_STYLES)
    print("CONTROL_FLAG: ", gb.CONTR_FLAG)
    for elem in l_rel:
        id1, id2 = elem[0], elem[1]
        if id1 != id2:
            num_id1, ind_pos1 = get_pos_ent(id1, ent_atr)
            num_id2, ind_pos2 = get_pos_ent(id2, ent_atr)
        else:
            num_id1, ind_pos1 = get_pos_ent(id1, ent_atr)
            num_id2, ind_pos2 = num_id1, ind_pos2


        h_rel, w_rel = size_object(elem[4], "rel")
        if num_id1 > num_id2:
            cop, cop2, cop3 = num_id2, ind_pos2, id2
            num_id2, ind_pos2, id2 = num_id1, ind_pos1, id1
            num_id1, ind_pos1, id1 = cop, cop2, cop3
        num_id += 1
        num_comp += 1
        rel_num += 1
        x_rel, y_rel, conn1, conn2, pos_card_1, pos_card_2, gp = pos_rel(num_id1, num_id2, ind_pos1, ind_pos2, pos, w_rel, h_rel)
        rel_s = f'''\n<draw:custom-shape draw:name="Decision {rel_num}" draw:style-name="{rel_style}" draw:text-style-name="P1" xml:id="id{num_id}" draw:id="id{num_id}" draw:layer="layout" svg:width="{w_rel * 2}cm" svg:height="{h_rel * 2}cm" svg:x="{x_rel}cm" svg:y="{y_rel}cm">
        <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[4]}</text:span></text:p>
        <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:mirror-horizontal="false" draw:mirror-vertical="false" draw:glue-points="10800 0 0 10800 10800 21600 21600 10800" draw:text-areas="5400 5400 16200 16200" draw:type="flowchart-decision" draw:enhanced-path="M 0 10800 L 10800 0 21600 10800 10800 21600 0 10800 Z N"/>
        </draw:custom-shape>'''
        num_comp += 1
        if (num_id1 == 0 and num_id2 == 3) or (num_id1 == 1 and num_id2 == 2):
            # Sin gluepoints
            conn1_s = f'''\n  <draw:connector draw:style-name="{line_style}" draw:text-style-name="P3" draw:layer="layout" {line_type} svg:x1="{conn1[0]}cm" svg:y1="{conn1[1]}cm" svg:x2="{conn1[2]}cm" svg:y2="{conn1[3]}cm" draw:start-shape="id{id1}"  draw:end-shape="id{num_id}" draw:end-glue-point="{gp[1]}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                <text:p/>
                        </draw:connector>'''
        else:
            conn1_s = f'''\n  <draw:connector draw:style-name="{line_style}" draw:text-style-name="P3" draw:layer="layout" {line_type} svg:x1="{conn1[0]}cm" svg:y1="{conn1[1]}cm" svg:x2="{conn1[2]}cm" svg:y2="{conn1[3]}cm" draw:start-shape="id{id1}" draw:start-glue-point="{gp[0]}" draw:end-shape="id{num_id}" draw:end-glue-point="{gp[1]}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                        <text:p/>
                            </draw:connector>'''
        
        num_comp += 1
        if (num_id1 == 0 and num_id2 == 3) or (num_id1 == 1 and num_id2 == 2):
            # Sin gluepoints
            conn2_s = f'''\n  <draw:connector draw:style-name="{line_style}" draw:text-style-name="P3" draw:layer="layout" {line_type} svg:x1="{conn2[0]}cm" svg:y1="{conn2[1]}cm" svg:x2="{conn2[2]}cm" svg:y2="{conn2[3]}cm" draw:start-shape="id{id2}" draw:end-shape="id{num_id}" draw:end-glue-point="{gp[3]}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                            <text:p/>
                        </draw:connector>''' 
        else:

            conn2_s = f'''\n  <draw:connector draw:style-name="{line_style}" draw:text-style-name="P3" draw:layer="layout" {line_type} svg:x1="{conn2[0]}cm" svg:y1="{conn2[1]}cm" svg:x2="{conn2[2]}cm" svg:y2="{conn2[3]}cm" draw:start-shape="id{id2}" draw:start-glue-point="{gp[2]}" draw:end-shape="id{num_id}" draw:end-glue-point="{gp[3]}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                </draw:connector>'''

        card1_s = f'''\n    <draw:frame draw:style-name="gr14" draw:text-style-name="P5" draw:layer="layout" svg:width="1.5cm" svg:height="0.4cm" svg:x="{pos_card_1[0]}cm" svg:y="{pos_card_1[1]}cm">
                                <draw:text-box>
                                <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[2]}</text:span></text:p>
                                </draw:text-box>
                            </draw:frame>'''
        card2_s = f'''\n    <draw:frame draw:style-name="gr14" draw:text-style-name="P5" draw:layer="layout" svg:width="1.5cm" svg:height="0.4cm" svg:x="{pos_card_2[0]}cm" svg:y="{pos_card_2[1]}cm">
                                <draw:text-box>
                                <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[3]}</text:span></text:p>
                                </draw:text-box>
                            </draw:frame>'''
        text_r += rel_s + conn1_s + conn2_s + card1_s + card2_s
        rel_pos.append([x_rel, y_rel, w_rel, h_rel])
    return text_r, rel_pos

def write_ent_atr(ent_atr, pos, obj_style, conn_style, line_type):
    num_id = len(ent_atr)
    num_proc, num_comp = 0, 0
    text_w, text_c = "", ""
    #Seleccion de estilos para la imagen
    #ent_style = rnd.choice(gb.OBJ_STYLES)
    #atr_style = rnd.choice(gb.OBJ_STYLES)
    for ind, elem in enumerate(ent_atr):
        num_comp += 1
        pos_img = elem[3]
        ent_s = f'''\n    <draw:custom-shape draw:name="Process {num_proc}" draw:style-name="{obj_style}" draw:text-style-name="P1" xml:id="{elem[0]}" draw:id="{elem[0]}" draw:layer="layout" svg:width="{pos[ind][3] * 2}cm" svg:height="{pos[ind][4] * 2}cm" svg:x="{pos[ind][0]}cm" svg:y="{pos[ind][1]}cm">
        <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[2]}</text:span></text:p>
        <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:mirror-horizontal="false" draw:mirror-vertical="false" draw:glue-points="10800 0 0 10800 10800 21600 21600 10800" draw:type="flowchart-process" draw:enhanced-path="M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N"/>
        </draw:custom-shape>'''
        text_w += ent_s
        num_proc += 1
        if len(elem[1]) > 0:
            for ind_atr, elem2 in enumerate(pos[ind][2]):
                num_id += 1
                num_comp += 1
                atr_s =  f'''\n    <draw:custom-shape draw:style-name="{obj_style}" draw:text-style-name="P1" xml:id="id{num_id}" draw:id="id{num_id}" draw:layer="layout" svg:width="{elem2[2] * 2}cm" svg:height="{elem2[3] * 2}cm" svg:x="{elem2[0]}cm" svg:y="{elem2[1]}cm">
                                <text:p text:style-name="P1"><text:span text:style-name="T1">{elem[1][ind_atr]}</text:span></text:p>
                                <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:glue-points="10800 0 3163 3163 0 10800 3163 18437 10800 21600 18437 18437 21600 10800 18437 3163" draw:text-areas="3163 3163 18437 18437" draw:type="ellipse" draw:enhanced-path="U 10800 10800 10800 10800 0 360 Z N"/>
                                </draw:custom-shape>'''
                text_w += atr_s
                x_c = elem2[0] + 2 * elem2[3] if pos_img in [0, 2, 4] else elem2[0] # Posicion X de Atributo
                x_e = pos[ind][0] if pos_img in [0, 2, 4] else pos[ind][0] + pos[ind][3] # Posicion X de Entidad
                gp_c = 1 if pos_img in [0,2,4] else 6
                gp_e = 3 if pos_img in [0,2,4] else 1
                conn_s = f'''\n    <draw:connector draw:style-name="{conn_style}" draw:text-style-name="P3" draw:layer="layout" {line_type} svg:x1="{x_e}cm" svg:y1="{pos[ind][1]}cm" svg:x2="{x_c}cm" svg:y2="{elem2[1]}cm" draw:start-shape="{elem[0]}" draw:start-glue-point="{gp_e}" draw:end-shape="id{num_id}" draw:end-glue-point="{gp_c}" svg:d="M13107 11077h1237v-1h1234" svg:viewBox="0 0 2472 2">
                                    <text:p/>
                                          </draw:connector>''' 
                text_c += conn_s

    return text_w + text_c, num_id, num_comp