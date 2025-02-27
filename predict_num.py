import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

def prepare_data(sequence, n_steps=3):
    X, y = [], []
    for i in range(len(sequence) - n_steps):
        X.append(sequence[i:i + n_steps])
        y.append(sequence[i + n_steps])
    return np.array(X), np.array(y)

sequence = np.array([10,11,12,13,14,15])
n_steps = 3
X, y = prepare_data(sequence, n_steps)
X = X.reshape((X.shape[0], X.shape[1], 1))

model = Sequential([
    Input(shape=(n_steps, 1)), 
    LSTM(50, activation='relu', return_sequences=True),
    LSTM(50, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=200, verbose=0)

def predict_next_numbers(model, sequence, n_steps=3, n_preds=5):
    inputs = list(sequence[-n_steps:])  
    preds = []

    for _ in range(n_preds):
        x_input = np.array(inputs).reshape((1, n_steps, 1))  
        next_number = model.predict(x_input, verbose=0)[0][0]
        preds.append(round(next_number)) 
        inputs.append(next_number)  
        inputs.pop(0)  

    return preds

predicted_numbers = predict_next_numbers(model, sequence)
print("Следующие 5 чисел:", predicted_numbers)
