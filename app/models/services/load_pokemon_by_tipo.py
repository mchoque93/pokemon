from typing import TYPE_CHECKING, Union, List

from itertools import groupby

from app.models.models import Pokemon, db
from app.models.services.serabii_loader import get_soup

if TYPE_CHECKING:
    from app.models.models import Tipo


def scrape_pokemon_type_page(tipo: "Tipo") -> List[List[Union[str, float]]]:
    url = f"pokedex/{tipo.name}.shtml"
    soup = get_soup(url)
    all_divs = soup.find_all('table', attrs={'align': 'center'})
    center_panel_info = all_divs[0].findAll('td', {'class': 'fooinfo'})
    raw_stats = [x.get_text().strip() for x in center_panel_info]
    stats = [row for row in raw_stats if row != '']
    result = [list(v) for k, v in groupby(stats, lambda x: x.find('#'))]
    i = 0
    lista_stats = []
    while i < len(result):
        lista_stats.append(result[i] + result[i + 1])
        i += 2
    return lista_stats


def load_pokemon_by_tipo(tipo: "Tipo"):
    lista_stats = scrape_pokemon_type_page(tipo)

    for pokedex_id, pokemon_name, hp, attack, defense, special, speed in lista_stats:
        pokemon = db.session.query(Pokemon).filter_by(name=pokemon_name).first()
        if not pokemon:
            Pokemon.add_pokemon(int(pokedex_id.replace("#", "")), pokemon_name, int(hp), int(attack), int(defense),
                                int(special), int(speed), [tipo])
        else:
            pokemon.tipos.append(tipo)
            pokemon.save()
