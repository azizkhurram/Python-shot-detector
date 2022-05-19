# Importing necessary Libraries
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import mediapipe as mp
import math
import numpy as np
import threading

# Configuring the very First appearing Window
win = Tk()
win.geometry("1350x740")
win.configure(background="dark violet")
win.title("Cricket Shot Analysis")

mp_pose = mp.solutions.pose

def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks need to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''
    
    # Create a copy of the input image.
    # output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape

    # Check if any landmarks are detected.
    if results.pose_landmarks:

        landmarks = [(int(landmark.x * width), int(landmark.y * height), (landmark.z * width)) 
                    for landmark in results.pose_landmarks.landmark]
    
        # Return the output image and the found landmarks.
        return image, landmarks

def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle

Shots = 0
flag_1 = 0
flag_2 = 0
flag_4 = 0
flag_5 = 0
bar_1 = 0
bar_2 = 0
right_shoulder_per_1 = 0
right_shoulder_per_2 = 0

def classifyPose(landmarks, output_image, display=False):
    '''
    This function classifies yoga poses depending upon the angles of various body joints.
    Args:
        landmarks: A list of detected landmarks of the person whose pose needs to be classified.
        output_image: A image of the person with the detected pose landmarks drawn.
        display: A boolean value that is if set to true the function displays the resultant image with the pose label 
        written on it and returns nothing.
    Returns:
        output_image: The image with the detected pose landmarks drawn and pose label written.
        label: The classified pose label of the person in the output_image.
        Shots: Number of correct repitiotions.

    '''
    cv2.line(output_image, (landmarks[16][0], landmarks[16][1]), (landmarks[14][0], landmarks[14][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[12][0], landmarks[12][1]), (landmarks[14][0], landmarks[14][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[12][0], landmarks[12][1]), (landmarks[24][0], landmarks[24][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[26][0], landmarks[26][1]), (landmarks[24][0], landmarks[24][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[26][0], landmarks[26][1]), (landmarks[28][0], landmarks[28][1]), (255, 255, 255), 3)

    cv2.line(output_image, (landmarks[15][0], landmarks[15][1]), (landmarks[13][0], landmarks[13][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[13][0], landmarks[13][1]), (landmarks[11][0], landmarks[11][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[11][0], landmarks[11][1]), (landmarks[23][0], landmarks[23][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[25][0], landmarks[25][1]), (landmarks[23][0], landmarks[23][1]), (255, 255, 255), 3)
    cv2.line(output_image, (landmarks[25][0], landmarks[25][1]), (landmarks[27][0], landmarks[27][1]), (255, 255, 255), 3)

    cv2.circle(output_image, (landmarks[12][0], landmarks[12][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[12][0], landmarks[12][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[14][0], landmarks[14][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[14][0], landmarks[14][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[16][0], landmarks[16][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[16][0], landmarks[16][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[11][0], landmarks[11][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[11][0], landmarks[11][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[13][0], landmarks[13][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[13][0], landmarks[13][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[15][0], landmarks[15][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[15][0], landmarks[15][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[23][0], landmarks[23][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[28][0], landmarks[28][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[25][0], landmarks[25][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[24][0], landmarks[24][1]), 15, (255, 0, 0), 2)

    cv2.circle(output_image, (landmarks[27][0], landmarks[27][1]), 10, (255, 0, 0), cv2.FILLED)
    cv2.circle(output_image, (landmarks[26][0], landmarks[26][1]), 15, (255, 0, 0), 2)


    # Initialize the label of the pose. It is not known at this stage.
    global label
    global color
    label = 'SHOT NOT DETECTED'
    global Shots
    global flag_1
    global flag_2
    global flag_4
    global flag_5
    global flag_6
    global flag_7
    color = "red"
    global bar_1
    global right_shoulder_per_1
    global bar_2
    global right_shoulder_per_2  
    global right_elbow_per_1
    global right_elbow_per_2 
    global left_elbow_angle
    global right_elbow_angle
    global left_shoulder_angle
    global right_shoulder_angle
    global left_hip_angle
    global right_hip_angle
    global left_knee_angle
    global right_knee_angle

    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------
    
    # Get the angle between the left shoulder, elbow and wrist points. 
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    #print(left_elbow_angle)
    # Get the angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])   
    
    # Get the angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points. 
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    # Get the angle between the right hip, knee and ankle points. 
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],  
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
                                          
    # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points. 
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value], 
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
                                          
    
    #----------------------------------------------------------------------------------------------------------------

    if (80 < (right_elbow_angle) < 110):

        bar_1 = np.interp((right_elbow_angle), (70, 120), (0, 100))
        right_shoulder_per_1 = np.interp(right_elbow_angle, (70, 120), (0, 100))

        bar_2 = np.interp((right_elbow_angle), (50, 160), (0, 100))
        right_shoulder_per_2 = np.interp(right_elbow_angle, (50, 160), (0, 100))

    elif(80 < (360-right_elbow_angle) < 110):

        bar_1 = np.interp((360-right_elbow_angle), (70, 120), (0, 100))
        right_shoulder_per_1 = np.interp((360-right_elbow_angle), (70, 120), (0, 100))

        bar_2 = np.interp((right_elbow_angle), (50, 160), (0, 100))
        right_shoulder_per_2 = np.interp(right_elbow_angle, (50, 160), (0, 100))

            # if angle1>120 or angle2>120:
            #     if angle3>70 or angle4>70:
            #         if angle5>80 or angle6>80:



#----------------------------------------------------------------------------------------------------------------

    # elif (((120 < left_knee_angle < 170) and (90 < right_knee_angle < 190)) or
    # ((130 < (360-left_knee_angle) < 170) and (90 < (360-right_knee_angle) < 190))):
    #     flag_1 = 1

    #     # if (((60 < left_hip_angle < 100) or (60 < right_hip_angle < 100)) or
    #     # ((60 < (360-left_hip_angle) < 100) or (60 < (360-right_hip_angle) < 100))):

    #         # Check if shoulders are at the required angle.
    #     if (((70 < left_shoulder_angle < 110) and (30 < right_shoulder_angle < 190)) or
    #     ((70 < (360-left_shoulder_angle) < 110) and (30 < (360-right_shoulder_angle) < 190))):
    #         # flag_2 = 1

            
    #         if (((10 < left_elbow_angle < 190) and (10 < right_elbow_angle < 110)) or
    #         ((10 < (360-left_elbow_angle) < 190) and (10 < (360-right_elbow_angle) < 110))):

    #             label='COVER DRIVE DETECTED'
    #             flag_2 = 1

    # Check if the both side arms are at 90 degrees.
    # elif (((80 > left_knee_angle > 120) or (80 > right_knee_angle > 120)) or
    # ((80 < (360-left_knee_angle) > 110) or (80 > (360-right_knee_angle) > 110))):
    #     flag_1 = 1

    #     if (((50 < left_hip_angle < 70) or (50 < right_hip_angle < 170)) or
    #     ((50 < (360-left_hip_angle) < 195) or (50 < (360-right_hip_angle) < 70))):

    #         # Check if shoulders are at the required angle.
    #         if (((70 < left_elbow_angle < 80) or (70 < right_elbow_angle < 80)) or
    #         ((70 < (360-left_elbow_angle) < 80) or (70 < (360-right_elbow_angle) < 80))):

    #             label='COVER DRIVE DETECTED'
    #             flag_2 = 1


    # elif (((80 < left_shoulder_angle < 110) or (80 < right_shoulder_angle < 110)) or
    # ((80 < (360-left_shoulder_angle) < 110) or (80 < (360-right_shoulder_angle) < 110))):
    #     flag_4 = 1

    #     # Check if shoulders are at the required angle.
    #     if (((160 < left_elbow_angle < 195) or (160 < right_elbow_angle < 195)) or
    #     ((160 < (360-left_elbow_angle) < 195) or (160 < (360-right_elbow_angle) < 195))):

    #         label='PULL SHOT DETECTED'
    #         flag_5 = 1


#********************************************************************************
            # if angle1>120 or angle2>120:
            #     if angle3>70 or angle4>70:
            #         if angle5>80 or angle6>80:
#********************************************************************************
#********************************************************************************

    # elif (((120 < left_knee_angle) or (120 < right_knee_angle)) or
    # ((120 < (360-left_knee_angle) < 170) and (120 < (360-right_knee_angle)))):
    #     flag_1 = 1

    #     # if (((60 < left_hip_angle < 100) or (60 < right_hip_angle < 100)) or
    #     # ((60 < (360-left_hip_angle) < 100) or (60 < (360-right_hip_angle) < 100))):

    #         # Check if shoulders are at the required angle.
       
    #     if (((70 < left_elbow_angle) and (70 < right_elbow_angle)) or
    #     ((70 < (360-left_elbow_angle)) and (70 < (360-right_elbow_angle)))):

    #         if (((80 < left_shoulder_angle) and (80 < right_shoulder_angle)) or
    #         ((80 < (360-left_shoulder_angle)) and (80 < (360-right_shoulder_angle)))):
    #             #flag_2 = 1

            
    #             label='COVER DRIVE DETECTED'
    #             flag_2 = 1

    elif (((80 < left_shoulder_angle < 110) or (80 < right_shoulder_angle < 110)) or
    ((80 < (360-left_shoulder_angle) < 110) or (80 < (360-right_shoulder_angle) < 110))):
        flag_4 = 1

        # Check if shoulders are at the required angle.
        if (((100 < left_elbow_angle) or (100 < right_elbow_angle)) or
        ((100 < (360-left_elbow_angle)) or (100 < (360-right_elbow_angle)))):

            label='PULL SHOT DETECTED'
            flag_5 = 1

##############################################################################################
    # elif (((120 < left_knee_angle) or (120 < right_knee_angle)) or
    # ((120 < (360-left_knee_angle) < 170) and (120 < (360-right_knee_angle)))):
    

        # if (((60 < left_hip_angle < 100) or (60 < right_hip_angle < 100)) or
        # ((60 < (360-left_hip_angle) < 100) or (60 < (360-right_hip_angle) < 100))):

            # Check if shoulders are at the required angle.
       

    # elif (((50 < left_knee_angle) or (50 < right_knee_angle)) or
    # ((50 < (360-left_knee_angle)) and (50 < (360-right_knee_angle)))):


    #         if (((110> left_shoulder_angle) and (110> right_shoulder_angle)) or
    #         ((110> (360-left_shoulder_angle)) and (110> (360-right_shoulder_angle)))):
    #             #flag_2 = 1

    #             if (((150 > left_elbow_angle)or
    #             ((150> (360-left_elbow_angle))))):

    #         #flag_1 = 1
    # # elif (((80 < left_shoulder_angle < 110) or (80 < right_shoulder_angle < 110)) or
    # # ((80 < (360-left_shoulder_angle) < 110) or (80 < (360-right_shoulder_angle) < 110))):
    # #     flag_4 = 1

    # #     # Check if shoulders are at the required angle.
    # #     if (((100 < left_elbow_angle) or (100 < right_elbow_angle)) or
    # #     ((100 < (360-left_elbow_angle)) or (100 < (360-right_elbow_angle)))):

    #                 label= 'COVER DRIVE DETECTED'
    #                 flag_5 = 1

    #             if (((150< left_elbow_angle) or
    #             ((150<  (360-left_elbow_angle))))):
    #                 label='PULL SHOT DETECTED'
    #                 flag_2 = 1


    if ( flag_2!=0) and (flag_5 !=0):

        Shots += 1
        # flag_1 = 0
        flag_2 = 0
        #flag_4 ==0
        flag_5 =0
        

    #----------------------------------------------------------------------------------------------------------------

    # Check if the pose is classified successfully
    if label != 'SHOT NOT DETECTED':
        
        # Update the color (to green) with which the label will be written on the image.
        color = "green"  

    # Return the output image and the classified label.
    return output_image, label


pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

# Function for Second Window when the Proceed Button is pressed.
def proceed():

    '''
    This function displays a Window with two Buttons, asking the user to select between Live Camera
    stream and Recorded Videos.

    '''

    win.destroy() # Destroying the previous window

    # Displaying the new window
    global root #name of 2nd window
    root = Tk()
    root.geometry("1350x740")
    # root.configure(background="dark violet")
    root.title("Main Menu")


    bgimg=PhotoImage(file="E:\CricketShotDetection\Working code\hardball.png")

    canvas=Canvas(root, width=1350, height=740)
    canvas.place(x=0,y=0)
    canvas.create_image(0,0, image=bgimg, anchor='nw')
    # Live Button
    live_btn = Button(root, text = 'Live Camera', bg = "yellow", fg = "Black", font = "Calibri 14 bold", relief = "solid", borderwidth = 12, command = live_bt)
    live_btn.place(x = 650, y = 200, width=140, height=55)

    # Video Button 
    video_btn = Button(root, text = 'Recorded Video', bg = "yellow", fg = "Black", font = "Calibri 14 bold", relief = "solid", borderwidth = 12, command = videoBtn)
    video_btn.place(x = 630, y = 400, width=200, height=55)

    root.mainloop() #update root window

# Video Button Window Function
def videoBtn():

    '''
    This function displays a Window on which Recorded videos will be played. User can switch between
    videos via the options given.
    
    '''

    root.destroy() # Destrying previous window

    # Configuring New Window
    global browse_btn
    global video

    video = Tk()
    video.geometry("1350x740")
    video.configure(background="DarkOrange1")
    video.title("Select Video")

    # Widgets
    browse_btn = Button(video, text = 'Browse Video', bg = "saddle brown", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 10, command=browse)
    browse_btn.place(x = 420, y = 480, width=150, height=60)

    back_btn = Button(video, text = 'Back', bg = "saddle brown", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 1, command=back_video)
    back_btn.place(x = 50, y = 30, width=100, height=25)

def browse():

    global vid
    global Shots
    Shots = 0
    global rect
    # w13 = Label(video, bg = "White")
    # w13.place(x=50, y=60, width=900, height=300)
    browse_btn.configure(text='Change Video', command=browse)    

    video.filename = filedialog.askopenfilename(initialdir="E:\CricketShotDetection\Working code",
    title="Video Selection", filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
    vid = video.filename
    if (vid != ''):
        play_video()


def play_video():

    global cap
    global w
    global h
    global label1
    global rect
    global bar_1
    global right_shoulder_per_1
    global flag_2
    global flag_5


    frame_1 = Frame(video, width=670, height=700, bg="DarkOrange1").place(x=0, y=0)

    cap = cv2.VideoCapture(vid)

    w = 400
    h = 400

    flag_2 =0
    flag_5 =0
    label1 = Label(frame_1, width=w, height=h)
    label1.place(x=300, y=50)

    rect = Progressbar(video, orient=HORIZONTAL, length=200, mode="determinate")
    rect.place(x = 800, y = 60, width=450, height=50)

    select_img()
    bar_1 = 0
    right_shoulder_per_1 = 0

    browse_btn = Button(video, text = 'Change video', bg = "SpringGreen2", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 14, command=browse)
    browse_btn.place(x = 420, y = 480, width=150, height=60)

    back_btn = Button(video, text = 'Back', bg = "saddle brown", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 1, command=back_browse)
    back_btn.place(x = 50, y = 30, width=100, height=25)


def select_img():

    global rect

    _, frame = cap.read()

    #frame = cv2.flip(frame, 1)

    frame, landmarks = detectPose(frame, pose_video, display=False)

    if landmarks:

        # Perform the Pose Classification.
        frame, _ = classifyPose(landmarks, frame, display=False)

    rep = Label(video, text = f'Shots:\n{int(Shots)}', bg = "midnight blue", fg = "red", font = "Times 20 bold")
    rep.place(x = 800, y = 140, width=160, height=70)

    pos = Label(video, text = 'POSITION:', bg = "midnight blue", fg = "Black", font = "Times 20 bold")
    pos.place(x = 800, y = 250, width=160, height=35) 

    lab = Label(video, text = f'{label}', bg = "midnight blue", fg = f"{color}", font = "Times 20 bold")
    lab.place(x = 800, y = 310, width=360, height=30)  

    rect['value'] = bar_1

    per = Label(video, text=f'{int(right_shoulder_per_1)}%',bg = "midnight blue", fg = "red", font = "Times 20 bold")
    per.place(x = 820, y = 15, width=80, height=40) 
    frame = cv2.resize(frame, (w, h))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage

    # print(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle, 
    # left_hip_angle, right_hip_angle, left_knee_angle, right_knee_angle)

    video.after(2, select_img)


def live_stream():
    global bar_2
    global right_shoulder_per_2

    _, frame = cap.read()

    #frame = cv2.flip(frame, 1)

    frame, landmarks = detectPose(frame, pose_video, display=False)

    if landmarks:

        # Perform the Pose Classification.
        frame, _ = classifyPose(landmarks, frame, display=False)

    pos = Label(live, text = 'POSITION:', bg = "blue2", fg = "Black", font = "Times 20 bold")
    pos.place(x = 610, y = 20, width=160, height=35) 

    lab = Label(live, text = f'{label}', bg = "blue2", fg = f"{color}", font = "Times 20 bold")
    lab.place(x = 530, y = 50, width=320, height=30)  

    rect = Progressbar(live, orient=HORIZONTAL, length=200, mode="determinate")
    rect.place(x = 450, y = 540, width=450, height=50)
    rect['value'] = bar_2

    per = Label(live, text=f'{int(right_shoulder_per_2)}%',bg = "blue2", fg = "Black", font = "Times 20 bold")
    per.place(x = 900, y = 540, width=80, height=40) 

    frame = cv2.resize(frame, (w, h))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage

    live.after(2, live_stream)
    bar_2 = 0
    right_shoulder_per_2 = 0

def back_browse():

    global Shots
    video.destroy()
    global root
    root = Tk()
    root.geometry("1x1")
    Shots=0
    videoBtn()

# Live Button Button Window Function
def live_bt():

    '''
    This function displays a Window on which Live Stream will be taken from Camera. User can select 
    any of the options given.
    
    '''
    root.destroy() # Destrying previous window

    # Configuring New Window
    global start_btn
    global live
    live = Tk()
    live.geometry("1350x740")
    live.configure(background="blue2")
    live.title("Web Cam")

    # Widgets
    # w7 = Label(live, text = 'Guide', bg = "light blue", fg = "Black", font = "Verdana 15 bold")
    # w7.place(x = 800, y = 150, width=160, height=22)


    global cap
    global w
    global h
    global label1
    global flag_2
    global flag_5
 
    frame_1 = Frame(live, width=670, height=700, bg="blue2").place(x=0, y=0)

    cap = cv2.VideoCapture(0)


    flag_2 = 0
    flag_5 =0
    w = 600
    h = 400

    label1 = Label(frame_1, width=w, height=h)
    label1.place(x=350, y=90)


    start_btn = Button(live, text = 'START', bg = "light blue", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 10, command=start)
    start_btn.place(x = 600, y = 620, width=160, height=55) 

    back_btn = Button(live, text = 'BACK', bg = "light blue", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 1, command=back)
    back_btn.place(x = 30, y = 20, width=100, height=30)

    threading.Thread(target=live_stream).start()

    live.mainloop()





def back():

    '''
    This function displays a Back Button which if pressed will get the user to the previous window.
    
    '''
    # Destroying current window and getting back to previous one.
    global win
    live.destroy()
    win = Tk()
    win.geometry("1350x740")

    proceed()

def back_video():

    '''
    This function displays a Back Button which if pressed will get the user to the previous window.
    
    '''
    # Destroying current window and getting back to previous one.

    video.destroy()
    global win
    win = Tk()
    win.geometry("1350x740")

    proceed()

# Initializing the value of Timer
hours = 0
minutes = 0
seconds = 0
flag_3 = 1

def start():

    global Shots
    global flag_3

    timer()

    start_btn.configure(text='STOP', command=stop)

    reset_btn = Button(live, text = 'RESET', bg = "light blue", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 14, command=reset)
    reset_btn.place(x = 400, y = 620, width=160, height=55)

    results_btn = Button(live, text = 'PROGRESS', bg = "light blue", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 10, command=results)
    results_btn.place(x = 800, y = 620, width=160, height=55)

def timer():

    '''
    This function displays a Timer on the window in order to note down the total time of workout.
    
    '''

    # Setting as Global variables to retain the value of timer
    global hours
    global minutes
    global seconds
    global clock
    global flag_3
    global Shots

    if flag_3 == 1:

        Shots = 0

    # Widgets
    clock = Label(live, text='00:00:00', height=2, bg='blue2', fg='red', font='Times 20')
    clock.place(x=1000, y=80, width=170, height=25)

    clock.config(text=f'{hours:02}:{minutes:02}:{seconds:02}')

    w9 = Label(live, text = 'Time:', bg = "blue2", fg = "red", font = "Times 25 bold")
    w9.place(x = 995, y = 40, width=170, height=25)

    seconds += 1

    if seconds == 60:

        minutes += 1
        seconds = 0

    if minutes == 60 and seconds == 0:

        hours += 1
        minutes = 0
        seconds = 0

    flag_3 += 1
    


    rep = Label(live, text = f'Shots:\n{int(Shots)}', bg = "blue2", fg = "red", font = "Times 20 bold")
    rep.place(x = 170, y = 20, width=160, height=70)

    live.after(1000, start)

def stop():

    '''
    This function displays a Stop Button which if pressed will stop the analysis.
    
    '''

    # DEstroying current window and showing the starting window again
    global root

    live.destroy()
    root = Tk()
    root.geometry("1x1")
    root.configure(background="dark green")
    root.title("Main Menu")

    live_bt()


def reset():

    '''
    This function displays a Reset Button which if pressed will reset the Timer.
    
    '''

    # Setting global variables to initialize them.
    global root
    global hours
    global minutes
    global seconds
    global clock

    # Giving the initial value of Timer
    hours=0
    minutes=0
    seconds=0

    # Updating the window
    live.destroy()
    root = Tk()
    root.geometry("1x1")
    root.configure(background="dark green")
    root.title("Main Menu")

    live_bt()

def results():

    '''
    This function displays a Show Results Button which if pressed will display the summary of the exercise.
    
    '''

    # Destroying the current window and initializing the Timer again.
    live.destroy()

    global hours
    global minutes
    global seconds

    global clock
    global result

    # Configuring the Results Window
    result = Tk()
    result.geometry("1350x740")
    result.configure(background="red2")
    result.title("Result")
    cap.release()

    # Widgets
    w10 = Label(result, text = 'Player Session', bg = "Black", fg = "medium violet red", font = "Verdana 15 bold")
    w10.place(x = 250, y = 80, width=200, height=25) 

    w11 = Label(result, text = f'{hours:02}:{minutes:02}:{seconds-1:02}', bg = "Black", fg = "medium violet red", font = "Verdana 15 bold")
    w11.place(x = 230, y = 115, width=200, height=25)

    w14 = Label(result, text = 'Total Shots', bg = "Black", fg = "medium violet red", font = "Verdana 15 bold")
    w14.place(x = 250, y = 150, width=200, height=25) 

    w15 = Label(result, text = f'{int(Shots)}', bg = "Black", fg = "medium violet red", font = "Verdana 15 bold")
    w15.place(x = 230, y = 180, width=200, height=25)

    back_btn = Button(result, text = 'Back to Main Menu', bg = "medium violet red", fg = "Black", font = "Times 14 bold", relief = "solid", borderwidth = 10, command=main_menu)
    back_btn.place(x = 30, y = 20, width=250, height=50)

    hours=0
    minutes=0
    seconds=0

def main_menu():

    '''
    This function displays a Main Menu Button which if pressed will get the user to the Main Menu.
    
    '''

    # Destroying the current window and Displaying the Main Window
    result.destroy()

    global win
    win = Tk()
    win.geometry("1350x740")

    proceed()

# Widgets of the First Window
w1 = Label(win, text = 'Welcome to Cricket Shot detection \n [Pull Shot and Cover Drive Analysis]', bg = "yellow", fg = "Black", font = "Verdana 15 bold")
w1.place(x = 0, y = 30, width=1400, height=55)

w2 = Label(win, text = 'Designed By:', bg = "White", fg = "Black", font = "calibri 12 bold")
w2.place(x = 330, y = 460, width=110, height=25)

w3 = Label(win, text = 'Faizan Tanveer  2020-MC-62', bg = "White", fg = "Black", font = "Times 12 bold")
w3.place(x = 330, y = 500, width=200, height=22)

w4 = Label(win, text = 'Khurram Aziz  2020-MC-49', bg = "White", fg = "Black", font = "Times 12 bold")
w4.place(x = 330, y = 530, width=190, height=22)

w5 = Label(win, text = 'Instructor:', bg = "White", fg = "Black", font = "calibri 12 bold")
w5.place(x = 900, y = 460, width=110, height=25)

w6 = Label(win, text = 'Sir Ahsan Naeem', bg = "White", fg = "Black", font = "Times 12 bold")
w6.place(x = 900, y = 500, width=160, height=22)

proceed_btn = Button(win, text = 'Proceed', bg = "Black", fg = "White", font = "Times 14 bold", relief = "solid", borderwidth = 12, command = proceed)
proceed_btn.place(x = 620, y = 300, width=120, height=50)


# Applying looping on each window
win.mainloop()
# root.mainloop()
# live.mainloop()
# result.mainloop()
# video.mainloop()