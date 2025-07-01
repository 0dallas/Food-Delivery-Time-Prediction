from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, make_scorer
from sklearn.model_selection import cross_val_score, KFold
from sklearn.exceptions import ConvergenceWarning
import optuna
import joblib
from functools import partial
from collections import defaultdict
import os
import warnings
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

current_script_directory = os.path.dirname(os.path.abspath(__file__))

best_model_scores = defaultdict(lambda: float("inf"))
best_model_params = {}

def objective(trial,X,y):
    model_name = trial.suggest_categorical("model", ["elasticnet","random_forest", "svm","lgbm", "xgb"])

    if model_name == "elasticnet":
        alpha = trial.suggest_float("alpha", 1e-4, 10.0, log=True)
        l1_ratio = trial.suggest_float("l1_ratio", 0.0, 1.0)
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio,max_iter=5000, random_state=42)

    if model_name == "random_forest":
        n_estimators = trial.suggest_int("rf_n_estimators", 100, 1000)
        max_depth = trial.suggest_int("rf_max_depth", 3, 30)
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

    elif model_name == "svm":
        C = trial.suggest_float("svm_C", 0.1, 100.0, log=True)
        epsilon = trial.suggest_float("svm_epsilon", 0.01, 1.0, log=True)
        kernel = trial.suggest_categorical("svm_kernel", ["linear", "rbf"])
        model = SVR(C=C, epsilon=epsilon, kernel=kernel)

    elif model_name == "xgb":
        n_estimators = trial.suggest_int("xgb_n_estimators", 100, 1000)
        max_depth = trial.suggest_int("xgb_max_depth", 3, 30)
        learning_rate = trial.suggest_float("xgb_lr", 0.01, 0.3)
        model = XGBRegressor(n_estimators=n_estimators, max_depth=max_depth,
                             learning_rate=learning_rate, random_state=42,
                             objective="reg:squarederror", verbosity=0)

    elif model_name == "lgbm":
        n_estimators = trial.suggest_int("lgb_n_estimators", 100, 1000)
        max_depth = trial.suggest_int("lgb_max_depth", 3, 30)
        learning_rate = trial.suggest_float("lgb_lr", 0.01, 0.3)
        model = LGBMRegressor(n_estimators=n_estimators, max_depth=max_depth,
                              learning_rate=learning_rate, random_state=42,verbose=-1)
        
    ## Cross-validation MAE
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    mae = cross_val_score(model, X, y, cv=cv, scoring=make_scorer(mean_absolute_error)).mean()
    
    ## Save if it's better for that model
    if mae < best_model_scores[model_name]:
        best_model_scores[model_name] = mae
        best_model_params[model_name] = trial.params

    return mae

def build_best_model(name, params):
    if name == "elasticnet":
        return ElasticNet(alpha=params['alpha'], l1_ratio=params['l1_ratio'], random_state=42)
    elif name == "random_forest":
        return RandomForestRegressor(n_estimators=params['rf_n_estimators'],
                                     max_depth=params['rf_max_depth'], random_state=42)
    elif name == "svm":
        return SVR(C=params['svm_C'], epsilon=params['svm_epsilon'], kernel=params['svm_kernel'])
    elif name == "lgbm":
        return LGBMRegressor(n_estimators=params['lgb_n_estimators'],
                             max_depth=params['lgb_max_depth'],
                             learning_rate=params['lgb_lr'],
                             random_state=42)
    elif name == "xgb":
        return XGBRegressor(n_estimators=params['xgb_n_estimators'],
                            max_depth=params['xgb_max_depth'],
                            learning_rate=params['xgb_lr'],
                            random_state=42,
                            objective="reg:squarederror", verbosity=0)
    

def train_model(X_train_processed, y_train):
    """
    Uses optuna for hyperparameter tuning
    """
    objective_with_data = partial(objective, X=X_train_processed, y=y_train)

    logging.info("Hyperparameterization with OPTUNA")
    study = optuna.create_study(direction="minimize")
    study.optimize(objective_with_data, n_trials=50)
    logging.info("Training completed")

    print("Best MAE by model")
    for model_name, mae in best_model_scores.items():
        print(f"  {model_name}: {mae:.4f}")

    print("Details best model")
    best_model_name = study.best_params['model']
    print(f"  Model: {best_model_name}")
    print(f"  MAE: {study.best_value:.4f}")
    print(f"  Hyperparameters: {study.best_params}")

    final_model = build_best_model(best_model_name, study.best_params)
    final_model.fit(X_train_processed, y_train)

    joblib.dump(final_model, os.path.join(current_script_directory,"..","models","model.pkl"))
    logging.info("Model saved successfully")

    return final_model