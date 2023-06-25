from avalia_sinal import get_probs

#path_sinal = r'C:\Users\vinic\Documents\datasets\sinais_renomeados_kay\Normal\normal19.wav'
#path_sinal = r'C:\Users\vinic\Documents\datasets\sinais_renomeados_kay\Paralisia\paralisia7.wav'
#path_sinal = r'C:\Users\vinic\Documents\datasets\sinais_renomeados_kay\Edema\edema3.wav'
#path_sinal = r'C:\Users\vinic\Documents\datasets\sinais_renomeados_kay\Nódulo\nodulo1.wav'
path_sinal = r'D:\Documentos_HDD\013_postdocIFPB\disciplinas\aulas_PPGEE\material_projetos_FAPS\dataBase1_MAV\dataBase1_MAV\hap7.wav'

path_modelo = r'C:\Users\vinic\Documents\IFPB\Arquitetura\proj-arquit\modelo\project_model.h5'

sdl_p , ptl_p = get_probs(path_sinal,path_modelo)
print(f"Probabilidade de ter patologia: {ptl_p:.2f} %")
print(f"Probabilidade de ter saúde: {sdl_p:.2f} %")