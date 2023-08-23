import os
import pandas as pd
import numpy as np

#lecture des fichiers txt

directory = os.path.join('daphnet/')
if not os.path.exists('daphnet_csv/'):
    os.mkdir('daphnet_csv/')
#data_frames = []
 
new_labels = ['Timestep', 'Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z', 'FoG']
for filename in os.listdir(directory):
    step = 0
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path, sep=' ')
        #data_frames.append(df)
        #print(filename)
        df.columns = new_labels
        df = df[df['FoG'] != 0]
        df = df.dropna(how='all', subset=['Shank_x', 'Shank_y', 'Shank_z'])
        df = df.dropna(how='all', subset=['Thigh_x', 'Thigh_y', 'Thigh_z'])
        df = df.dropna(how='all', subset=['Trunk_x', 'Trunk_y', 'Trunk_z'])
        df = df[(df[['Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z']] <= 6000.0).all(axis=1)]
        df = df[(df[['Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z']] >= -6000.0).all(axis=1)]
        for i in range(len(df)):
            df.iloc[i, 0] = step
            df.iloc[i, 10] -= 1
            step += 1
        df['Shank_z'], df['Shank_y'] = df['Shank_y'], df['Shank_z']
        df['Thigh_z'], df['Thigh_y'] = df['Thigh_y'], df['Thigh_z']
        df['Trunk_z'], df['Trunk_y'] = df['Trunk_y'], df['Trunk_z']
        df.iloc[:,1:10] = df.iloc[:,1:10]
        """
        df = df.assign(Shank_mean=np.sqrt(df['Shank_x']**2 + df['Shank_y']**2 + df['Shank_z']**2))
        df = df.assign(Thigh_mean=np.sqrt(df['Thigh_x']**2 + df['Thigh_y']**2 + df['Thigh_z']**2))
        df = df.assign(Trunk_mean=np.sqrt(df['Trunk_x']**2 + df['Trunk_y']**2 + df['Trunk_z']**2))
        df = df.assign(MEAN=(df['Shank_mean'] + df['Thigh_mean'] + df['Trunk_mean'])/3)
        """

        csv_file = 'daphnet_csv/'+ filename.split(".")[0] + '.csv'
        df.to_csv(csv_file, index=False)

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