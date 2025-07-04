# Delivery Time Prediction API
This project provides a concise FastAPI REST API for predicting food delivery times using a pre-trained machine learning model.

## Project Structure
```
api/
├── app/
│   ├── api.py           # Main FastAPI application, handles model loading, prediction, and configuration.
│   └── schemas.py       # Pydantic models for API request/response validation.
├── models/
│   ├── preprocessor.pkl # Serialized data preprocessor
│   └── model.pkl        # Serialized trained machine learning model
├── requirements.txt     # Python dependencies.
├── Dockerfile           # Docker image definition for deployment.
└── README.md            # Project documentation.
```

## Run the API with Docker (Recommended for Production Environment)

```
# 1. Build the Docker image
docker build -t delivery-prediction-api .

# 2. Run the Docker container
docker run -p 8000:8000 delivery-prediction-api
```

## API Endpoints
- `GET /health`:
    - **Description**: Health check endpoint to verify the API is running and the model is successfully loaded.
    - **Response**: `{"status": "ok", "message": "API is running and model is loaded."}`

- `POST /predict_delivery_time`:
    - **Description**: Predicts the delivery time based on provided features.
    - **Request Body (JSON)**:
        - Important: Categorical features (`Weather`, `Traffic_Level`, `Time_of_Day`, `Vehicle_Type`) are expected as integers. These integers correspond to the numerical encoding used during your model training weather.

    ```json
        {
            "Distance_km": 15.2,
            "Weather": 0,             // 0 : 'Clear', 1 : 'Rainy', 2 : 'Snowy'
            "Traffic_Level": 1,       // 0 : 'Low', 1 : 'Medium', 2 : 'High'
            "Time_of_Day": 1,         // 0 : 'Morning', 1 : 'Afternoon', etc.
            "Vehicle_Type": 0,        // 0 : 'Bike', 1 : 'Car'
            "Preparation_Time_min": 25,
            "Courier_Experience_yrs": 3.5
        }
    ```
    - **Response (JSON)**:
    ```json
        {
            "predicted_delivery_time_min": 45.75
        }
    ```

## Live Demo (Deployed Endpoint)
You can test the deployed API directly at the following URL:
- **Base URL**: https://food-delivery-time-prediction-rptz.onrender.com/predict_delivery_time

Access the interactive API documentation (Swagger UI) for this deployed endpoint at:
- **Swagger UI**: https://food-delivery-time-prediction-rptz.onrender.com/docs