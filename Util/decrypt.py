#encoding=utf-8

def decrypt_txt_file(filepath):
    '''
    Read annotation info from ".serval" file.

    Args:
        filepath -- the path of ".serval" file
    '''
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = [l[:-1] for l in f.read()] 
            f.close()
        return True, content
    except (UnicodeDecodeError, ValueError) as e:
        return False, "Failed to decode file {0}, error: {1}".format(filepath, e)
    except (IOError, FileNotFoundError) as e:
        return False, "Failed to open file {0}, error: {1}".format(filepath, e)
    return False, "Failed to read file {0}".format(filepath)