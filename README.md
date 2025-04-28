Face recognition project (face recognition, face recognition) with the Django framework. In this project, the dlib library has been used in a custom way.
Generally, it receives images in separate forms, then recognizes each form and compares it with the database model, and I can separate the unknowns and the known ones and even save their images in separate folders...


You can receive images from two cameras at the same time. To set it up, refer to the following file: verifi/camera.py

And to view the output of the camera views:

127.0.0.1:8000/stream
