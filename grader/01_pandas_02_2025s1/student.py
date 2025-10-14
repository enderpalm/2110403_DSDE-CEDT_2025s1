import pandas as pd

"""
    ASSIGNMENT 1 (STUDENT VERSION):
    Using pandas to explore youtube trending data from (videos.csv and category_id.json) and answer the questions.
"""


def Q1():
    """
    1. How many rows are there in the videos.csv after removing duplications?
    - To access 'videos.csv', use the path '/data/videos.csv'.
    """
    # TODO: Paste your code here
    df = pd.read_csv("/data/videos.csv")
    return len(df.drop_duplicates())


def Q2(vdo_df):
    """
    2. How many VDO that have "dislikes" more than "likes"? Make sure that you count only unique title!
        - videos.csv has been loaded into memory and is ready to be utilized as vdo_df
        - The duplicate rows of vdo_df have been removed.
    """
    # TODO: Paste your code here
    return len(vdo_df[vdo_df["dislikes"] > vdo_df["likes"]]["title"].drop_duplicates())


def Q3(vdo_df):
    """
    3. How many VDO that are trending on 22 Jan 2018 with comments more than 10,000 comments?
        - videos.csv has been loaded into memory and is ready to be utilized as vdo_df
        - The duplicate rows of vdo_df have been removed.
        - The trending date of vdo_df is represented as 'YY.DD.MM'. For example, January 22, 2018, is represented as '18.22.01'.
    """
    # TODO: Paste your code here
    return len(vdo_df[(vdo_df["trending_date"] == "18.22.01") & (vdo_df["comment_count"] > 10000)])


def Q4(vdo_df):
    """
    4. Which trending date that has the minimum average number of comments per VDO?
        - videos.csv has been loaded into memory and is ready to be utilized as vdo_df
        - The duplicate rows of vdo_df have been removed.
    """
    # TODO:  Paste your code here
    return vdo_df.groupby("trending_date").comment_count.mean().idxmin()


def Q5(vdo_df):
    """
    5. Compare "Sports" and "Comedy", how many days that there are more total daily views of VDO in "Sports" category than in "Comedy" category?
        - videos.csv has been loaded into memory and is ready to be utilized as vdo_df
        - The duplicate rows of vdo_df have been removed.
        - You must load the additional data from 'category_id.json' into memory before executing any operations.
        - To access 'category_id.json', use the path '/data/category_id.json'.
    """
    mapper = pd.read_json("/data/category_id.json")
    tags = []
    for m in mapper["items"]:
        if m["snippet"]["assignable"]:
            tags.append(((int)(m["id"]), m["snippet"]["title"]))
    tags_df = pd.DataFrame(tags, columns=["id", "category"])
    merged_df = vdo_df.merge(tags_df, left_on="category_id", right_on="id")

    sports_views = (
        merged_df[merged_df["category"] == "Sports"][["trending_date", "views"]]
        .groupby("trending_date")
        .sum()
    )
    comedy_views = (
        merged_df[merged_df["category"] == "Comedy"][["trending_date", "views"]]
        .groupby("trending_date")
        .sum()
    )
    sports_views = sports_views.merge(comedy_views, on="trending_date")
    return sports_views[sports_views["views_x"] > sports_views["views_y"]].shape[0]
