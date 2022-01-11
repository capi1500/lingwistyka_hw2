import argparse
import os.path

from modules.context import Context
from modules.line import process_line


def validate_file(context, path):
	print("Validate file:", path)
	try:
		with open(path, encoding="utf-8") as f:
			for line in f:
				line = line.rstrip("\n")
				process_line(line, context)
	except BaseException as err:
		print(f"Exception: {type(err)=}")


def validate(context):
	if os.path.isfile(context.path):
		validate_file(context, context.path)
	else:
		for file in os.listdir(context.path):
			validate_file(context, os.path.join(context.path, file))


def compare_file(context, path):
	print("Compare files:", path, context.model)
	try:
		with open(path, encoding="utf-8") as f:
			with open(context.model, encoding="utf-8") as model:
				line_no = 0
				for line1 in f:
					line1 = line1.rstrip("\n")
					out1 = process_line(line1, context)
					if out1 is None:
						continue
					line2 = model.readline()
					line2 = line2.rstrip("\n")
					out2 = process_line(line2, context)
					if out1 != out2:
						print("Error: line", line_no, "do not match:")
						print("\tline (" + path + "):", line1)
						print("\tline (" + context.model + "):", line2)
						out1.show_diff(out2)
						input()
					line_no += 1
	except BaseException as err:
		print(f"Exception: {type(err)=}")


def compare(context):
	if os.path.isfile(context.path):
		compare_file(context, context.path)
	else:
		for file in os.listdir(context.path):
			compare_file(context, os.path.join(context.path, file))


def main():
	parser = argparse.ArgumentParser(description='Options')
	parser.add_argument("-e", "--edit", action="store_true", help="allows for database changes in interactive mode", default=False)
	parser.add_argument("-c", "--compare", type=str, help="comapre input file to model answer", default="")
	parser.add_argument("input", help="file to check")
	args = parser.parse_args()

	context = Context(args.input, args)
	if args.compare:
		compare(context)
	else:
		validate(context)


if __name__ == "__main__":
	main()
