import os
import pandas as pd

#lecture des fichiers txt

directory = os.path.join('figshare/')
os.mkdir('figshare_csv/')

#data_frames = []

new_labels = ['step(133Hz)', 'Acc_x(m/s²)', 'Acc_y', 'Acc_z', 'Gyr_x(deg/s)', 'Gyr_y', 'Gyr_z', 'FoG']
cpt = 0
for filename in os.listdir(directory):
    step = 1
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path, sep='\t')
        df.drop(['Time [s]'], axis=1, inplace=True)
        df.columns = new_labels
        for i in range(len(df)):
            df.iloc[i, 0] = step
            step += 1
        df.iloc[:,1:4] = df.iloc[:,1:4]/(9.81)
        csv_file = 'figshare_csv/'+ filename.split(".")[0] + "_" + str(cpt) + '.csv'
        df.to_csv(csv_file, index=False)
        cpt += 1

# dernière colonne 0 -> Non FoG ; 1 -> FoG


'''Concatenation des fichiers txt
#concatenation des fichiers txt
concatenated_df = pd.concat(data_frames, axis=0, ignore_index=True)
concatenated_df.columns = new_labels
concatenated_df = concatenated_df[concatenated_df['FoG'] != 0]
for i in range(len(concatenated_df)):
    concatenated_df.iloc[i, 0] = step
    step += 1
csv_file = 'ankle_knee_trunk.csv'

concatenated_df.to_csv(csv_file, index=False)
'''

'''Txt to csv'''