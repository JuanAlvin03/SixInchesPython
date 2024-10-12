import pandas as pd
from loaddata import load_group_data, load_software_data, load_technique_data, load_relationship_data

def test_load_group_data():
    df = load_group_data()
    assert isinstance(df, pd.DataFrame), "The loaded data should be a pandas DataFrame"
    # Check actual column names
    expected_columns = ['ID', 'name', 'domain', 'associated groups']
    assert all(col in df.columns for col in expected_columns), "The DataFrame is missing required columns"

def test_load_software_data():
    df = load_software_data()
    assert isinstance(df, pd.DataFrame), "The loaded data should be a pandas DataFrame"
    # Check actual column names
    expected_columns = ['ID', 'name', 'domain', 'platforms', 'aliases', 'type']
    assert all(col in df.columns for col in expected_columns), "The DataFrame is missing required columns"
    assert not df.empty, "The software data should not be empty"

# Test loading techniques data
def test_load_technique_data():
    df = load_technique_data()
    assert isinstance(df, pd.DataFrame), "The loaded data should be a pandas DataFrame"
    # Validate that important columns are present
    expected_columns = ['ID', 'name', 'domain', 'tactics', 'detection', 'platforms', 'data sources']
    assert all(col in df.columns for col in expected_columns), "The DataFrame is missing required columns"

# Test loading relationships data
def test_load_relationship_data():
    df = load_relationship_data()
    assert isinstance(df, pd.DataFrame), "The loaded data should be a pandas DataFrame"
    # Validate that important columns are present
    expected_columns = ['source ID', 'source name', 'source ref', 'source type', 'mapping type', 'target ID', 'target name', 'target ref', 'target type', 'mapping description']
    assert all(col in df.columns for col in expected_columns), "The DataFrame is missing required columns"


