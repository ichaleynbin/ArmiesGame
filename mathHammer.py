#! /usr/bin/env python
import random

def hatred(attacks,attackerWS,defenderWS):
    firstround = hit(attacks,attackerWS,defenderWS)
    if firstround < attacks:
        print "Reroll missed to-hits."
        firstround += hit(attacks-firstround,attackerWS,defenderWS)
    return firstround;

def hit(attacks,attackerWS,defenderWS):
    if -attackerWS <= attackerWS-defenderWS <= 0:
        return attacks/2.0;
    elif attackerWS > defenderWS:
        return attacks*2.0/3;
    else:
        return attacks/3.0;

def wound(hits,attackerSTR,defenderTUF):
    woundpass = 4 - attackerSTR + defenderTUF
    if woundpass < 2:
        woundpass = 2
    if woundpass > 6:
        woundpass = 6
    return hits*(7-woundpass)/6.0;

def armor(wounds,attackerSTR,defenderARM):
    if attackerSTR > 3: 
        defenderARM -= (attackerSTR - 3)
    if defenderARM > 0:
        return wounds*(6-defenderARM)/6.0;
    else:
        return wounds;

def ward(wounds,wardsave):
    if wardsave > 0:
        return wounds*(6-wardsave)/6.0;
    else:
        return wounds;


#print "\nBegin Inputting Data now!\n"
#ATTacks = int(raw_input("Attacks? "))
#hater = raw_input("Does Attacker Have Hatred? (y/n) ")
#attackws = int(raw_input("Attackers Weapon Skill? "))
#defws = int(raw_input("Defenders Weapon skill? "))
#atackstr = int(raw_input("Attackers Strength? "))
#deftuf = int(raw_input("Defenders Toughness? "))
#defarmr = int(raw_input("Defenders Armor pieces? "))
#defward = int(raw_input("Defenders Ward Save Pieces? "))

#print "\nMathematically Calculating Your Result!"
#Hits = hit(ATTacks,attackws,defws)
#if hater == "n":
#    Hits = hit(ATTacks,attackws,defws)
#else:
#    Hits = hatred(ATTacks,attackws,defws)
#Wounds = wound(Hits,atackstr,deftuf)
#Wounds2 = armor(Wounds,atackstr,defarmr)
#Wounds3 = ward(Wounds2,defward)
#print "\nResults!\n"+ str(ATTacks) + " Attacks resulted in " + str(Hits) + " Hits, which resulted in " + str(Wounds) + " Wounds."
#if Wounds3 != Wounds:
#    print "After Armor save, " + str(Wounds2) + " Wounds remain. After Ward Save, " + str(Wounds3) + " Wounds will be taken!\n"
#else:
#    print "No saves were made! Take " + str(Wounds3) + " Wounds!" 
