import time
from tkinter import *
from tkinter import scrolledtext
from tkinter.scrolledtext import ScrolledText


class UI:

    def __init__(self):

        self.window = Tk()

        self.window.title("Dat ve tau lua - Client")

        self.window.geometry('500x300')

        self.clientData = ""

        self.host = ""

        self.message = ""

    def getServerHost(self):

        self.label = Label(self.window, text="Nhap server IP : ")

        self.label.grid(column=0, row=0)

        self.entry = Entry(self.window, width=60)

        self.entry.grid(column=1, row=0)

        self.btn = Button(self.window, text="Ket noi server", command=self.onGetHost)

        self.btn.grid(column=1, row=1)

    def onGetHost(self):

        self.host = self.entry.get()

        self.rest()

    def getClientData(self):

        Label(self.window, text='Danh sach cac chuyen tau : ').grid(column=1, row=0)

        self.selectedChuyenDi = IntVar()

        rad1 = Radiobutton(self.window, text='Chuyen TPHCM - Hanoi', value=0, variable=self.selectedChuyenDi)

        rad2 = Radiobutton(self.window, text='Chuyen TPHCM - Hue', value=1, variable=self.selectedChuyenDi)

        rad3 = Radiobutton(self.window, text='Chuyen Hanoi - Dalat', value=2, variable=self.selectedChuyenDi)

        rad1.grid(column=0, row=1)

        rad2.grid(column=1, row=1)

        rad3.grid(column=2, row=1)

        Label(self.window, text='Danh sach cac loai ve tau : ').grid(column=1, row=2)

        self.selectedType = IntVar()

        rad4 = Radiobutton(self.window, text='Loai A', value=0, variable=self.selectedType)

        rad5 = Radiobutton(self.window, text='Loai B', value=1, variable=self.selectedType)

        rad6 = Radiobutton(self.window, text='Loai C', value=2, variable=self.selectedType)

        rad4.grid(column=0, row=3)

        rad5.grid(column=1, row=3)

        rad6.grid(column=2, row=3)

        Label(self.window, text='Chon so luong ve tau : ').grid(column=0, row=4)

        self.spin = Spinbox(self.window, from_=0, to=60, width=30)

        self.spin.grid(column=1, row=4)

        self.btn = Button(self.window, text="Xac Nhan",
                          command=self.onGetClientData)

        self.btn.grid(column=1, row=5)

    def onGetClientData(self):

        selectedData = ""

        # Switch transacts
        if str(self.selectedChuyenDi.get()) == '0':
            selectedData += 'tphcm_hanoi'
        elif str(self.selectedChuyenDi.get()) == '1':
            selectedData += 'tphcm_hue'
        elif str(self.selectedChuyenDi.get()) == '2':
            selectedData += 'hanoi_dalat'

        # Switch transacts
        if str(self.selectedType.get()) == '0':
            selectedData += ' a'
        elif str(self.selectedType.get()) == '1':
            selectedData += ' b'
        elif str(self.selectedType.get()) == '2':
            selectedData += ' c'

        self.clientData = selectedData + " " + str(self.spin.get())

        self.rest()

    def getServerResponse(self, message):

        self.label = Label(self.window, text='Ket qua : ')

        self.label.grid(column=0, row=0)

        txt = ScrolledText(self.window, width=58, height=12)

        txt.grid(column=0, row=1)

        txt.insert(INSERT, message)

        btnC = Button(self.window, text="Tiep tuc dat ve", command=self.onContinue)

        btnC.grid(column=0, row=2)

        btnQ = Button(self.window, text="Ket thuc dat ve", command=self.onQuit)

        btnQ.grid(column=0, row=3)

    def onQuit(self):

        self.message = "quit"

        self.rest()

    def onContinue(self):

        self.message = "continue"

        self.rest()

    def run(self):

        self.window.mainloop()

    def rest(self):

        self.window.destroy()


