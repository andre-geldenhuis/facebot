from raspirobotboard import *
rr = RaspiRobot()

# Sample face - x,y,w,h from lower left
test_faces = [[ 83,  27, 167, 167]]
test_face = test_faces[0]

scene_width = 320

#Turning hysteresis
turning_hyst = 25

# Turning proportional settings
turningK = 0.1
turningMax = 0.2 # Max time turning

# Drive toward face settings
target_face_width = 100
# Target face proportional controller settings
driveK = 0.1
driveMax = 0.2


scene_center = scene_width / 2.0

def closest_face(faces):
    '''
    This function finds and returns the closes face in the faces array as
    output by an openCV haar cascade classifier.  If no faces are found it
    returns False.  Otherwise returns the closest face with it coordinates and
    bounding box.
    returns [x,y,w,h]
    '''
    if len(faces) == 0:  # No faces
        return False
    else:
        # Start assuming the first face is the closest
        closest = faces[0]
        [xc,yc,wc,hc] = closest

        for face in faces:
           [x,y,w,h] = face
           # if this face is closer
           if w > wc:
               closest = face
               [xc,yc,wc,hc] = closest

        return closest

def facedrive(face):
    '''
    Navigates toward the detected face -- menacingly
    '''
    [x,y,w,h] = face
    face_center = x + y/2.0

    # face center difference -ve means left adjust necessary, +ve means right adjust
    face_center_error= face_center - face_center

    #If outside the turning hysteresis window, turn, else don't.
    if abs(face_center_error) > turning_hyst:
        # turn
        # proportional control the turn
        turn_right = face_center_error >= 0
        turn_time = turningK * abs(face_center_error)
        if turn_time > turningMax:
            turn_time = turningMax

        # Commence turning
        if turn_right:
            rr.right(turn_time)
        else:
            rr.left(turn_time)

    else:
        #drive toward faces -- +ve == drive toward
        drive_error = target_face_width - w
        drive_forward = drive_error >= 0

        # Proportional Control
        drive_time = driveK * abs(drive_error)
        if drive_time > driveMax:
            drive_time = driveMax

        if drive_forward:
            rr.forward(drive_time)
        else:
            rr.backward(drive_time)
