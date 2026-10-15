def modify_features(df_input) -> pd.DataFrame:
    """
    Thought 1: The absolute difference between Left-Weight and Right-Weight can capture the imbalance in weight distribution.
    Thought 2: The absolute difference between Left-Distance and Right-Distance can capture the distance imbalance.
    Thought 3: The ratio of Left-Weight to Right-Weight can provide an additional perspective on weight imbalance.
    Thought 4: The ratio of Left-Distance to Right-Distance can provide an additional perspective on distance imbalance.
    Thought 5: The difference between the maximum weight-bearing capacity of the left and right sides can provide information about the potential tipping point.
    Thought 6: The difference between the maximum distance traveled by the left and right sides can provide information about the potential tipping point.
    New Features:
        - weight_difference: absolute difference between Left-Weight and Right-Weight
        - distance_difference: absolute difference between Left-Distance and Right-Distance
        - weight_ratio: ratio of Left-Weight to Right-Weight
        - distance_ratio: ratio of Left-Distance to Right-Distance
        - weight_capacity_difference: difference between the maximum weight-bearing capacity of the left and right sides
        - distance_traveled_difference: difference between the maximum distance traveled by the left and right sides
    """
    df_output = df_input.copy()
    df_output['weight_difference'] = abs(df_output['Left-Weight'] - df_output['Right-Weight'])
    df_output['distance_difference'] = abs(df_output['Left-Distance'] - df_output['Right-Distance'])
    df_output['weight_ratio'] = df_output['Left-Weight'] / df_output['Right-Weight']
    df_output['distance_ratio'] = df_output['Left-Distance'] / df_output['Right-Distance']
    df_output['weight_capacity_difference'] = df_output['Left-Weight'] + df_output['Left-Distance'] - df_output['Right-Weight'] - df_output['Right-Distance']
    df_output['distance_traveled_difference'] = df_output['Left-Weight'] + df_output['Left-Distance'] - df_output['Right-Weight'] - df_output['Right-Distance']
    df_output['Left-Weight'] = df_input['Left-Weight']
    df_output['Left-Distance'] = df_input['Left-Distance']
    df_output['Right-Weight'] = df_input['Right-Weight']
    df_output['Right-Distance'] = df_input['Right-Distance']
    df_output = df_output[['weight_difference', 'distance_difference', 'weight_ratio', 'distance_ratio', 'Left-Weight', 'Left-Distance', 'Right-Weight', 'Right-Distance', 'weight_capacity_difference', 'distance_traveled_difference']]
    return df_output
