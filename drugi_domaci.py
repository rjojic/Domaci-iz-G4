import sys
import cv2
import numpy


font = cv2.FONT_HERSHEY_SIMPLEX 
def skalarno_mnozenje(skalar, tacka):
    for i in range(0,3):
        tacka[i] = skalar*tacka[i]
    return tacka

def base_projpres(points):
    list = [points[0], points[1], points[2]]
    D = numpy.array(points[3])
    D = numpy.transpose(D)
    A = numpy.array(list)
    A = numpy.transpose(A)
    lambdas = numpy.dot(numpy.linalg.inv(A), D)
    lambdas = numpy.transpose(lambdas)
    matrix = []
    for i in range(0,3):
        matrix.append(skalarno_mnozenje(lambdas[i], points[i]))
    matrix = numpy.array(matrix)
    matrix = numpy.transpose(matrix)
    return matrix

def projpres(originali, slike):
    A = base_projpres(originali)
    B = base_projpres(slike)
    C = numpy.dot(B, numpy.linalg.inv(A))
    return C

def short(point):
    if point[2] == 0:
        exit("beskonacna tacka")
    x = point[0]/point[2]
    y = point[1]/point[2]
    A = []
    A.append(x)
    A.append(y)
    return A

def click_event(event, x, y, flags, params):
    global original, counter, img, new_image, matrix, printed
    
    if counter < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            # cv2.putText(image, '(' + str(x) + ' ,' + str(y) + ')', (x, y), font, 1, (255, 0, 0), 2)
            print("[" + str(x) + " ," + str(y) + "]")
            cv2.imshow("window", image)
            counter = counter + 1
            original.append([x, y, 1])
    
    else:
        PA = numpy.array(short(original[0]))
        PB = numpy.array(short(original[1]))
        PC = numpy.array(short(original[2]))
        PD = numpy.array(short(original[3]))
        heightAD = numpy.sqrt(((PA[0] - PD[0]) ** 2) + ((PA[1] - PD[1]) ** 2))
        heightBC = numpy.sqrt(((PB[0] - PC[0]) ** 2) + ((PB[1] - PC[1]) ** 2))
        widthAB = numpy.sqrt(((PA[0] - PB[0]) ** 2) + ((PA[1] - PB[1]) ** 2))
        widthCD = numpy.sqrt(((PC[0] - PD[0]) ** 2) + ((PC[1] - PD[1]) ** 2))
        height = max(int(heightAD), int(heightBC))
        width = max(int(widthAB), int(widthCD))
        img.append([0, 0, 1])
        img.append([0, height - 1, 1])
        img.append([width - 1, height - 1, 1])
        img.append([width - 1, 0, 1])
        matrix = projpres(original, img)
        new_image = cv2.warpPerspective(image, matrix, (width, height))
        cv2.imshow("new window", new_image)
        if printed == False:
            print ("slike:")
            for i in range (0, 4):
                print(short(img[i]))
            print("matrica:")
            print(matrix)
            printed = True


        



if len(sys.argv) < 2:
    exit("nedovoljan broj argumenata")

image = cv2.imread(sys.argv[1])
original = []
img = []
counter = 0
printed = False
cv2.namedWindow("window", cv2.WINDOW_NORMAL)#radi kontrole velicine prozora, nije neophodno
cv2.resizeWindow("window", 1200, 900)
print("originalne tacke:")
while True:
    cv2.imshow("window", image) #prikazuje sliku
    cv2.setMouseCallback('window', click_event)
    if counter == 4:
        cv2.imshow("new window", new_image)
    cv2.waitKey(0) #sluzi za prekid programa
    break
