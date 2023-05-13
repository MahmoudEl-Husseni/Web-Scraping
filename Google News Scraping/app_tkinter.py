from tkinter import * 

from config import *
from selenium import webdriver
from google_news_scraping import *

# Functions: 
df = pd.DataFrame()

# go button
def move_to_window():
    root.withdraw()

    if (search_type.get() == "Basic Search"):
        basic_search_window.deiconify()
    else:
        advanced_search_window.deiconify()

def return_to_root(window):
    window.withdraw()
    root.deiconify()
    if (drop.get() == "Basic Search"):
        basic_search_window.withdraw()
    else:
        advanced_search_window.withdraw()

def move_bsc_to_results():
    global df
    if(bsc_inpt.get() == ""):
        return
    
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(URL)

    driver = search_news(driver, bsc_inpt.get())
    df = get_news(driver, DF=True, DEBUG=True)

    basic_search_window.withdraw()
    advanced_search_window.withdraw()

    results_window.deiconify()
    rows = min(5, df.shape[0])
    columns = 5
    for i in range(len(df.columns)):
        e = Entry(results_window, width=20, font=('Arial',16,'bold'), 
                    fg='#ffffff', bg="#521D80", highlightthickness=0, relief="flat", borderwidth=0)
        e.grid(row=0, column=i)
        e.insert(END, df.columns[i])

    if df.shape[0] >= rows and df.shape[1] >= columns:
        for i in range(rows):
            for j in range(columns):
                e = Entry(results_window, width=20, fg='blue', font=('Arial',16,'bold'))
                e.grid(row=i+1, column=j)
                e.insert(END, df.iloc[i, j])
                e.config(state='readonly')

def move_adv_to_results():
    global df
    exct_ph = exact_phrase.get() if exact_phrase.get() != "Enter exact phrase" else ""
    hs_wrds = any_of_these_words.get() if any_of_these_words.get() != "Enter any of these words" else ""
    exc_wrds = none_of_these_words.get() if none_of_these_words.get() != "Enter none of these words" else ""
    # web = website.get()
    dt_op = date_op.get() if date_op.get() != "Enter date" else ""
    
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(URL)

    driver = advanced_search(driver, exact_phrase=exct_ph, has_words=hs_wrds, exclude_words=exc_wrds, date_op=dt_op)
    df = get_news(driver, DF=True, DEBUG=True)

    basic_search_window.withdraw()
    advanced_search_window.withdraw()
    results_window.deiconify()

    rows = min(5, df.shape[0])
    columns = 5
    for i in range(len(df.columns)):
        e = Entry(results_window, width=20, font=('Arial',16,'bold'), 
                    fg='#ffffff', bg="#521D80", highlightthickness=0, relief="flat", borderwidth=0)
        e.grid(row=0, column=i)
        e.insert(END, df.columns[i])

    if df.shape[0] >= rows and df.shape[1] >= columns:
        for i in range(rows):
            for j in range(columns):
                e = Entry(results_window, width=20, fg='blue', font=('Arial',16,'bold'))
                e.grid(row=i+1, column=j)
                e.insert(END, df.iloc[i, j])
                e.config(state='readonly')


# ========================== #
# Create Windows
root = Tk()
basic_search_window = Toplevel(root, width=500, height=500)
advanced_search_window = Toplevel(root, width=500, height=500)
results_window = Toplevel(root, width=500, height=500)


root.title("Google News Scraper")
basic_search_window.title("Basic Search")
advanced_search_window.title("Advanced Search")
results_window.title("Results")

# Open main window initially
basic_search_window.withdraw()
advanced_search_window.withdraw()
results_window.withdraw()


# Set bakcground color
root.config(bg="#521D80")
basic_search_window.config(bg="#521D80")
advanced_search_window.config(bg="#521D80")
# root.geometry("500x500")

# ========================== #
# Root window
# drop down menu
search_type = StringVar()
search_type.set("Basic Search")
search_options = ["Basic Search", "Advanced Search"]

drop = OptionMenu(root, search_type, *search_options)
drop.config(width=15, font=("Arial", 30, "bold", "italic"), bg="#E9A425", fg="#A81E23", 
            activebackground="#9E4B21", activeforeground="#ffffff", highlightthickness=0, relief="flat", 
            borderwidth=0)


drop["menu"].config(font=("Arial", 25, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                    activebackground="#9E4B21", activeforeground="#ffffff", relief="flat",
                    borderwidth=0)


drop.grid(row=0, column=4, columnspan=1, padx=230, pady=120, sticky="nsew")

    

go_btn = Button(root, text="Go", width=10,
                fg="#A81E23", bg="#E9A425", font=("Arial", 30, "bold", "italic"),
                command=move_to_window)
go_btn.grid(row=1, column=4, columnspan=2, pady=10, padx=230)


frame = LabelFrame(root, padx=5, pady=5)
frame.grid(row=2, column=4, columnspan=2, padx=230, pady=80)
 

# ========================== #
# Basic Search window

label = Label(basic_search_window, text="Search type: Basic Search", font=("Arial", 30, "bold", "italic"), bg="#521D80", fg="#ffffff")
label.grid(row=0, column=4, columnspan=3, padx=10, pady=10)

bsc_inpt = Entry(basic_search_window, font=("Arial", 30, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                highlightthickness=0, relief="flat", borderwidth=0)

bsc_inpt.insert(0, "Enter search term")
bsc_inpt.bind("<FocusIn>", lambda args: inpt.delete('0', 'end'))

bsc_inpt.grid(row=1, column=2, columnspan=5, padx=10, pady=10)


search_btn = Button(basic_search_window, text="Search", width=10,
                fg="#000000", bg="#ffffff", font=("Arial", 15, "bold", "italic"),
                command=move_bsc_to_results)

search_btn.grid(row=1, column=7, columnspan=1, pady=50)



ret_btn = Button(basic_search_window, text="Return", width=10,
                fg="#A81E23", bg="#E9A425", font=("Arial", 30, "bold", "italic"),
                 command=lambda: return_to_root(basic_search_window))
ret_btn.grid(row=3, column=5, columnspan=1)

frame = Frame(basic_search_window, padx=5, pady=5)
frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10)



# ========================== #
# Advanced Search window
label = Label(advanced_search_window, text="Search type: Advanced Search", font=("Arial", 30, "bold", "italic"), bg="#521D80", fg="#ffffff")
label.grid(row=0, column=4, columnspan=3, padx=10, pady=10)

# Exact phrase
exact_phrase = Entry(advanced_search_window, font=("Arial", 22, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                highlightthickness=0, relief="flat", borderwidth=0, width=30)

exact_phrase.insert(0, "Enter exact phrase")
exact_phrase.bind("<FocusIn>", lambda args: exact_phrase.delete('0', 'end'))
exact_phrase.grid(row=1, column=2, columnspan=5, padx=10, pady=10)

# Any of these words
any_of_these_words = Entry(advanced_search_window, font=("Arial", 22, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                highlightthickness=0, relief="flat", borderwidth=0, width=30)
any_of_these_words.insert(0, "Enter any of these words")
any_of_these_words.bind("<FocusIn>", lambda args: any_of_these_words.delete('0', 'end'))
any_of_these_words.grid(row=2, column=2, columnspan=5, padx=10, pady=10)

# None of these words
none_of_these_words = Entry(advanced_search_window, font=("Arial", 22, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                highlightthickness=0, relief="flat", borderwidth=0, width=30)
none_of_these_words.insert(0, "Enter none of these words")
none_of_these_words.bind("<FocusIn>", lambda args: none_of_these_words.delete('0', 'end'))
none_of_these_words.grid(row=3, column=2, columnspan=5, padx=10, pady=10)

# # Website
# website = Entry(advanced_search_window, font=("Arial", 30, "bold", "italic"), bg="#E9A425", fg="#A81E23",
#                 highlightthickness=0, relief="flat", borderwidth=0)
# website.insert(0, "Enter website")
# website.bind("<FocusIn>", lambda args: website.delete('0', 'end'))
# website.grid(row=4, column=2, columnspan=5, padx=10, pady=10)


# Date
date = Entry(advanced_search_window, font=("Arial", 22, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                highlightthickness=0, relief="flat", borderwidth=0, width=30)
date.insert(0, "Enter date")
date.bind("<FocusIn>", lambda args: date.delete('0', 'end'))
date.grid(row=4, column=2, columnspan=5, padx=10, pady=10)

# Date operator
date_op = StringVar()
date_op.set("Past year")


drop = OptionMenu(advanced_search_window, date_op, *DATE_OPTIONS.keys())
drop.config(width=15, font=("Arial", 30, "bold", "italic"), bg="#E9A425", fg="#A81E23",
            activebackground="#9E4B21", activeforeground="#ffffff", highlightthickness=0, relief="flat",
            borderwidth=0)

drop["menu"].config(font=("Arial", 25, "bold", "italic"), bg="#E9A425", fg="#A81E23",
                    activebackground="#9E4B21", activeforeground="#ffffff", relief="flat",
                    borderwidth=0)

drop.grid(row=4, column=7, columnspan=1, padx=10, pady=10)


# Search
search_btn = Button(advanced_search_window, text="Search", width=10,
                fg="#000000", bg="#ffffff", font=("Arial", 15, "bold", "italic"),
                command=move_adv_to_results)
search_btn.grid(row=5, column=7, columnspan=1, pady=50)


ret_btn = Button(advanced_search_window, text="Return", width=10,
                fg="#A81E23", bg="#E9A425", font=("Arial", 30, "bold", "italic"),
                command=lambda: return_to_root(advanced_search_window))

ret_btn.grid(row=5, column=5, columnspan=1)

# ========================== #
# Results window
ret_btn = Button(results_window, text="Return", width=10,
                fg="#A81E23", bg="#E9A425", font=("Arial", 30, "bold", "italic"),
                command=lambda: return_to_root(results_window))
ret_btn.grid(row=11, column=1, columnspan=3, pady=10, padx=10)

inpt = Entry(results_window, width=50, font=("Arial", 30, "bold", "italic"), bg="#ffffff", fg="#000000",
                highlightthickness=0, relief="flat", borderwidth=0, justify="center")

inpt.insert(0, "Enter save path")

inpt.grid(row=10, column=1, columnspan=3, padx=10, pady=10)

save_btn = Button(results_window, text="Save", width=8,
                fg="#A81E23", bg="#E9A425", font=("Arial", 24, "bold", "italic"),
                command=lambda: df.to_csv(inpt.get()))

save_btn.grid(row=10, column=4, columnspan=3, pady=10, padx=100)



root.mainloop()