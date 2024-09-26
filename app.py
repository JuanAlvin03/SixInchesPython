import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
def load_data():
    dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
    dataset = pd.read_excel(dataset_path, sheet_name="relationships")  # relationships is sheet name, header true
    return dataset

# Not used yet
def plot_scatter(df, selected_species, x_feature, y_feature):
    if selected_species:
        filtered_df = df[df['species'].isin(selected_species)]
    else:
        filtered_df = df

    fig = px.scatter(filtered_df, x=x_feature, y=y_feature, color="species", title="Scatter Plot of Iris Dataset")

    st.plotly_chart(fig)

def main():
    dataset = load_data()
    st.title('MITRE ATT&CK')

    #species_options = df['species'].unique().tolist()
    #default_species = species_options
    #selected_species = st.multiselect('Select Species', options=species_options, default=default_species)

    # Use all feature columns for the selectbox
    # x_feature = st.selectbox('Select X-axis Feature', options=df.columns[:-1], index=0)  # Exclude 'species'
    # y_feature = st.selectbox('Select Y-axis Feature', options=df.columns[:-1], index=1)  # Exclude 'species'

    dataset.drop(['created', 'last modified', 'STIX ID'], axis=1, inplace=True)
    # dataset.head()

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

    one_hot_encoded = group_use_software_df['target name']
    one_hot_encoded = one_hot_encoded.str.get_dummies()
    software_usage_count_by_groups = one_hot_encoded.sum()
    software_usage_count_by_groups.sort_values(ascending=False, inplace=True)

    top10 = software_usage_count_by_groups.head(10)
    # this means 'Mimikatz' software is used by 46 out of 136 groups

    fig = px.bar(top10, x=top10.index, y=top10.values, color=top10.values, title="Mitre Att&ck")

    st.plotly_chart(fig)

    #plot_scatter(df, selected_species, x_feature, y_feature)

if __name__ == "__main__":
    main()
