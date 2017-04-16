import os.path


class DaltonizeImage:
    def __init__(self, fileName, filePath, colorDeficit):
        self.fileName = fileName
        self.filePath = filePath
        self.colorDeficit = colorDeficit

    def execute(self):
        modified_filename = "%s-%s-%s" % ('Modified', self.colorDeficit, self.fileName)
        head, tail = os.path.split(self.filePath)
        # Save transformed image to the cache dir
        # head = head.replace('attachments', 'cache')
        modified_fpath = os.path.join(head, modified_filename)

        # Look if requested image is already available
        if os.path.isfile(modified_fpath):
            return (modified_filename, modified_fpath)

        helpers_available = True
        try:
            import numpy
            from PIL import Image
        except:
            helpers_available = False
        if not helpers_available:
            return (self.fileName, self.filePath)

        # Get image data
        im = Image.open(self.filePath)
        if im.mode in ['1', 'L']:  # Don't process black/white or grayscale images
            return (self.fileName, self.filePath)
        im = im.copy()
        im = im.convert('RGB')
        RGB = numpy.asarray(im, dtype=float)

        # Transformation matrix for Deuteranope (a form of red/green color deficit)
        lms2lmsd = numpy.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
        # Transformation matrix for Protanope (another form of red/green color deficit)
        lms2lmsp = numpy.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
        # Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
        lms2lmst = numpy.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])
        # Colorspace transformation matrices
        rgb2lms = numpy.array(
            [[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
        lms2rgb = numpy.linalg.inv(rgb2lms)
        # Daltonize image correction matrix
        # err2mod = numpy.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
        err2mod = numpy.array([[-1, 0, 0], [1, 1, 0], [1, 0, 1]])

        # Get the requested image correction
        if self.colorDeficit == 'd':
            lms2lms_deficit = lms2lmsd
        elif self.colorDeficit == 'p':
            lms2lms_deficit = lms2lmsp
        elif self.colorDeficit == 't':
            lms2lms_deficit = lms2lmst
        else:
            return (self.fileName, self.filePath)

        # Transform to LMS space
        LMS = numpy.zeros_like(RGB)
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                rgb = RGB[i, j, :3]
                LMS[i, j, :3] = numpy.dot(rgb2lms, rgb)

        # Calculate image as seen by the color blind
        _LMS = numpy.zeros_like(RGB)
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                lms = LMS[i, j, :3]
                _LMS[i, j, :3] = numpy.dot(lms2lms_deficit, lms)

        _RGB = numpy.zeros_like(RGB)
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                _lms = _LMS[i, j, :3]
                _RGB[i, j, :3] = numpy.dot(lms2rgb, _lms)

        # Calculate error between images
        error = (RGB - _RGB)
        # Daltonize
        ERR = numpy.zeros_like(RGB)
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                err = error[i, j, :3]
                ERR[i, j, :3] = numpy.dot(err2mod, err)

        dtpn = ERR + RGB
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                dtpn[i, j, 0] = max(0, dtpn[i, j, 0])
                dtpn[i, j, 0] = min(255, dtpn[i, j, 0])
                dtpn[i, j, 1] = max(0, dtpn[i, j, 1])
                dtpn[i, j, 1] = min(255, dtpn[i, j, 1])
                dtpn[i, j, 2] = max(0, dtpn[i, j, 2])
                dtpn[i, j, 2] = min(255, dtpn[i, j, 2])
        result = dtpn.astype('uint8')

        # Save daltonized image
        im_converted = Image.fromarray(result, mode='RGB')
        im_converted.save(modified_fpath)
        return (modified_filename, modified_fpath)

    def imageProcessing(self):
        import sys
        if len(sys.argv) != 2:
            modified_filename, modified_fpath = self.execute()
            return (modified_filename, modified_fpath)

        if not (os.path.isfile(sys.argv[1])):
            print "Given file does not exist"
            sys.exit(1)

        extpos = sys.argv[1].rfind(".")
        if not (extpos > 0 and sys.argv[1][extpos:].lower() in ['.gif', '.jpg', '.jpeg', '.png', '.bmp', '.ico', ]):
            print "Given file is not an image"
            sys.exit(1)
