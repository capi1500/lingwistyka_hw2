def conditional_input(text: str, alternative: str, default: bool) -> bool:
	cond = input(text)
	if cond == alternative:
		return not default
	return default


def set_to_str(s: set):
	if len(s) == 0:
		return "{}"
	return str(s)


def cmp_sets(set1: set, set2: set):
	if set1 != set2:
		print("\t\tgot: '" + set_to_str(set1) + "', expected: '" + set_to_str(set2) + "'")
