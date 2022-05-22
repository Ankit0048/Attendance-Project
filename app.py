from flask import Flask, redirect, render_template, request, Response, redirect
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
            faceLoc = face_recognition.face_locations(frame)
            face_encoding = face_recognition.face_encodings(frame)
            if len(faceLoc)!=0:
                faceLoc = faceLoc[0]
                frame = cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 0), 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type : image/jpeg\r\n\r\n'+frame+b'\r\n')

@app.route('/')
def index():
    # The main home poge of the web app is called
    user_email, user_name, user_password, match= "", "", "", ""
    return render_template('index.html')

# Get the registration details of the user 
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = 0
    if request.method == 'POST':
        global user_email
        user_email = request.form['email_id']
        global user_name
        user_name = request.form['user_id']
        global user_password
        user_password = request.form['password']
        global match
        match = request.form['password_match']

        print(user_email, user_name, user_password, match)
        if len(user_email.strip())==0 or len(user_name.strip())==0 or len(user_password.strip())==0 or len(match.strip()) == 0:
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
                print("going to next page")
                return redirect('/registercam')
    else:
        return render_template ('register.html', tasks=error)


@app.route('/registercam', methods=['POST', 'GET'])
def registercam():
    if request.method =="POST":
        if len(face_encoding)==0:
            return redirect('registerCam.html', tasks=0)
        else:
            camera.release()
            return redirect('/',task)
        
    else:
        return render_template('registerCam.html',tasks=1)


@app.route('/video')
def video():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)