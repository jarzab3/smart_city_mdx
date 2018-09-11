import argparse
import sys
import os
import csv
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

root = Tk()
root.attributes("-topmost", True)
delimiter = "*&*"
# root.geometry("1028x720")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("Adjust HSV values")
root.configure(background="white")
entries = []
file_name = "hsv_range_data.txt"


def save_value(data):
    with open(file_name, 'w', os.O_NONBLOCK) as w:
        writer = csv.writer(w, delimiter=',')
        writer.writerow(data)
        w.flush()

def read_data():
    """
    Reads from a file and returns a data in the array type.
    :return:
    """
    row_from_file = []
    with open(file_name, 'r', os.O_NONBLOCK) as rea:
        reader = csv.reader(rea, delimiter=',')
        for i, row in enumerate(reader):
            row_from_file = row
    if delimiter in row_from_file:
        row_from_file.remove(delimiter)
    return row_from_file

def update_value(val):
    all_entries_vals = []
    for index, entry in enumerate(entries):
        all_entries_vals.append(entry.get())
        if index == 5:
            all_entries_vals.append(delimiter)
    # Save to file
    save_value(all_entries_vals)
    # print("Values: {}".format(all_entries_vals))


def run_main():
    no_set = False
    latest_values = read_data()
    if len(latest_values) != 12:
        print("Current file does not have a correct format")
        no_set = True
    values_to_change = ['hue_min_R', 'hue_max_R', 'sat_min_R', 'sat_max_R', 'val_min_R', 'val_max_R', 'hue_min_G',
                        'hue_max_G', 'sat_min_G', 'sat_max_G', 'val_min_G', 'val_max_G']
    r = 0
    # Display color on the top of the window
    Label(root,
             text="RED",
             fg="black",
             bg="white",
             font="Verdana 13 bold").pack()

    for value in values_to_change:
        parent = Frame(root, bd=0, relief=SUNKEN)
        Label(parent, text=value, relief=RIDGE, pady=21, padx=10, width=20).grid(row=r, column=0)
        slider = Scale(parent, bg='light grey', from_=0, to=255, width=35, length=220, command=update_value,
                       orient=HORIZONTAL)
        if not no_set:
            slider.set(latest_values[r])
        slider.grid(row=r, column=1)
        entries.append(slider)
        parent.pack(expand=1, pady=5)
        r += 1
        if r == 6:
            Label(root,
                  text="GREEN",
                  fg="black",
                  bg="white",
                  font="Verdana 13 bold").pack()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run sliders for training')
    parser.add_argument('-c', '--color',
                        required=False,
                        help='Color for training data')
    params = parser.parse_args()
    run_main()
    mainloop()
