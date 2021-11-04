#!/bin/python3
from libs import pythematics as pl
from math import inf
import tkinter as Tk
import copy
import os
import re

global lbl_input, lbl_output
global __calcResult, __pendingSync


__calcBuiltinVariables = {
	"x_": pl.x,
}

__calcVariables = copy.copy(__calcBuiltinVariables)


from stuff import COLORS, gridElement, __ALPHABET, generateMessage, theAppFont

global FG_COLORS
FG_COLORS = [
	COLORS["fg-red"],
	COLORS["fg-orange"],
	COLORS["fg-yellow"],
	COLORS["fg-green"],
	COLORS["fg-cyan"],
	COLORS["fg-blue"],
	COLORS["fg-purple"],
]


__pendingSync: bool = False
__calcResult: int or float or pl.Polynomial = None

global GRAPH_PRECISION, GRAPH_WIDTH, GRAPH_HEIGHT

GRAPH_PRECISION: int = 100
GRAPH_WIDTH: int = 500
GRAPH_HEIGHT: int = 500
LINE_WIDTH: int = 3


def filterReals(cplxList):
	cplxList = filter(lambda x: x.imag == 0 , cplxList)
	return map(lambda x: x.real, cplxList)



# Izbacuje spisak vrednosti.
# Korisnik može da sačuva datu vrednost u promenjivu.
def putThing(equation: list or dict(tuple, bool)):
	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])

	# Nove vrednosti se smeštaju u novi red.
	# Tako ne dolazi do međusobnog poklapanja
	currentRow = 0

	# (dict) koji će biti prosleđen ima {(tuple) za ključ, {(bool)} za vrednost}
	# Ako je vrednost (True), tad se ključ uzima u razmatranje.
	if type(equation) == dict:
		for key, value in equation.items():
			if value:
				gridElement(
					Tk.Button, root,
					row = currentRow, column = 0, text = str(key[0]), width = 20,
					bg = COLORS["bg-key"], fg = COLORS["fg"],
					padx = 5, pady = 0,
					command = lambda val = key[0]: saveVariable(val)
				)
				gridElement(
					Tk.Label, root,
					row = currentRow, column = 1, text = "...",
					bg = COLORS["bg"], fg = COLORS["fg"],
					padx = 5, pady = 0,
				)
				gridElement(
					Tk.Button, root,
					row = currentRow, column = 2, text = str(key[1]), width = 20,
					bg = COLORS["bg-key"], fg = COLORS["fg"],
					padx = 5, pady = 0,
					command = lambda val = key[1]: saveVariable(val)
				)
				currentRow += 1
	elif type(equation) == list:
		for item in equation:
			if abs(item.imag) < 1e-12:
				gridElement(
					Tk.Button, root,
					row = currentRow, column = 0, text = str(item.real), width = 20,
					bg = COLORS["bg-key"], fg = COLORS["fg"],
					padx = 5, pady = 0,
					command = lambda val = item.real: saveVariable(val)
				)
			currentRow += 1

def whenNegative():
	calculate()
	putThing(__calcResult < 0)

def whenNeutral():
	calculate()
	putThing(__calcResult == 0)

def whenPositive():
	calculate()
	putThing(__calcResult > 0)


def sync():
	global __pendingSync
	result = __pendingSync
	__pendingSync = False
	return result

def formatExpression(expression):
	result = re.sub(r"([A-Za-z]+)", r"\1\_", expression).replace("↑", "**")

	# fixing exponential format
	result = re.sub(r"e\_(\+|\-)", r"e\_\1", result)

	return result.replace("\\_", "_")

# Program uses (eval) for calculating.
# That is problem if user wants
# to name a variable as builtIn words
# such as:
#     "def",
#     "class",
#     "else",
#     i tako dalje.
# Therefore variables are edited before {save, load}.
def formatVariableName(name):
	if name[-1] != "_":
		return name + "_"
	return name

def simplify(value):
	if type(value) in [pl.Polynomial]:
		result = ""
		arr = value.arr()
		for i in range(len(arr)-1, -1, -1):
			if (arr[i] != 0):
				if i > 1:
					result += f"{arr[i]} * x ↑ {i} + "
				elif i == 1:
					result += f"{arr[i]} * x + "
				else:
					result += f"{arr[i]} + "
		# uklanja trailing " + "
		return result[:-3]
	elif type(value) in [int, float]:
		return str(value)

	return "Unsupported type."


def calculate():
	global lbl_input, lbl_output
	global __calcResult

	theInput = formatExpression(lbl_input["text"])

	print(theInput)
	if len(theInput) > 0:
		try:
			__calcResult = eval(theInput, __calcVariables)
			resultToOutput()
		except Exception as exception:
			lbl_output["text"] = exception
	else:
		resultToOutput()


def clearVariables():
	global __pendingSync
	global __calcBuiltinVariables, __calcVariables
	__calcVariables = copy.copy(__calcBuiltinVariables)
	__pendingSync = True


def saveVariable(value = None):
	def confirm(name):
		global __calcResult
		global __pendingSync
		valid = True
		for ch in name:
			if ch in __ALPHABET:
				continue
			generateMessage("Please only letters.")
			valid = False


		if valid:
			# Pošto se {eval} koristi za računanje izraza
			#   moglo bi da dođe do problema gde promenjiva nije podržana.
			# Od trenutka kada su promenjive popraćene sa "_" pa na dalje,
			#   ovaj deo koda se koristi više kao sigurnosna mera u slučaju ažuriranja programa.
			#     (* 
			#      *   Ako dođe do bagova vezanog za promenjive:
			#      *       Ovaj deo će obavestiti korisnika o odabiru imena umesto da se ponaša nepredviđenjo.
			#      *       Programer će lakše ustanoviti gde je greška, brže će otkloniti kvar.
			#      *)
			if name in __calcBuiltinVariables.keys() or name + "_" in __calcBuiltinVariables.keys():
				generateMessage("No builtin names.")
				valid = False

		if valid:
			__calcVariables[name + "_"] = value
			__pendingSync = True
			root.destroy()



	def cancel():
		root.destroy()

	if value == None:
		if lbl_input["text"]:
			calculate()
		value = __calcResult


	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])

	lbl = gridElement(
		Tk.Label, root,
		row = 0, column = 0, columnspan = 2,
		text = "Enter Name",
		bg = COLORS["bg"], fg = COLORS["fg"],
		padx = 5, pady = 5,
	)

	nameEntry = gridElement(
		Tk.Entry, root,
		row = 1, column = 0, columnspan = 2,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)


	btn_confirm = gridElement(
		Tk.Button, root,
		row = 2, column = 0, text = "Confirm",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = lambda: confirm(nameEntry.get()),
	)

	btn_cancel = gridElement(
		Tk.Button, root,
		row = 2, column = 1, text = "Cancel",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = cancel
	)


	root.mainloop()


# Čuva trenutno stanje okruženja. 
# Trenutno, to su samo promenjive.
def saveState(name = None):
	def confirm(name, temporary = False):
		global __calcResult
		global __pendingSync
		valid = True
		for ch in name:
			if ch in __ALPHABET:
				continue
			generateMessage("Please only letters.")
			valid = False


		if valid:
			unsupportedTypes = []
			file = open(f"./.states/{'.' if temporary else ''}{name}.pyon", "w")
			file.write(f"{{\n")
			for key, value in __calcVariables.items():
				if key.startswith("_"):
					continue
				print(key, key not in __calcBuiltinVariables.keys())
				if key not in __calcBuiltinVariables.keys():
					if type(value) == pl.Polynomial:
						value = f"pl.Polynomial({value.arr()})"
					elif type(value) in [int, float, complex]:
						pass
					else:
						if type(value) not in unsupportedTypes:
							unsupportedTypes = type(value)
						value = None
						continue
					file.write(f"\t\"{key}\": {value},\n")
				
					
			file.write(f"}}\n")
			file.close()
			try:
				root.destroy()
			except:
				pass

			if len(unsupportedTypes) > 0:
				message = f"Types not supported: \n"
				for tip in unsupportedTypes:
					message += f'\t{str(tip)}'
				generateMessage(message)
				 
	def cancel():
		root.destroy()

	if name != None:
		return confirm(name, True)

	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])

	lbl = gridElement(
		Tk.Label, root,
		row = 0, column = 0, columnspan = 2,
		text = "Enter Name",
		bg = COLORS["bg"], fg = COLORS["fg"],
		padx = 5, pady = 5,
	)

	nameEntry = gridElement(
		Tk.Entry, root,
		row = 1, column = 0, columnspan = 2,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)


	btn_confirm = gridElement(
		Tk.Button, root,
		row = 2, column = 0, text = "Confirm",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = lambda: confirm(nameEntry.get()),
	)

	btn_cancel = gridElement(
		Tk.Button, root,
		row = 2, column = 1, text = "Cancel",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = cancel
	)


	root.mainloop()

# Učitava trenutno stanje okruženja. 
# Trenutno, to su samo promenjive.
def loadState(name = None):
	global __calcVariables
	global __pendingSync

	if name == None:
		root = Tk.Tk()
		root.configure(bg = COLORS["bg"])
		
		gridElement(
			Tk.Label, root,
			row = 0, column = 0, text = "Select state to load.", width = 32, height = 1,
			bg = COLORS["bg"], fg = COLORS["fg"],
		)
		currentRow = 1



		for item in os.listdir("./.states"):
			theName = item.split(".")[0]
			if theName == "":
				continue

		

			gridElement(
				Tk.Button, root,
				row = currentRow, column = 0, text = theName, width = 32, height = 1,
				bg = COLORS["bg-key-expression"], fg = COLORS["fg"],
				command = lambda name = theName: [root.destroy(), loadState(name)],
			)
			currentRow += 1
		root.mainloop()
	else:
		file = open(f"./.states/{name}.pyon", "r")
		print(name)
		variables = eval(file.read())
		file.close()

		__calcVariables = copy.copy(__calcBuiltinVariables)
		for key, value in variables.items():
			__calcVariables[key] = value
		

		del variables
		__pendingSync = True



def findLocalLimits(show = True):
	calculate()
	if type(__calcResult) != pl.Polynomial:
		generateMessage("Can not analyze min max of what is not poliomal")
		return

	diffrentiate = __calcResult.diffrentiate()

	verInkrising = (diffrentiate > 0)
	whereIncreasing = list(filter(lambda val: verInkrising[val], verInkrising))
	whereStays = []
	for where in whereIncreasing:
		whereStays += [*where]


	increaseStart = list(map(lambda x: x[0], whereIncreasing))
	increaseEnd = list(map(lambda x: x[1], whereIncreasing))
	localLimits = {}

	for point in whereStays:
		if ((point in increaseStart) and (point in increaseEnd)) or (point in [-inf, inf]):
			pass
		elif point in increaseStart:
			localLimits[point] = ["min", __calcResult(point)]
		elif point in increaseEnd:
			localLimits[point] = ["max", __calcResult(point)]


	if show:
		root = Tk.Tk()
		root.configure(bg = COLORS["bg"])
		currentRow = 0
		for key, value in localLimits.items():
			gridElement(
				Tk.Label, root,
				row = currentRow, column = 0, text = f"{value[0]} of ",
				bg = COLORS["bg"], fg = COLORS["fg"],
				padx = 5, pady = 0,
			)
			gridElement(
				Tk.Button, root,
				row = currentRow, column = 1, text = str(key), width = 20, height = 1,
				bg = COLORS["bg-key"], fg = COLORS["fg"],
				padx = 5, pady = 0,
				command = lambda val = key: saveVariable(val)
			)
			gridElement(
				Tk.Label, root,
				row = currentRow, column = 2, text = " is ",
				bg = COLORS["bg"], fg = COLORS["fg"],
				padx = 5, pady = 0,
			)
			gridElement(
				Tk.Button, root,
				row = currentRow, column = 3, text = str(value[1]), width = 20, height = 1,
				bg = COLORS["bg-key"], fg = COLORS["fg"],
				padx = 5, pady = 0,
				command = lambda val = value[1]: saveVariable(val)
			)
			currentRow += 1
		root.mainloop()


	return localLimits



def getMouseCoordinator(graphDrawZone, xMin, xMax, yMin, yMax):
	global __motionTextCoordinates
	global GRAPH_WIDTH, GRAPH_HEIGHT
	__MOUSE_TEXT_ALTERATOR_X = 10
	__MOUSE_TEXT_ALTERATOR_Y = 10
	__motionTextCoordinates = [None, None]
	def motion(event):
		global __motionTextCoordinates
		x, y = event.x, event.y
		
		# Ako su koordinate tamo gde je strelica miša
		#     Koordinate mogu ispasti iz ekrana
		xPos = (
			(x * __MOUSE_TEXT_ALTERATOR_X + GRAPH_WIDTH / 2) / (__MOUSE_TEXT_ALTERATOR_X + 1)
		)
		yPos = (
			(y - __MOUSE_TEXT_ALTERATOR_Y) 
		if y > __MOUSE_TEXT_ALTERATOR_Y else
			(y + __MOUSE_TEXT_ALTERATOR_Y * 3)
		)

		xPos_betweenZeroEtOne = x / GRAPH_WIDTH
		yPos_betweenZeroEtOne = y / GRAPH_HEIGHT
		
		xPos_final = xMin + xPos_betweenZeroEtOne * (xMax - xMin)
		yPos_final = yMin + yPos_betweenZeroEtOne * (yMax - yMin)

		textToDraw = f"({round(xPos_final, 3)}, {round(yPos_final, 3)})"

		graphDrawZone.delete(__motionTextCoordinates[0], __motionTextCoordinates[1])
		__motionTextCoordinates[0] = graphDrawZone.create_text(
			xPos, yPos,
			text = re.sub(".", "▓", textToDraw),
			font = theAppFont(style = "bold"), fill = COLORS["bg"]
		)
		__motionTextCoordinates[1] = graphDrawZone.create_text(
			xPos, yPos,
			text = textToDraw,
			font = theAppFont(), fill = COLORS["fg"]
		)
	return motion

def plotGraph():
	def confirm():
		global GRAPH_PRECISION, GRAPH_WIDTH, GRAPH_HEIGHT
		try:
			x_values = [float(entry_min_x.get()), float(entry_max_x.get())]
			y_values = [float(entry_min_y.get()), float(entry_max_y.get())]
		except ValueError:
			generateMessage("Please enter only Floats.")
			return

		reynj = []
		reynjStep = (x_values[1] - x_values[0]) / GRAPH_PRECISION
		currentValue = x_values[0]
		while currentValue < x_values[1]:
			reynj += [currentValue]
			currentValue += reynjStep
		limits = [y_values[0], y_values[1]]

		graph = Tk.Tk()
		graph.configure(bg = COLORS["bg"])
		graph.geometry(f"{GRAPH_WIDTH}x{GRAPH_HEIGHT}")

		graphDrawZone = gridElement(
			Tk.Canvas, graph,
			row = 0, column = 0, width = GRAPH_WIDTH, height = GRAPH_HEIGHT,
			bg = COLORS["bg"],
		)

		x_offset = x_values[0]
		y_offset = y_values[0]
		coordinates = []
		for fnArg in reynj:
			x_pos = (fnArg - x_offset) * GRAPH_WIDTH / (x_values[1] - x_values[0])
			y_pos = (__calcResult(fnArg) - y_offset) * GRAPH_HEIGHT / (y_values[1] - y_values[0])

			coordinates += [x_pos, GRAPH_HEIGHT - y_pos]
		
		graphDrawZone.create_line(*coordinates, width = LINE_WIDTH, fill = COLORS["fg"])		
		graphDrawZone.bind("<Motion>", getMouseCoordinator(
			graphDrawZone, x_values[0], x_values[1], y_values[0], y_values[1]
		))

	calculate()
	if type(__calcResult) != pl.Polynomial:
		generateMessage("Result is not Polinome")
		return

	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])
	
	rowId = 0
	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, columnspan = 2, text = "Graph Plot.", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	rowId += 1

	# Odabir dela grafikona nad kojim se vrši provera promenjivih
	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "min x", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_min_x = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "max x", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_max_x = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)


	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "min y", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_min_y = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "max y", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_max_y = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	btn_confirm = gridElement(
		Tk.Button, root,
		row = rowId, column = 0, columnspan = 2, text = "Confirm",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = confirm,
	)

def plotManyGraphs():
	global FG_COLORS
	def setVariableColor(vars, name, color):
		for i in range(len(vars)):
			if vars[i]["name"] == name:
				vars[i]["color"] = color
				return
		generateMessage("Unable to find variable to set color to.")

	def confirm(variables):
		print(variables)
		global GRAPH_PRECISION, GRAPH_WIDTH, GRAPH_HEIGHT
		try:
			x_values = [float(entry_min_x.get()), float(entry_max_x.get())]
			y_values = [float(entry_min_y.get()), float(entry_max_y.get())]
		except ValueError:
			generateMessage("Please enter only Floats.")
			return

		graph = Tk.Tk()
		graph.configure(bg = COLORS["bg"])
		graph.geometry(f"{GRAPH_WIDTH}x{GRAPH_HEIGHT}")

		reynj = []
		reynjStep = (x_values[1] - x_values[0]) / GRAPH_PRECISION
		currentValue = x_values[0]
		while currentValue < x_values[1]:
			reynj += [currentValue]
			currentValue += reynjStep
		limits = [y_values[0], y_values[1]]

		graphDrawZone = gridElement(
			Tk.Canvas, graph,
			row = 0, column = 0, width = GRAPH_WIDTH, height = GRAPH_HEIGHT,
			bg = COLORS["bg"],
		)
		for variable in variables:
			if variable["color"] == "None":
				continue

			x_offset = x_values[0]
			y_offset = y_values[0]
			coordinates = []
			for fnArg in reynj:
				x_pos = (fnArg - x_offset) * GRAPH_WIDTH / (x_values[1] - x_values[0])
				y_pos = (
					__calcVariables[variable["name"]](fnArg) - y_offset
				) * GRAPH_HEIGHT / (y_values[1] - y_values[0])
				coordinates += [x_pos, GRAPH_HEIGHT - y_pos]

			graphDrawZone.create_line(*coordinates, fill = variable["color"], width = LINE_WIDTH)

		graphDrawZone.create_line(*coordinates, width = LINE_WIDTH, fill = COLORS["fg"])		
		graphDrawZone.bind("<Motion>", getMouseCoordinator(
			graphDrawZone, x_values[0], x_values[1], y_values[0], y_values[1]
		))

	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])

	rowId = 0
	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, columnspan = 2, text = "Graph Plot.", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	rowId += 1

	# Odabir dela grafikona nad kojim se vrši provera promenjivih
	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "min x", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_min_x = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "max x", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_max_x = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)


	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "min y", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_min_y = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	gridElement(
		Tk.Label, root,
		row = rowId, column = 0, text = "max y", width = 32, height = 1,
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

	entry_max_y = gridElement(
		Tk.Entry, root,
		row = rowId, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)

	rowId += 1

	# Odabir promenjivih koje će biti prikazane, u kojoj će boji biti prikazane.
	variables = []

	for variableName in list(__calcVariables.keys()):
		if variableName in __calcBuiltinVariables.keys():
			continue
		if type(__calcVariables[variableName]) != pl.Polynomial:
			continue
		variableName = formatVariableName(variableName)
		variables += [{"name": variableName, "color": "None"}]
		columnId = 0
		radioGrouper = Tk.StringVar()

		gridElement(
			Tk.Label, root,
			row = rowId, column = columnId, text = variableName[:-1], width = 32, height = 1,
			bg = COLORS["bg"], fg = COLORS["fg"],
		)
		columnId += 1

		gridElement(
			Tk.Radiobutton, root, variable = radioGrouper,
			row = rowId, column = columnId, text = "None", value = "None",
			command = lambda x = variableName, y = "None": setVariableColor(variables, x, y)
		)
		columnId += 1

		for color in FG_COLORS:
			gridElement(
				Tk.Radiobutton, root, variable = radioGrouper,
				row = rowId, column = columnId, text = "▓▓▓", value = color, foreground = color,
				command = lambda x = variableName, y = color: setVariableColor(variables, x, y)
			)
			columnId += 1
		rowId += 1


	btn_confirm = gridElement(
		Tk.Button, root,
		row = rowId, column = 0, columnspan = 2, text = "Confirm",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = lambda x = variables: confirm(x),
	)


# računa izraz za zadato x.
def solveForX():
	global lbl_input, __calcResult
	calculate()

	global entry_value
	def confirm(value):
		global entry_value
		expression = simplify(__calcResult).replace("↑", "**")
		expression = expression.replace("x", entry_value.get())
		lbl_solved["text"] = eval(expression)

	root = Tk.Tk()
	# Omogućava korisniku da zada x.
	root.configure(bg = COLORS["bg"])
	gridElement(
		Tk.Label, root,
		row = 0, column = 0, text = "Solve " + str(__calcResult) + " for (x = ",
		bg = COLORS["bg"], fg = COLORS["fg"],
	)
	entry_value = gridElement(
		Tk.Entry, root,
		row = 0, column = 1,
		bg = COLORS["bg-plus"], fg = COLORS["fg"],
	)
	gridElement(
		Tk.Label, root,
		row = 0, column = 2, text = ")",
		bg = COLORS["bg"], fg = COLORS["fg"],
	)
	btn_confirm = gridElement(
		Tk.Button, root,
		row = 1, column = 0, columnspan = 2, text = "Confirm",
		bg = COLORS["bg-key-command"], fg = COLORS["fg"],
		padx = 5, pady = 5,
		command = lambda x = entry_value.get():confirm(x),
	)
	lbl_solved = gridElement(
		Tk.Label, root,
		row = 2, column = 0, columnspan = 2, text = "",
		bg = COLORS["bg"], fg = COLORS["fg"],
	)

# integral
def integrate():
	global lbl_input, lbl_output, __calcResult
	calculate()
	lbl_input["text"] = ""
	if type(__calcResult) == pl.Polynomial:
		__calcResult = __calcResult.integrate()
	elif type(__calcResult) in [float, int]:
		__calcResult = __calcResult * pl.x
	else:
		generateMessage("Unsupported type")
	resultToInput()
	resultToOutput()

# izvod
def diffrentiate():
	global lbl_input, __calcResult
	calculate()
	lbl_input["text"] = ""
	if type(__calcResult) == pl.Polynomial:
		__calcResult = __calcResult.diffrentiate()
	elif type(__calcResult) in [float, int]:
		__calcResult = 0
	else:
		generateMessage("Unsupported type.")
	resultToInput()
	resultToOutput()

def resultToInput():
	global __calcResult, lbl_input
	lbl_input["text"] = simplify(__calcResult)


def resultToOutput():
	global __calcResult, lbl_output
	lbl_output["text"] = simplify(__calcResult)

def removeVariable(name):
	global __calcBuiltinVariables, __calcVariables, __pendingSync
	name = formatVariableName(name)
	if isVariableBuiltin(name):
		generateMessage("Can not remove builtin variable.")
		return
	del __calcVariables[name]
	__pendingSync = True

def isVariableBuiltin(name):
	name = formatVariableName(name)
	return name in __calcBuiltinVariables
