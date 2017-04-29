#!/usr/bin/env python3

# Binary(possibly hexadecimal too) Toggle GUI

from tkinter import *
from binObj import *


class BinToggle(Button):
    def __init__(self, ln, value):
        """b.__init__(bintoggleln, value) -> None
            creates new bintoggle object(a switch for a single digit of binary)
            which is represented graphically in tkinter
            methods: b.update(), b.toggleState()"""
        self.state = 0  # state, can be 0 or 1
        self.val = value  # value of the toggle when set to 1
        self.l = ln  # master binary toggle line
        self.currentVal = 0  # current value of toggle
        Button.__init__(self, master=self.l, text="0", width=4, height=2, command=self.toggleState)  # initialise button
        # cosmetic
        self['bg'] = 'white'
        self.update()

    def update(self):
        """b.update() -> None
            updates the button's text, cosmetics
            and set currentVal"""
        self['text'] = str(self.state)
        if self.state == 1:
            self['bg'] = 'white'
            self['fg'] = 'blue'
            self.currentVal = self.val  # set val of switch to val at 1
        else:
            self['bg'] = 'white'
            self['fg'] = 'red'
            self.currentVal = 0

    def toggleState(self):
        """b.toggleState() -> None
            toggles between 0 and 1"""
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
        updateUseBin()  # update int and hex vals
        self.update()  # update button


class BinToggleLn(Frame):
    def __init__(self, master, row_pos):
        """b.__init__(master, row_pos) -> None
            initializes row of binary toggle switches
            methods: showErr(), getValue()"""
        self.m = master
        Frame.__init__(self, self.m)
        self.grid(row=row_pos)
        self.toggles = []  # list of toggles
        for val in range(8):
            Label(master=self, text=str(2 ** val)).grid(row=row_pos, column=8 - val)  # create labels for toggles
            self.toggles.append(BinToggle(self, 2 ** val))  # create toggle
            self.toggles[val].grid(row=row_pos + 1, column=8 - val)
        self.statL = Label(text='Status: Accurate', fg='green')  # status label
        self.statL.grid(row=row_pos + 1, column=0)

    def showErr(self):
        """b.showErr() -> None
            shows the integer overflow err"""
        self.statL['text'] = 'Status: Err: Integer Overflow'
        self.statL['fg'] = 'red'

    def getValue(self):
        """b.getValue() -> int
            returns the integer value of the
            binary toggles"""
        binStr = ''
        for ind in range(7, -1, -1):
            binStr += str(self.toggles[ind].state)  # add values of toggles to string
        binObj = Bin(binStr)  # pass to Bin obj in binObj file
        binObj.update_int()  # get int val
        return binObj.bv  # return int val

    def readInVal(self, binstr):
        """b.readInVal(binstr) -> None
            reads in a binary value, sets toggles
            to those values"""
        bstr = binstr[::-1]  # reverse bin string
        if len(self.toggles) < len(bstr):   # if integer overflow
            self.showErr()
            return None
        else:
            self.statL['text'] = 'Status: Accurate'
            self.statL['fg'] = 'green'
        for ind in range(len(bstr)):  # update toggle modes with string val
            self.toggles[ind].state = int(bstr[ind])
            self.toggles[ind].update()


root = Tk()
root.title("Bases")

toggleLn = BinToggleLn(root, 7)
# create entry and text variables
hexEntry = StringVar()
hexEntry.set('0')

intEntry = StringVar()
intEntry.set('0')

asciiL = StringVar()
asciiL.set('\x00')


def updateUseBin():
    """updateUseBin() -> None
        updates the int entry and the hex entry
        with the value of the binary toggles"""
    intEntry.set(str(toggleLn.getValue()))  # set using bin
    hexEntry.set(str(hex(toggleLn.getValue()))[2:])
    asciiL.set(chr(toggleLn.getValue()))


def updateUseInt(arg1, arg2, arg3):  # arg1, arg2, and arg3 are arguments passed by the trace function
    """updateUseInt(ar1, ar2, ar3) -> None
        updates the hex entry and the bin toggles
        with the value of the int entry"""
    if intEntry.get() == '':
        return None
    elif intEntry.get() == '0':  # if value is 0
        toggleLn.readInVal('00000000')
        hexEntry.set('0')
        asciiL.set('\x00')
        return None
    toggleLn.readInVal(bin(int(intEntry.get()))[2:])  # set using int
    hexEntry.set(str(hex(int(intEntry.get())))[2:])
    asciiL.set(chr(int(intEntry.get())))


def updateUseHex(arg1, arg2, arg3):
    """updateUseHex(arg1, arg2, arg3) -> None
        updates the int entry and bin toggles
        with the value of the hex entry"""
    if hexEntry.get() == '':
        return None
    elif hexEntry.get() == '0':
        toggleLn.readInVal('00000000')
        intEntry.set('0')
        asciiL.set('\x00')
        return None
    toggleLn.readInVal(bin(int(hexEntry.get(), 16))[2:])  # set using hex
    intEntry.set(str(int(hexEntry.get(), 16)))
    asciiL.set(chr(int(hexEntry.get(), 16)))


# create objects

Label(text="ASCII Char:", font=('Arial', 10, 'bold')).grid(row=0, column=0)
Label(textvariable=asciiL, bg='light yellow').grid(row=1, column=0)

Label(text="Base 10:", font=('Arial', 10, 'bold')).grid(row=2, column=0)
intE = Entry(textvariable=intEntry, width=20)
intEntry.trace('w', updateUseInt)
intE.grid(row=3, column=0)

Label(text="Base 16(Hex):", font=('Arial', 10, 'bold')).grid(row=4, column=0)
hexE = Entry(textvariable=hexEntry, width=20)
hexEntry.trace('w', updateUseHex)
hexE.grid(row=5, column=0)

Label(text="Binary Toggle:", font=('Arial', 10, 'bold')).grid(row=6, column=0)

root.mainloop()
