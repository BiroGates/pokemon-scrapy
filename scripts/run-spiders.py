from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from pokemon.spiders.pokemon_scalar_spider import PokemonSpider
from pokemon.spiders.pokemon_skills_spider import PokemonSkillSpider
project_settings = get_project_settings()


settings = {
    "FEEDS": {
        "output/pokemonRaw.json": {
            "format": "json",
            "encoding": "utf8",
            "store_empty": False,
            "fields": None,
            "indent": 4, # Para o JSON ficar bem formatado
            "overwrite": True # Sobrescreve o arquivo a cada execução
        },
    }
}

project_settings.update(settings)
process = CrawlerProcess(project_settings)

# A function to chain the spiders
def run_spiders():
    # Start the first spider
    d1 = process.crawl(PokemonSpider)

    settings = {
        "FEEDS": {
            "output/pokemonTreated.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "fields": None,
                "indent": 4, # Para o JSON ficar bem formatado
                "overwrite": True # Sobrescreve o arquivo a cada execução
            },
        }
    }
    project_settings.update(settings);
    d1.addCallback(lambda _: process.crawl(PokemonSkillSpider))
    # Start the reactor (the event loop that runs everything)
    process.start()

if __name__ == "__main__":
    run_spiders()
