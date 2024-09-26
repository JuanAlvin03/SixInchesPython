import streamlit as st
import pandas as pd
import plotly.express as px

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
def plot_bar(df, selected_type, selected_platform):
    if selected_type:
        #filtered_df = df[df['type'].isin(selected_type)]
        #pattern = '|'.join(selected_type)
        #filtered_df = df[df['type'].str.contains(pattern, na=False)]
        filtered_df = df[df['type'].str.contains(selected_type, na=False)]
    else:
        filtered_df = df

    if selected_platform:
        #filtered_df = filtered_df[filtered_df['platforms'].isin(selected_platform)]
        #pattern = '|'.join(selected_platform)
        #filtered_df = filtered_df[filtered_df['platforms'].str.contains(pattern, na=False)]
        filtered_df = filtered_df[filtered_df['platforms'].str.contains(selected_platform, na=False)]
    else:
        filtered_df = filtered_df

    one_hot_encoded = filtered_df['target name']
    one_hot_encoded = one_hot_encoded.str.get_dummies()
    software_usage_count_by_groups = one_hot_encoded.sum()
    software_usage_count_by_groups.sort_values(ascending=False, inplace=True)

    top10 = software_usage_count_by_groups.head(10)
    # this means 'Mimikatz' software is used by 46 out of 136 groups

    fig = px.bar(filtered_df, x=top10.index, y=top10.values, color=top10.values, title="Bar chart of Most used Softwares by Adversary Groups")

    st.plotly_chart(fig)

def main():
    dataset = load_relationship_data()
    st.title('MITRE ATT&CK')

    #species_options = dataset['species'].unique().tolist()
    #default_species = species_options
    #selected_species = st.multiselect('Select Species', options=species_options, default=default_species)

    # Use all feature columns for the selectbox
    # x_feature = st.selectbox('Select X-axis Feature', options=df.columns[:-1], index=0)  # Exclude 'species'
    # y_feature = st.selectbox('Select Y-axis Feature', options=df.columns[:-1], index=1)  # Exclude 'species'

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

    software_table = load_software_data()
    # merge
    # group_use_software_df = group_use_software_df.merge(group_table, left_on='source ID', right_on='ID')
    # group_use_software_df.drop(['name', 'ID', 'domain', 'mapping description'], axis=1, inplace=True)
    group_use_software_df = group_use_software_df.merge(software_table, left_on='target ID', right_on='ID')
    group_use_software_df.drop(['name', 'ID', 'domain'], axis=1, inplace=True)

    type_options = group_use_software_df['type'].unique().tolist()
    #default_type = ""
    selected_type = st.selectbox('Select Type', options=type_options, index=None,
    placeholder="Select Type...",)

    one_hot_encoded = group_use_software_df['platforms']
    one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    #platform_counts = one_hot_encoded.sum()

    platforms_options = one_hot_encoded.columns.tolist()
    #default_platform = ""
    selected_platform = st.selectbox('Select Platform', options=platforms_options, index=None,
    placeholder="Select Platforms...",)

    plot_bar(group_use_software_df, selected_type, selected_platform)

    #fig = px.bar(top10, x=top10.index, y=top10.values, color=top10.values, title="Mitre Att&ck")
    #st.plotly_chart(fig)

    # try to show which one is malware/tools
    # maybe platforms too
    # plot_scatter(df, selected_species, x_feature, y_feature)

if __name__ == "__main__":
    main()
