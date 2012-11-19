#! /usr/bin/env python
from warhammer import ward,armor,wound,hit
import random
import Lizardmen


####        CLASSES

class Model(object):
    def __init__(self):
        pass

class Unit(object):
    def __init__(self):
        pass

####        SPECIAL RULE APPLICATION METHODS

def BuildModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Points):
    unitList.append(Model())
    setattr(unitList[-1],'Movement',Mov)
    setattr(unitList[-1],'WeaponSkill',WepS)
    setattr(unitList[-1],'BallisticSkill',BalS)
    setattr(unitList[-1],'Strength',Str)
    setattr(unitList[-1],'Toughness',Tuf)
    setattr(unitList[-1],'Wounds',Wnd)
    setattr(unitList[-1],'Initiative',ini)
    setattr(unitList[-1],'Attacks',ata)
    setattr(unitList[-1],'Leadership',Led)
    setattr(unitList[-1],'ArmorPts',Armr)
    setattr(unitList[-1],'WardPts',Ward)
    setattr(unitList[-1],'Points',Points)
    return unitList[-1];

def Regenerate(Model,Points):
    pass

def ASL(Model,Points):
    setattr(Model,'ASL',1)
    Model.Points += Points
    return Model;

def Skirmishers(Model,Points):
    setattr(Model,'Skirmishers',1)
    Model.Points += Points
    return Model;

def Handweapon(Model,Points):
    setattr(Model,'HandWeapon',1)
    Model.Points += Points
    return Model;

def Shield(Model,Points):
    setattr(Model,'Shield',1)
    Model.ArmorPts += 1
    if Model.WardPts == 0:
        Model.WardPts = 1
    Model.Points += Points
    return Model;

def Spear(Model,Points):
    setattr(Model,'Spears',1)
    Model.Points += Points
    return Model;

def Champion(Model,Points):
    setattr(Model,'Champion',1)
    Model.Points += Points 

def Musician(Model,Points):
    setattr(Model,'Musician',1)
    Model.Points += Points
    return Model;

def Standard(Model,Points):
    setattr(Model,'Standard',1)
    Model.Points += Points
    return Model;

def Javelin(Model,Points):
    setattr(Model,'Javelin',1)
    Model.Points += Points
    return Model;

def GreatWeapon(Model,Points):
    setattr(Model,'GreatWeapon',1)
    Model.Points += Points
    Model.Strength += 2
    ASL(Model,0)
    return Model;

def AHW(Model,Points):
    setattr(Model,'AHW',1)
    Model.Points += Points
    return Model;

def Halberd(Model,Points):
    setattr(Model,'Halberd',1)
    Model.Points += Points
    return Model;

def LA(Model,Points):
    setattr(Model,'LA',1)
    Model.ArmorPts += 1
    Model.Points += Points
    return Model;

def Fear(Model,Points):
    setattr(Model,'Fear',1)
    Model.Points += Points
    return Model;

def Stupidity(Model,Points):
    setattr(Model,'Stupidity',1)
    Model.Points += Points
    return Model;

def Terror(Model,Points):
    setattr(Model,'Terror',1)
    Model.Points += Points
    return Model;

def Monster(Model,Points):
    Terror(Model,0)
    setattr(Model,'Monster',1)
    setattr(Model,'ThunderStomp',1)
    return Model;    

####        MOUNTS

def Cavalry(Rider,Mount,ThickSkinned,Points):
    setattr(Rider,'Mounted',1)
    setattr(Mount,'Mount',1)
    if ThickSkinned == 1:
        Rider.ArmorPts += 2
    else:
        Rider.ArmorPts += 1
    Rider.Points += Points
    return Rider,Mount;

def MonsterMount(Rider,Mount,Points):
    setattr(Rider,'MonsterMounted',1)
    setattr(Mount,'MonsterMount',1)
    Monster(Mount,0)
    Cavalry(Rider,Mount,0,Points)
    delattr(Mount,'Mount')
    return Rider,Mount;

def ColdOne(Unit,Points):
    Mountee = Unit.pop()
    Lizardmen.BuildModel(UnitList,7,3,0,4,4,1,2,1,3,2,0,0)
    setattr(Mount,'ColdOne',1)
    Stupidity(Fear(Mount,0),0)
    Cavalry(Mountee,Mount,1,Points)
    UnitList.append(Mountee)

####        MOVEMENT RULES

def Charge(UnitList,distance,dice,verbose):
    dicerolls = [random.randint(1,6) for x in range(dice)]
    Chargedist = sum(dicerolls) + UnitList[1].Movement
    if Chargedist < distance:
        if verbose >= 4:
            print "Charge Failed!"
        distance -= max(dicerolls)
    else:
        if verbose >= 4:
            print "Charge Made!"
        distance = 0
    return distance;

def flee(UnitList1,UnitList2,Chargedist,distance,verbose):
    distance1 = random.randint(1,6) + random.randint(1,6)
    distance2 = random.randint(1,6) + random.randint(1,6) + Chargedist
    if verbose >= 4:
        print "Attempting to flee! Ran a distance of " + str(distance1) + ". Pursuers ran "+str(distance2)+". Initial Separation distance was %i." %distance
    return (distance1 + distance - distance2);

def breaktest(UnitList,CombatRes,verbose):
    if hasattr(UnitList[1],"ColdBlooded"):
        rollList = [random.randint(1,6) for x in range(3)]
        rollList.sort()
        rolls = sum(rollList[0:2])
        if verbose >= 4:
            print "Cold Blooded Break Test Roll on Modifier -%i!" %CombatRes, rollList, rolls
    else:
        rolls = random.randint(1,6) + random.randint(1,6) 
        if verbose >= 4:
            print "Break Test Roll total on Modifier -%i!" %CombatRes, rolls 
    if rolls == 2:
        if verbose >= 3:
            print "Leadership Test Passed!"
        return 1;
    rolls += (0 if hasattr(UnitList[1],"Stubborn") else CombatRes)
    if rolls > max([UnitList[x].Leadership for x in range(1,len(UnitList))]):
        if verbose >= 3:
            print "Leadership Test Failed!"
        return 0;
    else:
        if verbose >= 3:
            print "Leadership Test Passed!"
        return 1;

def runaway(UnitListFlee,UnitListPursue,verbose):
    distance = flee(UnitListFlee,UnitListPursue,0,0,verbose)
    stand = 0      
    while stand == 0:  
        if distance <= 0:
            for x in range(len(UnitListFlee)-1):
                UnitListFlee.pop()
            if verbose >= 2:
                print "Unit was cut down in flight!"
            return; 4893122
        else:
            stand = breaktest(UnitListFlee,0,verbose)
            if stand == 1 and verbose >= 2:
                print "Unit Rallied!"
            if stand == 0:
                distance = flee(UnitListFlee,UnitListPursue,UnitListPursue[1].Movement,distance,verbose)

####        MELEE COMBAT SECTION

def BreathRanged():
    pass

def BreathMelee():
    pass

def PoisonedAttacks(AttackUnit,DefenseModel,AttackingModelsList,x,verbose):
    if x <AttackUnit[0].Width:
        Hits,ToHitRolls = hit(AttackUnit[AttackingModelsList[x]].Attacks,AttackUnit[AttackingModelsList[x]].WeaponSkill,DefenseModel.WeaponSkill,verbose)
        for y in range(Hits):
            if ToHitRolls[y] == 6:
                if verbose >=4:
                    print "Poisoned Attack Landed! Automatic Wound!"
                kills += ward(armor(1,AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
            else:
                kills += ward(armor(wound(1,AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.Toughness,verbose),AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
    else:
        Hits,ToHitRolls = hit(1,AttackUnit[AttackingModelsList[x]].WeaponSkill,DefenseModel.WeaponSkill,verbose)
        for y in range(Hits):
            if ToHitRolls[y] == 6:
                kills += ward(armor(1,AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
            else:
                kills += ward(armor(wound(1,AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.Toughness,verbose),AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)

def CarnosaurAttacks(AttackUnit,DefenseModel,AttackingModelsList,x,verbose):
    wounds = ward(armor(wound(hit(AttackUnit[AttackingModelsList[x]].Attacks,AttackUnit[AttackingModelsList[x]].WeaponSkill,DefenseModel.WeaponSkill,verbose)[0],AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.Toughness,verbose),AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
    if wounds > 0 and not hasattr(AttackUnit[AttackingModelsList[x]],'Frenzy'):
        setattr(AttackUnit[AttackingModelsList[x]],'Frenzy',2)
        AttackUnit[AttackingModelsList[x]].Attacks += 1
    kills = 0
    for x in range(wounds):
        kills += random.randint(1,3)
    if verbose >= 3:
        print kills, "Carnosaur Wounds Total"
    return kills;    

def attack(AttackUnit,DefenseModel,AttackingModelsList,verbose):
    kills = 0
    for x in range(len(AttackingModelsList)):
        if hasattr(AttackUnit[AttackingModelsList[x]],'JunglePoisons') or hasattr(AttackUnit[AttackingModelsList[x]],'PoisonedAttacks'):
            kills += PoisonedAttacks(AttackUnit,DefenseModel,AttackingModelsList,x,verbose)
        elif hasattr(AttackUnit[AttackingModelsList[x]],'Blood-frenzy') and hasattr(AttackUnit[AttackingModelsList[x]],'UltimatePredator'):
            kills += CarnosaurAttacks(AttackUnit,DefenseModel,AttackingModelsList,x,verbose)
        else:
            if x <AttackUnit[0].Width:
                kills += ward(armor(wound(hit(AttackUnit[AttackingModelsList[x]].Attacks,AttackUnit[AttackingModelsList[x]].WeaponSkill,DefenseModel.WeaponSkill,verbose)[0],AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.Toughness,verbose),AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
            else:
                kills += ward(armor(wound(hit(1,AttackUnit[AttackingModelsList[x]].WeaponSkill,DefenseModel.WeaponSkill,verbose)[0],AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.Toughness,verbose),AttackUnit[AttackingModelsList[x]].Strength,DefenseModel.ArmorPts,verbose),DefenseModel.WardPts,verbose)
    if verbose >= 3:
        print kills, "Wounds Total"
    return kills;

def inicheck(UnitList1,UnitList2):
    inilist = []
    for x in range(1,len(UnitList1)):
        if not UnitList1[x].Initiative in inilist:
            inilist.append(UnitList1[x].Initiative)
    for x in range(1,len(UnitList2)):
        if not UnitList2[x].Initiative in inilist:
            inilist.append(UnitList2[x].Initiative)
    inilist.sort()
    inilist.reverse()
    return inilist;

def takewounds(UnitList,Wounds):
    for y in range(Wounds):
        if len(UnitList) >= 2:
            if UnitList[-1].Wounds > 1:
                UnitList[-1].Wounds -= 1
            else:
                Model = UnitList.pop()
                if hasattr(Model,'Mounted') and hasattr(UnitList[1],'Mount'):
                    UnitList.pop()
    return Wounds;

def Stomp(UnitList1,UnitList2,roundwnds1,roundwnds2,verbose):
    if len(UnitList2) > 1:
        for x in range(1,len(UnitList1)):
            if hasattr(UnitList1[x],'Stomp'):
                roundwnds2 += ward(armor(wound(1,UnitList1[x].Strength,UnitList2[-1].Toughness,verbose),UnitList1[x].Strength,UnitList2[-1].ArmorPts,verbose),UnitList2[-1].WardPts,verbose)
            elif hasattr(UnitList1[x],'ThunderStomp'):
                roundwnds2 += ward(armor(wound(random.randint(1,6),UnitList1[x].Strength,UnitList2[-1].Toughness,verbose),UnitList1[x].Strength,UnitList2[-1].ArmorPts,verbose),UnitList2[-1].WardPts,verbose)
    if len(UnitList1) > 1:
        for x in range(1,len(UnitList2)):
            if hasattr(UnitList2[x],'Stomp'):
                roundwnds1 += ward(armor(wound(1,UnitList2[x].Strength,UnitList1[-1].Toughness,verbose),UnitList2[x].Strength,UnitList1[-1].ArmorPts,verbose),UnitList1[-1].WardPts,verbose)
            elif hasattr(UnitList2[x],'ThunderStomp'):
                roundwnds1 += ward(armor(wound(random.randint(1,6),UnitList2[x].Strength,UnitList1[-1].Toughness,verbose),UnitList2[x].Strength,UnitList1[-1].ArmorPts,verbose),UnitList1[-1].WardPts,verbose)
    return roundwnds1,roundwnds2;

def combatround(UnitList1,UnitList2,verbose):
    if verbose >= 2:
        print "Start round of combat!\n", "Army One has "+str(len(UnitList1)-1)+" Units left, Army Two has " +str(len(UnitList2)-1) + " left."
    IniList = inicheck(UnitList1,UnitList2)
    roundwndsA = 0
    roundwndsB = 0
    Models1 = 0
    Models2 = 0
    MaxModels1 = 2*UnitList1[0].Width
    MaxModels2 = 2*UnitList2[0].Width
    for x in range(len(IniList)):
        if verbose >= 3: print "Fighting at initiative "+str(x)
        AttackingModelsListA = []
        AttackingModelsListB = []
        AWounds = 0 
        BWounds = 0
        for y in range(1,len(UnitList1)):
            if UnitList1[y].Initiative == IniList[x] and Models1 <MaxModels1:
                AttackingModelsListA.append(y)
                Models1 += 1
        for y in range(1,len(UnitList2)):
            if UnitList2[y].Initiative == IniList[x] and Models2 <MaxModels2:
                AttackingModelsListB.append(y)
                Models2 += 1
        if len(AttackingModelsListA) > 0 and len(UnitList2) > 1:
            if verbose >= 3:
                print "First Army Attacks!"
            BWounds = attack(UnitList1,UnitList2[-1],AttackingModelsListA,verbose)
            roundwndsB += BWounds
        if len(AttackingModelsListB) > 0 and len(UnitList1) > 1:
            if verbose >= 3:
                print "Second Army Attacks!"
            AWounds = attack(UnitList2,UnitList1[-1],AttackingModelsListB,verbose)
            roundwndsA += AWounds
        takewounds(UnitList1,AWounds)
        takewounds(UnitList2,BWounds)
    roundwndsA,roundwndsB = Stomp(UnitList1,UnitList2,roundwndsA,roundwndsB,verbose)
    ARanks = int(len(UnitList1)/UnitList1[0].Width)
    BRanks = int(len(UnitList2)/UnitList2[0].Width)
    combatres = ARanks - BRanks + roundwndsB - roundwndsA
    return combatres;

####        POST COMBAT
