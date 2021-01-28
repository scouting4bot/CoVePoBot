
#------------------------------------------------------------------------
def ExecuteQueryInsert(table_name, chat_info, mysql):
	"""
	Executes the insert query on db.
	Is mandatory the table_name and the dictionary with chat_info.
	Returns 1 if success.
	"""

	#build query template
	columns_list = ''
	values_list = ''
	for key in chat_info.keys():
		if key is not None and chat_info.get(key) is not None:
			columns_list = columns_list+key+','
			values_list = values_list+'%('+key+')s,'

	if columns_list == '':
		print("The 'insert' query execution failed due to missing fields")
		return False, 500

	columns_list = columns_list[:-1]
	values_list = values_list[:-1]

	#Example of query:
	#INSERT INTO table_name (column1, column2) VALUES (%(column1)s, (%(column2)s);
	#INSERT INTO table_name (user_id, column2) VALUES (123456789, 'foo');
	query = 'INSERT INTO '+table_name+' ('+columns_list+') VALUES ('+values_list+');'

	print("Executing 'insert' query on db")
	result = ''
	try:
	    # Connect to DB
	    connection = mysql.connect()

	    with connection.cursor() as cursor:

	        # Execute the query
	        result = cursor.execute(query, chat_info)
	        print("Result execute = " + str(result))

	        connection.commit()

	    connection.close()

	except Exception as e:
		print("Problem inserting into db: " + str(e))

	print("Executed 'insert' query on db")
	return result


#------------------------------------------------------------------------
def ExecuteQuerySelect(table_name, chat_info, mysql):
	"""
	Executes the select query on db.
	Is mandatory the table_name and the dictionary with chat_info.
	Returns a list of results.
	"""

	#build query template
	columns2select = ''
	columns2select = chat_info.get('columns2select')
	chat_info['columns2select'] = None

	where_condition = ''
	for key in chat_info.keys():
		if key is not None and chat_info.get(key) is not None:
			where_condition = where_condition+' '+key+' = %('+key+')s AND'

	#Example of query:
	#SELECT (%(column1)s, (%(column2)s) FROM table_name WHERE column1 = %(column1)s;
	#SELECT user_id FROM table_name WHERE user_id = '1';
	query = ''
	if where_condition == '':
		query = 'SELECT '+columns2select+' FROM '+table_name+';'
	else:
		#remove last char
		where_condition = where_condition[:-3]
		query = 'SELECT '+columns2select+' FROM '+table_name+' WHERE '+where_condition+';'

	print("Executing 'select' query on db")
	result = ''
	try:
	    # Connect to DB
	    connection = mysql.connect()

	    with connection.cursor() as cursor:

	        # Execute the query
	        result = cursor.execute(query, chat_info)
	        print("Retrieved " + str(result) + " elements")

	    #fetch rows
	    rows = cursor.fetchall()
	    print("rows = " + str(rows))
	    #put the tuple of 'rows' in a list object
	    my_list = []
	    for row in rows:
	        my_list.append(row)
	    result = my_list
	    print("Result list = " + str(result))

	    connection.close()

	except Exception as e:
		print("Problem selecting into db: " + str(e))

	print("Executed 'select' query on db")
	return result

#------------------------------------------------------------------------
def ExecuteQueryUpdate(table_name, chat_info, mysql):
	"""
	Executes the update query on db.
	Is mandatory the table_name and the dictionary with chat_info.
	Returns 1 if success.
	"""

	#build query template
	where_condition = ''
	for key in chat_info.keys():
		if key is not None and key != 'nwVal' and chat_info.get(key) is not None:
			where_condition = where_condition+' '+key+' = %('+key+')s AND'

	if where_condition != '':
		where_condition = where_condition[:-3]
	
	nwVal_condition = ''
	placeholders = {};
	for key in chat_info.get('nwVal').keys():
		if key is not None and key != 'nwVal' and chat_info.get('nwVal').get(key) is not None:
			nwVal_condition = nwVal_condition+' '+key+' = %(nwVal_'+key+')s AND'
			nw_key = 'nwVal_'+key
			placeholders[nw_key] = chat_info.get('nwVal').get(key)

	if nwVal_condition != '':
		nwVal_condition = nwVal_condition[:-3]
		chat_info['nwVal']=''
		chat_info.update(placeholders)

	#Example of query:
	#UPDATE table_name SET column1 = "%(column1)s" where column1 = "%(column2)s";
	#UPDATE table_name SET column1 = "newValue" where column1 = "oldValue";
	query = 'UPDATE '+table_name+' SET ' + nwVal_condition +' WHERE '+where_condition+';'
	
	print("Executing 'update' query on db")
	result = ''
	try:
	    # Connect to DB
	    connection = mysql.connect()

	    with connection.cursor() as cursor:

	        # Execute the query
	        result = cursor.execute(query, chat_info)
	        print("Result execute = " + str(result))

	        connection.commit()

	    connection.close()

	except Exception as e:
		print("Problem updating into db: " + str(e))

	print("Executed 'update' query on db")
	return result

#------------------------------------------------------------------------
def ExecuteQueryDelete(table_name, chat_info, mysql):
	"""
	Executes the delete query on db.
	Is mandatory the table_name and the dictionary with chat_info.
	Returns 1 if success.
	"""

	#TODO
	return 1