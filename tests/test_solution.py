import os
import csv
import random
import pytest
import pandas as pd
from solution import *

random.seed(45)

def remove_null_records(expected_users_data):
  '''
  Remove records with null values
  '''
  expected_users_data_non_null = list()
  for record in expected_users_data:
    flag = False
    for value in record.values():
      if value == "NULL":
        flag = True
        break
    if not flag:
      expected_users_data_non_null.append(record)
  return expected_users_data_non_null

def remove_invalid_handles(expected_users_data):
  '''
  Remove records with invalid handles
  '''
  data_valid_handles = []
  for record in expected_users_data:
    if record['handle'].isalnum():
      data_valid_handles.append(record)
  return data_valid_handles


users_data_filepath = os.path.join(os.getcwd(), "data/users.csv")
expected_users_df = pd.read_csv(users_data_filepath)
# expected_users_df_non_null = expected_users_df.dropna()

expected_users_data = list(csv.DictReader(open(users_data_filepath, "r")))
expected_users_data_non_null = remove_null_records(expected_users_data)
expected_users_df_non_null = pd.DataFrame(expected_users_data_non_null)

@pytest.fixture
def state():
  '''
  A test fixture that picks a random state.
  '''
  return random.choice(expected_users_df["state"].unique())

@pytest.fixture
def affinity_type():
  '''
  A test fixture that picks a random affinity type column name.
  '''
  affinity_columns = [x for x in expected_users_df.columns if 'affinity' in x]
  return random.choice(affinity_columns)

@pytest.fixture
def old_domain():
  '''
  A test fixture with the old domain that should be replaced.
  '''
  return "@dmoz.org"

@pytest.fixture
def new_domain():
  '''
  A test fixture with the new domain that the old domain should be replaced with.
  '''
  return "@dmoz.com"

@pytest.fixture
def save_path():
  '''
  A test fixture with the path to the file where the data munging results should be saved.
  '''
  return os.path.join(os.getcwd(), "data/users_clean.csv")

### tests

class Tests:

  def test_get_csv_data_shape(self):
    '''
    Test the get_csv_data() function.
    '''
    actual_users_data = get_csv_data(users_data_filepath)
    assert actual_users_data != None, f"Expected get_csv_data() to return a list of dictionaries; instead, it returned None."
    assert len(actual_users_data) == expected_users_df.shape[0], f'Expected get_csv_data() to return a list with {expected_users_df.shape[0]} dictionaries; instead it returned a list with {len(actual_users_data)}.'
    assert all([len(x) == expected_users_df.shape[1] for x in actual_users_data]), f'Expected each dictionary returned by get_csv_data() to have {expected_users_df.shape[1]} values; this was not the case.'

  def test_remove_rows_with_null_valued_fields_shape(self):
    '''
    Test the remove_rows_with_null_valued_fields() function.
    '''
    returned_data = remove_rows_with_null_valued_fields(expected_users_data.copy())
    true_num_fields = len(expected_users_data[0])
    assert returned_data != None, f"Expected remove_rows_with_null_valued_fields() to return a list of dictionaries; instead, it returned None."
    assert len(returned_data) == len(expected_users_data_non_null), f'Expected remove_rows_with_null_valued_fields() to return a list with {len(expected_users_data_non_null)} dictionaries; instead it returned a list with {len(returned_data)}.'
    assert all([len(x) == true_num_fields for x in returned_data]), f'Expected each dictionary returned by remove_rows_with_null_valued_fields() to have {true_num_fields} values; this was not the case.'

  def test_remove_rows_with_null_valued_fields_value(self):
    '''
    Test the remove_rows_with_null_valued_fields() function.
    '''
    returned_data = remove_rows_with_null_valued_fields(expected_users_data.copy())
    assert returned_data != None
    count = 0
    for record in returned_data:
      for value in record.values():
        if value == 'NULL':
          count += 1
    assert count == 0, f'Expected remove_rows_with_null_valued_fields() to remove all records with null values; Instead, {count} NULL values were found.'

  def test_remove_rows_with_invalid_handles_shape(self):
    '''
    Test the shape of the results of the remove_rows_with_invalid_handles() function.
    '''
    returned_data = remove_rows_with_invalid_handles(expected_users_data.copy())
    true_data = remove_invalid_handles(expected_users_data.copy())
    check_len = len(true_data[0])
    assert returned_data != None, f"Expected remove_rows_with_invalid_handles() to return a list of dictionaries; instead, it returned None."
    assert len(returned_data) == len(true_data), f'Expected remove_rows_with_invalid_handles() to return a list with {len(true_data)} dictionaries; instead it returned a list with {len(returned_data)}.'
    assert all([len(x) == check_len for x in returned_data]), f'Expected each dictionary returned by remove_rows_with_invalid_handles() to have {check_len} values; this was not the case.'

  def test_remove_rows_with_invalid_handles_value(self):
    '''
    Test the values of the results of the remove_rows_with_invalid_handles() function.
    '''
    returned_data = remove_rows_with_invalid_handles(expected_users_data.copy())
    true_data = remove_invalid_handles(expected_users_data.copy())
    assert returned_data != None, f"Expected remove_rows_with_invalid_handles() to return a list of dictionaries; instead, it returned None."
    assert len(returned_data) == len(true_data), f'Expected remove_rows_with_invalid_handles() to return a list with {len(true_data)} dictionaries; instead it returned a list with {len(returned_data)}.'
    assert returned_data == true_data, f'Expected all rows with invalid handles to be removed by the remove_rows_with_invalid_handles() function; this was not the case.'
    count = 0
    for record in returned_data:
      if not record['handle'].isalnum():
        count += 1
      
    assert count == 0, f'Expected remove_rows_with_invalid_handles() to remove all records with invalid handles; Instead, {count} invalid handles were found.'

  def test_remove_rows_under_affinity_id_level_shape(self, affinity_type):
    '''
    Test the shape of the results of the remove_rows_under_affinity_id_level() function.
    '''
    threshold = int(random.choice(expected_users_df_non_null[~expected_users_df_non_null[affinity_type].isnull()][affinity_type].unique()))
    actual_users_data_removed_affinity_threshold = remove_rows_over_affinity_id_level(expected_users_data_non_null.copy(), affinity_type, threshold)
    expected_users_df_non_null[affinity_type] = expected_users_df_non_null[affinity_type].astype(int)
    expected_users_df_removed_affinity_threshold = expected_users_df_non_null[expected_users_df_non_null[affinity_type] <= threshold]

    assert actual_users_data_removed_affinity_threshold != None, f"Expected remove_rows_over_affinity_id_level() to return a list of dictionaries; instead, it returned None."
    assert len(actual_users_data_removed_affinity_threshold) == expected_users_df_removed_affinity_threshold.shape[0], f'Expected remove_rows_over_affinity_id_level() to return a list with {expected_users_df_removed_affinity_threshold.shape[0]} dictionaries; instead it returned a list with {len(actual_users_data_removed_affinity_threshold)}.'
    assert all([len(x) == expected_users_df_removed_affinity_threshold.shape[1] for x in actual_users_data_removed_affinity_threshold]), f'Expected each dictionary returned by remove_rows_over_affinity_id_level() to have {expected_users_df_removed_affinity_threshold.shape[1]} values; this was not the case.'

  def test_remove_rows_over_affinity_id_level_value(self, affinity_type):
    '''
    Test the values of the results of the remove_rows_over_affinity_id_level() function.
    '''
    threshold = int(random.choice(
      expected_users_df_non_null[~expected_users_df_non_null[affinity_type].isnull()][affinity_type].unique()))
    returned_data = remove_rows_over_affinity_id_level(expected_users_data_non_null.copy(), affinity_type, threshold)

    count = 0
    for record in returned_data:
      if int(record[affinity_type]) > threshold:
        count += 1
    assert returned_data != None, f"Expected remove_rows_over_affinity_id_level() to return a list of dictionaries; instead, it returned None."
    assert count == 0, f'Expected remove_rows_over_affinity_id_level() to remove all records with affinity_id values greater than {threshold}; Instead, {count} records with affinity_id values greater than {threshold} were found.'

  def test_replace_email_domain_shape(self, old_domain, new_domain):
    '''
    Test the shape of the results of the replace_email_domain() function.
    '''
    actual_users_data_replaced_email = replace_email_domain(expected_users_data_non_null.copy(), old_domain, new_domain)
    expected_users_df_non_null["email"] = expected_users_df_non_null["email"].str.replace(old_domain, new_domain)

    assert actual_users_data_replaced_email != None, f"Expected replace_email_domain() to return a list of dictionaries; instead, it returned None."
    assert len(actual_users_data_replaced_email) == expected_users_df_non_null.shape[0], f'Expected replace_email_domain() to return a list with {expected_users_df_non_null.shape[0]} dictionaries; instead it returned a list with {len(actual_users_data_replaced_email)}.'
    assert all([len(x) == expected_users_df_non_null.shape[1] for x in actual_users_data_replaced_email]), f'Expected each dictionary returned by replace_email_domain() to have {expected_users_df_non_null.shape[1]} values; this was not the case.'

  def test_replace_email_domain_value(self, old_domain, new_domain):
    '''
    Test the values of the results of the replace_email_domain() function.
    '''
    actual_users_data_replaced_email = replace_email_domain(expected_users_data_non_null.copy(), old_domain, new_domain)

    count = 0
    for record in actual_users_data_replaced_email:
      if old_domain in record["email"]:
        count += 1
    assert actual_users_data_replaced_email != None, f'Expected replace_email_domain() to return a list of dictionaries; instead, it returned None.'
    assert count == 0, f'Expected replace_email_domain() to replace all "{old_domain}" domains with "{new_domain}"; Instead, {count} email domains were not replaced.'

  def test_save_csv_data(self, save_path):
    '''
    Test the save_csv_data() function.
    '''
    assert os.path.exists(save_path), f'Expected save_csv_data() to save a file at {save_path}; instead, no file was found.'
    assert os.stat(save_path).st_size > 100, f'Expected save_csv_data() to save a file at {save_path} with more than 100 bytes; instead, the file was empty.'

  def test_get_average_and_median_affinity_id(self, affinity_type):
    '''
    Test the results of the get_average_and_median_affinity_id() function.
    '''
    returned_average, returned_median = get_average_and_median_affinity_id(expected_users_data_non_null.copy(), affinity_type)
    expected_users_df_non_null[affinity_type] = expected_users_df_non_null[affinity_type].astype(int)
    expected_affinity_average = expected_users_df_non_null[affinity_type].mean()
    expected_affinity_median = expected_users_df_non_null[affinity_type].median()
    assert returned_average != None, f'Expected get_average_and_median_affinity_id() to return the average of a particular affinity; instead, it returned "{returned_average}" for affinity type "{affinity_type}".'
    assert returned_median != None, f'Expected get_average_and_median_affinity_id() to return the median of a particular affinity; instead, it returned , {returned_median} for affinity type "{affinity_type}".'
    assert abs(returned_average - expected_affinity_average) < 10**-2, f'Expected get_average_and_median_affinity_id() to return the average of a particular affinity, within 10^-2 error; this was not the case.'
    assert returned_median == expected_affinity_median, f'Expected get_average_and_median_affinity_id() to return the median of a particular affinity; this was not the case.'
