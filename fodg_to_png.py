import subprocess as subp
import utils.ent_model_creator as EMC
import utils.ent_model_positions as EMP
import os
import utils.lexical_model as LM

def create_imgs(cont, num_file,folder_fodg, folder_img):
    #l = EMC.num_ent_atr(5, 3)
    #print("Lista: ", l)
    #rel = EMC.create_relations(l)
    # print("Relaciones: ", rel)
    l, rel = LM.create_lexical_model()
    obj_pos = EMP.pos_ent(l, rel)
    #print("Posiciones: ", obj_pos)
    fin_text, num_id, num_comp = EMC.write_ent_atr(l, obj_pos)
    rel_text = EMC.write_relations(rel, obj_pos, num_id, num_comp)
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
    string = f'''\"C:/Program Files/LibreOffice/program/soffice.exe\" --draw --headless --convert-to png:\"draw_png_Export\"'''
    string += f''' \"{path_file}\" --outdir \"{folder_img}\"'''
    proc2 = subp.run(string, shell=True)

if __name__ == "__main__":
    f = open("head.xml", "r", encoding="UTF-8")
    contents = f.read()
    f.close()
    path_folder_files = f'''fodg'''
    path_folder_img = f'''img'''
    if not os.path.isdir(path_folder_files):
        os.mkdir(path_folder_files)
    if not os.path.isdir(path_folder_img):
        os.mkdir(path_folder_img)
    num_img = 20
    for i in range(num_img):
        create_imgs(contents, i + 1, path_folder_files, path_folder_img)