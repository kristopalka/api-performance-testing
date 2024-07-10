def get_error_codes_counts(df):
    return {
        0: {'count': (df['error'] == 0).sum()},
        1: {'count': (df['error'] == 1).sum()},
        1211: {'count': (df['error'] == 1211).sum()},
        1050: {'count': (df['error'] == 1050).sum()},
        1220: {'count': (df['error'] == 1220).sum()}
    }