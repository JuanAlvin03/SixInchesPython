import streamlit as st
import plotly.express as px
import pandas as pd
from loaddata import load_group_data, load_software_data, load_technique_data, load_relationship_data

# First plot function (Pie chart for tactics)
def plot_pie(df):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    one_hot_encoded = df['tactics']
    one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    tactics_counts = one_hot_encoded.sum()

    largest_index = tactics_counts.idxmax()
    pull = [0.1 if tactic == largest_index else 0 for tactic in tactics_counts.index]

    fig = px.pie(
        values=tactics_counts.values,
        names=tactics_counts.index,
        title='Which Tactics Are Most Frequently Used by Adversary Groups?',
    )
    fig.update_traces(pull=pull)
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig, use_container_width=True)

# Second plot function (Bar chart for software usage)
def plot_bar(df, selected_type=None, selected_platform=None, num_bars=10):
    if selected_type:
        filtered_df = df[df['type'].str.contains(selected_type, na=False)]
    else:
        filtered_df = df

    if selected_platform:
        filtered_df = filtered_df[filtered_df['platforms'].str.contains(selected_platform, na=False)]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return

    one_hot_encoded = filtered_df['target name']
    one_hot_encoded = one_hot_encoded.str.get_dummies()
    software_usage_count_by_groups = one_hot_encoded.sum()
    software_usage_count_by_groups.sort_values(ascending=False, inplace=True)

    # Limit to the specified number of top bars
    top_n = software_usage_count_by_groups.head(num_bars)

    if top_n.empty:
        st.warning("No software usage data found for the selected filters.")
        return

    top_n_df = pd.DataFrame({
        'Software Name': top_n.index,
        'Number of Groups': top_n.values
    })

    # Get group information for each software
    group_info_dict = filtered_df.groupby('target name')['source name'].apply(list).to_dict()
    #top10_df['Groups'] = top10_df['Software Name'].map(lambda x: ', '.join(group_info_dict.get(x, []))) show all groups
    top_n_df['Groups'] = top_n_df['Software Name'].map(lambda x: ', '.join(group_info_dict.get(x, [])[:5]))

    # Create the bar chart
    fig = px.bar(
        top_n_df,
        x='Software Name',
        y='Number of Groups',
        color='Number of Groups',
        title="Which Software Is Most Frequently Used by Adversary Groups?",
        labels={'x': 'Software Name', 'y': 'Number of Groups'},
        custom_data=top_n_df[['Groups']]  # Include groups in custom data
    )

    # Update the hover template to display the custom data
    fig.update_traces(hovertemplate="<b>Software:</b> %{x}<br><b>Number of Groups:</b> %{y}<br><b>Groups:</b> %{customdata[0]}<extra></extra>")

    st.plotly_chart(fig)

    # Display full list of groups on click
    selected_software = st.selectbox('Select Software for Full Group List', options=top_n_df['Software Name'].tolist(),
                                     index=0)

    if selected_software:
        full_groups = group_info_dict.get(selected_software, [])
        with st.expander("Full List of Groups", expanded=False):
            if full_groups:
                st.write(', '.join(full_groups))
            else:
                st.warning("No groups found for this software.")

# Main visualization logic
def main():
    dataset = load_relationship_data()
    st.title('MITRE ATT&CK')

    uses_df = dataset[dataset['mapping type'] == 'uses']
    group_use = uses_df[uses_df['source type'] == 'group']
    group_use_software_df = group_use[group_use['target type'] == 'software']

    software_table = load_software_data()
    group_use_software_df = group_use_software_df.merge(software_table, left_on='target ID', right_on='ID')
    group_use_software_df.drop(['name', 'ID', 'domain'], axis=1, inplace=True)

    type_options = group_use_software_df['type'].unique().tolist()
    selected_type = st.selectbox('Select Type', options=type_options, index=None, placeholder="Select Type...")

    one_hot_encoded = group_use_software_df['platforms']
    one_hot_encoded = one_hot_encoded.str.get_dummies(sep=', ')
    platforms_options = one_hot_encoded.columns.tolist()
    selected_platform = st.selectbox('Select Platform', options=platforms_options, index=None, placeholder="Select Platforms...")

    # Add a slider for selecting the number of bars to display
    max_bars = min(20, group_use_software_df['target name'].nunique())  # Limit to max 20 or available software
    num_bars = st.slider('Select Number of Bars to Display', 1, max_bars, 10)  # Default to 10

    plot_bar(group_use_software_df, selected_type, selected_platform, num_bars)

# Experiment visualization logic
def experiments():
    dataset = load_relationship_data()
    st.title('Experiments - MITRE ATT&CK')

    uses_df = dataset[dataset['mapping type'] == 'uses']
    group_use = uses_df[uses_df['source type'] == 'group']
    group_use_tech_df = group_use[group_use['target type'] == 'technique']

    technique_table = load_technique_data()
    group_use_tech_df = group_use_tech_df.merge(technique_table, left_on='target ID', right_on='ID')
    group_use_tech_df.drop(['name', 'ID', 'domain', 'mapping type', 'target type', 'source type', 'mapping description'], axis=1, inplace=True)

    plot_pie(group_use_tech_df)

# Sidebar navigation
st.sidebar.title("Menu")
selection = st.sidebar.radio("Type", ["Bar chart Visualization", "Pie chart Visualization"])

# Main Visualization
if selection == "Bar chart Visualization":
    main()

# Experiments Visualization
elif selection == "Pie chart Visualization":
    experiments()
