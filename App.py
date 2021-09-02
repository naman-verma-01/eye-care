import time
import cv2
import streamlit as st
import imutils
import requests
import numpy as np
import matplotlib.pyplot as plt

# distance from camera to object(face) measured
# centimeter
Known_distance = 51
#url = "http://192.168.43.1:8080/shot.jpg"
# width of face in the real world or Object Plane
# centimeter
Known_width = 14.3


i = 0
j = 0
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
if 'Sec' not in st.session_state:
    st.session_state.Sec = 1
if 'NearSec' not in st.session_state:
    st.session_state.NearSec = 0
if 'FarSec' not in st.session_state:
    st.session_state.FarSec = 0
if 'CorrectSec' not in st.session_state:
    st.session_state.CorrectSec = 0
if 'Distarray' not in st.session_state:
    st.session_state.Distarray = []

#NearSec, NearMin, NearHr = 0, 0, 0
#FarSec, FarMin, FarHr = 0, 0, 0
#CorrectSec, CorrectMin, CorrectHr = 0, 0, 0
#Sec, Min, Hr = 0, 0, 0
value = st.sidebar.radio('Radio', ["Main App", "About"])



# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
state = None
# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame

    # return the distance
    return distance


def face_data(image):
    face_width = 0  # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width


def face_data2(image):
    face_width = 0  # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width
if value == "Main App":
    st.title("Eye Friend")
    st.write("Sit at the distance of 52cm or 20inches from your computer/laptop screen.")
    st.write("Face your webcam and click on the run check box to start.")
    start = st.checkbox("Start")
    run = st.checkbox("Run?")
    check = st.button("Check")
    graph1 = st.button("graph")
    Frame_window = st.image([])

    cap = cv2.VideoCapture(0)

    while start:
        try:

            _, frame = cap.read()
    #        img = requests.get(url)
    #        img_arr = np.array(bytearray(img.content), dtype=np.uint8)
    #        img = cv2.imdecode(img_arr, -1)
            frame = imutils.resize(frame, width=1000, height=1800)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # detecting face in the image
            cv2.putText(
                frame, "Press 0 to capture at right distance", (30, 35),
                fonts, 0.6, GREEN, 2)
            if run:
                ref_image = frame
                ref_image_face_width = face_data(ref_image)
                Focal_length_found = Focal_Length_Finder(Known_distance, Known_width, ref_image_face_width)
                while True:
                    _, frame1 = cap.read()
                   # img = requests.get(url)
                   # img_arr = np.array(bytearray(img.content), dtype=np.uint8)
                   # img = cv2.imdecode(img_arr, -1)
                    frame1 = imutils.resize(frame1, width=1000, height=1800)
                    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    # detecting face in the image
                    face_width_in_frame = face_data(frame1)

                    # check if the face is zero then not
                    # find the distance
                    if face_width_in_frame != 0:
                        # finding the distance by calling function
                        # Distance distnace finder function need
                        # these arguments the Focal_Length,
                        # Known_width(centimeters),
                        # and Known_distance(centimeters)
                        Distance = Distance_finder(
                            Focal_length_found, Known_width, face_width_in_frame)

                        # draw line as background of text
                        cv2.line(frame1, (30, 30), (230, 30), RED, 32)
                        cv2.line(frame1, (30, 30), (230, 30), BLACK, 28)

                        # Drawing Text on the screen
                        cv2.putText(
                            frame1, f"Distance: {round(Distance, 2)} CM", (30, 35),
                            fonts, 0.6, GREEN, 2)
                        if Distance < 40:
                            cv2.putText(
                                frame1, "Move back please", (300, 40),
                                fonts, 2, (255, 0, 0), 2)
                            state = "Near"
                        elif Distance > 70:
                            state = "Far"
                        elif Distance < 70 and Distance > 40:
                            state = "Correct"
                        else:
                            pass
                      #  st.session_state.Distarray[j] = Distance
                      # j += 1
                        Frame_window.image(frame1)
                    time.sleep(1)


                    st.session_state.Sec += 1

                  #  print(Sec)

                    if state == "Near":
                        st.session_state.NearSec += 1
                    elif state == "Far":
                        st.session_state.FarSec += 1

                    if state == "Correct":
                        st.session_state.CorrectSec += 1

               # if check:
               #    st.write("Correct => ", convert(CorrectSec))
                    #print("Correct => ", convert(CorrectSec))
                #    st.write("Near => ", convert(NearSec))
                #    st.write("Far =>  ", convert(FarSec))
                #    st.write("Total => ", convert(Sec))
                #if check:
                ##    st.write("Correct Distance Maintained for %d : %d : %d" % (CorrectHr, CorrectMin, CorrectSec))
                 # #  print("Correct", CorrectHr, CorrectMin, CorrectSec)
                 #   st.write("Too Far Distance Maintained for %d : %d : %d" % (FarHr, FarMin, FarSec))
                  #  print("Far", FarHr, FarMin, FarSec)
                #    st.write("Too Near Distance Maintained for %d : %d : %d" % (NearHr, NearMin, NearSec))
                  #  print("Near", NearHr, NearMin, NearSec)
                #    st.write("Total Time measured %d : %d : %d" % (Hr, Min, Sec))

            #if Check:
            #    st.write("Correct Distance Maintained for %d : %d : %d" % (CorrectHr, CorrectMin, CorrectSec))
            ##    st.write("Too Far Distance Maintained for %d : %d : %d" % (FarHr, FarMin, FarSec))
             #   st.write("Too Near Distance Maintained for %d : %d : %d" % (NearHr, NearMin, NearSec))
             #   st.write("Total Time measured %d : %d : %d" % (Hr, Min, Sec))


            # looping through the facblanes detect in the image
            # getting coordinates x, y , width and height
            Frame_window.image(frame)
            # reading reference_image from directory
        except:
            pass
    data = [st.session_state.CorrectSec,st.session_state.NearSec,st.session_state.FarSec]
    Data = ["Correct","Near","Far"]
    if check:
       # st.write("Correct => ", convert(st.session_state.CorrectSec))
       # st.write("Near => ",  convert(st.session_state.NearSec))
       # st.write("Far =>  ",convert(st.session_state.FarSec))
       # st.write("Total => ",  convert(st.session_state.Sec))
        plt.bar(Data, data, color='maroon',
                width=0.4)
        st.subheader("Correct " + convert(st.session_state.CorrectSec))
        st.progress((st.session_state.CorrectSec/st.session_state.Sec)*100)
        st.subheader("Near " + convert(st.session_state.NearSec))
        st.progress((st.session_state.NearSec/st.session_state.Sec)*100)
        st.subheader("Far " + convert(st.session_state.FarSec))
        st.progress((st.session_state.FarSec/st.session_state.Sec)*100)
        st.subheader("Total " + convert(st.session_state.Sec))
        st.progress(st.session_state.Sec)
        plt.bar(Data, data, color='maroon',
            width=0.4)
        plt.xlabel("Distance")
        plt.ylabel("Time in Seconds")
        plt.title("Distance vs Time")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(transparent=True)
if value == "About":
    st.title("About..")
#data = [st.session_state.CorrectSec,st.session_state.NearSec,st.session_state.FarSec]
#Data = ["Correct","Near","Far"]
#if graph1 or check:
  #  st.bar_chart(st.session_state.CorrectSec,st.session_state.NearSec,st.session_state.FarSec)
#    plt.bar(Data, data, color='maroon',
#            width=0.4)

 #   plt.xlabel("Distance")
 #   plt.ylabel("Time in Seconds")
 #   plt.title("Distance vs Time")
 #   st.set_option('deprecation.showPyplotGlobalUse', False)
 #   st.pyplot()


#Styling Code
st.markdown(
    """
<style>

.css-1v3fvcr{
    background: linear-gradient(225deg,#bdc3c7 ,#2c3e50);
}
."st-bg st-b2 st-bh st-bi st-bj st-bk st-bl st-bm st-bn st-bo st-bp st-bq st-br st-bs st-bt st-bu st-bv st-bw st-bx st-by st-bz st-av st-aw st-ax st-ay st-c0 st-c1 st-c2 st-c3 st-c4 st-c5 st-c6 st-c7 st-c8 st-c9 st-ca st-cb"{
    background: #bdc3c7

}
.marks {
    border : 3px solid #2c3e50;
    border-radius : 7px;
}

</style>
""",
    unsafe_allow_html=True,
)
