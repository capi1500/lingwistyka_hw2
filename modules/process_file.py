import os.path
from modules.line import process_line


def validate_file(context, path):
	print("Validate file:", path)
	try:
		with open(path, encoding="utf-8") as f:
			line_number = 0
			for line in f:
				line_number += 1
				line = line.rstrip("\n")
				process_line(line, context, line_number)
	except BaseException as err:
		print(f"Exception: {type(err)=}")


def validate(context):
	if os.path.isfile(context.path):
		validate_file(context, context.path)
	else:
		for file in os.listdir(context.path):
			validate_file(context, os.path.join(context.path, file))
			if context.args.interactive:
				input()


def compare_file(context, path):
	print("Compare files:", path, context.model)
	try:
		with open(path, encoding="utf-8") as f:
			with open(context.model, encoding="utf-8") as model:
				line_no1 = 1
				line_no2 = 1
				while True:
					line1 = None
					line2 = None
					out1 = None
					out2 = None
					while True:
						line1 = f.readline()
						line_no1 += 1
						if not line1:
							break
						line1 = line1.rstrip("\n")
						out1 = process_line(line1, context, line_no1)
						if out1 is not None:
							break
					while True:
						line2 = model.readline()
						line_no2 += 1
						if not line2:
							break
						line2 = line2.rstrip("\n")
						out2 = process_line(line2, context, line_no2)
						if out2 is not None:
							break
					if not line1 or not line2:
						if line1:
							print("\tWarning: trailing lines in file: '" + path + "'")
						elif line2:
							print("\tWarning: trailing lines in file: '" + context.model + "'")
						break

					if out1 != out2:
						print("\tError: lines do not match:")
						print("\t" + path + ", line " + str(line_no1) + ":", line1)
						print("\t" + context.model + ", line " + str(line_no2) + ":", line2)
						out1.show_diff(out2)
						if context.args.interactive:
							input()
	except BaseException as err:
		print(f"Exception: {type(err)=}")


def compare(context):
	if os.path.isfile(context.path):
		compare_file(context, context.path)
	else:
		for file in os.listdir(context.path):
			compare_file(context, os.path.join(context.path, file))
			if context.args.interactive:
				input()
