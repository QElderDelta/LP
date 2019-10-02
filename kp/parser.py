import re

def getID(line):
    ID = re.search(r"^0\s+@I(\d+)@\s+INDI$", line)
    if ID is not None:
        return ID.group(1)

def getName(line):
    Name = re.search(r"^1\s+NAME\s+(\w+)\s+/(\w+)/$", line)
    if Name is not None:
        return Name.group(1) + " " + Name.group(2)

if __name__ == '__main__':
    data = []
    output = open("db.pl", "w")
    with open("file.ged") as input:
        data = [row.strip() for row in input]
    indexes = list(filter(None, map(getID, data)))
    names = list(filter(None, map(getName, data)))
    persons = dict(zip(indexes, names))
    fatherPredicate = []
    motherPredicate = []
    for line in data:
        newFam = re.search(r"^0\s+@F(\d+)@\s+FAM$", line)
        if newFam is not None:
            father = None
            mother = None
            print("Found")
            continue
        fatherID = re.search(r"1\s+HUSB\s+@I(\d+)@", line)
        if fatherID is not None:
            father = persons[fatherID.group(1)]
            continue
        motherID = re.search(r"1\s+WIFE\s+@I(\d+)@", line)
        if motherID is not None:
            mother = persons[motherID.group(1)]
            continue
        childID = re.search(r"1\s+CHIL\s+@I(\d+)@", line)
        if childID is not None:
            if father is not None:
                withFather = (father, persons[childID.group(1)])
                fatherPredicate.append(withFather)
            if mother is not None:    
                withMother = (mother, persons[childID.group(1)])
                motherPredicate.append(withMother)
            continue
    for predicate in fatherPredicate:
        father, child = predicate
        output.write("father({}, {}).\n".format(father, child))
    output.write('\n')    
    for predicate in motherPredicate:
        mother, child = predicate
        output.write("mother({}, {}).\n".format(mother, child))
    output.close()
