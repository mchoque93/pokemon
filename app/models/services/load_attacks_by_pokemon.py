from typing import TYPE_CHECKING, List

from app.models.models import Attack
from app.models.orm import db
from app.models.services.serabii_loader import get_soup
if TYPE_CHECKING:
    from app.models.models import Pokemon


def scrape_pokedex_ataque(pokemon: "Pokemon")-> List["str"]:
    url = f"pokedex/{format(str(pokemon.pokedex_number).zfill(3))}.shtml"
    soup = get_soup(url)
    all_table = soup.find_all('table', attrs={'class': 'dextable'})
    all_td = all_table[6].find_all('td', {"class": "fooinfo"})
    lista_ataques = []
    for row in all_td:
        href_ataque = next(iter(row.find_all('a', href=True)), None)
        if href_ataque:
            lista_ataques.append(href_ataque.get_text())
    return lista_ataques

def load_attacks_by_pokemon(pokemon: "Pokemon"):
    lista_ataques = scrape_pokedex_ataque(pokemon)
    for ataque_name in set(lista_ataques):
        ataque = db.session.query(Attack).filter_by(name=ataque_name).first()
        pokemon.attacks.append(ataque)
    db.session.add(pokemon)
    db.session.commit()
