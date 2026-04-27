import firebase_admin
from firebase_admin import credentials, db
import joblib
import pandas as pd
import time

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smartwaterdetector-default-rtdb.firebaseio.com/"
})

model = joblib.load("water_model.pkl")

while True:
    try:
        ref = db.reference("RiverData")
        data = ref.get()

        if data:
            ph = float(data.get("pH", 7))
            tds = float(data.get("TDS", 0))
            turb = float(data.get("Turbidity", 0))

            X = pd.DataFrame([[ph,tds,turb]],
                             columns=["pH","TDS","Turbidity"])

            prediction = model.predict(X)[0]

            ref.update({"AI_Status": prediction})

            print(prediction)

        time.sleep(5)

    except Exception as e:
        print(e)
        time.sleep(5)