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



ruindict = { #General rule: use [n] as a grammatical placeholder for a/an, and replace after generation is complete. Needs to be done after the main construction function
    0: ('The path goes [path_location] a[n] [description] [building].', 'The path goes [path_location] a[n] [building] [post_description].', 
            "A[n] [description] [building] is [location]."),
    'description' : ('','[basic_description]', '[ruin_description]'),
    'ruin_description': ("abandoned", "overgrown","decayed","ancient", "ruined"),
    'basic_description': (),
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
    'monuments': ("sealed burial mound","plundered burial mound",
                  "[common_monuments]", "[ruin_description] [common_monuments]"),
    'common_monuments': ('obelisk', 'statue of a[n] [person_types]','statue of a[n] [renown] [person_types]',"circle of standing stones","totem pole","wayshrine"),
    'rare_monuments': (),
    'building': ('[basic_buildings]','[milit_buildings]' ,'[religious_buildings]' ,'[production_buildings]' , '[int_buildings]' ,'[meeting_buildings]','[tomb_buildings]' ),
    'basic_buildings' : ("inn","house", "tower","wall","staircase","pillar","hut","building","fountain","well", "archway"),
    'milit_buildings' : ("fortress","watchtower","outpost", "keep", "castle","guard station"),
    'religious_buildings' : ("temple","monastery","reliquary","battlefield", ),
    'tomb_buildings' : ("tomb","crypt","necropolis","memorial stone","graveyard"),
    'production_buildings' : ("quarry","orchard","hunting stand", "mine","farm","windmill","garden", "hunter/fisherman's shack"),
    'int_buildings' : ("[int_location] of a[renown] [intellectual]","[int_location]","artificer’s factory","alchemist's lab"),
    'meeting_buildings' : ("private meeting house for a [faction]","private meeting house for a[renown] [faction]"),
} #to do: cairn

print(text_construct(ruindict))


def monument():
    writing_options = ["a warning","a blessing","historical lore","a memorial","religious iconography","a holy symbol","an unholy symbol","arcane symbols","ancient graffiti", "a riddle"]
    surrounding_options = ["fresh flowers","a strange smell", "unnatural mist"]
    options = [f"surrounded by {random.choice(surrounding_options)}", f"etched with {random.choice(writing_options)}"]
    location_options = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
    if random.random() > 0.95:
        chosen = random.choice(("sealed pyramid", "plundered pyramid","group of faces, carved into a mountainside or cliff,","group of giant statues, carved out of a mountainside or cliff,","sealed tomb", "plundered tomb","sealed catacomb", "plundered catacomb", "plundered temple","circle of standing stones"))
    else:
        chosen = random.choice(())
    if "aeiou".find(chosen[0]) == -1:
        state_text = "A"
    else:
        state_text = "An"
    if random.random() < 0.5:
        post_text = f", {random.choice(options)}, is {random.choice(location_options)}."
    else:
        post_text = f" is {random.choice(location_options)}."
    return (f"{state_text} {chosen}{post_text}", "monument",)