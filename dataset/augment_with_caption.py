from tqdm import tqdm

import base64
import os
import requests
import json

api_key = os.getenv("API_KEY_HACKATHON")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

artists = []
painting_num = []
image_paths = []
image_encode = []

for dirs in os.listdir("data/"):
    for image in os.listdir(os.path.join("data/", dirs)):
        path = os.path.join("data/", dirs, image)
        artists.append(dirs)
        painting_num.append(int(image.split(".")[0]))
        image_paths.append(path)
        image_encode.append(encode_image(path))

headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

# with open("data.json", "r") as jf:
#     data_info = json.load(jf)
with open("data_augment.json", "r") as jf:
    data_info = json.load(jf)

def get_prompt_painting_description(artist, paint_num):
    artist_name = " ".join(artist.split("-"))
    painting_name = " ".join(data_info[artist]['paintings'][paint_num]['title'].split("-"))

    prompt_focus = "focusing on the colors, the imagery, the deeper contextual information, the style of the painting, the technique used and the era."
    if "screenshot" in  painting_name:
        return f"Deeply describe this artwork by {artist_name}, " + prompt_focus
    else:
        return f"Deeply describe this artwork with name {painting_name} by {artist_name}, " + prompt_focus

count = 0

for artist, image_path, pn, image_encode in tqdm(zip(artists, image_paths, painting_num, image_encode), total=len(artists)):
    count += 1 
    if count < 321: continue

    file_extension = image_path.split("/")[-1].split(".")[-1]
    prompt = get_prompt_painting_description(artist, int(pn))

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{file_extension};base64,{image_encode}",
                            "detail":"high"
                    }
                    }
                ]
                }
        ],
        "max_tokens": 1105
    }

    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    data_info[artist]["paintings"][pn]["raw_description"] = resp.json()

    if count % 25 == 0:
        with open("data_augment.json", "w") as jf:
            json.dump(data_info, jf)

with open("data_augment.json", "w") as jf:
    json.dump(data_info, jf)
