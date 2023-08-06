
from datetime import date, timedelta


def parse_date(date_str):
	if date_str is None:
		return date_str

	if type(date_str) == date:
		return date_str

	assert type(date_str) == str
	assert len(date_str) == 10

	y = int(date_str[:4])
	m = int(date_str[5:7])
	d = int(date_str[-2:])
	return date(y, m, d)


def iter_date(start_date, end_date):
	start_date = parse_date(start_date)
	end_date = parse_date(end_date)

	assert start_date and end_date
	assert start_date <= end_date

	dt = start_date
	while dt <= end_date:
		yield dt
		dt += timedelta(days=1)
