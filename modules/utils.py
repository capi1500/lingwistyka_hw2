# Print [text] and wait for input. If input equals [alternative], return [not default]. Return [default] otherwise
def conditional_input(text: str, alternative: str, default: bool) -> bool:
	cond = input(text)
	if cond == alternative:
		return not default
	return default


# Changes how empty set is printed from "set()" to "{}"
def set_to_str(s: set):
	if len(s) == 0:
		return "{}"
	return str(s)
