import Tkinter as tk
import imghdr
from tkFileDialog import *
import cv2
import os
import Daltonize_Image
from PIL import Image, ImageTk


class ColorAdjustment:
    def __init__(self, top):
        # crete top window instance
        self.top = top
        # create frame for title
        frameTitle = tk.Frame(top, height=40, width=1055)
        frameTitle.pack_propagate(0)
        frameTitle.pack(side=tk.TOP)
        # create label for title
        lblTitle = tk.Label(frameTitle, text="Color Adjustment on Digital Image for Red-Green Impairement")
        lblTitle.pack(side=tk.TOP)
        lblTitle.config(font=("Courier", 20))
        # create frame for upload image button
        self.frameTop = tk.Frame(top, height=400, width=500, bg="#9ca1a3")
        self.frameTop.pack_propagate(0)
        self.frameTop.pack(side=tk.TOP)
        # create upload image button
        btnImportImg = tk.Button(self.frameTop, command=self.displayImage, text="UPLOAD IMAGE")
        btnImportImg.config(borderwidth=20, cursor="plus")
        btnImportImg.pack(side=tk.LEFT)
        # uploadicon=ImageTk.PhotoImage(file="P:\Python\Images\Upload-Folder-icon.png")
        # btnImportImg.config(image=uploadicon)
        # btnImportImg.image=uploadicon
        # create clear image button
        btnClearImg = tk.Button(self.frameTop, command=self.clearImage, text="CLEAR IMAGE")
        btnClearImg.config(borderwidth=20, cursor="dotbox")
        btnClearImg.pack(side=tk.LEFT)
        # create frame for progressbar
        self.frameProgressBar = tk.Frame(self.frameTop, height=100, width=100, bg="#9ca1a3")
        self.frameProgressBar.pack_propagate(0)
        self.frameProgressBar.pack(side=tk.BOTTOM)
        # create label for progress bar
        self.lblProgressBar = tk.Label(self.frameProgressBar, bg="#9ca1a3")
        self.lblProgressBar.pack(side=tk.BOTTOM)
        # create image frames
        progressBarImagefile = os.path.join(os.path.dirname(__file__), 'Images/loading.gif')
        self.frames = [ImageTk.tkinter.PhotoImage(file=progressBarImagefile, format='gif -index %i' % (i)) for
                       i in range(12)]
        # create frame for empty space on left
        frameLeft = tk.Frame(top, height=200, width=125, bg="#9ca1a3")
        frameLeft.pack_propagate(0)
        frameLeft.pack(side=tk.LEFT)
        # create frame to display original uploaded image
        self.frameOriginalImage = tk.Frame(top, width=300, height=300, background="white")
        self.frameOriginalImage.pack_propagate(0)
        self.frameOriginalImage.pack(side=tk.LEFT)
        self.frameOriginalImage.config(borderwidth=40, bg="white")
        # create frame for buttons to convert image
        frameConvertBtn = tk.Frame(top, width=100, height=90, background="#9ca1a3")
        frameConvertBtn.pack_propagate(0)
        frameConvertBtn.pack(side=tk.LEFT)
        lblConvertSignal = tk.Label(frameConvertBtn, text=">>>", bg="#9ca1a3")
        lblConvertSignal.config(font=("Courier", 40))
        lblConvertSignal.pack()
        # create parent frame to converted image frames
        self.frameParentConvertedImage = tk.Frame(top, width=1000, height=500, bg="#9ca1a3")
        self.frameParentConvertedImage.pack_propagate(0)
        self.frameParentConvertedImage.pack()
        self.frameParentLbl = tk.Frame(self.frameParentConvertedImage, width=1050, height=2, bg="#9ca1a3")
        self.frameParentLbl.pack(side=tk.TOP)
        self.lblRedTitle = tk.Label(self.frameParentLbl, text="Red Adjustment", bg="#9ca1a3")
        self.lblRedTitle.config(height=2, width=35)
        self.lblRedTitle.pack(side=tk.LEFT)
        self.btnSaveRed = tk.Button(self.frameParentLbl, state="disabled", text="save", bg="#9ca1a3",
                                    command=lambda: self.OnButtonClick(1))
        self.btnSaveRed.pack(side=tk.LEFT)
        self.lblGreenTitle = tk.Label(self.frameParentLbl, text="Green Adjustment", bg="#9ca1a3")
        self.lblGreenTitle.config(height=2, width=35)
        self.lblGreenTitle.pack(side=tk.LEFT)
        self.btnSaveGreen = tk.Button(self.frameParentLbl, state="disabled", text="save", bg="#9ca1a3",
                                      command=lambda: self.OnButtonClick(2))
        self.btnSaveGreen.pack(side=tk.LEFT)
        self.lblBlueTitle = tk.Label(self.frameParentLbl, text="Blue Adjustment", bg="#9ca1a3")
        self.lblBlueTitle.config(height=2, width=35)
        self.lblBlueTitle.pack(side=tk.LEFT)
        self.btnSaveBlue = tk.Button(self.frameParentLbl, state="disabled", text="save", bg="#9ca1a3",
                                     command=lambda: self.OnButtonClick(3))
        self.btnSaveBlue.pack(side=tk.LEFT)
        # create frame for converted image for red
        self.frameConvertedImageRed = tk.Frame(self.frameParentConvertedImage, width=330, height=300,
                                               background="#f2cbcb")
        self.frameConvertedImageRed.pack_propagate(0)
        self.frameConvertedImageRed.pack(side=tk.LEFT)
        self.frameConvertedImageRed.config(borderwidth=10)
        # create frame for converted image for green
        self.frameConvertedImageGreen = tk.Frame(self.frameParentConvertedImage, width=330, height=300,
                                                 background="#c7efbf")
        self.frameConvertedImageGreen.pack_propagate(0)
        self.frameConvertedImageGreen.pack(side=tk.LEFT)
        self.frameConvertedImageGreen.config(borderwidth=10)
        # create frame for converted image for blue
        self.frameConvertedImageBlue = tk.Frame(self.frameParentConvertedImage, width=330, height=300,
                                                background="#8e91f2")
        self.frameConvertedImageBlue.pack_propagate(0)
        self.frameConvertedImageBlue.pack(side=tk.LEFT)
        self.frameConvertedImageBlue.config(borderwidth=10)
        # create label for original image
        self.lblOriginalTitle = tk.Label(self.frameOriginalImage, text="Uploaded Image for Color Adjustment",
                                         bg="white")
        self.lblOriginalTitle.pack(side=tk.TOP)

    def update(self, ind):
        if ind > 11:
            ind = 0
        frame = self.frames[ind]
        ind += 1
        self.lblProgressBar.configure(image=frame)
        self.top.after(100, self.update, ind)

    def displayImage(self):
        try:
            self.load_progressbar()
        except:
            print "Error: unable to start thread"
        # clear the frame
        for widget in self.frameOriginalImage.winfo_children():
            widget.destroy()
        # ask user to upload an image
        try:
            self.filePath = askopenfilename()
        except IOError:
            # remove progress bar
            self.lblProgressBar.grid_remove()
            # return `None` if dialog closed with "cancel".
            return
        if self.filePath is '':
            # remove progress bar
            self.lblProgressBar.grid_remove()
            # return `None` if dialog closed with "cancel".
            return
        # find out the extension of uploaded image file
        extension = imghdr.what(self.filePath)
        # check if the uploaded file is not an image
        if not (extension in ['gif', 'jpg', 'jpeg', 'png', 'bmp', 'ico', ]):
            # error message
            self.errMsg = "Only ('jpg', 'jpeg', 'png', 'bmp', 'ico')"
            # display error message in destination frame
            self.displayErrorMsg()
            # remove progress bar
            self.lblProgressBar.grid_remove()
        else:
            # change the format into 'pgm' if it is other than 'gif' and save in local directory called 'Images'
            if extension != "gif":
                img = cv2.imread(self.filePath, 1)
                filenameWithExtension = os.path.basename(self.filePath)
                self.actualFile = os.path.splitext(filenameWithExtension)[0]
                fn = os.path.join(os.path.dirname(__file__), 'Images/' + self.actualFile + ".pgm")
                # savedFile = "P:\Python\Images\\" + self.actualFile + ".pgm"
                savedFile = fn
                cv2.imwrite(savedFile, img)
                self.filePath = savedFile
            # resize the uploaded image
            self._toBeResized = self.filePath
            resizeimage = self.resizeImage()
            # display the resize image in the frame through the widget 'label'
            panel = tk.Label(self.frameOriginalImage, image=resizeimage)
            # store the image reference in local variable so the image does not disappear
            panel.image = resizeimage
            panel.pack(side="top", fill="both", expand='yes')
            self.convertImageRed()
            self.convertImageGreen()
            self.convertImageBlue()
            # remove progress bar
            self.lblProgressBar.grid_remove()
            self.btnSaveRed.configure(state="active")
            self.btnSaveGreen.configure(state="active")
            self.btnSaveBlue.configure(state="active")

    def convertImageRed(self):
        # specify type of impairement & destination frame to display adjusted image
        self.impairement = "p"
        self.frameDestination = self.frameConvertedImageRed
        # call function to adjust the image
        self.adjustColor()

    def convertImageGreen(self):
        # specify type of impairement & destination frame to display adjusted image
        self.impairement = "d"
        self.frameDestination = self.frameConvertedImageGreen
        # call function to adjust the image
        self.adjustColor()

    def convertImageBlue(self):
        # specify type of impairement & destination frame to display adjusted image
        self.impairement = "t"
        self.frameDestination = self.frameConvertedImageBlue
        # call function to adjust the image
        self.adjustColor()

    def resizeImage(self):
        original = Image.open(self._toBeResized)
        resized = original.resize((250, 250), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        return image

    def adjustColor(self):
        # clear the destination frame
        for widget in self.frameDestination.winfo_children():
            widget.destroy()
        # daltonize image to adjust color
        img = Daltonize_Image.DaltonizeImage("UpdatedImage" + self.actualFile + ".pgm", self.filePath, self.impairement)
        modifiedFileName, modifiedPathName = img.imageProcessing()
        self._toBeResized = modifiedPathName
        # create list of corrected images for saving propose
        if self.impairement is "p":
            self.redImg = modifiedFileName
        elif self.impairement is "d":
            self.greenImg = modifiedFileName
        else:
            self.blueImg = modifiedFileName
        # resize daltonized image
        resizeimage = self.resizeImage()
        # put resized image into the widget 'Label' included in destination frame
        panel = tk.Label(self.frameDestination, image=resizeimage)
        # save resized image reference into the local variable & attach panel to the destination frame
        panel.image = resizeimage
        panel.pack(side="top", fill="both", expand='yes')

    def displayErrorMsg(self):
        lblError = tk.Label(self.frameOriginalImage, text=self.errMsg, fg="red", font=("Helvetica", 10))
        lblError.pack()

    def clearImage(self):
        # create frame array
        frames = [self.frameConvertedImageRed, self.frameConvertedImageGreen, self.frameConvertedImageBlue,
                  self.frameOriginalImage]
        # clear the destination frame
        for widget in frames:
            for child in widget.winfo_children():
                child.destroy()
        # disable save buttons
        self.btnSaveRed.configure(state="disabled")
        self.btnSaveGreen.configure(state="disabled")
        self.btnSaveBlue.configure(state="disabled")

    def load_progressbar(self):
        # load progressbar
        self.lblProgressBar.grid()
        self.update(0)

    def OnButtonClick(self, button_id):
        f = asksaveasfilename(initialdir="/", title="Select file",
                              filetypes=(("png files", "*.png"), ("all files", "*.*")))
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        if button_id is 1:
            sImg = os.path.join(os.path.dirname(__file__), 'Images/' + self.redImg)
        elif button_id is 2:
            sImg = os.path.join(os.path.dirname(__file__), 'Images/' + self.greenImg)
        else:
            sImg = os.path.join(os.path.dirname(__file__), 'Images/' + self.blueImg)
        img = cv2.imread(sImg, 1)  # starts from `1.0`, not `0.0`
        cv2.imwrite(f + ".png", img)


topWindow = tk.Tk()
w, h = topWindow.winfo_screenwidth(), topWindow.winfo_screenheight()
topWindow.geometry("%dx%d+0+0" % (w, h))
topWindow.config(bg="#9ca1a3")
classObject = ColorAdjustment(topWindow)
topWindow.mainloop()
