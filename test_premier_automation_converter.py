'''

By: Bryce Eddy
Premier Automation Intern

This program is used to re-format CSV (.txt) files that are exported through IBA Analyzer.

IBA Analyzer is able to look at single and multiple .dat files, and generate/export usable CSV files from them.
However, these files need re-formatted and cleaned up, which is what this program does.

The only characters Sorba allows are A-F (capital), 0-9, and '_'.
If there are any symbols in the tag names, new rules can be added to delete/replace them.

'''

## This scirpt used Tkinter for the GUI
## By using 'pyinstaller', this script is converted to an Application file (.exe), and can be used by any PC regardless if Python is installed.
## THAT IS IN CMD BY: ##
'''
	C:[dir]> pip install pyinstaller
	C:[dir]> pyinstaller Converter.py -F -w

The application is in the 'dist' folder.
'''

import os
import csv
import math as m
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import Tk, Label, Button, filedialog, Entry


class Converter:
    def __init__(self, infile, outfile):
        self.replace = [  # ( <char to look for> , <char to replace it with> )
            (" ", "_"),
            ("#", "NUM"),
            ("\\", "__"),
            ("-", "_"),
            (".", "_")
        ]
        self.accept = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_,"  # Any other cases of non-conforming characters are deleted

        self.c = 0

        self.export_file = open(outfile, "w")
        self.csvfile = open(infile)
        self.csv_reader = csv.reader(self.csvfile, delimiter=',')

    def step(self, row):
        if self.c == 0:  # c == 0 is the first line of the file
            self.header = row[0].split(";")[1:]
            self.header[-1] = self.header[-1][1:-1]  # remove the unnecessary [ ] 's

        if self.c == 1:  # this is the row consisting of all the names, extract them from the unused first element
            self.names = row[0].split(";")[1:]

            self.names = ",".join(self.names)  # merge the list  of names back together into a string
            self.names = self.names.upper()

            self.n = list(self.names)  ### the following are just basic functions to manipulate the data for Sorba
            for i in range(len(self.n)):  # delete trailing whitespaces
                if self.n[i] == " ":
                    self.k = 1
                    while self.n[self.k + i] == " ":
                        self.n[self.k + i] = ""
                        self.k += 1
            self.names = "".join(self.n)

            for field in self.replace:  # replace special char cases
                self.names = self.names.replace(field[0], field[1])

            self.n = list(self.names)  # remove everything not in self.accept
            for i in range(len(self.n)):
                if not self.n[i] in self.accept: self.n[i] = ''
            self.names = "".join(self.n)

            self.names = self.names.split(",")
            self.t = 0
            while self.t == 0:  # Duplicates sometimes arise from the formatting, quick way to deal with them
                self.t = 1
                for i in range(len(self.names)):
                    for x in range(len(self.names)):
                        if (self.names[i] == self.names[x]) and not (x == i):
                            print("Dupe: " + self.names[x])
                            self.names[x] = self.names[x] + "_1"
                            self.t = 0
                            break
            self.names = ",".join(self.names)

            self.output = "Timestamp," + self.names  # output for the first line of the formatted CSV file.

        if self.c > 1:  # c > 1 is in the pure data section of the csv file
            self.split = row[0].split()

            # split row into date and time_data
            self.date = self.split[0]
            self.time_data = self.split[1]

            # reformat date
            self.s_date = self.date.split(".")
            self.o_date = "-".join([self.s_date[2], self.s_date[1], self.s_date[0]])

            # reformat time and data
            self.s_time_data = self.time_data.split(";")
            self.time = self.s_time_data[0]
            self.time = self.time[:12]
            self.o_time = "T" + self.time + "Z"
            self.data = self.s_time_data[1:]

            self.output = "".join([self.o_date, self.o_time, ",", ",".join(self.data)])  # output for formatted CSV data

        # Finally attempt to push the output into a new file
        try:
            if self.c != 0:
                self.export_file.write(self.output + "\n")
        except:
            print("Row " + str(self.c) + " was not written.")
        self.c += 1


class My_App:
    def __init__(self, master):
        self.master = master
        master.title("Converter")
        master.resizable(False, False)

        self.running = False

        self.stat = tk.StringVar()
        self.stat.set("Waiting for file...")

        self.pdir = tk.StringVar()
        self.pdir.set("No output directory selected")

        self.label = Label(master, text='Choose IBAanalyzer CSV (.txt) export  -->')
        self.label.grid(row=0, column=0, padx=5, pady=10)

        self.choose = Button(master, text='Choose file ', command=self.choose_press)
        self.choose.grid(row=0, column=1, pady=10)

        self.label1 = Label(master, textvariable=self.stat)
        self.label1.grid(row=1, columnspan=3, padx=10, pady=20)

        self.conv = Button(master, text='Choose path', command=self.cpath)
        self.conv.grid(row=2, column=1, padx=10, pady=5)

        self.label2 = Label(master, textvariable=self.pdir)
        self.label2.grid(row=2, column=0, padx=10, pady=10)

        self.fname = Entry(master)
        self.fname.grid(row=3, column=0, padx=10, sticky=tk.W + tk.E)

        self.conv = Button(master, text='Convert file', command=self.conv_press)
        self.conv.grid(row=3, column=1, padx=10, pady=5)

        self.pbar = Progressbar(master, orient="horizontal", length=150, mode="determinate")
        self.pbar.grid(row=4, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

    def choose_press(self):
        if not self.running:
            self.filepath = filedialog.askopenfile(mode='r', filetypes=[('Text Document', '*txt')])

            if self.filepath is not None:
                self.path, self.filename = os.path.split(self.filepath.name)
                self.newfilename = 'converted_' + self.filename

                self.fname.delete(0, tk.END)
                self.fname.insert(tk.END, self.newfilename)

                self.stat.set('File ' + self.filepath.name + ' selected')

    def cpath(self):
        if not self.running:
            currdir = "C:\\"
            self.temp_dir = filedialog.askdirectory(initialdir=currdir,
                                                    title="Please select a directory to save the file")

            if self.temp_dir != '':
                self.pdir.set(self.temp_dir)
                try:
                    self.fname.delete(0, tk.END)
                    self.fname.insert(tk.END, self.newfilename)
                    self.stat.set('File ' + self.filepath.name + ' selected')
                except:
                    self.stat.set("Please select a file to convert")

    def conv_press(self):
        if not self.running:
            if self.fname.get()[-4:] == ".txt":
                try:
                    self.newpath = os.path.join(self.temp_dir, self.fname.get())
                    self.stat.set("Processing...")
                    self.master.update()
                    try:
                        file = open(self.filepath.name)
                        self.pbar['maximum'] = len(file.readlines())
                        file.close()

                        self.running = True
                        converter = Converter(self.filepath.name, self.newpath)
                        for row in converter.csv_reader:
                            converter.step(row)
                            if converter.c % 1000 == 0:
                                self.master.update()
                                self.pbar['value'] = converter.c
                        self.pbar['value'] = self.pbar['maximum']
                        converter.export_file.close()
                        converter.csvfile.close()
                        self.running = False

                        self.s_newpath = self.newpath.replace("\\", "/")
                        self.stat.set('Converted file at: ' + self.s_newpath)
                        self.master.update()
                    except:
                        self.stat.set("Unable to convert file")
                except:
                    self.stat.set("Filepath or Filename Error")
            elif self.fname.get()[-4:] == "":
                self.stat.set("Enter a name for the output file")
            else:
                self.stat.set("Filename must be a .txt")
            self.fname.delete(0, tk.END)
            try:
                self.fname.insert(tk.END, self.newfilename)
            except:
                pass


if __name__ == "__main__":
    root = Tk()
    my_app = My_App(root)
    root.mainloop()