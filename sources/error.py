import carla

def checkConnection(host, port):
    try:
        carla.Client(host, port)
        return 0
    except:
        return -1

def checkDimensions(dimension):
    return type(dimension[0]) == int and dimension[0]>0 and type(dimension[1]) == int and dimension[1]>0

def checkImgNum(imgNum):
    return type(imgNum) == int and imgNum>0

def checkFov(fov):
    return fov>0 and fov<360
