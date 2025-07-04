# Delivery Time Prediction Project
This project focuses on building, evaluating, explaining, and deploying a machine learning model to accurately predict food delivery times. Leveraging historical operational data, the goal is to provide reliable delivery time estimates, improving customer satisfaction and optimizing logistics.

## Project Overview
The project encompasses a complete machine learning lifecycle, from initial data exploration to deploying a production-ready prediction API. It includes:
1. **Exploratory Data Analysis (EDA)**: In-depth analysis of delivery data to understand distributions, relationships, and identify key drivers of delivery time.

2. **Model Development & Evaluation:** Training and benchmarking various machine learning models (ElasticNet, Random Forest, LGBM, XGBoost, SVM) to identify the best-performing algorithm for delivery time prediction.

3. **Model Explainability**: Utilizing techniques like Permutation Feature Importance and SHAP values to understand why the model makes certain predictions and identify the most influential features.

4. **Error Analysis**: Investigating when and why the model might fail, particularly under specific conditions (adverse weather, high traffic).

5. **Strategic Reflections**: Addressing critical strategic questions regarding model failures, transferability to new markets, the role of GenAI tools in development, and considerations for production deployment.

6. **API Development & Deployment**: Building a lightweight FastAPI application to serve real-time predictions, packaged in a Docker container for easy deployment.

## Key Features & Deliverables
- **Data Insights**: Comprehensive understanding of factors influencing delivery times.
- **Optimized Prediction Model**: A fine-tuned Support Vector Regressor (SVM) model identified as the best performer.
- **Model Interpretability**: Clear explanations of feature importance and individual prediction contributions.
- **Failure Mode Identification**: Insights into scenarios where predictions might be less accurate.
- **Deployment-Ready API**: A Dockerized FastAPI service for real-time inference.

## Technologies Used
- Python 3.10+
- Data Handling: Pandas, NumPy
- Machine Learning: Scikit-learn, Optuna (for hyperparameter tuning), SHAP
- Visualization: Matplotlib, Seaborn
- API Development: FastAPI, Uvicorn, Pydantic
- Containerization: Docker

## Setup and Usage
### 1. Clone the Repository
```
git clone https://github.com/0dallas/Food-Delivery-Time-Prediction.git
cd Food-Delivery-Time-Prediction/food_delivery_project
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Generate Model Artifacts
Run the main pipeline script to process the data, train the models, evaluate them, and save the best model and its preprocessor artifacts (`model.pkl` and `preprocessor.pkl`) into the models/ directory
```
python model_pipeline/pipeline.py
```
### 4. Deploy the Prediction API
 You can containerize and run the API. Navigate to the `api/` directory and refer to its specific README.md for detailed instructions on setting up and running the FastAPI application, including Docker deployment.
