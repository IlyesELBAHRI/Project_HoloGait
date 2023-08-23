import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

path = os.path.join('multi-sorted/')
freq_ech = 500

def print_infos(directory):
    print(f"-->{directory}")
    cpt_task_fog = 0
    cpt_task_frames = 0
    durations_files = []  # Liste pour stocker les durées totales des fichiers
    durations_fog = []  # Liste pour stocker les durées totales de FoG

    for file in os.listdir(directory):
        print(f"---->{file}")
        df = pd.read_csv(os.path.join(directory, file), sep=',')
        cpt_file_fog = 0
        cpt_frames = 0

        for i in range(len(df)):
            if df.iloc[i, -1] == 1:
                cpt_file_fog += 1
                cpt_task_fog += 1
            cpt_frames += 1
            cpt_task_frames += 1

        duration_file = cpt_frames / freq_ech
        duration_fog = cpt_file_fog / freq_ech
        durations_files.append(duration_file)
        durations_fog.append(duration_fog)

        print(f"FoG % : {cpt_file_fog / cpt_frames * 100}")
        print(f"FoG secondes : {duration_fog} s")

    print(f"Durée totale tache : {round(cpt_task_frames / freq_ech, 3)} s")
    print(f"Durée totale FoG tache : {round(cpt_task_fog / freq_ech, 3)} s")
    print(f"% total FoG tache : {round(cpt_task_fog / cpt_task_frames * 100, 2)} %")

    return cpt_task_fog, cpt_task_frames, durations_files, durations_fog

cpt_total_fog = 0
cpt_total_frames = 0
task_names = []  # Liste pour stocker les noms des tâches
durations_task_files = []  # Liste pour stocker les durées totales des fichiers pour chaque tâche
durations_task_fog = []  # Liste pour stocker les durées totales de FoG pour chaque tâche

for directory in os.listdir(path):
    task_names.append(directory)  # Ajouter le nom de la tâche à la liste
    directory = os.path.join(path, directory)
    cpt_task_fog, cpt_task_frames, durations_files, durations_fog = print_infos(directory)
    cpt_total_fog += cpt_task_fog
    cpt_total_frames += cpt_task_frames
    durations_task_files.append(sum(durations_files))  # Ajouter la durée totale des fichiers pour la tâche
    durations_task_fog.append(sum(durations_fog))  # Ajouter la durée totale de FoG pour la tâche

print(f"Durée totale dataset : {round(cpt_total_frames / freq_ech, 3)} s")
print(f"Durée totale FoG dataset : {round(cpt_total_fog / freq_ech, 3)} s")
print(f"% total FoG dataset : {round(cpt_total_fog / cpt_total_frames * 100, 2)} %")

# Tracer l'histogramme
x = np.arange(2)  # Créer les positions x pour les tâches
width = 0.5  # Largeur des barres dans l'histogramme

fig, ax = plt.subplots()
rects1 = ax.bar(x, [cpt_total_fog / freq_ech, cpt_total_frames / freq_ech], width)

ax.set_ylabel('Duration (s)')
ax.set_title('Total duration of files and FoG for each task')
ax.set_xticks(x)
ax.set_xticklabels(['Total FoG', 'Total files'])
ax.legend()

plt.tight_layout()  # Ajustement automatique de la disposition du tracé
plt.show()
