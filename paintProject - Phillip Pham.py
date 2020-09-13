#Paint Program (Overwatch) - By: Phillip Pham
from pygame import * #all graphics programs will need this
from random import * #needed to use randint function
from math import *   #needed to use square root function
from tkinter import * #needed for opening and saving files
from tkinter import filedialog #stops the program from crashing on pyc (got this from Lavan from Mr. Mackenzie class because both our programs where crashing
#if you tried to use open and save without loading program from IDLE)
from textwrap import * #needed to use text wrap for information text (tells user about each tool), help from https://docs.python.org/2/library/textwrap.html

############################# BRIEF DESCRIPTIONS OF SOME TOOLS THAT ARE COMPLEX (IN MANY DIFFERENT PLACES OVER CODE)##################################
####### POLYGON TOOL
#if drawnPolygon is false (not currently drawing a polygon) and user clicks on canvas while that tool is selected
#we have to get the startPoint and save it to polygonList (holds all points of the polygon) and we have to get a copy of the
#canvas before user starts drawing polygon. we check in evt loop in MOUSEBUTTONUP after he clicked and set drawnPolygon to True.
#while it is true, we lock all other functions (user has to finish drawing polygon to avoid errors) andd if user clicks another point
#on the canvas, we check again in evt loop and add that point to polygonList, and we also save a copy of canvas to prevLine. we also
#check if that point is very close to the start point. if it is, we set drawnPolygon to false, blit the first copy of canvas and use draw.polygon to draw a polygon
#using polygonList (after finished, reset all variables so user can draw a polygon again). also in the while running loop (main loop), we check if drawnPolygon
#is true and we also blit prevLine each iteration and draw a line from last point in polygonList to mx, my to show user that they are drawing a "side" of a polygon

####### HIGHLIGHTER TOOL
#basically highlighter tool is just blitting a subsurface of another colour surface that is filled with the current colour at a transparency to canvas.
#however, each subsurface we take must be "removed" from the colour surface to avoid overlap of transparency if user goes over it again (it looks ugly).
#to do this we have to draw a black rect of that subsurface on the colour surface and use the colorkey function (on pygame website) to make all black colours
#on the surface (if current colour is exactly (0, 0, 0), we alter the black colour a little bit to (1, 1, 1)) completely transparent so it won't show up again on canvas.
#each time user changes colour or clears screen, uses redo or undo, uses eraser or changes tabs, we have to "refresh" the colour surface again and fill it with the current colour
#and transparency so user can use highlighter again.

###### TEXT TOOL
#if writeText is false (user not writing text) and if user clicks on canvas, we have to get the start point of where they clicked
#and save a copy of current screen to preText (before they write text). we check after they release mouse using MOUSEBUTTONUP in evt loop and set writeText to
#true, lock all other functions to avoid errors, and add confirm and delete buttons. while writeText is true, we check if KEYDOWN in evt loop and loop through
#all the unicodes on keyboard to check what key user typed. we then convert that unikey and add it to a string, which we then render with current font, font size, bold, etc
#and blit it on screen at the start point (orientation depends on left, right, center align). we blit the preText (to avoid overlap if user backspaces) and then we blit the
#rendered text at startpoint. if user click confirm button, we set writeText to false and reset all variables (leave current rendered text on screen). if they click
#decline we blit preText, set writeText to false and reset all variables (remove text from screen). 

###### SELECT TOOL and COPY CUT AND PASTE
#when user selects the select tool, we have to get a copy of the canvas in beforeSelect, so that we can blit it over screen if user wants to redraw another select
#rectangle. to check that, if the user selects on the canvas and selectClick is false (user didn't select an area yet) then we allow them to draw a select rectangle on
#the canvas; after they release mouse button, we check is selectClick is false in MOUSEBUTTONUP in the evt loop and set it to true. now, the user can click cut or copy
#to cut or copy the selected area and save it to the respective variable. if they do, then we blit beforeSelect to remove the selected area and set
#selectClick to false. if they click on canvas again while selectClick is true, then we have to blit beforeSelect and set selectClick to false so they can select another
#area again. if user clicks paste, then we set pasteMove to true and lock all other functions, save the current canvas to beforePaste, and then if the user hovers
#on canvas, we blit beforePaste and blit the cut or copied area (cut takes precedence first and you can only paste it once while copy you can paste forever until
#you select another area again) on top at mx, my to prevent multiple images from appearing. if user clicks on canvas, we check in the evt loop using MOUSEBUTTONUP, and then we
#set pasteMode to false so we can enable functions again (cut or copied image stays where you clicked). we also have to set selectClick to false and blit beforeSelect
#and update beforeSelect with current canvas each time user changes windows, uses undo and redo, clears screen, add or delete windows, or changes tool while
#selectClick is true to avoid blitting error.

root = Tk()     #create new "tk window"
root.withdraw() #hides the "tk window"

init() #initializes pygame
font.init() #initializes fonts

#simple colours needed for drawing in pygame 
       #r   g   b
RED  = (255, 0, 0) #tuple - a list that can not be changed!
GREEN = (0, 255, 0)
BLUE = (6, 147, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (204, 224, 90)

#setting background image and logo
backgroundPic = image.load("background.jpg") #loading background image
sizedBackgroundPic = transform.scale(backgroundPic, (1360, 768)) #transform background image into correct screen size
logoPic = image.load("logo.png") #loading logo image
sizedLogoPic = transform.scale(logoPic, (150, 100)) #transform logo image to correct size

windowSize = (1360, 768) #screen resolution
screen = display.set_mode(windowSize) #creating a 1024 x 768 window

screen.blit(sizedBackgroundPic, (0, 0)) #displaying background image on screen
screen.blit(sizedLogoPic, (1200, 5)) #displaying logo on screen

display.set_caption("Overwatch Paint Program - Phillip Pham") #setting window caption


#################################### IMAGES ######################################
#loading all images used in program

#tools icons
selectButton = image.load("Buttons/tools/select.png")
pencilButton = image.load("Buttons/tools/pencil.png")
paintButton = image.load("Buttons/tools/paint.png")
eraserButton = image.load("Buttons/tools/eraser.png")
fillButton = image.load("Buttons/tools/fill.png")
eyeButton = image.load("Buttons/tools/eyedrop.png")
sprayButton = image.load("Buttons/tools/spray.png")
sprinkleButton = image.load("Buttons/tools/sprinkles.png")
lineButton = image.load("Buttons/tools/line.png")
polygonButton = image.load("Buttons/tools/polygon.png")
rectButton = image.load("Buttons/tools/rectangle.png")
ellipseButton = image.load("Buttons/tools/ellipse.png")
textButton = image.load("Buttons/tools/text.png")
stampButton = image.load("Buttons/tools/stamp.png")

#blitting tool icons to screen
screen.blit(selectButton, (20, 30))
screen.blit(pencilButton, (110, 30))
screen.blit(paintButton, (20, 100))
screen.blit(eraserButton, (110, 100))
screen.blit(fillButton, (20, 170))
screen.blit(eyeButton, (110, 170))
screen.blit(sprayButton, (20, 240))
screen.blit(sprinkleButton, (110, 240))
screen.blit(lineButton, (20, 310))
screen.blit(polygonButton, (110, 310))
screen.blit(rectButton, (20, 380))
screen.blit(ellipseButton, (110, 380))
screen.blit(textButton, (20, 450))
screen.blit(stampButton, (110, 450))

#open and save icons and blitting to screen
openButton = image.load("Buttons/open.png")
saveButton = image.load("Buttons/save.png")
screen.blit(openButton, (1230, 680))
screen.blit(saveButton, (1300, 680))

#clear canvas icon
clearButton = image.load("Buttons/broom.png")
screen.blit(clearButton, (1100, 680))

#undo and redo icons
undoButton = image.load("Buttons/undo.png")
redoButton = image.load("Buttons/redo.png")
screen.blit(undoButton, (250, 690))
screen.blit(redoButton, (310, 690))

#cut, copy, paste icons
cutButton = image.load("Buttons/cut.png")
copyButton = image.load("Buttons/copy.png")
pasteButton = image.load("Buttons/paste.png")
screen.blit(cutButton, (760, 690))
screen.blit(copyButton, (700, 690))
screen.blit(pasteButton, (820, 690))

#confirm, decline icons for text tool to confirm text
confirmButton = image.load("Buttons/yes.png")
declineButton = image.load("Buttons/no.png")

#text options (left, right, center align and bold, italicize, and underline)
leftAlignButton = image.load("Buttons/leftAlign.png")
rightAlignButton = image.load("Buttons/rightAlign.png")
centerAlignButton = image.load("Buttons/centerAlign.png")
boldButton = image.load("Buttons/bold.png")
italicizeButton = image.load("Buttons/italicize.png")
underlineButton = image.load("Buttons/underline.png")

#add and delete windows icons
addWindowButton = image.load("Buttons/addWindow.png")
deleteWindowButton = image.load("Buttons/deleteWindow.png")
screen.blit(addWindowButton, (500, 690))
screen.blit(deleteWindowButton, (560, 690))

#filled or nonfilled (rect, ellipse, and polygon tools) icons
filledButton = image.load("Buttons/filled.png")
nonfilledButton = image.load("Buttons/nonfilled.png")

#brush or highlight icons (used for paint tool)
brushButton = image.load("Buttons/brush.png")
highlightButton = image.load("Buttons/highlight.png")

paint = "brush" #variable to tell wheter user is using brush tool or highlight tool (paint tool has 2 options)

#rects for brush tool and highlight tool
brushRect = Rect(1100, 150, 50, 50)
highlightRect = Rect(1200, 150, 50, 50)

#filters icons
filterButton = image.load("Buttons/filter.png")
screen.blit(filterButton, (1020, 680))
blackAndWhiteButton = image.load("Buttons/black-white.png")
sepiaButton = image.load("Buttons/sepia.jpg")

#character portraits
portraitList = [] #list to hold all loaded stamp select character portraits

#loading stamp selectcharacter portraits
bastion = image.load("Characters/bastion.png")
dva = image.load("Characters/dva.png")
genji = image.load("Characters/genji.png")
hanzo = image.load("Characters/hanzo.png")
junkrat = image.load("Characters/junkrat.png")
lucio = image.load("Characters/lucio.png")
mccree = image.load("Characters/mccree.png")
mei = image.load("Characters/mei.png")
mercy = image.load("Characters/mercy.png")
pharah = image.load("Characters/pharah.png")
reaper = image.load("Characters/reaper.png")
reinhardt = image.load("Characters/reinhardt.png")
roadhog = image.load("Characters/roadhog.png")
soldier76 = image.load("Characters/soldier76.png")
symmetra = image.load("Characters/symmetra.png")
torbjorn = image.load("Characters/torbjorn.png")
tracer = image.load("Characters/tracer.png")
widowmaker = image.load("Characters/widowmaker.png")
winston = image.load("Characters/winston.png")
zarya = image.load("Characters/zarya.png")
zenyatta = image.load("Characters/zenyatta.png")

#appending all protraits to portraitList
portraitList.append(bastion)
portraitList.append(dva)
portraitList.append(genji)
portraitList.append(hanzo)
portraitList.append(junkrat)
portraitList.append(lucio)
portraitList.append(mccree)
portraitList.append(mei)
portraitList.append(mercy)
portraitList.append(pharah)
portraitList.append(reaper)
portraitList.append(reinhardt)
portraitList.append(roadhog)
portraitList.append(soldier76)
portraitList.append(symmetra)
portraitList.append(torbjorn)
portraitList.append(tracer)
portraitList.append(widowmaker)
portraitList.append(winston)
portraitList.append(zarya)
portraitList.append(zenyatta)


#character stamps (each character is in same index of list as their portrait in portraitList)
stampList = [] #holds all character stamps to blit on canvas

#loading character stamps
bastionStamp = image.load("Stamps/bastion.png")
dvaStamp = image.load("Stamps/dva.png")
genjiStamp = image.load("Stamps/genji.png")
hanzoStamp = image.load("Stamps/hanzo.png")
junkratStamp = image.load("Stamps/junkrat.png")
lucioStamp = image.load("Stamps/lucio.png")
mccreeStamp = image.load("Stamps/mccree.png")
meiStamp = image.load("Stamps/mei.png")
mercyStamp = image.load("Stamps/mercy.png")
pharahStamp = image.load("Stamps/pharah.png")
reaperStamp = image.load("Stamps/reaper.png")
reinhardtStamp = image.load("Stamps/reinhardt.png")
roadhogStamp = image.load("Stamps/roadhog.png")
soldier76Stamp = image.load("Stamps/soldier76.png")
symmetraStamp = image.load("Stamps/symmetra.png")
torbjornStamp = image.load("Stamps/torbjorn.png")
tracerStamp = image.load("Stamps/tracer.png")
widowmakerStamp = image.load("Stamps/widowmaker.png")
winstonStamp = image.load("Stamps/winston.png")
zaryaStamp = image.load("Stamps/zarya.png")
zenyattaStamp = image.load("Stamps/zenyatta.png")

#adding them all to stampList
stampList.append(bastionStamp)
stampList.append(dvaStamp)
stampList.append(genjiStamp)
stampList.append(hanzoStamp)
stampList.append(junkratStamp)
stampList.append(lucioStamp)
stampList.append(mccreeStamp)
stampList.append(meiStamp)
stampList.append(mercyStamp)
stampList.append(pharahStamp)
stampList.append(reaperStamp)
stampList.append(reinhardtStamp)
stampList.append(roadhogStamp)
stampList.append(soldier76Stamp)
stampList.append(symmetraStamp)
stampList.append(torbjornStamp)
stampList.append(tracerStamp)
stampList.append(widowmakerStamp)
stampList.append(winstonStamp)
stampList.append(zaryaStamp)
stampList.append(zenyattaStamp)

currentStamp = 0 #index of current stamp (needed to find out what stamp user selected for stamp tool)
currentBackground = 0 #index of current background (needed to find out what background user selected for background tool)
currentStampSelect = "stamp" #when using the stamp tool, user has two options (character stamps or backgrounds). this
#variable is used to find out which option user is currently using

stampSelectRect = Rect(1080, 400, 90, 20) #rect for character stamp option in stamp tool
backgroundSelectRect = Rect(1200, 400, 90, 20) #rect for background stamp option in stamp tool


#backgrounds in stamp tool

backgroundsList = [] #list to hold all the backgrounds that user blits to canvas
backgroundPortraits = [] #list to hold all the background portrait images that user selects from

#loading all backgrounds and transfroming them to the correct size to fill whole canvas or use as portrait
hanger = image.load("Backgrounds/background1.jpg")
hanger = transform.scale(hanger, (750, 600))
hanger1 = transform.scale(hanger, (120, 100))

building = image.load("Backgrounds/background2.jpg")
building = transform.scale(building, (750, 600))
building1 = transform.scale(building, (120, 100))

street = image.load("Backgrounds/background3.png")
street = transform.scale(street, (750, 600))
street1 = transform.scale(street, (120, 100))

castle = image.load("Backgrounds/background4.png")
castle = transform.scale(castle, (750, 600))
castle1 = transform.scale(castle, (120, 100))

outside = image.load("Backgrounds/background5.png")
outside = transform.scale(outside, (750, 600))
outside1 = transform.scale(outside, (120, 100))

temple = image.load("Backgrounds/background6.jpg")
temple = transform.scale(temple, (750, 600))
temple1 = transform.scale(temple, (120, 100))

#appending all the canvas size backgrounds to backgroundsList
backgroundsList.append(hanger)
backgroundsList.append(building)
backgroundsList.append(street)
backgroundsList.append(castle)
backgroundsList.append(outside)
backgroundsList.append(temple)

#appending all the portrait size backgrounds to backgroundPortraits
backgroundPortraits.append(hanger1)
backgroundPortraits.append(building1)
backgroundPortraits.append(street1)
backgroundPortraits.append(castle1)
backgroundPortraits.append(outside1)
backgroundPortraits.append(temple1)


######################################## TOOLS RECTS ###################################
#tools select rectangles for each tool
selectRect = Rect(20, 30, 60, 60)
pencilRect = Rect(110, 30, 60, 60)
paintRect = Rect(20, 100, 60, 60)
eraserRect = Rect(110, 100, 60, 60)
fillRect = Rect(20, 170, 60, 60)
eyeRect = Rect(110, 170, 60, 60)
sprayRect = Rect(20, 240, 60, 60)
sprinkleRect = Rect(110, 240, 60, 60)
lineRect = Rect(20, 310, 60, 60)
polygonRect = Rect(110, 310, 60, 60)
rectRect = Rect(20, 380, 60, 60)
ellipseRect = Rect(110, 380, 60, 60)
textRect = Rect(20, 450, 60, 60)
stampRect = Rect(110, 450, 60, 60)

filterRect = Rect(1020, 680, 50, 50) 

clearRect = Rect(1100, 680, 50, 50)

#appending all the tools rects to toolsList (later used to check if user clicked on one of them)
#appending in same order in respect to toolsName list below
toolsList = []
toolsList.append(selectRect)
toolsList.append(pencilRect)
toolsList.append(paintRect)
toolsList.append(eraserRect)
toolsList.append(fillRect)
toolsList.append(eyeRect)
toolsList.append(sprayRect)
toolsList.append(sprinkleRect)
toolsList.append(lineRect)
toolsList.append(polygonRect)
toolsList.append(rectRect)
toolsList.append(ellipseRect)
toolsList.append(textRect)
toolsList.append(stampRect)
toolsList.append(filterRect)

toolsNames = ["select", "pencil", "paint", "eraser", "fill", "eyedrop", "spray",
              "sprinkles", "line", "polygon", "rect", "ellipse", "text", "stamp", "filter"]
#list that holds all the strings of each tool name, so that when user clicks on a tool rect
#we get index of what rect they clicked on toolsList and set the tool variable to current tool by
#finding out the string at that index on toolsName

tool = "pencil" #variable to hold current tool (default pencil)
prevTool = "pencil" #variable to hold last tool user selected (used so that we don't have to blit side bar of screen each time unless user changes tool)
draw.rect(screen, BLUE, clearRect, 2) #draws clear rect on screen (not part to toolbar on left side, so we have to draw independently instead of using for loop)

#open and save select rectangles
openRect = Rect(1230, 680, 50, 50)
saveRect = Rect(1300, 680, 50, 50)

#drawing open and save rectangles
draw.rect(screen, BLUE, openRect, 2)
draw.rect(screen, BLUE, saveRect, 2)


################################# COLOUR RELATED STUFF ########################################
col = GREEN #variable to hold current colour (default GREEN)
prevCol = col #variable to hold previous colour selected (used later in highlighter tool)

#create a surface used for highligher tool (will explain later)
#we have to convert it to change it to a different pixel format so that we can use functions like fill and set_alpha
#help from https://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert
highlightBack = Surface((750, 600)).convert()
#set transparency of that surface to 125
highlightBack.set_alpha(125)
#fill that surface with current colour
highlightBack.fill(col)

colourRect = Rect(1100, 25, 70, 70) #rectangle that displays current colour
draw.rect(screen, GREEN, colourRect) #draws rectangle to display current colour (GREEN)

colourWheel = image.load("colourpicker.png") #loading colour slider image
colourWheel = transform.scale(colourWheel, (200, 20)) #transforming it to correct dimensions
colourWheelRect = Rect(5, 519, 201, 22) #rect that draws border around colour slider (know if user clicked on it)
screen.blit(colourWheel, (5, 520)) #place colour slider picture on screen
draw.rect(screen, BLACK, colourWheelRect, 1) #drawing the border rect

colourPicker = Rect(4, 549, 201, 201) #rectangle that defines boundaries of colour gradient
draw.rect(screen, BLACK, colourPicker, 1) #drawing colourPicker border around colour gradient


#drawing colour gradient of current colour 
wheelColGradient = Surface((255, 255), SRCALPHA).convert() #create a surface 255 x 255 in length (rgb colours can only go up to num 255)
wheelColPix = col #gets rgb of current col
wheelColGradient.fill((0, 0, 0)) #first fill the gradient surface in all black (clear all pixels of last gradient)
x = 0 #x value of gradient pixel starts at 0 
y = 0 #y value of gradient pixel starts at 0 

#took me very long time to find out how to draw gradient on pygame
#i got help from these sites below 
#http://stackoverflow.com/questions/27532/generating-gradients-programmatically
#site helped me find out formula for drawing gradients
#http://stackoverflow.com/questions/32513387/how-to-create-a-color-canvas-for-color-picker-wpf?rq=1
#site helped me find out figure out idea of how to make each row have a more darker shade

while y < 255: #while the current gradient pixel is not at end of row of a surface
    ratio = x / 255 #ratio of the current x value over 255 (last x pixel)
    bright = y #the brightness of each pixel can also be equal to the y value of the pixel

    #finding out r, g, b values of current pixel. we are technically drawing a line gradient
    #for each line between the colour white and the current colour. you also have to subtract the
    #white colour by the brightness value(y) which makes it more darker each row. you multiply the
    #"white" colour by 1 - ratio, and add it to the wheelColPix value also subtracted by the brightness
    #multiplied by the ratio(if wheelColPix - brightness is negative, the wheelColPix value will be 0 or black)
    #for each the r, g, and b. once you find the r, g, b, you set that colour to that pixel
    r = int((255 - bright) * (1 - ratio) + (max(wheelColPix[0] - bright, 0)) * ratio)
    g = int((255 - bright) * (1 - ratio) + (max(wheelColPix[1] - bright, 0)) * ratio)
    b = int((255 - bright) * (1 - ratio) + (max(wheelColPix[2] - bright, 0)) * ratio)
    wheelColGradient.set_at((x, y), (r, g, b))
    #if the x value is not at end of row, then increase it by 1
    if x < 255:
        x += 1
    else:
        #otherwise reset the x at 0 and increase the y value by 1
        x = 0
        y += 1
    #this loop continues until whole gradient is drawn 

gradient = wheelColGradient.subsurface((0, 0, 255, 255)).copy() #after gradient is drawn we have to copy the gradient surface
#to resize it to fill dimensions of border
transformedGradient = transform.scale(gradient, (200, 200)) #transform the copied surface to correct dimensions
screen.blit(transformedGradient, (5, 550)) #blits it to the screen

draw.rect(screen, BLACK, colourPicker, 1) #draws border around gradient
colourUp = False #this is just a variable to check if mouse is clicking on colour slider so we only draw gradient
#once user releases his mouse (drawing gradients is very slow!)



#canvas windows (allows user to draw on more than one canvas)
canvasRect = Rect(220, 80, 750, 600) #rectangle that user draws on (actual canvas)
windows = [] #list holds all the canvas windows (copies of canvasRect)
addWindow = Rect(500, 690, 40, 40) #select rectangle that adds a new window
deleteWindow = Rect(560, 690, 40, 40) #select rectangle that deletes current window

#drawing add and delete windows rect
draw.rect(screen, BLUE, deleteWindow, 2)
draw.rect(screen, BLUE, addWindow, 2)



#undo and redo
undoList = [] #list to hold the undo canvasRect copies 
redoList = [] #list to hold the redo canvasRect copies
undoRect = Rect(250, 690, 40, 40) #rectangle that user clicks to undo
redoRect = Rect(310, 690, 40, 40) #rectangle that user clicks to redo
#drawing undo and redo rects
draw.rect(screen, BLUE, undoRect, 2)
draw.rect(screen, BLUE, redoRect, 2)




#defaults and other variables
mx, my = (0, 0) #placeholder point for current point (avoid crashing program at start)
omx, omy = (0, 0) #will be used for the pencil tool to check previous point of cursor
running = True #boolean variable (for main loop to run forever)
size = 10 #determines size for eraser, paint, sprinkles, and spray paint tool
thick = 5 #determines thickness for line tool, sprinkles, unfilled rect, ellipse, and polygon drawing
rotate = 0 #deternines rotation of stamps
filterType = "" #deternines what current filter user selected
scaleSize = 0 #determines how much to subtract from stamp height and width to make size smaller
speedSpray = 1.5 #determines speed of spray paint

################################# SELECT TOOL FUNCTIONS ##################################
#copy, cut, and paste rectangles
copyRect = Rect(700, 690, 40, 40)
cutRect = Rect(760, 690, 40, 40)
pasteRect = Rect(820, 690, 40, 40)

selectArea = None #the select tool will allow user to select area with a rectangle, this variable will save that
#area inside the rectangle so the user can copy or cut it
selectClick = False #checks to see there is already a select box on screen
beforeSelect = None #holds copy of canvas before user selected select tool so that we can reblit it if user wants to draw another select box
copy = None #holds subsurface from selectArea copied
cut = None #holds subsurface from selectArea cutted

pasteMove = False #checks if user is currently pasting something on screen so we can disable other functions

#draw rects for the copy, cut, and paste functions so user can select it
draw.rect(screen, BLUE, copyRect, 2)
draw.rect(screen, BLUE, cutRect, 2)
draw.rect(screen, BLUE, pasteRect, 2)


################################## BACKGROUND MUSIC #########################################
#playing music and sound
#help from https://www.pygame.org/docs/ref/music.html
mixer.music.load("theme.mp3") #loading music file
mixer.music.play(-1, 0.0) #playing music (loops forever with -1, starts at 0.0 s)


############################### TEXT TOOL RELATED STUFF ######################################
text = "" #holds text that user types
textAlign = "left" #var to hold current text alignment option

#rects for confirm and declining text written
confirmText = Rect(1050, 350, 40, 40)
declineText = Rect(1150, 350, 40, 40)

#rects for text align
leftAlign = Rect(1000, 250, 40, 40)
rightAlign = Rect(1200, 250, 40, 40) 
centerAlign = Rect(1100, 250, 40, 40)

#rects for bold, italicize, and underline
boldRect = Rect(1000, 300, 40, 40)
italicizeRect = Rect(1100, 300, 40, 40)
underlineRect = Rect(1200, 300, 40, 40)

#variables to check if user selected bold, italicize, or underline for text
bold = False
italicize = False
underline = False


#var to hold current font size (default 50)
fontSize = 50
currentFont = "BigNoodleTooOblique" #variable to hold current font
fontsList = ["Verdana", "Agency FB", "BigNoodleTooOblique", "Times New Roman", "Georgia", "Calibri"]
#list to hold available font names
writeText = False #checks to see if user is writing text currently on canvas so we can disable other functions




############################## POLYGON TOOL RELATED STUFF ############################################
polygonList = [] #list to hold points user clicked on canvas for polygon tool
drawnPolygon = False #checks if user is currently drawing a polygon so we can disable all other functions
polygonPoint = (0, 0) #placeholder for polygon point each time user clicks while drawing
startPoint = (0, 0) #placeholder for first start point user clicked
prevLine = None #copy of the screen at the previous point drawn for polygon (so that user can see line connecting
#to next point without multiple lines appearing on screen)
filledShape = True #checks if user is currently selecting filled or non - filled shapes to be drawn (for rect, ellipse, and polygon tools)


############################## BACKGROUND COPIES ####################################################
#these background copies are subsurfaces of original backgrounds so we can overwrite rects and buttons
#over top of them if user decides to select new tools

tabBack = screen.subsurface((220, 30, 721, 21)).copy() #surface to overwrite tab of canvas windows
#so if user deletes a tab, we can redraw the other tabs
backgroundSurface = screen.subsurface((979, 109, 1360 - 979, 330)).copy()#side bar surface so we can put buttons
#such as filled and unfilled, display current size and thickness for certain tools
backgroundCanvasRect = screen.subsurface((220, 80, 750, 600)).copy() #background of canvasRect if no canvas or tab is on screen at this moment
#(user has no windows open)
currentSizeBack = screen.subsurface((1049, 210, 300, 55)).copy() #small background surface so we can display current size in text without overlap
infoBack = screen.subsurface((1000, 450, 325, 200)).copy() #background surface for infobar in bottom right corner of screen that displays info about current tool
textToolBack = screen.subsurface((999, 299, 300, 41)).copy() #background surface for drawing confirm and decline text rects if user is currently typing using text tool


#function i found online on accident, used it to blit stamp portraits on screen
#so that it has a cool transparancy effect by reblitting the same image at low transparency until it reaches value of 255
#http://www.nerdparadise.com/programming/pygameblitopacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

#function for floodfill. i made this by myself with a little bit of help online
#and after lots of trial to keep program from not crashing
#https://gist.github.com/JDWarner/1158a9515c7f1b1c21f1
def floodFill(x, y, oldColour, newColour): #takes in coor user clicked, the colour of that coor, and the current colour
    listFill = [(x, y)] #list to hold points to be filled
    if oldColour == newColour: #if the coor clicked has same col as current, then we exit function to avoid crashing program
        return
    while len(listFill) > 0: #while there are still points to be filled
        x, y = listFill.pop() #take out last poinf from list
        while x > 970 or y > 680: #if point is off the canvas, then we pop another point until it isn't
            x, y = listFill.pop()
        if screen.get_at((x, y)) == oldColour: #if the colour at the coor is same as when user first clicked 
            screen.set_at((x, y), newColour) #we set the old colour to current colour
            #we have to then check where that point is located so we can add points
            #without a stack overflow
            if x > 220: #checks if the x of point is greater than canvas edge at left
                listFill.append((x - 1, y)) #if it is, we add the point to the left
            if x < 970: #checks if the x of point is less than canvas edge at right
                listFill.append((x + 1, y)) #if it is, we add the point to the right
            if y > 80: #checks if the y of point is greater than canvas edge at top
                listFill.append((x, y - 1)) #if it is, we add the bottom point
            if y < 680: #checks if the y of point is less than canvas edge at bottom
                listFill.append((x, y + 1)) #if it is, we add the down point

####################################### INFO BAR STUFF ##########################################

currentInfoDisplay = font.SysFont("BigNoodleTooOblique", 20) #sets main font for info bar text
infoBar = Surface((400, 400), SRCALPHA) #surface that holds text written (is also transparent)
infoBarBack = infoBar.subsurface((0, 0, 400, 400)).copy() #back surface of info bar so that we can reblit
#it on for new text and to avoid losing same transparancy
infoRect = Rect(0, 0, 325, 200) #rect that we draw on top of infoBar for red colour
infoText = "Default" #current info text to display on screen
prevInfoText = "Default" #previous info text

#main program loop that runs forever 
while running:
    ############################################################################
    
    ############################# HANDLING EVENTS ##############################
    #checks for all events while program is running
    for evt in event.get():
        #checks if the user exits, set running to false so loop stops and program ends
        if evt.type == QUIT:
            running = False
            
        #checks after user performs left mouse click and releases mouse
        if evt.type == MOUSEBUTTONUP and evt.button == 1:
            #if user is currently pasting and if he is colliding with canvas
            if pasteMove == True and canvasRect.collidepoint(mx, my):
                #if he clicks, we have to stop pasteMove since he already blitted cut or copied surface on screen
                if mb[0] == 1:
                    if cut != None:
                        cut = None #we set cut to none so user can cut again a new area
                    screen.blit(backgroundSurface, (979, 109)) #we erase the side bar
                    beforeSelect = screen.subsurface(canvasRect).copy() #we have to copy the canvas for blitting for select tool
                    undoList.append(screen.subsurface(canvasRect).copy()) #we add this new change to canvas on to undoList
                    del redoList[:]
                    pasteMove = False #we set pasteMove to false 

            #checks if user released the mouse over colour slider
            if colourUp == False and colourWheelRect.collidepoint(mx, my):
                wheelColPix = screen.get_at((mx, my)) #save the col pixel they are at on colour slider
                colourUp = True #set the coloutUp to true so way below code can draw gradient

            #checks if tool is select and select click is false and user is on canvas after clicking 
            if tool == "select" and selectClick == False and canvasRect.collidepoint(mx, my):
                selectClick = True #we set select click to true to indicate that they have now selected am area
                #since they just drew a select rect

            #checks if user is currently writing text 
            if writeText == True:
                #if they pressed the confirm button
                if confirmText.collidepoint(mx, my):
                    writeText = False #we have to set writeText to false to enable function again
                    screen.blit(backgroundSurface, (979, 109)) #removes confirm button by reblitting side bar
                    text = "" #reset text they typed back to nothing
                    undoList.append(screen.subsurface(canvasRect).copy()) #append new change to canvas (written text) to undoList
                    del redoList[:]
                    
                #if they pressed the decline button
                if declineText.collidepoint(mx, my):
                    writeText = False #we have to set writeText to false to enable function again
                    screen.blit(preText, (220, 80)) #reset canvas to before user wrote text
                    screen.blit(backgroundSurface, (979, 109)) #removes decline button by reblitting side bar
                    text = "" #reset text they typed back to nothing
                    
            #if the mouse is on the canvas and user is not pasting
            if canvasRect.collidepoint(mx, my) and pasteMove == False:
                #if the tool isn't eyedropper, then we copy image of canvas to undoList
                if tool != "eyedrop" and tool != "text" and tool != "select" and tool != "polygon" and len(windows) > 0: 
                    undoList.append(screen.subsurface(canvasRect).copy())
                    del redoList[:] #delete everything from redo so that you erase all previous undos
                #if it is, then we get the colour where the user clicked
                #and change it to the current colour
                if tool == "eyedrop" and len(windows) > 0:
                    col = screen.get_at((mx, my))
                    draw.rect(screen, col, colourRect) #draw rect to indicate diff colour

                #if the tool is polygon
                if tool == "polygon":
                    #if drawnPolygon is False and there is no start point
                    if drawnPolygon == False and startPoint != None:
                        drawnPolygon = True #we set drawnPolygon to true to disable all other functions and start drawing polygon
                    elif startPoint != None: #else if  there is a startpoint
                        #we check if the point user just clicked is very close to startpoint and there are at least 3 points
                        if sqrt((mx - startPoint[0]) ** 2) < 8 and sqrt((my - startPoint[1]) ** 2) < 8 and len(polygonList) > 2:
                            screen.blit(prevLine, (0, 0)) #we blit the canvas before the last point was clicked
                            polygonList.append(startPoint) #we append the firstpoint again to list
                            draw.line(screen, col, polygonPoint, startPoint, thick) #we draw a line connecting last point drawn to start point
                            display.flip() #we display this to screen
                            #if filled is selected
                            if filledShape == True:
                                screen.blit(firstCopy, (0, 0)) #we blit canvas before polygon was drawn
                                draw.polygon(screen, col, polygonList) #we now draw real polygon using points in polygonList
                            #if non- filled is selected
                            else:
                                #we do same thing except add thickness to draw polygon so that it can draw unfilled
                                screen.blit(firstCopy, (0, 0))
                                draw.polygon(screen, col, polygonList, thick)
                            undoList.append(screen.subsurface(canvasRect).copy())
                            del redoList[:]
                            #reset all variables used back in drawing the polygon to None so user can draw again
                            drawnPolygon = False
                            polygonPoint = None
                            startPoint = None
                            prevLine = None
                            del polygonList[:] #delete all points from polygonList, so user can draw another polygon
                        #if point user clicked is still far away from start point
                        else:
                            prevLine = screen.copy() #we save a copy of the current canvas to prevLine
                            polygonPoint = mx, my #add point user selected to polygonList
                            polygonList.append(polygonPoint)

            #if the mouse is on clear button, then we copy image of canvas to
            #undoList and fill the whole canvas white (clear canvas)
            #clear, add, and delete windows can only be used if tool is not select because it just causes too many problems with blitting the canvas
            if clearRect.collidepoint(mx, my) and len(windows) > 0 and writeText != True and drawnPolygon != True and pasteMove == False:
                #if there is a select area, we have to remove it by blitting beforeSelect so it won't show up when we add canvas to undoList
                if selectClick == True and beforeSelect != None:
                    screen.blit(beforeSelect, (220, 80))
                    
                undoList.append(screen.subsurface(canvasRect).copy())
                draw.rect(screen, WHITE, canvasRect) 
                undoList.append(screen.subsurface(canvasRect).copy())
                del redoList[:]
                #if user is pasting, we have to copy current screen to beforePaste to avoid problems of the last beforePaste showing up before
                #we cleared the screen
                if pasteMove == True:
                    beforePaste = screen.copy()

                if beforeSelect != None:
                    beforeSelect = screen.subsurface(canvasRect).copy()
                    selectClick = False
                    
                #we reset the surface used for highlighter tool
                highlightBack = Surface((800, 700)).convert()
                highlightBack.set_alpha(125)
                highlightBack.fill(col)
                
            #if the mouse is on add window button
            if addWindow.collidepoint(mx, my) and writeText != True and drawnPolygon != True and pasteMove == False:
                #we draw a new tab 
                #and we check if there is between 0 and 8 tabs (max 8 tabs) 
                if 0 < len(windows) < 8:
                    #avoid blitting error
                    if selectClick == True and beforeSelect != None:
                        screen.blit(beforeSelect, (220, 80))
                        selectClick = False
                        beforeSelect = None
                    #if there is, we delete the previous canvas instance and
                    #replace it with current canvas instance in the windowsList of the currentWindow
                    del windows[currentWindow]
                    windows.insert(currentWindow, screen.subsurface(canvasRect).copy())
                    #then we draw a new canvas overtop it and add it to the windows list 
                    addCanvas = draw.rect(screen, WHITE, canvasRect)
                    windows.append(addCanvas)
                    currentWindow = len(windows) - 1 #we then set the index of the currentWindow to that added canvas

                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)

                    #if tool is select, we have to set new beforeSelect to current screen and set selectClick to false
                    if tool == "select":
                        beforeSelect = screen.subsurface(canvasRect).copy()
                        selectClick = False
                    
                    #we add a new tab for the window as well
                #otherwise the user has no current windows
                elif len(windows) == 0:
                    #we draw a new canvas on the screen and add it to windows list
                    addCanvas = draw.rect(screen, WHITE, canvasRect)
                    windows.append(addCanvas.copy())
                    #we also add first instance of canvas to undoList and add a tab for it
                    firstCanvas = screen.subsurface(canvasRect).copy()
                    undoList.append(firstCanvas) 
                    currentWindow = 0 #we then set the index of the currentWindow to that added canvas

                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)

                    #avoid blitting error
                    if tool == "select":
                        beforeSelect = screen.subsurface(canvasRect).copy()
                        selectClick = False
            
            #if the mouse is on delete window button
            if deleteWindow.collidepoint(mx, my) and writeText != True and drawnPolygon != True and pasteMove == False:
                #if there is more than one tab
                if len(windows) > 1:
                    windows.remove(windows[currentWindow]) #we remove the currentWindow
                    currentWindow -= 1 #set the currentWindow to previous tab in list
                    if currentWindow < 0: #if the currentWindow is negative
                        currentWindow = 0 #we set it to 0
                    screen.blit(windows[currentWindow], (220, 80)) #we blit that previous tab in list to screen
                    #avoid blitting error
                    if tool == "select":
                        beforeSelect = screen.subsurface(canvasRect).copy()
                        selectClick = False
                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)
                #if there is only one tab
                elif len(windows) == 1:
                    windows.remove(windows[currentWindow]) #we remove the last tab
                    currentWindow -= 1
                    screen.blit(backgroundCanvasRect, (220, 80)) #we blit the background of screen over canvasRect to show there is currently no canvas
                    #if tool is select, we set beforeSelect to None and selectClick to false
                    if tool == "select":
                        beforeSelect = None
                        selectClick = False
                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)
                
            
        #checks if user is holding mouse down
        if evt.type == MOUSEBUTTONDOWN:
            
            #creates back copy of whole screen, so that we can blit it when
            #using tools such as stamps or rect so that there won't be multiple
            #instances of them on screen
            if evt.button == 1:
                back = screen.copy()
            
            #checks if it's left click and saves start position of left click
            #for tools like rect or ellipse
            if evt.button == 1: 
                start = evt.pos 
            if evt.button == 4: #check if scroll up
                if tool == "eraser" or tool == "paint" or tool == "sprinkles" or tool == "spray":
                    size += 1 #increase size by 1 for respective tools 
                if tool == "line" or tool == "polygon" or tool == "rect" or tool == "ellipse":
                    if drawnPolygon == False:
                        if filledShape != True or tool == "line":
                            #if user is drawing a line or is not drawing a filled shape
                            thick += 1 #increase thickness by 1
                if tool == "text" and writeText == False: #if tool is text and user is not currently writing text
                    fontSize += 1 #increase fontSize by 1
                if tool == "stamp": #if tool is stamp
                    if scaleSize > 0: #if the 
                        screen.blit(back, (0, 0)) #blit the back copy so there won't be multiple stamps
                        scaleSize -= 1 #decreases size to subtract to make stamp bigger
            if evt.button == 5: #scroll down
                #same logic as above except we decrease the property and check so that it won't be negative
                if tool == "eraser" or tool == "paint" or tool == "sprinkles" or tool == "spray":
                    if size > 1:
                        size -= 1
                if tool == "line" or tool == "polygon" or tool == "rect" or tool == "ellipse":
                    if drawnPolygon == False:
                        if thick > 1:
                            if filledShape != True or tool == "line":
                                thick -= 1
                if tool == "text" and writeText == False:
                    if fontSize > 1:
                        fontSize -= 1
                if tool == "stamp":
                    if scaleSize < 200:
                        scaleSize += 1
                    
                
                        
            #if user clicked undo button
            if undoRect.collidepoint(mx, my) and writeText != True and len(windows) > 0 and drawnPolygon != True and pasteMove == False:
                #checks if undoList has at least 2 elements
                if len(undoList) > 1:
                    undoPic = undoList.pop() #takes out the last element of list
                    #and adds it to end of redoList
                    redoList.append(undoPic)
                    screen.blit(undoList[len(undoList) - 1], (220, 80)) #blits previous canvas of last element to screen
                    if tool == "select":
                        beforeSelect = screen.subsurface(canvasRect).copy() #if user is using select tool, we have to save current copy of screen to beforeSelect
                        #so there won't be blitting error

                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)
                    
            #if user clicked redo button
            if redoRect.collidepoint(mx, my) and writeText != True and len(windows) > 0 and drawnPolygon != True and pasteMove == False:
                #checks if redoList has at least 1 element
                if len(redoList) > 0:
                    redoPic = redoList.pop() #takes out last element of redoList
                    #and adds it to end of undoList
                    undoList.append(redoPic)
                    screen.blit(undoList[len(undoList) - 1], (220, 80)) #blits that canvas as well
                    if tool == "select":
                        beforeSelect = screen.subsurface(canvasRect).copy()

                    #we reset the surface used for highlighter tool
                    highlightBack = Surface((800, 700)).convert()
                    highlightBack.set_alpha(125)
                    highlightBack.fill(col)

        #checks if user is pressing a key down       
        if evt.type == KEYDOWN:
            if evt.key == K_LEFT: #check if left key is pressed
                #same logic as scroll up 
                if tool == "eraser" or tool == "paint" or tool == "spray":
                    if size > 5:
                        size -= 5
                    else:
                        size = 1
                if tool == "sprinkles":
                    if size > 1:
                        size -= 1
                if tool == "line" or tool == "polygon" or tool == "rect" or tool == "ellipse":
                    if drawnPolygon == False:
                        if filledShape != True or tool == "line":
                            if thick > 5:
                                thick -= 5
                            else:
                                thick = 1
                if tool == "text" and writeText == False:
                    if fontSize > 5:
                        fontSize -= 5
                    else:
                        fontSize = 1
                if tool == "stamp":
                    rotate -= 45 #we subtract the rotation value by 45 for stamp
                    #rotation can deal with negatives so no need to check
            if evt.key == K_RIGHT: #check if right key is pressed
                 #same logic as scroll right
                if tool == "eraser" or tool == "paint" or tool == "spray":
                    size += 5
                if tool == "line" or tool == "polygon" or tool == "rect" or tool == "ellipse":
                    if drawnPolygon == False:
                        if filledShape != True or tool == "line":
                            thick += 5
                if tool == "text" and writeText == False:
                    fontSize += 5
                if tool == "sprinkles":
                    size += 1
                if tool == "stamp":
                    rotate += 45
            if evt.key == K_UP: #check if up key is pressed
                if tool == "spray":
                    if speedSpray < 2.0: #increase speed of spray paint (max is 2.0)
                        speedSpray += 0.1  
                if tool == "sprinkles":
                    thick += 1
            if evt.key == K_DOWN: #check down right key is pressed
                 if tool == "spray":
                     if speedSpray > 0.1:
                         speedSpray -= 0.1
                 if tool == "sprinkles":
                     if thick > 1:
                         thick -= 1

            #if user is currently writing text and there is a canvas
            if tool == "text" and writeText == True and len(windows) > 0:
                screen.blit(preText, (220, 80)) #we blit the canvas before user starteed typing
                #(avoinf overlap of text)
                if evt.key in range(K_BACKSPACE, K_KP_EQUALS + 1): #we check what key the user clicked (all the keys between backspace and kp equals)
                    if evt.key == K_BACKSPACE: #if user backspaced
                        text = text[:-1] #we delete last letter of text (only take string before last letter)
                    else: #otherwise the user pressed a normal key
                        letter = evt.unicode #we get unicode of that key and add it to text string
                        text = text + letter
                #checks if user is already typing something
                if text != "" and writeText == True:
                    currentFontDisplay = font.SysFont(currentFont, fontSize) #creates font using current font and font size
                
                    if bold == True:
                        currentFontDisplay = font.SysFont(currentFont, fontSize, bold = True) #bold the font if bold is true
                    if italicize == True:
                        currentFontDisplay = font.SysFont(currentFont, fontSize, bold = False, italic = True) #italicize the font if italicize is true
                        if bold == True:
                            currentFontDisplay = font.SysFont(currentFont, fontSize, bold = True, italic = True) #check if user also bolded font
                    if underline == True:
                        currentFontDisplay.set_underline(True) #set underline if underline is true
                    displayText = currentFontDisplay.render(text, True, col) #render the text using current colour and setted font
                    screen.set_clip(canvasRect) #makes sures the text only stays on canvas
                    if textAlign == "left": #if text align is left, we just blit the font at the start point user clicked before typing text
                        screen.blit(displayText, startText)
                    if textAlign == "center": #if text align is center, we have to get the rect of the display text, and find it's center x coor
                        displayTextRect = displayText.get_rect()
                        displayPosCenter = displayTextRect.centerx
                        screen.blit(displayText, (startText[0] - displayPosCenter, startText[1])) #then we have to subtract that center x coor from the x of the start
                        #pos to make text centered
                    if textAlign == "right":
                        displayTextRect = displayText.get_rect() #if text align is center, we have to get the rect of the display text, and find it's right x coor
                        displayPosRight = displayTextRect.right
                        screen.blit(displayText, (startText[0] - displayPosRight, startText[1]))#then we have to subtract that right x coor from the x of the start
                        #pos to make text right aligned
                    display.flip() #update current screen
                    screen.set_clip(None)




        #check if the tool is text 
        if tool == "text":
            #we have to blit the images and rects for the buttons of the text options
            screen.blit(boldButton, (1000, 300))
            screen.blit(italicizeButton, (1100, 300))
            screen.blit(underlineButton, (1200, 300))

            #we check if each property is true or false, and if it's true or if user collides with it, we draw a red rect
            #instead of a blue rect to show user selected it. if user clicked it again, we change that property to false
            #drawing a blue rect instead
            if bold == True:
                draw.rect(screen, RED, boldRect, 2)
                if mb[0] == 1 and writeText != True and boldRect.collidepoint(mx, my):
                    bold = False
                    draw.rect(screen, BLUE, boldRect, 2)
            else:
                draw.rect(screen, BLUE, boldRect, 2)
                if mb[0] == 1 and writeText != True and boldRect.collidepoint(mx, my):
                    bold = True
                    draw.rect(screen, RED, boldRect, 2)
                    
            if italicize == True:
                draw.rect(screen, RED, italicizeRect, 2)
                if mb[0] == 1 and writeText != True and italicizeRect.collidepoint(mx, my):
                    italicize = False
                    draw.rect(screen, BLUE, italicizeRect, 2)
            else:
                draw.rect(screen, BLUE, italicizeRect, 2)
                if mb[0] == 1 and writeText != True and italicizeRect.collidepoint(mx, my):
                    italicize = True
                    draw.rect(screen, RED, italicizeRect, 2)
                    
            if underline == True:
                draw.rect(screen, RED, underlineRect, 2)
                if mb[0] == 1 and writeText != True and underlineRect.collidepoint(mx, my):
                    underline = False
                    draw.rect(screen, BLUE, underlineRect, 2)
            else:
                draw.rect(screen, BLUE, underlineRect, 2)
                if mb[0] == 1 and writeText != True and underlineRect.collidepoint(mx, my):
                    underline = True
                    draw.rect(screen, RED, underlineRect, 2)

                    
    mx, my = mouse.get_pos() #gets current mouse position
    draw.rect(screen, GREEN, (3, 3, 70, 21)) #draws rect to act as background for displaying current mouse pos as text
    currentPosDisplay = font.SysFont("BigNoodleTooOblique", 20) #creates the font to display the mouse pos
    displayPos = currentPosDisplay.render("(" + str(mx) + ", " + str(my) + ")", True, (0, 0, 0)) #render the mouse pos as text
    screen.blit(displayPos, (3, 3)) #display the mouse pos on screen
    mb = mouse.get_pressed() #checks if mouse is pressed

    ########################################################################
    ########################## WINDOWS AND TABS ############################
    tabx = 220 #x coordinate for the tabRect
    screen.blit(tabBack, (220, 30)) #overwrite all the tabs so we can draw them again each iteration 
    for tab in windows: #check all canvas windows user has
        tabFontDisplay = font.SysFont("BigNoodleTooOblique", 20)  #creates the font to display the window num
        tabText = "Window " + str(windows.index(tab) + 1) #text that display window num (index + 1)
        displayTabText = tabFontDisplay.render(tabText, True, (0, 0, 0))
        screen.blit(displayTabText, (tabx, 30)) #blits it at tabx, 30
        tabRect = draw.rect(screen, BLUE, (tabx, 30, 80, 20), 2) #physical display rect so user can select each tab
        if windows[currentWindow] == windows[windows.index(tab)]: #if the current window is equal (ssame index) to this tab we are checking
            tabFontDisplay = font.SysFont("BigNoodleTooOblique", 20)
            tabText = "Window " + str(currentWindow + 1)
            displayTabText = tabFontDisplay.render(tabText, True, (0, 0, 0))
            screen.blit(displayTabText, (tabx, 30))
            tabRect = draw.rect(screen, RED, (tabx, 30, 80, 20), 2) #we draw a red rect instead  to show it is current tab  
        if tabRect.collidepoint(mx, my) and writeText != True and drawnPolygon != True and pasteMove == False: #if the mouse is on a tab
            tabRect = draw.rect(screen, RED, (tabx, 30, 80, 20), 2) #we draw a red rect to show user is colliding with it
            if mb[0] == 1: #if user clicks that tab
                
                #we blit beforeSelect if there is a select area to remove it
                if selectClick == True and beforeSelect != None:
                    screen.blit(beforeSelect, (220, 80))

                #we have to remove beforeSelect if user uses select tool so it won't cause blitting error on other window
                if beforeSelect != None:
                    screen.blit(beforeSelect, (220, 80))
                    beforeSelect = None
                prevWindow = currentWindow #set the previous window to currentWindow index
                currentWindow = windows.index(tab) #find index of tab user selected and set to current window
                windows.remove(windows[prevWindow]) #remove that previous window and insert a new copy of canvas to it at same index (update current canvas)
                windows.insert(prevWindow, screen.subsurface(canvasRect).copy())
                windowDisplay = windows[currentWindow] #get canvas instance for current tab and blits it
                screen.blit(windowDisplay, (220, 80))

                #refresh our highlighter surface
                highlightBack = Surface((800, 700)).convert()
                highlightBack.set_alpha(125)
                highlightBack.fill(col)

                #update beforeSelect
                if tool == "select":
                    beforeSelect = screen.subsurface(canvasRect).copy()
                     
        tabx += 90 #increase tabx by 90 and loop continues until all tabs are drawn
         
        
    
    ##################################### POLYGON TOOL LINES #################################################
    #if user is currently drawing polygon
    if tool == "polygon" and mb[0] == 0 and drawnPolygon == True and startPoint != None and prevLine != None:
        screen.set_clip(canvasRect)
        screen.blit(prevLine, (0, 0)) #we have to blit the prevLine copy so there are no multiple lines
        draw.line(screen, col, polygonPoint, (mx, my), thick) #draw line from last polygonpoint to current point
        screen.set_clip(None)

    ########################################################################

    ########################## SELECTING TOOL ##############################
    #checks to see if the select rect (button) for that tool is pressed (left click)
    #and if mouse is on button, and changes the tool vairable to that tool. also
    #draws red outline rect over selected tool and sets outline of all other tools
    #back to blue to show that it's selected

    if writeText != True and drawnPolygon != True and pasteMove == False:
        for rectangle in toolsList: #check all rects in toolsList
            toolRect = draw.rect(screen, BLUE, rectangle, 2) #we draw a blur rectangle over all tools rect
            if toolRect.collidepoint(mx, my): #but if user collides wit one, we change it to red to show user is hovering over it
                toolRect = draw.rect(screen, RED, rectangle, 2)
                if mb[0] == 1: #if they click over it, we set prev tool to current tool, and change the current tool
                    #by finding index of the rectangle and getting string with same index from toolsNames(all tools in order)
                     prevTool = tool
                     tool = toolsNames[toolsList.index(rectangle)]
                     if tool == "select":
                         beforeSelect = screen.subsurface(canvasRect).copy()
                         #copies canvas to beforeSelect if user selects select tool
                     else:
                         #if there is still a select area, we have to blit the beforeSelect and set it to none and set selectClick to false to remove it
                         if selectClick == True and beforeSelect != None:
                             screen.blit(beforeSelect, (220, 80))
                             selectClick = False
                             beforeSelect = None
                             
                     if tool == "paint":
                         #refresh our highlighter surface
                         highlightBack = Surface((800, 700)).convert()
                         highlightBack.set_alpha(125)
                         highlightBack.fill(col)

            #if current tool is equal to the rectangle we are checking, we draw red rect to show it's current tool
            if toolsNames.index(tool) == toolsList.index(rectangle):
                draw.rect(screen, RED, rectangle, 2)


    ############################################# SIDE BAR ###################################################################
    if tool != prevTool:
        screen.blit(backgroundSurface, (979, 109)) # we only erase everything from side bar if the tool is different (efficiency)
    if tool == "stamp":
        #displays text for stamp and background buttons
        currentFontDisplay = font.SysFont("BigNoodleTooOblique", 20)
        displayText = currentFontDisplay.render("Stamps", True, (0, 0, 0))
        screen.blit(displayText, (1090, 400))

        displayText = currentFontDisplay.render("Backgrounds", True, (0, 0, 0))
        screen.blit(displayText, (1200, 400))

        #draw those rectangle buttons
        draw.rect(screen, BLUE, stampSelectRect, 2)
        draw.rect(screen, BLUE, backgroundSelectRect, 2)

        #if currentStampSelect is equal to the selected tool or if mouse collides then we draw a red rect
        #if user clicks on other tool, we select other tool instead
        if stampSelectRect.collidepoint(mx, my):
            draw.rect(screen, RED, stampSelectRect, 2)
            if mb[0] == 1:
                currentStampSelect = "stamp"
                screen.blit(backgroundSurface, (979, 109))
        if backgroundSelectRect.collidepoint(mx, my):
            draw.rect(screen, RED, backgroundSelectRect, 2)
            if mb[0] == 1:
                currentStampSelect = "background"
                screen.blit(backgroundSurface, (979, 109))

        #if the user is using stamp option
        if currentStampSelect == "stamp":
            draw.rect(screen, RED, stampSelectRect, 2) 
            porx = 980
            pory = 110
            #draw all character stamp portraits and if user selects, we set currentStamp to whatever they selected, (same logic as tool select)
            for portrait in portraitList:
                blit_alpha(screen, portrait, (porx, pory), 5) #function for cool fade in effect by blitting the image with a low transparency until it reaches
                #255
                portraitRect = draw.rect(screen, (255, 255, 255), (porx, pory, 56, 50), 2)
                if portraitRect.collidepoint(mx, my):
                    screen.blit(portrait, (porx, pory))
                    portraitRect = draw.rect(screen, RED, (porx, pory, 56, 50), 2)
                    if mb[0] == 1:
                        currentStamp = portraitList.index(portrait)
                        #reset rotate and size values
                        rotate = 0
                        scaleSize = 0
                if portrait == portraitList[currentStamp]:
                    portraitRect = draw.rect(screen, RED, (porx, pory, 56, 50), 2)
                if porx > 1300:
                    pory += 70
                    porx = 900
                porx += 80
        if currentStampSelect == "background":
            #same as above except for backgrounds
            draw.rect(screen, RED, backgroundSelectRect, 2)
            backgroundx = 980
            backgroundy = 110
            for background in backgroundPortraits:
                blit_alpha(screen, background, (backgroundx, backgroundy), 5)
                backgroundRect = draw.rect(screen, (255, 255, 255), (backgroundx, backgroundy, 120, 100), 2)
                if backgroundRect.collidepoint(mx, my):
                    screen.blit(background, (backgroundx, backgroundy))
                    backgroundRect = draw.rect(screen, RED, (backgroundx, backgroundy, 120, 100), 2)
                    if mb[0] == 1:
                        currentBackground = backgroundPortraits.index(background)
                if background == backgroundPortraits[currentBackground]:
                    backgroundRect = draw.rect(screen, RED, (backgroundx, backgroundy, 120, 100), 2)
                if backgroundx > 1200:
                    backgroundy += 120
                    backgroundx = 850
                backgroundx += 130
    elif tool == "text": # if tool is text
        #if user is writing text, we have to add confirm and decline buttons 
        if writeText == True:
            screen.blit(confirmButton, (1050, 350))
            screen.blit(declineButton, (1150, 350))
            draw.rect(screen, BLUE, confirmText, 2)
            draw.rect(screen, BLUE, declineText, 2)
        #if user isn't writing we draw buttons for text options
        else:
            #displays current font size
            screen.blit(currentSizeBack, (1049, 210))
            currentSizeDisplay = font.SysFont("BigNoodleTooOblique", 30)
            displaySize = currentSizeDisplay.render("Current Font Size: " + str(fontSize), True, (0, 0, 0))
            screen.blit(displaySize, (1050, 210))
            fontx = 1000
            fonty = 125
            #same logic as tool select, except we render each respective font name in fontList before  drawing
            #rect; if user clicks on it, then we set currentFont to that fot
            for fontType in fontsList:
                #shortened font name if font is Times, or BigNoodle
                if fontType == "Times New Roman":
                    currentFontDisplay = font.SysFont(fontType, 20)
                    displayText = currentFontDisplay.render("Times", True, (0, 0, 0))
                    screen.blit(displayText, (fontx, fonty))
                elif fontType == "BigNoodleTooOblique":
                    currentFontDisplay = font.SysFont(fontType, 20)
                    displayText = currentFontDisplay.render("Big Noodle", True, (0, 0, 0))
                    screen.blit(displayText, (fontx, fonty))
                else:
                    currentFontDisplay = font.SysFont(fontType, 20)
                    displayText = currentFontDisplay.render(fontType, True, (0, 0, 0))
                    screen.blit(displayText, (fontx, fonty))
                fontRect = draw.rect(screen, (255, 255, 255), (fontx, fonty, 85, 30), 2)
                if fontRect.collidepoint(mx, my):
                    fontRect = draw.rect(screen, RED, (fontx, fonty, 85, 30), 2)
                    if mb[0] == 1:
                        currentFont = fontType
                if fontType == fontsList[fontsList.index(currentFont)]:
                    fontRect = draw.rect(screen, RED, (fontx, fonty, 85, 30), 2)
                if fontx >= 1200:
                    fonty += 50
                    fontx = 900
                fontx += 100

            #blit align buttons images 
            screen.blit(leftAlignButton, (1000, 250))
            screen.blit(centerAlignButton, (1100, 250))
            screen.blit(rightAlignButton, (1200, 250))

            #same logic as stamp and background buttons; if one is selected we draw red box to show that;
            #other it's a blur box unless user collides point; and if user clicks on a button, we set current align to that button
            if writeText != True and leftAlign.collidepoint(mx, my):
                draw.rect(screen, RED, leftAlign, 2)
                if mb[0] == 1:
                    textAlign = "left"
            else:
                draw.rect(screen, BLUE, leftAlign, 2)
                
            if writeText != True and centerAlign.collidepoint(mx, my):
                draw.rect(screen, RED, centerAlign, 2)
                if mb[0] == 1:
                    textAlign = "center"
            else:
                draw.rect(screen, BLUE, centerAlign, 2)
                
            if writeText != True and rightAlign.collidepoint(mx, my):
                draw.rect(screen, RED, rightAlign, 2)
                if mb[0] == 1:
                    textAlign = "right"
            else:
                draw.rect(screen, BLUE, rightAlign, 2)
        
            if textAlign == "left":
                draw.rect(screen, RED, leftAlign, 2)
            
            elif textAlign == "center":
                draw.rect(screen, RED, centerAlign, 2)

            elif textAlign == "right":
                draw.rect(screen, RED, rightAlign, 2)
    
    if tool == "paint" or tool == "eraser" or tool == "spray" or tool == "sprinkles":
        #for all these tools, we dislay curren size as text on screen
        screen.blit(currentSizeBack, (1049, 210))
        currentSizeDisplay = font.SysFont("BigNoodleTooOblique", 30)
        displaySize = currentSizeDisplay.render("Current Size: " + str(size), True, (0, 0, 0))
        screen.blit(displaySize, (1090, 211))
        #certain tool have more stuff to display, like speed for spray paint
        if tool == "sprinkles":
            displaySize = currentSizeDisplay.render("Current Thickness: " + str(thick), True, (0, 0, 0))
            screen.blit(displaySize, (1090, 235))
        if tool == "spray":
            displaySize = currentSizeDisplay.render("Current Speed: " + str(round(speedSpray, 1)), True, (0, 0, 0))
            screen.blit(displaySize, (1090, 235))
        if tool == "paint":
            #display brush and highlighter buttons if tool is paint
            screen.blit(brushButton, (1100, 150))
            screen.blit(highlightButton, (1200, 150))
            draw.rect(screen, BLUE, brushRect, 2)
            draw.rect(screen, BLUE, highlightRect, 2)
            #same logic as align buttons
            if paint == "brush":
                draw.rect(screen, RED, brushRect, 2)
                if highlightRect.collidepoint(mx, my):
                    draw.rect(screen, RED, highlightRect, 2)
                    if mb[0] == 1:
                        paint = "highlight"
            elif paint == "highlight":
                draw.rect(screen, RED, highlightRect, 2)
                if brushRect.collidepoint(mx, my):
                    draw.rect(screen, RED, brushRect, 2)
                    if mb[0] == 1:
                        paint = "brush"
                
    if tool == "line" or tool == "polygon":
        #displat current size for line and polygon tool as well
        screen.blit(currentSizeBack, (1049, 210))
        currentSizeDisplay = font.SysFont("BigNoodleTooOblique", 30)
        displaySize = currentSizeDisplay.render("Current Thickness: " + str(thick), True, (0, 0, 0))
        screen.blit(displaySize, (1090, 211))
        #if tool is polygon, we have to put options for filled and unfilled shapes
        #same logic as align
        if tool == "polygon":
            screen.blit(filledButton, (1100, 150))
            screen.blit(nonfilledButton, (1200, 150))
            filledShapeRect = draw.rect(screen, BLUE, (1100, 150, 50, 50), 2)
            outlineShapeRect = draw.rect(screen, BLUE, (1200, 150, 50, 50), 2)
            if filledShape == True:
                screen.blit(currentSizeBack, (1049, 210))
                filledShapeRect = draw.rect(screen, RED, (1100, 150, 50, 50), 2)
                if outlineShapeRect.collidepoint(mx, my):
                    outlineShapeRect = draw.rect(screen, RED, (1200, 150, 50, 50), 2)
                    if mb[0] == 1:
                        filledShape = False
            else:
                screen.blit(currentSizeBack, (1049, 210))
                currentSizeDisplay = font.SysFont("BigNoodleTooOblique", 30)
                displaySize = currentSizeDisplay.render("Current Thickness: " + str(thick), True, (0, 0, 0))
                screen.blit(displaySize, (1090, 211))
                outlineShapeRect = draw.rect(screen, RED, (1200, 150, 50, 50), 2)
                if filledShapeRect.collidepoint(mx, my):
                    filledShapeRect = draw.rect(screen, RED, (1100, 150, 50, 50), 2)
                    if mb[0] == 1:
                        filledShape = True  
    if tool == "ellipse" or tool == "rect":
        #if tool is ellipse or rect, we have to put options for filled and unfilled shapes
        #same logic as align
        screen.blit(filledButton, (1100, 150))
        screen.blit(nonfilledButton, (1200, 150))
        filledShapeRect = draw.rect(screen, BLUE, (1100, 150, 50, 50), 2)
        outlineShapeRect = draw.rect(screen, BLUE, (1200, 150, 50, 50), 2)
        
        if filledShape == True:
            screen.blit(currentSizeBack, (1049, 210))
            filledShapeRect = draw.rect(screen, RED, (1100, 150, 50, 50), 2)
            if outlineShapeRect.collidepoint(mx, my):
                outlineShapeRect = draw.rect(screen, RED, (1200, 150, 50, 50), 2)
                if mb[0] == 1:
                    filledShape = False
        else:
            screen.blit(currentSizeBack, (1049, 210))
            currentSizeDisplay = font.SysFont("BigNoodleTooOblique", 30)
            displaySize = currentSizeDisplay.render("Current Thickness: " + str(thick), True, (0, 0, 0))
            screen.blit(displaySize, (1090, 211))
            outlineShapeRect = draw.rect(screen, RED, (1200, 150, 50, 50), 2)
            if filledShapeRect.collidepoint(mx, my):
                filledShapeRect = draw.rect(screen, RED, (1100, 150, 50, 50), 2)
                if mb[0] == 1:
                    filledShape = True
                    
    if tool == "filter":
        #if tool is filter, we add sepia, and black and white buttons
        screen.blit(sepiaButton, (1100, 150))
        screen.blit(blackAndWhiteButton, (1200, 150))
       
        sepiaRect = draw.rect(screen, BLUE, (1100, 150, 50, 50), 2)
        blackAndWhiteRect = draw.rect(screen, BLUE, (1200, 150, 50, 50), 2)
        if sepiaRect.collidepoint(mx, my):
            sepiaRect = draw.rect(screen, RED, (1100, 150, 50, 50), 2)
            if mb[0] == 1 and len(windows) > 0 and pasteMove == False:
                #if user clicked sepia, we have a for loop to loop all pixels on canvas and
                #manpulate r, g, b values using formula for sepia; we have to append canvas
                #to undoList because of change 
                for x in range(220, 971): 
                    for y in range(80, 681):
                        r, g, b, a = screen.get_at((x, y))
                        r2 = min(255, int(r*.393 + g *.769 + b*.189))
                        g2 = min(255, int(r*.349 + g *.686 + b*.168))
                        b2 = min(255, int(r*.272 + g *.534 + b*.131))
                        screen.set_at((x, y), (r2, g2, b2))
                display.flip()
                undoList.append(screen.subsurface(canvasRect).copy())
                del redoList[:]
                filterType = "sepia"
                
        elif filterType != "sepia":
            sepiaRect = draw.rect(screen, BLUE, (1100, 150, 50, 50), 2)

        if blackAndWhiteRect.collidepoint(mx, my):
            blackAndWhiteRect = draw.rect(screen, RED, (1200, 150, 50, 50), 2)
            if mb[0] == 1 and len(windows) > 0 and pasteMove == False:
                #same as sepia above except for b/w
                for x in range(220, 971): 
                    for y in range(80, 681):
                        r, g, b, a = screen.get_at((x, y))
                        r2 = min(255, int((r + g + b) / 3))
                        g2 = min(255, int((r + g + b) / 3))
                        b2 = min(255, int((r + g + b) / 3))
                        screen.set_at((x, y), (r2, g2, b2))
                display.flip()
                undoList.append(screen.subsurface(canvasRect).copy())
                del redoList[:]
                filterType = "b/w"

        elif filterType != "b/w":
            blackAndWhiteRect = draw.rect(screen, BLUE, (1200, 150, 50, 50), 2)

    #checks if clear rect collidepoints and makes it red
    #does same thing with other rects that are not tools
    if clearRect.collidepoint(mx, my):
        draw.rect(screen, RED, clearRect, 2)
    else:
        draw.rect(screen, BLUE, clearRect, 2)

    if undoRect.collidepoint(mx, my):
        draw.rect(screen, RED, undoRect, 2)
    else:
        draw.rect(screen, BLUE, undoRect, 2)

    if redoRect.collidepoint(mx, my):
        draw.rect(screen, RED, redoRect, 2)
    else:
        draw.rect(screen, BLUE, redoRect, 2)

    if copyRect.collidepoint(mx, my):
        draw.rect(screen, RED, copyRect, 2)
    else:
        draw.rect(screen, BLUE, copyRect, 2)

    if cutRect.collidepoint(mx, my):
        draw.rect(screen, RED, cutRect, 2)
    else:
        draw.rect(screen, BLUE, cutRect, 2)

    if pasteRect.collidepoint(mx, my):
        draw.rect(screen, RED, pasteRect, 2)
    else:
        draw.rect(screen, BLUE, pasteRect, 2)

    if addWindow.collidepoint(mx, my):
        draw.rect(screen, RED, addWindow, 2)
    else:
        draw.rect(screen, BLUE, addWindow, 2)

    if deleteWindow.collidepoint(mx, my):
        draw.rect(screen, RED, deleteWindow, 2)
    else:
        draw.rect(screen, BLUE, deleteWindow, 2)

    if openRect.collidepoint(mx, my):
        draw.rect(screen, RED, openRect, 2)
    else:
        draw.rect(screen, BLUE, openRect, 2)

    if saveRect.collidepoint(mx, my):
        draw.rect(screen, RED, saveRect, 2)
    else:
        draw.rect(screen, BLUE, saveRect, 2)
    ########################################################################

    ########################## USING THE TOOL ##############################
    #checks if user left clicks, mouse is on canvas and if they have at least one window
    if canvasRect.collidepoint(mx, my) and mb[0] == 1 and len(windows) > 0 and writeText != True and drawnPolygon != True and pasteMove == False:
        screen.set_clip(canvasRect) #only allows the canvas to be modified
        if tool == "pencil": #checks what tool user currently selected
            draw.line(screen, col, (omx, omy), (mx, my), 1)
            #draws line on screen from previous point from last iteration of
            #loop to current mouse point 
        if tool == "eraser":
            draw.circle(screen, WHITE, (mx, my), size)
            #draws white circles (erase) on screen at current mouse point at which size
            #user selected
            dx = mx - omx #finds x distance between previous point and current point
            dy = my - omy #finds y distance between previous point and current point
            dist = int(sqrt(dx**2 + dy **2)) #finds hypotenuse from ds and dy
            for i in range(1, dist + 1): #start at next point and end at last point
                cx = int(omx + i * dx / dist) #horizontal move (run)
                cy = int(omy + i * dy / dist) #vertical move (rise)
                draw.circle(screen, WHITE, (cx, cy), size) #draws circle at (cx, cy)
                #loop continues until whole line is filled with circles (no holes)

            #refresh highlight surface
            highlightBack = Surface((800, 700)).convert()
            highlightBack.set_alpha(125)
            highlightBack.fill(col)
        if tool == "paint":
            if paint == "brush":
                #same logic as eraser, except circles are drawn in current colour (paint)
                dx = mx - omx 
                dy = my - omy 
                dist = int(sqrt(dx**2 + dy ** 2))
                for i in range(1, dist + 1): #start at next point and end at last point
                    cx = int(omx + i * dx / dist) #horizontal move (run)
                    cy = int(omy + i * dy / dist) #vertical move (rise)
                    draw.circle(screen, col, (cx, cy), size)
            elif paint == "highlight":
                #we use try and except in case error comes up if subsurface outside surface
                try:
                    highlightHead = highlightBack.subsurface([mx - 220, my - 80, size * 2, size * 2]).copy() #get subsurface of highlighter surface
                    #according to size at mx, my pos and copies it (mx - 220 and my - 80 because canvasRect does not start at (0, 0) like surface)
                    if col != (0, 0, 0): #we check if current col is (0, 0, 0) because we have to draw black rect over subsurface taken and "remove" it using colourkey
                        #which won't work if colour is completely (0, 0, 0), so we alter the values by 1 a little bit
                        draw.rect(highlightBack, (0, 0, 0), [mx - 220, my - 80, size * 2, size * 2]) #draws black rect over that subsurface
                        highlightBack.set_colorkey((0, 0, 0)) #set colorkey of anything black in that subsurface so that it won't appear when blitting subsurface
                    else:
                        draw.rect(highlightBack, (1, 1, 1), [mx - 220, my - 80, size * 2, size * 2]) #draws black rect over that subsurface
                        highlightBack.set_colorkey((1, 1, 1)) #set colorkey of anything black in that subsurface so that it won't appear when blitting subsurface
                    #again unless we refresh surface again (we do this so that alpha transpancy won't overlap and look ugly) (we refresh whenever screen is cleared,
                    #erase is used, switch to new tab, etc)
                    screen.blit(highlightHead, (mx - size, my - size)) #blit the transparent surface to canvas
                except:
                    pass
        
        if tool == "line":
            screen.blit(back, (0, 0)) #blits copy of screen under line so only one
            #line is drawn when user lets go of mouse
            draw.line(screen, col, start, (mx, my), thick)
            #draws line from start point where mouse was first clicked to current point
            #at thickness user selected
        if tool == "rect":
            screen.blit(back, (0, 0)) #blits back copy
            #checks for unfilled and filled
            if filledShape == True:  
                draw.rect(screen, col, (start[0], start[1], mx - start[0], my - start[1]))
            else:
                draw.rect(screen, col, (start[0], start[1], mx - start[0], my - start[1]), thick)
                #took a while to figured out unfilled rect without weird corners; basically you have to
                #draw a rectangle with length of 1, and draw another rect around that and another around that
                #with length of 1 until you reach thickness; i used draw polygon instead of rect because i
                #wanted to deal with actual points, and through where the mx, my is relative to start point,
                #i calculated how much to subtract or add to the point the rectSize that was increasing each time
                #in the for loop 
                for rectSize in range(thick + 1):
                    if mx >= start[0] and my <= start[1]: #mouse right of start and up
                        point1 = (start[0] - rectSize, start[1] + rectSize)
                        point2 = (mx + rectSize, start[1] + rectSize)
                        point3 = (mx + rectSize, my - rectSize)
                        point4 = (start[0] - rectSize, my - rectSize)
                    elif mx >= start[0] and my >= start[1]: #mouse right of start and down
                        point1 = (start[0] - rectSize, start[1] - rectSize)
                        point2 = (mx + rectSize, start[1] - rectSize)
                        point3 = (mx + rectSize, my + rectSize)
                        point4 = (start[0] - rectSize, my + rectSize)
                    elif mx <= start[0] and my >= start[1]: #mouse left of start and down
                        point1 = (start[0] + rectSize, start[1] - rectSize)
                        point2 = (mx - rectSize, start[1] - rectSize)
                        point3 = (mx - rectSize, my + rectSize)
                        point4 = (start[0] + rectSize, my + rectSize)
                    elif mx <= start[0] and my <= start[1]: #mouse left of start and up
                        point1 = (start[0] + rectSize, start[1] + rectSize)
                        point2 = (mx - rectSize, start[1] + rectSize)
                        point3 = (mx - rectSize, my - rectSize)
                        point4 = (start[0] + rectSize, my - rectSize)
                    draw.polygon(screen, col, [point1, point2, point3, point4], 1)
                    
            #draws rect starting from start point and using the distance travelled
            #between the x of current point and x coor of start as width, and distance
            #travelled between y of current point and y coor of start as height
        if tool == "ellipse":
            screen.blit(back, (0, 0)) #blits back copy
            ellRect = Rect(start[0], start[1], mx - start[0], my - start[1])
            #same logic as drawing rectangle, except we have to consider negative
            #or zero widths and heights as well
            ellRect.normalize() #if there are, change all negative values to positive
            if filledShape == True:
                draw.ellipse(screen, col, ellRect) #we then draw the ellipse
            else:
                #for unfilled ellipse, if thickness is bigger than radius, than it will throw error, so we have to use try and except
                #and only draw ellipse if radius is big enough
                try:
                    draw.ellipse(screen, col, ellRect, thick)
                except:
                    draw.ellipse(screen, col, ellRect) #draws a filled ellipse instead to look like thickness overlaps
        if tool == "sprinkles":
            rx  = randint(-size, size) #generates random num between current size and negative of it
            ry = randint(-size, size) #generates random num between current size and negative of it
            draw.line(screen, col, (mx, my), (mx + rx, my + ry), thick)
            #draws a line from current point to another point with the x coordinate being
            #the x of current point added with random num from rx, and the y coordinate being
            #the y of current point added with random num from ry (result being many random lines
            #drawn from central point after many iterations)
        if tool == "fill":
            oldCol = screen.get_at((mx, my)) #get colour where user clicked
            floodFill(mx, my, oldCol, col) #call floodFill
        if tool == "spray":
            #help from http://compsci.ca/v3/viewtopic.php?t=30507
            for i in range (int(size ** speedSpray)): #multiplies radius by speed (default 1.5), how much dots to draw per iteration
                sx = randint(mx - size, mx + size) #generates random num between current size and negative of it
                sy = randint(my - size, my + size) #generates random num between current size and negative of it
                if ((mx - sx) ** 2 + (my - sy) ** 2) ** 0.5 <= size: #checks if distance of sx, sy is less than or equal to the radius from mx, my (inside circle)
                    draw.line(screen, col, (sx, sy), (sx, sy)) #draws a point (using lines)
        if tool == "select":
            #if user hasn't already selected an area
            if selectClick == False:
                screen.blit(beforeSelect, (220, 80)) #blit beforeSelect
                selectArea = draw.rect(screen, (0, 0, 0), (start[0], start[1], mx - start[0], my - start[1]), 1)
                #draws a rectangle to allow user to select area
            #if they did select area 
            if selectClick == True:
                screen.blit(beforeSelect, (220, 80)) #blit beforeSelect
                selectClick = False #set selectClick to false so user can select another area again
        #unused triangle tool code         
        '''
        if tool == "triangle":
            screen.blit(back, (0, 0))
            draw.line(screen, col, start, (mx, my), size)
            draw.line(screen, col, start, [start[0] + (mx - start[0]), start[1]], size)
            draw.line(screen, col, [start[0] + (mx - start[0]), start[1]], (mx, my), size)
        '''
        if tool == "polygon":
            #if user not already drawing polygon
            if drawnPolygon == False:
                screen.blit(back, (0, 0))#blit back
                firstCopy = screen.copy() #copies screen before user draws polygon 
                startPoint = mx, my #gets start point as where user clicked
                draw.circle(screen, col, startPoint, thick + 2) #draws crcle at that point to show user first point to click again to finish drawing polygon
                polygonPoint = startPoint #sets previous polygon point to start point
                polygonList.append(polygonPoint) #appends that point to the polygonList
                prevLine = screen.copy() #copies the screen for prevLine
            #if user already drawing polygon
            if drawnPolygon == True:
                screen.blit(back, (0, 0)) #blit back
                draw.line(screen, col, polygonPoint, (mx, my), thick) #draw a line from the previous point clicked to current mx, my
            #drawing polygon resolves in event loop after MOUSEBUTTONUP 
        if tool == "text":
            #if user is not writing text
            if writeText == False:
                #get start point of where they clicked for text to blit from
                startText = mx, my
                preText = screen.subsurface(canvasRect).copy() #gets copy of canvas to blit when writing text (no overlap)
                writeText = True #sets writing text to true
            #drawing text resolves in event loop after MOUSEBUTTONUP 
        if tool == "stamp":
            #if user is using stamps
            if currentStampSelect == "stamp":
                screen.blit(back, (0, 0))
                #gets width and height of currentStamp pic
                stampWidth = stampList[currentStamp].get_width() 
                stampHeight = stampList[currentStamp].get_height()
                #rotates stamp according to rotate value
                stamp = transform.rotate(stampList[currentStamp], rotate)
                #transfroms dimensions by subtracting scaleSize value from width and height
                stamp = transform.scale(stamp, (stampHeight - scaleSize, stampHeight - scaleSize))
                #gets new width and height of stamp after transformed
                stampWidth = stamp.get_width() 
                stampHeight = stamp.get_height()
                #blits the pic current mouse pos according to center of image (subtract mx and my from width and height divided by 2)
                screen.blit(stamp, (mx - (stampWidth) / 2, my - (stampHeight) / 2))
                beforeSelect = screen.subsurface(canvasRect).copy() #updates beforeSelect
            #if user is using backgrounds
            if currentStampSelect == "background":
                #blits currentBackground to whole canvas
                screen.blit(backgroundsList[currentBackground], (220, 80))
                beforeSelect = screen.subsurface(canvasRect).copy() #updates beforeSelect
            
        screen.set_clip(None) #allows user to modify everything after they are done using tool
    
        
    #######SELECT TOOL######
    #if user selected an area using select tool
    if selectClick == True and pasteMove == False and drawnPolygon != True and writeText != True:
        #if user clicked copy button
        if copyRect.collidepoint(mx, my) and mb[0] == 1:
            #only copies if there is a select area
            if selectArea != None and beforeSelect != None:
                screen.blit(beforeSelect, (220, 80)) #we blit canvas before user selected area (remove select rect from canvas)
                copy = screen.subsurface(selectArea).copy() #we get subsurface of the selectArea and save it to copy
                selectArea = None #remove the select area and set selectClick to false so user can select another area
                selectClick = False 
                beforeSelect = screen.subsurface(canvasRect).copy() #update beforeSelect
        #if user clicked cut button
        if cutRect.collidepoint(mx, my) and mb[0] == 1:
            #same logic as above except you save it to cut var and you draw a white rect over that selected area to show you cutted
            if selectArea != None and beforeSelect != None:
                screen.blit(beforeSelect, (220, 80))
                cut = screen.subsurface(selectArea).copy()
                draw.rect(screen, WHITE, selectArea)
                undoList.append(screen.subsurface(canvasRect).copy())
                del redoList[:]
                selectArea = None
                selectClick = False
                beforeSelect = screen.subsurface(canvasRect).copy()

    #if user clicked paste
    if pasteRect.collidepoint(mx, my) and mb[0] == 1 and pasteMove == False and drawnPolygon != True and writeText != True and len(windows) > 0:
        #if copy or cut has a subsurface, then we set pasteMove to true and lock all other functions
        if copy != None or cut != None:
            pasteMove = True
        #we also check if there is a select area still on screen from select tool
        if selectClick == True and beforeSelect != None and tool == "select":
            #we bilt before select and set selectArea and selectClick to None and Flase and update beforeSelect
            screen.blit(beforeSelect, (220, 80))
            selectArea = None
            selectClick = False
            beforeSelect = screen.subsurface(canvasRect).copy()
        beforePaste = screen.subsurface(canvasRect).copy() #we also copy canvas before we paste

    #if user is pasting 
    if pasteMove == True:
        if canvasRect.collidepoint(mx, my):
            screen.set_clip(canvasRect)
            #if cut has a subsurface, it takes precedance over copy when pasting
            if cut != None:
                screen.blit(beforePaste, (220, 80)) #blit beforePaste to prevent multiple pastes
                pasteWidth = cut.get_width()
                pasteHeight = cut.get_height()
                screen.blit(cut, (mx - (pasteWidth) / 2, my - (pasteHeight) / 2)) #display cut subsurface on cavas
            else:
                if copy != None:
                    screen.blit(beforePaste, (220, 80))
                    pasteWidth = copy.get_width()
                    pasteHeight = copy.get_height()
                    screen.blit(copy, (mx - (pasteHeight) / 2, my - (pasteHeight) / 2)) #othewise we display copied subsurface on canvas
            #pasting resolves in event loop after MOUSEBUTTONUP    
            screen.set_clip(None)


    ######################INFO BAR################################
    #we have to set infoText for the current tool, or if user is pasting or drawing polygons or writing text, or if user collides with a rect
    #to display as instructions in infoBar

    #if user is pasting or drawing polygon or writing text, we set the infoText to what they are doing (most precedence over other infoText
    #because all othe functions are locked during this time)
    if pasteMove == True or drawnPolygon == True or writeText == True:
        if pasteMove == True:
            infoText = "Click on the canvas to paste the copied or cut image. Note all other functions are locked during this time."
        elif drawnPolygon == True:
            infoText = "Click on the canvas to determine the points to draw the polygon. To finish, click first point again. Note all other functions are locked during this time."
        elif writeText == True:
            infoText = ("Type any text on your keyboard to display it on the canvas. " +
            "When you are done, click the check mark or x mark on the side to confirm or " +
            "decline the written text." + " Note all other functions are locked during this time.")
    else:
        #if user is not colliding with any other rects, we set the infoText to display info about current tool (least precedence)
        if tool == "select":
            infoText = ("Select Tool: Select any part of the canvas using a rectangle to copy or cut it.")
            
        if tool == "pencil":
            infoText = "Pencil Tool: Hold and drag anywhere on the canvas to draw a pencil line."
            
        if tool == "paint":
            infoText = ("Paint Tool: Hold and drag anywhere on the canvas to paint. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the tip.")
            if brushRect.collidepoint(mx, my):
                infoText = "Brush Tool: Paint a certain colour over the canvas."
            if highlightRect.collidepoint(mx, my):
                infoText = "Highlighter Tool: Highlight canvas with current colour and transparency."

        if tool == "eraser":
            infoText = ("Eraser Tool: Hold and drag anywhere on the canvas to erase. "
            + "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the eraser.")

        if tool == "fill":
            infoText = ("Fill Tool: Click anywhere on the canvas to fill the enclosed area of the same colour." +
            "Note it may be slow, so only click once on canvas and wait until it is finished before clicking again.")

        if tool == "eyedrop":
            infoText = ("Eyedrop Tool: Ciick anywhere on the canvas to set the current colour equal to the colour " +
            "of the pixel you selected.")

        if tool == "spray":
            infoText = ("Spray Paint Tool: Hold and drag to draw many miny dots on the screen. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the spray. "
            + "Use the up and down buttons on your keyboard to change the speed of the spray.")

        if tool == "sprinkles":
            infoText = ("Sprinkle Tool: Hold and drag to draw many miny lines on the screen. " + 
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the sprinkler. "
            + "Use the up and down buttons on your keyboard to change the thickness of the lines.")
        if tool == "line":
            infoText = ("Line Tool: Hold and drag to draw a line on screen from your starting clicked point to your " +
            "current point." + "Use the mouse scroll or the left and right buttons on your keyboard to change the thickness of the line.")
            
        if tool == "polygon":
            infoText = ("Polygon Tool: Draw any polygon on the screen by clicking points on the canvas. To finish, click"
            + " the first point again.")
            #if user is hovering over filled or unfilled rects, then we overwrite infoText to display info about those buttons
            if filledShapeRect.collidepoint(mx, my):
                infoText = "Draws a filled polygon."
            if outlineShapeRect.collidepoint(mx, my):
                infoText = "Draws an outlined polygon. Use the mouse scroll or the left and right buttons on your keyboard to change the thickness of the outline."
                
        if tool == "rect":
            infoText = "Rectangle Tool: Hold and drag to draw a rectangle on the canvas."
            if filledShapeRect.collidepoint(mx, my):
                infoText = "Draws a filled rectangle."
            if outlineShapeRect.collidepoint(mx, my):
                infoText = "Draws an outlined rectangle. Use the mouse scroll or the left and right buttons on your keyboard to change the thickness of the outline."
                
        if tool == "ellipse":
            infoText = "Ellipse Tool: Hold and drag to draw a ellipse on the canvas."
            if filledShapeRect.collidepoint(mx, my):
                infoText = "Draws a filled ellipse."
            if outlineShapeRect.collidepoint(mx, my):
                infoText = "Draws an outlined ellipse. Use the mouse scroll or the left and right buttons on your keyboard to change the thickness of the outline."
                
        if tool == "text":
            infoText = ("Text Tool: Click anywhere on the canvas and start typing to place text on your "
            + "drawing. You can change the font type on the side of the screen while you are not typing. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the font size while you are not typing.")

        if tool == "stamp":
            infoText = ("Stamps and Background Tool: Select a stamp or background from the side and click the canvas to put it on the screen. Use mouse scroll" +
            " to change size of stamp and use left or right buttons to rotate stamp.")
            #if user is hovering over stamp or background rects, then we overwrite infoText to display info about those buttons
            if stampSelectRect.collidepoint(mx, my):
                infoText = "Select a character and hold and drag on the canvas to place it on your drawing."
            if backgroundSelectRect.collidepoint(mx, my):
                infoText = "Select a background and click on the screen to set it on your drawing."
                
        if tool == "filter":
            if sepiaRect.collidepoint(mx, my):
                infoText = "Sepia Filter"
            if blackAndWhiteRect.collidepoint(mx, my):
                infoText = "Black and White Filter"

        #otherwise if the user hovers over other tools rects, then we overwrite infoText display info about those tools

        if selectRect.collidepoint(mx, my):
            infoText = ("Select Tool: Select any part of the canvas using a rectangle to copy or cut it.")
            
        if pencilRect.collidepoint(mx, my):
            infoText = "Pencil Tool: Hold and drag anywhere on the canvas to draw a pencil line."
            
        if paintRect.collidepoint(mx, my):
            infoText = ("Brush Tool: Hold and drag anywhere on the canvas to paint. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the brush.")

        if eraserRect.collidepoint(mx, my):
            infoText = ("Eraser Tool: Hold and drag anywhere on the canvas to erase. "
            + "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the eraser.")

        if fillRect.collidepoint(mx, my):
            infoText = ("Fill Tool: Click anywhere on the canvas to fill the enclosed area of the same colour." +
            "Note it may be slow, so only click once on canvas and wait until it is finished before clicking again.")

        if eyeRect.collidepoint(mx, my):
            infoText = ("Eyedrop Tool: Ciick anywhere on the canvas to set the current colour equal to the colour " +
            "of the pixel you selected.")

        if sprayRect.collidepoint(mx, my):
            infoText = ("Spray Paint Tool: Hold and drag to draw many miny dots on the screen. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the spray. "
            + "Use the up and down buttons on your keyboard to change the speed of the spray.")

        if sprinkleRect.collidepoint(mx, my):
            infoText = ("Sprinkle Tool: Hold and drag to draw many miny lines on the screen. " + 
            "Use the mouse scroll or the left and right buttons on your keyboard to change the size of the sprinkler. "
            + "Use the up and down buttons on your keyboard to change the thickness of the lines.")
        if lineRect.collidepoint(mx, my):
            infoText = ("Line Tool: Hold and drag to draw a line on screen from your starting clicked point to your " +
            "current point." + "Use the mouse scroll or the left and right buttons on your keyboard to change the thickness of the line.")
            
        if polygonRect.collidepoint(mx, my):
            infoText = ("Polygon Tool: Draw any polygon on the screen by clicking points on the canvas. To finish, click"
            + " the first point again.")
                
        if rectRect.collidepoint(mx, my):
            infoText = "Rectangle Tool: Hold and drag to draw a rectangle on the canvas."
                
        if ellipseRect.collidepoint(mx, my):
            infoText = "Ellipse Tool: Hold and drag to draw a ellipse on the canvas."
                
        if textRect.collidepoint(mx, my):
            infoText = ("Text Tool: Click anywhere on the canvas and start typing to place text on your "
            + "drawing. You can change the font type on the side of the screen while you are not typing. " +
            "Use the mouse scroll or the left and right buttons on your keyboard to change the font size while you are not typing.")

        if stampRect.collidepoint(mx, my):
            infoText = "Stamps and Background Tool: Select a stamp or background from the side and click the canvas to put it on the screen. "

        if filterRect.collidepoint(mx, my):
            infoText = "Filter Tool: Select a filter to place over your current canvas!"

        #otherwise if the user hovers over other function rects, then we overwrite infoText display info about those functions (most precedence)
        if colourWheelRect.collidepoint(mx, my):
            infoText = "Colour Slider: Select the shade of colour for the colour picker."
        if colourPicker.collidepoint(mx, my):
            infoText = "Colour Picker: Click anywhere on the gradient to select the current colour used for all the tools."

        if openRect.collidepoint(mx, my):
            infoText = "Open File: Opens an image on your hard drive and displays it on the canvas. Supported images are .png, .jpg, .jpeg, .bmp."

        if saveRect.collidepoint(mx, my):
            infoText = ("Save File: Saves the canvas to your hard drive as an image. Supported output images are .png, .jpg, .jpeg, .bmp. Default "
            + "is .png if user did not specify.")

        if undoRect.collidepoint(mx, my):
            infoText = "Undo: Click to undo the last operation you did to modify the canvas."

        if redoRect.collidepoint(mx, my):
            infoText = "Redo: Click to redo the last operation you did to modify the canvas."

        if copyRect.collidepoint(mx, my):
            infoText = "Copy: After selecting an area with the select tool, use this to copy that area for the paste tool."

        if cutRect.collidepoint(mx, my):
            infoText = "Cut: After selecting an area with the select tool, use this to cut that area for the paste tool."

        if pasteRect.collidepoint(mx, my):
            infoText = "Paste: Pastes the copied or cut image on the canvas."

        if clearRect.collidepoint(mx, my):
            infoText = "Clear: Clears the whole canvas."

        if colourRect.collidepoint(mx, my):
            infoText = "RGB of current colour is " + str(col[0]) + ", " + str(col[1]) + ", " + str(col[2])
            
        if addWindow.collidepoint(mx, my):
            infoText = "Add Window: Adds another canvas window to the screen for you to draw on."
            
        if deleteWindow.collidepoint(mx, my):
            infoText = "Delete Window: Deletes the current canvas window."

    #we only update infoBar is text is different from previous text (don't want overlap)
    if infoText != prevInfoText:
        screen.blit(infoBack, (1000, 450)) #erase infoBar
        draw.rect(infoBar, (216, 15, 15, 125), infoRect) #draw a red rect on infoBar surface with transparancy
        #sometimes word wrap gives this error, although i don't know why
        '''
        Traceback (most recent call last):
  File "F:\Paint Project\paintProject - Phillip Pham.py", line 1556, in <module>
    infoText = wrap(infoText, 45)
  File "C:\Python32\lib\textwrap.py", line 318, in wrap
    return w.wrap(text)
  File "C:\Python32\lib\textwrap.py", line 289, in wrap
    text = self._munge_whitespace(text)
  File "C:\Python32\lib\textwrap.py", line 128, in _munge_whitespace
    text = text.expandtabs()
AttributeError: 'list' object has no attribute 'expandtabs'
        '''
        prevInfoText = infoText #sets old infoText to prevInfoText
        #try and except because above error
        try:
            infoText = wrap(infoText, 45) #wraps the infoText so that only 45 characters appear on each line and saves it to infoText
        except:
            pass
        textLines = [] #list to hold each rendered lines
        for line in infoText: #for each lined returned from wrap function
            renderLine = currentInfoDisplay.render(line, True, BLACK) #render each line 
            textLines.append(renderLine) #append each line to textLines list

        textLiney = 0 #y coor for each line
        
        for eachRenderLine in textLines: #for each rendered line in textLines
            infoBar.blit(eachRenderLine, (0, textLiney)) # we blit it to the infoBar surface
            textLiney += 20 #increase the y value by 20 after each line and loop continues until each line is blitted
            
        screen.blit(infoBar, (1000, 450)) #blits infoBar surface to screen after finished
        
    ############################################################################

    ########################## CHANGING COLOUR #################################
    #checks if mouse is over colour slider
    if colourWheelRect.collidepoint(mx, my) and writeText != True and drawnPolygon != True and pasteMove == False:
        #checks if colourUp is true (mouse button released up in MOUSEBUTTONUP in event loop)
        if colourUp == True:
            #draw gradient of colour pixel mouse was released from
            #read code up before program runs to find out explanation for gradient
            wheelColGradient.fill((0, 0, 0)) 
            x = 0
            y = 0
            
            while y < 255:
                ratio = x / 255
                bright = y
                r = int((255 - bright) * (1 - ratio) + (max(wheelColPix[0] - bright, 0)) * ratio)
                g = int((255 - bright) * (1 - ratio) + (max(wheelColPix[1] - bright, 0)) * ratio)
                b = int((255 - bright) * (1 - ratio) + (max(wheelColPix[2] - bright, 0)) * ratio)
                wheelColGradient.set_at((x, y), (r, g, b))
                if x < 255:
                    x += 1
                else:
                    x = 0
                    y += 1

            gradient = wheelColGradient.subsurface((0, 0, 255, 255)).copy()
            transformedGradient = transform.scale(gradient, (200, 200))
            screen.blit(transformedGradient, (5, 550))
            draw.rect(screen, BLACK, colourPicker, 1)
            colourUp = False #resets colourUp back to false

    #checks if mouse is on colour picker gradient and if user is left clicking
    if colourPicker.collidepoint(mx, my) and mb[0] == 1 and writeText != True and drawnPolygon != True and pasteMove == False:
        prevCol = col #set old col to prevCol
        col = screen.get_at((mx, my)) #gets the colour of the current pixel
        #and sets it as current colour
        if col != prevCol:
            #if the col is different from previous colour we refresh highlighter surface
            highlightBack = Surface((800, 700)).convert()
            highlightBack.set_alpha(125)
            highlightBack.fill(col)
        draw.rect(screen, col, colourRect) #draws rect to show new current colour
        


    ############################################################################

    ########################## OPENING AND SAVING ##############################
    #saving the picture (only on canvas)
    #checks if mouse is on save rect button and if user is left clicking
    if saveRect.collidepoint(mx, my) and mb[0] == 1 and len(windows) > 0 and writeText != True and drawnPolygon != True and pasteMove == False:
        try: #tries this code
            fname = filedialog.asksaveasfilename(defaultextension = ".png")
            #asks the user to input the file name
            #default extention is PNG
            image.save(screen.subsurface(canvasRect), fname)
            #save tha canvas as an image using file name user typed in
        except:
            pass #if above doesn't work, prevents crashing

    #open the picture (load)
    #checks if mouse is on open rect button and if user is left clicking
    if openRect.collidepoint(mx, my) and mb[0] == 1 and len(windows) > 0 and writeText != True and drawnPolygon != True and pasteMove == False:
        try:
            fname = filedialog.askopenfilename(filetypes = [("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
            #allows user to pick an image on their hard drive (supported images are .png, .jpg, .jpeg, .bmp)
            pic = image.load(fname) #loads that image
            dimensions = pic.get_rect().size #gets size of that image
            #checks if that image is over the size of the canvas in width in height
            if dimensions[0] > 750 and dimensions[1] > 600:
                #if it is then, we transform image to fit canvas
                pic = transform.scale(pic, (750, 600))
            #checks if that image is over the size of the canvas in width
            elif dimensions[0] > 750:
                #if it is then, we transform image width to fit canvas
                pic = transform.scale(pic, (750, size[1]))
            #checks if that image is over the size of the canvas in height
            elif dimensions[1] > 600:
                #if it is then, we transform image height to fit canvas
                pic = transform.scale(pic, (size[0], 600))
                
            if selectClick == True and beforeSelect != None:
                 screen.blit(beforeSelect, (220, 80))
                 selectClick = False
                 beforeSelect = None
                 
            screen.blit(pic, (220, 80)) #we blit the transformed image to canvas
            undoList.append(screen.subsurface(canvasRect).copy())
            del redoList[:]
            #if tool is select, update beforeSelect
            if tool == "select":
                beforeSelect = screen.subsurface(canvasRect).copy()
        except:
            pass

    if canvasRect.collidepoint(mx, my): #if user is colliding with canvas
        omx, omy = mx, my #updates previous point with current point (used for
        #pencil, paint, and eraser tool to draw continuous line)

    display.flip() #displays all drawn stuff in this iteration to screen
            
quit() #closing the pygame window







    
