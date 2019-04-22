import copy
def reduce_domain(state,country,cntry_colors):
    for j in country[state]:
        if colored[state] in cntry_colors[j]:
      #      #print("Removing %s color from %s ", j, colored[state])
            cntry_colors[j].remove(colored[state])


def reduce_domain_forward_check(color,state,country,cntry_colors):
    #print ("inside reduce domain forward check")
    p = copy.deepcopy(cntry_colors)
    for j in country[state]:
        #print("---------------------------------------------------Color",p[state][color],p[j])
        if p[state][color] in p[j] :
            p[j].remove(p[state][color])
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

colored = {}
def solve_problem(state,country,country_colors):
    flag = 0
    popped = 0
    b = copy.deepcopy(country_colors)
    for i in range(len(b[state])):
        # Taking Colours of Country into temporary Variable since it will be used for backtracking
        a = copy.deepcopy(b)
        # if popped == 0:
        #print("State =  a[state]",len(a[state]))
        #print("country_colors[state][i]", state, i, a[state])
        #print("Check a before reduce domain forward check", a)
        if reduce_domain_forward_check(i,state,country,a) == False:
            #print("Got False")
            #print("Check a after reduce domain forward check and got false", a)
            # if i < len(b[state]) - 1:
            continue
            # else:
            #     break
        #print("country_colors[state][i]",state,i,a[state])
        colored[state] = b[state][i]
        print("Trying to give color %s to %s" %(colored[state],state))
        reduce_domain(state, country, a)
        #for j in country[state]:
            #print("Neighbour Colors Value",j,a[j])
        #print("Check  a before assigning color to a state",a)
        a[state] = [colored[state]]
        #print("Check a after assigning color to a state",a)
        for neigh in country[state]:
            if neigh not in colored:
                #print("Calling neighbour",neigh)
                if (solve_problem(neigh,country,a)) == False :
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

# WA  = 'western australia'
# NT  = 'northwest territories'
# SA  = 'southern australia'
# Q   = 'queensland'
# NSW = 'new south wales'
# V   = 'victoria'
# T   = 'tasmania'
#
# australia = { T:   {V               },
#               WA:  {NT, SA         },
#               NT:  {WA, Q, SA       },
#               SA:  {WA, NT, Q, NSW, V},
#               Q:   {NT, SA, NSW   },
#               NSW: {Q, SA, V         },
#               V:   {SA, NSW, T     } }

AL = "Alabama"
AK = "Alaska"
AZ = "Arizona"
AR = "Arkansas"
CA = "California"
CO = "Colorado"
CT = "Connecticut"
DE = "Delaware"
FL = "Florida"
GA = "Georgia"
HI = "Hawaii"
ID = "Idaho"
IL = "Illinois"
IN = "Indiana"
IA = "Iowa"
KS = "Kansas"
KY = "Kentucky"
LA = "Louisiana"
ME = "Maine"
MD = "Maryland"
MA = "Massachusetts"
MI = "Michigan"
MN = "Minnesota"
MS = "Mississippi"
MO = "Missouri"
MT = "Montana"
NE = "Nebraska"
NV = "Nevada"
NH = "NewHampshire"
NJ = "NewJersey"
NM = "NewMexico"
NY = "NewYork"
NC = "NorthCarolina"
ND = "NorthDakota"
OH = "Ohio"
OK = "Oklahoma"
OR = "Oregon"
PA = "Pennsylvania"
RI = "RhodeIsland"
SC = "SouthCarolina"
SD = "SouthDakota"
TN = "Tennessee"
TX = "Texas"
UT = "Utah"
VT = "Vermont"
VA = "Virginia"
WA = "Washington"
WV = "WestVirginia"
WI = "Wisconsin"
WY = "Wyoming"
#
united_stated_of_america = {
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



# Can't be bothered to complete the East part of the map - removing unused nodes (keeping them is also a good way to test your algorithm and see if still works)
#united_stated_of_america = {n:neigh for n,neigh in united_stated_of_america.items() if neigh}

#colors  = {'r', 'g', 'b', 'y'}
# colors_aus  = {'r', 'g', 'b'}

def main():

    # aus_colors = {T: ['R', 'G', 'B'],
    #               WA: ['R', 'G', 'B'],
    #               NT: ['R', 'G', 'B'],
    #               SA: ['R', 'G', 'B'],
    #               Q: ['R', 'G', 'B'],
    #               NSW: ['R', 'G', 'B'],
    #               V: ['R', 'G', 'B']
    #               }

    us_colors = {
        AL: ['r', 'p', 'g', 'y'],
        AK: ['r', 'p', 'g', 'y'],
        AZ: ['r', 'p', 'g', 'y'],
        AR: ['r', 'p', 'g', 'y'],
        CA: ['r', 'p', 'g', 'y'],
        CO: ['r', 'p', 'g', 'y'],
        CT: ['r', 'p', 'g', 'y'],
        DE: ['r', 'p', 'g', 'y'],
        FL: ['r', 'p', 'g', 'y'],
        GA: ['r', 'p', 'g', 'y'],
        HI: ['r', 'p', 'g', 'y'],
        ID: ['r', 'p', 'g', 'y'],
        IL: ['r', 'p', 'g', 'y'],
        IN: ['r', 'p', 'g', 'y'],
        IA: ['r', 'p', 'g', 'y'],
        KS: ['r', 'p', 'g', 'y'],
        KY: ['r', 'p', 'g', 'y'],
        LA: ['r', 'p', 'g', 'y'],
        ME: ['r', 'p', 'g', 'y'],
        MD: ['r', 'p', 'g', 'y'],
        MA: ['r', 'p', 'g', 'y'],
        MI: ['r', 'p', 'g', 'y'],
        MN: ['r', 'p', 'g', 'y'],
        MS: ['r', 'p', 'g', 'y'],
        MO: ['r', 'p', 'g', 'y'],
        MT: ['r', 'p', 'g', 'y'],
        NE: ['r', 'p', 'g', 'y'],
        NV: ['r', 'p', 'g', 'y'],
        NH: ['r', 'p', 'g', 'y'],
        NJ: ['r', 'p', 'g', 'y'],
        NM: ['r', 'p', 'g', 'y'],
        NY: ['r', 'p', 'g', 'y'],
        NC: ['r', 'p', 'g', 'y'],
        ND: ['r', 'p', 'g', 'y'],
        OH: ['r', 'p', 'g', 'y'],
        OK: ['r', 'p', 'g', 'y'],
        OR: ['r', 'p', 'g', 'y'],
        PA: ['r', 'p', 'g', 'y'],
        RI: ['r', 'p', 'g', 'y'],
        SC: ['r', 'p', 'g', 'y'],
        SD: ['r', 'p', 'g', 'y'],
        TN: ['r', 'p', 'g', 'y'],
        TX: ['r', 'p', 'g', 'y'],
        UT: ['r', 'p', 'g', 'y'],
        VA: ['r', 'p', 'g', 'y'],
        VT: ['r', 'p', 'g', 'y'],
        WA: ['r', 'p', 'g', 'y'],
        WV: ['r', 'p', 'g', 'y'],
        WI: ['r', 'p', 'g', 'y'],
        WY: ['r', 'p', 'g', 'y'],
    }
    if (solve_problem(WV,united_stated_of_america,us_colors)):
        print("Count",len(colored.keys()))
        print(colored)
    colored.clear()

if __name__ ==  '__main__':
    main()