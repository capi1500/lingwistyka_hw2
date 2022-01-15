from modules.context import Context
from modules.utils import conditional_input, cmp_sets
import modules.database as db


class LineValue:
	def __init__(self, word):
		self.word = word
		self.clas = set()
		self.case = set()
		self.gend = set()
		self.numb = set()
		self.pers = set()
		self.degr = set()
		self.aspe = set()
		self.time = set()
		self.mood = set()

	def add(self, category: int, value: str):
		if category == 1:
			self.clas.add(value)
		elif category == 2:
			self.case.add(value)
		elif category == 3:
			self.gend.add(value)
		elif category == 4:
			self.numb.add(value)
		elif category == 5:
			self.pers.add(value)
		elif category == 6:
			self.degr.add(value)
		elif category == 7:
			self.aspe.add(value)
		elif category == 8:
			self.time.add(value)
		elif category == 9:
			self.mood.add(value)

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
			print("\t\tgot: '" + self.word + "', expected: '" + other.word + "'")
		cmp_sets(self.clas, other.clas)
		cmp_sets(self.gend, other.gend)
		cmp_sets(self.numb, other.numb)
		cmp_sets(self.pers, other.pers)
		cmp_sets(self.degr, other.degr)
		cmp_sets(self.aspe, other.aspe)
		cmp_sets(self.time, other.time)
		cmp_sets(self.mood, other.mood)
	
	def empty(self):
		return (len(self.clas) == 0 and 
	            len(self.case) == 0 and 
	            len(self.gend) == 0 and 
	            len(self.numb) == 0 and 
	            len(self.pers) == 0 and 
	            len(self.degr) == 0 and 
	            len(self.aspe) == 0 and 
	            len(self.time) == 0 and 
	            len(self.mood) == 0)
		

def process_line(line: str, context: Context, line_number: int):
	line = line.lower()
	possibly_illegal = False
	if line == "":
		if not context.args.errors_only:
			print("\tWarning (line " + str(line_number) + "): Empty line")
		return None
	if line.find(":") == -1:
		(word, gramma) = line.split(" ", 1)
		if not context.args.errors_only:
			print("\tWarning (line " + str(line_number) + "): ':' not found. Line: '" + line + "'")
			if context.args.interactive:
				if conditional_input("\t\tSkip line? (y/N) ", "y", False):
					return None
			else:
				possibly_illegal = True
		else:
			possibly_illegal = True
	else:
		(word, gramma) = line.split(":", 1)

	word = word.strip()
	if word.find(" ") != -1 and not context.args.errors_only:
		print("\tWarning (line " + str(line_number) + "): One line should describe one word only, got: '" + word + "'")

	out = LineValue(word)
	last_added_category = 0

	for value_list in gramma.split(","):
		category_id = 0
		for value in value_list.split("/"):
			value = value.strip()
			if value == "":
				if not context.args.errors_only:
					print("\tWarning (line " + str(line_number) + "): empty value. Check line for additional ',' characters.")
					continue
			(_, form, category) = db.get_default_form(context.db, value)
			if form == "":
				print("\tError (line " + str(line_number) + "): Value '" + value + "' not found in the database")
				if context.args.edit:
					if conditional_input("\t\tAdd value '" + value + "' to the database? (y/N) ", "y", False):
						ref = input("\t\tWhat should it reference?\n> ")
						while not db.value_exists(context.db, ref):
							ref = input("\t\tValue '" + "' not found. What should '" + value + "' reference?\n> ")
						db.insert_value(context.con, context.db, value, ref)
			else:
				if category_id == 0:
					category_id = category
					if category_id <= last_added_category:
						if not context.args.errors_only:
							print("\tWarning (line " + str(line_number) + "): current value (" + value + ") probably should go before previous one. Check order of categories in this line.")
					else:
						last_added_category = category_id
				elif category != category_id:
					print("\tError (line " + str(line_number) + "): previous category (" + db.get_category_str(context.db, category) + ") differs from current one (" + db.get_category_str(context.db, category_id) + ")")
				out.add(category, form)
	
	if possibly_illegal and out.empty():
		if not context.args.errors_only:
			print("\tWarning (line " + str(line_number) + "): Line probably is illegal, script is skipping it")
		return None
	
	return out
