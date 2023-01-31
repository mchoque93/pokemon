from typing import TYPE_CHECKING, List

from app.api.repositories.memory_pokemon_repository import MemoryPokemonRepository
from app.models.models import Attack
from app.models.services.serabii_loader import get_soup

memory=MemoryPokemonRepository()
if TYPE_CHECKING:
    from app.models.models import Tipo


def scrape_attack_type_page(tipo: "Tipo") -> List[str]:
    url_tipo = f"attackdex-rby/type/{tipo.name}.shtml"
    soup = get_soup(url_tipo)
    all_td = soup.findAll('td', {'class': 'fooinfo'})
    lista_ataques_tipo = []
    for row in all_td:
        href_ataque = next(iter(row.find_all('a', href=True)), None)
        if href_ataque:
            lista_ataques_tipo.append(href_ataque.get_text())
    return lista_ataques_tipo


def load_attacks_by_tipo(tipo: "Tipo"):
    lista_ataques_tipo = scrape_attack_type_page(tipo)
    for attack_name in lista_ataques_tipo:
        memory.add_attack(attack_name, tipo)
