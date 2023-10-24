H_LINE, W_LET = 0.5, 0.3125

def size_object(words, obj_type):
    h_obj, w_obj = 0, 0
    max_word_len = 8 if obj_type == "ent" or obj_type == "atr" else 12
    add_h = 0.5 if obj_type == "rel" else 0
    if len(words) <= max_word_len:
        h_obj += H_LINE + add_h
        w_obj += len(words) * W_LET
    else:
        num_l = int(len(words)/max_word_len)
        w_obj += max_word_len * W_LET
        h_obj += (H_LINE * num_l) + add_h
    
    return h_obj/2, w_obj/2

def has_reflx_rel(id_ent, rel):
    for elem in rel:
        if elem[0] == elem[1] == id_ent:
            h, _ = size_object(elem[4], "rel")
            return h
    return 0

def get_pos_ent(id_ent, ent_atr):
    for elem in ent_atr:
        if elem[0] == id_ent:
            return elem[3]