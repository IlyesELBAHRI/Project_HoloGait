import os
import pandas as pd

#lecture des fichiers txt

directory = os.path.join('multi/')
path = os.path.join('multi-sorted/')
"""
os.mkdir(path + "task_1")
os.mkdir(path + "task_2")
os.mkdir(path + "task_3")
os.mkdir(path + "task_4")
os.mkdir(path + "task_others")
"""
def directory2csv(directory):
    print(directory)
    for dir in os.listdir(directory):
        if dir.endswith(".csv"):
            print("--> " + dir)
            df = pd.read_csv(directory + '/' + dir, sep=',')
            file_name = ""
            k=0
            while k < len(df.columns):
                if df.columns[k].startswith("lTibia"):
                    file_name += "lTibia_"
                    k += 6
                elif df.columns[k].startswith("rTibia"):
                    file_name += "rTibia_"
                    k += 6
                elif df.columns[k].startswith("Waist"):
                    file_name += "Waist_"
                    k += 6
                elif df.columns[k].startswith("Wrist"):
                    file_name += "Wrist_"
                    k += 6
                else:
                    k += 1
            
            if dir.startswith("task_1"):
                write_path = path + "task_1/" + directory.replace("multi/", "")
            elif dir.startswith("task_2"):
                write_path = path + "task_2/" + directory.replace("multi/", "")
            elif dir.startswith("task_3"):
                write_path = path + "task_3/" + directory.replace("multi/", "")
            elif dir.startswith("task_4"):
                write_path = path + "task_4/" + directory.replace("multi/", "")
            else:
                write_path = path + "task_others/" + directory.replace("multi/", "") + dir.split(".")[0]
            write_path = write_path.replace("\\", "_")
            csv_file = write_path + "_" + file_name +'.csv'
            print(csv_file)
            df.to_csv(csv_file, index=False)
        else:
            print(dir)
            directory2csv(os.path.join(directory, dir))
    return

# dernière colonne 0 -> Non FoG ; 1 -> FoG

directory2csv(directory)
