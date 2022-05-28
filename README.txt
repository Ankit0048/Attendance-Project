** Description **

Hi, I am Ankit kumar. I am a second year college student who is working on the  Attendance using Face recognition using a self designed API in flask.
The code is written in python version 3.10.4. The basic knowledge of HTML and CSS is being utilized. For the development of the webpages.
The app can register a user in a database and each put up his attendance by recognizing his face and is directly put up on the excel file depending on the time.
It has also admin control where he can see data of all the user and remove the registered user. It is like a portal where each user has id and password.

** The libraries used are:(Requirements.txt) **

    click==8.1.3
    cmake==3.22.4
    colorama==0.4.4
    dlib @ https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl
    et-xmlfile==1.1.0
    face-recognition==1.3.0
    face-recognition-models==0.3.0
    Flask==2.1.2
    Flask-SQLAlchemy==2.5.1
    greenlet==1.1.2
    gunicorn==20.1.0
    itsdangerous==2.1.2
    Jinja2==3.1.2
    MarkupSafe==2.1.1
    numpy==1.22.4
    opencv-python==4.5.5.64
    openpyxl==3.0.10
    Pillow==9.1.1
    SQLAlchemy==1.4.36
    Werkzeug==2.1.2

** Installation of libraries **

All libraries except dlib can be installed from pip install except for the dlib which gives an error.
First make sure cmake is been already installed. Instead of directly using "pip install dlib" use ->
"pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl"

Libraries Used:
1. flask                : pip install flask
2. flask_sqlalchemy     : pip install flask-sqlalchemy
3. cv2                  : pip install opencv-python
4. datetime             : by default in python
5. face_recognition     : pip install face-recognition
6. openpyxl             : pip install openpyxl

One can prefer installing all the libraries in a virtual environment with the required python version 3.10.4 or can directly 
install also in the system

If you wish to set up the virtual environment
** To Setup Virtual Environment **
1. pip install virtualenv
2. virtualenv env
3. .\env\Scripts\activate

Then install the requirements

** Instructions **

1.This development is designed for desktop web app. 
2.The excel workbook should not be edited manually as it corrupts the file.
3.While face registration and recognition one person at a time is preferred.
4.When giving the attendance the camera stops and image freezes on the screen after that you need to press Done.
5.An area with sufficient lightning is preferred. 
6.Current admin password : admin1234

** RUN **
1.To the run the program make sure all the libraries are present with their required version and python version 3.10.4 is installed.
2.In the root folder of Project open Command Prompt or any other terminal
3.Type the command 'python ./app.py' and execute