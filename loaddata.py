import pandas as pd

# Load Group Table
def load_group_data():
    dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
    group_table = pd.read_excel(dataset_path, sheet_name="groups")
    group_table.drop(
        ['created', 'last modified', 'STIX ID', 'url', 'version', 'contributors', 'associated groups citations',
         'relationship citations', 'description'], axis=1, inplace=True)
    return group_table

# Load Software Table
def load_software_data():
    dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
    software_table = pd.read_excel(dataset_path, sheet_name="software")
    software_table.drop(
        ['created', 'last modified', 'STIX ID', 'url', 'version', 'contributors', 'relationship citations',
         'description'], axis=1, inplace=True)
    return software_table

# Load Techniques Data
def load_technique_data():
    dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
    techniques_table = pd.read_excel(dataset_path, sheet_name="techniques")
    techniques_table.drop(
        ['created', 'last modified', 'STIX ID', 'url', 'version', 'contributors', 'relationship citations',
         'description'], axis=1, inplace=True)
    return techniques_table

# Load Relationship Data
def load_relationship_data():
    dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
    relationship_table = pd.read_excel(dataset_path, sheet_name="relationships")
    relationship_table.drop(['created', 'last modified', 'STIX ID'], axis=1, inplace=True)
    return relationship_table
