import pickle

# from typing import List
from warnings import warn
import numpy as np
import sys

sys.path.append("..")
import SHSlib as sh


class Processor:
    # Set
    def __init__(
        self,
        floorCap=60,
        minDist=20,
        NZernike=7,
        storeImages=False,
        NApatures=None,
        printZernikeEqasion=False,
        normZernike=True,
        scaleToUnitCircle=False,
        showWarnings=False,
    ):

        self.minDist = minDist
        self.floorCap = floorCap
        self.showWarnings = showWarnings
        if NZernike > 9:
            warn("Number of Zernike Polinomial canot be above 9, it is now set to 9.")
            self.NZernike = 9
        else:
            self.NZernike = NZernike
        self.NApertures = NApatures
        self.storeImages = storeImages
        self.Images = []
        self._refAvailable = False
        self.normZernike = normZernike
        self.Wavefront = []
        self.WavefrontComponents = []

        # saving paste mesurments
        self.pastCentroids = None
        self._dxList = []
        self._dyList = []
        self._Coefficients = []
        self.rejectedImages = []
        self.generateZernikeFunctions(printZernikeEqasion=printZernikeEqasion)
        self.scale = 1
        self.scaleToUnitCircle = scaleToUnitCircle

        self.normdx = []
        self.normdy = []

    def setRef(self, Image):
        self.refImage = Image
        self.refImageNp = self.asNumpy(Image)
        self.refImageNp = self.preprocessImage(self.refImageNp)

        # test if Number of Apatures match Number of Lables
        self.refLabels = self.getLables(self.refImageNp)
        self.refCentroids = self.getCentroids(self.refImageNp)
        # self.refCentroids = sh.analyse.getMomentum(self.refLabels,self.refImageNp)
        # self.refCentroids = (self.refCentroids[0] / self.scale, self.refCentroids[1] / self.scale)
        # self.refCentroids[1] = self.refCentroids[1] / self.scale

        if self.NApertures and not self.testValidRef():
            warn("NApature dose not match Number of Lables")
        else:
            self._refAvailable = True

        self.generateModeBaseMatrix()

    def testValidRef(self):
        if not self.NApertures:
            warn("can't be performed, because no NApature was providet")
            return False

        if self.NApertures and self.NApertures != self.refLabels.max():
            return False

        return True

    def setNextSample(self, Image):
        if not self._refAvailable:
            warn("no ref is set yet")
        Image = self.preprocessImage(Image)
        # TODO convert to NP if not
        try:

            Centroids = self.getCentroids(Image)
            PartnerCentroidShift = self.getPartner(Centroids, self.refCentroids)

            dx = PartnerCentroidShift[0]
            dy = PartnerCentroidShift[1]

            Coefficients = self.getZernikeCoefficient(dx, dy)
            self._Coefficients += [Coefficients]

            self._dxList += [dx]
            self._dyList += [dy]

            if self.storeImages:
                self.Images += [Image]
        except ZeroDivisionError:
            if self.showWarnings:
                print(f"error with at index :{len(self.rejectedImages)}")
            self.rejectedImages += [Image]
            return
        except Exception as e:
            raise e

        Wavefront, WavefrontComponents = self.getWavefront(Coefficients[0])
        self.Wavefront += [Wavefront]
        self.WavefrontComponents += [WavefrontComponents]

        return None

    # Convert List of dx/dy to Numpy
    @property
    def dx(self):
        dx = self.ListToNumpy(self._dxList)
        return dx

    @property
    def dy(self):
        dy = self.ListToNumpy(self._dyList)
        return dy

    @property
    def Coefficients(self):

        Coefficients = [sub[0] for sub in self._Coefficients]
        Coefficients = self.ListToNumpy(Coefficients)
        return Coefficients

    def ListToNumpy(self, ListToNumpy):

        if len(ListToNumpy[1].shape) > 1:
            ListToNumpy = [np.squeeze(a) for a in ListToNumpy]
        NumpyArray = np.ones((len(ListToNumpy), len(ListToNumpy[1])))

        for i in range(len(ListToNumpy)):

            NumpyArray[i, :] = ListToNumpy[i]
        return NumpyArray

    def readPickel(self, filePfad):
        with open(filePfad, "rb") as f:
            pikleLoad = pickle.load(f)
            # test if consecutive Elements have eqal length
            # beause some dataset have more than the images an need to be treatet diferently
            for a1, a2 in zip(pikleLoad, pikleLoad[2:]):
                if len(a1) != len(a2):
                    out = pikleLoad[0]
                    break
            else:
                out = pikleLoad
            return out

    def readHdf5(self, filePath):
        import h5py

        with h5py.File(filePath, "r") as f:
            out = f["data"][()]
        return out

    def loadFile(self, filePfad, refIndex=0):
        # load file into python worksapce
        from pathlib import Path

        fileExtension = Path(filePfad).suffixes[0]

        if fileExtension == ".picke":
            self.loadedImages = self.readPickel(filePfad)
        elif fileExtension == ".hdf5":
            self.loadedImages = self.readHdf5(filePfad)
        else:
            raise Exception("File extension has to be .pickle or .hdf5")

        self.setRef(self.loadedImages[refIndex])
        self.restImgs = self.loadedImages[refIndex + 1 :]
        #        if self.storeImages:
        #            self.savedImages = [self.asNumpy(imgs) for imgs in self.loadedImages[1:]]

        for i, img in enumerate(self.restImgs):
            self.setNextSample(self.asNumpy(img))

        return None

    def preprocessImage(self, Image):
        Image[Image < self.floorCap] = 0

        return Image

    def getLables(self, img):
        return sh.analyse.getSeperation(img, min_distance=self.minDist)

    def getCentroids(self, img):
        Centroid = sh.analyse.getMomentum(self.refLabels, img)
        if self.scaleToUnitCircle:
            scaling = max(np.shape(img))
            Centroid = (
                Centroid[0] / (scaling / 2) - 1,
                Centroid[1] / (scaling / 2) - 1,
            )
        return Centroid

    def getPartner(self, CurrentCentoids, refCentroids):
        return sh.analyse.getPartner(CurrentCentoids, refCentroids)

    def saveAsPickel(self, fileName):
        # TODO
        return None

    def asNumpy(self, img):
        img = np.int16(img)
        img = np.uint8((img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) / 3)
        return img

    def getWavefront(self, Coefficients):

        Wavefront = np.zeros_like(self.refLabels, dtype=np.double())
        WavefrontComponents = []

        # loop over Number of Zernike Polynom
        for modelIndx in range(self.NZernike):
            ModeValues = Coefficients[modelIndx] * self.ZernikeFunctions[modelIndx](
                self.refCentroids[0], self.refCentroids[1]
            )
            singeWavefrontComponent = np.zeros_like(self.refLabels, dtype=np.double())

            for CentroidIndex in range(len(self.refCentroids[1])):
                singeWavefrontComponent[
                    self.refLabels == CentroidIndex + 1
                ] = ModeValues[CentroidIndex]

            WavefrontComponents += [singeWavefrontComponent]
            Wavefront += singeWavefrontComponent

        return Wavefront, WavefrontComponents

    # WavefrontReconstruction
    def generateModeBaseMatrix(self):

        XPos = self.refCentroids[0].T
        YPos = self.refCentroids[1].T
        ModelZdx = self.ZernikeFunctionsDx
        ModelZdy = self.ZernikeFunctionsDy

        # Reconstruction Matrix
        Xi = np.zeros((self.NZernike, 2 * len(XPos)))

        # Populate Xi Matrix with Model Values
        for i in range(self.NZernike):
            # Map first half of vector to dx
            ValuesZdx = ModelZdx[i](XPos, YPos)
            # and second to dy
            ValuesZdy = ModelZdy[i](XPos, YPos)

            # normilize Model Valuse to have ceficcians compearable size
            if self.normZernike and np.max(ValuesZdx) != 0:
                self.normdx += [np.max(np.abs(ValuesZdx))]
                ValuesZdx = ValuesZdx / self.normdx[i]

            elif self.normZernike and np.max(ValuesZdx) == 0:
                self.normdx += [1]

            if self.normZernike and np.max(ValuesZdy) != 0:
                self.normdy += [np.max(np.abs(ValuesZdy))]
                ValuesZdy = ValuesZdy / self.normdy[i]

            elif self.normZernike and np.max(ValuesZdy) == 0:
                self.normdy += [1]

            Xi[i, 0 : len(XPos)] = ValuesZdx
            Xi[i, len(XPos) :] = ValuesZdy
        self.BaseMatrix = Xi.T
        return self.BaseMatrix

    def squeezeTo(self, mat, minVal, maxVal):
        pass

    def getZernikeCoefficient(self, dX, dY):
        Z = self.ZernikeFunctions

        MeasurementVector = np.hstack((dX.T, dY.T))[
            np.newaxis
        ].T  # newaxis makes it operationally with Matrixes
        Coefficient = np.linalg.lstsq(self.BaseMatrix, MeasurementVector, rcond=None)
        return Coefficient

    def generateZernikeFunctions(self, printZernikeEqasion=False):
        z2 = "x"
        z3 = "y"
        z4 = "x**2 - y**2"
        z5 = "-1 + 2*x**2 + 2*y**2"
        z6 = "2*x*y"
        z7 = "x**3 - 3*x*y**2"
        z8 = "3*x**3 + 3*x*y**2 + 2*x"
        z9 = "3*y**3 + 3*x**2 *y - 2*y"
        z10 = "-y**3 + 3*x**2*y"

        NZBaseStr = [z2, z3, z4, z5, z6, z7, z8, z9, z10]
        NZBaseStr = NZBaseStr[: self.NZernike]

        self.ZernikeFunctions = []
        self.ZernikeFunctionsDx = []
        self.ZernikeFunctionsDy = []

        for ZBaseStr in NZBaseStr:
            (ZBase, Zdx, Zdy) = self.str2Equation(
                ZBaseStr, printZernikeEqasion=printZernikeEqasion
            )
            self.ZernikeFunctions += [ZBase]
            self.ZernikeFunctionsDx += [Zdx]
            self.ZernikeFunctionsDy += [Zdy]

    def str2Equation(self, strFunction, printZernikeEqasion=False):
        import sympy as sy
        from sympy.parsing.sympy_parser import parse_expr
        from sympy.utilities.lambdify import lambdify
        from sympy.abc import x, y

        symFun = parse_expr(strFunction)
        dx = sy.diff(symFun, "x")
        dy = sy.diff(symFun, "y")
        if printZernikeEqasion:
            print(f"base: {symFun}")
            print(f"dx: {dx}")
            print(f"dy: {dy}")

        # np.vectorize mittigates sceneario where output is just 0 and an input array
        # will becom jut a outbut scaler, breaking potentialy breaking stuff
        BaseFunktion = np.vectorize(lambdify([x, y], strFunction))
        dx = np.vectorize(lambdify([x, y], dx))
        dy = np.vectorize(lambdify([x, y], dy))

        return BaseFunktion, dx, dy
