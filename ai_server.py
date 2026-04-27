import os
import json
import time
import joblib
import pandas as pd
import firebase_admin

from firebase_admin import credentials, db

# ==============================
# Firebase Secret from Render
# ==============================
firebase_json = json.loads(os.environ["FIREBASE_KEY"])

cred = credentials.Certificate(firebase_json)

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smartwaterdetector-default-rtdb.firebaseio.com/"
})

# ==============================
# Load AI Model
# ==============================
model = joblib.load("water_model.pkl")

print("AI Server Started Successfully")

# ==============================
# Infinite Loop
# ==============================
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

            print("Updated AI_Status:", prediction)

        else:
            print("No RiverData found")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
        time.sleep(5)
