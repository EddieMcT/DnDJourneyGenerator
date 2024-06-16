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



structuredict = { #General rule: use a[n] as a grammatical placeholder for a/an, and replace after generation is complete. Needs to be done after the main construction function
    0: ('The path goes [path_location] a[n] [description] [structure].', 'The path goes [path_location] a[n] [structure] [post_description].', 
            'The path goes [path_location] a[n] [description] [structure], long since [ruin_description].'
            ,"A[n] [description] [structure] is [location].","A[n] [structure], visibly [ruin_description], is [location]."),
    'structure' : ('[building]', '[monument]', '[shop]', '[settlement]'), #old: (specific_ruins(colours),random_ruins(),monument(),signpost(DC),shop(),village())
    'description' : ('','[basic_description]', '[ruin_description]'),
    'ruin_description': ("abandoned", "overgrown","decayed","ruined", "plundered"),
    'basic_description': ('great', "ancient", 'stone'),
    'post_description': ('etched with [writing]', 'with [writing] carved into it', 'made from [material]' ),
    'writing': ("a warning","a blessing","historical lore","a memorial","religious iconography","a holy symbol","an unholy symbol","arcane symbols","ancient graffiti", "a riddle"),
    'surroundings' : ("fresh flowers","a strange smell", "mist", 'unusual plants', 'buzzing insects'),
    'path_location': ("through","past","next to","around"),
    'location': ("up ahead","just off the path","visible nearby",
                "a short walk away from the path","a half-mile off the path"),
    'person_types': ('[intellectual]', '[religious_figure]', '[person]'),
    'intellectual': ('wizard', 'sorcerer', 'artificer', 'alchemist'),
    'religious_figure' : ('deity', 'minor deity', 'priest', 'prophet', 'religious figure'),
    'person' : ('person', 'child', 'folk hero', 'warrior') , 
    'int_location': ('study', 'library', 'tower'),
    'renown': ('famous', 'infamous', 'well-renowned', 'lesser known'),
    'faction': ('criminal club', 'guild', 'secret society', 'enemy faction', 'social club'), 
    'material': ('native rock', 'assorted stones', 'imported marble'),
    'monument': ("sealed burial mound","plundered burial mound",
                  "[common_monuments]", "[ruin_description] [common_monuments]"),
    'common_monuments': ('obelisk', 'statue of a[n] [person_types]','statue of a[n] [renown] [person_types]',"circle of standing stones","totem pole","wayshrine", "[rare_monuments]"),
    'rare_monuments': ("pyramid","group of faces, carved into a mountainside or cliff,","group of giant statues, carved out of a mountainside or cliff,","sealed catacomb", "plundered catacomb", "plundered temple","circle of standing stones"),
    'building': ('[basic_buildings]','[milit_buildings]' ,'[religious_buildings]' ,'[production_buildings]' , '[int_buildings]' ,'[meeting_buildings]','[tomb_buildings]','[signpost]' ),
    'basic_buildings' : ("inn","house", "tower","wall","staircase","pillar","hut","building","fountain","well", "archway"),
    'milit_buildings' : ("fortress","watchtower","outpost", "keep", "castle","guard station"),
    'religious_buildings' : ("temple","monastery","reliquary" ),
    'tomb_buildings' : ("tomb","crypt","necropolis","memorial stone","graveyard"),
    'production_buildings' : ("quarry","orchard","hunting stand", "mine","farm","windmill","garden", "hunter/fisherman's shack"),
    'int_buildings' : ("[int_location] of a[renown] [intellectual]","[int_location]","artificer’s factory","alchemist's lab"),
    'meeting_buildings' : ("private meeting house for a [faction]","private meeting house for a[renown] [faction]"),
    'signpost': ()
} #to do: cairn, battlefield

print(text_construct(structuredict))


