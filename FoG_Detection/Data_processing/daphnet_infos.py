import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

path = os.path.join('daphnet_csv/')
freq_ech = 64

def print_infos(directory):
    print(f"-->{directory}")
    cpt_task_fog = 0
    cpt_task_frames = 0

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

        print(f"FoG % : {cpt_file_fog / cpt_frames * 100}")
        print(f"FoG secondes : {duration_fog} s")


    return cpt_task_fog, cpt_task_frames

cpt_total_fog, cpt_total_frames = print_infos(path)


print(f"Durée totale dataset : {round(cpt_total_frames / freq_ech, 3)} s")
print(f"Durée totale FoG dataset : {round(cpt_total_fog / freq_ech, 3)} s")
print(f"% total FoG dataset : {round(cpt_total_fog / cpt_total_frames * 100, 2)} %")

# Tracer l'histogramme
x = np.arange(2)  # Créer les positions x pour les tâches
width = 0.5  # Largeur des barres dans l'histogramme

fig, ax = plt.subplots()
rects1 = ax.bar(x, [cpt_total_fog / freq_ech, cpt_total_frames / freq_ech], width)

ax.set_ylabel('Duration (s)')
ax.set_title('Total duration of files and FoG for Daphnet dataset')
ax.set_xticks(x)
ax.set_xticklabels(['Total FoG', 'Total files'])
ax.legend()

plt.tight_layout()  # Ajustement automatique de la disposition du tracé
plt.show()

