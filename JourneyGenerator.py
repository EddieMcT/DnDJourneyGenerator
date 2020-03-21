import numpy
import random
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d, Voronoi
import pandas

#import saved data
points = [] #assigned points
#allowedpos = [startpos*granularity] #unused, was planned for use with arc constraints
endgoal = [] #list of indices in points list
remdist = [] #distanceleft to endgoal
startpoint = [] #index in points list
fromdist = [] #total distance from startpoint
prevpoint = [] #index
prevdist = [] #path length
nextpoint = [] #index
nextdist = [] #distance to corresponding point in nextdist
event_dcs = []

loopstarts = []
loopends = []
looprelatives = []
loopbasedist = []
loopdist = []
loopremainders = []
looplast = []
loopdiffs = []
fixed = []
loopcolours = []


tilesx = []
tilesy = []
colours = []
event_descriptions = []

paths= [] #paths that each point is on
eventnames = [] #path id- event number

load_old_data = False
loadfile = str(input("Name of save file (.csv) to load (leave blank for new maps)\n"))
if not loadfile == "":
    load_old_data = True
    if loadfile.find(".csv") == -1:
        loadfile = loadfile + ".csv"
if load_old_data:
    try:
        df_load = pandas.read_csv(loadfile)
    except:
        print("could not find save file")
        load_old_data = False
if load_old_data:
    def cleanup(variable,dest,type_):
        for i in range(len(df_load)):
            a = df_load[variable][i]
            n = 0
            b = [""]
            for letter in (a[1:len(a)-1]):
                if letter == ",":
                    n +=1
                    b.append("")
                else:
                    b[n] = b[n] + letter
            for entry in range(0,len(b)):
                b[entry] = type_(b[entry])
            dest.append(b)

    cleanup("nextpoint",nextpoint,int)
    cleanup("prevpoint",prevpoint,int)
    cleanup("startpoint",startpoint,int)
    cleanup("endgoal",endgoal,int)
    cleanup("fromdist",fromdist,float)
    cleanup("prevdist",prevdist,float)
    cleanup("nextdist",nextdist,float)
    cleanup("points",points,float)
    cleanup("remdist",remdist,float)
    cleanup("paths",paths,int)
    cleanup("event_dcs",event_dcs,int)
    for a in df_load["fixed"]:
        fixed.append(a)
    for a in df_load["colours"]:
        colours.append(a)
    for a in df_load["event_descriptions"]:
        event_descriptions.append(a)



pathvalues = [[]]#points on each path. To be calculated from paths[]
pathpointx = [[]]
pathpointy = [[]]

if load_old_data: #rebuild pathvalues for previously existing points
    for point in range(0,len(points)):
        for path in range(0,len(paths[point])):
            while paths[point][path] >= len(pathvalues): #expand pathvalues to maximum range of paths
                pathvalues.append([])
                pathpointx.append([])
                pathpointy.append([])
                #expend all loop variables by 1? or create loop offset
            if not endgoal[point][path] == point:
                pathvalues[paths[point][path]].append(point)#dont include end
    for path in range(0,len(pathvalues)):
        firstpoint = int(pathvalues[path][0])
        for i in range(0,len(paths[firstpoint])):#move endgoal of that path to the end by checking related endgoal firstpoint in path
            if paths[firstpoint][i] == path:
                pathvalues[path].append(endgoal[firstpoint][i])




#user input
reanneal = True
restart = True
granularity = 1 #points per unit distance. Unused, may be needed in conversion to time
highpathdistance = 0
pathdistance = highpathdistance*granularity
try:
    pathdistance = int(input("How far is your journey? (nearest mile) (type 0 for no new journey)\n"))
except:
    pathdistance = int(input("Number not recognised, please try again:\n"))

intractability = 20
if pathdistance > 0:
    try:
        intractability = int(input("Intractability of new path? \nIntractability determines maximum DC of events on path. Likelihood of events per mile, as a percentage, is half the intractability\n"))
    except:
        intractability = int(input("Number not recognised, please try again:\n"))
eventchancemod = 0.005
startexists = False
endexists = False
startindex = 8
endindex = 1
startpos = [0,0]
endpos = [10,10]
mainpathcolour = "W"
if pathdistance > 0:
    mainpathcolour = input("path colour") #Update with colour id list

if load_old_data and pathdistance > 0:
    loadinput = input("Index of existing startpoint, type n for new startpoint\n")
    try:
        startindex = int(loadinput)
        startexists = True
    except:
        newx = input("x coordinate of new startpoint?\n")
        newy = input("y coordinate of new startpoint?\n")
        try:
            startpos = [float(newx),float(newy)]
        except:
            print("coordinates not recognised, beginning from origin (0,0)")
            startpos = [0,0]
    loadinput = input("Index of existing endpoint, type n for new startpoint\n")
    try:
        endindex = int(loadinput)
        endexists = True
    except:
        newx = input("x coordinate of new endpoint?\n")
        newy = input("y coordinate of new endpoint?\n")
        try:
            endpos = [float(newx),float(newy)]
        except:
            newx = float(pathdistance/2)
            print(f"coordinates not recognised, beginning from origin ({newx},{newx})")
            endpos = [newx,newx]
elif pathdistance > 0:
    newx = input("x coordinate of startpoint?\n")
    newy = input("y coordinate of startpoint?\n")
    try:
        startpos = [float(newx),float(newy)]
    except:
        print("coordinates not recognised, beginning from origin (0,0)")
        startpos = [0,0]
    newx = input("x coordinate of new endpoint?\n")
    newy = input("y coordinate of new endpoint?\n")
    try:
        endpos = [float(newx),float(newy)]
    except:
        newx = float(pathdistance/2)
        print(f"coordinates not recognised, beginning from origin ({newx},{newx})")
        endpos = [newx,newx]

if load_old_data and pathdistance > 0:
    pathvalues.append([]) #new main path
    pathpointx.append([])
    pathpointy.append([])

loopchance = 0.2
mainpathid = len(pathvalues)-1


if pathdistance > 0: #build variable lists for start and end
    if not startexists:
        startindex = len(points)
        points.append(startpos)
        endgoal.append([])
        remdist.append([])
        startpoint.append([])
        fromdist.append([])
        prevpoint.append([])
        prevdist.append([])
        nextpoint.append([])
        nextdist.append([])
        fixed.append(True)
        paths.append([])
        event_dcs.append([intractability])
        colours.append(mainpathcolour)
        event_descriptions.append([""])
    else:
        startpos = points[startindex]
    if not endexists:
        endindex = len(points)
        points.append(endpos)
        endgoal.append([])
        remdist.append([])
        startpoint.append([])
        fromdist.append([])
        prevpoint.append([])
        prevdist.append([])
        nextpoint.append([])
        nextdist.append([])
        fixed.append(True)
        paths.append([])
        event_dcs.append([intractability])
        colours.append(mainpathcolour)
        event_descriptions.append([""])
    else:
        endpos = points[endindex] #recent fix, to be checked if problems arise

    endgoal[startindex].append(endindex)
    endgoal[endindex].append(endindex)
    remdist[startindex].append(pathdistance)
    remdist[endindex].append(0)
    startpoint[startindex].append(startindex)
    startpoint[endindex].append(startindex)
    fromdist[startindex].append(0)
    fromdist[endindex].append(pathdistance)
    prevpoint[startindex].append(startindex)
    prevdist[startindex].append(0)
    nextpoint[endindex].append(endindex)
    nextdist[endindex].append(0)

    paths[startindex].append(mainpathid)
    paths[endindex].append(mainpathid)
    pathvalues[mainpathid].append(startindex)

#generate empty forces list of correct length
forces = []
for i in points:
    forces.append([])

def distance(a,b):
    sqardist = 0
    for i in range (0,min(len(a),len(b))):
        sqardist += numpy.square(a[i]-b[i])
    return numpy.sqrt(sqardist)

compression = float(pathdistance/distance(startpos,endpos))
if compression < 1 and pathdistance > 0:
    print("warning, path too short for required distance. Score will not be good")

#semi-global variables to track influences
humanoid_only = False
is_structure = False
is_items = False
is_valuable = False
is_magic = False
is_magic_danger = False
is_ambush = False
is_hazard = False
is_bridge = False
is_leyline = False
is_second = False
structure_id = "structure"
weapon = random.choice(("simple melee weapon","simple ranged weapon","martial melee weapon","martial ranged weapon"))


colour_ident = {"W":"White","U":"Blue","B":"Black","R":"Red","G":"Green","C":"Coastal","DR":"Desert","V":"Volcanic","A":"Arctic","c":"Cave/Neutral"}
secondary_options = ("W","U","B","R","G")
secondary_options_rare = ("W","U","B","R","G","WU","UB","BR","RG","WG","WB","UR","BG","WR","UG")

def eventterrain(colours):
    landscape_type = random.random()
    if landscape_type < 0.4:
        return (random.choice(landscapes[colours]),colours)
    if landscape_type < 0.5:
        new_colours = colours + random.choice(secondary_options)
        return (random.choice(landscapes[new_colours]), new_colours)
    if landscape_type < 0.6:
        new_colours = random.choice(secondary_options)
        return (f"{random.choice(influence_options[new_colours])} {random.choice(landscapes[colours])}", colours +new_colours)
    if landscape_type < 0.7:
        new_colours = random.choice(secondary_options)
        return (random.choice(landscapes[new_colours]), new_colours)#link to separate list of replacement terrains
    if landscape_type < 0.8:
        new_colours = colours + random.choice(secondary_options)
        influence_colour = random.choice(secondary_options)
        return (f"{random.choice(influence_options[influence_colour])} {random.choice(landscapes[new_colours])}", new_colours +influence_colour)
    if landscape_type < 0.9:
        new_colours = colours + random.choice(secondary_options_rare)
        influence_colour = random.choice(secondary_options)
        return (f"{random.choice(influence_options[influence_colour])} {random.choice(rare_landscapes[new_colours])}", new_colours +influence_colour)
    else:
        new_colours = colours + random.choice(secondary_options_rare)
        return (random.choice(rare_landscapes[new_colours]), new_colours)


#landscape and location descriptions, to be filled in in excel and updated (hopefully)

influence_options = {"W":("wide-open","sunlit","tranquil","sacred","windswept"),"U":("flooded","riverside"),"B":("corrupted","fungus-filled","marshy","swampy","waterlogged","dead","unholy","sunken","tainted"),"R":("stony","rocky","hilltop","boulder-filled","firelit"),"G":("overgrown","wooded","forested","tree-shaded","woodland")}

landscapes = {"W":("plains",),"U":("riverbank","river","creek",),"B":("swamp",),"R":("mountain","hill","valley","gorge","ravine","hillock","knoll","strath (broad valley)","glen (narrow valley)","highlands","karst",),"G":("forest","jungle",),"C":("shoreline","water","skerrie","isthmus",),"D":("dunes","desert",),"V":("V",),"A":("A",),"c":("c",),"WW":("grassland","prarie","wastes",),"UW":("tranquil cove","dunes","floodplains","grassland skerry","fluvial terrace","grassland strath (broad river valley)",),"BW":("shrub swamp","barrens","scrubland",),"RW":("alpine tundra","steppe","plateau","subalpine meadow","mesa","pass",),"GW":("woodland","clearing",),"CW":("beach","tranquil cove","dunes","floodplains","grassland skerry","baymouth bar","spit","isthmus",),"DW":("etchplain","wastes",),"VW":("lava field",),"AW":("tundra",),"cW":("cW",),"WU":("creek","meandering river","pond","floodplain",),"UU":("river island","confluence","hole","rapids","meander","billabong","braided river","riffle","creek",),"BU":("marsh","backwater","pond","tidal marsh","salt marsh",),"RU":("tarn","hollow","spring","gully",),"GU":("GU",),"CU":("rivermouth","shoal or sandbar","hole","barrier island (bridging lagoon)","cove","estuary","isthmus",),"DU":("oasis","panhole","arroyo or wash (desert river","currently with water)"," arroyo or wash (desert river","currently dry)","dried up river-bed",),"VU":("VU",),"AU":("AU",),"cU":("sinkhole","sea cave","cenote",),"WB":(" fen","barrens","scrubland",),"UB":("backwater","tidal marsh",),"BB":("bog","quaking or blanket bog","peat bog",),"RB":("sink",),"GB":("carr",),"CB":("mudflats","saltmarsh","tidal marsh","mangrove swamp","estuary",),"DB":("salt flats",),"VB":("geothermal swamp",),"AB":("muskeg",),"cB":("karst",),"WR":("boulderfield","stone run","mountain or hill pass","rugged prarie",),"UR":("strath (broad river valley)","glen","ravine","gully","riffle","hollow",),"BR":("raised bog (peat mound)",),"RR":("tor","mountain pass","scree slope","ridge",),"GR":("GR",),"CR":("raised beach","rocky beach","cliffside",),"DR":("badlands",),"VR":("volcanic plug",),"AR":("glacier","tunnel valley",),"cR":("abime (vertical hole to a cave network",),"WG":("savannah",),"UG":("wooded strath","wooded glen",),"BG":("pocosin or scrub bog","mangrove swamp","bayou",),"RG":("montane forest","pass","wooded glen (narrow sloping valley)","wooded strath (broad sloping valley)",),"GG":("GG",),"CG":("mangrove","wooded skerry",),"DG":("scrub",),"VG":("VG",),"AG":("taiga",),"cG":("cG",)}
rare_landscapes = {"WW":("WW",),"UW":("machair",),"BW":("fetid heath",),"RW":("canyon","grassy cove","backslope","highlands","crag",),"GW":("GW",),"CW":("CW",),"DW":("desert pavement",),"VW":("VW",),"AW":("AW",),"cW":("cW",),"WU":("flooded wastes",),"UU":("hole","ria",),"BU":("BU",),"RU":("shut in","fjord","hanging valley (tributary with waterfall)","kettle hole lakes","cascade bluffs",),"GU":("flooded grove",),"CU":("reef, atoll",),"DU":("DU",),"VU":("geyser","sulfurous springs ",),"AU":("AU",),"cU":("cU",),"WB":("fetid heath","scrubland",),"UB":("UB",),"BB":("deadmarsh","tar pit",),"RB":("sulfurous springs","badlands","tar pit",),"GB":("gnarled and fungus covered stand",),"CB":("bayou","boneyard",),"DB":("dry lake",),"VB":("sulfurous springs",),"AB":("AB",),"cB":("cB",),"WR":("inselberg","petrified field",),"UR":("waterfall","fjord","cascade bluffs","sulfurous springs ",),"BR":("sulfurous springs","badlands","tar pit",),"RR":("stone pillars","arrete","hanging valley",),"GR":("petrified forest","fire-lit thicket",),"CR":("boulder bank","volcanic island",),"DR":("butte",),"VR":("firefall",),"AR":("arrete","hanging valley (tributary glacier)",),"cR":("cR",),"WG":("WG",),"UG":("flooded grove",),"BG":("BG",),"RG":("cloud forest","cove forest",),"GG":("GG",),"CG":("flooded grove","tropical island",),"DG":("DG",),"VG":("VG",),"AG":("AG",),"cG":("cG",),"WWU":("WWU",),"UWU":("UWU",),"BWU":("BWU",),"RWU":("RWU",),"GWU":("GWU",),"CWU":("river delta",),"DWU":("flooded wastes",),"VWU":("VWU",),"AWU":("tundra",),"cWU":("cWU",),"WWB":("WWB",),"UWB":("machair",),"BWB":("BWB",),"RWB":("RWB",),"GWB":("GWB",),"CWB":("CWB",),"DWB":("DWB",),"VWB":("VWB",),"AWB":("AWB",),"cWB":("cWB",),"WWR":("causeway","butte",),"UWR":("pavement or causeway","strandflat",),"BWR":("BWR",),"RWR":("stack field","glacial outwash plain","potrero (sloped mesa)",),"GWR":("GWR",),"CWR":("CWR",),"DWR":("butte",),"VWR":("VWR",),"AWR":("AWR",),"cWR":("cWR",),"WWG":("WWG",),"UWG":("UWG",),"BWG":("BWG",),"RWG":("dell",),"GWG":("GWG",),"CWG":("CWG",),"DWG":("DWG",),"VWG":("VWG",),"AWG":("AWG",),"cWG":("cWG",),"WUB":("WUB",),"UUB":("UUB",),"BUB":("BUB",),"RUB":("RUB",),"GUB":("GUB",),"CUB":("estuary",),"DUB":("DUB",),"VUB":("VUB",),"AUB":("AUB",),"cUB":("cUB",),"WUR":("WUR",),"UUR":("hanging valley (tributary with waterfall)",),"BUR":("BUR",),"RUR":("hanging valley (tributary with waterfall)",),"GUR":("GUR",),"CUR":("cascade bluffs",),"DUR":("DUR",),"VUR":("geyser",),"AUR":("kettle hole lakes",),"cUR":("cUR",),"WUG":("canal","ditch",),"UUG":("UUG",),"BUG":("bayou",),"RUG":("RUG",),"GUG":("GUG",),"CUG":("flooded grove",),"DUG":("oasis",),"VUG":("VUG",),"AUG":("AUG",),"cUG":("cUG",),"WBR":("WBR",),"UBR":("UBR",),"BBR":("BBR",),"RBR":("RBR",),"GBR":("GBR",),"CBR":("CBR",),"DBR":("DBR",),"VBR":("VBR",),"ABR":("ABR",),"cBR":("cBR",),"WBG":("WBG",),"UBG":("mangrove swamp",),"BBG":("BBG",),"RBG":("geothermal crevice",),"GBG":("GBG",),"CBG":("CBG",),"DBG":("DBG",),"VBG":("geothermal crevice",),"ABG":("ABG",),"cBG":("cBG",),"WRG":("WRG",),"URG":("URG",),"BRG":("BRG",),"RRG":("peat bog",),"GRG":("GRG",),"CRG":("CRG",),"DRG":("DRG",),"VRG":("VRG",),"ARG":("ARG",),"cRG":("cRG",)}

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




def random_ruins():
    return ("A ruined " + random.choice(("tower","wall","staircase","pillar","hut","building")) + " is visible " + random.choice(("beside the path","visible nearby","a short walk away from the path","a half-mile off the path" )) + ".", "ruin" )

def monument():
    writing_options = ["a warning","a blessing","historical lore","a memorial","religious iconography","a holy symbol","an unholy symbol","arcane symbols","ancient graffiti", "a riddle"]
    surrounding_options = ["fresh flowers","a strange smell", "unnatural mist"]
    options = [f"surrounded by {random.choice(surrounding_options)}", f"etched with {random.choice(writing_options)}"]
    location_options = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
    if random.random() > 0.95:
        chosen = random.choice(("sealed pyramid", "plundered pyramid","group of faces, carved into a mountainside or cliff,","group of giant statues, carved out of a mountainside or cliff,","sealed tomb", "plundered tomb","sealed catacomb", "plundered catacomb", "plundered temple","circle of standing stones"))
    else:
        chosen = random.choice(("sealed burial mound","plundered burial mound","intact obelisk","ruined obelisk","toppled obelisk","intact statue of a person","intact statue of a deity","ruined statue of a deity","toppled statue of a deity","ruined statue of a person","toppled statue of a person","great stone wall","great stone wall in ruins","great stone arch","fountain","ruined circle of standing stones","toppled circle of standing stones","totem pole","wayshrine"))
    if "aeiou".find(chosen[0]) == -1:
        state_text = "A"
    else:
        state_text = "An"
    if random.random() < 0.5:
        post_text = f", {random.choice(options)}, is {random.choice(location_options)}."
    else:
        post_text = f" is {random.choice(location_options)}."
    return (f"{state_text} {chosen}{post_text}", "monument",)


def shop():
    options = ("n abandoned"," nearly abandoned", ""," busy","n expensive"," lively"," cheap", " shabby","","") #inn or shop descriptions
    location = random.choice(("inn","roadside stall"))
    return (f"A{random.choice(options)} {location} is up ahead.", location)

def village():
    options = (" abandoned"," nearly abandoned", ""," yet bustling")#village descriptions, mainly focused on population size
    location_options = ("up ahead","just off the path","visible nearby","a short walk away from the path","a half-mile off the path")
    return (f"There is a small{random.choice(options)} village {random.choice(location_options)}.", "buildings")

def signpost(DC):
    direction = random.choice(("clockwise","anticlockwise","180 degrees"))
    change = random.choice((f"rotated {direction}","switched around at random","knocked onto the ground"))
    options = ["with signs pointing towards multiple points of interest","listing the distance to multiple places","with signs showing direction and distance to multiple places","listing the walking times to multiple places","with signs showing direction and walking time to multiple places"]
    if random.random() < float(DC/100):
        options.extend((f"with signs pointing towards multiple points of interest {change}","but the writing is worn and illegible",f"with signs showing direction and distance to multiple places {change}","but it has been destroyed",f"with signs showing direction and walking time to multiple places {change}"))
        global is_magic
        if (is_magic and random.random() < 0.2) or random.random() < 0.01:
            options.extend((f"with signs pointing towards locations you've never heard of","but the writing is in an uninteligible script",f"with signs showing direction and distance to historical events","but it describes locations on another world","with signs pointing towards particular emotions and concepts"))
    return (f"There is a signpost here, {random.choice(options)}","signpost")
            

def structure(DC,colours):
    options = (specific_ruins(colours),random_ruins(),monument(),signpost(DC),shop(),village())
    chosen = (len(options) -1)
    global is_structure, structure_id
    is_structure = True
    while chosen >=1 and random.random() < (DC/50): #lower DC means more civilised. Problem 
        chosen += -1
    if chosen > len(options)-3:
        global humanoid_only
        humanoid_only = True
    structure_id = str(options[chosen][1])
    return options[chosen][0]

def item(DC):
    global is_items, weapon
    is_items = True
    weight = random.choice(("light","medium","heavy"))
    options = (("A pile of a scraps & supplies","A purse containing a few coins", f"A broken {weapon}"),("A small stash of trade goods","A discarded trinket","Enough food & supplies for a week"),(f"A {weapon}", "A shield","A piece of equipment","An explorers pack","A full coin purse"),("A common item","A cursed common item","A defective common item"),("A cursed item","A magical item", f"A suit of {weight} armour"),("A small hoard",),("A large hoard",)) #items organised in tiers of equivalent rarity
    location_options = ("lying discarded just off the path", "hidden next to the path", "in a locked container", "in a hidden stash","hidden in a lockbox") #locations arranged approximately by difficulty to spot
    rarity = 0
    location = 0
    while rarity < (len(options)-1) and random.random() < (DC/50): # 2% chance to increase rarity, repeated until end of rarity tier list or until not increased
        rarity += 1
    while location < (len(location_options)-1) and random.random() < float(rarity/len(options)): #more likely hidden for more valuable items
        location += 1
    if is_structure and random.random() < 0.95:
        location_text = f"in/around the {structure_id}"
    else:
        location_text = location_options[location]
    return f"{random.choice(options[rarity])} is {location_text}."

def leyline(DC,colours):
    global is_structure, structure_id
    school = random.choice(("abjuration","conjuration","divination","enchantment","evocation","illusion","necromancy","transmutation"))
    options = ("positive","unusual","protective","obstructive","misleading","confusing","negligible", "potent","bizarre","extreme","negative","disastrous","harmful","damaging")
    if is_structure and random.random() < 0.5:
        location_options = (f"the {structure_id}",)
    else:
        location_options = ("the area","parts of the local terrain","local weather", "any creatures who pass through", "any creatures who rest here","nearby plants","wildlife")
    colour_text = ""
    symbol_options = ("holy", "unholy","arcane","mystical","unnatural", "magical")
    symbol_types = ("runes", "symbols","markings")
    magic_type = random.choice(("magical force", "planar influence", "leyline", "magical power"))
    transformation_options = ("petrified","vitrified","transformed","transmuted","schorched","frozen", "disguised")
    global is_magic
    if len(colours) > 0 and random.random() < 0.5:
        global colour_ident
        for i in range(0,len(colours)):
            new_text = colour_ident[colours[i]]
            if colour_text.find(new_text) == -1:
                if i < (len(colours)-1):
                    colour_text = colour_text + new_text + "-"
                else:
                    colour_text = colour_text + new_text
        colour_text = colour_text + " aligned "
    if random.random() < 0.5:
    	alignment_text = random.choice(("Lawful","Neutral","Chaotic")) + " " + random.choice(("Good","Neutral","Evil"))
    	if alignment_text == "Neutral Neutral":
    		alignment_text = "True Neutral"
    else:
    	alignment_text = ""
    if is_magic:
        first_effect = random.randrange(0,len(options))
        second_effect = random.randrange(0,len(options))
        while second_effect == first_effect:
            second_effect = random.randrange(0,len(options))
        second_type = random.randrange(0,3)
        second_options = ("",f" {school}-based",f" and {options[second_effect]}",f" {alignment_text}")
        if first_effect > 10 or (second_effect > 10 and second_type == 2):
            global is_magic_danger
            is_magic_danger = True
        effect_text = f"There is a {colour_text}{options[first_effect]}{second_options[second_type]} {magic_type} here affecting {random.choice(location_options)}"
    else:
        effect_text = ""
    if random.random() < (DC/50):
        if not is_magic:
            effect_text = "There is evidence of magic here"
            is_magic_danger = True
        if is_structure:
            appearance_text = random.choice((f": {random.choice(symbol_options)} {random.choice(symbol_types)} are carved on the {structure_id}",f": {random.choice(symbol_options)} {random.choice(symbol_types)} are carved around the {structure_id}",": magical damage marrs the area",", the area is nearly destroyed by magic",f": the terrain is {random.choice(transformation_options)}")) + "."
        else:
            appearance_text = random.choice((f": {random.choice(symbol_options)} {random.choice(symbol_types)} are carved in a nearby tree",f": {random.choice(symbol_options)} {random.choice(symbol_types)} are carved in a nearby stone",f": {random.choice(symbol_options)} {random.choice(symbol_types)} are carved in the ground",": magical damage marrs the area",": the area is nearly destroyed by magic",": a fallen star lies in a crater",": the terrain is {random.choice(transformation_options)}",", there is a faerie ring",f": {random.choice(symbol_options)} growth patterns are visible", ", burned magical reagents litter the area",f", {random.choice(symbol_options)} {random.choice(symbol_types)} are drawn in blood")) + "."
    else:
        if is_magic:
            appearance_text = "."
        else:
            appearance_text = ""
    return (effect_text + appearance_text) 


def shelter(DC):
    sheltext = ""
    global is_structure, structure_id
    if is_structure and random.random() < 0.8:
        sheltext = f"The {structure_id}"
    else:
        sheltext = random.choice(("There is a sheltered area here, it", "This place"))
    if random.random() < (DC/100):
        sheldesc = "would be a good ambush spot."
        global is_ambush
        is_ambush = True
    elif random.random() < 0.5:
        sheldesc ="looks like a safe spot to rest."
    elif random.random() < 0.3:
        sheldesc = f"provides a clear view of the surroundings. {sensory_event(random.randrange(21,81)/100)}"
    else:
        sheldesc = "provides a clear view of the surroundings."
    return f"{sheltext} {sheldesc}"


def specific_hazard(DC,colour):#dangerous events, usually not recurring
    location_options = {"W":("hunting trap", "sinkhole"),"U":("flash flood",),"B":("cloud of brightly coloured gas","cloud of invisible poisonous gas"),"R":("rockfall",),"G":("falling tree",),"C":("patch of quicksand",),"D":("patch of quicksand",),"V":("lavaburst","cloud of brightly coloured gas","cloud of invisible poisonous gas"),"A":("avalanche",),"c":("sinkhole","rockfall")}
    options = ("n unexpected", " sudden", "n imminent", "n unseen", "n unforeseen")
    return f"A{random.choice(options)} {random.choice(location_options[colour])} threatens to harm adventurers on the path ahead."

def obstruction(DC,colour):
    options = ("small ","","large ","huge ")
    size = random.choice(options)
    location_options = {"W":("object on path (natural or artificial)","sinkhole","overturned cart"),"U":("washout","flash flood","destroyed bridge","river"),"B":("patch of waterlogged ground",),"R":("ravine","scree slope","rockslide","rockfall","boulder"),"G":("fallen tree","tangle of vines"),"C":("dune","rivermouth"),"D":("dune",),"V":("lavaflow",),"A":("crevasse",),"c":("cavein",)}#dictionary of possible obstructions for each terrain
    choice = random.choice(location_options[colour])
    global is_magic
    if is_magic and random.random() < 0.05:
        choice = random.choice(("magical obstruction","magical defense","magical barrier"))
    solution_options = {"river" : ("bridge","stone bridge","rope bridge","treetrunk, laying across the river,","wooden bridge"), 
        "ravine" : ("bridge","stone bridge","rope bridge","fallen tree, bridging the gap,","wooden bridge", "single rope, secured to large boulders,", "single rope, secured at either end to tree stumps,"),
        "crevasse": ("bridge","stone bridge","rope bridge","fallen tree, bridging the gap,","wooden bridge", "single rope, secured to pitons at either end,"),
        "lavaflow": ("bridge","stone bridge"),
        "magical obstruction": ("secret passageway", "puzzle door","riddle or passphrase"),
        "magical defense": ("secret passageway", "puzzle door","riddle or passphrase"),
        "magical barrier": ("secret passageway", "puzzle door","riddle or passphrase")
        }#dictionary linking obstructions to solutions, if they have them
    if random.random() > float(DC/100):
        global is_bridge
        solution = ""
        try:
            solution = random.choice(solution_options[choice])
            if random.random > (DC/100):
                state_options = (" "," "," slightly damaged "," visibly damaged ", "n unstable ","n improvised ")
                is_bridge = True
                return f"A {size}{choice} blocks the path. A{random.choice(state_options)}{solution} offers a path across."
            else:
                state_options = (" destroyed","n unstable","n collapsing")
                is_bridge = False
                return f"A {size}{choice} blocks the path. A{random.choice(state_options)}{solution} is visible nearby."
        except:
            is_bridge = False
    return f"A {size}{choice} blocks the path."
    

def hazard(DC, colour):
    if random.random() < DC/100:
        global is_hazard
        is_hazard = True
        return random.choice(("The path here is unstable, and could collapse.",specific_hazard(DC,colour)))
    else:
        return random.choice((obstruction(DC,colour),"The path here is slippery, and adventurers may fall."))

def slope(DC):
    direction = random.choice(("climb","descend"))
    if random.random() < (DC/100):
        global is_hazard
        is_hazard = True
        options = ("small","","large","huge")
        location_options = ("cliff","scarp","bluff","drop","series of terraces") #climbs that include risk of falling. Try to keep landscape-agnostic where possible
    else:
        options = ("slight","moderate","","steep")
        location_options = ("slope",) #climbs that don't include risk of falling. Try to keep landscape-agnostic where possible
    choice = 0 #set based on dc thresholds
    return f"The path {direction}s a {options[choice]} {random.choice(location_options)}."

def damaging(DC,colour):#damaging passive features of terrain
    global is_hazard
    is_hazard = True
    plant = random.choice(("trees","shrubs","vines","leaves","undergrowth","flowers","treebark","fruit","berries"))
    options = ("dense thorns","hunting traps and snares","stinging nettles",f"poisonous {plant}") #general list of possible passive damaging elements
    location_options = {"W":("traps and snares","stinging nettles"),"U":("poisonous algae", "jagged stones", f"poisonous {plant}"),"B":(f"poisonous {plant}","poisonous gases"),"R":("jagged stones", "falling stones"),"G":("dense thorns","hunting traps","stinging nettles",f"poisonous {plant}"),"C":("poisonous algae", "jagged stones","sharp shells"),"D":(),"V":("poisonous gases","thick smoke"),"A":(),"c":("falling rocks")}
    if random.random() < 0.9: #weight towards expected in a region
        return f"The {random.choice(location_options[colour])} in this area may harm travellers."
    else:
        return f"The {random.choice(options)} in this area may harm travellers."

def slow(DC, colour):#passive features of a terrain that make it difficult, but not harmful
    options = {"W":("thick mud","gnarled roots","overgrown path"),"U":("loose sand", "thick mud"),"B":("thick mud",),"R":("loose gravel",), "G":("dense underbrush","thick mud","gnarled roots", "overgrown path"),"C":("thick mud", "loose sand"),"V":("loose gravel","loose sand"),"A":("powdery snow",),"c":("loose gravel",)}
    return f"The {random.choice(options[colour])} makes progress difficult."

def difficulty(DC, colour):
    if random.random() < 0.5:
        return slope(DC)
    elif random.random() < (DC/100):
        return damaging(DC, colour)
    else:
        return slow(DC, colour)

def emissary():
    options = ("a nearby settlement","a distant city","a powerful guild","a local nobleman","local royalty","foreign royalty","a supernatural power")
    choice = [min(random.randrange(0,len(options)),random.randrange(0,len(options))),min(random.randrange(0,len(options)),random.randrange(0,len(options)))]
    return f"emissary from {options[choice[0]]} travelling to {options[choice[1]]}"

def caravan():
    if random.random() > 0.5:
        caravanstring = random.choice(("family","noble", "merchant", random.choice(("performing troupe", "travelling circus", "mystic"))))
        return f"a caravan carrying a {caravanstring}"
    else:
        numcaravans = random.randrange(1,5) + random.randrange(1,5)
        caravanstring = f"convoy of {numcaravans} caravans, carrying"
        for i in range (0, numcaravans+1):
            caravanstring += " a " + random.choice(("family","noble", "merchant", random.choice(("performing troupe", "travelling circus", "mystic")))) +","
    return caravanstring

def hostile_humanoids():
    global is_magic, is_magic_danger
    school = random.choice(("abjuration","conjuration","divination","enchantment","evocation","illusion","necromancy","transmutation"))
    size = random.randrange(1,11) + random.randrange(1,11) 
    options = [f"group of {size} bandits",f"group of {size} corrupt guards",f"bandit scout posing as a {nonhostile_humanoids(True)}","con man", "band of monstrous humanoids"]#needs expanding
    if (is_magic or is_magic_danger and random.random() < 0.2) or random.random() < 0.01: #unlikely or magical options for (potentially) hostile humanoids
        options.extend(("sorcerer", f"wizard ({school})","lycanthrope", "pack of lycanthropes", "doppelganger", "shapechanger", "deranged mage", "adventurer", "monster hunter"))
    return random.choice(options)

def nonhostile_humanoids(disguise):
    global is_magic, is_magic_danger
    school = random.choice(("abjuration","conjuration","divination","enchantment","evocation","illusion","necromancy","transmutation"))
    if disguise:
        return random.choice(("courier","lost child","elderly traveller",emissary(),"noble","farmer","fisher","guard","hunter","merchant","soldier","missionary","passerby","ranger","commoner","storyteller","travelling performer","escaped convict","commoner","beggar","noble","commoner","peasant"))#nonhostile humanoids that something might pretend to be (no groups)
    groupsize = random.randrange(1,9) + random.randrange(1,9) 
    options = ["courier",f"group of {groupsize} travellers","lost child","elderly traveller",emissary(),"noble","farmer with livestock","farmer, with livestock running everywhere,","fisher","guard","guard, demanding tolls,",f"group of {groupsize} guards",f"group of {groupsize} guards, demanding tolls,","hunter","merchant","soldier",f"group of {groupsize} soldiers","missionary",f"group of {groupsize} missionaries","passerby","ranger","commoner","storyteller","survivor of attack",f"group of {groupsize} travelling performers",caravan,"travelling performer","escaped convict","hunting party","commoner","beggar","noble disguised as a commoner","noble disguised as a beggar","commoner","peasant","young family"]
    if (is_magic or is_magic_danger and random.random() < 0.2) or random.random() < 0.01:
        options.extend(("mage","mystic", f"wizard ({school})","fortune teller", "priest","seer","adventurer","druid"))
    if random.random() < 0.05: #rare nonmagical options
        options.extend(("famous knight", "knight and squire", "squadron of soldiers", "adventurer", "famous noble or royalty"))
    return random.choice(options)

def activity(civ):
    global is_bridge, is_hazard, is_items, is_magic, is_magic_danger, is_structure, is_second, structure_id
    if random.random() < civ:
        options = ["walking along the path", "camping just off the path","playing a trick on passersby","greeting the party happily","camping nearby","making camp nearby","breaking camp nearby", "about to pass the party", "walking slowly ahead of the party","talking loudly about plans", "walking in the opposite direction of the party","studying","painting","practicing a hobby","trying to talk to the party","trying to barter with the party","offering life advice to the party","offering practical advice to the party","asking for advice","asking for help","asking for assistance","asking questions of passersby","offering local knowledge or gossip","in need of help","running towards the party from up ahead","running towards the party from behind","muttering to themselves", "inviting passersby to a game (riddles, skill, or chance)","that has mistaken the party for someone else","that is waiting impatiently","stuck, with a broken wheel on their cart","travelling swiftly on horseback","travelling in a cart"]#list of civilised-only activities
        if is_bridge:
            options.extend(("claiming ownership of the nearby bridge",))
        if is_hazard:
            options.extend(("looking for a way past the nearby hazard","offering to guide the party past the hazard"))
        if is_items:
            options.extend(("searching for the nearby items", "transporting items"))
        if is_magic or is_magic_danger:
            options.extend(("cautiously invistigating the nearby magic","claiming to understand the nearby magic"))
        if is_second:
            options.extend(("trying to get the attention of the other creatures",))
    else:
        options = ["walking across the path", "nesting nearby","walking alongside the path","sneaking alongside the path","sneaking towards the path","tracking someone/something","eyeing up the party's posessions"]#list of uncivilised-only activities
        if is_ambush:
            options.extend(("lying in wait",))
        if is_hazard:
            options.extend(("waiting for passersby to be injured",))
        if is_second:
            options.extend(("running away from the other creatures", "sneaking towards the other creatures",))
    options.extend(("stopped on the path","stopped just off the path","hunting","faking an injury","eating by the side of the path","watching the party intently","glaring at the party", "watching the party curiously","sitting and watching the party walk past", "resting"))#list of activities available to all encounters
    if is_structure:
        options.extend((f"moving towards the {structure_id}",f"moving away from the {structure_id}",f"examining the {structure_id}"))
    if is_hazard:
        options.extend(("trying to make their way past the nearby hazard", "about to fall victim to the nearby hazard","struggling with the nearby hazard"))
    if is_bridge:
        options.extend(("making their way across the nearby hazard",))
    if is_ambush:
        options.extend(("hiding",))
    if is_second:
        options.extend(("approaching the other creatures",))
    if random.random() < (0.1):
        return f"{random.choice(options)} and {random.choice(options)}"
    else:
        return random.choice(options)
    

def injury_options():
    global weapon, is_hazard, is_magic_danger
    options = [f"a {weapon}", "natural causes or illness", "a wild animal", "a monster"]
    if is_hazard:
        options.extend(("a nearby hazard", "the nearby hazard"))
    if is_magic_danger:
        options.extend((random.choice(("magic", random.choice(("a fey", "a fiend", "a celestial", "a dragon", "a giant", "a magical plant", "a construct","an undead", "an elemental","an ooze","an abberation")), "magic", "dangerous magic","malevolent magic", "badly controlled magic")),random.choice(("magic", random.choice(("a fey", "a fiend", "a celestial", "a dragon", "a giant", "a magical plant", "a construct","an undead", "an elemental","an ooze","an abberation")), "magic", "dangerous magic","malevolent magic", "badly controlled magic"))))
    return random.choice(options)



def encounter(DC):
    global is_structure, structure_id
    enctype = random.random()
    encstr = ""
    if random.random() > (DC/100):
        hostile = True
    else:
        hostile = True
    if enctype < 0.49 or (humanoid_only and random.random() < 0.95):
        if hostile:
            encstr = hostile_humanoids()
            civ = 0.99
        else:
            encstr = nonhostile_humanoids(False)
            civ = 0.7
    elif enctype < 0.98:
        if hostile:
            encstr = "monster"
            civ = 0.1
        else:
            animal_size = random.choice(("tiny","small","","large"))
            rare_size = random.choice((animal_size,"huge","gargantuan",animal_size))
            encstr = random.choice((f"{animal_size} animal", "young animal",f"{animal_size} old animal","huge game animal",f"{rare_size} rare animal", "animal cub/pup", f"herd of {animal_size} animals",f"flock of {animal_size} animals", f"swarm of bugs", "swarm of animals"))
            civ = 0.01
    else:
        options = ("fey", "fiend", "celestial", "dragon", "giant", "magical plant", "construct","undead", "elemental","ooze","abberation")
        encstr = random.choice(options)
        civ_dict = {"fey":0.7, "fiend":0.4, "celestial":0.5, "dragon":0.3, "construct":0.2,"undead":0.2, "elemental":0.15, "giant":0.15,"ooze":0.01,"abberation":0.1, "magical plant":0.0} #likelihood to encounter such a creature type doing something that demonstrates intelligence, vs something that appears to be wild
        civ = civ_dict[encstr]
        if encstr == "undead" and random.random() < 0.5:
            encstr = random.choice((f"undead {nonhostile_humanoids(True)}", f"undead {hostile_humanoids()}","undead animal"))
    if random.random() < float(DC/50):
        if random.random() < 0.5:
            state_text = random.choice(("an injured", "a wounded","a slightly wounded", "a gravely wounded", "a badly injured"))
        else:
            state_text = random.choice(("a deceased","a recently deceased","a dying","a freshly killed", "a partly decomposed, deceased","a partially eaten", "a severely decayed dead", "a skeletonised"))
        post_text = f". Their injuries were caused by {injury_options()}."
    elif random.random() < 0.2:
        if "aeiou".find(encstr[0]) == -1:
            state_text = "a"
        else:
            state_text = "an"
        location_options = [f"There is {state_text} {encstr} visible in the distance.",f"There is {state_text} {encstr} visible nearby.",f"There are signs of {state_text} {encstr}.",f"There are signs that {state_text} {encstr} passed through here recently."]
        if is_structure:
            location_options.extend((f"There is {state_text} {encstr} visible near the {structure_id}",f"There are tracks from {state_text} {encstr} around the {structure_id}",f"There is {state_text} {encstr} visible near the {structure_id}"))
        post_text = ""
    else:
        if "aeiou".find(encstr[0]) == -1:
            state_text = "a"
        else:
            state_text = "an"
        if random.random() < 0.9:
            post_text = f", {activity(civ)}."
        else:
            post_text = "."
    return f"There is {state_text} {encstr}{post_text}"

def sensory_event(determined):
    options = ["strange","unexpected"]
    adverbs = ["notably", "noticeably", "peculiarly", "quite"]
    if determined == 0:
        eventtype = random.random()
    else:
        eventtype = determined
    global is_magic, is_magic_danger
    if is_magic or is_magic_danger or random.random() < 0.05:
        options.extend(("familiar","unfamiliar", "unsettling", "calming", "terrifying"))
        adverbs.extend(("unnaturally", "imperceptibly", "overwhelmingly"))
    if eventtype < 0.2:
        options.extend(("acrid", "pungent", "strange","pleasant", "floral"))
        if random.random() < 0.5:
            return f"The air here is {random.choice(adverbs)} {random.choice(options)}."
        else:
            return f"The air here smells {random.choice(options)}."
    if eventtype < 0.4:
        options.extend(("bright","dim", "red", "orange","yellow","blue"))
        direction = random.choice(("North","South","East","West"))
        location_options = ("on the path", "off the path", f"to the {direction}")
        if random.random() < 0.2:
            return f"There are {random.choice(adverbs)} {random.choice(options)} lights visible {random.choice(location_options)}."
        else:
            return f"There are {random.choice(options)} lights visible {random.choice(location_options)}."
    if eventtype < 0.6:
        return "A flock of birds is visible in the distance."
    if eventtype < 0.8:
        return f"A {random.choice(options)} sound can be heard."
    else:
        return "You hear a noise."
        
        
    


def random_event(DC, colours):
    global humanoid_only, is_leyline, is_structure,is_second, is_items, is_magic, is_magic_danger, is_ambush, is_hazard, is_bridge, weapon, structure_id
    humanoid_only = False
    is_structure = False
    is_items = False
    is_magic = False
    is_magic_danger = False
    is_ambush = False
    is_hazard = False
    is_bridge = False
    is_leyline = False
    is_second = False
    structure_id = "structure"
    weapon = random.choice(("simple melee weapon","simple ranged weapon","martial melee weapon","martial ranged weapon"))
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
        if random.random() < 0.3:
            new_text = structure(DC,colours)
            event_text = event_text + new_text + " "
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

#generate events in given path
def eventgen(start,end,dist,diff,currentpathid,pathcolour):
    previous = [int(start)]
    currentdist = 1
    global points, mainpathid, pathpointx,pathpointy,pathvalues,loopdiffs,eventgen, endgoal, remdist, startpoint, fromdist, prevpoint, prevdist, nextpoint,nextdist,loopstarts,loopends,looprelatives,loopbasedist,loopchance,loopremainders,looplast
    alreadyloops = len(loopstarts)
    loopsmade = 0
    for i in range (1,int(dist)):
        if random.random() < diff*eventchancemod: #new point is created, lists expanded to accomadate it (same index pos for all details)
            points.append([])
            endgoal.append([end])
            remdist.append([dist-i])
            startpoint.append([start])
            fromdist.append([i])
            prevpoint.append(previous)
            prevdist.append([currentdist])
            nextpoint[previous[0]].append(len(points)-1)
            nextpoint.append([])
            nextdist.append([])
            nextdist[previous[0]].append(currentdist)
            previous = [len(points)-1]
            paths.append([currentpathid])
            previousvalues = pathvalues[currentpathid]
            previousvalues.append(int(previous[0]))
            pathvalues[currentpathid] = previousvalues
            fixed.append(False)
            forces.append([])
            local_dc = min(random.randrange(5,diff),random.randrange(5,diff))
            local_terrain = eventterrain(pathcolour)
            local_desc = random_event(local_dc, local_terrain[1])
            event_dcs.append([local_dc])
            colours.append(local_terrain[1])
            event_descriptions.append(local_terrain[0] + ": " + local_desc)
            if random.random() < loopchance: #begin a new sideloop
                loopstarts.append(previous)
                print(previous) #debug
                print(loopstarts) #debug
                loopsmade +=1
                length = random.choice([1,2,2,2,3,3,4,4,5,6,7])
                loopends.append([previous[0]+length])
                loopbasedist.append(0)
                loopdist.append(0)
                loopremainders.append([])
                looplast.append([])
                pathvalues.append([])
                pathpointx.append([])
                pathpointy.append([])
                loopcolours.append(random.choice(local_terrain[1]))
                loopdiffs.append(random.randrange(diff-5,min(diff+5,30)))
                looprelatives.append(int(max(random.randrange(1,11,1),random.randrange(1,11,1))*5*(random.randrange(1,9,1))))
            currentdist = 0
        currentdist += 1
    endpoint = previous[0] # most recent point made on this path. Still set to startpoint if no points made
    #trim loops and make loop basedists
    if loopsmade != 0:
        for i in range (alreadyloops, alreadyloops+loopsmade):#i = loop index of current run only (starting at 0 for first side loop)
            if loopends[i][0] >= len(points):
                loopends[i] = [end] #trim to current endgoal if it would go further than ultimate endpoint, can still adjust reentry point
                for leg in prevdist[loopstarts[i][0]+1:]: #add lengths together for pathtotal that's being avoided. limit to end of shortcut?
                    loopbasedist[i] += float(leg[0])
                loopbasedist[i] += float(currentdist)
                #print("currentdisthereis",currentdist)
            else:
                for leg in prevdist[loopstarts[i][0]+1: loopends[i][0]+1]:
                    loopbasedist[i] += float(leg[0])
            loopdist[i] = max(numpy.round_(loopbasedist[i]*looprelatives[i]/100),1) #actual distance a path or detour takes
            pathvalues[i+1 + mainpathid].append(int(loopstarts[i][0])) # add starting position to pathvalue track *before* adding events
            paths[loopstarts[i][0]].append(i+1+mainpathid)
            paths[loopends[i][0]].append(i+1+mainpathid)
            endgoal[loopstarts[i][0]].append(loopends[i][0]) #additional endgoal,remdist for start of loop
            remdist[loopstarts[i][0]].append(loopdist[i])
            startpoint[loopends[i][0]].append(loopstarts[i][0]) # additional startpoint, fromdist, for point where a loop rejoins
            fromdist[loopends[i][0]].append(loopdist[i])
            endgoal[loopends[i][0]].append(loopends[i][0]) #additional endgoal,remdist for end of loop
            remdist[loopends[i][0]].append(0)
            startpoint[loopstarts[i][0]].append(loopstarts[i][0]) # additional startpoint, fromdist, for start of loop
            fromdist[loopstarts[i][0]].append(0)
        #make loop events (recursively)
        for i in range (alreadyloops, alreadyloops+loopsmade):
            print("loopstart before making",loopstarts, i)
            endpointloop = eventgen(int(loopstarts[i][0]),int(loopends[i][0]),int(loopdist[i]),int(loopdiffs[i]),int(i+1 + mainpathid),loopcolours[i])
            loopremainders[i] = endpointloop[0]
            looplast[i] = endpointloop[1]
            nextpoint[looplast[i]].append(loopends[i][0]) #nextpoint of final step in a loop
            nextdist[looplast[i]].append(loopremainders[i]) #nextdist of final step in loop
            prevpoint[loopends[i][0]].append(int(looplast[i])) #additional prevpoint, prevdist, for point where a loop rejoins #PROBLEM
            prevdist[loopends[i][0]].append(loopremainders[i])
            pathvalues[i+1].append(int(loopends[i][0])) # add end position to pathvalue track *after* adding events
    return([currentdist, endpoint])

#generate main path and add remaining distance to end
if pathdistance > 0:
    mainpathleft = (eventgen(startindex,endindex,pathdistance,intractability,mainpathid,mainpathcolour))
    prevdist[endindex].append(mainpathleft[0])
    prevpoint[endindex].append(mainpathleft[1])
    nextdist[mainpathleft[1]].append(mainpathleft[0])
    nextpoint[mainpathleft[1]].append(endindex)
    pathvalues[mainpathid].append(endindex)


#temp annealing model begins here
originaltemp = 1
temperature = 5
cooling = True #model will reduce temperature proportionally to score... might cause it to 'boil' though
momentum = 0.1 #fraction of previous force to remain when recalculating forces in order to smooth movement. Ranges from 0 to 1
width = 0.1 #size of the area over which the gradient is calculated

#default weights and timescale. Defaults are 1. Lower weights mean less importance of a factor, higher weights mean a factor causes greater penalties but can cause it to become unstable without smaller timescales
goalweight = 0.1 #constraint to a circle around goal and startpoints of a path. minor penalty for being too far inside
repulsweight = 1#/len(points)  #weak repulsion between all points
distweight = 2 #constraint to path distance between directly connected points (nextpoint and prevpoint)
timescale = 0.1 #relative 'time' between calculations. Smaller values mean more frequent recalculation to prevent bouncing over ideal.
angleweight = 0.5
timescale_orig = timescale

def equal_starting_distribution():
    for i in range(0,len(points)): #assign starting positions based on expected distribution for a straight line
        if not fixed[i] and len(points[i]) < 1:
            journeydone = float(fromdist[i][0]/(remdist[i][0] + fromdist[i][0]))
            origin = [0,0]
            origin[0] = int(points[startpoint[i][0]][0])
            origin[1] = int(points[startpoint[i][0]][1])
            #print(journeydone)
            #print(origin)
            destination = points[endgoal[i][0]]
            #print(destination)
            origin[0] += (destination[0]*journeydone) + random.normalvariate(0,temperature)
            origin[1] += (destination[0]*journeydone) + random.normalvariate(0,temperature)
            #print(origin)
            points[i] = origin

done = not restart
startattempt = 0
startposattemptmax = 10*(len(points) ** 3)
startposattempt = 0

def starting_distribution(ident,bearing):
    #print(ident)
    global startposattemptmax, startposattempt
    if ident >= len(points): #all points already done
        return(True)
    if fixed[ident]:
        done = starting_distribution(ident+1,bearing)
    else: #assign starting positions, radial version
        origin = [0,0]
        origin[0] = float(points[startpoint[ident][0]][0])
        origin[1] = float(points[startpoint[ident][0]][1])
        destination = [0,0]
        destination[0] = float(points[endgoal[ident][0]][0])
        destination[1] = float(points[endgoal[ident][0]][1])
        previouspoint = [0,0]
        previouspoint[0] = float(points[prevpoint[ident][0]][0])
        previouspoint[1] = float(points[prevpoint[ident][0]][1])
        legdist = float(prevdist[ident][0])
        i = 0
        done = False
        while not done and i < 10 and startposattempt < startposattemptmax:
            i += 1
            startposattempt += 1
            angle = random.normalvariate(bearing,0.05*i)
            xdiff = float(previouspoint[0] + (numpy.sin(angle) * legdist))
            ydiff =float(previouspoint[1] + (numpy.cos(angle) * legdist))
            if distance([xdiff,ydiff],destination) < remdist[ident][0] and distance([xdiff,ydiff],origin) < fromdist[ident][0]:
                points[ident] = [xdiff,ydiff]
                done = starting_distribution(ident+1,angle)
    return(done)




def calc_score(ident,x,y,check):
    score = 0
    report = []
    for i in range(0,len(points)):
        if not i == ident: #generally has each point repel the other slightly
            scoredist = distance(points[i],[x,y])
            if scoredist <= 15:
                scoredist = 1.0/(max(scoredist,0.1))
                score += float(scoredist * repulsweight) # result is repulsweight at distance 1, half at distance 2, and so on. Slope becomes 0 shortly after distance 1, weight will spread this further out
    a = float(score)
    #print (f"repulsion score is {score}")
    for i in range(0,len(startpoint[ident])):
        reqdist = int(fromdist[ident][i]) #path distance from selected startpoint (looking backwards)
        #reqdist = reqdist / numpy.sqrt(compression) #maybe a mistake, aiming for more even distribution of paths
        goal = [0.0,0.0]
        goal[0] = float(points[startpoint[ident][i]][0])
        goal[1] = float(points[startpoint[ident][i]][1])
        scoredist = distance(goal,[x,y]) - reqdist # negative if inside reqdist radius
        report.append(f"from start {scoredist}")
        scoredist = max(scoredist, scoredist/10) #reduces penalty for being too close
        scoredist = float(scoredist ** 2) 
        scoredist = scoredist * 0.5 * goalweight#score minimum (0) at pathdistance, half square of deviation otherwise. Slope equal to distance away from pathdistance, or less of that when inside
        score += scoredist
    b = float(score - a)
    #print(f"startpoint score is {b}")
    for i in range(0,len(endgoal[ident])):
        reqdist = int(remdist[ident][i]) #path distance from selected goal (looking forwards)
        #reqdist = reqdist / numpy.sqrt(compression) #maybe a mistake, aiming for more even distribution of paths
        goal = [0.0,0.0]
        goal[0] = float(points[endgoal[ident][i]][0])
        goal[1] = float(points[endgoal[ident][i]][1])
        scoredist = float(distance(goal,[x,y]) - reqdist)# negative if inside reqdist radius
        report.append(f"from end {scoredist}")
        scoredist = max(scoredist, scoredist/10) #reduces penalty for being too close
        scoredist = float(scoredist ** 2)  
        scoredist = scoredist * 0.5 * goalweight#score minimum (0) at pathdistance, half square of deviation otherwise. Slope equal to distance away from pathdistance, or less of that when inside
        score += scoredist
    a = float(score - b)
    #print(f"goal score is {a}")
    for i in range(0,len(nextpoint[ident])):
        reqdist = int(nextdist[ident][i])
        goal = [0.0,0.0]
        goal[0] = float(points[nextpoint[ident][i]][0])
        goal[1] = float(points[nextpoint[ident][i]][1])
        scoredist = float(distance(goal,[x,y]) - reqdist)
        report.append(f"from next {scoredist}")
        scoredist = float(scoredist ** 2)  #New Version!! To be checked.
        scoredist = scoredist*0.5*distweight #slope = distance away from exact distance
        score += scoredist
    b = float(score - a)
    #print(f"nextpoint score is {b}")
    for i in range(0,len(prevpoint[ident])):
        reqdist = int(prevdist[ident][i])
        goal = [0.0,0.0]
        goal[0] = float(points[prevpoint[ident][i]][0])
        goal[1] = float(points[prevpoint[ident][i]][1])
        scoredist = float(distance(goal,[x,y]) - reqdist)
        report.append(f"from previous {scoredist}")
        scoredist = float(scoredist ** 2)  #New Version!! To be checked.
        scoredist = scoredist*0.5*distweight #slope = distance away from exact distance
        score += scoredist
    a = float(score - b)
    #print(f"prevpoint score is {a}")
    goal = [0.0,0.0]
    goal[0] = float(points[prevpoint[ident][0]][0] - x)
    goal[1] = float(points[prevpoint[ident][0]][1] - y)
    goal1 = [0.0,0.0]
    goal1[0] = float(points[nextpoint[ident][0]][0] - x)
    goal1[1] = float(points[nextpoint[ident][0]][1] - y)
    dotproduct = goal[0]*goal1[0] + goal[1]*goal1[1]
    absolutes = [0.0,0.0]
    absolutes[0] = max(distance(goal,[0,0]),0.01)
    absolutes[1] = max(distance(goal1,[0,0]),0.01)
    scoredist = 0-float(dotproduct/(absolutes[0]*absolutes[1]))
    report.append(f"from angle {scoredist}")
    score += scoredist * angleweight
    if check:
        print(report)
    return(float(score))

def score_gradient(ident):
    ident = int(ident)
    coordinates = [0.0,0.0]
    coordinates[0] = float(points[ident][0])
    coordinates[1] = float(points[ident][1])
    newforce = [0.0,0.0]
    newforce[0] = float(forces[ident][0])*momentum
    newforce[1] = float(forces[ident][1])*momentum
    scoreup = calc_score(ident, coordinates[0],coordinates[1] + width,False)
    scoredown = calc_score(ident, coordinates[0],coordinates[1] - width,False)
    scoreleft = calc_score(ident, coordinates[0] - width,coordinates[1],False)
    scoreright = calc_score(ident, coordinates[0] + width,coordinates[1],False)
    newforce[0] += float((scoreleft-scoreright)/width)
    newforce[1] += float((scoredown-scoreup)/width)
    return(newforce)



for force in range(0,len(forces)):
    forces[force] = [random.normalvariate(0,temperature),random.normalvariate(0,temperature)]

equal_starting_distribution()

done = not restart
startattempt = 0
startposattemptmax = 10*(len(points) ** 3)
startposattempt = 0


while not done:
    done = starting_distribution(endindex,random.normalvariate(0.785,compression/2)) #currently only generates points for new path...should tgis be expanded?
    startattempt += 1
    if startattempt >10 and not done:
        done = True
        print("Using default start")


pointorder = []
bestscore = 0
bestpoints = points
for i in range(0,len(points)): #evaluate current scores, initialise point order
    pointorder.append(i)
    coordinates = [0.0,0.0]
    coordinates[0] = float(points[i][0])
    coordinates[1] = float(points[i][1])
    bestscore += calc_score(i, coordinates[0],coordinates[1],False)

done = not reanneal # skips annealing
oldscore = 0
setscore = 1
threshold = 0.5
turnsnochange = 0
attempt = 0
attemptsmax = int(max(5000/len(points),1) )
steps = 10
temperature = originaltemp




while not done:
    oldscore = float(setscore)
    setscore = 0.0
    attempt += 1
    random.shuffle(pointorder)
    movedist2 = 0
    for i in pointorder: #cycle over points in different order each time
        if not fixed[i]: #produce gradients/forces for current points
            for step in range (0, steps):
                vector = [0.0,0.0] #include momentum here
                vector = score_gradient(i)
                vector[0] += float(forces[i][0])*momentum
                vector[1] += float(forces[i][1])*momentum
                forces[i] = vector
                movex = float(vector[0] + random.normalvariate(0,temperature))
                movey = float(vector[1] + random.normalvariate(0,temperature))
                points[i][0] += (movex * timescale)
                points[i][1] += (movey * timescale)
                movedist2 += movex **2
                movedist2 += movey **2
    for i in range(0,len(points)):#score whole current set of points
        coordinates = [0.0,0.0]
        coordinates[0] = float(points[i][0])
        coordinates[1] = float(points[i][1])
        setscore += float(calc_score(i, coordinates[0],coordinates[0],False)/len(points))
    if setscore < bestscore:
        bestpoints = []
        for point in range(0,len(points)):
            bestpoints.append([])
            for d in range(0,len(points[point])):
                bestpoints[point].append(float(points[point][d]))
        bestscore = float(setscore)
        print(bestscore)
    if attempt % int(attemptsmax/10) == 0:
        print(f"{int(100*attempt/attemptsmax)}% done, score {setscore}")
    if oldscore-setscore < threshold:
        turnsnochange += 1
        if turnsnochange >= 50:
            turnsnochange = 0
            if random.random() > 0.75:
                for point in range(0,len(points)):
                    if not fixed[point]:
                        points[i] = []
                starting_distribution(2,random.normalvariate(0.785,compression/2))
                equal_starting_distribution()
            else:
                points = bestpoints
            print(f"restarting")
    else:
        turnsnochange = max(turnsnochange-1, 0)
    if attempt >= attemptsmax or setscore < threshold:
        if turnsnochange > 0:
            print(f"Attempt {attempt}, current score is {setscore}, {turnsnochange} trials since last improvement")
        else:
            print(f"Attempt {attempt}, current score is {setscore}")
        done = True
    elif cooling:
        #timescale = timescale * 0.999
        if setscore < 1 or attempt > attemptsmax/2:
            temperature = min(originaltemp* setscore, temperature,2*originaltemp*(1-(attempt/attemptsmax)))

if setscore > bestscore:
    points = bestpoints
    print(f"Reverting to bestscore {bestscore}, using {bestpoints}")
else:
    print(f"using current score {setscore} instead of {bestscore}")
setscore = 0
for i in range(0,len(points)): #evaluate current scores
    coordinates = [0.0,0.0]
    coordinates[0] = float(points[i][0])
    coordinates[1] = float(points[i][1])
    if not fixed[i]:
        checktime = True
    else:
        checktime = False
    setscore += calc_score(i, coordinates[0],coordinates[1],checktime)
print(setscore/len(points))
#for i in (endgoal, "remdist", remdist, "startpoint",startpoint, "fromdist",fromdist, "prevpoint",prevpoint, "prevdist",prevdist,"nextpoint,dist",nextpoint,nextdist,"loopstarts,ends",loopstarts,loopends,looprelatives,loopbasedist,loopdist,"looplast, remainders",looplast,loopremainders,"pathvalues",pathvalues):
#    print(i)



backgroundpoints = []
backgroundrange = [[0,0],[0,0]]

for point in (points):
    backgroundrange[1][1] = int(max(point[1],backgroundrange[1][1]))
    backgroundrange[1][0] = int(min(point[1],backgroundrange[1][0]))
    backgroundrange[0][1] = int(max(point[0],backgroundrange[0][1]))
    backgroundrange[0][0] = int(min(point[0],backgroundrange[0][0]))



for n in range(0,20):
    backgroundpoints.append([random.randrange(backgroundrange[0][0]-10,backgroundrange[0][1]+10),random.randrange(backgroundrange[1][0]-10,backgroundrange[1][1]+10)])

pathmap = Voronoi((points+backgroundpoints))
fig = voronoi_plot_2d(pathmap, show_vertices=False, line_alpha = 0.0)

for path in range(0,len(pathvalues)):
    for event in pathvalues[path]:
        pathpointx[path].append(float(points[event][0]))
        pathpointy[path].append(float(points[event][1]))
    plt.plot(pathpointx[path],pathpointy[path],linewidth=1, c=[random.random(),random.random(),random.random()])

"""
Create Dataframe to save
Variables still to save:

,"backgroundpoints","eventnames"

,backgroundpoints,eventnames
Loop info?
"""

dictsave = {}
names = ["nextpoint","nextdist","prevpoint","prevdist","startpoint","fromdist","endgoal","remdist","points","event_dcs","colours","event_descriptions","paths","fixed"]
variables = [nextpoint,nextdist,prevpoint,prevdist,startpoint,fromdist,endgoal,remdist,points,event_dcs,colours,event_descriptions,paths,fixed]
for i in range(0,len(names)):
    dictsave[names[i]] = variables[i]


terrain_colour = {"W":"xkcd:straw","U":"xkcd:blue","B":"xkcd:slate","R":"xkcd:burnt orange","G":"xkcd:grass green",
    "WU":"xkcd:sky blue","UB":"xkcd:dark blue","BR":"xkcd:dark red","RG":"xkcd:khaki",
    "WG":"xkcd:very light green","WB":"xkcd:tan","UR":"xkcd:magenta","BG":"xkcd:forest green",
    "WR":"xkcd:rose","UG":"xkcd:turquoise",
    "C":"xkcd:cerulean","WC":"xkcd:light blue","UC":"xkcd:bright blue","BC":"xkcd: royal blue","RC":"xkcd:royal purple","GC":"xkcd:aqua",
    "D":"xkcd:sand","WD":"xkcd:beige","UD":"xkcd:azure","BD":"xkcd:dark tan","RD":"xkcd:dusty rose","GD":"xkcd:light olive",
    "V":"xkcd:rust","WV":"xkcd:dark pink","UV":"xkcd:purple","BV":"xkcd:crimson","RV":"xkcd:rust","GV":"xkcd:taupe",
    "A":"xkcd:robin's egg blue","WA":"xkcd:pale blue","UA":"xkcd:baby blue","BA":"xkcd:greyish blue","RA":"xkcd:dark purple","GA":"xkcd:teal",
    "c":"xkcd:grey","Wc":"xkcd:light grey","Uc":"xkcd:sea blue","Bc":"xkcd:dark brown","Rc":"xkcd:dark lavender","Gc":"xkcd:greenish grey",
    "WUG":"xkcd:bright teal","WUB":"xkcd:dusty blue",
    "UBR":"xkcd:wine","BRG":"brick red",
    "WRG":"xkcd:sage green","WBR":"xkcd:amber",
    "URG":"xkcd:cornflower","WBG":"xkcd:greyish green",
    "WUR":"xkcd:sky","UBG":"xkcd:dark aqua"}

def local_colour(colour_code):
    true_code = ""
    for letter in "WUBRGCDAVc":
        if not colour_code.find(letter) == -1:
            true_code = true_code + letter
    return terrain_colour[true_code]

for region in range(0,len(colours)):
    indexlist = pathmap.regions[region]
    tilesx.append([])
    tilesy.append([])
    for point in indexlist:
        if point >= 0:
            tilesx[region].append(pathmap.vertices[point][0])
            tilesy[region].append(pathmap.vertices[point][1])
    print(tilesx[region],tilesy[region],pathmap.regions[region])
    if len(tilesx[region]) >= 3:
        region_colour = local_colour(colours[region])
        plt.fill(tilesx[region],tilesy[region],region_colour)

plt.show()


dfsave = pandas.DataFrame(dictsave)
print(dfsave)


save = input("Save new points? y/n\n")
if (not save.find("y")  ==-1)  or not (save.find("Y") == -1):
    savefile = input(f"File (.csv) to write to? Default is {loadfile}\n")
    if savefile == "":
        savefile = loadfile
    elif savefile.find(".csv") == -1:
        savefile = savefile + ".csv"
    try:
        dfsave.to_csv(savefile)
        print (savefile)
    except:
        savefile = input("Could not find file. Please retype filename including .csv extension\n")
        try:
            dfsave.to_csv(savefile)
        except:
            print("Could not save data. Pausing to let you copy data manually. Press enter to quit")

