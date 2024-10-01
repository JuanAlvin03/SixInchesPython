import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib.pyplot import xlabel, ylabel


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
    relationship_table = pd.read_excel(dataset_path, sheet_name="relationships")  # relationships are sheet name, header true
    relationship_table.drop(['created', 'last modified', 'STIX ID'], axis=1, inplace=True)
    return relationship_table


#
def plot_scatter(df):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return  # Exit the function early

    one_hot_encoded = df['target name']
    one_hot_encoded = one_hot_encoded.str.get_dummies()
    software_usage_count_by_groups = one_hot_encoded.sum()
    software_usage_count_by_groups.sort_values(ascending=False, inplace=True)


    fig = px.bar(df, x="top10.index", y={"top10.values"}, color="top10.values", title="Bar chart of Most used Softwares by Adversary Groups",
        labels={
            'x': 'Software Name',
            'y': 'Number of Groups (out of 136)'
        })

    st.plotly_chart(fig)

def main():
    dataset = load_relationship_data()
    st.title('MITRE ATT&CK')

    # filter data that has 'uses' as value of 'mapping type'
    uses_df = dataset[dataset['mapping type'] == 'uses']

    # filter data uses_df that has 'group' as value of 'source type'
    group_use = uses_df[uses_df['source type'] == 'group']

    # filter group_use that has 'software' as value of 'target type'
    # this will be "what software are used by certain groups"
    group_use_software_df = group_use[group_use['target type'] == 'software']

    # filter group_use that has 'technique' as value of 'target type'
    # this will be "what techniques are used by certain groups"
    group_use_tech_df = group_use[group_use['target type'] == 'technique']

    # filter uses_df to see what techniques are used by a certain software
    software_use_tech_df = uses_df[uses_df['source type'] == 'software']

    #==============================================================================

    technique_table = load_technique_data()

    # merge
    software_use_tech_df = software_use_tech_df.merge(technique_table, left_on='target ID', right_on='ID')
    software_use_tech_df.drop(['name', 'ID', 'domain'], axis=1, inplace=True)

    one_hot_encoded = software_use_tech_df['platforms']
    one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    #platform_counts = one_hot_encoded.sum()


    plot_scatter(software_use_tech_df)

    #st.plotly_chart(fig)

    # plot_scatter(df, selected_species, x_feature, y_feature)

if __name__ == "__main__":
    main()
