"""my_controller controller."""

from asyncio.windows_events import NULL
from turtle import right
from controller import Robot
from PIL import Image
import numpy as np
from entryState import EntryState
from maze_map import MazeMap
import math
from queue import Queue

# create the Robot instance.
robot = Robot()

timestep = int(robot.getBasicTimeStep())

camera = robot.getDevice("camera")
camera.enable(timestep)

compass = robot.getDevice("compass")
compass.enable(timestep)

# initialize wheels
frontLeftWheel = robot.getDevice('front left wheel')
frontRightWheel = robot.getDevice('front right wheel')
backLeftWheel = robot.getDevice('back left wheel')
backRightWheel = robot.getDevice('back right wheel')

# Disable motor PID control mode.
frontLeftWheel.setPosition(float('inf'))
frontRightWheel.setPosition(float('inf'))
backLeftWheel.setPosition(float('inf'))
backRightWheel.setPosition(float('inf'))


# initialize sensors
frontLeftSensor = robot.getDevice('so0')
frontRightSensor = robot.getDevice('so7')
backLeftSensor = robot.getDevice('so15')
backRightSensor = robot.getDevice('so8')
frontLeftMiddleSensor = robot.getDevice('so3')
frontRightMiddleSensor = robot.getDevice('so4')
backLeftMiddleSensor = robot.getDevice('so11')
backRightMiddleSensor = robot.getDevice('so12')

frontLeftSensor.enable(timestep)
frontRightSensor.enable(timestep)
backLeftSensor.enable(timestep)
backRightSensor.enable(timestep)
frontLeftMiddleSensor.enable(timestep)
frontRightMiddleSensor.enable(timestep)
backLeftMiddleSensor.enable(timestep)
backRightMiddleSensor.enable(timestep)

initialVelocity = 5.0
currentVelocity = initialVelocity

imageColorInputQueue = Queue(3)

goalReached = False

# utility functions


def setRobotVelocity(vel):
    frontLeftWheel.setVelocity(vel)
    frontRightWheel.setVelocity(vel)
    backLeftWheel.setVelocity(vel)
    backRightWheel.setVelocity(vel)


def roundBy(x, base=5):
    return base * round(x/base)


def turn(turnDirection, turnSoftly=False):
    if turnDirection == 'right':
        if turnSoftly == True:
            frontRightWheel.setVelocity(-3)
            backRightWheel.setVelocity(-3)
        else:
            frontRightWheel.setVelocity(-initialVelocity)
            backRightWheel.setVelocity(-initialVelocity)
    elif turnDirection == 'left':
        if turnSoftly == True:
            frontLeftWheel.setVelocity(-3)
            backLeftWheel.setVelocity(-3)
        else:
            frontLeftWheel.setVelocity(-initialVelocity)
            backLeftWheel.setVelocity(-initialVelocity)
    elif turnDirection == "around":
        if turnSoftly == True:
            frontLeftWheel.setVelocity(-3)
            backLeftWheel.setVelocity(-3)
        else:
            frontLeftWheel.setVelocity(-initialVelocity)
            backLeftWheel.setVelocity(-initialVelocity)
    else:
        setRobotVelocity(initialVelocity)


def getCameraImageDominantColor():
    global goalReached
    img = camera.getImageArray()
    im = Image.fromarray(np.array(img), mode="RGB")
    im = im.resize((1, 1), resample=0)
    dominant_color = im.getpixel((0, 0))
    imageColorInputQueue.enqueue(dominant_color[0])
    average = sum(imageColorInputQueue.items) / imageColorInputQueue.size()

    if average > 200:
        return "white"
    if round(average) == 0:
        goalReached = True
        return "green"
    return "brown"

# reference: https://www.cyberbotics.com/doc/reference/compass


def getBearingInDegrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[1])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if bearing < 0.0:
        bearing += 360.0
    return bearing


def getDirection(bearing, direction=None):
    if 355 < bearing < 360 or bearing < 5:
        return "east"
    elif 175 < bearing < 185:
        return "west"
    elif 85 < bearing < 95:
        return "north"
    elif 265 < bearing < 275:
        return "south"
    elif direction:
        return direction


def getTargetBearing(direction, turnType=None):
    if direction == "east":
        if turnType == "left":
            return 90
        if turnType == "right":
            return 270
        if turnType == "around":
            return 180
        return 360
    elif direction == "west":
        if turnType == "left":
            return 270
        if turnType == "right":
            return 90
        if turnType == "around":
            return 360
        return 180
    elif direction == "north":
        if turnType == "left":
            return 180
        if turnType == "right":
            return 0
        if turnType == "around":
            return 270
        return 90
    elif direction == "south":
        if turnType == "left":
            return 360
        if turnType == "right":
            return 180
        if turnType == "around":
            return 90
        return 270


def adjustDirection(bearing, targetBearing, direction):
    if targetBearing != None and bearing < targetBearing - 1.5:
        if direction == "west":
            frontLeftWheel.setVelocity(
                frontLeftWheel.getVelocity() - 0.05)
            backLeftWheel.setVelocity(
                backLeftWheel.getVelocity() - 0.05)
        elif direction == "east":
            frontRightWheel.setVelocity(
                frontRightWheel.getVelocity() - 0.05)
            backRightWheel.setVelocity(
                backRightWheel.getVelocity() - 0.05)
        elif direction == "north":
            frontLeftWheel.setVelocity(
                frontLeftWheel.getVelocity() - 0.05)
            backLeftWheel.setVelocity(
                backLeftWheel.getVelocity() - 0.05)
        elif direction == "south":
            frontLeftWheel.setVelocity(
                frontLeftWheel.getVelocity() - 0.05)
            backLeftWheel.setVelocity(
                backLeftWheel.getVelocity() - 0.05)
    elif targetBearing != None and bearing > targetBearing + 1.5:
        if direction == "west":
            frontRightWheel.setVelocity(
                frontRightWheel.getVelocity() - 0.05)
            backRightWheel.setVelocity(
                backRightWheel.getVelocity() - 0.05)
        elif direction == "east":
            frontLeftWheel.setVelocity(
                frontLeftWheel.getVelocity() - 0.05)
            backLeftWheel.setVelocity(
                backLeftWheel.getVelocity() - 0.05)
        elif direction == "north":
            frontRightWheel.setVelocity(
                frontRightWheel.getVelocity() - 0.05)
            backRightWheel.setVelocity(
                backRightWheel.getVelocity() - 0.05)
        elif direction == "south":
            frontRightWheel.setVelocity(
                frontRightWheel.getVelocity() - 0.05)
            backRightWheel.setVelocity(
                backRightWheel.getVelocity() - 0.05)
    else:
        setRobotVelocity(initialVelocity)


def getPotentialJunctions(frontDistance, backDistance, leftDistance, rightDistance, leftBackDistance, rightBackDistance):
    front = False
    back = False
    left = False
    right = False
    # if frontDistance < 800:
    #    front = True
    # if backDistance < 800:
    #    back = True
    if leftDistance < 800 or leftBackDistance < 800:
        left = True
    if rightDistance < 800 or rightBackDistance < 800:
        right = True
    return [front, back, left, right]


maze = MazeMap(1000, 1000)
maze.setup(m_size=[31, 31])

# initialize wall following alogrithm
# possible robot states: 1 (follow wall), 2 (turn), 3 (follow path), 4 (stop)
# start by following wall
robotState = 1
turnType = NULL
turnSoftly = False
turnTimeout = 0
timer = 0
# main loop

step = 0  # count how many tiles have been discovered
currentColor = "white"
matrixPosition = [0, 0]
positionType = EntryState.START
direction = getDirection(getBearingInDegrees())
targetBearing = getTargetBearing(direction)

junctionsQueue = Queue(2)

targetDirections = None
turnedTowardsPathStart = False
pathFollowingStartTimeout = 0
startTurnTimeout = 0

while robot.step(timestep) != -1:
    timer += timestep
    bearing = getBearingInDegrees()
    direction = getDirection(bearing, direction)
    dominantColor = getCameraImageDominantColor()
    # get distance readings
    frontDistance = (frontLeftMiddleSensor.getValue() +
                     frontRightMiddleSensor.getValue()) / 2
    backDistance = (backLeftMiddleSensor.getValue() +
                    backRightMiddleSensor.getValue()) / 2
    leftDistance = frontLeftSensor.getValue()
    rightDistance = frontRightSensor.getValue()
    leftBackDistance = backLeftSensor.getValue()
    rightBackDistance = backRightSensor.getValue()

    if dominantColor != currentColor:  # means that robot has reached another tile
        currentColor = dominantColor
        step += 1
        potentialJunctions = getPotentialJunctions(
            frontDistance, backDistance, leftDistance, rightDistance, leftBackDistance, rightBackDistance)
        if targetDirections != None:
            potentialJunctions = [False, False, False, False]
        mazeData = maze.addMazePathSection(
            direction=direction, currentPosition=matrixPosition, potentialJunctions=potentialJunctions)
        matrixPosition = mazeData[0]
        toBePreviousPosition = mazeData[1]
        positionType = mazeData[2]
        junctionAdded = mazeData[3]
        if junctionAdded != NULL and goalReached == False:
            junctionsQueue.enqueue(junctionAdded)
            if junctionsQueue.size() == junctionsQueue.maxlength:
                robotState = 3
                pathFollowingStartTimeout = timer + 1000
                targetDirections = maze.getTargetPathDirections(
                    targetPosition=junctionsQueue.dequeue(), currentPosition=toBePreviousPosition)
        elif goalReached == True and targetDirections == None:
            maze.addGoalSection(
                position=matrixPosition)
            robotState = 4
            targetDirections = maze.getTargetPathDirections(
                targetPosition=[0, 0], currentPosition=toBePreviousPosition, visualizeFinalPath=True)

    if junctionsQueue.hasItem(matrixPosition):
        junctionsQueue.removeItem(matrixPosition)
    if robotState == 1 and timer > turnTimeout:
        # first check if we are on a visited path: need to find a new opening to move into
        surroundingPositionTypes = maze.getSurroundingPositionTypes(
            direction, matrixPosition)
        if surroundingPositionTypes[2] != None and surroundingPositionTypes[2] == EntryState.VISITED_TWICE:
            if rightDistance < 800:
                if surroundingPositionTypes[1] == EntryState.OBSTACLE:
                    turnType = "right"
                    targetBearing = getTargetBearing(direction, turnType)
                    robotState = 2
                elif surroundingPositionTypes[1] == EntryState.VISITED_ONCE:
                    if leftDistance < 800 and surroundingPositionTypes[0] == EntryState.OBSTACLE:
                        turnType = "left"
                        targetBearing = getTargetBearing(direction, turnType)
                        robotState = 2

            elif leftDistance < 800:
                if surroundingPositionTypes[0] == EntryState.OBSTACLE:
                    turnType = "left"
                    targetBearing = getTargetBearing(direction, turnType)
                    robotState = 2
                elif surroundingPositionTypes[0] == EntryState.VISITED_ONCE:
                    if rightDistance < 800 and surroundingPositionTypes[1] == EntryState.OBSTACLE:
                        turnType = "right"
                        targetBearing = getTargetBearing(direction, turnType)
                        robotState = 2
        elif surroundingPositionTypes[2] == EntryState.OBSTACLE and surroundingPositionTypes[3] == EntryState.VISITED_ONCE:
            if frontDistance < 800:
                continue
        if frontDistance > 950:
            if rightDistance > 800 and leftDistance < 800:
                turnType = "left"
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
            elif (leftDistance > 800 and rightDistance < 800) or (rightDistance < 800 and leftDistance < 800):
                turnType = "right"
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
            elif rightDistance > 800 and leftDistance > 800:
                turnType = "around"
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
        elif frontDistance < 800 and backDistance < 800:
            if surroundingPositionTypes[2] == EntryState.OBSTACLE and surroundingPositionTypes[0] == EntryState.VISITED_ONCE:
                turnType = "straight"
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
            elif leftBackDistance > 800 and rightBackDistance < 800:
                turnType = "right"
                turnSoftly = True
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
            elif (rightBackDistance > 800 and leftBackDistance < 800) or (rightBackDistance < 800 and leftBackDistance < 800):
                turnType = "left"
                turnSoftly = True
                targetBearing = getTargetBearing(direction, turnType)
                robotState = 2
            adjustDirection(bearing, targetBearing, direction)
    if robotState == 2:
        if roundBy(bearing, 10) != targetBearing:
            turn(turnType, turnSoftly)
        else:
            if targetDirections != None:
                robotState = 3
            else:
                robotState = 1
            turnType = NULL
            turnSoftly = False
            turnTimeout = timer + 2500
            setRobotVelocity(initialVelocity)
    if robotState == 3 and timer > pathFollowingStartTimeout:
        if turnedTowardsPathStart == False:
            pathStart = targetDirections[len(targetDirections) - 1]
            pathStartDir = maze.getDirectionRelativeToCurrentPosition(
                currentPosition=matrixPosition, key=pathStart, direction=direction)
            setRobotVelocity(initialVelocity)
            targetBearing = getTargetBearing(pathStartDir[0])
            turnType = pathStartDir[1]
            robotState = 2
            turnedTowardsPathStart = True
        elif turnedTowardsPathStart == True and len(targetDirections) > 0:
            key = targetDirections[len(targetDirections) - 1]
            if maze.getKey(matrixPosition) == key and len(targetDirections) > 0:
                targetDirections.pop()
                startTurnTimeout = timer + 1000
                #adjustDirection(bearing, targetBearing, direction)
            else:
                try:
                    key = targetDirections[len(targetDirections) - 1]
                    nextDir = maze.getDirectionRelativeToCurrentPosition(
                        currentPosition=matrixPosition, key=key, direction=direction)
                    targetBearing = getTargetBearing(nextDir[0])
                    turnType = nextDir[1]
                    if timer > startTurnTimeout:
                        robotState = 2
                except:
                    continue
        elif len(targetDirections) == 0:
            targetDirections = None
            robotState = 1
            turnedTowardsPathStart = False

    if robotState == 4:
        setRobotVelocity(0)
        break
