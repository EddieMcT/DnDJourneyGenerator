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


#Common component sets, to be reused
writing = ("a warning","a blessing","historical lore","a memorial","religious iconography","a holy symbol","an unholy symbol","arcane symbols","ancient graffiti", "a riddle")
ruins = ("abandoned", "overgrown","decayed","ruined", "plundered")
surroundings = ("fresh flowers","a strange smell", 'buzzing insects', 'shrubs and undergrowth')
path_loc = ("through","past","next to","around", 'alongisde')
renown = ('famous', 'infamous', 'well-renowned', 'lesser known', 'legendary')
location = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
structure_0 = ('The path runs [path_location] a[n] [description] [structure].', 'The path runs [path_location] a[n] [structure], [post_description].', 
            'The path runs [path_location] a[n] [basic_description] [structure], [post_description].',
            'The path runs [path_location] a[n] [basic_description] [structure], long since [ruin_description].',
            "A[n] [description] [structure] is [location].","A[n] [structure], visibly [ruin_description], is [location].",
            "A[n] [structure], [post_description], is [location].")

structuredict = { #General rule: use a[n] as a grammatical placeholder for a/an, and replace after generation is complete. Needs to be done after the main construction function
    0: structure_0,
    'structure' : ('[building]', '[monument]','signpost [signpost]' ), #old: (specific_ruins(colours),random_ruins(),monument(),signpost(DC),shop(),village())
    'description' : ('[basic_description]', '[ruin_description]'),
    'ruin_description': ruins,
    'basic_description': ('great', "ancient", 'stone','makeshift', 'flimsy', 'large'),
    'post_description': ('etched with [writing]', 'with [writing] carved into it',
                          'made from [material]' , 'carved from the native rock', 'set into nearby trees',
                         'surrounded by [surroundings]', 'with [surroundings] around it',
                         'long since [ruin_description]', 'visibly [ruin_description]', 'nearly [ruin_description]' , 'recently [ruin_description]'),
    'writing': writing,
    'surroundings' : surroundings,
    'path_location': path_loc,
    'location': location,
    'person_types': ('[intellectual]', '[religious_figure]', '[person]'),
    'intellectual': ('wizard', 'sorcerer', 'artificer', 'alchemist'),
    'religious_figure' : ('deity', 'minor deity', 'priest', 'prophet', 'religious figure'),
    'person' : ('person', 'child', 'folk hero', 'warrior', 'unknown figure', 'soldier') , 
    'int_location': ('study', 'library', 'tower'),
    'renown': renown,
    'faction': ('criminal club', 'guild', 'secret society', 'enemy faction', 'social club'), 
    'material': ('native rock', 'assorted stones', 'imported marble', 'mismatched stones', 'half rotted wood', 'fine wood','unusual materials'),
    'monument': ("[common_monuments]", "[ruin_description] [common_monuments]"),
    'common_monuments': ("burial mound",'obelisk', 'gravestone of a[n] [person_types]','statue of a[n] [person_types]','statue of a[n] [renown] [person_types]',"circle of standing stones","totem pole","wayshrine", "[rare_monuments]"),
    'rare_monuments': ("pyramid",
                       "group of carved faces","group of giant statues",#Check interactions
                       "scatacomb", "circle of standing stones"),
    'building': ('[basic_buildings]','[milit_buildings]' ,'[religious_buildings]' ,'[production_buildings]' , '[int_buildings]' ,'[meeting_buildings]','[tomb_buildings]'),
    'basic_buildings' : ("inn","house", "tower","wall","staircase","pillar","hut","building","fountain","well", "archway"),
    'milit_buildings' : ("fortress","watchtower","outpost", "keep", "castle","guard station"),
    'religious_buildings' : ("temple","monastery","reliquary" ),
    'tomb_buildings' : ("tomb","crypt","necropolis","memorial stone","graveyard"),
    'production_buildings' : ("quarry","orchard","hunting stand", "mine","farm","windmill","garden", "hunter/fisherman's shack"),
    'int_buildings' : ("[int_location] of a[n] [renown] [intellectual]","[int_location]","artificer’s factory","alchemist's lab"),
    'meeting_buildings' : ("private meeting house for a [faction]","private meeting house for a[renown] [faction]"),
} #to do: cairn, battlefield

magicalextension = {
    'material':('strange metals', 'living wood'),
    'signpost_common': ('historical events', 'major teleportation circles', "locations you've never heard of", 'written in an unintelligible script', 'other planes of existence', 'abstract concepts and emotions'),
    'person_types': ('party member'),
    'renown': ('long forgotten'),
    'writing': ('glowing runes', 'bizarre symbols'),
    'basic_description':('haunted', 'illusory'),
    'surroundings':('a faint glow', 'mysterious lights', 'an unnatural chill',"mist", 'unusual plants' ),
    'post_description': ('carved from the native rock', 'set into nearby trees')
    }

structureextension_shelter = {
    location : ("[structure_pos] about the structure","[structure_pos] around the structure","around the structure","in the shadow of the structure","a short walk away from the structure","near the structure"),
    structure_0 : (
        "A[n] [description] [structure] can be found [location].","A[n] [structure], visibly [ruin_description], can be found [location].",
        "A[n] [basic_description] [structure] can be found [location].","A[n] [structure], [post_description], can be found [location]."
        "A[n] [description] [structure] is [location].","A[n] [structure], recently [ruin_description], is [location].",
        "A[n] [basic_description] [structure] is [location].","A[n] [structure], [post_description], is [location].")
        }


signpost_dict = {0: structure_0,#Currently duplicated from structure_dict, to be revised
    'structure' : ("signpost with signs pointing towards [signpost_common]",  
                 "sign listing the distance to [signpost_common]","signpost with signs showing direction and distance to [signpost_common]",
                 "sign listing the walking times to [signpost_common]","post with signs showing direction and walking time to [signpost_common]",
                 ),
    'description' : ('[basic_description]', '[ruin_description]'),
    'ruin_description': ruins,
    'basic_description': ('makeshift', 'flimsy', 'large'),
    'post_description': ('etched with [writing]', 'with [writing] carved into it',
                          'made from [material]', 
                         'surrounded by [surroundings]', 'with [surroundings] around it',
                         'worn and illegible', 'with signs knocked loose in a storm',
                         'long since [ruin_description]', 'visibly [ruin_description]', 'nearly [ruin_description]'),
    'writing': writing,
    'surroundings' : surroundings,
    'path_location': path_loc,
    'location': location,
    'material': ('stone', 'half rotted wood', 'fine wood','unusual materials', 'cheap timber'),
    'signpost_common': ('nearby points of interest', 'several cities and settlements', 'multiple places', 'nearby inns', 'natural features of the terrain'),
    }


shelter_dict = {
    0: ('The path runs [path_location] a[n] [description] [structure].', 
        'The path runs [path_location] a[n] [structure], [post_description].', 
        'The path runs [path_location] a[n] [basic_description] [structure], built largely from [material].',
        'The path runs [path_location] a[n] [basic_description] [structure].',
        "A[n] [basic_description] [structure] is [location].",
        "A[n] [description] [structure] is [location].",
        "A[n] [structure], recently [ruin_description], is [location].",
        "A[n] [structure], [post_description], is [location]."), 
    'path_location': path_loc,
    'location': location,
    
    'structure': ('[shop]', '[settlement]', '[campsite]'),
    'shop':("inn","roadside stall", "[storekeep]'s store", "[storekeep]'s shop", "roadside stall of a [storekeep]"),
    'storekeep':("alchemist", "greengrocer", 'local farmer','[renown] criminal pretending to be a [storekeep]'),
    'settlement':(), 
    'campsite':(),
    'structure_pos': ('built up', 'scattered', 'loosely'), #Eg a shop (is/can be found) [structure_pos] around the structure
    'description' : ('[basic_description]','[renown]', '[ruin_description]'),
    'renown' : renown,
    'ruin_description': ("abandoned","ruined", "plundered", "half-buried", 'empty'),
    'basic_description': ('makeshift', 'flimsy', 'run-down',  'ramshackle', 'shabby'
                          'large', 'small', 
                          'busy', 'bustling', 'lively',
                          'upmarket','wealthy',
                          'quiet'),
    'material': ('native rock', 'assorted stones', 'imported marble', 'mismatched stones', 'half rotted wood', 'fine wood','unusual materials'),
    'post_description': ('built largely from [material]' , 
                         'surrounded by [surroundings]', 
                         'nearly [ruin_description]' , 'recently [ruin_description]'),

}

def village():
    options = (" abandoned"," nearly abandoned", ""," yet bustling")#village descriptions, mainly focused on population size
    location_options = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
    return (f"There is a small{random.choice(options)} village {random.choice(location_options)}.", "buildings")

class event():
    def __init__(self, default_dict = structuredict, extras = {}):
        self.default_dict = default_dict
        self.extra_dict = extras #Dict of dicts for different additional situations
    
    def extend(self, k, v):
        if k in self.temp_dict.keys():
            self.temp_dict[k].update(v)
        else:
            self.temp_dict[k] = v

    def generate(self, input = '[0]', extras = {}, extra_keys = {}):#To be used with conditional extensions, ie if the location is magical
        self.temp_dict = dict(self.default_dict)
        for k,v in extras.items(): #Freeform conditional extensions
            self.extend(k,v)
        for k, v in extra_keys.items(): #Dict of booleans indicating whether to add the standard extras of that type
            if k in self.extra_dict.keys() and v:
                for k1, v1 in self.extra_dict[k]:
                    self.extend(k1, v1)
        output = text_construct(input = self.temp_dict, text = input)
        return (output)

structure_event = event(structuredict, extras={'magical':magicalextension})
signpost_event = event(signpost_dict, extras={'magical':magicalextension})
shelter_event = event(shelter_dict, extras={'magical':magicalextension, 'structure':structureextension_shelter})

print(signpost_event.generate())

def generate_event(DC = 10):
    is_structure = False 
    structure_id = "structure"
    is_items = False
    is_magic = False
    is_magic_danger = False
    is_ambush = False
    is_hazard = False
    is_bridge = False
    is_leyline = False
    is_second = False
    event_text = ""
    while event_text == "":
        if random.random() < 0.1:
            is_leyline = True
        else:
            is_leyline = False
        if is_leyline and random.random() < float(DC/100): #predict in advance if there will be magic
            is_magic = True
        else:
            is_magic = False
        if random.random() < 0.3: #Uninhabited structures, walls, ruins, etc.
            new_text = structure_event.generate(extra_keys={'magical':is_magic})
            event_text = event_text + new_text + "\n"
            is_structure = True
        if random.random() < 0.3: #Signposts
            new_text = signpost_event.generate(extra_keys={'magical':is_magic})
            event_text = event_text + new_text + "\n"
            is_structure = True
        
        if random.random() < 0.3: #Potentially inhabited structure, camps, villages, shops
            new_text = text_construct(shelterdict)
            event_text = event_text + new_text + "\n"


        if random.random() < 0.3:
            new_text = item(DC)
            event_text = event_text + new_text + " "
        if is_leyline:
            new_text = leyline(DC,colours)
            event_text = event_text + new_text + " "
        if random.random() < 0.3:
            new_text = shelter(DC)
            event_text = event_text + new_text + " "
        if random.random() < 0.1:
            new_text = sensory_event(0)
            event_text = event_text + new_text + " "
        if random.random() < 0.3:
            new_text = hazard(DC, random.choice(colours))
            event_text = event_text + new_text + " "
        if random.random() < 0.3:
            new_text = difficulty(DC, random.choice(colours))
            event_text = event_text + new_text + " "
        if random.random() < 0.3:
            if random.random() < float(DC/100):
                is_second = True
            else:
                is_second = False
            new_text = encounter(DC)
            event_text = event_text + new_text + " "
            if is_second:
                new_text = encounter(DC)
                event_text = event_text + new_text + " "
    return event_text




