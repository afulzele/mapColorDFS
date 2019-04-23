import copy
import webbrowser

colored = {}

singleton = 0
dfs_with_heuristic = 0
def check_valid(graph):
    for node,nexts in graph.items():
        assert(node not in nexts) # # no node linked to itself
        for next in nexts:
            assert(next in graph and node in graph[next]) # A linked to B implies B linked to A
#DFS

def get_neighbours(state,country,country_colors):
    if dfs_with_heuristic == 0:
        return country[state]
    else:
        if singleton == 0:
            candidates_with_add_info = [
            (
            -len({colored[neigh] for neigh in country[n] if neigh     in colored}), # nb_forbidden_colors(nrighbour with colors ?)
            -len({neigh          for neigh in country[n] if neigh not in colored}), # minus nb_uncolored_neighbour(if neigh is not in color list
            #then calculate the number of neighbours)
            n
            ) for n in country[state] if n not in colored]
        else:
            candidates_with_add_info = [
            (
                -len({colored[neigh] for neigh in country[n] if neigh in colored}),
                # nb_forbidden_colors(nrighbour with colors ?)
                -len({neigh for neigh in country[n] if neigh not in colored}),
                # minus nb_uncolored_neighbour(if neigh is not in color list
                # then calculate the number of neighbours)
                len(country_colors[n]),
                n
            ) for n in country[state] if n not in colored]

        print(candidates_with_add_info,"()()()()()")
        candidates_with_add_info.sort()
        print(candidates_with_add_info,"--Sort - ()()()()()")
        if singleton == 0:
            candidates = [n for _,_,n in candidates_with_add_info]
        else:
            candidates = [n for _,_,_,n in candidates_with_add_info]
        return candidates

def get_colors(state,country,country_colors):
    if dfs_with_heuristic == 0:
        return country_colors[state]
    else:
        a = []
        for color in country_colors[state]:
            no_of_colors = 0
            a.append([color])
            #print("a",a)
            for neigh in country[state]:
                if color in country_colors[neigh]:
                    no_of_colors = no_of_colors + len(country_colors[neigh]) - 1
                else:
                    no_of_colors = no_of_colors + len(country_colors[neigh])
            #print ("Index Of Color",a.index(color))
            a[a.index([color])].append(no_of_colors)
        #print(a)
        a = sorted(a,key = lambda x:x[1],reverse = True)
        a = [x[0] for x in a]
        #print("a after sorting ",a)
        return a

def solve_problem_DFS(state,country,country_colors):
    increment_color = 0
    flag = 0
    #print("Country Colors",country_colors)
    for color in get_colors(state,country,country_colors):
        # if lsv(state,country,country_colors,color) == False:

        for j in country[state]:
            #print("country_colors[state][i]",j,i,country_colors[state][i])
            if j in colored and colored[j] == color:
                #print("break",state)
                increment_color = 1
                break
        if increment_color == 1:
            increment_color = 0
            continue
        colored[state] = color
        print("Trying to give color %s to %s" %(colored[state],state))
        #print(state,colored[state])
        for k in get_neighbours(state,country,country_colors):
            if k not in colored:
                if (solve_problem_DFS(k, country, country_colors) == False):
                    colored.pop(state)
                    flag = 1
                    break
        if flag == 0:
            print("Gave color %s to %s" % (colored[state],state))
            return True
        else:
            flag = 0
            continue
    return False

#DFS with Forward Chaining
def reduce_domain(state,country,cntry_colors):
    for j in country[state]:
        if colored[state] in cntry_colors[j]:
            # print("Removing %s color from %s ", j, colored[state])
            cntry_colors[j].remove(colored[state])

def reduce_domain_forward_check(color,state,country,cntry_colors):
    #print ("inside reduce domain forward check")
    p = copy.deepcopy(cntry_colors)
    for j in country[state]:
        #print("---------------------------------------------------Color",p[state][color],p[j])
        if color in p[j] :
            p[j].remove(color)
        #print("Checking Empty List")
        if not check_domain(j,p):
            #print("returned False from Reduce Domain Forward check for state",state)
            return False
    return True

def check_domain(state,cntry_colors):
    #print ("Inside Check Domain")
    if not (cntry_colors[state]) :
        #print("the list is empty",state)
        return False
    return True

def solve_problem_DFS_FC(state,country,country_colors):
    flag = 0
    popped = 0
    b = copy.deepcopy(country_colors)
    for color in get_colors(state,country,country_colors):
        # Taking Colours of Country into temporary Variable since it will be used for backtracking
        a = copy.deepcopy(b)
        # if popped == 0:
        #print("State =  a[state]",len(a[state]))
        #print("country_colors[state][i]", state, i, a[state])
        #print("Check a before reduce domain forward check", a)
        if reduce_domain_forward_check(color,state,country,a) == False:
            #print("Got False")
            #print("Check a after reduce domain forward check and got false", a)
            # if i < len(b[state]) - 1:
            continue
            # else:
            #     break
        #print("country_colors[state][i]",state,i,a[state])
        colored[state] = color
        print("Trying to give color %s to %s" %(color,state))
        reduce_domain(state, country, a)
        #for j in country[state]:
            #print("Neighbour Colors Value",j,a[j])
        #print("Check  a before assigning color to a state",a)
        a[state] = color
        #print("Check a after assigning color to a state",a)

        print("Neighbours of State before Sorting",state,country[state])
        if singleton == 1 and dfs_with_heuristic == 0:
            #a_list = [[neigh,len(a[neigh])] for neigh in country[state]]
            country[state] = sorted(country[state],key = lambda x:len(country_colors[x]),reverse = False)
            #print(a_list)
            #country[state] = list(map(lambda x: x[0],a_list))
            print("Neighbours of State after sorting", state, country[state])

        for neigh in get_neighbours(state,country,country_colors):
            if neigh not in colored:
                #print("Calling neighbour",neigh)
                if (solve_problem_DFS_FC(neigh,country,a)) == False :
                    colored.pop(state)
                    #print("Values of Color for all the states after popping", state,a)
                    flag = 1
                    break
        if flag == 0:
            return True
        else:
            #print("popped the colors for ", state, a[state])
            flag = 0
            #popped = 1
             # if i < len(b[state]) - 1:
            continue
            # else:
            #     break
    #print("No Values found for state",state,a[state])
    #print ("Values of Color for all the states",a)
    return False

AUWA  = 'AU-WA'
AUNT  = 'AU-NT'
AUSA  = 'AU-SA'
AUQ   = 'AU-QLD'
AUNSW = 'AU-NSW'
AUV   = 'AU-VIC'
AUT   = 'AU-TAS'

australia = { 
    AUT:   {AUV},
    AUWA:  {AUNT, AUSA},
    AUNT:  {AUWA, AUQ, AUSA},
    AUSA:  {AUWA, AUNT, AUQ, AUNSW, AUV},
    AUQ:   {AUNT, AUSA, AUNSW},
    AUNSW: {AUQ, AUSA, AUV},
    AUV:   {AUSA, AUNSW, AUT} 
}

au_colors= { 
    AUT:  ['red','green','blue'],
    AUWA: ['red','green','blue'],
    AUNT: ['red','green','blue'],
    AUSA: ['red','green','blue'],
    AUQ:  ['red','green','blue'],
    AUNSW:['red','green','blue'],
    AUV:  ['red','green','blue']
}

AL = "US-AL"
AK = "US-AK"
AZ = "US-AZ"
AR = "US-AR"
CA = "US-CA"
CO = "US-CO"
CT = "US-CT"
DE = "US-DE"
FL = "US-FL"
GA = "US-GA"
HI = "US-HI"
ID = "US-ID"
IL = "US-IL"
IN = "US-IN"
IA = "US-IA"
KS = "US-KS"
KY = "US-KY"
LA = "US-LA"
ME = "US-ME"
MD = "US-MD"
MA = "US-MA"
MI = "US-MI"
MN = "US-MN"
MS = "US-MS"
MO = "US-MO"
MT = "US-MT"
NE = "US-NE"
NV = "US-NV"
NH = "US-NH"
NJ = "US-NJ"
NM = "US-NM"
NY = "US-NY"
NC = "US-NC"
ND = "US-ND"
OH = "US-OH"
OK = "US-OK"
OR = "US-OR"
PA = "US-PA"
RI = "US-RI"
SC = "US-SC"
SD = "US-SD"
TN = "US-TN"
TX = "US-TX"
UT = "US-UT"
VT = "US-VT"
VA = "US-VA"
WA = "US-WA"
WV = "US-WV"
WI = "US-WI"
WY = "US-WY"

united_states_of_america = {
    AL: {GA, FL, TN, MS},
    AK: {WA},
    AZ: {CA, NV, UT, CO, NM},
    AR: {MO, OK, TX, LA, TN, MS },
    CA: {OR, NV, AZ,HI},
    CO: {WY, NE, KS, OK, NM, AZ, UT},
    CT: {NY,RI,MA},
    DE: {MD,PA,NJ},
    FL: {AL, GA},
    GA: {SC, NC, TN, AL, FL},
    HI: {CA},
    ID: {WA, MT, OR, WY, UT, NV},
    IL: {WI, IA, MO, KY, IN, MI},
    IN: {MI, IL, KY, OH},
    IA: {MN, SD, NE, MO, WI, IL},
    KS: {NE, CO, OK, MO},
    KY: {IN, IL, MO, TN, OH, WV, VA},
    LA: {AR, TX, MS},
    ME: {NH},
    MD: {PA,WV,VA,DE},
    MA: {NY,VT,NH,CT,RI},
    MI: {IL, WI, IN, OH},
    MN: {ND, SD, IA, WI},
    MS: {TN, AR, LA, AL},
    MO: {IA, NE, KS, OK, AR, IL, KY, TN},
    MT: {ID, WY, SD, ND},
    NE: {SD, CO, WY, KS, MO, IA},
    NV: {OR, ID, UT, AZ, CA},
    NH: {ME,VT,MA},
    NJ: {NY,PA,DE},
    NM: {AZ, UT, CO, OK, TX},
    NY: {PA,NJ,CT,MA,VT},
    NC: {GA, TN, SC, VA},
    ND: {MT, SD, MN},
    OH: {MI, IN, KY, WV,PA},
    OK: {KS, CO, NM, TX, AR, MO},
    OR: {WA, ID, NV, CA},
    PA: {OH,WV,DE,NJ,NY,MD},
    RI: {CT,MA},
    SC: {GA, NC},
    SD: {ND, MT, WY, NE, MN, IA},
    TN: {KY,AR, MS, MO, AL, GA, NC,VA},
    TX: {OK, NM, AR, LA},
    UT: {ID, NV, WY, CO, AZ, NM},
    VT: {MA,NY,NH},
    VA: {WV, KY, NC,TN,MD},
    WA: {OR,ID,AK},
    WV: {OH, VA, KY,PA,MD},
    WI: {MN, IL, MI, IA},
    WY: {MT, SD,NE, CO, UT, ID},
}

us_colors = {
    AL: ['red', 'green', 'blue', 'yellow'],
    AK: ['red', 'green', 'blue', 'yellow'],
    AZ: ['red', 'green', 'blue', 'yellow'],
    AR: ['red', 'green', 'blue', 'yellow'],
    CA: ['red', 'green', 'blue', 'yellow'],
    CO: ['red', 'green', 'blue', 'yellow'],
    CT: ['red', 'green', 'blue', 'yellow'],
    DE: ['red', 'green', 'blue', 'yellow'],
    FL: ['red', 'green', 'blue', 'yellow'],
    GA: ['red', 'green', 'blue', 'yellow'],
    HI: ['red', 'green', 'blue', 'yellow'],
    ID: ['red', 'green', 'blue', 'yellow'],
    IL: ['red', 'green', 'blue', 'yellow'],
    IN: ['red', 'green', 'blue', 'yellow'],
    IA: ['red', 'green', 'blue', 'yellow'],
    KS: ['red', 'green', 'blue', 'yellow'],
    KY: ['red', 'green', 'blue', 'yellow'],
    LA: ['red', 'green', 'blue', 'yellow'],
    ME: ['red', 'green', 'blue', 'yellow'],
    MD: ['red', 'green', 'blue', 'yellow'],
    MA: ['red', 'green', 'blue', 'yellow'],
    MI: ['red', 'green', 'blue', 'yellow'],
    MN: ['red', 'green', 'blue', 'yellow'],
    MS: ['red', 'green', 'blue', 'yellow'],
    MO: ['red', 'green', 'blue', 'yellow'],
    MT: ['red', 'green', 'blue', 'yellow'],
    NE: ['red', 'green', 'blue', 'yellow'],
    NV: ['red', 'green', 'blue', 'yellow'],
    NH: ['red', 'green', 'blue', 'yellow'],
    NJ: ['red', 'green', 'blue', 'yellow'],
    NM: ['red', 'green', 'blue', 'yellow'],
    NY: ['red', 'green', 'blue', 'yellow'],
    NC: ['red', 'green', 'blue', 'yellow'],
    ND: ['red', 'green', 'blue', 'yellow'],
    OH: ['red', 'green', 'blue', 'yellow'],
    OK: ['red', 'green', 'blue', 'yellow'],
    OR: ['red', 'green', 'blue', 'yellow'],
    PA: ['red', 'green', 'blue', 'yellow'],
    RI: ['red', 'green', 'blue', 'yellow'],
    SC: ['red', 'green', 'blue', 'yellow'],
    SD: ['red', 'green', 'blue', 'yellow'],
    TN: ['red', 'green', 'blue', 'yellow'],
    TX: ['red', 'green', 'blue', 'yellow'],
    UT: ['red', 'green', 'blue', 'yellow'],
    VA: ['red', 'green', 'blue', 'yellow'],
    VT: ['red', 'green', 'blue', 'yellow'],
    WA: ['red', 'green', 'blue', 'yellow'],
    WV: ['red', 'green', 'blue', 'yellow'],
    WI: ['red', 'green', 'blue', 'yellow'],
    WY: ['red', 'green', 'blue', 'yellow'],
}

# Can't be bothered to complete the East part of the map - removing unused nodes (keeping them is also a good way to test your algorithm and see if still works)
united_states_of_america = {n:neigh for n,neigh in united_states_of_america.items() if neigh}

def makeBrowser(cname):
    global colored
    
    f = open('worldmap.html','w')

    message = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>IS Project 3 - Abhishek Fulzele & Rahul Patel</title>
    <link rel="stylesheet" media="all" href="./jquery-jvectormap.css"/>
    <script src="assets/jquery-1.8.2.js"></script>
    <script src="./jquery-jvectormap.js"></script>
    <script src="../lib/jquery-mousewheel.js"></script>

    <script src="../src/jvectormap.js"></script>

    <script src="../src/abstract-element.js"></script>
    <script src="../src/abstract-canvas-element.js"></script>
    <script src="../src/abstract-shape-element.js"></script>

    <script src="../src/svg-element.js"></script>
    <script src="../src/svg-group-element.js"></script>
    <script src="../src/svg-canvas-element.js"></script>
    <script src="../src/svg-shape-element.js"></script>
    <script src="../src/svg-path-element.js"></script>
    <script src="../src/svg-circle-element.js"></script>
    <script src="../src/svg-image-element.js"></script>
    <script src="../src/svg-text-element.js"></script>

    <script src="../src/vml-element.js"></script>
    <script src="../src/vml-group-element.js"></script>
    <script src="../src/vml-canvas-element.js"></script>
    <script src="../src/vml-shape-element.js"></script>
    <script src="../src/vml-path-element.js"></script>
    <script src="../src/vml-circle-element.js"></script>
    <script src="../src/vml-image-element.js"></script>

    <script src="../src/map-object.js"></script>
    <script src="../src/region.js"></script>
    <script src="../src/marker.js"></script>

    <script src="../src/vector-canvas.js"></script>
    <script src="../src/simple-scale.js"></script>
    <script src="../src/ordinal-scale.js"></script>
    <script src="../src/numeric-scale.js"></script>
    <script src="../src/color-scale.js"></script>
    <script src="../src/legend.js"></script>
    <script src="../src/data-series.js"></script>
    <script src="../src/proj.js"></script>
    <script src="../src/map.js"></script>

    <script src="assets/jquery-jvectormap-world-mill-en.js"></script>
    <script src="assets/jquery-jvectormap-us-aea-en.js"></script>
    <script src="assets/jquery-jvectormap-aus-en.js"></script>

    <script>
        jQuery.noConflict();
        jQuery(function(){
            var $ = jQuery;
            
            $('#map1').vectorMap({
                map: '"""
    message1 = """',
                panOnDrag: true,       
                series: {                    
                    regions: [{
                        scale: {
                            red: '#ff0000',
                            green: '#00ff00',
                            blue: '#0000ff',
                            yellow: '#ffee34'
                        },
                        attribute: 'fill',
                        values: 
    """
    message2 = """
                        ,
                        legend: {
                            horizontal: true,
                            title: 'Color'
                        }
                    }]
                }
            });
        })
    </script>
    </head>
    <body>
        <div id="map1" style="width: 600px; height: 400px"></div>
    </body>
    </html>
    """

    x = str(cname)

    mainmessage = message + x + message1 + str(colored) + message2

    f.write(mainmessage)
    f.close()

    webbrowser.open_new_tab('worldmap.html')


if __name__ ==  '__main__':

    print("1. America      2. Australia")
    country_name = int(input("Which country would you like to select:\n "))

    cname = ""
    fullname = {}
    color = {}
    abbr = ""

    if country_name == 1:
        cname = "us_aea_en"
        fullname = united_states_of_america
        color = us_colors
        abbr = WV
    elif country_name == 2:
        cname = "au_mill"
        fullname = australia
        color = au_colors
        abbr = AUWA

    check_valid(united_states_of_america)
    print("----------------------\n1. DFS\n2. DFS with Forward Chaining\n3. DFS with Forward Chaining and Singleton\n4. DFS With Heuristic\n5. DFS with Heuristic and Forward Chaining\n6. DFS with heuristic, Forward Chaining and singleton\n----------------------")
    algo_name = int(input("Which algorithm would you like to select:\n"))

    if algo_name == 1:
        if (solve_problem_DFS(abbr, fullname, color)):
            print(colored)
    if algo_name == 2:
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print("Count",len(colored.keys()))
            print(colored)
    if algo_name == 3:
        singleton = 1
        if solve_problem_DFS_FC(abbr, fullname, color):
            print("Count",len(colored.keys()))
            print(colored)
    if algo_name == 4:
        dfs_with_heuristic = 1
        if (solve_problem_DFS(abbr, fullname, color)):
            print(colored)
    if algo_name == 5:
        dfs_with_heuristic = 1
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print(colored)
    if algo_name == 6:
        dfs_with_heuristic = 1
        singleton = 1
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print(colored)

    makeBrowser(cname)
    colored.clear()
