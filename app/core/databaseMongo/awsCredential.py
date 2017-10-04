from mainDB import db

tab = db.awsCred

def createCred(akID, saID, arn):
    if checkPresence():
        return "Resource already present"
    
    tab.insert_one({"accessKeyID": akID,
                    "secretAccessID": saID,
                    "ARN": arn})
    return "OK"

def deleteCred():
    tab.delete_one({})
    return

def getCred():
    return tab.find_one()

def checkPresence():
    n = tab.find().count()
    return n > 0