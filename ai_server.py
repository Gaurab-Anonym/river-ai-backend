import os
import json
import time
import joblib
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# Firebase Secret
firebase_json = json.loads(os.environ["FIREBASE_KEY"])

cred = credentials.Certificate(firebase_json)

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smartwaterdetector-default-rtdb.firebaseio.com/"
})

# Load Model
model = joblib.load("water_model.pkl")

print("AI Server Started")

while True:
    try:
        ref = db.reference("RiverData")
        data = ref.get()

        if data:
            ph = float(data.get("pH", 7))
            tds = float(data.get("TDS", 0))
            turb = float(data.get("Turbidity", 0))

            X = pd.DataFrame(
                [[ph, tds, turb]],
                columns=["pH", "TDS", "Turbidity"]
            )

            prediction = model.predict(X)[0]

            ref.update({
                "AI_Status": prediction
            })

            print("Updated:", prediction)

        else:
            print("No data found")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
