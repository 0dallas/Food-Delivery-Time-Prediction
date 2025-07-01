import shutil
import os
import kagglehub
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_data():
    """
    Download the data from Kaggle and save it in the "data" folder.
    """
    path = kagglehub.dataset_download("denkuznetz/food-delivery-time-prediction")

    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    origin_path = os.path.join(path,"Food_Delivery_Times.csv")
    final_path = os.path.join(current_script_directory,"..","data")

    try:
        os.makedirs(final_path, exist_ok=True)
        shutil.copy(origin_path, final_path)
        logging.info("The Food_Delivery_Times.csv file has been successfully downloaded and saved.")
    except Exception as e:
        logging.error(f"An error occurred while copying the file: {e}")