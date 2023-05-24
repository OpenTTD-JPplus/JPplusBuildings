import os, shutil
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

for b in buildings:
    print("Deleting " + b + " switch folder contents")
    folder = './src/houses/' + b +'/variants/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))