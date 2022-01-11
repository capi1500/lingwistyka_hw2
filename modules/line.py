from modules.context import Context
from modules.utils import conditional_input
import modules.database as db


class LineValue:
	def __init__(self, word):
		self.word = word
		self.clas = []
		self.case = []
		self.gend = []
		self.numb = []
		self.pers = []
		self.degr = []
		self.aspe = []
		self.time = []
		self.mood = []

	def add(self, category: int, value: str):
		if category == 1:
			self.clas.append(value)
		elif category == 2:
			self.case.append(value)
		elif category == 3:
			self.gend.append(value)
		elif category == 4:
			self.numb.append(value)
		elif category == 5:
			self.pers.append(value)
		elif category == 6:
			self.degr.append(value)
		elif category == 7:
			self.aspe.append(value)
		elif category == 8:
			self.time.append(value)
		elif category == 9:
			self.mood.append(value)

	def __str__(self):
		out = "Line(" + self.word + ")\n"
		out += "\tclass = " + str(self.clas) + "\n"
		out += "\tcase = " + str(self.case) + "\n"
		out += "\tgend = " + str(self.gend) + "\n"
		out += "\tnumb = " + str(self.numb) + "\n"
		out += "\tpers = " + str(self.pers) + "\n"
		out += "\tdegr = " + str(self.degr) + "\n"
		out += "\taspe = " + str(self.aspe) + "\n"
		out += "\ttime = " + str(self.time) + "\n"
		out += "\tmood = " + str(self.mood) + "\n"
		return out

	def __eq__(self, other):
		return (self.word == other.word and
		        self.clas == other.clas and
		        self.gend == other.gend and
		        self.numb == other.numb and
		        self.pers == other.pers and
		        self.degr == other.degr and
		        self.aspe == other.aspe and
		        self.time == other.time and
		        self.mood == other.mood)
	
	def show_diff(self, other):
		if self.word != other.word:
			print("got: '" + self.word + "', expected: '" + other.word + "'")
		if self.clas != other.clas:
			print("got: " + str(self.clas) + ", expected: " + str(other.clas) + "")
		if self.gend != other.gend:
			print("got: " + str(self.gend) + ", expected: " + str(other.gend) + "")
		if self.numb != other.numb:
			print("got: " + str(self.numb) + ", expected: " + str(other.numb) + "")
		if self.pers != other.pers:
			print("got: " + str(self.pers) + ", expected: " + str(other.pers) + "")
		if self.degr != other.degr:
			print("got: " + str(self.degr) + ", expected: " + str(other.degr) + "")
		if self.aspe != other.aspe:
			print("got: " + str(self.aspe) + ", expected: " + str(other.aspe) + "")
		if self.time != other.time:
			print("got: " + str(self.time) + ", expected: " + str(other.time) + "")
		if self.mood != other.mood:
			print("got: " + str(self.mood) + ", expected: " + str(other.mood) + "")
		

def process_line(line: str, context: Context):
	line = line.lower()
	if line.find(":") == -1:
		(word, gramma) = line.split(" ", 1)
		print("Warning: ':' not found. Line: '" + line + "'")
		if conditional_input("Skip line? (y/N) ", "y", False):
			return None
	else:
		(word, gramma) = line.split(":", 1)

	out = LineValue(word)
	last_added_category = 0

	for value_list in gramma.split(","):
		for value in value_list.split("/"):
			category_id = 0
			category_str = ""
			value = value.strip()
			(_, form, category) = db.get_default_form(context.db, value)
			if form == "":
				print("Error: Value '" + value + "' not found in the database")
				if context.args.edit:
					if conditional_input("Add value '" + value + "' to the database? (y/N) ", "y", False):
						ref = input("What should it reference?\n> ")
						while not db.value_exists(context.db, ref):
							ref = input("Value '" + "' not found. What should '" + value + "' reference?\n> ")
						db.insert_value(context.con, context.db, value, ref)
			else:
				if category_id == 0:
					category_id = category
					if category_id <= last_added_category:
						print("Warning: current category should go before previous one. Check order of categories.")
				elif category != category_id:
					print("Error: previous category (" + category_str + ") differs from current one (" + category + ")")
				out.add(category, form)
	return out
