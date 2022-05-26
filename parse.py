from logger import logger, bcolors, set_logger_config
from GET_requests import simple_GET
from jsonfunctions import json, save_json
import asyncio
import aiohttp

REWRITE_EVERYTHING = False

def parse_cities_names(what_we_search, do_it):
    if not do_it:
        return

    logger("GET LIST OF MAIN CITIES", "", "start of the function")

    main_cities_request_link = ("https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1"
                    "&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=shareurl"
                   f"&wd={what_we_search}&c=1&src=0&pn=0&sug=0&l=4"
                    "&b=(6960738.085766194,1626935.4738798793;15774880.771956017,8004903.491170261)"
                    "&from=webmap&biz_forward=%7B%22scaler%22:2,%22styles%22:%22pl%22%7D&device_ratio=2"
                    "&auth=OMgZDF%3DVUVCTX42KDJWMSE2fwX3I5RdvuxLERELBRzzt1do71qofD%3DCvYgP1PcGCgYvjPuVtv"
                    "YgPMGvgWv%40uVtvYgPPxRYuVtvYgP%40vYZcvWPCuVtvYgP%40ZPcPPuVtvYgPhPPyheuVtvhgMuxVVty1"
                    "uVtCGYuVt1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3Guxt58Jv7uPYIUvhgMZSguxzBEHLNRTVtcEWe1G"
                    "D8zv7u%40ZPuVtcvY1SGpuzVtc3CuVteuVtegvcguxLERELBRzVteh33uVtrZZWuV&seckey=-1%2C94H7o"
                    "dC4oiQ7p0IvmBpExxVo7XLA3qQ-0_9d5sf2yGMy7KInXvynNDW3ybq-7lwWBww-Za2BwTi-p6pbW-WW8NY4"
                    "ZFyNPFrUahsfqhVLTVzlLrwNe11ytzKJoyglyBWy0KG811AwtH-OEab7AcXUYbq4_3zpFZqc2_t7rrcxZFG"
                    "LG3ihminwg-1of8y1okuO&tn=B_NORMAL_MAP&nn=0&u_loc=4150649,7458515&ie=utf-8"
                    "&t=1648463822824&newfrom=zhuzhan_webmap")

    info_json = json.loads(simple_GET(main_cities_request_link, "", create_new=REWRITE_EVERYTHING))

    logger("GET LIST OF MAIN CITIES", "", "Trying to get main cities that are visible on the main page")

    all_cities = []

    main_cities = info_json["content"]
    for main_city in main_cities:
        all_cities.append(
            {
                "city_id": main_city.get("code"),
                "city_name": main_city.get("name")                
            }
        )

    logger("GET LIST OF MAIN CITIES", "", f"{len(all_cities)} have been succesfully parsed", bcolors.OKGREEN)
    logger("GET LIST OF ADDITIONAL CITIES", "", "Trying to get more cities")

    try:
        regions = info_json["more_city"]
        for region in regions:
            more_cities = region["city"]
            for additional_city in more_cities:
                all_cities.append(
                    {
                        "city_id": additional_city.get("code"),
                        "city_name": additional_city.get("name")                
                    }
                )
    except:
        logger("GET LIST OF ADDITIONAL CITIES", "", "There are no regions on baidu maps")

    logger("GET LIST OF ADDITIONAL CITIES", "", f"{len(all_cities)} have been succesfully parsed with invisible cities", bcolors.OKGREEN)

    save_json(f"{what_we_search}_all_cities_list.json", all_cities)


has_phone_cnt = 0
has_phone_city = {}
contacts = []
n_processed_cities = 0

def make_request_link_for_city(request, city_id, page_number):
    page_number -= 1
    page_start = page_number * 10
    if page_number > 1:
        page_number += 1
    return ("https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct"
           f"&pcevaname=pc4.1&qt=con&from=webmap&c={city_id}&wd={request}&wd2=&pn={page_number}&nn={page_start}"
           "&db=0&sug=0&addr=0&&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=13"
           "&auth=vLLLzTbfd1MK2BbLD5X4exDH2xA4axyauxLBzTzHTHRtBalTBnlcAZzvYgP1PcGCgYvjPuVtvYgPMGvgWv%40uVtvYgPP"
           "xRYuVtvYgP%40vYZcvWPCuVtvYgP%40ZPcPPuVtvYgPhPPyheuVtvhgMuxVVty1uVtCGYuxtE20w5V198P8J9v7u1cv3uVtGccZ"
           "cuVtPWv3GuxBt80SGdFPYIUvhgMZSguxzBEHLNRTVtcEWe1aDYyuVt%40ZPuRtj5IC%40BcvY1SGpuzxtfvMujlBhlAD5GEYED7"
           "7Gz0kMMxXwrZZWuV&seckey=646f10cb77181888e7eef50bc07d45274c5fe0c85c4ae6a2b8a66de6bcc21f3371287d727a5"
           "322140481ce64c70ad1b657a6e09c31496fd4129b0c48c0873df51c1493b0870c4ae16f0f98e4c8f9aa7c716e6f32f0fb3f"
           "4ae40e6dd5b7a990a5c53cde6def8f047d4a1dde68098b2c7294cf6160da49e1fcfae805de53beaa9d2d0450d131818bf17"
           "85644ca34468165cdff21a4fafbe8a6be90db38cd2a5eb2ec9453252a198af9f3701eb24ce14788398cb74fdb7da82510bf"
           "611ec7078fbabca4d36cab653a257c825f0a7d52e77a71079e38b057262012089ed6cc21c251d8d27667386f0a34378f5b9"
           "bbe1ea9e7&device_ratio=1&tn=B_NORMAL_MAP&u_loc=4196984,7433030&ie=utf-8"
           "&t=1632925969664&newfrom=zhuzhan_webmap")

async def get_city_data(session, request, city_id, city_name):
    logger("GET CITY DATA", "", f"with parameters request={request}, city_id={city_id}, city_name={city_name}")

    global has_phone_cnt
    global n_processed_cities

    for page_number in range(1, 21):
        logger("GET CITY DATA", f"parsing page {page_number}", f"with parameters request={request}, city_id={city_id}, city_name={city_name}")

        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
        url = make_request_link_for_city(request, city_id, page_number)
        async with session.get(url=url, headers=headers) as response:
            response_text = await response.text()

            ten_points = json.loads(response_text)
            if not ten_points.get("content"):
                break

            is_end = False
            for point in ten_points["content"]:
                if not point.get('addr'):
                    is_end = True
                    break
                phone_number = "none"
                if point.get("tel"):
                    has_phone_cnt += 1
                    if city_id in has_phone_city:
                        has_phone_city[city_id] += 1
                    else:
                        has_phone_city.update({city_id: 1})
                    phone_number = point.get("tel")
                if phone_number != "none":
                    contacts.append(
                        {
                            "city_id": city_id,
                            "city_name": city_name,
                            "point_name": point["addr"],
                            "contact": phone_number
                        }
                    )
            if is_end:
                break

    n_processed_cities += 1

async def gather_data(request, cities_list_filename):
    with open(cities_list_filename, "r") as file:
        cities = json.load(file)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_number in range(0, len(cities)):
            city_id, city_name = cities[city_number]["city_id"], cities[city_number]["city_name"]
            task = asyncio.create_task(get_city_data(session, request, city_id, city_name))
            tasks.append(task)

        await asyncio.gather(*tasks)

def get_data_by_request(what_we_search):
    parse_cities_names(what_we_search, do_it=True)

    asyncio.run(gather_data(what_we_search, f"{what_we_search}_all_cities_list.json"))

    save_json(f"{what_we_search}_contacts.json", contacts)


def main():
    set_logger_config(OK_responses=True, WARNING_responses=True, FAIL_responses=True)

    # 美容

    what_we_search = input("What to find: ")
    print(f"Searching for {what_we_search}")

    get_data_by_request(what_we_search)
    print(has_phone_cnt)
    print(n_processed_cities)

if __name__ == "__main__":
    main()