"""
Python file to handle the recommendation system.
"""

from .models import Recom

# preserved because it it a really well documented piece of code in a mess.

# import os
# import pandas as pd


# def start():
#     """
#     Function to check if the file to store the user file access data
#     already exists or not, if not then create one.
#
#     Parameters
#     ----------
#     None
#
#     Returns
#     -------
#     None
#     """
#     if not os.path.exists("recom_data.csv"):
#         with open("recom_data.csv", "a") as fp:
#             fp.write("Files")
#
#     global df, val_count
#     val_count = 0
#     df = pd.read_csv("recom_data.csv", index_col="Files")
#
#
# start()  # Call the start function


def get_recom(user_id):
    """
    Function to get the list of recommended files for a given user.

    Parameters
    ----------
    user_id : int, str
        Unique ID of the user.

    Returns
    -------
    list
        A list of recommended files sorted in descending order of priority.
        With max length of list equals to 10.
    """

    user_id = str(user_id)

    recom_list = []

    for obj in Recom.objects.filter(userid = user_id):
        if obj.cnt >= 5:
            recom_list.append(obj.fname)

    return recom_list

    # if user_id in df.columns:
    #     if len(df) > 0:
    #         corr = df.corr()[user_id]
    #         wght = df * corr
    #         wght = wght.loc[:, wght.columns != user_id]
    #
    #         wght["mean"] = wght.mean(axis=1)
    #         final = wght[["mean"]]
    #         final = final.sort_values(by=["mean"], ascending=False)[:10]
    #
    #         return final.index.tolist()
    #
    #     return []
    #
    # else:
    #     df[user_id] = [0] * len(df)
    #     return []


def update_recom(file, user_id):
    """
    Function to update the list of files accessed by user.

    Parameters
    ----------
    file : str
        Name of the file being accessed by user.
    user_id : int, str
        Unique ID of the user accessing the file.

    Returns
    -------
    None
    """

    user_id = str(user_id)

    try:
        recom_entry = Recom.objects.filter(userid = user_id, fname = file).get()
        recom_entry.cnt += 1
        recom_entry.save()
    except Recom.DoesNotExist:
        Recom(userid = user_id, fname = file).save()
    except Recom.MultipleObjectsReturned:
        # actually impossible, someething wrong with db. purge it.
        Recom.objects.filter(userid = user_id, fname = file).delete()


    # if user_id in df.columns:
    #     df[user_id] = df[user_id].apply(lambda x: round((x * 0.8), 2))
    # else:
    #     df[user_id] = [0] * len(df)
    #
    # if file not in df.index:
    #     df.loc[file] = [0] * len(df.columns)
    #
    # df.loc[[file], [user_id]] = 10
    #
    # global val_count
    # val_count += 1
    #
    # if val_count >= 5:
    #     df.to_csv("recom_data.csv")
    #     val_count = 0
