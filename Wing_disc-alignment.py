
'''
This script takes an excel file witn samples in sheets.
It corrects the x-values with a given value x0-r and aligns the x values of each sample to each other.
Further the average and Standard Deviation are calculated.
The Script has been written for Shinya Matsuda by Etienne Schmelzer.
'''


import pandas as pd
import os
import sys
import matplotlib.pyplot as plt


# making it a standalone executable: pyinstaller --onefile Shinya.py
# but i can not use the pyinstaller inside of the virtual environment!!

if __name__=="__main__":

    config_name = 'Wing_disc-alighment.cfg'

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        print("frozen")
    elif __file__:
        application_path = os.path.dirname(__file__)

    config_path = os.path.join(application_path, config_name)
    print(application_path)

    if application_path == "":
        application_path = os.path.dirname(os.path.abspath(__file__))


    filename = os.path.join(application_path,"wingdiscs.xlsx")
    print(filename)
    #print(os.path.dirname(os.path.abspath(__file__)))

    dir = application_path

    minimum_substraction = "yes"

    # Reading in the Datafile
    file = pd.read_excel(filename, sheet_name=None)
    # creating an empty dataframe
    df = pd.DataFrame()
    # for loop iterating through the Sheets / Samples in the excel file
    for index, sheetname in enumerate(file):
        # reading in the data of the sheet with sheetname
        df1 = file[sheetname]
        # defining the xcor factor specific for this sample
        xcor = df1.iloc[0, 2]
        # Progress report, which sample is beeing processed
        print("Sample {} is processed; Sheetname: '{}' \nwith x-axis correction of {} ".format(index, sheetname, xcor))
        # adjusting x-axis/x0 with x0_r/the xcor factor
        df1["x0"] = (df1["x0"] - xcor).round(1)
        if minimum_substraction == "yes":
            df1[df1.columns[1]] = df1.iloc[:, 1] - df1.iloc[:, 1].min()

        if df.empty:
            df = df1.iloc[:, 0:2]
        # if the dataframe is not empty -> merge/align the two datasets with each other on the column with name 'x0'
        else:
            df = pd.merge(df, df1.iloc[:, 0:2], how='outer', on='x0')
        # reset df1 to an empty dataframe
        df1 = pd.DataFrame()
    # sorting the values of x0, in case that they are not properly sorted
    df = df.sort_values(by="x0", ascending=True)
    # set the index of the dataframe to the column "x0"
    df = df.set_index("x0")
    # calculate the average of the each row
    df["average"] = df.mean(axis=1)
    # calculate the standard deviation for each row
    df["std"] = df.iloc[:, :-1].std(axis=1)
    # count the non-NAN values for each row
    df["count"] = df.iloc[:, 0:-2].count(axis=1)
    # Generate the Result excel file
    df.to_excel("{}/Results_minimum_substraction.xlsx".format(dir), sheet_name='Minimum Substracted')
    #df.to_csv("Results_minimum_substraction.tab", sep='\t')
    #df.to_csv("{}/Results_minimum_substraction.tsv".format(dir), sep='\t')
    df_minimum_sub = df.copy(deep=True)

    # now without minimum substraction
    minimum_substraction = "no"

    # Reading in the Datafile
    file = pd.read_excel(filename, sheet_name=None)
    # creating an empty dataframe
    df = pd.DataFrame()
    # for loop iterating through the Sheets / Samples in the excel file
    for index, sheetname in enumerate(file):
        # reading in the data of the sheet with sheetname
        df1 = file[sheetname]
        # defining the xcor factor specific for this sample
        xcor = df1.iloc[0, 2]
        # Progress report, which sample is beeing processed
        print("Sample {} is processed; Sheetname: '{}' \nwith x-axis correction of {} ".format(index, sheetname, xcor))
        # adjusting x-axis/x0 with x0_r/the xcor factor
        df1["x0"] = (df1["x0"] - xcor).round(1)
        if minimum_substraction == "yes":
            df1[df1.columns[1]] = df1.iloc[:, 1] - df1.iloc[:, 1].min()

        if df.empty:
            df = df1.iloc[:, 0:2]
        # if the dataframe is not empty -> merge/align the two datasets with each other on the column with name 'x0'
        else:
            df = pd.merge(df, df1.iloc[:, 0:2], how='outer', on='x0')
        # reset df1 to an empty dataframe
        df1 = pd.DataFrame()
    # sorting the values of x0, in case that they are not properly sorted
    df = df.sort_values(by="x0", ascending=True)
    # set the index of the dataframe to the column "x0"
    df = df.set_index("x0")
    # calculate the average of the each row
    df["average"] = df.mean(axis=1)
    # calculate the standard deviation for each row
    df["std"] = df.iloc[:, :-1].std(axis=1)
    # count the non-NAN values for each row
    df["count"] = df.iloc[:, 0:-2].count(axis=1)
    # Generate the Result excel file
    df.to_excel("{}/Results_no_minimum_substraction.xlsx".format(dir), sheet_name='Minimum Substracted')
    #df.to_csv("Results_no_minimum_substraction.tab", sep='\t')
    #df.to_csv("{}/Results_no_minimum_substraction.tsv".format(dir), sep='\t')


    df_no_minimum = df.copy(deep=True)



    # Plotting the dataframes, using subplots:
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
    f0 = df_no_minimum.iloc[:, :-3].plot(ax=axes[0, 0])
    f0.set_title("no minimum substraction")
    # f0.set_xlabel("aligned x-value")
    # f0.set_ylabel("Fluorescent intensity")

    f1 = df_no_minimum.iloc[:, -3].plot(ax=axes[1, 0])
    f1.set_title("no minimum substraction")
    # f1.set_xlabel("aligned x-value")
    # f1.set_ylabel("Fluorescent intensity - average")

    f2 = df_minimum_sub.iloc[:, :-3].plot(ax=axes[0, 1])
    f2.set_title("minimum substracted")
    # f2.set_xlabel("aligned x-value")
    # f2.set_ylabel("Fluorescent intensity")

    f3 = df_minimum_sub.iloc[:, -3].plot(ax=axes[1, 1])
    f3.set_title("minimum substracted")
    # f3.set_xlabel("aligned x-value")
    # f3.set_ylabel("Fluorescent intensity - average")
    plt.savefig("{}/Plots.pdf".format(dir))

    print("The Data has been processed - Awesome")
