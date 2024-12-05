from fastapi import FastAPI, UploadFile, HTTPException
import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import get_file
import os

app = FastAPI()

# URL publik dari model yang ada di Cloud Storage
MODEL_URL = "https://storage.googleapis.com/monisick-ml/trained_model2.h5"  # Ganti dengan URL Anda

# Download model dari URL publik dan simpan di lokal sementara
MODEL_PATH = get_file("trained_model2.h5", MODEL_URL)
model = load_model(MODEL_PATH, compile=False)

# Define image size (sesuaikan dengan ukuran input model Anda)
IMAGE_SIZE = (224, 224)

# Endpoint untuk prediksi
@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        # Validasi format file
        if not file.filename.endswith(("jpg", "jpeg", "png")):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an image file (jpg, jpeg, png).")

        # Simpan file sementara
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Preprocess image
        img = load_img(file_location, target_size=IMAGE_SIZE)
        img_array = img_to_array(img) / 255.0  # Normalize image
        img_array = np.expand_dims(img_array, axis=0)  # Tambahkan batch dimension

        # Predict
        predictions = model.predict(img_array)

        # Extract predicted values
        predicted_mass = round(predictions[0][0].item(), 2)
        predicted_fat = round(predictions[1][0].item(), 2)
        predicted_carb = round(predictions[2][0].item(), 2)
        predicted_protein = round(predictions[3][0].item(), 2)

        # Buat dictionary hasil prediksi
        prediction_dict = {
            "mass": predicted_mass,
            "fat": predicted_fat,
            "carbohydrates": predicted_carb,
            "protein": predicted_protein
        }

        # Simpan hasil ke file JSON
        output_file = "prediction_output.json"
        with open(output_file, "w") as json_file:
            json.dump(prediction_dict, json_file, indent=4)

        # Hapus file sementara
        os.remove(file_location)

        return {
            "message": "Prediction successful",
            "predictions": prediction_dict,
            "output_file": output_file
        }

    except Exception as e:
        # Tangani error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Endpoint untuk tes server
@app.get("/")
def read_root():   
    return {"message": "Welcome to the FastAPI Prediction Service"}
