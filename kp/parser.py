import re

#if string looks like 0 @I...@ INDI we get ID of a person from it
def getID(line):
    ID = re.search(r"^0\s+@I(\d+)@\s+INDI$", line)
    if ID is not None:
        return ID.group(1)

#if string looks like 1 NAME <first name> /<last name>/ we get name and surname
#of a person from it
def getName(line):
    Name = re.search(r"^1\s+NAME\s+(\w+)\s+/(\w+)/$", line)
    if Name is not None:
        return Name.group(1) + " " + Name.group(2)

if __name__ == '__main__':
    data = []
    output = open("db.pl", "w")
    #creating a list of string from input file
    with open("file.ged") as input:
        data = [row.strip() for row in input]
    indexes = list(filter(None, map(getID, data)))
    names = list(filter(None, map(getName, data)))
    #creating a dictionary which stores pairs "ID - first name, last name"
    persons = dict(zip(indexes, names))
    fatherPredicate = []
    motherPredicate = []
    for line in data:
        #since some families can lack father or mother we have to make sure
        #that we won't use father or mother from previous family
        newFam = re.search(r"^0\s+@F(\d+)@\s+FAM$", line)
        if newFam is not None:
            father = None
            mother = None
            continue
        #if father is present store his name
        fatherID = re.search(r"1\s+HUSB\s+@I(\d+)@", line)
        if fatherID is not None:
            father = persons[fatherID.group(1)]
            continue
        #if mother is present store her name 
        motherID = re.search(r"1\s+WIFE\s+@I(\d+)@", line)
        if motherID is not None:
            mother = persons[motherID.group(1)]
            continue
        #getting child name
        childID = re.search(r"1\s+CHIL\s+@I(\d+)@", line)
        if childID is not None:
            #if father is present add father predicate
            if father is not None:
                withFather = (father, persons[childID.group(1)])
                fatherPredicate.append(withFather)
            #if mother is present add mother predicate    
            if mother is not None:    
                withMother = (mother, persons[childID.group(1)])
                motherPredicate.append(withMother)
            continue
    #constructing predicates and printing them    
    for predicate in fatherPredicate:
        father, child = predicate
        output.write("father({}, {}).\n".format(father, child))
    output.write('\n')    
    for predicate in motherPredicate:
        mother, child = predicate
        output.write("mother({}, {}).\n".format(mother, child))
    output.close()
