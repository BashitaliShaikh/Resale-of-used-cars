from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open("vot_reg.pkl", "rb"))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    Fuel_Type_Diesel=0
    
    if request.method == 'POST':
        year = int(request.form['year'])
        engineSize=float(request.form['engineSize'])
        mpg=float(request.form['mpg'])
        mileage=int(request.form['mileage'])
        tax=int(request.form['tax'])
        fuelType_Petrol=request.form['fuelType_Petrol']
        if(fuelType_Petrol=='Petrol'):
             fuelType_Petrol=1
             fuelType_Other=0
             fuelType_Hybrid=0        
        elif(fuelType_Petrol=='Other'):
             fuelType_Petrol=0
             fuelType_Other=1
             fuelType_Hybrid=0
        else:
             fuelType_Hybrid=1
        year=2021-year
        transmission_Mannual=request.form['transmission_Mannual']
        if(transmission_Mannual=='Mannual'):
            transmission_Mannual=1
            transmission_Automatic=0
        elif (transmission_Mannual=='Automatic'):
            transmission_Mannual=0
            transmission_Automatic=1
        else:
             transmission_Mannual=0
             transmission_Automatic=0

        prediction=model.predict(np.array([[year,
                                            mileage,
                                            tax,
                                            engineSize,
                                            mpg,
                                            transmission_Mannual,
                                            transmission_Automatic,
                                            fuelType_Hybrid,
                                            fuelType_Other,
                                            fuelType_Petrol]]))
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You can sell the Car at {} lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)