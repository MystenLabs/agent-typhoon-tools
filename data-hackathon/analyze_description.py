import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import time
import logging
from datetime import datetime

# Configure logging
def setup_logging():
    """Configure logging with proper format and file output"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"analysis_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Logging initialized")
    return log_file

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_description(description: str) -> Dict:
    """Analyze a single description using GPT-4."""
    try:
        logging.debug(f"Analyzing description (truncated): {description[:100]}...")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a classifier that categorizes project descriptions.
                    Categorize into: DeFi, Gaming, Infrastructure, Social, NFT, DAO, Security, Education, Other.
                    Respond with JSON format only: {"category": "CATEGORY", "confidence": 0.95}"""
                },
                {"role": "user", "content": description}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        logging.info(f"Successfully categorized as: {result['category']} (confidence: {result['confidence']})")
        return {
            "description": description,
            "category": result["category"],
            "confidence": result["confidence"]
        }
    except Exception as e:
        logging.error(f"Error processing description: {str(e)}", exc_info=True)
        return {
            "description": description,
            "category": "ERROR",
            "confidence": 0
        }

def create_visualizations(df: pd.DataFrame, from_summary: bool = False):
    """Create and save various visualizations."""
    logging.info("Creating visualizations")
    try:
        # Set the style for all plots
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")

        if from_summary:
            # For data loaded from summary json
            # Bar Plot
            plt.figure(figsize=(12, 6))
            sns.barplot(data=df, x='category', y='count')
            plt.title('Distribution of Project Categories')
            plt.xlabel('Category')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            
            # Add value labels on top of each bar
            for i, v in enumerate(df['count']):
                plt.text(i, v, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig('category_distribution.png')
            plt.close()
            
            # Pie Chart
            plt.figure(figsize=(10, 8))
            colors = sns.color_palette("Pastel1", n_colors=len(df))
            plt.pie(
                df['count'].values,
                labels=df['category'],
                autopct='%1.1f%%',
                startangle=140,
                colors=colors
            )
            total_projects = df['count'].sum()
            plt.title(f'Category Distribution\n(Total Qualified Projects: {total_projects})')
            plt.tight_layout()
            plt.savefig('category_distribution_pie.png')
            plt.close()
            
        else:
            # For fresh analysis data
            category_counts = df['category'].value_counts()
            
            # Bar Plot
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(x=category_counts.index, y=category_counts.values)
            plt.title('Distribution of Project Categories', pad=20)
            plt.xlabel('Category')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            
            # Add value labels on top of each bar
            for i, v in enumerate(category_counts.values):
                ax.text(i, v, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig('category_distribution.png')
            plt.close()
            
            # Pie Chart
            plt.figure(figsize=(10, 8))
            colors = sns.color_palette("Pastel1", n_colors=len(category_counts))
            plt.pie(
                category_counts.values,
                labels=category_counts.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=colors
            )
            total_projects = len(df)
            plt.title(f'Category Distribution\n(Total Qualified Projects: {total_projects})')
            plt.tight_layout()
            plt.savefig('category_distribution_pie.png')
            plt.close()

            # Confidence Distribution
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=df, x='category', y='confidence')
            plt.title('Confidence Distribution by Category')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('confidence_distribution.png')
            plt.close()

        logging.info("Saved all visualizations")

    except Exception as e:
        logging.error(f"Error creating visualizations: {str(e)}", exc_info=True)

def load_existing_results() -> Dict:
    """Load existing results from qualified_category_summary.json if it exists."""
    try:
        if os.path.exists('qualified_category_summary.json'):
            with open('qualified_category_summary.json', 'r') as f:
                data = json.load(f)
                logging.info("Loaded existing category summary")
                return data
        return None
    except Exception as e:
        logging.error(f"Error loading existing results: {str(e)}", exc_info=True)
        return None

def main():
    log_file = setup_logging()
    logging.info("Starting analysis")
    
    try:
        # Check for existing results first
        existing_results = load_existing_results()
        if existing_results:
            logging.info("Found existing analysis results")
            logging.info("Category Distribution for Qualified Projects:")
            for category, count in existing_results.items():
                logging.info(f"  {category}: {count}")
            
            # Create DataFrame from existing results for visualization
            results_df = pd.DataFrame([
                {"category": cat, "count": count}
                for cat, count in existing_results.items()
            ])
            
            # Create visualizations from existing data
            create_visualizations(results_df, from_summary=True)
            logging.info("Created visualizations from existing data")
            return

        # If no existing results, proceed with full analysis
        logging.info("No existing results found. Starting new analysis...")
        
        # Read descriptions from CSV file
        logging.info("Reading CSV file")
        df = pd.read_csv('ANALYSIS COPY AI Hackathon Submission Qualifications - AI Hackathon Project Submissions.csv')
        
        # Convert 'Disqualified' to proper boolean
        df['Disqualified'] = df['Disqualified'].fillna(False)
        df['Disqualified'] = df['Disqualified'].map({
            'TRUE': True, 'True': True, True: True,
            'FALSE': False, 'False': False, False: False
        })
        
        # Filter for qualified projects only
        qualified_df = df[df['Disqualified'] == False].copy()
        logging.info(f"Found {len(qualified_df)} qualified projects out of {len(df)} total projects")
        
        # Extract descriptions from qualified projects, removing any null values
        descriptions = qualified_df['Description'].dropna().tolist()
        logging.info(f"Found {len(descriptions)} valid descriptions to analyze")

        results = []
        
        # Process descriptions with rate limiting
        for i, desc in enumerate(descriptions, 1):
            logging.info(f"Processing description {i}/{len(descriptions)}")
            result = analyze_description(desc)
            results.append(result)
            
            if i < len(descriptions):
                logging.debug("Rate limiting pause")
                time.sleep(1)

        # Convert to DataFrame
        results_df = pd.DataFrame(results)

        # Save raw results
        results_df.to_csv('qualified_analysis_results.csv', index=False)
        logging.info("Saved results to qualified_analysis_results.csv")
        
        # Create category summary
        category_summary = results_df['category'].value_counts().to_dict()
        with open('qualified_category_summary.json', 'w') as f:
            json.dump(category_summary, f, indent=2)
        logging.info("Saved category summary to qualified_category_summary.json")

        # Create visualizations
        create_visualizations(results_df)

        # Log final summary
        logging.info("Analysis complete")
        logging.info("Category Distribution for Qualified Projects:")
        for category, count in category_summary.items():
            logging.info(f"  {category}: {count}")

        logging.info(f"Log file saved to: {log_file}")

    except Exception as e:
        logging.error(f"Fatal error in main execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()