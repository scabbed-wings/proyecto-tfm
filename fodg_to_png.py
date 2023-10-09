import subprocess as subp
import utils.ent_model_creator as EMC
import os

WIDTH, HEIGHT = 21, 29.70
W_ATR, H_ATR = 1, 0.5
W_ENT, H_ENT = 1.25, 1
W_REL, H_REL = 1.5, 1
OBJ_SPACE = 1

def create_imgs(cont, num_file,folder_fodg, folder_img):
    l = EMC.num_ent_atr(4, 3)
    #print("Lista: ", l)
    rel = EMC.create_relations(l)
    #print("Relaciones: ", rel)
    obj_pos = EMC.pos_ent(l)
    #print("Posiciones: ", obj_pos)
    fin_text, num_id, num_comp = EMC.write_ent_atr(l, obj_pos)
    rel_text = EMC.write_relations(rel, obj_pos, num_id, num_comp)
    cont_text = fin_text + rel_text
    cont_text += '''\n</draw:page>
    </office:drawing>
    </office:body>
    </office:document>'''
    path_file = f'''{folder_fodg}/img{num_file}.fodg'''

    f = open(path_file, "x",encoding="utf-8")
    f.write(cont + cont_text)
    f.close()
    string = f'''\"C:/Program Files/LibreOffice/program/soffice.exe\" --draw --headless --convert-to png:\"draw_png_Export\"'''
    string += f''' \"{path_file}\" --outdir \"{folder_img}\"'''
    proc2 = subp.run(string, shell=True)

if __name__ == "__main__":
    f = open("proyecto\head.xml", "r", encoding="UTF-8")
    contents = f.read()
    f.close()
    path_folder_files = f'''C:/Users/Miguel Pérez/Desktop/muva/Trabajo Fin de master/proyecto/fodg'''
    path_folder_img = f'''C:/Users/Miguel Pérez/Desktop/muva/Trabajo Fin de master/proyecto/img'''
    if not os.path.isdir(path_folder_files):
        os.mkdir(path_folder_files)
    if not os.path.isdir(path_folder_img):
        os.mkdir(path_folder_img)
    num_img = 10
    for i in range(num_img):
        create_imgs(contents, i + 1, path_folder_files, path_folder_img)