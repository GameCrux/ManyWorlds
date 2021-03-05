import math
import numpy as np
#import urllib3
import json

# Consider adding the https certificate verification


with open('MobData.json', 'r') as f:
    data = f.read()

mobData = json.loads(data)

'''
class mob:

    def __init__(self, HP, level, MP, name, physicalDefense, magicDefense, evasion, exp, isUndead):
        self.HP = HP
        self.level = level
        self.MP = MP
        self.name = name
        # self.speed=speed
        self.physicalDefense = physicalDefense
        self.magicDefense = magicDefense
        self.evasion = evasion
        self.exp = exp
        self.isUndead = isUndead
    # self.elementalAttributes=elementalAttributes

'''
''' IDK if this is the move...
for monsterNumber in mobData:
  #print(monsterNumber)
  name=mobData[monsterNumber]['info']['name']
  HP=mobData[monsterNumber]['meta']['maxHP']
  level=mobData[monsterNumber]['meta']['level']
  MP=mobData[monsterNumber]['meta']['maxMP']
  #speed=mobData[monsterNumber]['meta']['speed']
  physicalDefense=mobData[monsterNumber]['meta']['physicalDefense']
  magicDefense=mobData[monsterNumber]['meta']['magicDefense']
  evasion=mobData[monsterNumber]['meta']['evasion']
  exp=mobData[monsterNumber]['meta']['exp']
  isUndead=mobData[monsterNumber]['meta']['isUndead']
  #elementalAttributes=mobData[monsterNumber]['meta']['elementalAttributes']
  monsterNumber=mob(HP,level,MP,name,physicalDefense,magicDefense,evasion,exp,isUndead)

print(monsterNumber.name)
'''

'''
#Online Data Access
#http=urllib3.PoolManager()
#osmlibrary='http://lib.oldschoolmaple.com/api/v1/search?q='
#mobsearch=['slime','wild boar']

for monster in mobsearch:

  lib_response=http.request('GET', osmlibrary+mobsearch)
  mob_data=json.loads(lib_response.data.decode('utf-8'))

  HP=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['maxHP']
  level=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['level']
  name=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobName']
  MP=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['maxMP']
  speed=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['speed']
  physicalDefense=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['physicalDefense']
  magicDefense=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['magicDefense']
  evasion=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['evasion']
  exp=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['exp']
  isUndead=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['isUndead']
  elementalAttributes=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['elementalAttributes']
  accuracyRequiredToHit=mob_data['result']['exactMatchInfo']['mobInfo'][0]['mobMeta']['accuracyRequiredToHit']


monster=mob(HP,level,MP,name,speed,physicalDefense,magicDefense,evasion,exp,isUndead,elementalAttributes,accuracyRequiredToHit)
'''

def avghits_crit(minatk, maxatk, hp, skill, skillPercent, critical_rate, critical_damage):

    maxhits = math.ceil(hp / minatk)

    skilldict = {'none': 0, 'lucky7': 2, 'doublestab': 2, 'power strike': 1, 'energy bolt': 1, 'magic claw': 2}

    if skill == 'none':
        skillPercent = 1

    r = critical_rate

    if minatk == 0:
        minatk = 1
    if maxatk == 0:
        maxatk = 1

    n_attacklist = np.round(skillPercent * np.array(list(range(minatk, maxatk + 1))), 0)
    n_attacklist = n_attacklist.astype(int)

    c_attacklist = np.round(n_attacklist * critical_damage)

    c_attacklist = c_attacklist.astype(int)

    entropy = len(c_attacklist) + len(n_attacklist)

    multiplicity = np.zeros((maxhits, hp, maxhits+1), dtype=float)
    multiplicity[0, 0, 0] = len(n_attacklist)
    multiplicity[0, 0, 1] = len(c_attacklist)

    hpvar = np.ones(len(n_attacklist), dtype=int)

    for x in range(1, hp):
        hpvar = hpvar + 1

        newhp_n = hpvar - n_attacklist
        newhp_c = hpvar - c_attacklist

        n_multiplicity = sum(i <= 0 for i in newhp_n)
        c_multiplicity = sum(i <= 0 for i in newhp_c)

        multiplicity[0, hpvar[0]-1, 0] = n_multiplicity

        multiplicity[0, hpvar[0]-1, 1] = c_multiplicity

        recursion_terms_n = np.zeros((maxhits, maxhits+1), dtype=int) #hits+1 critical hits possible, including 0
        newhp_n = newhp_n[newhp_n > 0]

        for m in newhp_n:
            recursion_terms_n = recursion_terms_n + multiplicity[:, m - 1, :]

        multiplicity[1:, hpvar[0] - 1, :] = multiplicity[1:, hpvar[0] - 1, :] + recursion_terms_n[:-1, :]

        recursion_terms_c = np.zeros((maxhits, maxhits+1), dtype=int)
        newhp_c = newhp_c[newhp_c > 0]

        for m in newhp_c:
            recursion_terms_c = recursion_terms_c + multiplicity[:, m - 1, :]

        multiplicity[1:, hpvar[0] - 1, 1:] = multiplicity[1:, hpvar[0] - 1, 1:] + recursion_terms_c[:-1, :-1]


    mult_norm = np.zeros((maxhits, 1), dtype=float)

    for hit_number in range(1, maxhits + 1):

        mult_norm[hit_number-1, 0] = 0

        for c in range(0, maxhits+1):

            norm_term = r**c * (1-r)**(hit_number - c) / len(n_attacklist)**hit_number
            multi = multiplicity[hit_number-1, hp-1, c]
            mult_norm[hit_number-1, 0] = mult_norm[hit_number-1, 0] + multi*norm_term
    '''
    for d in range(0, maxhits):
            if entropy ** (d + 1) < 1.7976931348623157e308:
                norm_term = multiplicity[d, hp - 1] / entropy ** (d + 1)
            else:
                norm_term = 0
            mult_norm[d, 0] = norm_term
            continue
    '''
    average_hits = 0
    if skilldict[skill] == 0:
        for m in range(0, maxhits):
            average_hits = average_hits + mult_norm[m][0] * (m + 1)
    else:
        for m in range(0, maxhits):
            average_hits = average_hits + mult_norm[m][0] * math.ceil((m + 1) / skilldict[skill])

    return average_hits






minatk = 1
maxatk = 2
hp = 50
skill = 'none'
skillPercent = 1.4
critical_rate = 0.5
critical_damage = 1.4
#(avghits_crit(minatk, maxatk, hp, skill, skillPercent, critical_rate, critical_damage))



def avghits(minatk, maxatk, hp, skill, skillPercent):

    skilldict = {'none': 0, 'lucky7': 2, 'doublestab': 2, 'power strike': 1, 'energy bolt': 1, 'magic claw': 2}

    if skilldict[skill] == 0 or skill == 'magic claw' or skill == 'energy bolt':
        attacklist = np.array(list(range(minatk, maxatk + 1)))

        entropy = maxatk - minatk + 1

        maxhits = math.ceil(hp / minatk)

        multiplicity = np.zeros((maxhits, hp), dtype=float)
        multiplicity[0][0] = entropy

        hpvar = np.ones(len(attacklist), dtype=int)

        for eee in range(1, hp):
            hpvar = hpvar + 1
            newhp = hpvar - attacklist

            multiplicity[0][hpvar[0] - 1] = sum(i <= 0 for i in newhp)
            newhp = newhp[newhp > 0]
            recursion_terms = np.zeros((maxhits, 1), dtype=int)

            for m in newhp:
                recursion_terms = recursion_terms + multiplicity[:, m - 1].reshape(maxhits, 1)
                continue

            multiplicity[1:, hpvar[0] - 1] = multiplicity[1:, hpvar[0] - 1] + recursion_terms[:-1, 0]

        mult_norm = np.zeros((maxhits, 1), dtype=float)
        for d in range(0, maxhits):
            if entropy ** (d + 1) < 1.7976931348623157e308:
                norm_term = multiplicity[d, hp - 1] / entropy ** (d + 1)
            else:
                norm_term = 0
            mult_norm[d, 0] = norm_term
            continue

        average_hits = 0

        if skilldict[skill] == 0:
            for m in range(0, maxhits):
                average_hits = average_hits + mult_norm[m][0] * (m + 1)
        else:
            for m in range(0, maxhits):
                average_hits = average_hits + mult_norm[m][0] * math.ceil((m + 1) / skilldict[skill])

    else:

        attacklist = np.round(skillPercent*np.array(list(range(minatk, maxatk + 1))), 0)
        attacklist = attacklist.astype(int)

        entropy = len(attacklist)

        maxhits = math.ceil(hp / np.amin(attacklist))

        multiplicity = np.zeros((maxhits, hp), dtype=float)

        multiplicity[0][0] = entropy

        hpvar = np.ones(len(attacklist), dtype=int)

        for eee in range(1, hp):
            hpvar = hpvar + 1
            newhp = hpvar - attacklist

            multiplicity[0][hpvar[0] - 1] = sum(i <= 0 for i in newhp)
            newhp = newhp[newhp > 0]
            recursion_terms = np.zeros((maxhits, 1), dtype=int)

            for m in newhp:

                recursion_terms = recursion_terms + multiplicity[:, m - 1].reshape(maxhits, 1)
                continue

            multiplicity[1:, hpvar[0] - 1] = multiplicity[1:, hpvar[0] - 1] + recursion_terms[:-1, 0]

        mult_norm = np.zeros((maxhits, 1), dtype=float)
        for d in range(0, maxhits):
            if entropy ** (d + 1) < 1.7976931348623157e308:
                norm_term = multiplicity[d, hp - 1] / entropy ** (d + 1)
            else:
                norm_term = 0
            mult_norm[d, 0] = norm_term
            continue

        def normal_round(n):
            if n - math.floor(n) < 0.5:
                return math.floor(n)
            return math.ceil(n)

        average_hits = 0
        for m in range(0, maxhits):
            average_hits = average_hits + mult_norm[m][0] * math.ceil((m + 1) / skilldict[skill])

    return average_hits


def manyworlds(playerLevel, minatk_in, maxatk_in, accuracy, skill, skillPercent, LUK, wepatk, revenue, sort, magic, INT,
               spell_mastery, spell_attack, critical_check, critical_chance, critical_damage):
    monsterDict = {}
    monsterIndex = 0
    monsterStats = []

    if skill == 'lucky7':
        minatk_in = LUK*2.5*wepatk/100
        maxatk_in = LUK*5*wepatk/100

    if skill == 'magic claw' or skill == 'energy bolt':
        minatk_in = ((magic**2/1000+magic*spell_mastery*0.9)/30+INT/200)*spell_attack
        maxatk_in = ((magic**2/1000+magic)/30+INT/200)*spell_attack


    def getExpRequired(playerLevel):
        if playerLevel<=3:
            expReq=2*playerLevel**2+13*playerLevel
        elif playerLevel<=5:
            expReq=4*playerLevel**2+7*playerLevel
        elif playerLevel<=50:
            if playerLevel%3==0:
                expReq=(playerLevel**4+57*playerLevel**2)/9
            else:
                expReq=(playerLevel**4 + 55 * playerLevel**2 - 56) / 9
        else:
            expReq = math.floor(1.0548*getExpRequired(playerLevel-1))

        return expReq

    expRequired = getExpRequired(playerLevel)

    ''' OSM EXP Algorithm~~~~~~~~~~~~~~~~~

    if playerLevel<=10:
        expMultiplier = 1
    elif playerLevel<=80:
        expMultiplier = 1-(1/70)*(playerLevel-10)
    else:
        expMultiplier=0
        
    '''

    expMultiplier = 1

    def expPerHitKey(theTuple):
        return theTuple[1]

    def mesosPerHitKey(theTuple):
        return theTuple[4]

    for monsterNumber in mobData:
        level = mobData[monsterNumber]['meta']['level']
        levelDifference = level - playerLevel
        avoid = mobData[monsterNumber]['meta']['evasion']
        print("Now killing", mobData[monsterNumber]['info']['name'], '...')

        if skill == 'energy bolt' or skill == 'magic claw':
            hitChance = 1
        else:
            if avoid == 0:
                hitChance = 1
            else:
                hitChance = accuracy / ((1.84 + 0.07 * levelDifference) * avoid) - 1

        if level <= 10 + playerLevel and hitChance >= 1:
            monsterDict[monsterIndex] = monsterNumber
            HP = mobData[monsterNumber]['meta']['maxHP']

            #print(monsterNumber)
            if revenue == 1:

                total_item_revenue = 0

                if not mobData[monsterNumber]['mesos']:
                    continue
                else:
                    mesos = mobData[monsterNumber]['mesos'][0]['mesos']
                    meso_chance = mobData[monsterNumber]['mesos'][0]['chance']/1e9
                    mesos_revenue = mesos*meso_chance
                for ii in range(0, len(mobData[monsterNumber]['drops'])):
                    if not mobData[monsterNumber]['drops'][ii]['info']:
                        continue
                    else:
                        item_price = mobData[monsterNumber]['drops'][ii]['meta']['shop']['price']
                        item_chance = mobData[monsterNumber]['drops'][ii]['chance']/1e9
                        item_revenue = item_price*item_chance
                        total_item_revenue = total_item_revenue + item_revenue
                total_revenue_per_kill = mesos_revenue+total_item_revenue



            # Defense Modifier

            WDEF = mobData[monsterNumber]['meta']['physicalDefense']
            MDEF = mobData[monsterNumber]['meta']['magicDefense']

            if skill != 'magic claw' or skill != 'energy bolt':
                if levelDifference > 0:
                    maxatk = round(maxatk_in * (1 - 0.01 * levelDifference) - 0.5 * WDEF)
                    minatk = round(minatk_in * (1 - 0.01 * levelDifference) - 0.6 * WDEF)
                    if minatk <= 0:
                        minatk = 1
                    if maxatk <= 0:
                        maxatk = 1
                else:
                    maxatk = int(maxatk_in - 0.5 * WDEF)
                    minatk = int(minatk_in - 0.6 * WDEF)
                    if minatk <= 0:
                        minatk = 1
                    if maxatk <= 0:
                        maxatk = 1
            else:
                if levelDifference > 0:
                    maxatk = int(round(maxatk_in - MDEF*0.5 * (1 + 0.01 * levelDifference)))
                    minatk = int(round(minatk_in - MDEF*0.6 * (1 + 0.01 * levelDifference)))
                    if minatk <= 0:
                        minatk = 1
                    if maxatk <= 0:
                        maxatk = 1
                else:
                    maxatk = int(maxatk_in)
                    minatk = int(minatk_in)

            maxhits = math.ceil(HP / minatk)
            if maxhits <= 50:
                if critical_check == 0:
                    averageHitsRequired = avghits(minatk, maxatk, HP, skill, skillPercent)
                else:
                    averageHitsRequired = avghits_crit(minatk, maxatk, HP, skill, skillPercent, critical_chance,
                                                       critical_damage)
            else:
                continue

            monsterExp=math.floor(expMultiplier*mobData[monsterNumber]['meta']['exp'])

            expPerHit=monsterExp / averageHitsRequired
            percentPerHit=expPerHit * 100 / expRequired

            if revenue == 1:
                revenue_per_hit = total_revenue_per_kill / averageHitsRequired
                monsterStats.append((monsterIndex, expPerHit, percentPerHit, averageHitsRequired, revenue_per_hit))
            else:
                monsterStats.append((monsterIndex, expPerHit, percentPerHit, averageHitsRequired))

            monsterIndex = monsterIndex + 1
        else:
            continue

    print("~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~")

    if sort == 'Level up':
        monsterStats.sort(key=expPerHitKey, reverse=True)
    elif sort == 'Wealth':
        monsterStats.sort(key=mesosPerHitKey, reverse=True)

    class results:
        def __init__(self, monsterDict, monsterIndex, monsterStats):
            self.monsterDict = monsterDict
            self.monsterIndex = monsterIndex
            self.monsterStats = monsterStats

    answer = results(monsterDict, monsterIndex, monsterStats)

    return answer


#inputs
minatk_in = 23
maxatk_in = 46
playerLevel = 30
accuracy = 85
skill = 'lucky7'
skillPercent = 150
LUK = 114
wepatk = 35
magic = 50
INT = 4
spell_mastery = 60
spell_attack = 40

HP = 45

#test = avghits(minatk_in, maxatk_in, HP, skill, skillPercent/100)
#print(test)


#test=manyworlds(playerLevel, minatk_in, maxatk_in, accuracy, skill, skillPercent/100, LUK, wepatk, 0, 0, magic, INT,
                #spell_mastery, spell_attack, 0, 0, 0)

#print(test.monsterStats)

