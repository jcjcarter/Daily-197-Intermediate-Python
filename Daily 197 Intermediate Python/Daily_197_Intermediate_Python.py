class Path:
    def __init__(self, target, times, streetName):
        self.targetNumber = target
        self.targetName = chr(target + 65)
        self.times = times
        self.streetName = streetName

    def getTime(self,currentTime):
        if not currentTime < Time(600) and currentTime < Time(1000):
            return self.times[0]
        elif not currentTime < Time(1000) and currentTime < Time(1500):
            return self.times[1]
        elif not currentTime < Time(1500) and currentTime < Time(1900):
            return self.times[2]
        else:
            return self.times[3]

class Node:
    def __init__(self, number):
        self.number = number
        self.paths = []
        self.reset()

    def addPath(self, path):
        self.paths.append(path)

    def reset(self):
        self.distance = 0
        self.visited = False
        self.route = ""

    def printPathNames(self):
        for path in self.paths:
            print (path.streetName)

class Time:
    def __init__(self,*args):
        if len(args) == 1:
            time = str(args[0])
            self.hour = 0 if time[:-2] == '' else int(time[:-2])
            self.minutes = int(time[-2:])
        else:
            self.hour = args[0]
            self.minutes = args[1]

    def __add__(self,minutes):
        newMinutes = self.minutes + minutes
        outMinutes = newMinutes % 60
        hourIncrement = (newMinutes - self.minutes) / 60
        outHour = (self.hour + hourIncrement) % 24
        return Time(outHour, outMinutes)

    def __lt__(self,time):
        return (self.hour < time.hour or
            (self.hour == time.hour and self.minutes < time.minutes))

    def printTime(self):
        print (str(self.hour) + ":" + str(self.minutes))

def modifiedDijkstra(nodes, start, target, startTime):
    # Dijkstra's algorithm where edge weights are a function of time
    currentNode = start
    nodes[currentNode].route = chr(currentNode + 65)
    while True:
        nodes[currentNode].visited = True
        newTime = startTime + nodes[currentNode].distance
        for path in nodes[currentNode].paths:
            if not nodes[path.targetNumber].visited:
                newDistance = (nodes[currentNode].distance +
                    path.getTime(startTime + nodes[currentNode].distance))
                if (nodes[path.targetNumber].distance == 0 or 
                    newDistance < nodes[path.targetNumber].distance):
                    nodes[path.targetNumber].distance = newDistance
                    nodes[path.targetNumber].route = " ".join(
                        (nodes[currentNode].route,path.targetName,
                        ('('+str(path.getTime(startTime + nodes[currentNode].distance))+')')))
        currentNode = findNextNode(nodes)
        if currentNode == -1:
            print ("\nNo Solution")
            break
        elif currentNode == target:
            print ("\nSolution Found!")
            print ("Route: " + nodes[currentNode].route)
            print ("Distance: " + str(nodes[currentNode].distance))
            break

def findNextNode(nodes):
    lowestDistance = 0
    nextNode = -1
    for node in nodes:
        if not node.visited:
            if (lowestDistance == 0 or 
                (node.distance > 0 and node.distance < lowestDistance)):
                lowestDistance = node.distance
                nextNode = node.number
    return nextNode

def resetNodes(nodes):
    for node in nodes:
        node.reset()

def parseInput(filePath, nodes=[]):
    file = open(filePath,'r')
    for line in file:
        splitLine = line.replace("\"","").split(" ")
        nodeNumber = ord(splitLine[0]) - 65
        targetNumber = ord(splitLine[1]) - 65
        streetName = " ".join(splitLine[2:-4])
        times = splitLine[-4:]
        times = [int(time) for time in times]
        try:
            nodes[nodeNumber].addPath(Path(targetNumber,times,streetName))
        except:
            for i in range(len(nodes),nodeNumber+1):
                nodes.append(Node(i))
            nodes[nodeNumber].addPath(Path(targetNumber,times,streetName))
        try:
            nodes[targetNumber].addPath(Path(nodeNumber,times,streetName))
        except:
            for i in range(len(nodes),targetNumber+1):
                nodes.append(Node(i))
            nodes[targetNumber].addPath(Path(nodeNumber,times,streetName))
    return nodes

def calculatePath(line, nodes):
    print ("\n" + line)
    splitLine = line.split(" ")
    start = ord(splitLine[0])-65
    end = ord(splitLine[1])-65
    startTime = Time(splitLine[2][0:4])
    resetNodes(nodes)
    modifiedDijkstra(nodes,start,end,startTime)

def main():
    filePath = 'Data.txt'
    nodes = parseInput(filePath)
    file = open('input.txt','r')
    for line in file:
        calculatePath(line,nodes)

if __name__ == "__main__":
    main()