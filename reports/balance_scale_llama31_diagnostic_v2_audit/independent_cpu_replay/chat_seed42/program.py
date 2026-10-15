def modify_features(df_input) -> pd.DataFrame:
    """
    This function creates a new feature that calculates the difference between the sum of Left-Weight and Left-Distance and the sum of Right-Weight and Right-Distance, captures the absolute difference between Left-Weight and Right-Weight, and calculates the ratio of Left-Distance to Left-Weight and the ratio of Right-Distance to Right-Weight, then returns the modified DataFrame.
    """
    df_output = df_input.copy()
    df_output['weight_distance_difference'] = abs(df_output['Left-Weight'] + df_output['Left-Distance'] - (df_output['Right-Weight'] + df_output['Right-Distance']))
    df_output['weight_difference'] = abs(df_output['Left-Weight'] - df_output['Right-Weight'])
    df_output['left_distance_ratio'] = df_output['Left-Distance'] / df_output['Left-Weight']
    df_output['right_distance_ratio'] = df_output['Right-Distance'] / df_output['Right-Weight']
    df_output.drop(['Left-Weight', 'Left-Distance', 'Right-Weight', 'Right-Distance'], axis=1, inplace=True)
    return df_output
