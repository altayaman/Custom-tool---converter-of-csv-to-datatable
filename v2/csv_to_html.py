import pandas as pd
from IPython.display import display, HTML	
from collections import OrderedDict
from optparse import OptionParser
from pprint import pprint
from sqlalchemy import create_engine, text
from sqlalchemy.engine.reflection import Inspector
from collections import defaultdict
import sqlite3
import sys
import os
import csv
import time
import distutils

help_text = """\n  -f, --csv_file  // csv file to be imported into Postrgres
			"""
parser = OptionParser(usage=help_text)
parser.add_option("--cf", "--config_file",         dest='config_file',         help="")
parser.add_option("-f",   "--csv_file",            dest='csv_file',            help="",   default='no input')
parser.add_option("-o",   "--out_html_file",       dest='out_html_file',       help="",   default='no input')    # unnecessary
parser.add_option("-s",   "--sqlite_file_name",    dest='sqlite_file_name',    help="",   default='no input')    # unnecessary
parser.add_option("-t",   "--table_name",          dest='table_name',          help="",   default='no input')    # unnecessary
#(options, args) = parser.parse_args() 

def print_ls(ls, prefix='', index=False):
	if(index):
		for ix, i in enumerate(ls):
			#print(prefix,(ix+1),' ',i)
			print(prefix,'%-2d' % (ix+1),' ','%-22s' % i,'text')
	else:
		for i in ls:
			#print(prefix,i)
			print(prefix,' ','%-22s' % i,'text')

def print_odict(odict, prefix='', index=False):
	ls = list(odict.items())
	if(index):
		for ix, kv_pair in enumerate(ls):
			#print(prefix,(ix+1),' ',i)
			print(prefix,'%-2d' % (ix+1),' ','%-30s' % kv_pair[0],kv_pair[1])
	else:
		for i in ls:
			#print(prefix,i)
			print(prefix,' ','%-30s' % kv_pair[0],kv_pair[1])

def str_num_int_to_int(sentence_):
    printable_ = '0123456789'
    str_num_processed = "".join((char if char in printable_ else "") for char in str(sentence_).lower())
    
    if(str_num_processed in ['','0.0','.0','.']):
    	return '0'
    else:
    	return str_num_processed

def headers_to_default_types(ls):
	odict = OrderedDict();
	for i in ls:
		odict[i] = 'text'

	return odict

def qry_create_table(table_name, header_names_odict):
	qry_create_table = "CREATE TABLE IF NOT EXISTS "+table_name+" (\nid integer PRIMARY KEY,"
	qry_create_table = "CREATE TABLE "+table_name+" (\nid integer PRIMARY KEY,"
	qry_create_table = "CREATE TABLE "+table_name+" ("
								
	for i, kv in enumerate(header_names_odict.items()):
		#print(kv)
		comma = ','
		if((i+1) == len(header_names_odict)):
			comma=''
		column_name = kv[0]
		if(column_name in ['order']):
			column_name = '"'+column_name+'"'
		column_type = kv[1]
		qry_create_table = qry_create_table +'\n'+ column_name + ' ' + column_type + comma

	qry_create_table = qry_create_table+"\n); "
	return qry_create_table

def get_ranges_for_df(input_df_size_, insertion_chunk_size_):
    ranges_ = []

    c = 0
    while(True):
        if(input_df_size_ >= insertion_chunk_size_):
            input_df_size_ = input_df_size_ - insertion_chunk_size_
            range_ = (c * insertion_chunk_size_ , (c+1) * insertion_chunk_size_ - 1)
            ranges_.extend([range_])
            c = c + 1
            if(input_df_size_ == 0):
                break
        else:
            if(input_df_size_-1 < c*insertion_chunk_size_):
                range_ = (c * insertion_chunk_size_, (c*insertion_chunk_size_) + input_df_size_ - 1)
            else:
                range_ = (c * insertion_chunk_size_, input_df_size_ - 1)
            ranges_.extend([range_])
            break

    return ranges_

# Make sure that column types of dataframe to be inserted and db table name are consistent
def insert_df_into_db(df, insert_chunk_size, schema_table_name, columns_list, engine):
	from sqlalchemy import text
	conn = engine.connect()

	# get insert chunk ranges
	ranges = get_ranges_for_df(df.shape[0], insert_chunk_size)

	columns_list_=None
	if(len(columns_list)==0):
		columns_list_ = df.columns.values.tolist()
	else:
		columns_list_ = columns_list

    # get query template
	qry_template = "insert into " + schema_table_name + " (" + ','.join(columns_list_) + ") values "

	values_holder_dict = {}
	for range_ in ranges:
		qry = qry_template
        #print(range_)
		for i in range(range_[0], range_[1]+1):
			for col_name in columns_list_:
				value = df.loc[i, col_name]
				value = str(value)
				value = value.replace("'","''")   # replace special characters
				value = value.replace(":","\:")   # replace special characters
				values_holder_dict[col_name] = value

				comma = ","
				if(i == range_[0]):
					comma = ""

			values_line_ls = [values_holder_dict[col_name] for col_name in columns_list_]
			values_line_ls = ["'"+value_+"'" for value_ in values_line_ls]
			values_line_str = ','.join(values_line_ls)
			values_line_str = comma + "(" + values_line_str + ")"
			#line = comma + "('" + description + "','" + str(order) + "')"
			qry = qry + values_line_str
			#print(qry)
         
		#print('\n'+qry)   
		conn.execute(text(qry))
        
	conn.close()
	#print('\nData insertion into db is complete ...')

def second_input(inspector):
	input_ = input('Input:')
	if(input_ == ''):
		print('Program halted')
		sys.exit(0)
	elif(len(input_) > 0 and input_.replace(' ','') == ''):
		print('\nList of tables:')
		for t in inspector.get_table_names():
			print('	',t)
		
		print()
		print('Give a table name')
		print('OR PRESS [Space + Enter] to list table names')
		print('OR PRESS [Enter] to halt\n')
		return second_input(inspector)
	else:
		return input_

def check_if_table_exists(table_name, inspector):
	input_ = None
	if(table_name.lower() in inspector.get_table_names()):
		print('\nSQL Error:')
		print('Table '+table_name+' already exists\n')

		print('Give different table name')
		print('OR PRESS [Space + Enter] to list table names')
		print('OR PRESS [Enter] to halt\n')

		input_ = second_input(inspector)
		table_name = input_.replace(' ','')
		return check_if_table_exists(table_name, inspector)
	else:
		return table_name

def print_format(print_formatted_ls = [], ident_factor = 1, prefix_ls = [], postfix_ls = []):
	spaces = '  '

	if(len(prefix_ls) > 0):
		for p in prefix_ls:
			print(p)

	if(len(print_formatted_ls) == 2):
		print('%-20s' % (spaces*ident_factor + print_formatted_ls[0]), print_formatted_ls[1])
	elif(len(print_formatted_ls) == 1):
		print('%-20s' % (spaces*ident_factor + print_formatted_ls[0]))

	if(len(postfix_ls) > 0):
		for p in postfix_ls:
			print(p)



# ===================================================================================================================
if __name__ == "__main__":
	(options, args) = parser.parse_args()
	csv_file_path = options.csv_file
	csv_file = None

	# abs_path = os.path.dirname(os.path.abspath(__file__))
	
	# output_dir_path = abs_path + '/generated_html'
	# if os.path.exists(output_dir_path):
	# 	print(output_dir_path + ' already exists')
	# else:
	# 	distutils.dir_util.copy_tree(abs_path+'/css',output_dir_path)
	# 	os.makedirs(output_dir_path)

	# sys.exit(0)

	spaces = '  '
	print('='*100)
	print('File description:'.upper())
	if(csv_file_path == 'no input'):
		print('ERROR 1:')
		print('	No arguments passed')
		print('	Need to pass csv file name to be imported into Postgres')
		sys.exit(0)
	else:
		csv_file = csv_file_path.split('/')[-1:][0]
		print('%-20s' % (' '*2 + 'csv file path:'), csv_file_path)
		print('%-20s' % (' '*2 + 'csv file:'), csv_file)


	# open file
	# ---------------------------------------------------------------------------------------------------------
	infile = open(csv_file_path, encoding='utf-8-sig')
	csv_reader = csv.reader(infile)
	csv_reader = csv.DictReader(infile)

	# print col names (header names)
	# ---------------------------------------------------------------------------------------------------------
	#col_names_ls = csv_reader.fieldnames
	#col_names_odict = headers_to_default_types(col_names_ls)
	#print('Header names with default types:')
	#print_odict(col_names_odict, prefix='	', index=True)
	#print()


	# Analyze column types and print
	# ---------------------------------------------------------------------------------------------------------
	print()
	print('%-20s' % (' '*2+'Analyzing file ...'))
	col_names_ls = csv_reader.fieldnames
	col_names_odict = defaultdict(lambda:'Integer')
	for col in col_names_ls:
		col_names_odict[col]

	
	col_names_ls_temp = col_names_ls
	for row_idx, row in enumerate(csv_reader):
		col_names_ls_copy = col_names_ls_temp[:]
		if(len(col_names_ls_temp) == 0):
			break
		for i, col_ in enumerate(col_names_ls_copy):
			if(row[col_].isdigit() == False):
				#print(row)
				#print(col_, ' is Text', row[col_],'\n')
				col_names_odict[col_] = 'Text'
				col_names_ls_temp = [x for x in col_names_ls_temp if x!= col_]
	infile.close()

	print('%-20s' % (' '*4+'Rows count:'), (row_idx+1))


	print()
	print('%-20s' % (' '*4+'Column names and types:'))
	print_odict(col_names_odict, prefix='	', index=True)
	print()


	# Prompt user to indicate columns by entering their order numbers seperated by comma
	# ---------------------------------------------------------------------------------------------------------

	print('='*100)
	print('INDICATE COLUMNS TO BE INCLUDED:\n')

	cols_included = input(' '*2+'Enter column order numbers seperated by comma:  ')
	cols_included_names_ls = []
	if(cols_included == ''):
		cols_included_names_ls = col_names_ls
	else:
		cols_included = cols_included.replace(' ','')
		cols_included_idx_ls = cols_included.strip(',').split(',')
		cols_included_idx_ls = [int(x) for x in cols_included_idx_ls]

		cols_included_names_ls = [col_names_ls[ix-1] for ix in cols_included_idx_ls]

	#col_names_odict_selected = {col: col_names_odict[col] for col in cols_included_names_ls if col in col_names_odict}

	#print(cols_included_idx_ls)
	print()
	print(' '*2+'Following columns selected:')
	print(' '*2, cols_included_names_ls)
	print()
	#print_odict(col_names_odict_selected, prefix='	', index=True)


	# convert csv to html, using special html template
	# ---------------------------------------------------------------------------------------------------------
	print('Processing data from CSV file ...')
	start = time.time()


	# get html file name
	html_filename = None
	if(options.out_html_file == 'no input'):
		print('WARNING 2:')
		print('	No file name for output html is passsed')
		print('	The output html file will be called as [filled_template.html]')
		html_filename = 'filled_template.html'

		abs_path = os.path.dirname(os.path.abspath(__file__))	
		output_dir_path = abs_path + '/' + html_filename
		print()
		if os.path.exists(output_dir_path):
			print('ERROR:')
			print(output_dir_path + ' already exists')
			sys.exit(0)
	else:
		html_filename = options.out_html_file
		if('.html' not in html_filename):
			html_filename = html_filename + '.html'
		print('	The output html file will be called as ['+html_filename+']')

		abs_path = os.path.dirname(os.path.abspath(__file__))	
		output_dir_path = abs_path + '/' + html_filename
		print()
		if os.path.exists(output_dir_path):
			print('ERROR:')
			print(output_dir_path + ' already exists')
			sys.exit(0)


	# start filling template
	f = open(html_filename, 'w')

	# get html template
	with open('csv_to_html template/datatable_template.html') as html_:
		html_template = html_.read()


	# PLACE HOLDER 4 (toogle headers) ______________________________________________________________________
	html_table_header_tooglers = """
	"""
	
	col_idx_g = 0
	for col_idx, col_ in enumerate(cols_included_names_ls):
		toogle_button_template = """<input class="toggle-vis" id="toggle%g" data-column="%g" type="button" value="%s" style="background-color:#F2F4F4">"""
		toogle_button = toogle_button_template % (col_idx, col_idx, col_)
		html_table_header_tooglers = html_table_header_tooglers + "\t\t\t\t\t" + toogle_button + "\n"
		col_idx_g = col_idx

	last_aux_columns = ['TF Type', 'TF Type hid']
	for col_idx, col_ in enumerate(last_aux_columns):
		col_idx_g = col_idx_g + 1
		toogle_button_template = """<input class="toggle-vis" id="toggle%g" data-column="%g" type="button" value="%s" style="background-color:#F2F4F4">"""
		toogle_button = toogle_button_template % (col_idx_g, col_idx_g, col_)
		html_table_header_tooglers = html_table_header_tooglers + "\t\t\t\t\t" + toogle_button + "\n"

	html_template = html_template.replace('PLACE_HOLDER_4_toogle_header_buttons', html_table_header_tooglers)


	# PLACE HOLDER 5 (toogle headers) ______________________________________________________________________
	tf_type_hid_col_idx = len(cols_included_names_ls)+1;
	tf_type_hid_col_idx = str(tf_type_hid_col_idx)
	html_template = html_template.replace('PLACE_HOLDER_5_col_index', tf_type_hid_col_idx)


	# PLACE HOLDER 1 (headers) _____________________________________________________________________________
	html_table_header = """
	"""
	for col_ in cols_included_names_ls:
		html_table_header = html_table_header + "\t\t\t\t\t<th>" + col_ + "</th>\n"

	html_template = html_template.replace('PLACE_HOLDER_1_header_names',html_table_header)


	# PLACE HOLDER 2 _______________________________________________________________________________________
	last_col_indices = [len(cols_included_names_ls),len(cols_included_names_ls)+1]
	html_template = html_template.replace('PLACE_HOLDER_2_1', str(last_col_indices[0]))
	html_template = html_template.replace('PLACE_HOLDER_2_2', str(last_col_indices[1]))

	f.write(html_template)


	# place holder 3
	infile = open(csv_file_path, encoding='utf-8-sig')
	csv_reader = csv.DictReader(infile)

	placeholder_3 = """
	"""
	row_counter = 0
	data_line_values_ls = []
	for row_idx, row in enumerate(csv_reader):
		for col_ in cols_included_names_ls:
			data_line_values_ls.append("""'<a href="#" onclick="googleSearch(this);" > %s </a>'""" % row[col_].replace("'",r"\'"))

		radio_1 = """<input type="radio" name="radio_%g" value="TruePos"  onclick="find(this);" checked > TruePos  </input>""" % (row_idx+1)
		radio_2 = """<input type="radio" name="radio_%g" value="FalsePos" onclick="find(this);"         > FalsePos </input>""" % (row_idx+1)
		radio_  = "'<div>" + '<div class="rb">' + radio_1 + '</div><div class="rb">' + radio_2 + '</div>' + "</div>'"
		data_line_values_ls.append(radio_)

		dummy = """'<div id="_radio_%g"> TruePos </div>'""" % (row_idx+1)
		data_line_values_ls.append(dummy)

		#placeholder_3 = placeholder_3 + '[' + ','.join(data_line_values_ls) + '],\n'
		f.write('[' + ','.join(data_line_values_ls) + '],\n')
		data_line_values_ls = []
		row_counter = row_counter + 1
	infile.close()

	html_template_ending = """
	                ];

	    </script>
	</html>
	"""
	f.write(html_template_ending)

	#html_template = html_template.replace('PLACE_HOLDER_3_dataset', placeholder_3)

	#f.write(html_template)
	f.close()
	print('Processed',row_counter,'rows')
	print('Processing took %g s' % (time.time()-start))









