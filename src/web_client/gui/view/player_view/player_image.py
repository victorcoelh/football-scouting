import requests
from bs4 import BeautifulSoup


def get_player_image(player_name: str) -> str:
    player_name = player_name.replace(" ", "+")
    url = "https://www.google.com/search?tbm=isch&q="+player_name
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    img_tags = soup.find_all("img")

    for img in img_tags:
        src = img.get("src") # type: ignore
        if src and "http" in src:
            return src # type: ignore
        
    return "./assets/placeholder_avatar.png"
