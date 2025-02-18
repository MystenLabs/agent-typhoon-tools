import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('ANALYSIS COPY AI Hackathon Submission Qualifications - AI Hackathon Project Submissions.csv')

# Set the style for all plots
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8-whitegrid')

# Create a figure with subplots
plt.figure(figsize=(15, 10))

# 1. Track Distribution
plt.subplot(2, 2, 1)
# Split the 'Tracks' column and explode into separate rows
tracks = df['Tracks'].str.split(',', expand=True).stack()
track_counts = tracks.value_counts()

sns.barplot(x=track_counts.values, y=track_counts.index)
plt.title('Distribution of Projects by Track')
plt.xlabel('Number of Projects')
plt.ylabel('Track')

# 2. Tech Integration Analysis
plt.subplot(2, 2, 2)
# Count non-null values for each tech integration column
tech_cols = ['Sui tech integration', 'Eliza tech integration', 'Atoma tech integration', 
             'Suilend tech integration', 'Bluefin tech integration', 'Navi tech integration']
tech_usage = df[tech_cols].notna().sum()

sns.barplot(x=tech_usage.values, y=[col.replace(' tech integration', '') for col in tech_usage.index])
plt.title('Technology Integration Distribution')
plt.xlabel('Number of Projects')
plt.ylabel('Technology')

# 3. Project Qualification Status
plt.subplot(2, 2, 3)
disqualified_counts = df['Disqualified'].value_counts()
colors = ['#ff9999' if x == True else '#66b3ff' for x in disqualified_counts.index]

plt.pie(disqualified_counts.values, labels=disqualified_counts.index, 
        autopct='%1.1f%%', colors=colors)
plt.title('Project Qualification Status')

# 4. Platform Presence
plt.subplot(2, 2, 4)
platform_cols = ['GitHub Repository', 'Website', 'Demo Video']
platform_presence = df[platform_cols].notna().sum()

sns.barplot(x=platform_presence.values, y=platform_presence.index)
plt.title('Platform Presence Distribution')
plt.xlabel('Number of Projects')
plt.ylabel('Platform')

# Adjust layout and display
plt.tight_layout()
plt.show()

# Additional visualization: Project Description Length Distribution
plt.figure(figsize=(10, 6))
df['Description_Length'] = df['Description'].str.len()
sns.histplot(data=df, x='Description_Length', bins=30)
plt.title('Distribution of Project Description Lengths')
plt.xlabel('Description Length (characters)')
plt.ylabel('Count')
plt.show()