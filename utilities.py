def country_codes_with_world():
	stmt = db.session.query(Country_Continent).statement
	df = pd.read_sql_query(stmt, db.session.bind)

	list_of_country_codes = df.iloc[:, 3]

	# Add 900 to the codes
	list_of_country_codes.index += 1
	country_code_df = list_of_country_codes.to_frame()
	country_code_df = pd.DataFrame(np.insert(country_code_df.values, 0, values=[900], axis=0))
	country_code_df.columns = ['country_code']
	return country_code_df


def country_codes_without_world():
	stmt = db.session.query(Country_Continent).statement
	df = pd.read_sql_query(stmt, db.session.bind)

	list_of_country_codes = df.iloc[:, 3]
	country_code_df = list_of_country_codes.to_frame()
	country_code_df.columns = ['country_code']
	return country_code_df


