import requests
import io, os, time, re, json
from collections import defaultdict

from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image


artists_raw = """<div class="div-col" style="column-width: 22em;">
<ul><li><a href="/wiki/Billy_Apple" title="Billy Apple">Billy Apple</a> (1935–2021)</li>
<li><a href="/wiki/Evelyne_Axell" title="Evelyne Axell">Evelyne Axell</a> (1935–1972)</li>
<li><a href="/wiki/Peter_Blake_(artist)" title="Peter Blake (artist)">Sir Peter Blake</a> (born 1932)</li>
<li><a href="/wiki/Derek_Boshier" title="Derek Boshier">Derek Boshier</a> (born 1937)</li>
<li><a href="/wiki/Pauline_Boty" title="Pauline Boty">Pauline Boty</a> (1938–1966)</li>
<li><a href="/wiki/Patrick_Caulfield" title="Patrick Caulfield">Patrick Caulfield</a> (1936–2005)</li>
<li><a href="/wiki/Allan_D%27Arcangelo" title="Allan D'Arcangelo">Allan D'Arcangelo</a> (1930–1998)</li>
<li><a href="/wiki/Jim_Dine" title="Jim Dine">Jim Dine</a> (born 1935)</li>
<li><a href="/wiki/Burhan_Dogancay" class="mw-redirect" title="Burhan Dogancay">Burhan Dogancay</a> (1929–2013)</li>
<li><a href="/wiki/Robert_Dowd_(artist)" title="Robert Dowd (artist)">Robert Dowd</a> (1936–1996)</li>
<li><a href="/wiki/Rosalyn_Drexler" title="Rosalyn Drexler">Rosalyn Drexler</a> (born 1926)</li>
<li><a href="/wiki/Ken_Elias" title="Ken Elias">Ken Elias</a> (born 1944)</li>
<li><a href="/wiki/Err%C3%B3" title="Erró">Erró</a> (born 1932)</li>
<li><a href="/wiki/Marisol_Escobar" title="Marisol Escobar">Marisol Escobar</a> (1930–2016)</li>
<li><a href="/wiki/James_Gill_(artist)" title="James Gill (artist)">James Gill</a> (born 1934)</li>
<li><a href="/wiki/Dorothy_Grebenak" title="Dorothy Grebenak">Dorothy Grebenak</a> (1913–1990)</li>
<li><a href="/wiki/Red_Grooms" title="Red Grooms">Red Grooms</a> (born 1937)</li>
<li><a href="/wiki/Richard_Hamilton_(artist)" title="Richard Hamilton (artist)">Richard Hamilton</a> (1922–2011)</li>
<li><a href="/wiki/Keith_Haring" title="Keith Haring">Keith Haring</a> (1958–1990)</li>
<li><a href="/wiki/Jann_Haworth" title="Jann Haworth">Jann Haworth</a> (born 1942)</li>
<li><a href="/wiki/David_Hockney" title="David Hockney">David Hockney</a> (born 1937)</li>
<li><a href="/wiki/Dorothy_Iannone" title="Dorothy Iannone">Dorothy Iannone</a> (1933–2022)</li>
<li><a href="/wiki/Robert_Indiana" title="Robert Indiana">Robert Indiana</a> (1928–2018)</li>
<li><a href="/wiki/Jasper_Johns" title="Jasper Johns">Jasper Johns</a> (born 1930)</li>
<li><a href="/wiki/Ray_Johnson" title="Ray Johnson">Ray Johnson</a> (1927–1995)</li>
<li><a href="/wiki/Allen_Jones_(sculptor)" class="mw-redirect" title="Allen Jones (sculptor)">Allen Jones</a> (born 1937)</li>
<li><a href="/wiki/Alex_Katz" title="Alex Katz">Alex Katz</a> (born 1927)</li>
<li><a href="/wiki/Corita_Kent" title="Corita Kent">Corita Kent</a> (1918–1986)</li>
<li><a href="/wiki/Konrad_Klapheck" title="Konrad Klapheck">Konrad Klapheck</a> (1935–2023)</li>
<li><a href="/wiki/Kiki_Kogelnik" title="Kiki Kogelnik">Kiki Kogelnik</a> (1935–1997)</li>
<li><a href="/wiki/Nicholas_Krushenick" title="Nicholas Krushenick">Nicholas Krushenick</a> (1929–1999)</li>
<li><a href="/wiki/Yayoi_Kusama" title="Yayoi Kusama">Yayoi Kusama</a> (born 1929)</li>
<li><a href="/wiki/Gerald_Laing" title="Gerald Laing">Gerald Laing</a> (1936–2011)</li>
<li><a href="/wiki/Roy_Lichtenstein" title="Roy Lichtenstein">Roy Lichtenstein</a> (1923–1997)</li>
<li><a href="/wiki/Richard_Lindner_(painter)" title="Richard Lindner (painter)">Richard Lindner</a> (1901–1978)</li>
<li><a href="/wiki/Peter_Max" title="Peter Max">Peter Max</a> (born 1937)</li>
<li><a href="/wiki/John_McHale_(artist)" title="John McHale (artist)">John McHale</a> (1922–1978)</li>
<li><a href="/wiki/Marta_Minujin" class="mw-redirect" title="Marta Minujin">Marta Minujin</a> (born 1943)</li>
<li><a href="/wiki/Claes_Oldenburg" title="Claes Oldenburg">Claes Oldenburg</a> (1929–2022)</li>
<li><a href="/wiki/Don_Nice" title="Don Nice">Don Nice</a> (1932–2019)</li>
<li><a href="/wiki/Julian_Opie" title="Julian Opie">Julian Opie</a> (born 1958)</li>
<li><a href="/wiki/Eduardo_Paolozzi" title="Eduardo Paolozzi">Eduardo Paolozzi</a> (1924–2005)</li>
<li><a href="/wiki/Peter_Phillips_(artist)" title="Peter Phillips (artist)">Peter Phillips</a> (born 1939)</li>
<li><a href="/wiki/Sigmar_Polke" title="Sigmar Polke">Sigmar Polke</a> (1941–2010)</li>
<li><a href="/wiki/Hariton_Pushwagner" title="Hariton Pushwagner">Hariton Pushwagner</a> (1940–2018)</li>
<li><a href="/wiki/Mel_Ramos" title="Mel Ramos">Mel Ramos</a> (1935–2018)</li>
<li><a href="/wiki/Robert_Rauschenberg" title="Robert Rauschenberg">Robert Rauschenberg</a> (1925–2008)</li>
<li><a href="/wiki/Larry_Rivers" title="Larry Rivers">Larry Rivers</a> (1923–2002)</li>
<li><a href="/wiki/James_Rizzi" title="James Rizzi">James Rizzi</a> (1950–2011)</li>
<li><a href="/wiki/James_Rosenquist" title="James Rosenquist">James Rosenquist</a> (1933–2017)</li>
<li><a href="/wiki/Niki_de_Saint_Phalle" title="Niki de Saint Phalle">Niki de Saint Phalle</a> (1930–2002)</li>
<li><a href="/wiki/Peter_Saul" title="Peter Saul">Peter Saul</a> (born 1934)</li>
<li><a href="/wiki/George_Segal_(artist)" title="George Segal (artist)">George Segal</a> (1924–2000)</li>
<li><a href="/wiki/Colin_Self" title="Colin Self">Colin Self</a> (born 1941)</li>
<li><a href="/wiki/Marjorie_Strider" title="Marjorie Strider">Marjorie Strider</a> (1931–2014)</li>
<li><a href="/wiki/Elaine_Sturtevant" title="Elaine Sturtevant">Elaine Sturtevant</a> (1924–2014)</li>
<li><a href="/wiki/Wayne_Thiebaud" title="Wayne Thiebaud">Wayne Thiebaud</a> (1920–2021)</li>
<li><a href="/wiki/Joe_Tilson" title="Joe Tilson">Joe Tilson</a> (born 1928)</li>
<li><a href="/wiki/Andy_Warhol" title="Andy Warhol">Andy Warhol</a> (1928–1987)</li>
<li><a href="/wiki/Idelle_Weber" title="Idelle Weber">Idelle Weber</a> (1932–2020)</li>
<li><a href="/wiki/John_Wesley_(artist)" title="John Wesley (artist)">John Wesley</a> (1928–2022)</li>
<li><a href="/wiki/Tom_Wesselmann" title="Tom Wesselmann">Tom Wesselmann</a> (1931–2004)</li></ul>
</div>"""

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_wikiart_url(artist):
    artist_hyphened = '-'.join(artist.lower().split(" "))
    return f"https://www.wikiart.org/en/{artist_hyphened}/all-works", artist_hyphened

def remove_pinterest_trim_from_url(img_url):
    pin_small_addition = "!PinterestSmall.jpg"
    if pin_small_addition  in img_url: return img_url.replace(pin_small_addition, "")
    return img_url

def extract_artist_image_urls(artist):
    wiki_url, artist_hyphened = get_wikiart_url(artist)
    
    artist_data = {
        "artist" : artist_hyphened,
        "url" : wiki_url,
        "paintings" : []
    }
    
    
    driver = webdriver.Chrome()
    driver.get(wiki_url)

    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    painting_entries =  soup.find_all('div', attrs={'class': "view-all-works ng-scope", "ng-controller":"MasonryCtrl"})
    
    if len(painting_entries) == 0: return artist_hyphened, artist_data

    url_pattern = r'https?://[\w./()-]+'
    urls = re.findall(url_pattern, painting_entries[0]["ng-init"])

    for j, url in enumerate(urls):
        folder_path = os.path.join("data/", artist_hyphened)
        if not os.path.exists(folder_path): os.makedirs(folder_path)

        file_extension = url.split("/")[-1].split(".")[-1]

        file_path = os.path.join(folder_path, f"{j}.{file_extension}")

        title = url.split("/")[-1][:-4]

        image_info = {
            "id" : j,
            "url" : url,
            "title" : title,
            "file_path" : file_path,
        }
        
        print(image_info)

        # resp_image = requests.get(image_info["url"])

        # if resp_image.status_code == 200:
        #     img = Image.open(io.BytesIO(resp_image.content))
        #     img.save(image_info['file_path'])

        artist_data['paintings'].append(image_info)

    return artist_hyphened, artist_data

if __name__ == '__main__':
    soup = BeautifulSoup(artists_raw, "html.parser")
    list_entries = soup.find_all('a')

    artists = []
    artist_to_images = defaultdict()

    for i in range(len(list_entries)):
        artists.append(list_entries[i].get_text())

    for artist in artists:
        artist_hyphened, artist_data = extract_artist_image_urls(artist)
        artist_to_images[artist_hyphened] = artist_data

    with open("data.json", "w") as jf:
        json.dump(artist_to_images, jf)
    