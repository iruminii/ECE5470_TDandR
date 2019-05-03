# ECE5470_TDandR
Very very simple text detection and recognition 

April 19, 2019

Use detect light text for testing

it works for light and dark, may need mods for dark tho

other buttons are irrelevant atm

May 2, 2019

we'll figure it out tomorrow/this weekend

model.h5 is on gdrive bc its too big btw

predict.py needs keras so download that too 

### Todo:
- ~~Improve text segmentation~~
- Improve ROI detection/decision
- ~~Add trained model and prediction file~~
- ~~Add translator API~~
- Finish up the GUI once everythings working
- '!' predicts as 'q' with 89.733 confidence, needs fixing
- Use images with:
  - symbols in text? (emnist is only letters + numbers)
  - capitalize entire string? (recognition for upper/lowercase kinda bad)
  - simple/clean backgrounds?
  - only light characters on dark backgrounds?
  - if simplifying to ^, make a canvas that allows user to draw words and detect that?
  - if not, fill in gradient for character recognition

##### Thicken letters, don't detect non-alphanumeric characters

![dark foreground](https://github.com/iruminii/ECE5470_TDandR/blob/master/images/lightbg_darkfg.PNG)


##### Fix noise around letters from processing outline

![light foreground](https://github.com/iruminii/ECE5470_TDandR/blob/master/images/darkbg_lightfg.PNG)
