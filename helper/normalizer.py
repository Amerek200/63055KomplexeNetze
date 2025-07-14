def normalize(df, features):
    normalized_df = df
    normalized_df[features] = (df[features] - df[features].min()) / (df[features].max() - df[features].min())

    return normalized_df