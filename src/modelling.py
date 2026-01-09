
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from pathlib import Path
import joblib
from src.logging_configuration import logger


def ML_model_training(Xtrain, ytrain, Xtest, ytest, output_dir=None):
    if output_dir is None:
        logger.error("directory to save the models has not been provided")
        raise TypeError("Please provide a valid directory to save models")
    else:
        Path(output_dir).mkdir(exist_ok=True)
        model = RandomForestRegressor(random_state=42)
        model.fit(Xtrain, ytrain)
        logger.info("Fitted model successfully")
        predictions = model.predict(Xtest)
        joblib.dump(model, f"{output_dir}/random_forest_model.pkl")
        return ytest, predictions
    