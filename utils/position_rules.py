import utils.globals as gb

def init_diag_vals():
    #print("CONTROL FLAG 2: ", gb.CONTR_FLAG)
    R_DIAG8_LOW = (not gb.CONTR_FLAG[0] and gb.CONTR_FLAG[7] + gb.CONTR_FLAG[6] + gb.CONTR_FLAG[1] >= 1) or \
            (gb.CONTR_FLAG[7] and not gb.CONTR_FLAG[5] and not gb.CONTR_FLAG[9])

    R_DIAG9_UP = (not gb.CONTR_FLAG[0] and not gb.CONTR_FLAG[8] and gb.CONTR_FLAG[7] + gb.CONTR_FLAG[6] + gb.CONTR_FLAG[1] >= 1) or \
                (gb.CONTR_FLAG[6] and not gb.CONTR_FLAG[4] and not gb.CONTR_FLAG[8])
    
    #print("Diagonal por aabajo? ", R_DIAG8_LOW)
    #print("Diagonal por arriba? ", R_DIAG9_UP)
    
    return R_DIAG8_LOW, R_DIAG9_UP

def mod_rules_ent0(id_pos2):
    R_DIAG8_LOW, R_DIAG9_UP = init_diag_vals()
    mod_x, mod_y = 0, 0
    if id_pos2 in [1,2]: # ID pos 1 or pos 2
        if id_pos2 == 1:
            if gb.CONTR_FLAG[4] and (gb.CONTR_FLAG[8] and not R_DIAG8_LOW):
                mod_y = -2
        else:
            if gb.CONTR_FLAG[10] or R_DIAG8_LOW or R_DIAG9_UP:
                mod_x = -2
    else:
        if id_pos2 == 3: # ID pos 3
            # If diagonal relation by lower path
            
            if R_DIAG8_LOW:
                print("Diagonal 9 por abajo")
                mod_y = 9
                mod_x = -6
            else: # Diagonal relation by higher path
                mod_y = -7 # Evitar colision con entidad numero 5
                mod_x = 3 # Evitar colision con entidad numero 5 
        else: # ID pos 4 this position has to be aware of atributes in entity 4
            if not gb.CONTR_FLAG[8] and not gb.CONTR_FLAG[7]:
                mod_x = 2
                mod_y = 2
            else:
                mod_x = 1
                mod_y = -1
    return mod_x, mod_y

def mod_rules_ent1(id_pos2):
    R_DIAG8_LOW, R_DIAG9_UP = init_diag_vals()
    mod_x, mod_y = 0, 0
    if id_pos2 in [2, 3]: # ID pos 2 or pos 3
        if id_pos2 == 2:
            # Diagonal relation by higher path
            if R_DIAG9_UP:
                print("Diagonal 10 por arriba")
                mod_y = -9
                mod_x = -6
            else: # If diagonal relation by lower path
                mod_y = 9
                mod_x = 4
        else: # ID pos 3
            if not R_DIAG8_LOW or not R_DIAG9_UP or gb.CONTR_FLAG[6] or gb.CONTR_FLAG[7]:
                print("Desplazando relacion 1-3")
                mod_x = 3
    else: # ID pos 4
        if not gb.CONTR_FLAG[4]:
            mod_x = -2
            mod_y = 1
        else:
            mod_x = 2
            mod_y = 2
    return mod_x, mod_y

def mod_rules_ent2(id_pos2):
    R_DIAG8_LOW, R_DIAG9_UP = init_diag_vals()
    mod_x, mod_y = 0, 0
    if id_pos2 == 3: # ID pos 3
        if (gb.CONTR_FLAG[5] and gb.CONTR_FLAG[10]) or R_DIAG8_LOW or not R_DIAG9_UP:
            mod_y = 2
    else: # ID pos 4 this position has to be aware of atributes in entity 4
        if gb.CONTR_FLAG[10] or (gb.CONTR_FLAG[9] and not R_DIAG9_UP) or (gb.CONTR_FLAG[8] and R_DIAG8_LOW):
            mod_y = 1
            mod_x = 1.5
    
    return mod_x, mod_y

def mod_rules_ent3():
    mod_x, mod_y = 0, 0
    if gb.CONTR_FLAG[10] and gb.CONTR_FLAG[5]:
        mod_x = -1
        mod_y = -2
    elif not gb.CONTR_FLAG[5]:
        mod_x = -2
        mod_y = -2
    return mod_x, mod_y