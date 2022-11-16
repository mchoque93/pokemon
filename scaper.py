import argparse
import json
import logging
import bs4
import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

OUTPUT_FILE = 'pokemon.json'

PARSER = argparse.ArgumentParser(description='A Pokémon web scraper')
PARSER.add_argument('-s', '--save', action='store_true',
                    help='save the output to JSON')
PARSER.add_argument('-f', '--first', default=1, type=int,
                    help='the number of the first Pokémon to retrieve')
PARSER.add_argument('-l', '--last', default=1, type=int,
                    help='the number of the last Pokémon to retrieve')
PARSER.add_argument('-v', '--verbose', action='store_true',
                    help='print the Pokémon\'s statistics to console')
ARGS = PARSER.parse_args()


def get_pokemon_data(urls):
    """
    Scrape Pokémon data from Serebii.net and output to console.
    :param urls: URLs to extract the data from.
    """
    pokemon_list = []

    for url in urls:
        LOGGER.info('Extracting data from Serebii.net')
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        try:
            all_divs = soup.find_all('div', attrs={'align': 'center'})
            center_panel_info = all_divs[1].findAll('td', {'class': 'fooinfo'})
        except Exception:
            LOGGER.error(
                'There was an error trying to identify HTML elements on the webpage.')
            raise

        pokemon = dict()
        pokemon['name'] = center_panel_info[1].text
        pokemon['number'] = center_panel_info[3].text
        pokemon['classification'] = center_panel_info[4].text
        pokemon['height'] = (center_panel_info[5].text).split('\r\n\t\t\t')
        pokemon['weight'] = (center_panel_info[6].text).split('\r\n\t\t\t')

        try:
            base_stats_table = soup.find(
                'a', attrs={'name': 'stats'}).find_next('table')
            base_stats_td = base_stats_table.findAll('td')
        except Exception:
            LOGGER.error(
                'There was an error trying to identify HTML elements on the webpage.')
            raise

        pokemon['hit_points'] = int(base_stats_td[8].text)
        pokemon['attack'] = int(base_stats_td[9].text)
        pokemon['defense'] = int(base_stats_td[10].text)
        pokemon['special'] = int(base_stats_td[11].text)
        pokemon['speed'] = int(base_stats_td[12].text)

        if not ARGS.save or ARGS.verbose:
            print_pokemon_data(pokemon)
        LOGGER.info('Adding %s %s to dataset',
                    pokemon['number'], pokemon['name'])
        pokemon_list.append(pokemon)

    if ARGS.save:
        LOGGER.info('Saving to %s', OUTPUT_FILE)
        save_to_json(pokemon_list)
    else:
        LOGGER.info(
            'All Pokémon retrieved! To save to JSON, use the --save flag')


def save_to_json(pokemon_list):
    """
    Save Pokémon array to JSON file.
    :param pokemon_list: Array of Pokémon data.
    """
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as output_file:
        json.dump(pokemon_list, output_file, indent=4)


def print_pokemon_data(pokemon):
    """
    Print formatted Pokémon data.
    :param pokemon: Pokémon object containing statistics.
    """
    print('Name\t\t', pokemon['name'])
    print('Number\t\t', pokemon['number'])
    print('Classification\t', pokemon['classification'])
    print('Height\t\t', ' '.join(str(i) for i in pokemon['height']))
    print('Weight\t\t', ' '.join(str(i) for i in pokemon['weight']))
    print('HP\t\t', pokemon['hit_points'])
    print('Attack\t\t', pokemon['attack'])
    print('Defense\t\t', pokemon['defense'])
    print('Special\t\t', pokemon['special'])
    print('Speed\t\t', pokemon['speed'])


if __name__ == '__main__':
    try:
        URLS = ['https://serebii.net/pokedex/{}.shtml'.format(str(x).zfill(3))
                for x in range(ARGS.first, ARGS.last + 1)]
        get_pokemon_data(URLS)
    except Exception as ex:
        LOGGER.error(ex)
        raise


def function_desfase(tabla, tipo):
    tabla = tabla.withColumn(
        "gf_default_type",
        f.when(
            (f.col("gf_basel_criteria_ent_st_type") == "M")
            & (f.col("gf_default_type") != "S")
            & dates_after_default(),
            "R",
        ).otherwise(f.col("gf_default_type")),
    )
    tabla = tabla.withColumn(
        "gf_ope_default_days_number",
        f.when(
            notmissing("gf_ope_default_days_number") & dates_after_default(),
            f.greatest(
                f.lit(0), f.col("gf_ope_default_days_number") - f.col("desfase")
            ),
        ).otherwise(f.col("gf_ope_default_days_number")),
    )
    tabla = tabla.withColumn(
        "gf_cust_default_days_number",
        f.when(
            notmissing("gf_cust_default_days_number") & dates_after_default(),
            f.greatest(
                f.lit(0), f.col("gf_cust_default_days_number") - f.col("desfase")
            ),
        ).otherwise(f.col("gf_cust_default_days_number")),
    )
    tabla = tabla.withColumn(
        "gf_elapsed_term_number",
        f.when(
            notmissing("gf_elapsed_term_number") & dates_after_default(),
            f.greatest(f.lit(0), f.col("gf_elapsed_term_number") - f.col("desfase")),
        ).otherwise(f.col("gf_elapsed_term_number")),
    )
    if tipo == "mayorista":
        tabla = tabla.withColumn(
            "gf_resdl_trm_title_days_number",
            f.when(
                notmissing("gf_resdl_trm_title_days_number") & dates_after_default(),
                f.greatest(
                    f.lit(0), f.col("gf_resdl_trm_title_days_number") + f.col("desfase")
                ),
            ).otherwise(f.col("gf_resdl_trm_title_days_number")),
        )
        tabla = tabla.withColumn(
            "gf_cont_residual_term_number",
            f.when(
                notmissing("gf_cont_residual_term_number") & dates_after_default(),
                f.greatest(
                    f.lit(0), f.col("gf_cont_residual_term_number") + f.col("desfase")
                ),
            ).otherwise(f.col("gf_cont_residual_term_number")),
        )
    # prioridad 2
    tabla = (
        tabla.withColumn(
            "gf_basel_criteria_ent_st_type",
            f.when(prioridad2() & dates_after_default(), "M").otherwise(
                f.col("gf_basel_criteria_ent_st_type")
            ),
        )
        .withColumn(
            "gf_default_type",
            f.when(prioridad2() & dates_after_default(), "R").otherwise(
                f.col("gf_default_type")
            ),
        )
        .withColumn(
            "gf_cust_default_days_number",
            f.when(
                prioridad2() & dates_after_default(),
                f.months_between(
                    f.lit(f.col(tp_tipo[tipo]["exit"])),
                    f.lit(f.col("gf_init_default_date")),
                )
                / 12,
            ).otherwise(f.col("gf_cust_default_days_number")),
        )
        .withColumn(
            "gf_ope_default_days_number",
            f.when(
            prioridad2() & dates_after_default(),
            f.least(
                f.col("gf_cust_default_days_number"),
                f.col("gf_elapsed_term_number"),
            ),
        )
        .otherwise("gf_ope_default_days_number")
    )
    )
    return tabla

