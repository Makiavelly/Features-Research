def modify_features(df_input):
    result = df_input.copy()
    result['torque_diff'] = df_input['Left-Weight'] * df_input['Left-Distance'] - df_input['Right-Weight'] * df_input['Right-Distance']
    return result
