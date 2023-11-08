import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import IsolationForest
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

import names as n


class CreateTargetColumn(BaseEstimator, TransformerMixin):
    def __init__(self, targets):
        self.targets = targets

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[n.c.IS_TARGET] = 0
        X.loc[X.event_action.isin(self.targets), n.c.IS_TARGET] = 1
        X.drop(columns='event_action', inplace=True)

        X = X.sort_values(by=["is_target"], ascending=False)

        X = X.drop_duplicates(subset=["session_id"], keep="first")

        return X


class ColumnDropperTransformer:
    def __init__(self, columns): self.columns = columns
    def fit(self, X, y=None): return self
    def transform(self, X):
        return X.drop(self.columns, axis=1)


class CustomOheTransformer:
    def __init__(self, columns, need_drop_from_columns: bool):
        self.columns = columns
        self.need_drop_from_columns = need_drop_from_columns
        self.ohe = OneHotEncoder(sparse_output=False, )
        self.feature_names = None

    def fit(self, X, y=None):
        self.ohe.fit(X[self.columns])
        self.feature_names = self.ohe.get_feature_names_out()
        return self

    def transform(self, X):
        data = self.ohe.transform(X[self.columns])

        ohe_df = pd.DataFrame(columns=self.feature_names, data=data)
        ohe_df.index = X.index

        if self.need_drop_from_columns:
            X.drop(columns=self.columns, axis=1, inplace=True)

        return pd.concat([X, ohe_df], axis=1)


class CustomStdTransformer:
    def __init__(self, columns, need_drop_from_columns: bool):
        self.columns = columns
        self.need_drop_from_columns = need_drop_from_columns
        self.std = StandardScaler()

    def fit(self, X, y=None):
        self.std.fit(X[self.columns])
        return self

    def transform(self, X):
        out_columns = self.std.get_feature_names_out()
        data = self.std.transform(X[self.columns])

        std_df = pd.DataFrame(columns=out_columns, data=data)
        std_df.index = X.index

        if self.need_drop_from_columns:
            X.drop(columns=self.columns, axis=1, inplace=True)

        return pd.concat([X, std_df], axis=1)


class CleanOutliersWithIsolationForest(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.isolation_forest = IsolationForest(max_samples=100, random_state=42, contamination=.025)

    def fit(self, X, y):
        self.isolation_forest.fit(X)
        return self

    def transform(self, X):
        predict_outlier_vec = self.isolation_forest.predict(X)

        mask = predict_outlier_vec == 1

        X = X[mask]

        return X


class ChooserBestFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, chooser, max_features):
        self.chooser = chooser
        self.max_features = max_features
        self.best_features_l = None

    def fit(self, X, y=None):
        self.chooser.fit(X, y)
        selector = SelectFromModel(estimator=self.chooser, prefit=True, max_features=self.max_features)

        self.best_features_l = X.columns[selector.get_support()].tolist()
        return self

    def transform(self, X):
        return X[self.best_features_l]


class ConverterIntoDateTime(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.columns] = X[self.columns].apply(pd.to_datetime)
        return X


class ColumnsFromDateTimeCreator(BaseEstimator, TransformerMixin):
    def __init__(self, dt_column, which_columns_need, names_new_columns, need_to_drop_dt_column):
        self.dt_column = dt_column
        self.which_columns_need = which_columns_need
        self.names_new_columns = names_new_columns
        self.need_to_drop_dt_column = need_to_drop_dt_column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        dt = X[self.dt_column].dt

        if type(self.which_columns_need) == str:
            new_column = self.names_new_columns

            if 'year' in self.which_columns_need:
                X[new_column] = dt.year

            if 'month' in self.which_columns_need:
                X[new_column] = dt.month

            if 'weekday' in self.which_columns_need:
                X[new_column] = dt.weekday

            if 'hour' in self.which_columns_need:
                X[new_column] = dt.hour

            if 'minute' in self.which_columns_need:
                X[new_column] = dt.minute

            if 'second' in self.which_columns_need:
                X[new_column] = dt.second

        else:
            i = 0

            if 'year' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.year
                i += 1

            if 'month' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.month
                i += 1

            if 'weekday' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.weekday
                i += 1

            if 'hour' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.hour
                i += 1

            if 'minute' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.minute
                i += 1

            if 'second' in self.which_columns_need:
                X[self.names_new_columns[i]] = dt.second
                i += 1

        if self.need_to_drop_dt_column:
            X.drop(columns=[self.dt_column], axis=1, inplace=True)

        return X


class AddHourColumn(BaseEstimator, TransformerMixin):
    def __init__(self, names_new_columns):
        self.names_new_columns = names_new_columns
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        print(X)
        print(type(X))

        for column in X.columns:
            dt = X[column].dt

            X[self.names_new_columns[0]] = dt.hour

            X.drop(columns=column, axis=1, inplace=True)

        return X


class SpliterStrings(BaseEstimator, TransformerMixin):
    def __init__(self, spliter,  column_from, column_to, need_drop_column_from):
        self.spliter = spliter
        self.column_from = column_from
        self.column_to = column_to
        self.need_drop_column_from = need_drop_column_from

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        def split(x):
            split_x = x.split(self.spliter)
            return int(split_x[0]) * int(split_x[1])

        X[self.column_to] = X[self.column_from].apply(lambda x: split(x))

        if self.need_drop_column_from:
            X.drop(columns=self.column_from, axis=1, inplace=True)

        return X


class CreateBoolColumnsFromCategorical(BaseEstimator, TransformerMixin):
    def __init__(self, column_from, column_to, name_categorical_for_1):
        self.column_from = column_from
        self.column_to = column_to
        self.name_categorical_for_1 = name_categorical_for_1

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.column_to] = X[self.column_from].apply(lambda x: 1 if x == self.name_categorical_for_1 else 0)

        return X


class DecreaseCategoricalVariables(BaseEstimator, TransformerMixin):
    def __init__(self, column_from, column_to, ratio, need_to_remove_from_column):
        self.column_from = column_from
        self.column_to = column_to
        self.ratio = ratio
        self.need_to_remove_from_column = need_to_remove_from_column
        self.needed_cols = None

    def fit(self, X, y=None):
        val_counts = (X[self.column_from].value_counts() / len(X))
        self.needed_cols = val_counts[val_counts > self.ratio]
        return self

    def transform(self, X):

        X[self.column_to] = X[self.column_from].apply(lambda x: 'else' if x not in self.needed_cols else x)

        if self.need_to_remove_from_column:
            X.drop(columns=self.column_from, axis=1, inplace=True)

        return X


class CustomInputer(BaseEstimator, TransformerMixin):
    def __init__(self, inputer, columns):
        self.inputer = inputer
        self.columns = columns

    def fit(self, X, y=None):
        self.inputer.fit(X[self.columns])
        return self

    def transform(self, X):
        X[self.columns] = self.inputer.transform(X[self.columns])
        return X


class LeaverColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.loc[:,self.columns]



