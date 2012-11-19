#! /usr/bin/env python
import random

def hit(attacks,attackerWS,defenderWS,verbose):
    rolls = [random.randint(1,6) for x in range(attacks)]
    if verbose >= 4:
        print "To Hit Rolls:", rolls
    if -attackerWS <= attackerWS-defenderWS <= 0:
        attackpass = 4
    elif attackerWS > defenderWS:
        attackpass = 3
    else:
        attackpass = 5
    poplist = [x for x in range(len(rolls)) if rolls[x] < attackpass]
    for x in range(len(poplist)):
        rolls.pop(poplist[len(poplist)-x-1])
    hits = len(rolls)
    return hits,rolls;

def wound(hits,attackerSTR,defenderTUF,verbose):
    rolls = [random.randint(1,6) for x in range(hits)]
    if verbose >= 4:
        print "To Wound Rolls:", rolls
    woundpass = 4 - attackerSTR + defenderTUF
    if woundpass < 2:
        woundpass = 2
    if woundpass > 6:
        woundpass = 6
    poplist = [x for x in range(len(rolls)) if rolls[x] < woundpass]
    for x in range(len(poplist)):
        rolls.pop(poplist[len(poplist)-x-1])
    wounds = len(rolls)
    return wounds;

def armor(wounds,attackerSTR,defenderARM,verbose):
    if attackerSTR > 3: 
        defenderARM -= (attackerSTR - 3)
    if defenderARM > 0:
        rolls = [random.randint(1,6) for x in range(wounds)]
        if verbose >= 4:
            print "Armor Save Rolls:", rolls
        poplist = [x for x in range(len(rolls)) if rolls[x] >= (7 - defenderARM)]
        for x in range(len(poplist)):
            rolls.pop(poplist[len(poplist)-x-1])
        return len(rolls)
    else:
        return wounds;

def ward(wounds,wardsave,verbose):
    if wardsave > 0:
        rolls = [random.randint(1,6) for x in range(wounds)]
        if verbose >= 4:
            print "Ward Save Rolls:", rolls
        poplist = [x for x in range(len(rolls)) if rolls[x] >= (7-wardsave)]
        for x in range(len(poplist)):
            rolls.pop(poplist[len(poplist)-x-1])
        return len(rolls);
    else:
        return wounds;

def hatred(attacks,attackerWS,defenderWS,verbose):
    firstround = hit(attacks,attackerWS,defenderWS)
    if firstround < attacks:
        if verbose >= 4:
            print "Reroll missed to-hits."
        firstround += hit(attacks-firstround,attackerWS,defenderWS)
    return firstround;
    
def oneroll():
    print "\nBegin Inputting Data now!\n"
    ATTacks = int(raw_input("Attacks? "))
    hater = raw_input("Does Attacker Have Hatred? (y/n) ")
    attackws = int(raw_input("Attackers Weapon Skill? "))
    defws = int(raw_input("Defenders Weapon skill? "))
    atackstr = int(raw_input("Attackers Strength? "))
    deftuf = int(raw_input("Defenders Toughness? "))
    defarmr = int(raw_input("Defenders Armor pieces? "))
    defward = int(raw_input("Defenders Ward Save Pieces? "))

    print "\nRolling the dice now!"
    if hater == "n":
        Hits = hit(ATTacks,attackws,defws,1)
    else:
        Hits = hatred(ATTacks,attackws,defws,1)
    Wounds = wound(Hits,atackstr,deftuf,1)
    Wounds2 = armor(Wounds,atackstr,defarmr,1)
    Wounds3 = ward(Wounds2,defward,1)
    print "\nResults!\n"+ str(ATTacks) + " Attacks resulted in " + str(Hits) + " Hits, which resulted in " + str(Wounds) + " Wounds."
    if Wounds3 != Wounds:
        print "After Armor save, " + str(Wounds2) + " Wounds remain. After Ward Save, " + str(Wounds3) + " Wounds will be taken!\n"
    else:
        print "No saves were made! Take " + str(Wounds3) + " Wounds!"
