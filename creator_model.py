import pandas as pd
import names as n
import pipeline_manager
import joblib

folder_name = 'data'

ga_hits_filename = folder_name + '/ga_hits.csv'
ga_sessions_filename = folder_name + '/ga_sessions.csv'


def main():
    ga_hits_df = pd.read_csv(ga_hits_filename, low_memory=False)
    ga_sessions_df = pd.read_csv(ga_sessions_filename, low_memory=False)

    df = pd.merge(ga_sessions_df, ga_hits_df, how="inner", on='session_id')

    #
    df = pipeline_manager.start_pl.fit_transform(df)

    #
    X = df.drop(columns=n.c.IS_TARGET)
    y = df[n.c.IS_TARGET]

    X_result = pipeline_manager.main_pl.fit_transform(X, y)

    X_result = pipeline_manager.cleaning_outliers_pl.fit_transform(X_result, y)
    y_result = y[X_result.index]

    X_result = pipeline_manager.choose_best_features_pl.fit_transform(X_result, y_result)

    pipeline_manager.best_model_pl.fit(X_result, y_result)

    # Saving
    df.sample(20).to_json(folder_name+'/random_customers.json', orient='records')
    joblib.dump(pipeline_manager.result_pl, folder_name+'/main_pipeline')


if __name__ == '__main__':
    main()
