import pandas as pd
import matplotlib.pyplot as plt

dataset_path = 'https://github.com/JuanAlvin03/mitre_attck_dataset/raw/main/mitre_dataset.xlsx'
dataset = pd.read_excel(dataset_path, sheet_name="relationships") # relationships is sheet name, header true
# dataset.describe()

dataset.drop(['created', 'last modified', 'STIX ID'], axis=1, inplace=True)
#dataset.head()

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

# check data count

# group_use_software_df.count() # must be 921
# group_use_tech_df.count() # must be 3387
# software_use_tech_df.count() # must be 8967

# number of 'unique' groups # 136
# print(group_use_software_df['source name'].nunique())

one_hot_encoded = group_use_software_df['target name']
one_hot_encoded = one_hot_encoded.str.get_dummies()
software_usage_count_by_groups = one_hot_encoded.sum()
software_usage_count_by_groups.sort_values(ascending=False, inplace=True)

top10 = software_usage_count_by_groups.head(10)
# this means 'Mimikatz' software is used by 46 out of 136 groups

plt.figure(figsize=(10, 8))
plt.bar(top10.index, top10.values, color='skyblue')
plt.title('Top 10 Software usage by groups')
plt.xlabel('Software')
plt.ylabel('out of 136 groups')
plt.grid()
plt.show()


# number of 'unique' technique in (group use technique) # 403
# print(group_use_tech_df['target name'].nunique())

one_hot_encoded2 = group_use_tech_df['target name']
one_hot_encoded2 = one_hot_encoded2.str.get_dummies()
tech_usage_count_by_groups = one_hot_encoded2.sum()
tech_usage_count_by_groups.sort_values(ascending=False, inplace=True)

top10grouptech = tech_usage_count_by_groups.head(10)

# figsize=(width, height)
plt.figure(figsize=(30, 10))
plt.bar(top10grouptech.index, top10grouptech.values, color='skyblue')
plt.title('Top 10 Techniques used by groups')
plt.xlabel('Techniques')
plt.ylabel('out of 136 groups')
plt.grid()
plt.show()

# number of 'unique' software # 677
# number of 'unique' tech # 423
#print(software_use_tech_df['source name'].nunique())
#print(software_use_tech_df['target name'].nunique())

one_hot_encoded3 = software_use_tech_df['target name']
one_hot_encoded3 = one_hot_encoded3.str.get_dummies()
tech_usage_count_by_soft = one_hot_encoded3.sum()
tech_usage_count_by_soft.sort_values(ascending=False, inplace=True)

top10softtech = tech_usage_count_by_soft.head(10)
tech_usage_count_by_soft.head(10)
# this means 'Ingress Tool Transfer' technique is used by 351 out of 677 software

plt.figure(figsize=(35, 10))
plt.bar(top10softtech.index, top10softtech.values, color='skyblue')
plt.title('10 Most Common Techniques used by software')
plt.xlabel('Techniques')
plt.ylabel('out of 136 groups')
plt.grid()
plt.show()