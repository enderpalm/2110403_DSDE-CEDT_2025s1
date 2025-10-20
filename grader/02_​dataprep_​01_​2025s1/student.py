import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

"""
    ASSIGNMENT 2 (STUDENT VERSION):
    Using pandas to explore Titanic data from Kaggle (titanic_to_student.csv) and answer the questions.
    (Note that the following functions already take the Titanic dataset as a DataFrame, so you don’t need to use read_csv.)

"""


def Q1(df):
    """
        Problem 1:
            How many rows are there in the "titanic_to_student.csv"?
    """
    # TODO: Code here
    return df.shape[0]


def Q2(df):
    '''
        Problem 2:
            2.1 Drop variables with missing > 50%
            2.2 Check all columns except 'Age' and 'Fare' for flat values, drop the columns where flat value > 70%
            From 2.1 and 2.2, how many columns do we have left?
            Note: 
            -Ensure missing values are considered in your calculation. If you use normalize in .value_counts(), please include dropna=False.
    '''
    # TODO: Code here
    missing_threshold = 0.5 * df.shape[0]
    non_flat_column = ["Age", "Fare"]
    cols_to_drop = df.columns[df.isna().sum() > missing_threshold]

    for i in df.columns:
        if i in non_flat_column or i in cols_to_drop:
            continue
        most_freq = df[i].value_counts(normalize=True, dropna=False).iloc[0]
        if most_freq > 0.7:
            cols_to_drop = cols_to_drop.union(pd.Index([i]))

    df.drop(cols_to_drop.to_list(), axis=1, inplace=True)
    return df.shape[1]


def Q3(df):
    '''
       Problem 3:
            Remove all rows with missing targets (the variable "Survived")
            How many rows do we have left?
    '''
    # TODO: Code here
    df.dropna(subset=["Survived"], inplace=True)
    return df.shape[0]


def Q4(df):
    '''
       Problem 4:
            Handle outliers
            For the variable “Fare”, replace outlier values with the boundary values
            If value < (Q1 - 1.5IQR), replace with (Q1 - 1.5IQR)
            If value > (Q3 + 1.5IQR), replace with (Q3 + 1.5IQR)
            What is the mean of “Fare” after replacing the outliers (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    q1 = df["Fare"].quantile(0.25)
    q3 = df["Fare"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df["Fare"] = df["Fare"].apply(
        lambda x: (
            lower_bound if x < lower_bound else (upper_bound if x > upper_bound else x)
        )
    )
    return round(df["Fare"].mean(), 2)


def Q5(df):
    '''
       Problem 5:
            Impute missing value
            For number type column, impute missing values with mean
            What is the average (mean) of “Age” after imputing the missing values (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
    df["Age"] = pd.DataFrame(imputer.fit_transform(df[["Age"]]))

    return round(df['Age'].mean(), 2)


def Q6(df):
    '''
        Problem 6:
            Convert categorical to numeric values
            For the variable “Embarked”, perform the dummy coding.
            What is the average (mean) of “Embarked_Q” after performing dummy coding (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    enc = OneHotEncoder(handle_unknown="error", drop="first")
    encoded_embarked = enc.fit_transform(df[["Embarked"]]).toarray()
    encoded_column = pd.DataFrame(
        columns=enc.get_feature_names_out(["Embarked"]), data=encoded_embarked
    )
    df = pd.concat(
        [df.reset_index(drop=True), encoded_column.reset_index(drop=True)], axis=1
    )
    return round(df["Embarked_Q"].mean(), 2)


def Q7(df):
    '''
        Problem 7:
            Split train/test split with stratification using 70%:30% and random seed with 123
            Show a proportion between survived (1) and died (0) in all data sets (total data, train, test)
            What is the proportion of survivors (survived = 1) in the training data (round 2 decimal points)?
            Hint: Use function round(_, 2), and train_test_split() from sklearn.model_selection, 
            Don't forget to impute missing values with mean.
    '''
    # TODO: Code here
    target = df.pop("Survived")
    x_train, x_test, y_train, y_test = train_test_split(
        df, target, train_size=0.7, stratify=target, random_state=123
    )
    return round((pd.Series)(y_train).eq(1).mean(), 2)
