import glob
import json

def fromJsonToDict(path):
    """
    Return the requestd JSON file as a dictionary.
    """
    result_dict = {}
    with open(path, 'r', encoding='latin-1') as filehandle:
        result_dict = json.load(filehandle)
    return result_dict

def getobjattr(obj, attributename):
    """
    If 'obj' has the requested attribute, returns the attribute. Otherwise None.
    """
    if hasattr(obj, attributename):
        return obj.__dict__.get(attributename)
    return None

def getListOfFiles(path, file_extension):
    """
    Return a list of files in the path-direactory matching the given file_extension.
    If file_extension is empty all files in the directory will be returned.
    """
    print("{}*.{}".format(path, file_extension))
    return glob.glob("{}*.{}".format(path, file_extension))

def extractValue(key, dict):
    """
    Geven a 'key', the method returns the related value from the 'dict' dictionary.
    If dict has no keys of value "key" the method returns None.
    """
    if key is None:
        return None
    return None if dict.get(key) is None else dict.get(key)