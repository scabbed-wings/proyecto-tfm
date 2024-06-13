import subprocess as subp
import utils.ent_model_creator as EMC
import utils.ent_model_positions as EMP
import os
import utils.lexical_model as LM
from utils.tools import rel_by_pos, init_control_flags, set_styles, create_labels

def create_imgs(cont, max_ent, num_file, folder_fodg, folder_img):
    #l = EMC.num_ent_atr(5, 3)
    #print("Lista: ", l)
    #rel = EMC.create_relations(l)
    # print("Relaciones: ", rel)
    init_control_flags() # Init control flags to avoid redundancies
    l, rel = LM.create_lexical_model(max_ent) # Creation of the lexical model
    obj_pos = EMP.pos_ent(l, rel) # Get the positions of the entities
    rel_by_pos(l, rel) # Get the positions of the relations
    #print("Posiciones: ", obj_pos)
    ltr, lta, obs, conn_s = set_styles()
    fin_text, num_id, num_comp = EMC.write_ent_atr(l, obj_pos, obs, conn_s, lta)
    rel_text, rel_pos = EMC.write_relations(rel, obj_pos, num_id, num_comp, l, obs, conn_s, ltr)


    path_csv = f'''{folder_img}/img{num_file}.csv'''
    if os.path.exists(path_csv):
        os.remove(path_csv)
    create_labels(obj_pos, rel_pos, path_csv)
    # Write the FODG files
    cont_text = fin_text + rel_text
    cont_text += '''\n</draw:page>
    </office:drawing>
    </office:body>
    </office:document>'''
    path_file = f'''{folder_fodg}/img{num_file}.fodg'''
    if os.path.exists(path_file):
        os.remove(path_file)

    f = open(path_file, "x",encoding="utf-8")
    f.write(cont + cont_text)
    f.close()
    # Transform the fodg file into an image
    string = f'''\"C:/Program Files/LibreOffice/program/soffice.exe\" --draw --headless --convert-to png:\"draw_png_Export\"'''
    string += f''' \"{path_file}\" --outdir \"{folder_img}\"'''
    proc2 = subp.run(string, shell=True)

if __name__ == "__main__":
    f = open("data_generator/head.xml", "r", encoding="UTF-8")
    contents = f.read()
    f.close()
    path_folder_files = f'''data_generator/fodg'''
    path_folder_img = f'''data_generator/img_fractional'''
    if not os.path.isdir(path_folder_files):
        os.mkdir(path_folder_files)
    if not os.path.isdir(path_folder_img):
        os.mkdir(path_folder_img)
    set_img = 100 # Numero de imágenes por cada grupo de entidades
    num_img = 0
    for i in range(2,6):
        for j in range(set_img):
            num_img += 1
            print(f"-------- CREANDO IMAGEN NUMERO {num_img} ----------------")
            create_imgs(contents, i, num_img, path_folder_files, path_folder_img)