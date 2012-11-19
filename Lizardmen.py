#! /usr/bin/env python
import random
import BRB

def Aquatic(Model):
    setattr(Model,'Aquatic',1)
    return Model;

def JunglePoisons(Model):
    setattr(Model,'JunglePoisons',1)
    return Model;

def BuildLizardModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Points):
    BRB.BuildModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Points)
    setattr(unitList[-1],"ColdBlooded",1)
    return unitList[-1];

def Carnosaur(UnitList,Points):
    Rider = UnitList.pop()
    BRB.Terror(BuildLizardModel(UnitList,7,3,0,7,5,5,2,4,5,3,0,Points),0)
    setattr(UnitList[-1],'Blood-frenzy',1)
    setattr(UnitList[-1],'UltimatePredator',1)
    UnitList.append(Rider)
    BRB.MonsterMount(UnitList[-1],UnitList[-2],210)
    return UnitList;

def SaurusWarrior(UnitList,number,Champion,Musician,Standard,spear):
    number2 = number
    if Champion == 1:
        BRB.Champion(BuildLizardModel(UnitList,4,3,0,4,4,1,1,3,8,2,0,11),12)
        number2 -= 1
    if Musician == 1:
        BRB.Musician(BuildLizardModel(UnitList,4,3,0,4,4,1,1,2,8,2,0,11),6)
        number2 -= 1
    if Standard == 1:
        BRB.Standard(BuildLizardModel(UnitList,4,3,0,4,4,1,1,2,8,2,0,11),12)
        number2 -= 1
    for x in range(number2):
        BuildLizardModel(UnitList,4,3,0,4,4,1,1,2,8,2,0,11)
    for x in range(len(UnitList)-number,len(UnitList)):
        BRB.Handweapon(BRB.Shield(UnitList[x],0),0)
        if spear == 1:
            UnitList[x].Points += 1
            Spear(UnitList[x])
        
def Skink(UnitList,number,Champion,Musician,Standard,Kroxigors):
    number2 = number
    if Champion == 1:
        BRB.Champion(BuildLizardModel(UnitList,6,2,3,3,2,1,4,2,6,1,1,5),8)
        number2 -= 1
    if Musician == 1:
        BRB.Musician(BuildLizardModel(UnitList,6,2,3,3,2,1,4,1,6,1,1,5),6)
        number2 -= 1
    if Standard == 1:
        BRB.Standard(BuildLizardModel(UnitList,6,2,3,3,2,1,4,1,6,1,1,5),8)
        number2 -= 1
    if Kroxigors > 0:
        Kroxigor(UnitList,Kroxigors,0,0,0)
    for x in range(number2):
        BuildLizardModel(UnitList,6,2,3,3,2,1,4,1,6,1,1,5)
    for x in range(len(UnitList)-number,len(UnitList)):
        BRB.Handweapon(BRB.Javelin(BRB.Shield(Aquatic(JunglePoisons(UnitList[x])),0),0),0)

def SaurusOldblood(UnitList,Weapon,LA,S,Mount,*args):
    BRB.Handweapon(BuildLizardModel(UnitList,4,6,0,5,5,3,4,5,8,3,0,145),0)
    if Weapon == 1:
        BRB.Spear(UnitList[-1],8)
    elif Weapon == 2:
        BRB.GreatWeapon(UnitList[-1],12)
    elif Weapon == 3:
        BRB.Halberd(UnitList[-1],8)
    elif Weapon == 4:
        BRB.AHW(UnitList[-1],8)
    if LA == 1:
        BRB.LA(UnitList[-1],10)
    if S == 1:
        BRB.Shield(UnitList[-1],6)
    if Mount == 1:
        BRB.ColdOne(UnitList,30)
    elif Mount == 2:
        Carnosaur(UnitList,210)
    for arg in args:
        pass## insert magical items possible to hold here. suspect magical item assignment subroutine appropriate. try: army subroutine calls BRB subroutine.
