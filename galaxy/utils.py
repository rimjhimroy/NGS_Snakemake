'''
Containing functions are called from Galaxy to populate lists/checkboxes with selectable items
'''
import csv
import glob
import os


__author__ = "Marcel Kempenaar"
__contact__ = "brs@nbic.nl"
__copyright__ = "Copyright, 2012, Netherlands Bioinformatics Centre"
__license__ = "MIT"

def get_column_type(library_file):
    '''
    Returns a Galaxy formatted list of tuples containing all possibilities for the
    GC-column types. Used by the library_lookup.xml tool
    @param library_file: given library file from which the list of GC-column types is extracted
    '''
    if library_file == "":
        galaxy_output = [("", "", False)]
    else:
        (data, header) = read_library(library_file)
    
        if 'columntype' not in header:
            raise IOError('Missing columns in ', library_file)
    
        # Filter data on column type
        column_type = header.index("columntype")
        amounts_in_list_dict = count_occurrence([row[column_type] for row in data])
        galaxy_output = [(str(a) + "(" + str(b) + ")", a, False) for a, b in amounts_in_list_dict.items()]
        
    return(galaxy_output)


def filter_column(library_file, column_type_name):
    '''
    Filters the Retention Index database on column type
    @param library_file: file containing the database
    @param column_type_name: column type to filter on
    '''
    if library_file == "":
        galaxy_output = [("", "", False)]
    else:
        (data, header) = read_library(library_file)
    
        if ('columntype' not in header or
            'columnphasetype' not in header):
            raise IOError('Missing columns in ', library_file)
    
        column_type = header.index("columntype")
        statphase = header.index("columnphasetype")
    
        # Filter data on colunn type name
        statphase_list = [line[statphase] for line in data if line[column_type] == column_type_name]
        amounts_in_list_dict = count_occurrence(statphase_list)
        galaxy_output = [(str(a) + "(" + str(b) + ")", a, False)for a, b in amounts_in_list_dict.items()]
        
    return(sorted(galaxy_output))


def filter_column2(library_file, column_type_name, statphase):
    '''
    Filters the Retention Index database on column type
    @param library_file: file containing the database
    @param column_type_name: column type to filter on
    @param statphase: stationary phase of the column to filter on
    '''
    if library_file == "":
        galaxy_output = [("", "", False)]
    else:
        (data, header) = read_library(library_file)
    
        if ('columntype' not in header or
            'columnphasetype' not in header or
            'columnname' not in header):
            raise IOError('Missing columns in ', library_file)
    
        column_type_column = header.index("columntype")
        statphase_column = header.index("columnphasetype")
        column_name_column = header.index("columnname")
    
        # Filter data on given column type name and stationary phase
        statphase_list = [line[column_name_column] for line in data if line[column_type_column] == column_type_name and
                          line[statphase_column] == statphase]
        amounts_in_list_dict = count_occurrence(statphase_list)
        galaxy_output = [(str(a) + "(" + str(b) + ")", a, False)for a, b in amounts_in_list_dict.items()]
        
    return(sorted(galaxy_output))


def read_library(filename):
    '''
    Reads a CSV file and returns its contents and a normalized header
    @param filename: file to read
    '''
    data = list(csv.reader(open(filename, 'rU'), delimiter='\t'))
    header_clean = [i.lower().strip().replace(".", "").replace("%", "") for i in data.pop(0)]
    return(data, header_clean)



def get_directory_files(dir_name, filterStr=None):
    '''
    Reads the directory and
    returns the list of .txt files found as a dictionary
    with file name and full path so that it can 
    fill a Galaxy drop-down combo box.
    
    '''
    files = glob.glob(dir_name + ("/*.*" if filterStr == None else "/" + filterStr))
    if len(files) == 0:
        # Configuration error: no library files found in <galaxy-home-dir>/" + dir_name :
        galaxy_output = [("Configuration error: expected file not found in <galaxy-home-dir>/" + dir_name, "", False)]
    else:
        galaxy_output = [(str(get_file_name_no_ext(file_name)), str(os.path.abspath(file_name)), False) for file_name in files]
    return(galaxy_output)
    
def get_file_name_no_ext(full_name):
    '''
    returns just the last part of the name
    '''
    simple_name = os.path.basename(full_name)
    base, ext = os.path.splitext(simple_name)
    return base
    

def count_occurrence(data_list):
    '''
    Counts occurrences in a list and returns a dict with item:occurrence
    @param data_list: list to count items from
    '''
    return dict((key, data_list.count(key)) for key in set(data_list))