def conditional_input(text: str, alternative: str, default: bool) -> bool:
	cond = input(text)
	if cond == alternative:
		return not default
	return default
