import tkinter as tk
from Main import manyworlds
import json
from prettytable import PrettyTable

with open('MobData.json', 'r') as f:
    data = f.read()

mobData = json.loads(data)


root = tk.Tk()

inputframe = tk.Frame(root)
inputframe.pack()

minatklabel = tk.Label(inputframe, text='Minimum attack').grid(row=2, column=1)
minatk = tk.Entry(inputframe)
minatk.grid(row=2, column=2)


maxatklabel = tk.Label(inputframe, text='Maximum attack').grid(row=3, column=1)
maxatk = tk.Entry(inputframe)
maxatk.grid(row=3, column=2)

levelLabel = tk.Label(inputframe, text='Character level').grid(row=0, column=1)
level = tk.Entry(inputframe)
level.grid(row=0, column=2)

wepatklabel= tk.Label(inputframe, text='Weapon Attack').grid(row=1, column=1)
wepatk = tk.Entry(inputframe)
wepatk.grid(row=1, column=2)

accuracylabel = tk.Label(inputframe, text='Accuracy').grid(row=4, column=1)
accuracy = tk.Entry(inputframe)
accuracy.grid(row=4, column=2)

INTlabel = tk.Label(inputframe, text='INT').grid(row=5, column=1)
INT = tk.Entry(inputframe)
INT.grid(row=5, column=2)

LUKlabel = tk.Label(inputframe, text='LUK').grid(row=6, column=1)
LUK = tk.Entry(inputframe)
LUK.grid(row=6, column=2)


def graycriticals():
    if criticalCheck.get() == 0:
        CriticalPercent = tk.Entry(inputframe, state='disabled')
        CriticalPercent.grid(row=8, column=2)
        CriticalDamage = tk.Entry(inputframe, state='disabled')
        CriticalDamage.grid(row=9, column=2)
    else:
        CriticalPercent = tk.Entry(inputframe, state='normal')
        CriticalPercent.grid(row=8, column=2)
        CriticalDamage = tk.Entry(inputframe, state='normal')
        CriticalDamage.grid(row=9, column=2)



criticalCheck = tk.IntVar()
CriticalHits = tk.Checkbutton(inputframe, text='Criticals', variable=criticalCheck, command=graycriticals())
CriticalHits.grid(row=7, column=1, pady=(10, 0))


CriticalPercentLabel = tk.Label(inputframe, text='% Chance').grid(row=8, column=1)
CriticalPercent = tk.Entry(inputframe)
CriticalPercent.grid(row=8, column=2)
CriticalDamageLabel = tk.Label(inputframe, text='% Damage').grid(row=9, column=1)
CriticalDamage = tk.Entry(inputframe)
CriticalDamage.grid(row=9, column=2)

skill = tk.StringVar()

beginnerlabel = tk.Label(inputframe, text='Beginner')
beginnerlabel.grid(column=3, row=0, padx=100, sticky='w')

noskill=tk.Radiobutton(inputframe, text='No Skill', variable=skill, value='none')
noskill.grid(row=1, column=3, sticky='w', padx=(100, 0))

thieflabel=tk.Label(inputframe, text='Thief')
thieflabel.grid(column=3, row=2, padx=100, pady=(10, 0), sticky='w')

luckyseven=tk.Radiobutton(inputframe, text='Lucky Seven', variable=skill, value='lucky7')
luckyseven.grid(column=3, row=3, sticky='w', padx=(100, 0))

doublestab=tk.Radiobutton(inputframe, text='Double Stab', variable=skill, value='doublestab')
doublestab.grid(column=4, row=3)

warriorlabel = tk.Label(inputframe, text='Warrior').grid(row=4, column=3, sticky='w', padx=100, pady=(10, 0))

powerstrike = tk.Radiobutton(inputframe, text='Power Strike', variable=skill, value='power strike')
powerstrike.grid(column=3, row=5, sticky='w', padx=(100, 0))

magicianlabel = tk.Label(inputframe, text='Magician').grid(row=6, column=3, sticky='w', padx=100, pady=(10, 0))

energybolt = tk.Radiobutton(inputframe, text='Energy Bolt', variable=skill, value='energy bolt')
energybolt.grid(column=3, row=7, sticky='w', padx=(100, 0))

magicclaw = tk.Radiobutton(inputframe, text='Magic Claw', variable=skill, value='magic claw')
magicclaw.grid(row=7, column=4)

magiclabel = tk.Label(inputframe, text='Magic')
magiclabel.grid(row=8, column=3, sticky='e')
magic = tk.Entry(inputframe)
magic.grid(row=8, column=4, sticky='w')

spell_mastery_label = tk.Label(inputframe, text='Spell Mastery %:')
spell_mastery_label.grid(row=9, column=3, sticky='e')
spell_mastery = tk.Entry(inputframe)
spell_mastery.grid(row=9, column=4, sticky='w')

spell_attack_label = tk.Label(inputframe, text='Spell Attack')
spell_attack_label.grid(row=10, column=3, sticky='e')
spell_attack = tk.Entry(inputframe)
spell_attack.grid(row=10, column=4, sticky='w')



damagepercentlabel=tk.Label(inputframe, text='Skill Damage % :')
damagepercentlabel.grid(row=11, column=3, padx=(30, 0))
damagepercent= tk.Entry(inputframe)
damagepercent.grid(row=11, column=4)


sortingframe = tk.Frame(root)
sortingframe.pack()

sortlabel= tk.Label(sortingframe, text='Priority:').grid(row=0, column=0)
sortoptions = tk.Spinbox(sortingframe, values=('Level up', 'Wealth'))
sortoptions.grid(row=0, column=1)
sortnumberlabel = tk.Label(sortingframe, text='Show:').grid(row=1, column=0)
sortnumber = tk.Spinbox(sortingframe, from_=1, to=15)
sortnumber.grid(row=1, column=1)

revenue_status = tk.IntVar()
revenue = tk.Checkbutton(sortingframe, text='Compute Revenue', variable=revenue_status)
revenue.grid(columnspan=2, row=2, column=0)

submitframe = tk.Frame(root)
submitframe.pack()


def getresults(shown_results):

    atkmin = minatk.get()
    if not atkmin:
        atkmin = 1
    else:
        atkmin = int(minatk.get())

    atkmax = maxatk.get()
    if not atkmax:
        atkmax =1
    else:
        atkmax = int(maxatk.get())

    skill_percent = damagepercent.get()
    if not skill_percent:
        skill_percent = 1
    else:
        skill_percent = int(damagepercent.get())/100

    luk = LUK.get()
    if not luk:
        luk = 1
    else:
        luk = int(LUK.get())

    weapon_attack = wepatk.get()
    if not weapon_attack:
        weapon_attack = 1
    else:
        weapon_attack = int(wepatk.get())

    Magic = magic.get()
    if not Magic:
        Magic = 1
    else:
        Magic = int(magic.get())

    Int = INT.get()
    if not Int:
        Int = 1
    else:
        Int = int(INT.get())

    Spell_Mastery = spell_mastery.get()
    if not Spell_Mastery:
        Spell_Mastery = 1
    else:
        Spell_Mastery = int(spell_mastery.get())/100

    Spell_Attack = spell_attack.get()
    if not Spell_Attack:
        Spell_Attack = 1
    else:
        Spell_Attack = int(spell_attack.get())

    Accuracy = accuracy.get()
    if not Accuracy:
        Accuracy = 1
    else:
        Accuracy = int(accuracy.get())

    critical_check = criticalCheck.get()
    if critical_check == 0:
        critical_chance = 0
        critical_damage = 0
    else:
        #print(CriticalPercent.get())
        critical_chance = int(CriticalPercent.get())/100
        critical_damage = int(CriticalDamage.get())/100

    answer = manyworlds(int(level.get()), atkmin, atkmax, Accuracy, skill.get(), skill_percent, luk, weapon_attack,
                        revenue_status.get(), sortoptions.get(), Magic, Int, Spell_Mastery,
                        Spell_Attack, critical_check, critical_chance, critical_damage)
    target = []
    EPHordered = []
    PPHordered = []
    Averagehits = []
    RevenuePerHit = []
    for k in range(0, shown_results):
        monsterNumber = answer.monsterDict[answer.monsterStats[k][0]]
        target.append(mobData[monsterNumber]['info']['name'])
        EPHordered.append(answer.monsterStats[k][1])
        PPHordered.append(answer.monsterStats[k][2])
        Averagehits.append(answer.monsterStats[k][3])
        if revenue_status.get() == 1:
            RevenuePerHit.append(answer.monsterStats[k][4])
    output.delete('0.0', 'end')
    output.insert(0.0, 'Your Hit List:\n')

    if revenue_status.get() == 1:
        t = PrettyTable(['Rank', 'Mob', 'Exp/Hit', '%/Hit', 'Hits/Kill', 'Mesos/Hit'])
        for k in range(0, shown_results):
            rank = k + 1
            t.add_row([rank, target[k], round(EPHordered[k], 2), round(PPHordered[k], 3), round(Averagehits[k], 3), round(RevenuePerHit[k], 3)])

        output.insert('end', t)
    else:
        t = PrettyTable(['Rank', 'Mob', 'Exp/Hit', '%/Hit', 'Hits/Kill'])
        for k in range(0, shown_results):
            rank = k + 1
            t.add_row([rank, target[k], round(EPHordered[k], 2), round(PPHordered[k], 3), round(Averagehits[k], 3)])

        output.insert('end', t)


'''
    class results:
        def __init__(self, monsterDict, monsterIndex, expPerHit):
            self.monsterDict=monsterDict
            self.monsterIndex=monsterIndex
            self.expPerHit=expPerHit
    '''

submit = tk.Button(submitframe, text='Submit', command=lambda: getresults(int(sortnumber.get())))
submit.pack()

outputframe = tk.Frame(root, height=10, width=10)
outputframe.pack(side='bottom')
output = tk.Text(outputframe)
output.pack(side='bottom')


root.mainloop()
