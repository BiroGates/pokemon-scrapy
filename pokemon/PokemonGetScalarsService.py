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
        return weight;

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

    def getEffectiveness(self, response: Response):
        tables = response.css('table.type-table');
        self.logger.info(f"TABLES: {tables}");

        allTypes = []
        allEffectiveness = [];
        
        outpout = [];
        
        i = 0;
        # For some fucking reason its returning 4 tables but in the html we only have 2;
        for table in tables:
            if i > 1:
                break;
            infoRow = table.css('tr');
            
            self.logger.info(f"ITERATING IN THE: {i} TABLE");
            self.logger.info(f"infoRow: {infoRow}");
            
            for idx, row in enumerate(infoRow):
                if idx == 0:
                    allTypes += row.css('th a::attr(title)').getall();
                    self.logger.info(f"typesOutput: {allTypes}");
                else:
                    valuesRaw = row.css('td').getall();
                    self.logger.info(f"valuesRaw: {valuesRaw}");
                    
                    for value in valuesRaw:
                        valuefound = re.search(r'>([^<]+)<', value);
                        if valuefound:
                            self.logger.info(f"VALUE FOUND: {valuefound.group(1)}")
                            allEffectiveness.append(valuefound.group(1));
                        else:
                            allEffectiveness.append("0");
            i+=1;

        for idx in range(len(allTypes)):
            outpout.append({
                "type": allTypes[idx],
                "value": allEffectiveness[idx],
            });

        self.logger.info(f"secondTablevaluesOutpout: {allTypes}");
        self.logger.info(f"secondTablevaluesOutpout: {allEffectiveness}");
        self.logger.info(f"output===: {outpout}");
        
        return outpout;


