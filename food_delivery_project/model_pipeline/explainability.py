import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("shap").disabled = True

current_script_directory = os.path.dirname(os.path.abspath(__file__))

from sklearn.inspection import permutation_importance

def get_feature_importance(model, model_name, X_train, y_train, top_n=10, shap_option=False):
    """
    Calculates the importance of features according to the model type.
    """
    importances = None
    feature_names = X_train.columns

    if model_name == "elasticnet":
        importances = np.abs(model.coef_)
        method = "coef_"

    elif model_name == "random_forest":
        importances = model.feature_importances_
        method = "feature_importances_"

    elif model_name in ["lgbm", "xgb"]:
        importances = model.feature_importances_
        method = "feature_importances_"

    elif model_name == "svm":
        result = permutation_importance(model, X_train, y_train, n_repeats=10, random_state=42, n_jobs=-1)
        importances = result.importances_mean
        method = "permutation"

    else:
        logging.error("Unsupported model")

    report_path = os.path.join(current_script_directory,"..","reports","explainability","feature_importance.csv")
    df_importances = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values(by="importance", ascending=False)
    df_importances.to_csv(report_path,index=False)
    logging.info("Feature importance report saved successfully")

    ## Plot
    plot_path = os.path.join(current_script_directory,"..","reports","plots","Explainability","feature_importance.png")
    top_df = df_importances.head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_df, x="importance", y="feature", hue="feature", palette="viridis")
    plt.title(f"{model_name.upper()} - Feature Importances ({method})")
    plt.tight_layout()
    plt.savefig(plot_path,bbox_inches='tight')
    logging.info("Feature importance plot saved successfully")

    """
    SHAP analysis
    """
    if shap_option:
        plot_path = os.path.join(current_script_directory,"..","reports","plots","Explainability","shap.png")
        if model_name in ["random_forest", "xgb", "lgbm"]:
            explainer = shap.Explainer(model, X_train)  
        elif model_name in ["elasticnet", "svm"]:
            explainer = shap.KernelExplainer(model.predict, shap.sample(X_train, 100))
        else:
            logging.error("Model not supported for SHAP.")
        
        shap_values = explainer(X_train)

        shap.summary_plot(shap_values, X_train, show=False)
        plt.savefig(plot_path, bbox_inches='tight')
        logging.info("SHAP plot saved successfully")
    else:
        logging.info("SHAP analysis has not been considered")