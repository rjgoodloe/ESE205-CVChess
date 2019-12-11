from Camera import Camera
# test the camera 
def test_Camera():
    camera=Camera()
    assert camera
    assert camera.cam

# call the camera test 
test_Camera()
