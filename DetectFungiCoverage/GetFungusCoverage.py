import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import numpy as np
from matplotlib.patches import Circle
import matplotlib.image as mpimg

import cv2
import os
os.chdir("LOCAL DIR")  ####### Specify the directory in which you are working


from matplotlib import patches

from os import listdir
from os.path import isfile, join



######################
##### Step 1. Build ListeChampi: The list containing the name of all of the images
######################


###############################################################################



mypath = "LOCAL DIR"  ##### Specify the path to the directory where the fungi pictures are stored
ListeChampi = [f for f in listdir(mypath) if isfile(join(mypath, f))]



def RemoveBeinning(TheFile):  ### This function has been build specificaly according to the name of our fungi. It may be changed if the name are differents
    NewFile =[]
    for i in TheFile:
        if i[0] == ".":
            #TheFile.remove(i)
            New = i[2:]
            NewFile.append(New)
        elif i[0] == "L":
            NewFile.append(i)
    return NewFile
            
            
ListeChampi = RemoveBeinning(ListeChampi)


###############################################################################



######################
##### Step 2. Measure the size of the fungi
######################


def AppliquerCercle(image,r,g,b,posx,posy,taille,texture): ## Apply first circle to detect the image
    cv2.circle(image,(posx, posy), taille, (r,g,b),texture)


def MontrerImage(image): ## Show the image 
    plt.imshow(image)            
    plt.show()
    

def Lireimage(nom): ## Open the image and read it
   img = mpimg.imread(nom)
   if img.dtype == np.float32: # 
       img = (img * 255).astype(np.uint8)
   return img


def LireCoordCercle(image, tailleY, tailleX): ## Get coordinates of the circle
    Liste = []
    for i in range(0,(tailleY*2)):
        for j in range(0,(tailleX*2)):
            if image[i][j][0] == 255 and image[i][j][1] == 0 and image[i][j][2] == 0:
                linter = [i,j]
                Liste.append(linter)
    return Liste


def LireCoordCercleDeuxListes(image, tailleY, tailleX): ## Get coordinates of second circle
    ListeRouge = []
    ListeVert = []
    for i in range(0,(tailleY*2)):
        for j in range(0,(tailleX*2)):
            if image[i][j][0] == 255 and image[i][j][1] == 0 and image[i][j][2] == 0:
                linter = [i,j]
                ListeRouge.append(linter)
            elif image[i][j][0] == 0 and image[i][j][1] == 255 and image[i][j][2] == 0:
                linter = [i,j]
                ListeVert.append(linter)
    return ListeRouge,ListeVert

def LireCoordJaune(image, tailleY, tailleX):
    ListeJaune = []
    for i in range(0,(tailleY*2)):
        for j in range(0,(tailleX*2)):
            if image[i][j][0] == 255 and image[i][j][1] == 255 and image[i][j][2] == 0:
                linter = [i,j]
                ListeJaune.append(linter)
    return ListeJaune
    


def AttribuerCouleursSansCorrection(image, CoordGrand, CoordPetit): ## Color the fungi without correction
    vert = 0
    bleu = 0
    for i in CoordGrand:
        x = i[0]
        y = i[1]
        if image[x][y][0] <200 and image[x][y][1] <200 and image[x][y][2] <200:
            image[x][y] = [0,255,0]
            vert +=1
        elif image[x][y][0] >100 and image[x][y][0] < 240 and image[x][y][1] >100 and image[x][y][1] <240 and image[x][y][2] >100 and image[x][y][2] <240:
            image[x][y] = [0,0,255]
            bleu +=1
    for i in CoordPetit:
        x = i[0]
        y = i[1]
        if image[x][y][0] <200 and image[x][y][1] <200 and image[x][y][2] <200:
            image[x][y] = [0,255,0]
            vert +=1
        elif image[x][y][0] >100 and image[x][y][0] < 240 and image[x][y][1] >100 and image[x][y][1] <240 and image[x][y][2] >100 and image[x][y][2] <240:
            image[x][y] = [0,0,255]
            bleu +=1
    pourc = float(100)*float(vert)/(float(bleu)+float(vert))
    return pourc
            
def AttribuerCouleursAvecCorrection(img, CoordGrand, CoordPetit): ## Color the fungi with correction
    vert = 0
    bleu =0
    for i in CoordGrand:
        x = i[0]
        y = i[1]
        if img[x][y][0] <245 and img[x][y][1] <245 and img[x][y][2] <245:
                img[x][y] = [0,0,255]
                bleu += 1
    for i in CoordPetit:
        x = i[0]
        y = i[1]
        if img[x][y][0] <200 and img[x][y][1] <200 and img[x][y][2] <200:
            img[x][y] = [0,255,0]
            vert +=1

        elif img[x][y][0] >100 and img[x][y][0] < 240 and img[x][y][1] >100 and img[x][y][1] <240 and img[x][y][2] >100 and img[x][y][2] <240:
            img[x][y] = [0,0,255]
            bleu +=1
    pourc = float(100)*float(vert)/(float(bleu)+float(vert))
    return pourc




def ChoixCorrection(Liste,image): ## Define if the picture needs correction
    correction = False
    for i in Liste:
        x = i[0]
        y = i[1]
        if image[x][y][0] <200 and image[x][y][1] <200 and image[x][y][2] <200:
            continue
        else:
            correction = True
            break
    print correction
    return correction



        


########## Parameters




CoordGrand =[]
CoordPetit = []
Resultats = open("Resultas.txt", "w") ####### This is the name of the final output file

##################################



for image in ListeChampi: ### Main loop

    img = Lireimage(image)
    x = len(img[0])/2
    y = len(img)/2
    #MontrerImage(img)

    AppliquerCercle(img,255,0,0,x,y,1500,-1)
    #MontrerImage(img)

    AppliquerCercle(img,0,255,0,x,y,1250,-1)
    #MontrerImage(img)


    ListeRouge,ListeVert=LireCoordCercleDeuxListes(img, y, x)
    
    img = Lireimage(image)
    correction = ChoixCorrection(ListeVert,img)
    if correction == True:
        pourc = AttribuerCouleursAvecCorrection(img, ListeRouge, ListeVert)
        if float(pourc) < float(25):
            img = Lireimage(image)
            AppliquerCercle(img,255,0,0,x,y,1500,-1)
            AppliquerCercle(img,0,255,0,x,y,800,-1)
            #MontrerImage(img)
            ListeRouge,ListeVert=LireCoordCercleDeuxListes(img, y, x)

            
            img = Lireimage(image)
            #MontrerImage(img)
            pourc = AttribuerCouleursAvecCorrection(img, ListeRouge, ListeVert)
    else:
        pourc = AttribuerCouleursSansCorrection(img, ListeRouge, ListeVert)

    #MontrerImage(img)
    mpimg.imsave(image, img)
    #print pourc

    Resultats.write(str(image)+" "+str(pourc)+"\n")
    nom = "Corr"+str(image)
    #mpimg.imsave(nom, img)
    #print "ll"


Resultats.close()
#mpimg.imsave("resultat.png", img)







