import actionsDB as db
import mainDB

d = mainDB.Database().db
for c in d.collection_names():
    d.drop_collection(c)

"""for i in range(1, 10):
    n = {"description" : "a" * i}
    db.insertAction("n_" + str(i), n)

for f in db.getActions():
    print f

db.updateAvailability("n_1", "b")
db.updateAvailability("n_2", "b")
db.updateAvailability("n_3", "b")
db.updateAvailability("n_5", "b")
db.updateAvailability("n_6", "c")
db.updateAvailability("n_7", "c")
db.updateAvailability("n_2", "c")
db.updateAvailability("n_1", "f")
db.updateAvailability("n_2", "f")
db.updateAvailability("n_3", "f")
db.updateAvailability("n_4", "f")

for i in range(1, 10):
    print str(i) + "\t" + str(db.getAvailability("n_" + str(i)))

db.removeNodeAV("b")

for i in range(1, 10):
    print str(i) + "\t" + str(db.getAvailability("n_" + str(i)))

print db.availableActionName("n_6")

db.deleteAction("n_6")

print db.availableActionName("n_6")

for f in db.getActions():
    print f"""