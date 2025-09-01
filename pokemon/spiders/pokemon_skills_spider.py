from scrapy.http import Response
import scrapy

import json

class PokemonSkillSpider(scrapy.Spider):
    name = "pokemonSkillSpider"
    start_urls = ["https://pokemondb.net/ability"]
    baseUrl = "https://pokemondb.net"

    custom_settings = {
        'ITEM_PIPELINES': {
            'pokemon.pipelines.MongoPipeline': 400,
            'pokemon.pipelines.PokemonPipeline': 300
        }
    }

    def parse(self, response: Response):
        try:
            with open('output\pokemonRaw.json', 'r') as file:
                pokemons = json.load(file);
        
            print(f"JSON: {pokemons}");
        except FileNotFoundError:
            print("Error: 'pokemons.json' not found. Please ensure the file exists.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in 'data.json'.")


        
        
        skillsHash = {};
        rows = response.css('tbody tr')

        for row in rows:
            skillIdentifier = row.css('a::attr(href)').get();
            skillName = row.css('a::text').get();
            desc = row.css('td.cell-med-text::text').get();
            
            skillsHash[skillIdentifier] = {
                "name": skillName,
                "desc": desc,
                "url": self.baseUrl + skillIdentifier
            }

        for pokemon in pokemons:
            pokemon['skills'] = [];
            links = pokemon['linksToSkillPage'];

            for link in links:
                pokemon['skills'].append(skillsHash[link])

            yield {
                "name": pokemon["name"],
                "number": pokemon["number"],
                "size": pokemon["size"],
                "weight": pokemon["weight"],
                "effectiveness": pokemon["effectiveness"],
                "types": pokemon["types"],
                "skills": pokemon["skills"],
                "evolutions": pokemon["evolutions"],
                "evolutionArrowsRaw": pokemon["evolutionArrowsRaw"],
                "url": pokemon["url"],
            }
