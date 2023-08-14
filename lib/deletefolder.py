import os, shutil
from lib.buildings_and_colours import buildings_dict as buildings

# THIS FUNCTION IS UNTESTED

def DeleteFolder(target_folder):
    for b in buildings:
        print("Deleting " + b + target_folder + " folder contents")
        folder = './src/houses/' + b +'/' + target_folder + '/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))