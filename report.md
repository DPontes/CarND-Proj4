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

All image processing is in the _process_image_ function. It receives an image and returns an array of warped, filtered images.

The process is:

- Undistort the image
- Convert to __HSV__ and separate the channels
- Apply __EqualizeHist__ to value and saturation channels
- Apply a __GaussianBlur__ with a 7x7 kernel to value and saturation channels
- Call a special __remove_dark__ function (later explained)
- Apply a set of filters and warp the resulting images

The __remove_dark__ function was originally used to remove dark lines and soft some edges. Finally it became a more generalized light equalization. It's process is:

- Divide the lower half of the image (with the exception of the bottom 20 pixels) in __n__ horizontal slides
- For each slide compute the average __V__ value in the center of the image (between 20% and 80% of the width)
- Select all points below this average value and apply to them a BoxFilter with 50x50 pixels in __S__ and __V__ channels
- Just for the __V__ channel move all below average intensities between 0 and 50 and expand the ones over the average to 50-255

The idea is that low intensity features are blurred and will generate less gradients as high intensities have a greater range.

Here is an example of the value channel, first the original image:

![Original Image](/test_images/filter1.png)

Then this one is just after the equalization and __GaussianBlur__:

![Filter2 Image](/test_images/filter2.png)

And this one is the same as the previous one but after __remove_dark__ with 3 slides:

![Filter3 Image](/test_images/filter3.png)

To get the bitmap images I have used 2 filters and an additional color filter.

First one is the one talked in the course, just selecting pixels with gradient in x and y direction and those special values and saturations. It is in the __gradient_filter__ function that uses the __color_threshold__ and the __abs_sobel_thresh__. Here is an example of the same image with said filters:

![Filter4 Image](/test_images/filter4.png)

The other algorithm uses similar sobel computations linked with values in gradient x and saturation but "or's" them together so usually is messier. It is implemented in the __complex_sobel__ function.

![Filter5 Image](/test_images/filter5.png)

Selecting hue is difficult but a way to do it is select just the road, expand its borders and intersect with the results of the other algorithm so we have a mask that may be intersected with the other results, giving:

![Filter6 Image](/test_images/filter6.png)
![Filter7 Image](/test_images/filter7.png)

which is a lot better.

So we have 4 different possibilities in total. Depending on the situation we may like to use one or another result so that the main filtering function, __super_filter__ may return an array of all identified as "gr", "so", "grt" and "sot" corresponding to the images presented.

### 3. Describe how (and identify in your code) you performed a perspective transform and provide an example of a transformed image

At the beginning the perspective transformation was calculated manually. Afterwards a small piece of code was developed in order to generate the transformation from just one parameter that is linked to the camera focal length and information about how to compress the images so that the curves on the road are visible when warped.

It is in the _perspective_ function:

```
def perspective(focal=1.3245, maxHeight=460, size=(1280,720), shrink=0.0, xmpp=0.004):
```

The conversion in the X axis from pixels to meters is modified accordingly and returned

## Original Image
![Original Image](/test_images/straight_lines2.jpg)

## Warped Image
![Warped](/test_images/warped.jpg)

As seen in the warped image, lane lines are parallel to each other.

For the previous filtered images we get:

![FilterCurve1 Image](/test_images/filterCurve1.png)
![FilterCurve2 Image](/test_images/filterCurve2.png)

which are similar and quite parallel at the bottom but not so clear at the top.

### 4. Describe how (and identify in the code) you identified lane-line pixels and fit their positions with a polynomial

### 5. Describe how (and identify where in the code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center

### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly

## Pipeline (video)

### Provide a link to your final video output. Your pipeline should perform reasonably well on the entire project video

## Discussion

### Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?
