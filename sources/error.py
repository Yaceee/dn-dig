import carla

towns = ['town01', 'town02', 'town03', 'town04',
                 'town05', 'town06', 'town07', 'town10HD']


def checkConnection(host, port):
    try:
        carla.Client(host, port)
        return True
    except:
        print('Can\'t connect to server')
        return False

def checkDimensions(dimension):
    if( type(dimension[0]) == int and dimension[0]>0 and type(dimension[1]) == int and dimension[1]>0):
        return True
    else:
        print("Dimensions values wrong (must be int >0)")
        return False

def checkImgNum(imgNum):
    if( type(imgNum) == int and imgNum>0):
        return True
    else:
        print("ImNum value wrong (must be int >0)")
        return False

def checkFov(fov):
    if( fov>0 and fov<360):
        return True
    else:
        print("FOV value wrong (must be between 0 and 360)")
        return False

def checkTown(town):
    if (town in towns):
        return True
    else:
        print('Can\'t find town')
        return False

def checkAngle(angle):
    if (angle>=-180 and angle<=180):
        return True
    else:
        print("Angle value wrong (must be between -180 and 180)")
        return False
