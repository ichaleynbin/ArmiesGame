#! /usr/bin/env python
import units
import BRB
import Lizardmen

def initializearmies(UnitList1,UnitList2):
    Lizardmen.SaurusWarrior(UnitList1,32,1,1,1,0)
    Lizardmen.SaurusOldblood(UnitList2,2,1,1,2)
    return UnitList1,UnitList2;

sims = 5000
total = 0
totalMargin1 = 0
totalMargin2 = 0
for x in range(sims):
    UnitList1 = [BRB.Unit()]
    UnitList1[0].Width = 8
    UnitList2 = [BRB.Unit()]
    UnitList2[0].Width = 2
    UnitList1,UnitList2 = initializearmies(UnitList1,UnitList2)
    margin = units.deathbattle(UnitList1,UnitList2,0)
    if margin < 0:
        total -= 1
        totalMargin1 += 1.0*margin
    else:
        total += 1
        totalMargin2 += 1.0*margin
if total < 0:
    base = (sims + total)/ (sims*.02)
    print "Army One won %f percent of the time; Army Two won %f percent." %((base+(abs(total)/(sims/100.0))),base)
else:
    base = (sims - total)/ (sims*.02)
    print "Army One won %f percent of the time; Army Two won %f percent." %(base,(base+(total/(sims/100.0))))
print "Average Units Left was %f for Army One and %f for Army Two" %(abs(totalMargin1/sims),abs(totalMargin2/sims))
