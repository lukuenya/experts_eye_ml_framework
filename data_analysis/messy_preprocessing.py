# some preprocessing steps used for in my project
# Garbage code but useful ! (Need to modify it )

#### DIRECTORIES HANDLING 

##### Renaming a directory  `march` as `gait`
import os 
import re
import shutil

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


# -----------------------------------------------------------------------------------------------------

#I want a list of the first-level subfolders containing more than two files with names starting with a date and hour in a format like `2017-09-21_08_22_12_`
main_folder = "P:/DATA_OCT_22/stade_2_Global_dataset/New/"
date_hour_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2}_")
string_pattern = re.compile(r"ACQ_")
first_level_subfolder = []

for entry in os.scandir(main_folder):
    if entry.is_dir():
        matched_files_count = 0
        for item in os.scandir(entry.path):
            if item.is_file() and date_hour_pattern.match(item.name):
                matched_files_count +=1

        if matched_files_count == 2 :
            first_level_subfolder.append(entry.path)

print(first_level_subfolder)


# --------------------------------------------------------------------------------------------------------

# Moving `posture` and `marche` data in theirs folders respectively
main_folder = "P:/DATA_OCT_22/stade_2_Global_dataset/New/"
date_hour_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2}_")
acq_pattern = re.compile(r"^ACQ_")

for entry in os.scandir(main_folder):
    if entry.is_dir():
        posture_folder = os.path.join(entry.path, "posture")
        marche_folder = os.path.join(entry.path, "march")

        # Create posture and march folders if they don't exist
        os.makedirs(posture_folder, exist_ok=True)
        os.makedirs(marche_folder, exist_ok=True)

        for item in os.scandir(entry.path):
            if item.is_file():
                if date_hour_pattern.match(item.name):
                    shutil.move(item.path, os.path.join(posture_folder, item.name))

                elif acq_pattern.match(item.name):
                    shutil.move(item.path, os.path.join(marche_folder, item.name))

print('ok')

# ----------------------------------------------------------------------------------------------------------

source_folder = 'P:/DATA_OCT_22/stade_2_Global_dataset/New/'
destination_folder = 'P:/DATA_OCT_22/posture_copy/ici/'

#Get the first level subfolder in both directories
source_subfolders = [name for name in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, name))]

destination_subfolders = [name for name in os.listdir(destination_folder) if os.path.isdir(os.path.join(destination_folder, name))]

# Check the match between the 2 subfolders
matching_subfolders = set(source_subfolders) & set(destination_subfolders)

for subfolder in matching_subfolders:
    for root, dirs, files in os.walk(os.path.join(source_folder, subfolder)):
        # Check if 'features' is in the directories
        if 'Features' in dirs:
            features_dir = os.path.join(root, 'Features')

            # check for 'feat2017-09-21_08_22_12.json' and 'featXsens.json' in the 'features' directory
            if 'feat2017-09-21_08_22_12.json' in os.listdir(features_dir):
                shutil.copytree(features_dir, os.path.join(destination_folder, subfolder, 't0', 'posture', 'Features'), dirs_exist_ok=True)

            elif 'featXsens.json' in os.listdir(features_dir):
                shutil.copytree(features_dir, os.path.join(destination_folder, subfolder, 't0', 'gait', 'Features'), dirs_exist_ok=True)
            

# ----------------------------------------------------------------------------------------------------------

feat_pattern = re.compile(r"^feat")

for entry in os.scandir(destination_folder):
    if entry.is_dir():
        feature_folder = os.path.join(destination_folder, entry, 't0', 'gait', 'Features')

        os.makedirs(feature_folder, exist_ok=True)

        for item in os.walk(os.path.join(destination_folder, entry, 't0' )):
            if item.is_file():
                if feat_pattern.match(item.name):
                    shutil.move(item.path, os.path.join(feature_folder, item.name))
# -------------------------------------------------------------------------------------------------------

# Dro all the empty folders
main_folder = "./copy_v1/"

for entry in os.scandir(main_folder):
    if entry.is_dir():
        posture_folder = os.path.join(entry.path, "posture")
        marche_folder = os.path.join(entry.path, "march")

        if os.path.exists(posture_folder) and not any(os.scandir(posture_folder)):
            shutil.rmtree(posture_folder)

        if os.path.exists(marche_folder) and not any(os.scandir(marche_folder)):
            shutil.rmtree(marche_folder)

print('removed')

# -------------------------------------------------------------------------------------------------

# Move `posture` folder in t0 and `march` in t1
main_folder = "./copy_v1 - Copy/"

for entry in os.scandir(main_folder):
    if entry.is_dir():
        t0_folder = os.path.join(entry.path, "t0")
        t1_folder = os.path.join(entry.path, "t1")

        posture_folder = os.path.join(entry.path, "posture")
        marche_folder = os.path.join(entry.path, "march")

        os.makedirs(t0_folder, exist_ok=True)
        os.makedirs(t1_folder, exist_ok=True)

        if os.path.exists(posture_folder):
            shutil.move(posture_folder, os.path.join(t0_folder, "posture"))

        if os.path.exists(marche_folder):
            shutil.move(marche_folder, os.path.join(t0_folder, "march"))

print('ok')

# ----------------------------------------------------------------------------------------

import os
import gzip
import shutil

def unzip_and_move_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".gz"):
                file_path = os.path.join(dirpath, file)
                
                # Create new file path without .gz
                new_file_path = os.path.join(dirpath, file[:-3])
                
                # Unzip the file
                with gzip.open(file_path, 'rb') as f_in:
                    with open(new_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Delete the .gz file
                os.remove(file_path)

                # Define the destination directory (2nd level)
                destination_dir = os.path.join(root_dir, os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(dirpath)))))
                
                # Create the directory if it doesn't exist
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                
                # Move the unzipped file to the destination directory
                shutil.move(new_file_path, os.path.join(destination_dir, file[:-3]))

unzip_and_move_files('./ici/')

# ----------------------------------------------------------------------------------------------------
# Find list of folder in root and keep equivalent in df
rootDir = 'p:/DATA_OCT_22/stade_2_Global_dataset/Donnees_t0_copy_posture/'
folder_names = [name for name in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, name))]

print(list(folder_names))

# Keep rows where 'Foldername' is in the list of folder names
df = df[df['Foldername'].isin(folder_names)]


# ---------------------------------------------------------------------------------------------------------

import os
import shutil

# Specify the directory you want to start from
rootDir = 'p:/DATA_OCT_22/Data_Oct_2022/Anon_20221010/Donnees'

# Specify the directory where you want to copy folders
destinationDir = 'p:/DATA_OCT_22/stade_2_Global_dataset/New'


# For each directory in the directory tree
for dir_name, subdir_list, file_list in os.walk(rootDir):
    # If the base directory name is in the list of list_col
    if os.path.basename(dir_name) in list_col:
        # Construct the destination path
        dest_path = os.path.join(destinationDir, os.path.basename(dir_name))
        # Copy the directory
        shutil.copytree(dir_name, dest_path)
# -----------------------------------------------------------------------------------------

# Merge partially duplicated rows
def merge_rows_with_more_data(group):
    if len(group) == 1:
        return group
    

    row1, row2 = group.iloc[0], group.iloc[1]
    row1_count = row1.notnull().sum()
    row2_count = row2.notnull().sum()

    if row1_count >= row2_count:
        return row1.combine_first(row2).to_frame().T
    else:
        return row2.combine_first(row1).to_frame().T
    
# Group the Dataframe by 'foldernumber' column
grouped_by = data.groupby('Foldername')

# merge the partially duplicated rows within each group
data_v1 = pd.concat([merge_rows_with_more_data(group) for _, group in grouped_by]).reset_index(drop=True)

data_v1.to_excel('merged_rows_encoded_data.xlsx', index=False)

#--------------------------------------------------------------------------

def merge_rows_with_more_data(group):
    """
    In this code, the merge_rows_with_more_data function goes through each row in a group and uses
    the combine_first method to fill in null values in the base row with values from the current row. 
    This is done for each column in the DataFrame. The result is a DataFrame where each group of duplicate rows
    has been merged into a single row, with each column containing the first non-null value found in the duplicate rows.

    """
    # Use the first row as the base
    base_row = group.iloc[0]
    
    # Iterate over the rest of the rows in the group
    for i in range(1, len(group)):
        # Use combine_first to fill in null values in the base row with values from the current row
        base_row = base_row.combine_first(group.iloc[i])
    
    # Return the merged row
    return base_row

# Group the DataFrame by 'Foldername' column
grouped = all_data_copy.groupby('Foldername')

# Apply the merge_rows_with_more_data function to each group
merged_df = grouped.apply(merge_rows_with_more_data).reset_index(drop=True)

# Print the merged DataFrame
print(merged_df)



