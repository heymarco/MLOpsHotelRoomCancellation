import joblib
import numpy as np
import pandas as pd

from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request


app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_dict = {key: int(value) if key != "avg_price_per_room" else float(value)
                     for key, value in request.form.items()}
        df = pd.DataFrame([post_dict], columns=loaded_model.feature_names_in_)
        prediction = loaded_model.predict(df)
        return render_template("index.html", prediction=prediction[0])
    return render_template("index.html", prediction=None)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


