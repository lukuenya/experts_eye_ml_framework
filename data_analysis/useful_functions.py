# Useful functions used for data analysis in my project

#### DIRECTORIES HANDLING 

##### Renaming a directory  `march` as `gait`
import os 

def rename_subfolder(root_folder, old_name, new_name):
    # Iterate over all directories and files in the root directory
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # If the directory is named as old_name
        if os.path.basename(dirpath) == old_name:
            # Form the new directory path
            new_dirpath = os.path.join(os.path.dirname(dirpath), new_name)
            # Rename the directory
            os.rename(dirpath, new_dirpath)
            print(f"Renamed directory {dirpath} to {new_dirpath}")

# Call the function
rename_subfolder("Donnees_t0", "march", "gait")

# --------------------------------------------------------------------------------------------------------

#### This function loads the data from `Donnees_t0`. As the name of subfolder changes (foldername for each individual)
#### i have only to change the name of the subfolder(foldername) because the rest of the path stays unchanged in order to retrieve the .txt files.

def load_data(subfolder_name):
    base_path_marche = "./Donnees_t0/{}/t0/gait/"
    base_path_posture = "./Donnees_t0/{}/t0/posture/"

    marche_data_files = {
        'ce_data': "ACQ_CE.txt",
        'pd_data': "ACQ_PD.txt",
        'pg_data': "ACQ_PG.txt",
        'te_data': "ACQ_TE.txt"
    }

    posture_data_files = {
        'yf_data': "2017-09-21_08_22_12_YF.txt",
        'yo_data': "2017-09-21_08_22_12_YO.txt"
    }

    data_marche = {}
    for name, filename in marche_data_files.items():
        path = base_path_marche.format(subfolder_name) + filename
        data_marche[name] = pd.read_csv(path, sep="\t", skiprows=4)

    data_posture = {}
    for name, filename in posture_data_files.items():
        path = base_path_posture.format(subfolder_name) + filename
        data_posture[name] = pd.read_csv(path, sep="\t")

    return data_marche, data_posture

# Usage
data_marche, data_posture = load_data('foldername') # Replace foldername 




