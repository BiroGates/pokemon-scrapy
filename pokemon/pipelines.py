# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re;
import pymongo



class PokemonPipeline:
    def process_item(self, item, spider):
        print("PROCESSING PIPELINE");
        self.removeDuplicatesEvolutions(item);
        self.removeDuplicatesTypes(item);
        self.converteSizeInCm(item);
        self.convertWeight(item);
        self.treatEffectiveness(item);
        return item
    

    def removeDuplicatesEvolutions(self, pokemon):
        try:
            pokemonNumber = pokemon["number"];
            evolutions = pokemon["evolutions"];
            evolutionsWithoutMainPokemon = [];
            evolutionsPayload = [];
            
            for evolution in evolutions:
                if evolution["number"] == pokemonNumber:
                    continue
                evolutionsWithoutMainPokemon.append(evolution);
            
            
            for idx, treatedEvolution in enumerate(evolutionsWithoutMainPokemon):
                evolutionArrow = pokemon["evolutionArrowsRaw"][idx];
                if treatedEvolution["number"] <= pokemonNumber:
                    continue;

                # Setting level and items for the evolution if exists
                level = self.getLevelInEvolutionArrow(evolutionArrow);
                item = self.getItemInEvolutionArrow(evolutionArrow);
                
            

                if level:
                    treatedEvolution["level"] = level;
                if item:
                    treatedEvolution["item"] = item;            

                evolutionsPayload.append(treatedEvolution);
            
            # This property is useless now;
            del pokemon["evolutionArrowsRaw"];
            pokemon["evolutions"] = evolutionsPayload;
        except Exception as e:
                print(f"GOT AN ERROR ON removeDuplicatesEvolutions WITH POKEMON: {pokemon} AND ERROR MESSAGE: {e}")

    def getLevelInEvolutionArrow(self, evolutionArrow: str):
        levelKeyWordRegex = r"(?<=\()Level [0-9]{1,2}";
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

    def removeDuplicatesTypes(self, pokemon):
        try:
            # 100% sure there is a better way to do it, but I'm new in this dogshit language!
            types = pokemon["types"];
            typesPayload = [];
            typesSet = set();

            for type in types:
                if type in typesSet:
                    continue;
                typesPayload.append(type);
                typesSet.add(type);

            pokemon["types"] = typesPayload
        except Exception as e:
            print(f"GOT AN ERROR ON removeDuplicatesTypes WITH POKEMON: {pokemon} AND ERROR MESSAGE: {e}")


    def converteSizeInCm(self, pokemon):
        try:
            numbersRegex = r"^[0-9]{0,3}.[0-9]{0,3}";
            treatedSize = float(re.search(numbersRegex, pokemon["size"]).group());
            pokemon["size"] = round(treatedSize * 100, 2);
        except Exception as e:
            print(f"GOT AN ERROR ON converteSizeInCm WITH POKEMON: {pokemon} AND ERROR MESSAGE: {e}")


    def convertWeight(self, pokemon):
        try:
            numbersRegex = r"^[0-9]{0,3}.[0-9]{0,3}";
            treatedWeight = float(re.search(numbersRegex, pokemon["weight"]).group());
            pokemon["weight"] = round(treatedWeight, 2);
    
        except Exception as e:
            print(f"GOT AN ERROR ON convertWeight WITH POKEMON: {pokemon} AND ERROR MESSAGE: {e}")

    def treatEffectiveness(self, pokemon):
        for effectiveness in pokemon["effectiveness"]:
            if effectiveness['value'] == 'Â½':
                effectiveness['value'] = "1/2";
            
            if effectiveness['value'] == 'Â¼':
                effectiveness['value'] = "1/4";

class MongoPipeline:
    collection_name = "pokemon_collection"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print("INSERTING ITENS ON MONGODB");
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item