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
def plot_bar(df):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return  # Exit the function early

    #one_hot_encoded = df['target name']
    #one_hot_encoded = one_hot_encoded.str.get_dummies()
    #tech_usage_count_by_group = one_hot_encoded.sum()
    #tech_usage_count_by_group.sort_values(ascending=False, inplace=True)
    # top10grouptech = tech_usage_count_by_group.head(10)

    one_hot_encoded = df['tactics']
    one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    tactics_counts = one_hot_encoded.sum()
    # Determine the index of the largest segment
    largest_index = tactics_counts.idxmax()
    #smallest_index = tactics_counts.idxmin()

    # Create the pull array
    pull = [0.1 if tactic == largest_index else 0 for tactic in tactics_counts.index]

    fig = px.pie(
        df,
        values=tactics_counts.values,
        names=tactics_counts.index,
        title='Pie Chart',
    )
    # fig = px.bar(df, x=tactics_counts.index, y=tactics_counts.values, color=tactics_counts.values, title="Bar chart of Most used Techniques by Groups",
        #labels={
            #'x': 'Techniques Name',
            #'y': 'Number of Groups (out of ...)'
        #})
    fig = px.pie(df, values=tactics_counts.values, names=tactics_counts.index, title='Pie Chart', )
    fig.update_traces(pull=pull)
    #fig.update_traces(
    #    hovertemplate='%{label}: %{percent:.1%}<extra></extra>',  # Custom hover text
    #    hoverlabel=dict(
    #        font=dict(size=16),  # Change the font size
    #        bgcolor="white",  # Background color of the hover label
    #        bordercolor="black"  # Border color of the hover label
    #    )
    #)

    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig, use_container_width=True)

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

    software_use_tech_df = software_use_tech_df.merge(technique_table, left_on='target ID', right_on='ID')
    software_use_tech_df.drop(['name', 'ID', 'name', 'mapping description', 'source type', 'target type', 'mapping type'], axis=1, inplace=True)

    # merge
    group_use_tech_df = group_use_tech_df.merge(technique_table, left_on='target ID', right_on='ID')
    group_use_tech_df.drop(['name', 'ID', 'domain', 'mapping type', 'target type', 'source type', 'mapping description'], axis=1, inplace=True)

    #one_hot_encoded = software_use_tech_df['platforms']
    #one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    #platform_counts = one_hot_encoded.sum()

    plot_bar(group_use_tech_df)

    #st.plotly_chart(fig)

    # plot_scatter(df, selected_species, x_feature, y_feature)

if __name__ == "__main__":
    main()
