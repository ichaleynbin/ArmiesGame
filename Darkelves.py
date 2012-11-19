#! /usr/bin/env python
import BRB
import units
import random

def Khainite(Model):
    setattr(Model,'Khainite',1)
    return Model;

def BuildModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Points):
    BRB.BuildModel(unitList,Mov,WepS,BalS,Str,Tuf,Wnd,ini,ata,Led,Armr,Ward,Points)
    setattr(unitList[-1],'EternalHatred')
    setattr(unitList[-1],'Hatred')


