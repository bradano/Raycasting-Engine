import math
import pygame

pygame.init()

# Window size, window area, camera location X, camera location y, camera location z, the length of the direction vectors, length of phi-hat vectors, the length of the theta-hat vecotrs, resolution, field of view on the x-y plane, field of view on the z-axis, degrees per "pixel" for the phi angle, degrees per "pixel" for the theta angle, speed controller for the camera, look sensitivity multiplier
wS = 1000
wA = wS * wS
cameraLocX = 0
cameraLocY = 0
cameraLocZ = 0
r = 1
phiH = 1
thetaH = 1
phiDirec = 90
thetaDirec = 90
res = 5000
fovPHI = 90
fovTHETA = 90
dppPHI = fovPHI / math.sqrt(res)
dppTHETA = fovTHETA / math.sqrt(res)
speedMult = .1
turnMult = .1

#test comment
# all of the object lists (0 = point, 1 = cube, 2 = sphere)
ob = [0, 0, 0, 0]
#point locations and colors
pX = [0, 0, 1, -1]
pY = [1, -1, 0, 0]
pZ = [0, 0, 0, 0]
pColor = [(0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255)]
#cube center points, side lengths, and colors
cubeX = [10]
cubeY = [10]
cubeZ = [10]
cubeS = [5]
cubeC = [(0, 0, 150)]

#sphere center points, radii, and colors
sphX = []
sphY = []
sphZ = []
sphR = []
sphC = [(100, 0, 0)]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def checkPoint(x0, y0, z0, x, y, z, r, phi, theta):
    phi = math.radians(phi)
    theta = math.radians(theta)

    a = (math.cos(phi) * math.sin(theta) * r) #+ (math.cos(phi) * math.cos(theta) * thetaH) - (math.sin(phi) * phiH)
    b = (math.sin(phi) * math.sin(theta) * r) #+ (math.sin(phi) * math.cos(theta) * thetaH) + (math.cos(phi) * phiH)
    c = (math.cos(theta) * r) #- (math.sin(theta) * thetaH)

    # x-combined with x0, y-combined with y0, z-combined with z0
    xC = x0 - x
    yC = y0 - y
    zC = z0 - z

    #cross product the two matricies
    i = (yC * c) - (zC * b)
    j = (xC * c) - (zC * a)
    k = (xC * b) - (yC * a)

    d = math.sqrt(((i * i) + (j * j) + (k * k)) / ((a * a) + (b * b) + (c * c)))

    if d <= 0.05:
        return True
    else:
        return False

def checkCube():

    return False

def checkSphere():
    return False

#checks to make sure that the object is in front of the camera
def inView(x0, y0, x, y, phi):

    phiT = phi + 90
    phiT = math.radians(phiT)
    phi = math.radians(phi)

    s = math.tan(phiT)

    k = math.sin(phi)/math.fabs(math.sin(phi))

    return (k * y) >= k * ((s * (x - x0)) + y0)


window = pygame.display.set_mode((wS, wS))

# n is the diameter of each circle
n = math.sqrt(wA / res)
# pPerR is the pixels per row/column
pPR = wS / n

# setup mouse controls
pygame.mouse.set_pos(wS / 2, wS / 2)
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)




font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
while True:
    keys = pygame.key.get_pressed()
    window.fill(WHITE)

    #display fps
    fps = font.render(str(int(clock.get_fps())), True, BLACK)
    window.blit(fps, ((wS - 25), 5))
    clock.tick(30)

    # get the mouse movement vector values
    mous = pygame.mouse.get_rel()
    for event in pygame.event.get():
        pass
    if keys[pygame.K_ESCAPE]:
        break


    if event.type == pygame.MOUSEMOTION:
        phiDirec -= (mous[0] * turnMult)
        thetaDirec += (mous[1] * turnMult)

    if keys[pygame.K_w]:
        cameraLocX = (math.cos(math.radians(phiDirec)) * math.sin(
            math.radians(thetaDirec)) * r * speedMult) + cameraLocX
        cameraLocY = (math.sin(math.radians(phiDirec)) * math.sin(
            math.radians(thetaDirec)) * r * speedMult) + cameraLocY
        cameraLocZ = (math.cos(math.radians(thetaDirec)) * r * speedMult) + cameraLocZ
    elif keys[pygame.K_s]:
        cameraLocX = (math.cos(math.radians(phiDirec)) * math.sin(
            math.radians(thetaDirec)) * -r * speedMult) + cameraLocX
        cameraLocY = (math.sin(math.radians(phiDirec)) * math.sin(
            math.radians(thetaDirec)) * -r * speedMult) + cameraLocY
        cameraLocZ = (math.cos(math.radians(thetaDirec)) * -r * speedMult) + cameraLocZ

    # I want the middle to be pointing straight so I added half the field of view to the starting phi angle
    curPHI = phiDirec + (fovPHI / 2)
    # I want the middle to be pointing straight so I subtracted half the theta field of view to make it start facing up
    curTHETA = thetaDirec - (fovTHETA / 2)

    curX = n / 2
    curY = n / 2



    for f in range(int(pPR)):
        for l in range(int(pPR)):
            for u in range(0, len(ob)):
                # all check methods and object type lists
                checks = [checkPoint(cameraLocX, cameraLocY, cameraLocZ, pX[u], pY[u], pZ[u], r, curPHI, curTHETA), checkCube(), checkSphere()]
                if ob[u] == 0:
                    if inView(cameraLocX, cameraLocY, pX[u], pY[u], curPHI):
                        if checkPoint(cameraLocX, cameraLocY, cameraLocZ, pX[u], pY[u], pZ[u], r, curPHI, curTHETA):
                            pygame.draw.circle(window, pColor[u], (int(curX), int(curY)), int(n / 2))
                elif ob[u] == 1:
                    if inView(cameraLocX, cameraLocY, cubeX[u], cubeY[u], curPHI):
                        if checkCube():
                            pygame.draw.circle(window, cubeC[u], (int(curX), int(curY)), int(n / 2))
                elif ob[u] == 2:
                    if inView(cameraLocX, cameraLocY, sphX[u], sphY[u], curPHI):
                        if checkSphere():
                            print("sphere")
            curPHI -= dppPHI
            curX += n
        curX = n / 2
        curPHI = phiDirec + (fovPHI / 2)
        curY += n
        curTHETA += dppTHETA



    pygame.display.update()

pygame.quit()
quit()
