import os
import pandas as pd

#lecture des fichiers txt

directory = os.path.join('4IMU/')
path = os.path.join('multi/')

#data_frames = []

new_labels = [  'step', 'lTibia_Acc_x', 'lTibia_Acc_y', 'lTibia_Acc_z', 'lTibia_Gyr_x', 'lTibia_Gyr_y', 'lTibia_Gyr_z',
                        'Waist_Acc_x',  'Waist_Acc_y',  'Waist_Acc_z',  'Waist_Gyr_x',  'Waist_Gyr_y',  'Waist_Gyr_z',
                        'Wrist_Acc_x',  'Wrist_Acc_y',  'Wrist_Acc_z',  'Wrist_Gyr_x',  'Wrist_Gyr_y',  'Wrist_Gyr_z',
                'FoG']


def directory2csv(directory):
    print(directory)
    #create directory
    if not os.path.exists(path + directory.replace("4IMU/", "")):
        os.mkdir(path + directory.replace("4IMU/", ""))
    for dir in os.listdir(directory):
        if dir.endswith(".csv"):
            print("--> " + dir)
            df = pd.read_csv(directory + '/' + dir, sep=',')
            df.drop('time', axis=1, inplace=True)
            #delete null columns
            drop_tab = []
            for j, k in enumerate(df.columns):
                if k == 'FoG':
                    break
                if df.iloc[0, j] == 0.0:
                    drop_tab.append(k)
            df.drop(drop_tab, axis=1, inplace=True)
            df.iloc[:,1:-1] = df.iloc[:,1:-1].round(6)
            write_path = path + directory.replace("4IMU/", "") + '/'
            csv_file = write_path + dir.split(".")[0] + '.csv'
            df.to_csv(csv_file, index=False)
        else:
            print(dir)
            directory2csv(os.path.join(directory, dir))
    return

# dernière colonne 0 -> Non FoG ; 1 -> FoG

directory2csv(directory)