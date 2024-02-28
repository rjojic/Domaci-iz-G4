import sys
import cv2
counter = 0 #brojac tacaka
points = [] #sluzi za belezenje tacaka
font = cv2.FONT_HERSHEY_SIMPLEX 
def vProizvod(A, B): #presek pravi i spojnicu tacaka trazimo preko vektorskog proizvoda
    C = []
    C.append(A[1]*B[2] - A[2]*B[1])
    C.append(A[2]*B[0] - A[0]*B[2])
    C.append(A[0]*B[1] - A[1]*B[0])
    return C

def find_point(points):
    global font
    p12 = vProizvod(points[0], points[1]) #1-2 spojnica
    p56 = vProizvod(points[4], points[5]) #5-6 spojnica
    T1 = vProizvod(p12, p56)
    p15 = vProizvod(points[0], points[4])
    p26 = vProizvod(points[1], points[5])
    T2 = vProizvod(p15, p26)
    p1 = vProizvod(points[2], T1) #prva prava na kojoj se nalazi nasa tacka
    p2 = vProizvod(points[7], T2) #druga prava na kojoj se nalazi nasa tacka
    T = vProizvod(p1, p2) #trazena tacka
    if T[2] == 0: #izbegavamo slucaj beskonacne tacke
        print("beskonacna tacka")
        exit()
    point = [] #tacku prebacujemo iz homogenih u obicne koordinate
    point.append(T[0]/T[2])
    point.append(T[1]/T[2])
    return point #trazene koordinate
    

def click_event(event, x, y, flags, params):
    global counter, points, font
    if counter == 3: #ovaj korak sluzi radi lakseg odredjivanja indeksa kad radimo sa points (uvek trazimo tacku broj 4)
        points.append("-")
        counter = counter + 1
    
    if counter >= 8: #kada imamo 8 (u stvari 7 tacaka), prelazimo na trazenje tacke
        point = find_point(points)
        cv2.putText(image, '(' + str(int(point[0])) + ',' + str(int(point[1])) + ')', (int(point[0]), int(point[1])), font, 1, (0, 255, 0), 2)
        cv2.imshow('image', image)
        
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            point = [x, y, 1] #prebacivanje tacke u homogene koordinate
            points.append(point)
            cv2.putText(image, '(' + str(x) +  ',' + str(y) + ')', (x,y), font, 1, (255, 0, 0), 2)
            cv2.imshow('image', image) #ispisivanje tacke na sliku
            counter = counter + 1
        




if len(sys.argv) < 2: #slika ce biti drugi argument
    exit("Nedovoljan broj argumenata")
image = cv2.imread(sys.argv[1])
while True:
    cv2.imshow("image", image) #prikazuje sliku
    cv2.setMouseCallback('image', click_event) 
    cv2.waitKey(0) #sluzi za prekid programa
    break
