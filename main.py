import argparse

from modules.context import Context
from modules.process_file import compare, validate


def main():
	parser = argparse.ArgumentParser(description='Options')
	parser.add_argument("-i", "--interactive", action="store_true", help="interactive mode", default=False)
	parser.add_argument("-e", "--edit", action="store_true", help="mode that allows for changes in the database", default=False)
	parser.add_argument("-c", "--compare", type=str, help="comapre input file to model answer", default="")
	parser.add_argument("--errors_only", action="store_true", help="output only errors", default=False)
	parser.add_argument("input", help="file to check")
	args = parser.parse_args()

	context = Context(args.input, args)
	if args.compare:
		compare(context)
	else:
		validate(context)


if __name__ == "__main__":
	main()
