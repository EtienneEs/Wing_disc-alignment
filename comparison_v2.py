print("loading complete")
import pandas as pd
import os

from tkinter import filedialog
from tkinter import *



def getfilepath(title = "Select File"):
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="os.path.abspath(__file__))", title=title)
    print("Filepath:" + root.filename)
    filename = root.filename
    return filename

n_cond = int(input("How many conditions do you want to combine, including control?\n>"))
paths_cond = []
for n in range(n_cond):
    if n == 0:
        print("Please select the Control")
        paths_cond.append(getfilepath("Select your CONTROL"))
    else:
        print("Please select your Condition {}".format(n))
        paths_cond.append(getfilepath("Select condition:"))

print("Files were selected\nStart processing....")
min_opt = str(input("Use Minimum value from control for normalization of all conditions? (y/n/no_min)\n(n will use minimum value of the respective condition)\n(no_min: no minimum value will be substracted)\n>"))

if min_opt == "y":
    print("The Minimum value of the Condition 0 / Control will be used for all conditions")
    n_method = "Normalization_against_min-value_from_control"
elif min_opt == "n":
    print("The conditions are normalized with the intrinsic minimum value")
    n_method = "Normalization_against_min-value_each_condition"
else:
    print("The Conditions will be processed without any substraction of a minimum value")
    n_method = "no_min_substraction"

df = pd.DataFrame()
max_value = pd.read_excel(paths_cond[0]).loc[:, "average"].max()
min_value = pd.read_excel(paths_cond[0]).loc[:, "average"].min()
for n, path in enumerate(paths_cond):
    print("Processing Condition {}".format(n))
    df1 = pd.read_excel(path)
    df2 = pd.DataFrame()
    name = os.path.basename(path).split(".")[0]
    # writing a new dataframe with all the necessary values
    df2["x0"] = df1.loc[:, "x0"]
    if min_opt == "y":
        df2[name + "_average"] = (df1.loc[:, "average"]-min_value) / (max_value - min_value)
        df2[name + "_std"] = df1.loc[:, "std"]/ (max_value - min_value)
    elif min_opt == "n":
        df2[name + "_average"] = (df1.loc[:, "average"] - df1.loc[:, "average"].min()) / (max_value - min_value)
        df2[name + "_std"] = df1.loc[:, "std"] / (max_value - min_value)
    else:
        df2[name + "_average"] = (df1.loc[:, "average"]) / max_value
    df2[name + "_std_original"] = df1.loc[:, "std"]
    df2[name + "_count"] = df1.loc[:, "count"]

    # extracting the maximum value of the control
    if n == 0:
        df = df2
    else:
        print("Merging Data")
        df = pd.merge(df, df2, how="outer", on="x0")

df = df.set_index("x0")
print("All conditions were processed")
savename = paths_cond[0].split(".")[0]

savename_excel = "{}_Normalized_comparison_{}.xlsx".format(savename,n_method)
print("Saving excel file as {}".format(savename_excel))
df.to_excel(savename_excel)

import matplotlib.pyplot as plt # i need to import it here because otherwise i get troubles with tkinter
print("Generating Plot")
df.filter(regex='average').plot(figsize=(10, 10))
art=[]
lgd = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1))
art.append(lgd)
print("Saving Plot")
plt.savefig("{}_Normalized_comparison_{}.pdf".format(savename, n_method), additional_artists=art, bbox_inches="tight")

print("Awesome - Comparison finished")
