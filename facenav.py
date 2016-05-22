#

def closest_face(faces):
    '''
    This function finds and returns the closes face in the faces array as
    output by an openCV haar cascade classifier.  If no faces are found it
    returns False
    '''
    if len(faces) == 0:  # No faces
        return False
    else:
        # Start assuming the first face is the closest
        closest = faces[0]
        for face in faces:
            1/0
