import pickle
import cv2
import numpy as np

class Calibration:

    def __init__(self, mtx, dist, M, Minv, xm, ym):
    # Has some calibration data
    # mtx  - Camera Matrix
    # dist - Distortion correction coeficients
    # M    - Perspective Matrix
    # Minv - Inverse Perspective Matrix
    # xm   - X meters per pixel
    # ym   - Y meters per pixel

        self.mtx = mtx
        self.dist = dist
        self.M = M
        self.Minv = Minv
        self.xm = xm
        self.ym = ym

class Drive:

    def __init__(self, calibration, laneWidths=(3.0, 4.5), minLaneCurv=200, maxBaseJump=20, speed=24, speedSigma2=14):
    # laneWidth   - Minimum Lane width
    # minLaneCurv - Minumum Lane Curvature
    # maxBaseJump - Maximum jump from one measurement to the next
    # speed       - Perceived speed
    # speedSigma2 - Error generated when speed is applied

        self.calibration = calibration
        self.laneWidths  = laneWidths
        self.minLaneCurv = minLaneCurv
        self.maxBaseJump = maxBaseJump
        self.speed       = speed
        self.speedSigma2 = speedSigma2

def perspective(focal=1.3245, maxHeight=460, size=(1280,720), shrink=0.0, xmpp=0.004):

    # Generates a perpective transformation given the variable focal
    # focal     - tries to get the focal on the camera
    # maxHeight - it is the highest pixel to be considered for fitting.
    #             Mapped to y = 0.0
    # shrink    - proportion of the image width to be used to reduce
    #             width between lanes in pixels so curves fit in the window
    #             If shrink!=0 then the meters for X pixels should be
    #             modified accordingly

    left  = size[0]*0.2
    right = size[0]*0.8
    newLeft = left + size[0] * shrink
    newRight = right - size[0] * shrink
    frameHeight = size[1]

    src = np.float32([
                     [left, frameHeight],
                     [left + (frameHeight - maxHeight) * focal, maxHeight],
                     [right - (frameHeight - maxHeight) * focal, maxHeight],
                     [right, frameHeight]
                     ])

    dst = np.float32([
                     [newLeft, frameHeight],
                     [newLeft, 0.],
                     [newRight, 0.],
                     [newRight, frameHeight]
                     ])

    # Compute new xm_per_pix
    newXmpp = xmpp / (newRight - newLeft) * (right - left)
    print(focal)
    print(src)
    print(dst)
    M = cv2.getPerspectiveTransform(src, dst)
    ret, Minv = cv2.invert(M)

    return M, Minv, newXmpp

def main():

    # Define conversions in x and y from pixels space to meters
    # ym_per_pix - Meters per pixel in Y axis
    # xm_per_pix - Meters per pixel in X axis

    ym_per_pix = 30.0 / 720
    xm_per_pix = 3.7 / 900

    # Load calibration data from wide_dist_pickle.p
    # mtx  - camera Matrix
    # dist - Distortion correction coeficients

    calibration_data = pickle.load(open('./wide_dist_pickle.p', 'rb'))
    mtx  = calibration_data['mtx']
    dist = calibration_data['dist']

    # Calculate M, Minv, xm_per_pix
    # M - Perspective Matrix
    # M - Inverse of M

    M, Minv, xm_per_pix = perspective(focal=1.280, maxHeight=455, shrink=0.15, xmpp = xm_per_pix)
    margin = 80

    # Calibrate Drive
    calibration = Calibration(mtx, dist, M, Minv, xm_per_pix, ym_per_pix)
    drive = Drive(calibration)
    # drive.margin = margin
    # drive.max_skipped = 20
    # drive.num_windows = 5
    # drive.speed = 24
    # drive.speed_sigma2 = 10
    #
    # # Let's try to process one image
    # process_an_image(drive, "./test_images/", "test2.jpg")

if __name__ == "__main__": main()
