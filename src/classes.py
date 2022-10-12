# PYQT Trial 
# BUILDING A SCREEN
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2 as cv

# create class for photo viewing screen
class imageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image) :
        super().setPixmap(image)

# provides the basic application constructor
class crtnfyApp(QWidget) :
    def __init__(self) :
        super().__init__()
        self.resize(500,550)
        self.setWindowTitle('Cartoonify')
        self.setAcceptDrops(True)
        self.setUp()

    def setUp(self):    

        # make buttons (set with self to access wherever in class )
        self.crtnfy_btn = QPushButton('Cartoonify')
        self.dwnld_btn = QPushButton('Download')        
        # make drop screen widget
        self.photoViewer = imageLabel()
        # create invisible label to save file_path 
        self.invisible_path = ''
        
        # create layout
        layout = QHBoxLayout() 
        # add buttons and photoviewer to layout
        layout.addWidget(self.crtnfy_btn, 1) # second argument indicates proportion 
        layout.addWidget(self.dwnld_btn, 1)
        layout.addWidget(self.photoViewer, 8)

        # add layout to class
        self.setLayout(layout)

        # listen to buttons (¿what happens if they are pressed?)
        self.dwnld_btn.clicked.connect(self.dwnldImage)
        self.crtnfy_btn.clicked.connect(self.crtnfyImage)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
        
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            self.invisible_path = file_path
            event.accept()
        else:
            event.ignore()
    
    def set_image(self, file_path):
        # QPixmap used to load image
        self.photoViewer.setPixmap(QPixmap(file_path))
        self.path = file_path

    def dwnldImage(self):
        image = ImageQt.fromqpixmap(self.photoViewer.pixmap())
        name = input()
        image.save('./images/'+ name +'.png')

    def crtnfyImage(self):

        # read image and correct color
        originalPic = cv.imread(str( self.invisible_path))
        originalPic = cv.cvtColor(originalPic, cv.COLOR_BGR2RGB)

        # create greyscale image, smoothen and retrieve edges with thresholding technique
        grayScaleImage = cv.cvtColor(originalPic, cv.COLOR_BGR2GRAY)
        smoothGrayScale = cv.medianBlur(grayScaleImage, 5)
        getEdge = cv.adaptiveThreshold(smoothGrayScale, 255, 
        cv.ADAPTIVE_THRESH_MEAN_C, 
        cv.THRESH_BINARY, 9, 9)

        # applying bilateral filter to remove noise, keep sharp edge
        colorImage = cv.bilateralFilter(originalPic, 9, 300, 300)

        #masking edged image with our "BEAUTIFY" image
        cartoonImage = cv.bitwise_and(colorImage, colorImage, mask=getEdge)
        # ReSized6 = cv.resize(cartoonImage, (960, 540))

        # turn into compatible qpixmap
        height, width, channel = cartoonImage.shape
        bytesPerLine = 3 * width
        convertedImage= QImage(cartoonImage.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
   
        self.photoViewer.setPixmap(QPixmap(convertedImage))   


