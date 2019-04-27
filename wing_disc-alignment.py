'''
This script takes an excel file witn samples in sheets.
It corrects the x-values with a given value x0-r and aligns the x values of each sample to each other.
Further the average and Standard Deviation are calculated.
The Script has been written for Shinya Matsuda by Etienne Schmelzer.
'''

# to improve compatibility with jupyter notebook decomment:
#%gui tk

import pandas as pd
import os
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

print("""
Wingdisc alignment
Version 5, for mac
Release date: 27.04.2019
""")

# making it a standalone executable: pyinstaller --onefile filename.py
# but i can not use the pyinstaller inside of the virtual environment!!

def getfilepath(title = "Select File"):
    """
    Generates a Popup window for the user to choose the filepath. If no file is selected,
    the program will stop.
    :param title: Title displayed in the Popupwindow (only in LINUX and Windows)
    :return: tuple, complete filepath
    """
    filename = filedialog.askopenfilenames(initialdir="os.path.abspath(__file__))", title=title)
    print(filename)

    if filename == "":
        print("No file was selected")
        quit(0)
    return filename

def make_folder(path):
    """
    Will check if directory exists and if not create it
    :param path: str 
    """
    if not os.path.exists(path):
        os.makedirs(path)

def create_subfolder(bool, filename, suffix):
    if bool == "y" or bool == True:
        # We will create a directory with the same name as the original file
        directory = filename.split(".")[0]
        # Name of the subdirectory
        directory = directory + suffix
        make_folder(directory)

    else:
        directory = os.path.dirname(filename)
    return directory


def align_wingdiscs(filename, min_sub):
    """
    Takes an Excel file with multiple sheets as input.
    Each sheet represents an individual wingdisc, with x coordinates,
    intensity values and an x_correction value.
    The x-values are corrected with x-corr (alignment of each wingdisc on x).
    Choice: min_sub:

    True: minimum Intensity value of the individual wingdisc is substracted
    False: no minimum substraction of the Intensity values.

    Then the intensity values are merged into a complete database, containing
    all values. Further average, standard deviation and number of sample per row
    is calculated.
    The database is returned
    :param filename: str
    :param min_sub: boolean
    :return: pd.DataFrame
    """
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
        if min_sub == True:
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
    if min_sub == True:
        choice=""
    else: choice="_no"
    df.to_excel("{}/{}{}_min_sub.xlsx".format(dir, outfilename, choice), sheet_name='no Minimum Substracted'.format(choice))
    # df.to_csv("Results_minimum_substraction.tab", sep='\t')
    # df.to_csv("{}/Results_minimum_substraction.tsv".format(dir), sep='\t')
    return df

def HarryPlotter(dir, outfilename, df_no_minimum, df_minimum_sub):
    # Tkinter and matplotlib seem to be incompatible if imported simultaneously.
    # Later import of matplotlib solves the issue.
    import matplotlib.pyplot as plt

    # Plotting the dataframes, using subplots:
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
    f0 = df_no_minimum.iloc[:, :-3].plot(ax=axes[0, 0])
    f0.set_title("no minimum substraction")
    f0.set_xlabel("x")
    f0.set_ylabel("Fluorescent intensity")

    f1 = df_no_minimum.iloc[:, -3].plot(ax=axes[1, 0])
    f1.set_title("no minimum substraction")
    f1.set_xlabel("x")
    f1.set_ylabel("Fluorescent intensity")

    f2 = df_minimum_sub.iloc[:, :-3].plot(ax=axes[0, 1])
    f2.set_title("minimum substracted")
    f2.set_xlabel("x")
    f2.set_ylabel("Fluorescent intensity")

    f3 = df_minimum_sub.iloc[:, -3].plot(ax=axes[1, 1])
    f3.set_title("minimum substracted")
    f3.set_xlabel("x")
    f3.set_ylabel("Fluorescent intensity")
    plt.savefig("{}/{}Plots.pdf".format(dir, outfilename))

if __name__=="__main__":

    root=Tk()
    root.withdraw()

    # Read in filename
    filenames = getfilepath("Please select your file(s)")
    # Ask if to store in a subfolder
    bool_from_user = messagebox.askyesno("Please Choose:",
                                        "Do you desire to store your Results in a subfolder?")
    print("2")
    for filename in filenames:


        # depending on user choice selection of the destination directory
        dir = create_subfolder(bool_from_user, filename, "_aligned")

        # Samplename
        outfilename = os.path.basename(filename).split(".")[0]
        print(outfilename)

        df_minimum_sub=align_wingdiscs(filename, min_sub=True)
        # now without minimum substraction
        df_no_minimum=align_wingdiscs(filename, min_sub=False)

        HarryPlotter(dir, outfilename, df_no_minimum, df_minimum_sub)

    print("\nThe Data has been processed - Awesome\n")

    print("""
                        Exterminate!
                       /
          _n__n__
         /       \===V==<D
        /_________\\
         |   |   |
        ------------               This script was
        |  || || || \+++----<(     written for you
        =============              by Etienne Schmelzer
        | O | O | O |
       (| O | O | O |\)
        | O | O | O | \\
       (| O | O | O | O\)
     ======================
    """)
    root.destroy()