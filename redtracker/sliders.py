import sys
import os
import csv
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

root = Tk()
root.attributes("-topmost", True)

root.geometry("720x480")
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
    return row_from_file


def update_value(val):
    all_entries_vals = []
    for entry in entries:
        all_entries_vals.append(entry.get())
    # Save to file
    save_value(all_entries_vals)
    # print("Values: {}".format(all_entries_vals))


latest_values = read_data()
values_to_change = ['hue_min', 'hue_max', 'sat_min', 'sat_max', 'val_min', 'val_max']
r = 0

for value in values_to_change:
    parent = Frame(root, bd=0, relief=SUNKEN)
    Label(parent, text=value, relief=RIDGE, pady=21, padx=10, width=20).grid(row=r, column=0)
    slider = Scale(parent, bg='light grey', from_=0, to=255, width=35, length=220, command=update_value,
                   orient=HORIZONTAL)
    slider.set(latest_values[r])
    slider.grid(row=r, column=1)
    entries.append(slider)
    parent.pack(expand=1, pady=5)
    r += 1


if __name__ == '__main__':
    mainloop()
