from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import os
import mysql.connector
import folium
import requests
import map

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="delta")
mycursor = mydb.cursor()

# UPLOAD_FOLDER = 'static/file/'
app = Flask(__name__)
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "5b0d498b57a2899ac882b7f6b8544290"
temp_data=[]

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to insert a new post into the database
def insert_post(user_id, image_path, post_content):
    sql = "INSERT INTO posts (user_id, image_path, post_content) VALUES (%s, %s, %s)"
    val = (user_id, image_path, post_content)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print("Post inserted successfully.")

# Function to retrieve all posts from the database
def get_all_posts():
    sql = "SELECT * FROM posts"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    return mycursor.fetchall()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/loginpost', methods=['POST', 'GET'])
def userloginpost():
    global data1
    if request.method == 'POST':
        data1 = request.form.get('uname')
        data2 = request.form.get('password')
        
        print("Username:", data1)  # Debug statement
        print("Password:", data2)  # Debug statement

        if data2 is None:
            return render_template('login.html', msg='Password not provided')

        sql = "SELECT * FROM `users` WHERE `uname` = %s AND `password` = %s"
        val = (data1, data2)

        try:
            mycursor.execute(sql, val)
            account = mycursor.fetchone()  # Fetch one row

            if account:
                # Consume remaining results
                mycursor.fetchall()
                mydb.commit()
                return render_template('post.html')
            else:
                return render_template('login.html', msg='Invalid username or password')
        except mysql.connector.Error as err:
            print("Error:", err)  # Debug statement
            return render_template('login.html', msg='An error occurred. Please try again.')

@app.route('/NewUser')
def newuser():
    return render_template('NewUser2.html')

@app.route('/reg', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        uname = request.form.get('uname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = request.form.get('age')
        password = request.form.get('psw')
        gender = request.form.get('gender')
        sql = "INSERT INTO users (name, uname, email , phone, age, password, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, uname, email, phone, age, password, gender)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('login.html')
    else:
        return render_template('NewUser2.html')
    

@app.route('/index3')
def index3():
    posts = get_all_posts()
    return render_template('post.html', posts=posts)


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Assuming you have a form field for user ID
        post_content = request.form.get('post_content')
        file = request.files['file']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)
        insert_post(user_id, image_path, post_content)
        return redirect(url_for('index3'))

@app.route('/main')
def main():
    return render_template('index1.html')

# @app.route('/index1')
# def index1():
#     return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

# def get_weather_data(city):
#     url = f"{BASE_URL}q={city}&appid={API_KEY}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         temp_data.append(data)
        

#         main = data['main']
#         coord = data['coord']
#         wind = data['wind']
#         temperature = main['temp'] - 273.15
#         humidity = main['humidity']
#         pressure = main['pressure']
#         wind_speed = wind['speed']
#         report = data['weather']
#         lon = coord['lon']
#         lat = coord['lat']
        
#         print(f"{city:-^30}")
#         print(f"Temperature: {round(temperature, 2)}°C")
#         print(f"Humidity: {humidity}%")
#         print(f"Pressure: {pressure} hPa")
#         print(f"Wind Speed: {wind_speed} m/s")
#         print(f"Longitude and Latitude: {lon}, {lat}")
#         print(f"Weather: {report[0]['main']}")
#         print(f"Weather Description: {report[0]['description']}")
        
#         return lat, lon
#     else:
#         print("Error in the HTTP request")
#         return None, None
# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         classes=['fish market','flower','ganapathi vilas scl','kaasi vishwanathar temple','kalki park']
#         # classes = ['bio fertility' , 'CSI Church','elephant','finlay scl','fish market','flower','ganapathi vilas scl','haridra nadhi','kaasi vishwanathar temple',' kalki park','katalai muttai','maiden colony','mannai narayanaswamy nagar','municipality','national scl','national scl ground','oil mill','old housing unit','pamani river','puthur','quaters','railway station','rajagopalaswamy temple','rukkumani kulam','saviour scl','Selliyamman Temple','silk','taluk office','thamarai kulam','vaithiya salai','vannan kuzham','veannai thali thiruvila','vennai thali mandapam','water tank'
#         #            'Hostel','Finally Ground','Airavatheeswarar Temple Kumbakonam','Ayi Kulam Kumbakonam',' Ezhutharinathar Temple Innambur','Garuda sevai kumbakonam','Government Men College kumbakonam','government women college kumbakonam','Handloom Silk making kumbakonam','Krishna school fire accident kumbakonam','Kumbeshwarar Temple kumbakonam','Mahamaha kulam kumbakonam','MGR school kumbakonam','Nageshwarar Temple kumbakona','Navagraha Temple','Potramarai kulam Kumbakonam','Ramaswamy Temple Kumbakonam','sri vedanarayana perumal temple kumbakonam','Srinivasa Ramanujam House']
#         desc={'fish market':'The Mannargudi fish market is located in Mannargudi, a town in the Thiruvarur district of Tamil Nadu, India. Mannargudi is known for its vibrant fish market, where a variety of fresh seafood is bought and sold daily. Fishermen bring in their catches from the nearby coastal areas, offering a wide range of fish, prawns, crabs, and other seafood to both locals and visitors',
#               'flower':'Mannargudi is also renowned for its flower market, which is a significant hub for the trade of flowers in the region. The town is particularly famous for its production of jasmine flowers, which are highly prized for their fragrance and aesthetic appeal. The Mannargudi flower market sees a bustling activity, especially in the early morning hours when fresh blooms arrive from nearby flower farms and gardens.',
#               'ganapathi vilas scl':' In Mannargudi, "Ganapathi Vilas" is a well-known vegetarian restaurant that serves South Indian cuisine. "SCL" could potentially stand for "South Indian Cuisine Lovers" or something similar, indicating a group or community related to South Indian food appreciation. Ganapathi Vilas is popular for its traditional Tamil Nadu dishes, including dosas, idlis, vadas, sambar, and various rice-based dishes like biryani and pongal.',
#               'kaasi vishwanathar temple':'The Kaasi Viswanathar Temple is a renowned Hindu temple located in Mannargudi, Tamil Nadu, India. Dedicated to Lord Shiva, this temple is one of the oldest and most significant religious landmarks in the region. The temple is also known as the Mannargudi Rajagopalaswamy Temple, as it is home to deities of both Lord Shiva and Lord Vishnu.',
#               'kalki park':'"Kalki Park" in Mannargudi, Tamil Nadu. However, it s possible that developments or new establishments have emerged since then. If "Kalki Park" is a recent addition, it might be a recreational area, park, or any other facility named after Kalki Krishnamurthy, the renowned Tamil writer and novelist. To get more accurate information about Kalki Park in Mannargudi, I suggest checking local directories, tourism websites, or contacting local authorities or residents in Mannargudi for the most up-to-date details.'}
#         file1 = request.files['filename']
#         imgfile = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        
#         # Create the directory if it doesn't exist
#         os.makedirs(os.path.dirname(imgfile), exist_ok=True)
        
#         file1.save(imgfile)
#         #model = load_model('model.h5')
#         model = load_model('keras_model.h5')
#         # Load the labels
#         # classes = open("labels.txt", "r").readlines()
#         img_ = image.load_img(imgfile, target_size=(224, 224, 3))
#         img_array = image.img_to_array(img_)
#         img_processed = np.expand_dims(img_array, axis=0)
#         img_processed /= 255.
#         prediction = model.predict(img_processed)
#         index = np.argmax(prediction)
#         result = "Unknown"
#         percentage = 0.0
#         value="description not availble"

#         if index < len(classes):
#             result = str(classes[index]).title()
#             value=desc.get(result.lower())
           
#         image_url = url_for('static', filename='file/' + file1.filename)
#         city="mannargudi"
#         url = f"{BASE_URL}q={city}&appid={API_KEY}"
#         response = requests.get(url)
    
#         if response.status_code == 200:
#             data = response.json()
#             temp_data.append(data)
#             temp_data1=f"{city:-^30}"+"\n"+f"Temperature: {round( data['main']['temp'] - 273.15, 2)}°C"+"\n"+f"Humidity: {data['main']['humidity']}%"+"\n"+f"Pressure: {data['main']['pressure']} hPa"+"\n"+f"Wind Speed: {data['wind']['speed']} m/s"+"\n"+f"Longitude and Latitude: {data['coord']['lon']}, {data['coord']['lat']}"+"\n"+f"Weather: {data['weather'][0]['main']}"+"\n"+f"Weather Description: {data['weather'][0]['description']}"
#         print("map_res",temp_data1)

#         return render_template('prediction_result1.html', msg=result,data=temp_data1 ,desc_msg =value, src=imgfile, view='style=display:block', view1='style=display:none')
#     elif request.method == 'GET':
#         return render_template('index.html')

# @app.route('/prediction_result')
# def prediction_result():
#     result = request.args.get('result')
#     image_url = request.args.get('image_url')
    
#     # Assuming 'result' contains the city name for which you want to display the weather map
#     city = result
    
#     # Generate weather map
#     weather_map_path = generate_weather_map(city)
    
#     if weather_map_path:
#         # If weather map is generated successfully, render the template with both prediction result and weather map
#         return render_template('prediction_result1.html', result=result, image_url=image_url, weather_map_path=weather_map_path)
#     else:
#         # If weather data is not available for the city, render the template with only prediction result
#         return render_template('prediction_result1.html', result=result, image_url=image_url)

@app.route('/upload2', methods=['POST', 'GET'])
def upload2():
    if request.method == 'POST':
        classes = ['butterfly park', ' kallanai', 'malaikottai', 'mukampur', 'samayapuram', 'srirakam', 'st joseph church', 'thepakulam']
        desc    = {'Butterfly Park': 'The Tropical Butterfly Conservatory, is located in the Upper Anaicut reserve forest in Srirangam. It covers 25 acres.',
                   'Kallanai': 'Kallanai Dam is the fourth oldest dam in the world, and first in India. It is a rock-solid project that has survived 2,000 years. The purpose of the dam was to divert the waters of the Kaveri across the fertile Thanjavur delta region for irrigation via canals.',
                   'Malaikottai':'Tiruchirappalli Rock Fort, locally known as Malaikottai, is a historic fortification and temple complex built on an ancient rock. It is located in the city of Tiruchirappalli, on the banks of river Kaveri, Tamil Nadu, India.',
                   'Mukampur':'Upper Anaicut or Mukkombu is about 18 kilometers (11 mi) west of Trichy and 2 kilometers away from Jeeyapuram at a point where River Kollidam branches out from the main river, Cauvery. It is a lovely picnic spot skirting acres of verdant greenery.',
                   'Samayapuram':'Arulmigu Sri Mariamman Temple, Samayapuram is an ancient Hindu temple in Tiruchirappalli district in Tamil Nadu, India. The main deity, Samayapuram Mariamman, a form of Adi Parashakti and Mariamman, is made of sand and clay with extractions of medicinal herbs unlike many of the traditional stone idols and is considered as most powerful Goddess.',
                    'Srirakam':'Srirangam is a neighbourhood in the city of Tiruchirappalli in the Indian state of Tamil Nadu. A river island, Srirangam is bounded by the Kaveri River on one side and its distributary Kollidam on the other side.',
                    'St joseph church':'St. Joseph Church is a common name for Catholic churches dedicated to St. Joseph, the husband of the Virgin Mary and the earthly father of Jesus Christ.',
                    'Teppakulam':'Teppakulam is a locality near the centre of the Indian city of Tiruchirappalli. It consists of a large artificial tank surrounded by bazaars, prominent among which is a flower market.'}
        file1 = request.files['filename']
        imgfile = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(imgfile), exist_ok=True)
        
        file1.save(imgfile)
        #model = load_model('model.h5')
        model = load_model('keras_model.h5')
        # Load the labels
        #classes = open("labels.txt", "r").readlines()
        img_ = image.load_img(imgfile, target_size=(224, 224, 3))
        img_array = image.img_to_array(img_)
        img_processed = np.expand_dims(img_array, axis=0)
        img_processed /= 255.
        prediction = model.predict(img_processed)
        index = np.argmax(prediction)
        result = "Unknown"
        value = "Description not available"

        if index < len(classes):
            result = str(classes[index]).title()
            print("result",result)
            # Retrieve description from desc dictionary based on result
            value = desc.get(result, "Description not available")  # Get description or default message
            print(value)
        
        image_url = url_for('static', filename='file/' + file1.filename)
        city="Trichy"
        url = f"{BASE_URL}q={city}&appid={API_KEY}"
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            temp_data.append(data)
            temp_data1=f"{city:-^30}"+"\n"+f"Temperature: {round( data['main']['temp'] - 273.15, 2)}°C"+"\n"+f"Humidity: {data['main']['humidity']}%"+"\n"+f"Pressure: {data['main']['pressure']} hPa"+"\n"+f"Wind Speed: {data['wind']['speed']} m/s"+"\n"+f"Longitude and Latitude: {data['coord']['lon']}, {data['coord']['lat']}"+"\n"+f"Weather: {data['weather'][0]['main']}"+"\n"+f"Weather Description: {data['weather'][0]['description']}"
        print("map_res",temp_data1)
        return render_template('prediction_result.html', msg=result, desc_msg=value, src=imgfile, temp_msg=temp_data1, view='style=display:block', view1='style=display:none')
    elif request.method == 'GET':
        return render_template('index2.html')

@app.route('/prediction_result2')
def prediction_result2():
    result = request.args.get('result')
    image_url = request.args.get('image_url')
    return render_template('prediction_result.html', result=result, image_url=image_url)

# Weather map integration

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "5b0d498b57a2899ac882b7f6b8544290"

def get_weather_data(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        coord = data['coord']
        wind = data['wind']
        temperature = main['temp'] - 273.15
        humidity = main['humidity']
        pressure = main['pressure']
        wind_speed = wind['speed']
        report = data['weather']
        lon = coord['lon']
        lat = coord['lat']
        
        return lat, lon
    else:
        return None, None

def generate_weather_map(city):
    lat, lon = get_weather_data(city)
    
    if lat is not None and lon is not None:
        map = folium.Map(location=[lat, lon], zoom_start=8)
        
        folium.CircleMarker(    
            location=[lat, lon],
            radius=30,
            popup=city,
            color="#3186cc",
            fill=True,
            fill_color="#3186cc",
        ).add_to(map)
        
        weather_map_path = f"static/weather_maps/weather_map_{city}.html"
        map.save(weather_map_path)
        return weather_map_path
    else:
        return None

@app.route('/weather_map/<city>')
def weather_map(city):
    weather_map_path = generate_weather_map(city)
    if weather_map_path:
        return render_template('map.html', weather_map_path=weather_map_path)
    else:
        return "Weather data for this city is not available."
@app.route('/map1')
def map1():
    return render_template("Trichy_map.html")
# @app.route('/map2')
# def map2():
#     return render_template("mannargudi_map.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
