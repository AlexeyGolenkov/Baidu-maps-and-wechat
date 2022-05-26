import os
import requests
from selenium import webdriver
from countdown import countdown
from logger import *

TIME_BETWEEN_FAILED_REQUESTS = 3
ATTEMPTS_FOR_GET_REQUESTS = 3


def simple_GET(url, save_to_file, create_new, n_attempts = 1):
    logger(f"SIMPLE GET {n_attempts}", url, "start of the function")

    if n_attempts > ATTEMPTS_FOR_GET_REQUESTS:
        logger(f"SIMPLE GET {n_attempts}", url, "FAILED", bcolors.FAIL)
        return

    if not create_new and os.path.isfile(save_to_file):
        logger(f"SIMPLE GET {n_attempts}", url, f"the file '{save_to_file}' does already exist. Delete it or call with attr 'create_new=True'")
        return

    try:
        response = requests.get(url)

        logger(f"SIMPLE GET {n_attempts}", url, "OK", bcolors.OKGREEN)

        if save_to_file == "":
            return response.text

        with open(save_to_file, "w") as file:
            file.write(response.text)
    except:

        logger(f"SIMPLE GET {n_attempts}", url, "the url doesn't response. I'm trying again...")

        countdown(TIME_BETWEEN_FAILED_REQUESTS)
        simple_GET(url, save_to_file, create_new, n_attempts + 1)



def selenium_GET(url, filename, create_new, n_attempts = 1):
    logger(f"SELENIUM GET {n_attempts}", url, "start of the function")

    if n_attempts > ATTEMPTS_FOR_GET_REQUESTS:
        logger(f"SELENIUM GET {n_attempts}", url, "FAILED", bcolors.FAIL)
        return

    if not create_new and os.path.isfile(filename):
        logger(f"SELENIUM GET {n_attempts}", url, f"the file '{filename}' does already exist. Delete it or call with attr 'create_new=True'")
        return

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0")
    try:
        driver = webdriver.Firefox(
            executable_path = "/Users/alexeygolenkov/Work/youtube playlist downloader/geckodriver",
            options=options
        )
        driver.get(url = url)

        logger(f"SELENIUM GET {n_attempts}", url, "OK", bcolors.OKGREEN)

        countdown(3)
        with open(filename, "w") as file:
            file.write(driver.page_source)
    except Exception as ex:
        logger(f"SELENIUM GET {n_attempts}", url, "the url doesn't response. I'm trying again")

        countdown(TIME_BETWEEN_FAILED_REQUESTS)

        selenium_GET(url, filename, create_new, n_attempts + 1)
    finally:
        driver.close()
        driver.quit()
