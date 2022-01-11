def get_from_alternative(db, value: str) -> (int, str, str):
	db.execute(
		"""
		select v.*
			from Value v join AlternativeValue a
				on v.id = a.same_as
			where a.form = %s;
		""", [value]
	)
	res = db.fetchall()
	if not res:
		return 0, "", ""
	(out,) = res
	return out


def get_from_value(db, value: str) -> (int, str, str):
	db.execute(
		"""
		select * from Value v where form = %s;
		""", [value]
	)
	res = db.fetchall()
	if not res:
		return 0, "", ""
	(out,) = res
	return out


def get_default_form(db, value: str) -> (int, str, str):
	(value_id, form, category) = get_from_value(db, value)
	if value_id == 0:
		return get_from_alternative(db, value)
	return value_id, form, category


def value_exists(db, value: str):
	return get_default_form(db, value) != (0, "", "")


def insert_value(con, db, value: str, ref: str):
	(ref_id, _, _) = get_default_form(db, ref)
	db.execute(
		"""
		insert into AlternativeValue(form, same_as) 
		values (%s, %s);
		""", [value, ref_id]
	)
	con.commit()


def get_category_id(db, category: str) -> int:
	db.execute(
		"""
		select id from category where name = %s
		""", [category]
	)
	(out,) = db.fetchall()
	return out
