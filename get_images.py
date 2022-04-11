""" Scrapes images from SerenesForest. """

# CREDIT: Base code written by Jonathan on
# https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup


import re
import os
import requests
from bs4 import BeautifulSoup


def scrape_images(site):
    """
    Scrapes images from site and puts them in img folder.
    :param site: str
    :return: None
    """
    try:
        os.mkdir("img")
    except FileExistsError:
        pass

    if "blazing" in site:
        game = "fe7"
    else:  # "sacred" in site:
        game = "fe8"

    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    if game == "fe8":
        urls = ["https://serenesforest.net" + img['src'] for img in img_tags]
    else:  # game == "fe7":
        urls = [img['src'] for img in img_tags]

    print(f"{len(urls)} urls found. Processing...")
    # print (urls)

    processed = 0
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            print(f"Regex didn't match with the url: {url}")
            continue

        if game == "fe7":
            basename = "fe7" + filename.group(1).lower()
            if "-" in basename:
                basename = basename[:basename.find("-")] + ".png"
            path = os.path.join("img", basename)

        else:  # game == "fe8":
            basename = filename.group(1)
            path = os.path.join("img", basename)
        if basename in ["fe7eleanora.png", "fe8caellach.gif"]:  # non playable characters
            break
        if basename in ["fe8orson.gif"]:  # skipped characters - fe8 orson, e.g.
            continue

        with open(path, 'wb') as file:
            response = requests.get(url)
            file.write(response.content)
            print(f"Processed {basename}.")
            processed += 1

    print(f"Of {len(urls)} urls found, {processed} processed and {len(urls) - processed} skipped.")


if __name__ == "__main__":
    scrape_images('https://serenesforest.net/blazing-sword/characters/introduction/')
    scrape_images('https://serenesforest.net/the-sacred-stones/characters/introduction/')
