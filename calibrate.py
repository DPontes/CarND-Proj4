import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import cv2
import pickle

## Generates calibration values and perspective matrix
## Stores the data created in wide_dist_pickle.p

calibration_imge_dir = './camera_cal'
load_calib = False #If True, doesn't recalibrate camera

if load_calib == False:
    # prepare object points
    n_Xaxis = 9
    n_Yaxis = 6

    objp = np.zeros((n_Xaxis * n_Yaxis, 3), np.float32)
    objp[:, :2] = np.mgrid[0:n_Xaxis, 0:n_Yaxis].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images
    objpoints = [] # 3D points in the real world space
    imgpoints = [] # 2D points in the image space

    # Make a list of the chessboard calibration images
    images = glob.glob('./camera_cal/calibration*.jpg')

    # Loop through the list and find the chessboard corners
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (n_Xaxis,n_Yaxis), None)

        # If found, add objects and image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

    # Do camera calibration given object and image points
    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,imgpoints,img_size,None,None)

else:
    cal_data = pickle.load(open('./wide_dist_pickle.p', 'rb'))
    mtx = cal_data['mtx']
    dist = cal_data['dist']

# Test undistortion on an image
img = plt.imread('./test_images/straight_lines2.jpg')
img_size = (img.shape[1],img.shape[0])

undist = cv2.undistort(img, mtx, dist, None, mtx)

plt.imsave('./test_images/Undistorted.jpg', undist)

# image1 correction
src = np.float32([[202., 720.], [582., 460.], [700., 460.], [1110., 720.]])
dst = np.float32([[202., 720.], [202., 100.], [1110., 100.], [1110., 720.]])

#image 2 correction
src = np.float32([[250., 700.], [598., 448.], [685., 448.], [1068., 700.]])
dst = np.float32([[250., 700.], [250., 00.], [1068., 00.], [1068., 700.]])

#image 2 correction bis
src = np.float32([[220., 720.], [580., 460.], [702., 460.], [1090., 720.]])
dst = np.float32([[220., 720.], [210., 130.], [1000., 130.], [1000., 720.]])

M = cv2.getPerspectiveTransform(src, dst)

# Save the camera calibration result for later
dist_pickle = {}
dist_pickle['mtx'] = mtx
dist_pickle['dist'] = dist
dist_pickle['warp'] = M

pickle.dump(dist_pickle, open('wide_dist_pickle.p', 'wb'))

warped = cv2.warpPerspective(undist, M, img_size, flags=cv2.INTER_LINEAR)

plt.imsave('./test_images/warped.jpg', warped)

# Visualize undistortion
f, axes = plt.subplots(2, 2, figsize=(20,10))
axes[0, 0].imshow(img)
axes[0, 0].set_title('Original Image', fontsize=30)
axes[0, 1].imshow(undist)
axes[0, 1].set_title('Undistorted Image', fontsize=30)
axes[1, 0].imshow(warped)
axes[1, 0].set_title('Warped Image', fontsize=30)
plt.show()
