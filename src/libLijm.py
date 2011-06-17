
import os
from xml.dom import minidom

def bestandVerwerkExtractPad(log, pad, bagObjecten, appyield=None):
    verwerkteBestanden = 0
    # Loop door alle bestanden binnen de gekozen directory en verwerk deze
    for (root, subdirectories, files) in os.walk(pad):
        for subdirectoryNaam in subdirectories:
            # Sla de mutatiebestanden over in deze verwerking. Deze zijn
            # herkenbaar aan de aanduiding MUT in de naam.
            if not "MUT" in subdirectoryNaam:
                subdirectory = os.path.join(root, subdirectoryNaam)
                log(subdirectory)
                for xmlFileNaam in os.listdir(subdirectory):
                    if xmlFileNaam == ".":
                        break
                    (naam,extensie) = os.path.splitext(xmlFileNaam)
                    if extensie.upper() == ".XML":
                        xmlFile = os.path.join(subdirectory, xmlFileNaam)
                        log(xmlFileNaam + "...")
                        log.startTimer()
                        
                        try:
                            xml = minidom.parse(xmlFile)
                            teller = 0
                            for bagObject in bagObjecten:
                                for xmlObject in xml.getElementsByTagName(bagObject.tag()):
                                    bagObject.leesUitXML(xmlObject)
                                    bagObject.voegToeInDatabase()
                                    teller += 1
                                    if appyield is not None:
                                        appyield.Yield(True)
                            log.schrijfTimer("=> %d objecten toegevoegd" %(teller))
                            xml.unlink()
                            verwerkteBestanden += 1
                        except Exception, foutmelding:
                            log("*** FOUT *** Fout in verwerking xml-bestand '%s':\n %s" %(xmlFileNaam, foutmelding))
                log("")
        return verwerkteBestanden

def bestandVerwerkMutatiePad(log, pad, appyield=None):
    verwerkteBestanden = 0
    wWPL = 0
    wOPR = 0
    wNUM = 0
    wLIG = 0
    wSTA = 0
    wVBO = 0
    wPND = 0
    nWPL = 0
    nOPR = 0
    nNUM = 0
    nLIG = 0
    nSTA = 0
    nVBO = 0
    nPND = 0
    tellerFout = 0
    # Loop door alle mutatiebestanden binnen de gekozen directory en verwerk deze
    for (root, subdirectories, files) in os.walk(pad):
        for subdirectoryNaam in subdirectories:
            # De mutatiebestanden zijn herkenbaar aan de aanduiding MUT in de naam
            if "MUT" in subdirectoryNaam:
                subdirectory = os.path.join(root, subdirectoryNaam)
                log(subdirectory)
                for xmlFileNaam in os.listdir(subdirectory):
                    if xmlFileNaam == ".":
                        break
                    (naam,extensie) = os.path.splitext(xmlFileNaam)
                    if extensie.upper() == ".XML":
                        xmlFile = os.path.join(subdirectory, xmlFileNaam)
                        log(xmlFileNaam + "...")
                        log.startTimer()
                        
                        try:
                            xml = minidom.parse(xmlFile)
                            tellerNieuw  = 0
                            tellerWijzig = 0
                            for xmlMutatie in xml.getElementsByTagName("product_LVC:Mutatie-product"):
                                xmlObjectType = xmlMutatie.getElementsByTagName("product_LVC:ObjectType")
                                if len(xmlObjectType) > 0:
                                    bagObjectOrigineel = getBAGobjectBijType(getText(xmlObjectType[0].childNodes))
                                    bagObjectWijziging = getBAGobjectBijType(getText(xmlObjectType[0].childNodes))
                                    bagObjectNieuw     = getBAGobjectBijType(getText(xmlObjectType[0].childNodes))

                                    xmlOrigineel = xmlMutatie.getElementsByTagName("product_LVC:Origineel")
                                    xmlWijziging = xmlMutatie.getElementsByTagName("product_LVC:Wijziging")
                                    xmlNieuw     = xmlMutatie.getElementsByTagName("product_LVC:Nieuw")
                                    if len(xmlOrigineel) > 0 and bagObjectOrigineel and len(xmlWijziging) > 0 and bagObjectWijziging:
                                        bagObjectOrigineel.leesUitXML(xmlOrigineel[0].getElementsByTagName(bagObjectOrigineel.tag())[0])
                                        bagObjectWijziging.leesUitXML(xmlWijziging[0].getElementsByTagName(bagObjectWijziging.tag())[0])
                                        bagObjectOrigineel.wijzigInDatabase(bagObjectWijziging)
                                        tellerWijzig += 1
                                        if bagObjectOrigineel.objectType() == "WPL":
                                            wWPL += 1
                                        if bagObjectOrigineel.objectType() == "OPR":
                                            wOPR += 1
                                        if bagObjectOrigineel.objectType() == "NUM":
                                            wNUM += 1
                                        if bagObjectOrigineel.objectType() == "LIG":
                                            wLIG += 1
                                        if bagObjectOrigineel.objectType() == "STA":
                                            wSTA += 1
                                        if bagObjectOrigineel.objectType() == "VBO":
                                            wVBO += 1
                                        if bagObjectOrigineel.objectType() == "PND":
                                            wPND += 1
                                    if len(xmlNieuw) > 0:
                                        bagObjectNieuw.leesUitXML(xmlNieuw[0].getElementsByTagName(bagObjectNieuw.tag())[0])
                                        bagObjectNieuw.voegToeInDatabase()
                                        #bagObjectNieuw.controleerLevenscyclus(toonResultaat=True)
                                        #if not bagObjectNieuw.levenscyclusCorrect:
                                        #    tellerFout += 1
                                        tellerNieuw += 1
                                        if bagObjectNieuw.objectType() == "WPL":
                                            nWPL += 1
                                        if bagObjectNieuw.objectType() == "OPR":
                                            nOPR += 1
                                        if bagObjectNieuw.objectType() == "NUM":
                                            nNUM += 1
                                        if bagObjectNieuw.objectType() == "LIG":
                                            nLIG += 1
                                        if bagObjectNieuw.objectType() == "STA":
                                            nSTA += 1
                                        if bagObjectNieuw.objectType() == "VBO":
                                            nVBO += 1
                                        if bagObjectNieuw.objectType() == "PND":
                                            nPND += 1
                                if appyield is not None:
                                    appyield.Yield(True)
                            log.schrijfTimer("=> %d objecten toegevoegd, %d objecten gewijzigd" %(tellerNieuw, tellerWijzig))
                            xml.unlink()
                            verwerkteBestanden += 1
                        except Exception, foutmelding:
                            log("*** FOUT *** Fout in verwerking xml-bestand '%s':\n %s" %(xmlFileNaam, foutmelding))
                log("")

def dbInit(bagObjecten):
    for bagObject in bagObjecten:
        bagObject.maakTabel()
        bagObject.maakIndex()
        bagObject.maakViews()
    
def dbMaakIndex(bagObjecten):
    for bagObject in bagObjecten:
        bagObject.maakIndex()

