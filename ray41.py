import math
import pygame
import os

#sets the screen to the top left corner of the monitor
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (5, 5)
pygame.init()

class Sphere:
        def __init__(self, r, m, e, c, p):
            self.radius = r
            self.mass = m
            self.elasticity = e
            self.color = c
            self.position = p

        def getRadius(self):
            return self.radius

        def getElasticity(self):
            return self.elasticity

        def getPosition(self):
            return self.position

        def getColor(self):
            return self.color

        def getPosition(self):
            return self.position


# Window size, window area, camera location X, camera location y, camera location z, the length of the direction vectors, length of phi-hat vectors, the length of the theta-hat vecotrs, resolution, field of view on the x-y plane, field of view on the z-axis, degrees per "pixel" for the phi angle, degrees per "pixel" for the theta angle, speed controller for the camera, look sensitivity multiplier, fram rate target
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
res = 1000
fovPHI = 90
fovTHETA = 90
dppPHI = fovPHI / math.sqrt(res)
dppTHETA = fovTHETA / math.sqrt(res)
speedMult = .1
turnMult = .1
frTarget = 30


#light source coordinates
lx = 1.5
ly = 8
lz = 0

#test comment
# all of the object lists (0 = point, 1 = cube, 2 = sphere)
ob = [2, 2, 2]
#point locations and colors
pX = [lx, 0, 1, -1]
pY = [ly, -1, 0, 0]
pZ = [lz, 0, 0, 0]
pColor = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)]
#cube center points, side lengths, and colors
cubeX = [10]
cubeY = [10]
cubeZ = [10]
cubeS = [5]
cubeC = [(0, 0, 150)]

#sphere creations, (radii, mass, elasticity, color, position)
sphere1 = Sphere(2, 100, 1, (250, 0, 0), (0, 10, 0))
sphere2 = Sphere(2, 10, 1, (0, 0, 250), (6, 10, 0))
sphere3 = Sphere(0.5, 5, 1, (255, 255, 255), (0, 3, 0))
sphs = [sphere1, sphere2, sphere3]


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
#test comment
    #cross product the two matricies
    i = (yC * c) - (zC * b)
    j = (xC * c) - (zC * a)
    k = (xC * b) - (yC * a)

    d = math.sqrt(((i * i) + (j * j) + (k * k)) / ((a * a) + (b * b) + (c * c)))

    #distance from point to camera
    dd = math.sqrt(((x0 - x) * (x0 - x)) + ((y0 - y) * (y0 - y)) + ((z0 - z) * (z0 - z)))
    if d <= 0.05:
        return True, dd
    else:
        return False, dd

def checkCube():

    return False

def checkSphere(x0, y0, z0, sphere, r, phi, theta):
    phi = math.radians(phi)
    theta = math.radians(theta)

    pos = sphere.getPosition()
    h = pos[0]
    k = pos[1]
    l = pos[2]
    sR = sphere.getRadius()

    a = (math.cos(phi) * math.sin(theta) * r)  # + (math.cos(phi) * math.cos(theta) * thetaH) - (math.sin(phi) * phiH)
    b = (math.sin(phi) * math.sin(theta) * r)  # + (math.sin(phi) * math.cos(theta) * thetaH) + (math.cos(phi) * phiH)
    c = (math.cos(theta) * r)  # - (math.sin(theta) * thetaH)

    # a b and c for the quadratic involving the line and the sphere
    bb = ((2 * x0 * a) - (2 * h * a) + (2 * y0 * b) - (2 * k * b) + (2 * z0 * c) - (2 * l * c))
    aa = (a * a) + (b * b) + (c * c)
    cc = ((x0 * x0) + (y0 * y0) + (z0 * z0) + (h * h) + (k * k) + (l * l) - (2 * h * x0) - (2 * k * y0) - (2 * l * z0) - (sR * sR))
    # now do the formula of the discriminant (B^2 - 4AC)
    bb = bb * bb


    discrim = bb - (4 * aa * cc)


    if discrim >= 0:
        # a b and c for the quadratic involving the line and the sphere
        bb = ((2 * x0 * a) - (2 * h * a) + (2 * y0 * b) - (2 * k * b) + (2 * z0 * c) - (2 * l * c))


        # quadratic equation
        # its supposed to be -b + or - but I still need to implement that
        # actually I found that only the - seems to result in a sphere that is not inverted
        t = ((-1 * bb) - math.sqrt((bb * bb) - (4 * aa * cc))) / (2 * aa)

        # now plug t in to the parametric forms of the line to get the intersect point(s)
        x = (t * a) + x0
        y = (t * b) + y0
        z = (t * c) + z0

        # find distance from camera or light source to intersect point
        d = math.sqrt(((x0 - x) * (x0 - x)) + ((y0 - y) * (y0 - y)) + ((z0 - z) * (z0 - z)))
        return True, d
    else:
        #placeholder distance (will never even be checked)
        d = 1000000
        return False, d

def sphereShader(x0, y0, z0, sphere, r, phi, theta):
    phi = math.radians(phi)
    theta = math.radians(theta)

    a = (math.cos(phi) * math.sin(theta) * r)  # + (math.cos(phi) * math.cos(theta) * thetaH) - (math.sin(phi) * phiH)
    b = (math.sin(phi) * math.sin(theta) * r)  # + (math.sin(phi) * math.cos(theta) * thetaH) + (math.cos(phi) * phiH)
    c = (math.cos(theta) * r)  # - (math.sin(theta) * thetaH)

    #we must now find t for the line equations to get the point(s) that they intersect at
    #a b and c for the quadratic involving the line and the sphere
    pos = sphere.getPosition()
    h = pos[0]
    k = pos[1]
    l = pos[2]
    sR = sphere.getRadius()

    bb = ((2 * x0 * a) - (2 * h * a) + (2 * y0 * b) - (2 * k * b) + (2 * z0 * c) - (2 * l * c))
    aa = (a * a) + (b * b) + (c * c)
    cc = ((x0 * x0) + (y0 * y0) + (z0 * z0) + (h * h) + (k * k) + (l * l) - (2 * h * x0) - (2 * k * y0) - (2 * l * z0) - (sR * sR))

    #quadratic equation
    #its supposed to be -b + or - but I still need to implement that
    #actually I found that only the - seems to result in a sphere that is not inverted
    t = ((-1 * bb) - math.sqrt((bb * bb) - (4 * aa * cc))) / (2 * aa)

    #now plug t in to the parametric forms of the line to get the intersect point(s)
    x = (t * a) + x0
    y = (t * b) + y0
    z = (t * c) + z0

    #the light source location
    llx = x0
    lly = y0
    llz = z0

    #find distance from camera or light source to intersect point
    d = math.sqrt(((llx - x) * (llx - x)) + ((lly - y) * (lly - y)) + ((llz - z) * (llz - z)))
    #d = math.sqrt(((lx - x) * (lx - x)) + ((ly - y) * (ly - y)) + ((lz - z) * (lz - z)))
    #now return a fraction dependant on the size of the distance
    maxDist = 1

    distanceThreshold = 1
    if ((d*d) >= distanceThreshold):
        return (maxDist / (d * d))
    else:
        return (maxDist / (distanceThreshold))


#checks to make sure that the object is in front of the camera
def inView(x0, y0, x, y, phi):

    phiT = phi + 90
    phiT = math.radians(phiT)
    phi = math.radians(phi)

    s = math.tan(phiT)

    k = math.sin(phi)/math.fabs(math.sin(phi))

    return (k * y) >= k * ((s * (x - x0)) + y0)


window = pygame.display.set_mode((wS, wS), 0, 0)

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
    #set phi to within -2pi and 2pi  still have to figure something out with this(and theta to within -pi and pi)
    phiDirec = phiDirec % 360


    if clock.get_fps() < frTarget:
        res -= 1
    else:
        res += 1

    dppPHI = fovPHI / math.sqrt(res)
    dppTHETA = fovTHETA / math.sqrt(res)
    # n is the diameter of each circle
    n = math.sqrt(wA / res)
    # pPerR is the pixels per row/column
    pPR = wS / n

    keys = pygame.key.get_pressed()
    window.fill(BLACK)

    # display fps
    fps = font.render(str(int(clock.get_fps())), True, WHITE)
    window.blit(fps, ((wS - 25), 5))
    clock.tick(60)

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
    #for strafing add 90 degrees to the phi direction to go left and right, also we dont need the z movement because strafing only deals with the x-y plane
    if keys[pygame.K_a]:
        cameraLocX = (math.cos(math.radians(phiDirec + 90)) * math.sin(math.radians(thetaDirec)) * r * speedMult) + cameraLocX
        cameraLocY = (math.sin(math.radians(phiDirec + 90)) * math.sin(math.radians(thetaDirec)) * r * speedMult) + cameraLocY

    elif keys[pygame.K_d]:
        cameraLocX = (math.cos(math.radians(phiDirec + 90)) * math.sin(math.radians(thetaDirec)) * -r * speedMult) + cameraLocX
        cameraLocY = (math.sin(math.radians(phiDirec + 90)) * math.sin(math.radians(thetaDirec)) * -r * speedMult) + cameraLocY

    # I want the middle to be pointing straight so I added half the field of view to the starting phi angle
    curPHI = phiDirec + (fovPHI / 2)
    # I want the middle to be pointing straight so I subtracted half the theta field of view to make it start facing up
    curTHETA = thetaDirec - (fovTHETA / 2)

    curX = n / 2
    curY = n / 2


    for f in range(int(pPR)):
        for l in range(int(pPR)):
            # keeps track of how many objects per type are checked for
            objP = 0
            objS = 0
            objC = 0
            #comment for creating reflection branch
            #distance from camera to closest object that has intersect point with camera
            objDist = -1
            #Color of closest object to camera that intersects with ray
            objC = (0, 0, 0)
            for u in range(0, len(ob)):


                if ob[u] == 0:
                    if inView(cameraLocX, cameraLocY, pX[objP], pY[objP], curPHI):
                        # boolean to check if the ray intersects the sphere, distance from camera to intersect point
                        cP, distP = checkPoint(cameraLocX, cameraLocY, cameraLocZ, pX[objP], pY[objP], pZ[objP], r, curPHI, curTHETA)
                        if cP and distP < objDist:
                            objC = pColor[objP]
                            objDist = distP
                        elif cP and objDist < 0:
                            objC = pColor[objP]
                            objDist = distP
                    objP += 1
                #cube code needs to be updated
                elif ob[u] == 1:
                    if inView(cameraLocX, cameraLocY, cubeX[objC], cubeY[objC], curPHI):
                        if checkCube():
                            pygame.draw.circle(window, cubeC[objC], (int(curX), int(curY)), int(n / 2))
                    objC += 1

                elif ob[u] == 2:
                    position = sphs[objS].getPosition()
                    if inView(cameraLocX, cameraLocY, position[0], position[1], curPHI):
                        #boolean to check if the ray intersects the sphere, distance from camera to intersect point
                        cS, distS = checkSphere(cameraLocX, cameraLocY, cameraLocZ, sphs[objS], r, curPHI, curTHETA)
                        if cS and distS < objDist:
                            sS = sphereShader(cameraLocX, cameraLocY, cameraLocZ, sphs[objS], r, curPHI, curTHETA)
                            color = sphs[objS].getColor()
                            objC = (color[0] * sS, color[1] * sS, color[2] * sS)
                            objDist = distS
                        elif cS and objDist < 0:
                            sS = sphereShader(cameraLocX, cameraLocY, cameraLocZ, sphs[objS], r, curPHI, curTHETA)
                            color = sphs[objS].getColor()
                            objC = (color[0] * sS, color[1] * sS, color[2] * sS)
                            objDist = distS
                    objS += 1

            #draw the pixel based on which object is closest
            if objDist >= 0:
                pygame.draw.circle(window, objC, (int(curX), int(curY)), int(n / 2))


            curPHI -= dppPHI
            curX += n
        curX = n / 2
        curPHI = phiDirec + (fovPHI / 2)
        curY += n
        curTHETA += dppTHETA

    w = font.render("W", True, (150, 150, 150))
    a = font.render("A", True, (150, 150, 150))
    s = font.render("S", True, (150, 150, 150))
    d = font.render("D", True, (150, 150, 150))
    if keys[pygame.K_w]:
        w = font.render("W", True, WHITE)

    if keys[pygame.K_a]:
        a = font.render("A", True, WHITE)

    if keys[pygame.K_s]:
        s = font.render("S", True, WHITE)

    if keys[pygame.K_d]:
        d = font.render("D", True, WHITE)

    window.blit(w, (30, (wS - 50)))
    window.blit(a, (5, (wS - 25)))
    window.blit(s, (30, (wS - 25)))
    window.blit(d, (55, (wS - 25)))

    direcLabel = font.render(str(int(phiDirec)) + "*", True, WHITE)
    window.blit(direcLabel, (wS/2, 10))

    pygame.display.update()

pygame.quit()
quit()
