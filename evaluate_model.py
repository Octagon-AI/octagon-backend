import onnx
from onnx2pytorch import ConvertModel
import os
import torch
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def evaluate_model(id, dataset):
    # Load the ONNX model
    onnx_model_path = os.path.join('models', id, 'model.onnx')
    onnx_model = onnx.load(onnx_model_path)

    dataset_path = os.path.join('Graph', "poolData", dataset)
    data = json.load(open(dataset_path, 'r'))
    df = pd.DataFrame(data)
    # Preprocess the data
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df.set_index('date', inplace=True)

    # Feature selection
    features = df[["liquidity", "sqrtPrice", "token0Price", "token1Price", "feeGrowthGlobal0X128",
                "feeGrowthGlobal1X128", "volumeToken0", "volumeToken1", "volumeUSD", "txCount"]]
    targets = df[['feesUSD', 'high', 'low']]

    # Normalize the data
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    target_scaler = MinMaxScaler()
    targets_scaled = target_scaler.fit_transform(targets)

    # Split the data into training and testing sets
    test_size = 2  # Set test size to at least 1
    train_size = len(features_scaled) - test_size

    
    def create_sequences(features, targets, n_past, n_future):
        X = []
        y = []
        for i in range(n_past, len(features) - n_future + 1):
            X.append(features[i - n_past:i, 0:features.shape[1]])
            # The next line is changed to extract a 2D array
            y.append(targets[i + n_future - 1, 0:targets.shape[1]]) # Extract a single row 
        return np.array(X), np.array(y)


    n_past = 1  # number of past days to use for prediction
    n_future = 1  # number of days to predict

    test_features = features_scaled[train_size:]
    test_targets = targets_scaled[train_size:]
    X_test, y_test = create_sequences(test_features, test_targets, n_past, n_future)
    X_test_torch = torch.tensor(X_test, dtype=torch.float32)
    y_test_torch = torch.tensor(y_test, dtype=torch.float32)

    # Convert the ONNX model to PyTorch
    model = ConvertModel(onnx_model)



    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test_torch).numpy()

    # Inverse transform the predictions and true values
    test_predictions_inverse = target_scaler.inverse_transform(test_predictions)
    y_test_inverse = target_scaler.inverse_transform(y_test)

    # Compute MSE and MAE for each target
    mse_feesUSD = mean_squared_error(y_test_inverse[:, 0], test_predictions_inverse[:, 0])
    mae_feesUSD = mean_absolute_error(y_test_inverse[:, 0], test_predictions_inverse[:, 0])
    mse_high = mean_squared_error(y_test_inverse[:, 1], test_predictions_inverse[:, 1])
    mae_high = mean_absolute_error(y_test_inverse[:, 1], test_predictions_inverse[:, 1])
    mse_low = mean_squared_error(y_test_inverse[:, 2], test_predictions_inverse[:, 2])
    mae_low = mean_absolute_error(y_test_inverse[:, 2], test_predictions_inverse[:, 2])

    print(f'Test MSE (feesUSD): {mse_feesUSD}')
    print(f'Test MAE (feesUSD): {mae_feesUSD}')
    print(f'Test MSE (high): {mse_high}')
    print(f'Test MAE (high): {mae_high}')
    print(f'Test MSE (low): {mse_low}')
    print(f'Test MAE (low): {mae_low}')

    return {
        'mse_feesUSD': mse_feesUSD,
        'mae_feesUSD': mae_feesUSD,
        'mse_high': mse_high,
        'mae_high': mae_high,
        'mse_low': mse_low,
        'mae_low': mae_low
    }


if __name__ == '__main__':
    evaluate_model('12345', 'ETH_USDC_1.json')