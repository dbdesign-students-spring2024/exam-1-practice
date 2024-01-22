# write your Python code here according to the instructions

## import the csv module
import csv


def get_csv_data(filepath):
    """
    Opens the file at filepath, reads the data using the csv module's DictReader, 
    converts that data to a regular list containing a dictionary for each row of data in the CSV file
    and returns that list.

    :param filepath: The file path of the CSV data file to open
    :returns: A list of dictionaries, where each dictionary represents one row from the file
    """
    ## place your code here to complete this method according to the instructions above

def remove_rows_with_null_valued_fields(data):
    """
    Removes any rows with one or more fields set to 'NULL' (string format) from the data set.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above

def remove_rows_with_invalid_handles(data):
    """
    Removes any rows that have handles containing special (non-alphanumeric) characters such as ('$', '*', etc.). 
    Handles can only have alphabets or numbers.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above


def remove_rows_over_affinity_id_level(data, affinity_type, threshold):
    """
    Removes any rows with a value in a given affinity category id field greater than to the supplied threshold.

    :param data: The data, as a list of dictionaries
    :param affinity_type: The type of affinity category id of interest...
    :param threshold: The maximum acceptable id value for this affinity type... records with higher values will be removed.
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above


def replace_email_domain(data, old_domain, new_domain):
    """
    Updates any rows where the 'email' ends in the old domain.  Updates to the new domain.

    :param data: The data, as a list of dictionaries
    :param old_domain: The old domain to remove, e.g. '@dmoz.org'
    :param new_domain: The new domain to replace the old_domain with, e.g. '@dmoz.com'
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above

def save_csv_data(data, filepath):
    """
    Saves the data into the specified file.  Include the field headers as the first row.

    :param data: The data, as a list of dictionaries
    :param filepath: The file path of the CSV data file to save to
    """
    ## place your code here to complete this method according to the instructions above


def get_average_and_median_affinity_id(data, affinity_type):
    """
    Calculates the average and median number of the affinity category id of all records in the data set.

    :param data: The data, as a list of dictionaries
    :param affinity_type: The type of affinity category id of interest...
    :returns: The average and median number of affinity id for the given affinity_type (both are of type float) in the order << average, median >>
    """
    ## place your code here to complete this method according to the instructions above



#################################################
## Do not modify the code below this line      ##
## except to comment out any function calls    ##
## that you do not wish to test at the moment  ##
#################################################

def main():
    ## use the functions defined above to complete munging of the data file

    # get the data from the file
    data = get_csv_data('data/users.csv')

    # munge it
    data = remove_rows_with_null_valued_fields(data)
    data = remove_rows_with_invalid_handles(data)
    data = remove_rows_over_affinity_id_level(data, 'tech_gadget_affinity_category_id', 10)
    data = replace_email_domain(data, '@dmoz.org', '@dmoz.com')
    # save to the new csv file
    save_csv_data(data, 'data/users_clean.csv')

    # print the average and median affinity level for real food
    avg, median = get_average_and_median_affinity_id(data, 'tech_gadget_affinity_category_id')
    print('The average affinity id for tech gadget is: {}.'.format(avg))
    print('The median affinity id for tech gadget is: {}.'.format(median))

if __name__ == "__main__":
    main()
