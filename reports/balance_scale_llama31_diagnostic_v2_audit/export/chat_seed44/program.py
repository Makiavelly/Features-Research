def modify_features(df_input) -> pd.DataFrame:
    """
    Modified version of `modify_features_v0` with additional derived features to enhance the model's ability to solve the task.
    New Features:
    1. weight_difference | weight_difference = abs(Left-Weight - Right-Weight)
    2. weight_ratio | weight_ratio = (Left-Weight + Right-Weight) / 2
    3. distance_difference | distance_difference = abs(Left-Distance - Right-Distance)
    4. distance_ratio | distance_ratio = (Left-Distance + Right-Distance) / 2
    5. weight_distance_product | weight_distance_product = Left-Weight * Left-Distance + Right-Weight * Right-Distance
    """
    df_output = df_input.copy()
    df_output['weight_difference'] = abs(df_output['Left-Weight'] - df_output['Right-Weight'])
    df_output['weight_ratio'] = (df_output['Left-Weight'] + df_output['Right-Weight']) / 2
    df_output['distance_difference'] = abs(df_output['Left-Distance'] - df_output['Right-Distance'])
    df_output['distance_ratio'] = (df_output['Left-Distance'] + df_output['Right-Distance']) / 2
    df_output['weight_distance_product_left'] = df_output['Left-Weight'] * df_output['Left-Distance']
    df_output['weight_distance_product_right'] = df_output['Right-Weight'] * df_output['Right-Distance']
    df_output['weight_distance_product'] = df_output['weight_distance_product_left'] + df_output['weight_distance_product_right']
    df_output.drop(['Left-Weight', 'Right-Weight', 'Left-Distance', 'Right-Distance'], axis=1, inplace=True)
    return df_output
