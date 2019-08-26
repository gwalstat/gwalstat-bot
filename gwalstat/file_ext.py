from glob import glob

FILE_EXTENSION_CHECK = ["md", "rst"]

def filepath(dirpath):

    reg_list = []

    for ext in FILE_EXTENSION_CHECK:
        reg_list += glob(dirpath+"/**/*."+ ext, recursive=True)

    return reg_list

# filepath("/Users/nick/Gwalstat/gwalstat/")
