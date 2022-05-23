from flask import Flask, g, redirect, render_template, request, Response, redirect
from flask_sqlalchemy import SQLAlchemy
import cv2
import face_recognition


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'
db = SQLAlchemy(app)



class User(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    encoding = db.Column(db.String(), nullable=False)

    def __repr__(self) -> str:
        return "{}-{}".format(self.email,self.password)


def global_reset():
        global face_encoding
        face_encoding = []
        global user_email
        user_email = ""
        global name_user
        name_user = ""
        global user_password
        user_password = ""
        global match
        match = ""


def  generate_frame ():
    global face_encoding
    global camera
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame2 = cv2.resize(frame, (0,0), None, 0.25, 0.25)
            faceLoc = face_recognition.face_locations(frame2)
            face_encoding = face_recognition.face_encodings(frame2)
            if len(faceLoc)!=0:
                faceLoc = faceLoc[0]
                faceLoc2 = [int(x*4) for x in faceLoc]
                frame = cv2.rectangle(frame, (faceLoc2[3], faceLoc2[0]), (faceLoc2[1], faceLoc2[2]), (255, 0, 0), 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type : image/jpeg\r\n\r\n'+frame+b'\r\n')

@app.route('/')
def index():
    # The main home poge of the web app is called
    try:
        camera.release()
        if name_user == "" and match==1:
            global_reset()
            # Opens the main page with a text message when the registration is complete
            return render_template('index.html', tasks= 0)
        else:
            global_reset()
            return render_template('index.html',tasks=1)
    except: 
        pass
    global_reset()
    return render_template('index.html', tasks=1)

# Get the registration details of the user 
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = 0
    if request.method == 'POST':
        global user_email
        user_email = request.form['email_id']
        global name_user
        name_user = request.form['user_id']
        global user_password
        user_password = request.form['password']
        global match
        match = request.form['password_match']

        if len(user_email.strip())==0 or len(name_user.strip())==0 or len(user_password.strip())==0 or len(match.strip()) == 0:
            error = 1
            # Error because the fields were empty so ask the user to enter the information again and put a message
            return render_template('register.html', tasks=error)
        elif user_password != match:
            error = 2
             # Error because the password did not match so ask the user to enter the information again and put a message
            return render_template('register.html', tasks=error)
        else:
            try:
                 # Error because the email id already exist so ask the user to enter the information again and put a message
                User.query.get_or_404(user_email)
                error = 3
                return render_template('register.html', tasks=error)
            except:
                return redirect('/registercam')
    else:
        return render_template ('register.html', tasks=error)


@app.route('/registercam', methods=['POST', 'GET'])
def registercam():
    if request.method =="POST":
        if len(face_encoding)==0:
            # if the face is not recognized to come out with a message
            return render_template('registerCam.html', tasks=0)
        else:
            # converted the user face encoding into string to store
            encoding_list = face_encoding[0].tolist()
            encoded_string = " ".join([str(X) for X in encoding_list])
            # create an object to store in the database
            user_register = User(email=user_email, password=user_password, user_name=name_user, encoding=encoded_string)
            # Add the registered data of the user in the database
            db.session.add(user_register)
            db.session.commit()
            global_reset()
            # Here match is used as a flag to show that the registration is being done
            global match
            match=1
            return redirect('/')
        
    else:
        return render_template('registerCam.html',tasks=1)


@app.route('/video')
def video():
    # get the camera input in the browser 
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html', tasks=1)


if __name__ == '__main__':
    app.run(debug=True)