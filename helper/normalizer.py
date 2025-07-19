# def normalize(df, features):
#     normalized_df = df
#     normalized_df[features] = (df[features] - df[features].min()) / (df[features].max() - df[features].min())
#
#     return normalized_df

def normalize(df, features):
    normalized_df = df.copy()
    for feature in features:
        min_val = df[feature].min()
        max_val = df[feature].max()
        if max_val == min_val:
            normalized_df[feature] = min_val
        else:
            normalized_df[feature] = (df[feature] - min_val) / (max_val - min_val)
    return normalized_df