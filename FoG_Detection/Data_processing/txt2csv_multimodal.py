import os
import pandas as pd

#lecture des fichiers txt

directory = os.path.join('multimodal/')
path = os.path.join('4IMU/')

#data_frames = []

new_labels = [  'step', 'time', 'lTibia_Acc_x', 'lTibia_Acc_y', 'lTibia_Acc_z', 'lTibia_Gyr_x', 'lTibia_Gyr_y', 'lTibia_Gyr_z',
                                'rTibia_Acc_x', 'rTibia_Acc_y', 'rTibia_Acc_z', 'rTibia_Gyr_x', 'rTibia_Gyr_y', 'rTibia_Gyr_z',
                                'Waist_Acc_x',  'Waist_Acc_y',  'Waist_Acc_z',  'Waist_Gyr_x',  'Waist_Gyr_y',  'Waist_Gyr_z',
                                'Wrist_Acc_x',  'Wrist_Acc_y',  'Wrist_Acc_z',  'Wrist_Gyr_x',  'Wrist_Gyr_y',  'Wrist_Gyr_z',
                'FoG']


def directory2csv(directory):
    print(directory)
    if not os.path.exists(path + directory.replace("multimodal/", "")):
        os.mkdir(path + directory.replace("multimodal/", ""))
    for dir in os.listdir(directory):
        if dir.endswith(".txt"):
            print("--> " + dir)
            df = pd.read_csv(directory + '/' + dir, sep=',')
            df.drop(df.columns[2:32], axis=1, inplace=True)
            df.drop(df.columns[8], axis=1, inplace=True)
            df.drop(df.columns[14], axis=1, inplace=True)
            df.drop(df.columns[20], axis=1, inplace=True)
            df.drop(df.columns[26], axis=1, inplace=True)
            df.columns = new_labels
            df.iloc[:,1:-1] = df.iloc[:,1:-1].round(6)
            write_path = path + directory.replace("multimodal/", "") + '/'
            csv_file = write_path + dir.split(".")[0] + '.csv'
            df.to_csv(csv_file, index=False)
        else:
            print(dir)
            directory2csv(os.path.join(directory, dir))
            
    return
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

directory2csv('multimodal/')