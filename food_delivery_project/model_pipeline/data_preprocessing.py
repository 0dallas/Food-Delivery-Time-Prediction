import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
current_script_directory = os.path.dirname(os.path.abspath(__file__))

def load_data(filepath:str)-> pd.DataFrame:
    """
    Loads the dataset from a CSV file
    """
    try:
        df = pd.read_csv(filepath)
        logging.info("Data loaded successfully")
        return df
    except Exception as e:
        logging.error(f"An error occurred while loading data: {e}")



def preprocess_data(df:pd.DataFrame, random_state:int = 42):
    """
    Performs data preprocessing:
    - Handling missing values.
    - Coding categorical variables.
    - Scaling numerical variables.
    - Dividing into training and test sets.
    """

    ## Identify numeric and categorical columns
    numerical_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
    categorical_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']

    ## Create transformers for preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer',SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer',SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    ## Create a preprocessor that applies the transformations
    preprocessor = ColumnTransformer(
        transformers=[
            ('num',numeric_transformer,numerical_features),
            ('cat',categorical_transformer,categorical_features)
        ],
     
    )

    X = df.drop(columns=['Delivery_Time_min'])
    y = df['Delivery_Time_min']

    ## Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    ## Fit the preprocessor
    preprocessor.fit(X_train)
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    logging.info("Data successfully preprocessed")

    ## Save the preprocessor
    joblib.dump(preprocessor, os.path.join(current_script_directory,"..","models","preprocessor.pkl"))
    logging.info("Preprocessor saved successfully")

    num_features = preprocessor.transformers_[0][2]
    ohe = preprocessor.transformers_[1][1]
    cat_features = preprocessor.transformers_[1][2]
    ohe_feature_names = ohe.get_feature_names_out(cat_features)
    all_feature_names = list(num_features) + list(ohe_feature_names)

    ## Convert the processed data with the new columns
    X_train_processed_df = pd.DataFrame(X_train_processed,columns=all_feature_names)
    X_test_processed_df = pd.DataFrame(X_test_processed,columns=all_feature_names)

    return X_train_processed_df, X_test_processed_df, y_train, y_test

if __name__ == "__main__":
    df = load_data(os.path.join(current_script_directory,"..","data","Food_Delivery_Times.csv"))
    print(df.head(2))

    X_train, X_test, _ , _ = preprocess_data(df)
    print(X_train.head(2))