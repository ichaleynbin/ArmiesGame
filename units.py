#! /usr/bin/env python
from warhammer import ward,armor,wound,hit
import random
import BRB

class BeastmenModel():
    pass

class LizardmenModel():
    def __init__(self):
        setattr(self,"ColdBlooded",1)

def NewModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Lizard):
    if Lizard == 1:
        NewMod = LizardmenModel()
    else:
        NewMod = BeastmenModel()
    unitList.append(NewMod)
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


def fillunits(unitList1,unitList2):
    unitList1.append(6)
    unitList2.append(10)
    NewModel(unitList1,4,6,0,5,5,3,4,5,8,3,0,1)
    NewModel(unitList2,5,6,3,5,5,3,5,4,9,0,0,0)
    for x in range(101):
        NewModel(unitList2,5,4,3,3,4,1,3,1,7,0,0,0)
    for x in range(50):
        NewModel(unitList1,4,3,0,4,4,1,1,2,8,3,1,1)
    return unitList1, unitList2;

def RemoveFear(UnitList):
    if hasattr(UnitList[0],'Terror'):
        delattr(UnitList[0],'Terror')
    if hasattr(UnitList[0],'Fear'):
        delattr(UnitList[0],'Fear')

def SetFear(UnitList):
    for x in range(1,len(UnitList)):
        if hasattr(UnitList[x],'Fear') and not(hasattr(UnitList[0],'Terror')) and not(hasattr(UnitList[0],'Fear')):
            setattr(UnitList[0],'Fear',1)
        if hasattr(UnitList[x],'Terror') and not(hasattr(UnitList[0],'Terror')) and not(hasattr(UnitList[0],'Fear')):
            setattr(UnitList[0],'Terror',1)

def FearCheck(UnitList1,UnitList2):
    if hasattr(UnitList1[0],'Terror') and not hasattr(UnitList2[0],'Terror'):
        return 1;
    if hasattr(UnitList1[0],'Fear') and not hasattr(UnitList2[0],'Terror') and not hasattr(UnitList2[0],'Fear'):
        return 1;
    return 0;

def Feartest(UnitListA,UnitListB,verbose):
    RemoveFear(UnitListA)
    RemoveFear(UnitListB)
    SetFear(UnitListA)
    SetFear(UnitListB)
    if FearCheck(UnitListA,UnitListB):
        if verbose >=4:
            print "Army Two must Fear Test!"
        if BRB.breaktest(UnitListB,0,verbose):
            if verbose >=4:
                print "Fear Test Passed!"
        else:
            BRB.runaway(UnitListB,UnitListA,verbose)
            if verbose >=4:
                print "Fear Test Failed!"
    if FearCheck(UnitListB,UnitListA):
        if verbose >=4:
            print "Army One must Fear Test!"
        if BRB.breaktest(UnitListA,0,verbose):
            if verbose >=4:
                print "Fear Test Passed!"
        else:
            BRB.runaway(UnitListA,UnitListB,verbose)
            if verbose >=4:
                print "Fear Test Failed!"

def deathbattle(UnitListA,UnitListB,verbose):
    while len(UnitListA) > 1 and len(UnitListB) > 1:
        Feartest(UnitListA,UnitListB,verbose)
        CombatRes = BRB.combatround(UnitListA,UnitListB,verbose) 
        rankbonus1 = 3 if (len(UnitListA) - 1) / UnitListA[0].Width > 3 else (len(UnitListA) - 1) / UnitListA[0].Width
        rankbonus2 = 3 if (len(UnitListB) - 1) / UnitListB[0].Width > 3 else (len(UnitListB) - 1) / UnitListB[0].Width
        CombatRes += rankbonus1 - rankbonus2
        if CombatRes > 0:
            if verbose >= 2:
                print "Army One won that round of combat by %i!"  %(CombatRes)
            if len(UnitListB) > 1 and len(UnitListA) > 1 and len(UnitListB)/UnitListB[0].Width <= len(UnitListA)/UnitListA[0].Width:
                if BRB.breaktest(UnitListB,CombatRes,verbose) == 0:
                    BRB.runaway(UnitListB,UnitListA,verbose)
        elif CombatRes < 0:
            CombatRes = abs(CombatRes)
            if verbose >= 2:
                print "Army two won that round of combat by %i!" %(CombatRes)
            if len(UnitListA) >  1 and len(UnitListB) > 1 and len(UnitListA)/UnitListA[0].Width <= len(UnitListB)/UnitListB[0].Width:
                if BRB.breaktest(UnitListA,CombatRes,verbose) == 0:
                    BRB.runaway(UnitListA,UnitListB,verbose)
        else:
            if verbose >= 2:
                print "Combat was a tie!"
    if len(UnitListA) == 1:
        if verbose >= 1:
            print "Army Two wins with %i Models Remaining!" %(len(UnitListB)-1)
        return len(UnitListB)-1
    elif len(UnitListB) == 1:
        if verbose >= 1:
            print "Army One wins with %i Models Remaining!" %(len(UnitListA)-1)
        return -(len(UnitListA)-1)

def manybattles(sims,verbose):
    total = 0
    for x in range(sims):
        fillunits(UnitListOne,UnitListTwo)
        total += deathbattle(UnitListOne,UnitListTwo,verbose)
    return total/float(sims)

#print manybattles(5000,0)
