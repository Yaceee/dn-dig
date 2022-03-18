import carla

def checkConnection(host, port):
    try:
        carla.Client(host, port)
        return 0
    except:
        return -1

def checkDimensions(width, height):
    return type(width) == int and width>0 and type(height) == int and height>0

def checkImgNum(imgNum):
    return type(imgNum) == int and imgNum>0

def checkFov(fov):
    return fov>0 and fov<360