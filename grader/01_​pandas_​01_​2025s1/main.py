import pandas as pd
from student import *
import os


def main():
    input_string = input().strip()
    df = pd.read_csv('/home/enderpalm/cedt/dsde/2110403_DSDE-CEDT_2025s1/grader/01_​pandas_​01_​2025s1/scores.csv')
    input_command = f"{input_string}(df)"
    print(f"{eval(input_command)}")


if __name__ == "__main__":
    main()
