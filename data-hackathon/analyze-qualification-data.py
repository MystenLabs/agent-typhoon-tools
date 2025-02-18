import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create the charts/ directory if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Read the CSV file and properly handle boolean values
df = pd.read_csv('ANALYSIS COPY AI Hackathon Submission Qualifications - AI Hackathon Project Submissions.csv')

# Print debugging information
print(f"Total number of projects: {len(df)}")
print("\nUnique values in 'Disqualified' column:", df['Disqualified'].unique())
print("\nValue counts in 'Disqualified' column:\n", df['Disqualified'].value_counts())

# Convert 'Disqualified' to proper boolean
df['Disqualified'] = df['Disqualified'].fillna(False)  # Handle NaN values
df['Disqualified'] = df['Disqualified'].map({'TRUE': True, 'True': True, True: True, 
                                            'FALSE': False, 'False': False, False: False})

# Print after conversion
print("\nAfter conversion - Value counts in 'Disqualified' column:\n", df['Disqualified'].value_counts())

# Set the style for all plots
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Define tech columns
tech_cols = [
    'Sui tech integration', 'Eliza tech integration', 'Atoma tech integration',
    'Suilend tech integration', 'Bluefin tech integration', 'Navi tech integration'
]

# Main Overview Plot
plt.figure(figsize=(12, 8))

# 1. Project Qualification Status (pie chart)
plt.subplot(1, 2, 1)
disqualified_counts = df['Disqualified'].value_counts().sort_index()  # Sort by index to ensure consistent order
total_projects = len(df)
qualified_count = disqualified_counts[False] if False in disqualified_counts else 0
disqualified_count = disqualified_counts[True] if True in disqualified_counts else 0
colors = sns.color_palette("pastel")[:2]
plt.pie([qualified_count, disqualified_count],  # Changed order to show qualified first
        labels=[f'Qualified\n({qualified_count}/{total_projects})',
                f'Disqualified\n({disqualified_count}/{total_projects})'],
        autopct='%1.1f%%',
        colors=colors)
plt.title('Project Qualification Status')

# 2. Technology Integration Overview (bar plot)
plt.subplot(1, 2, 2)
tech_usage = df[tech_cols].notna().sum()
tech_df = pd.DataFrame({
    'Technology': [col.replace(' tech integration', '') for col in tech_usage.index],
    'Count': tech_usage.values
})
sns.barplot(data=tech_df, x='Count', y='Technology', hue='Technology', legend=False)
plt.title('Overall Technology Integration Distribution')
plt.xlabel('Number of Projects')

plt.tight_layout()
plt.savefig('charts/qualification_and_tech_overview.png')
plt.close()

# ------------------------------------------------------------------------------
# Analysis of Qualified Projects Only
qualified_df = df[df['Disqualified'] == False].copy()

# Technology Integration Analysis for Qualified Projects
plt.figure(figsize=(12, 6))

# Technology Integration Bar Plot (Qualified Projects Only)
tech_usage_qualified = qualified_df[tech_cols].notna().sum()
tech_qualified_df = pd.DataFrame({
    'Technology': [col.replace(' tech integration', '') for col in tech_usage_qualified.index],
    'Count': tech_usage_qualified.values
})
sns.barplot(data=tech_qualified_df, x='Count', y='Technology', hue='Technology', legend=False)
plt.title(f'Technology Integration Distribution\n(Qualified Projects Only: {len(qualified_df)} projects)')
plt.xlabel('Number of Projects')

plt.tight_layout()
plt.savefig('charts/qualified_tech_distribution.png')
plt.close()

# Technology Integration Correlation Heatmap
tech_binary = qualified_df[tech_cols].notna().astype(int)
tech_corr = tech_binary.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(tech_corr, 
            annot=True, 
            cmap=sns.color_palette("vlag", as_cmap=True),
            fmt=".2f",
            xticklabels=[col.replace(' tech integration', '') for col in tech_cols],
            yticklabels=[col.replace(' tech integration', '') for col in tech_cols])
plt.title('Technology Integration Correlation Heatmap\n(Qualified Projects)')
plt.tight_layout()
plt.savefig('charts/tech_correlation_heatmap.png')
plt.close()

# Technology Integration Pie Chart (Qualified Projects)
plt.figure(figsize=(10, 8))
plt.pie(
    tech_usage_qualified.values,
    labels=[col.replace(' tech integration', '') for col in tech_usage_qualified.index],
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette("Pastel1", n_colors=len(tech_cols))
)
plt.title(f'Technology Integration Distribution\n(Qualified Projects: {len(qualified_df)} total)')
plt.tight_layout()
plt.savefig('charts/tech_integration_pie.png')
plt.close()