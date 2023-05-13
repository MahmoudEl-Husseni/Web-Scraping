# Description: This file contains all the configurations for the project
# It contains the following:
#   - Configs
#   - Directories
#   - XPATHS
#   - CLASS_NAMES


# Configs
DF = True
SAVE = False
DEBUG = False


# Directories
DATA_DIR = "data"
URL = "https://news.google.com/"
DRIVER_PATH = "/home/mahmoud/Downloads/chromedriver"




DATE_OPTIONS = {
    "Anytime": 1,
    "Past hour": 2,
    "Past 24 hours": 3,
    "Past week": 4,
    "Past year": 5
}
XPATHS = {
    "search_bar": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/input[2]',

    # ADvanced Search xpaths
    "Adv_search_btn": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/button[2]',
    "Exact_phrase": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[1]/input',
    "Has_words": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div[1]/input',
    "Exclude_words": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[4]/div[2]/div/div[1]/div/div[1]/input',
    "Website": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[5]/div[2]/div/div[1]/div/div[1]/input',
    "Date": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[6]/div[2]/div/div/div[1]',
    "Date_choice": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[6]/div[2]/div/div/div[2]/ul/li[{}]',
    "Search_btn": '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[7]/div[2]',
}

CLASS_NAMES = {
    "Main_sub_divs1" : "DBQmFf.NclIid.BL5WZb.Oc0wGc.xP6mwf.j7vNaf",
    
    "Category" : "oOr8M.yETrXb.Ir3o3e.cS3HJf", 
    "Titles" : "DY5T1d.RZIKme", 
    "Sources" : "wEwyrc.AVN2gc.WfKKme",
    "links_div" : "VDXfz", 
    "time" : "WW6dff.uQIVzc.Sksgp.slhocf",

    "Main_sub_divs2" : "NiLAwe.y6IFtc.R7GTQ.keNKEd.j7vNaf.nID9nc",
}