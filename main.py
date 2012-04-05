from itertools import repeat
import random
import csv

class Passenger:
	def __init__(self, row):
		self.wait = 0
		self.row = row
		self.seated = False
		self.waitWhileSeated = 0
		self.totalWait = 0

population = []

#VARIABLES YOU CAN AND SHOULD CHANGE
SIMULATIONITERATIONS = 1000
MEANLOADINGTIME = 1
SDLOADINGTIME = 0.5
MEANWALKINGTIME = 0.02
SDWALKINGTIME = 0.005
rows = 30

#Seats 
seats = [x for x in xrange(0,rows)]
frontDoorSeats = [x for x in xrange(0, rows/2)]
rearDoorSeats = [x for x in xrange((rows/2), rows)]
rearDoorSeats.reverse()


def generatePopulation(rows, cols):
	#generates population
	for i in xrange(0, rows):
		for j in xrange(0, cols):
			passenger = Passenger(i)
			population.append(passenger)

def resetPassengers():
	for i in population:
		i.wait = 0
		i.seated = False
		i.waitWhileSeated = 0
		i.totalWait = 0


def unseatedPassengers(waitTime, queue):
	for passenger in queue:
		if not passenger.seated:
			passenger.wait += waitTime
		else:
			passenger.waitWhileSeated += waitTime
		passenger.totalWait += waitTime

def seated(passenger, row, queue):
	loadingTime = 0
	walkTime = getWalkTime()
	if passenger.row == row:
		passenger.seated = True
		loadingTime = getLoadingTime()
	unseatedPassengers(loadingTime+walkTime, queue)
	if passenger.seated:
		return True
	else:
		return False

def getWalkTime():
	randomWalkTime = abs(random.gauss(MEANWALKINGTIME, SDWALKINGTIME))
	walkTime = randomWalkTime
	return walkTime

def getLoadingTime():
	randomMultiplier = abs(random.gauss(MEANLOADINGTIME, SDLOADINGTIME)) # must be non zero
	loadingTime = randomMultiplier
	return loadingTime

def outputFile(filename, trial = 0):
	f = open(filename, 'a')
	csvWriter = csv.writer(f)
	for passenger in population:
		csvWriter.writerow([trial, passenger.row, passenger.wait, passenger.waitWhileSeated, passenger.totalWait])
	f.close()


def jetStarStyle():
	queue1 = []
	queue2 = []
	for i in population:
		if i.row <= rows/2:
			queue1.append(i)
		else:
			queue2.append(i)
	random.shuffle(queue1)
	random.shuffle(queue2)
	return queue1, queue2

def jetStarLateStyle():
	queue1 = []
	queue2 = []
	queue3 = []
	partition = rows/3

	for i in population:
		if i.row <= partition:
			queue1.append(i)
		elif i.row >= rows - partition:
			queue2.append(i)
		else:
			queue3.append(i)
	random.shuffle(queue1)
	random.shuffle(queue2)
	random.shuffle(queue3)
	return queue1, queue2, queue3

def oddEvenStyle():
	queue1 = []
	queue2 = []
	for i in population:
		if i.row %2 == 0:
			queue1.append(i)
		else:
			queue2.append(i)
	random.shuffle(queue1)
	random.shuffle(queue2)
	return queue1, queue2

def oeSplitStyle():
	queue1 = []
	queue2 = []
	queue3 = []
	queue4 = []
	for i in population:
		if i.row <= rows/2:
			if i.row %2 == 0:
				queue1.append(i)
			else:
				queue2.append(i)
		else:
			if i.row %2 == 0:
				queue3.append(i)
			else:
				queue4.append(i)
	random.shuffle(queue1)
	random.shuffle(queue2)
	random.shuffle(queue3)
	random.shuffle(queue4)
	return queue1, queue2, queue3, queue4


def board(queue, door):
	for passenger in queue:
		for seat in door:
			if seated(passenger, seat, queue):
				continue

def boardingProcess(**kwargs):
	for door, arg in kwargs.items():
		if door == "front":
			board(arg, frontDoorSeats)
		elif door == "back":
			board(arg, rearDoorSeats)
		elif door == "backAll":
			board(arg, reversed(seats))
		else:
			board(arg, seats)


#main simulation - runs for a 1000 times
for i in range(0, SIMULATIONITERATIONS):
	generatePopulation(30, 6)
	q1, q2 = jetStarStyle()
	boardingProcess(front = q1, back = q2)
	outputFile('jetstar1000.csv', i)

	resetPassengers()
	q1, q2 = oddEvenStyle()
	boardingProcess(frontAll = q1, backAll = q2)
	outputFile('oddEvenTwoQueues1000.csv', i)

	resetPassengers()
	q1, q2 = oddEvenStyle()
	frontDoor = q1 + q2
	boardingProcess(frontAll = frontDoor)
	outputFile('oddEven1000.csv', i)

	resetPassengers()
	q1, q2, q3, q4 = oeSplitStyle()
	frontDoor = q1 + q2
	rearDoor = q3 + q4
	boardingProcess(front = frontDoor, back = rearDoor)
	outputFile('oeSplit1000.csv', i)

	resetPassengers()
	q1, q2, q3 = jetStarLateStyle()
	frontDoor = q2 + q1
	boardingProcess(front = frontDoor, back = q3)
	outputFile('jetstarLate1000.csv', i)
	population = []