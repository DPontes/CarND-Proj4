# Advanced Line Detection

*Author:* Diogo Pontes

*Email:* dpontes11@gmail.com

## Objective of the project

In this project, the goal is to write a software pipeline to identify the lane boundaries in a video from a front-facing camera on a car.


## The Goals/steps of this project are the following:

- Compute the camera calibration matrix and distortion coefficientes given a set of chessboard images
- Apply a distortion correction to raw images
- Use color transforms, gradients, etc., to create a thresholded binary image
- Apply a perspective transform to rectify binary image ("birdseye view").
- Detect lane pixels and fit to find lane boundary
- Determine the curvature of the lane and vehicle position with respect to center
- Warp the detected lane boundaries back onto the original image
- Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position

## Camera Calibration and distortion correction

### Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image

The code for the camera calibration is in the _calibrate.py_ file. It simply loads the images from _/camera_cal/_ directory and uses the chessboard corners to compute the camera matrix and distortion coeficients.

The result data is stored in the _wide_dist_pickle.p_ file which will be used by the rest of the scripts.

## Original Image
![Original Image](/test_images/straight_lines2.jpg)

## Calibrated / Undistorted
![Undistorted](/test_images/undistorted2.jpg)

## Pipeline (test images)

### 1. Provide an example of a distortion-corrected image

Example given previously

### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image. Provide an example of a binary image result

### 3. Describe how (and identify in your code) you performed a perspective transform and provide an example of a transformed image

At the beginning the perspective transformation was calculated manually. Afterwards a small piece of code was developed in order to generate the transformation from just one parameter that is linked to the camera focal length and information about how to compress the images so that the curves on the road are visible when warped.

It is in the _perpective_ function:

```
sh
def perpective():
```


### 4. Describe how (and identify in the code) you identified lane-line pixels and fit their positions with a polynomial

### 5. Describe how (and identify where in the code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center

### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly

## Pipeline (video)

### Provide a link to your final video output. Your pipeline should perform reasonably well on the entire project video

## Discussion

### Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?
