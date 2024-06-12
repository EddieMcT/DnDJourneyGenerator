import random

test_dict = {
    0 : ['[a]', '[b]'],
    'a':['test 1', 'test 2[b]'],
    'b':['test 3 [a] [c]']
}
def text_replace(text, new_text, start_pos, end_pos):
    output = text[:start_pos] + new_text + text[end_pos+1:]
    return(output)

def replace_set(text, replace_dict):
    for i in replace_dict.keys():
        start_pos = text.find(i)
        while start_pos >= 0:
            text = text_replace(text, replace_dict[i], start_pos, start_pos+len(replace_dict[i])-1)
            start_pos = text.find(i)
    return(text)



def text_construct(input = test_dict, text = '[0]'):
    start_pos = text.find('[')
    end_pos = text.find(']')

    while start_pos >= 0 and end_pos >= 0:
        ind = text[start_pos+1:end_pos]
        try:
            new_text = random.choice(input[ind])
        except:
            try:
                ind = int(ind)
                new_text = random.choice(input[ind])
            except:
                new_text = '{' + ind +'}' #keys that aren't found are surrounded by {}
        text = text_replace(text, new_text, start_pos, end_pos)
        start_pos = text.find('[')
        end_pos = text.find(']')
    text = replace_set(text, {'{':'[', '}':']'})
    return(text)

print(text_construct())

ruindict = {
    0: ('The path goes [path_location] a[ruindescription] [ruin].', 
            "A[ruindescription] [ruin] is [location]."),
    'ruindescription': ("n abandoned", "n overgrown"," decayed","n ancient", " ruined", ' collapsed'),
    'path_location': ("through","past","next to","around"),
    'location': ("up ahead","just off the path","visible nearby",
                "a short walk away from the path","a half-mile off the path"),
    'intellectual': ('wizard', 'sorcerer', 'artificer', 'alchemist'),
    'int_location': ('study', 'library', 'tower'),
    'renown': (' famous', 'n infamous', ' well-renowned', ' lesser known'),
    'faction': ('criminal club', 'guild', 'secret society', 'enemy faction', 'social club'), 
    'ruin': ("inn","house", "tower","wall","staircase","pillar","hut","building","fountain","well",
                "fortress","watchtower","outpost", "keep", "castle","guard station", 
                "temple","monastery","reliquary","battlefield", 
                "tomb","crypt","necropolis","memorial stone","graveyard",
                "quarry","orchard","hunting stand", "mine","farm","windmill","garden", "hunter/fisherman's shack"
                "[int_location] of a[renown] [intellectual]","[int_location]","artificer’s factory","alchemist's lab",
                "private meeting house for a [faction]",
                "private meeting house for a[renown] [faction]"
                )
} #to do: cairn

def specific_ruins(colours):
    if len(colours) > 2:
        filtered_colours = colours[0:2]
    else:
        filtered_colours = colours
    specific_ruin_options = {"W":("inn","house",),"U":("docks","sunken ruins","fountain","well",),"B":("graveyard",),"R":("R",),"G":("hunting station","garden",),"C":("sunken ruins","seafloor debris",),"D":("D",),"V":("V",),"A":("A",),"c":("mine",),"WW":("fortress","watchtower","outpost","castle",),"UW":("customs office",),"BW":("memorial stone",),"RW":("quarry","watchtower",),"GW":("orchard","garden",),"CW":("coastal tower","lighthouse","port",),"DW":("DW",),"VW":("VW",),"AW":("AW",),"cW":("open quarry",),"WU":("reliquary","canal","fountain","well",),"UU":("alchemist's lab","artificer's study","library","sunken ruins","artificer’s factory","well",),"BU":("private meeting house for a criminal club","private meeting house for a guild","private meeting house for a secret society)","sunken ruins",),"RU":("sorcerer's study",),"GU":("canal","well",),"CU":("port",),"DU":("DU",),"VU":("VU",),"AU":("AU",),"cU":("cU",),"WB":("temple","monastery",),"UB":("smuggler's hideout","sunken ruins",),"BB":("tomb","crypt","bog wreckage/offerings","necropolis",),"RB":("cairns",),"GB":("GB",),"CB":("CB",),"DB":("DB",),"VB":("VB",),"AB":("AB",),"cB":("barrow, swarmyard",),"WR":("battlefield",),"UR":("wizard's tower",),"BR":("cairns",),"RR":("keep",),"GR":("tinder farm","game trail",),"CR":("CR",),"DR":("DR",),"VR":("VR",),"AR":("AR",),"cR":("cR",),"WG":("farm","windmill","garden",),"UG":("fisherman's hut",),"BG":("BG",),"RG":("game trail",),"GG":("forestry stand","copse",),"CG":("CG",),"DG":("DG",),"VG":("VG",),"AG":("AG",),"cG":("cG",)}
    options = ["n abandoned", "n overgrown"," decayed","n ancient"]
    chosen = random.choice(specific_ruin_options[filtered_colours])
    if chosen.find("ruin") == -1:
        options.append((" ruined"))
    if random.random()<0.5:
        location_options = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
        return (f"A{random.choice(options)} {chosen} is {random.choice(location_options)}.", chosen)
    else:
        location_options = ("through","past","next to","around")
        return (f"The path goes {random.choice(location_options)} a{random.choice(options)} {chosen}.", chosen)

