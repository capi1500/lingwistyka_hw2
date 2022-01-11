import os.path
import psycopg2


class Context:
	def __init__(self, path, args):
		self.args = args
		self.path = path
		assert os.path.exists(path), "path '" + path + "' does not exist"
		self.model = args.compare
		if self.model != "":
			assert os.path.exists(self.model), "path '" + path + "' does not exist"
			assert os.path.isfile(self.model), "path '" + path + "' is not a file"
		self.con = psycopg2.connect(
			host="localhost",
			database="postgres",
			user="postgres",
			password="x"
		)
		self.db = self.con.cursor()

	def __del__(self):
		self.db.close()
		self.con.close()
