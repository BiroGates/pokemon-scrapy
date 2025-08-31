import re
from typing import List
from scrapy.http import Response


class PokemonGetScalarsService:
    baseUrl = "https://pokemondb.net/pokedex/"

    def __init__(self, response: Response, logger):
        self.response = response
        self.logger = logger

    def getName(self, response):
        name = response.css("main h1::text").get()
        return name

    def getNumber(self, response):
        number = response.css("strong::text").get()
        return int(number);

    def getSizeInCm(self, response):
        size = response.css("table.vitals-table tr:contains('Height') td::text").get()
        return size;

    def getWeight(self, response):
        weight = response.css("table.vitals-table tr:contains('Weight') td::text").get()
        treatedWeight = re.sub(r'\s[a-z]', '', weight.split(' ')[0])
        return treatedWeight

    def getTypes(self, response):
        types = response.css("table.vitals-table td a.type-icon::text").getall()
        return types

    def getEvolutions(self, response):
        evolutions = []
        cards = response.css("div.infocard")
        
        for card in cards:
            evolution = {};
            evolution["number"] = int(card.css("div.infocard small::text").get().replace("#", ""));
            evolution["name"] = card.css("div.infocard a.ent-name::text").get()
            evolution["url"] = self.baseUrl + evolution["name"].lower()
            evolutions.append(evolution)
        
        return evolutions

    def getEvolutionArrows(self, response):
        evolutionArrowsRaw = response.css("span.infocard-arrow").getall()
        return evolutionArrowsRaw

    def getLinksToSkillPage(self, response: Response):
        skillsRaw = response.css("table.vitals-table tr:contains('Abilities') td span a::attr(href)").getall()
        return skillsRaw;
