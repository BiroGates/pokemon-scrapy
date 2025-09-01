from scrapy.http import Response
import scrapy

from pokemon.PokemonGetScalarsService import PokemonGetScalarsService


class PokemonSpider(scrapy.Spider):
    name = "pokemonScalarSpider"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    baseUrl = "https://pokemondb.net/pokedex/"

    def parse(self, response: Response):
        pokemonNames = response.css("a.ent-name::text").getall()
        i=0
        for name in pokemonNames:
            yield response.follow(
                self.baseUrl + name,
                callback=self.getPokemons,
                meta={"logger": self.logger},
                dont_filter=True
            )

    def getPokemons(self, response: Response):
        pokemonService = PokemonGetScalarsService(response, response.meta["logger"])
        yield {
            "name": pokemonService.getName(response),
            "number": pokemonService.getNumber(response),
            "size": pokemonService.getSizeInCm(response),
            "types": pokemonService.getTypes(response),
            "evolutions": pokemonService.getEvolutions(response),
            "weight": pokemonService.getWeight(response),
            "effectiveness": pokemonService.getEffectiveness(response),
            "evolutionArrowsRaw": pokemonService.getEvolutionArrows(response),
            "url": self.baseUrl + pokemonService.getName(response).lower(),
            "linksToSkillPage": pokemonService.getLinksToSkillPage(response),
        }