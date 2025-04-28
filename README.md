## Face recognition project (face detection, face recognition) with the Django framework.

In this project, the  ``dlib`` library has been used in a custom way.
Generally, it receives images in separate forms, then recognizes each form and compares it with the database model, and I can separate the unknowns and the known ones and even save their images in separate folders...

# The algorithm has an accuracy of 98.86 You can see part of the algorithm in the following link to better understand it:

ref : https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

You can receive images from two cameras at the same time. To set it up, refer to the following file:`` verifi/camera.py ``

And to view the output of the camera views: `` 127.0.0.1:8000/stream ``

To create a new model (for people who are going to be recognized), follow this address:‍‍`` ‍1‍2‍7.0.0.1/createMode ``

First, it receives specifications such as name or ID for the user from you, then to receive the model's photo, there are two solutions. First, get the saved photo. Second, take a photo from the camera.

