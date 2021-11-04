#!/bin/python3
import time
from tkinter.constants import COMMAND

import os, sys
import stuff
from stuff import COLORS, generateMessage, gridElement, theAppFont, __OPERATORS, __ALPHABET
import tkinter as Tk
import calculator
import threading


def clear():
	try:
		lbl_input["text"] = lbl_input["text"].strip()
		if lbl_input["text"][-1] in __ALPHABET+ "_":
			while lbl_input["text"][-1] in __ALPHABET+ "_":
				lbl_input["text"] = lbl_input["text"][:-1]
		else:
			lbl_input["text"] = lbl_input["text"][:-1].strip()
		if lbl_input["text"][-1] in __OPERATORS + ",":
			lbl_input["text"] += " "
	except IndexError:
		pass


def clearAll():
	lbl_input["text"] = ""


def refreshVariablePad():
	for widgets in variablePad.winfo_children():
		widgets.destroy()
	currentRow = 0
	for variable in calculator.__calcVariables.keys():
		if variable.startswith("_"):
			continue
		gridElement(
			Tk.Button, variablePad,
			row = currentRow, column = 0, text = variable[:-1], width = 15, height = 1,
			bg = COLORS["bg-key-variable"], fg = COLORS["fg"],
			command = lambda txt = variable[:-1]: insertText(txt),
		)
		gridElement(
			Tk.Label, variablePad,
			row = currentRow, column = 1, text = str(
				calculator.simplify(calculator.__calcVariables[variable])
			), font = theAppFont(size = "9"),
			bg = COLORS["bg"], fg = COLORS["fg"],
		)
		if not calculator.isVariableBuiltin(variable):
			gridElement(
				Tk.Button, variablePad,
				row = currentRow, column = 2, text = "remove", width = 15, height = 1,
				bg = COLORS["bg-key"], fg = COLORS["fg"],
				command = lambda txt = variable: calculator.removeVariable(txt[:-1]),
			)
		currentRow += 1


def refreshInterface():
	while True:
		time.sleep(1)
		if calculator.sync():
			refreshVariablePad()




# Koristi se za formatiranje teksta.
def insertText(text):
	calcResult = None
	lbl_output["text"] = ""
	# radi preglednosti, oko operatora se stavlja razmak
	if text in __OPERATORS:
		lbl_input["text"] += " "
	# radi preglednosti, nakon zareza se stavlja razmak
	lbl_input["text"] += text
	if text in __OPERATORS + ",":
		lbl_input["text"] += " "


def alterColors(isLightMode):
	stuff.setColorMode(isLightMode)
	calculator.saveState("temp")
	os.execl(sys.executable, sys.executable, *sys.argv)

def setColorMode():
	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])
	gridElement(
		Tk.Button, root, text = "Dark",
		row = 0, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(False)
	)
	gridElement(
		Tk.Button, root, text = "Ask System",
		row = 1, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(None)
	)
	gridElement(
		Tk.Button, root, text = "Light",
		row = 2, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(True)
	)


if __name__ == "__main__":
	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])
	lbl_input = gridElement(
		Tk.Label, root,
		row = 0, column = 0, columnspan = 4,
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
	)
	lbl_output = gridElement(
		Tk.Label, root,
		row = 1, column = 0, columnspan = 4,
		bg = COLORS["bg"], font = theAppFont(size = "20"),
		padx = 5, pady = 5,
	)

	calculator.lbl_input = lbl_input
	calculator.lbl_output = lbl_output

	# Brojčana tastatura za unos teksta.
	numPad = gridElement(Tk.Frame, root, row = 2, column = 0, padx = 5, pady = 5)

	gridElement(
		Tk.Button, numPad,
		row = 0, column = 1, text = "(", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("("),
	)
	gridElement(
		Tk.Button, numPad,
		row = 0, column = 2, text = ")", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText(")"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 0, column = 3, text = "+", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("+"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 1, column = 0, text = "7", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("7"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 1, column = 1, text = "8", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("8"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 1, column = 2, text = "9", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("9"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 1, column = 3, text = "-", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("-"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 2, column = 0, text = "4", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("4"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 2, column = 1, text = "5", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("5"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 2, column = 2, text = "6", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("6"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 2, column = 3, text = "*", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("*"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 3, column = 0, text = "1", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("1"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 3, column = 1, text = "2", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("2"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 3, column = 2, text = "3", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("3"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 3, column = 3, text = "/", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("/"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 4, column = 0, text = "0", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("0"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 4, column = 1, text = ".", width = 1, height = 1,
		bg = COLORS["bg-key-digit"], fg = COLORS["fg"],
		command = lambda : insertText("."),
	)
	gridElement(
		Tk.Button, numPad,
		row = 4, column = 2, text = "%", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("%"),
	)
	gridElement(
		Tk.Button, numPad,
		row = 4, column = 3, text = "↑", width = 1, height = 1,
		bg = COLORS["bg-key"], fg = COLORS["fg"],
		command = lambda : insertText("↑"),
	)

	gridElement(
		Tk.Button, numPad,
		row = 5, column = 0, columnspan = 4, text = "EVAL",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.calculate,
	)


	# Prostor za promenjive.
	variablePad = gridElement(Tk.Frame, root, row = 2, column = 1, padx = 5, pady = 5)
	refreshVariablePad()

	# Razne operacije vezane za okuženje
	utilPad = gridElement(Tk.Frame, root, row = 3, column = 0, padx = 5, pady = 5)

	gridElement(
		Tk.Button, utilPad,
		row = 0, column = 0, text = "Clear", width = 15, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = clear,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 0, column = 1, text = "Clear All", width = 15, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = clearAll,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 1, column = 0, columnspan = 2, text = "Save Variable", width = 32, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.saveVariable,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 2, column = 0, columnspan = 2, text = "Clear Variables", width = 32, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.clearVariables,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 3, column = 0, columnspan = 2, text = "Save State", width = 32, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.saveState,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 4, column = 0, columnspan = 2, text = "Load State", width = 32, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.loadState,
	)
	gridElement(
		Tk.Button, utilPad,
		row = 6, column = 0, columnspan = 2, text = "Set Color Mode", width = 32, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = setColorMode,
	)


	# Razne operacije vezane za izraz.
	analysisPad = gridElement(Tk.Frame, root, row = 3, column = 1, padx = 5, pady = 5)

	gridElement(
		Tk.Button, analysisPad,
		row = 0, column = 0, text = "When Negative", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.whenNegative,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 1, column = 0, text = "When Neutral", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.whenNeutral,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 2, column = 0, text = "When Positive", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.whenPositive,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 3, column = 0, text = "Find Local Limits", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.findLocalLimits,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 4, column = 0, text = "Plot Graph", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.plotGraph,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 5, column = 0, text = "Plot Many Graphs", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.plotManyGraphs,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 6, column = 0, text = "Solve For (x)", width = 20, height = 1,
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		command = calculator.solveForX,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 7, column = 0, text = "Integrate", width = 20, height = 1,
		bg = COLORS["bg-key-function"], fg = COLORS["fg"],
		command = calculator.integrate,
	)
	gridElement(
		Tk.Button, analysisPad,
		row = 8, column = 0, text = "Differentiate", width = 20, height = 1,
		bg = COLORS["bg-key-function"], fg = COLORS["fg"],
		command = calculator.diffrentiate,
	)

	if os.path.isfile("./.states/.temp.pyon"):
		calculator.loadState(".temp")
		os.remove("./.states/.temp.pyon")
	

	refresherOfInterface = threading.Thread(target = refreshInterface, daemon = True)
	refresherOfInterface.start()
	root.mainloop()
