import pickle
import numpy as np
import logging
import os

logger = logging.getLogger(str('preds'))

data = {"transaction_time_since_first_april_2022_00am_in_seconds" : 27,
        "transaction_amount" : 11.11,
        "beneficiary" : "Mike",
        "type": "credit_card",
        "country" : "France"}

def get_encodings(data):
    return_dict = {}
    for item in data:
        if item in ["beneficiary", "type", "country"]:
            loaded_encoder = pickle.load(open(item + ".pkl", 'rb'))
            value = loaded_encoder.transform([data[item]])[0]
            return_dict[item] = value
        else:
            if item not in ["transaction_time_since_first_april_2022_00am_in_seconds"]:
                return_dict[item] = data[item]
    encoded = np.array([return_dict["beneficiary"], return_dict["type"], return_dict["country"], return_dict["transaction_amount"]])
    return encoded

# # Predict customer
# encoded_data = get_encodings(data)

# # Load the model from disk
# loaded_model = pickle.load(open("model.sav", 'rb'))

# # Run the prediction
# result = loaded_model.predict(encoded_data.reshape(1, -1))[0]
# print(result)


def get_transaction_prediction(transaction):
    print(os.listdir('.'))
    encoded_data = get_encodings(transaction)
    loaded_model = pickle.load(open("model.sav", 'rb'))
    prediction = loaded_model.predict(encoded_data.reshape(1, -1))[0]
    return {'prediction':str(prediction)}






