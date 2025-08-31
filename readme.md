## Solution
### The ideia
We are goint to break down the problem of treating all the data in submodules
- Extract
    - Here we extract all the data ( scrapy )
- Trasnform
    - Here we transform all the data we got from the previous step
- Load
    - Here we load all the data in the datbase doing the necessary transformations if needed


### Evolutions
Here lies the worst part of all this case scenario, we need to treat this a saperate case, first loading all the cards
of the evolutions and just then in the `transform` step we chage these data to be something we can put on the datbabase.

### Problems to not forget
I'm having some problems with some pokemons, so I'll list here to not forget about all the errors I'm recieving:

- Duplicate names to the same pokemon
- Scraping a '.' in the pokemon number
- Weight not being converted correctly

### Regex:
Regex to extract an evolution item:
- /use <a href="\/item\/[a-zA-Z]+(-?[a-zA-Z])+"/

Regex to extract an evolution level:
- /Level [0-9]{2}/



## Pokemon Attributes
- number
- url
- name
- sizeInCm
- weight
- type
- effectiveness 

Here we need to have a special treatment
- evolutions
- skills



