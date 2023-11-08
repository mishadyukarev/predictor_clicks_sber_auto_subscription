from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
import names as n
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import pipelines


for_filling_null_cols_l = ['visit_date', 'visit_time', 'utm_source',
                           'utm_medium', 'utm_campaign', 'utm_adcontent',
                           'utm_keyword', 'device_category', 'device_os',
                           'device_brand', 'device_model', 'device_screen_resolution',
                           'device_browser', 'geo_country', 'geo_city']

targets_l = ['sub_car_claim_click', 'sub_car_claim_submit_click',
                 'sub_open_dialog_click', 'sub_custom_question_submit_click',
                 'sub_call_number_click', 'sub_callback_submit_click', 'sub_submit_success',
                 'sub_car_request_submit_click']

needed_cols = ['visit_date', 'visit_time', 'visit_number',
             'utm_source', 'utm_medium', 'utm_campaign',
             'utm_adcontent', 'utm_keyword', 'device_category',
             'device_os', 'device_brand', 'device_model',
             'device_screen_resolution', 'device_browser',
             'geo_country', 'geo_city', 'is_target']



columns_for_dt = [n.Columns.VISIT_TIME, n.Columns.VISIT_DATE]

cols_for_ohe = [n.c.DEVICE_CATEGORY,
                n.c.DEVICE_OS,
                n.c.DEVICE_BROWSER,
                n.c.GEO_COUNTRY,

                n.c.VISIT_DATE_YEAR,
                n.c.VISIT_DATE_MONTH,
                n.c.VISIT_DATE_WEEKDAY,

                n.c.UTM_SOURCE_CUSTOMISED,
                n.c.UTM_MEDIUM_CUSTOMISED,
                n.c.UTM_CAMPAIGN_CUSTOMISED,
                n.c.UTM_ADCONTENT_CUSTOMISED,
                n.c.UTM_KEYWORD_CUSTOMISED,

                n.c.DEVICE_BRAND_CUSTOMISED,
                n.c.GEO_CITY_CUSTOMISED
                ]

cols_for_std = [n.c.VISIT_NUMBER, n.c.DEVICE_SCREEN_RESOLUTION_MULT, n.c.VISIT_TIME_HOURS, ]  #

not_needed_cols_for_deleting = [n.c.DEVICE_MODEL]

create_column_from_visit_time = pipelines.ColumnsFromDateTimeCreator(dt_column=columns_for_dt[0],
                                                                     which_columns_need='hour',
                                                                     names_new_columns=n.c.VISIT_TIME_HOURS,
                                                                     need_to_drop_dt_column=True)

create_columns_from_visit_date = pipelines.ColumnsFromDateTimeCreator(columns_for_dt[1],
                                                                      ('year', 'month', 'weekday'),
                                                                      (n.c.VISIT_DATE_YEAR, n.c.VISIT_DATE_MONTH,
                                                                       n.c.VISIT_DATE_WEEKDAY),
                                                                      True)


start_pl = Pipeline([
    ('create_target_column', pipelines.CreateTargetColumn(targets_l)),
    ('input_median', pipelines.CustomInputer(SimpleImputer(strategy='median'), [n.c.VISIT_NUMBER])),
    ('input_null',
     pipelines.CustomInputer(SimpleImputer(strategy='constant', fill_value='null'), for_filling_null_cols_l)),
    ('leave_needed_columns', pipelines.LeaverColumns(needed_cols))

])


main_pl = Pipeline([
    ('converter_date', pipelines.ConverterIntoDateTime(columns_for_dt)),
    ('create_columns_from_visit_time', create_column_from_visit_time),
    ('create_columns_from_visit_date', create_columns_from_visit_date),
    ('split', pipelines.SpliterStrings('x', n.c.DEVICE_SCREEN_RESOLUTION, n.c.DEVICE_SCREEN_RESOLUTION_MULT, True)),
    ('create_is_from_russia_column',
     pipelines.CreateBoolColumnsFromCategorical(n.c.GEO_COUNTRY, n.c.IS_FROM_RUSSIA_INT, 'Russia')),
    ('1', pipelines.DecreaseCategoricalVariables(n.c.UTM_SOURCE, n.c.UTM_SOURCE_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('2', pipelines.DecreaseCategoricalVariables(n.c.UTM_MEDIUM, n.c.UTM_MEDIUM_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('3', pipelines.DecreaseCategoricalVariables(n.c.UTM_CAMPAIGN, n.c.UTM_CAMPAIGN_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('4', pipelines.DecreaseCategoricalVariables(n.c.UTM_ADCONTENT, n.c.UTM_ADCONTENT_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('5', pipelines.DecreaseCategoricalVariables(n.c.UTM_KEYWORD, n.c.UTM_KEYWORD_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('6', pipelines.DecreaseCategoricalVariables(n.c.DEVICE_BRAND, n.c.DEVICE_BRAND_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),
    ('7', pipelines.DecreaseCategoricalVariables(n.c.GEO_CITY, n.c.GEO_CITY_CUSTOMISED, ratio=0.001,
                                                 need_to_remove_from_column=True)),

    ('ohe', pipelines.CustomOheTransformer(cols_for_ohe, True)),
    ('std', pipelines.CustomStdTransformer(cols_for_std, True)),
    ('drop_not_needed_columns_for_prediction', pipelines.ColumnDropperTransformer(not_needed_cols_for_deleting)),
])


cleaning_outliers_pl = Pipeline([
        ('clean_outliers_with_isolation_forest', pipelines.CleanOutliersWithIsolationForest()),
    ])

# We can choose
#chooser = RandomForestClassifier(n_estimators=10, random_state=42)
#chooser = DecisionTreeClassifier(random_state=42)
chooser = LogisticRegression()
choose_best_features_pl = Pipeline([('chooser_best_features', pipelines.ChooserBestFeatures(chooser, 250))])

best_model_pl = Pipeline([('model', RandomForestClassifier(max_depth=15, random_state=42))])


result_pl = make_pipeline(main_pl, choose_best_features_pl,  best_model_pl)