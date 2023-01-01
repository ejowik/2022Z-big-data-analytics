# Concept
## Core functionalities:
1. (pre-)training the model on historical data
2. forecasting the load of websites for weather forecasts for the project's business purposes
3. forecasting load pages for current weather conditions to continuously monitor model quality
4. re-estimation of the model on historical data augmented with new observations
## Side functionalities:
1. preliminary processing of historical data, including combining data from miscellaneous sources (weather API and Google Trends)
2. updating the training set with batches of observations not included in the training set created to estimate the latest model at a given moment
## Additional remarks:
- All notebooks are parameterized so that on demand, they can estimate the model for a given time (day/night model), location and website.
- All notebooks are equipped with a versioning mechanism (based on the modification date of files in the system) to operate automatically (without specifying paths) on the latest file versions.
# Implementation:
1. `step2_pretrain_model.ipynb`
    - dependencies: `step1_preprocess_historical_data.ipynb`
2. `step3_1_predict_for_forecast.ipynb`
    - dependencies: `stream_weather_forecast.ipynb`
    - remark: the volume of forecast data implies significant latency (as a consequence of prolonged data pre-processing). Therefore, predictions are not generated strictly in real-time but near real-time, i.e., in batch, when no new messages flow from the stream. There are no business contraindications for predictions for long-term weather forecasts to be generated with a slight delay
3. `step3_2_predict_for_observations.ipynb`
    - dependencies: `stream_weather_observations.ipynb`
    - remark: predictions are not generated strictly in real-time
4. `step5_refresh_model.ipynb`
    - dependencies: `step4_preprocess_data_for_reestimation.ipynb`


