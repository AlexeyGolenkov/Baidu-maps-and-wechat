import json
from logger import logger, bcolors

def save_json(filename, list):
    try:
        with open(filename, "w") as file:
            json.dump(list, file, indent=4, ensure_ascii=False)

        logger("JSON SAVING", "", f"the file '{filename}' has been saved", bcolors.OKGREEN)
    except:
        logger("JSON SAVING", "", f"the file '{filename}' hasn't been saved", bcolors.FAIL)


def open_json(filename):
    with open(filename) as file:
        return json.load(file)