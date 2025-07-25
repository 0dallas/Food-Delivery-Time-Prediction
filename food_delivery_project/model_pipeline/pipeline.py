from get_data import get_data
from data_preprocessing import load_data, preprocess_data
from model_training import train_model
from explainability import get_feature_importance
def main():
    get_data()
    df = load_data("../data/Food_Delivery_Times.csv")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    model, model_name = train_model(X_train,y_train)
    get_feature_importance(model,model_name,X_train,y_train,shap_option=False)

if __name__ == "__main__":
    main()