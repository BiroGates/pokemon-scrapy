# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re;

class PokemonPipeline:
    def process_item(self, item, spider):
        print("PROCESSING PIPELINE");
        self.removeDuplicatesEvolutions(item);
        return item
    

    def removeDuplicatesEvolutions(self, pokemon):
        # I can also treat some other data in here;
        pokemonId = pokemon["number"];
        evolutions = pokemon["evolutions"];
        treatedEvolutions = [];
        
        
        for evolution in evolutions:
            if evolution["number"] == pokemonId:
                continue
            treatedEvolutions.append(evolution);
            

        
        
        for idx, treatedEvolution in enumerate(treatedEvolutions):
            evolutionArrow = pokemon["evolutionArrowsRaw"][idx];

            level = self.getLevelInEvolutionArrow(evolutionArrow);
            item = self.getItemInEvolutionArrow(evolutionArrow);

            if level:
                treatedEvolutions[idx]["level"] = level;
            if item:
                treatedEvolutions[idx]["item"] = item;            

        print(f"TREATED EVOLUTIONS: {treatedEvolutions}")
        pokemon["evolutions"] = treatedEvolutions;
        
        return;

    def getLevelInEvolutionArrow(self, evolutionArrow: str):
        levelKeyWordRegex = r"(?<=\()Level [0-9]{2}";
        
        levelFound = re.search(levelKeyWordRegex, evolutionArrow).group();

        if levelFound:
            return levelFound;

        return False;

    def getItemInEvolutionArrow(self, evolutionArrow: str):
        useKeyWordRegex = r"use";
        itemNameExtractorRegex = r"(?<=>)[a-zA-z]+ [a-zA-Z]+(?=<)";

        if re.search(useKeyWordRegex, evolutionArrow):
            itemFound = re.search(itemNameExtractorRegex, evolutionArrow).group();
            print(f"FOUND ITEM: {itemFound}");
            return itemFound;

        return False;
