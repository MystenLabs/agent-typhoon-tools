import csv
import os
from typing import List, Tuple

def parse_csv_scores(filepath: str) -> List[Tuple[str, float]]:
    """Parse CSV file and return list of (project_name, avg_score) tuples."""
    projects = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header rows
        for _ in range(7):
            next(reader)
            
        for row in reader:
            if len(row) >= 8:  # Ensure row has enough columns
                project_name = row[0].strip()
                try:
                    avg_score = float(row[7]) if row[7] else 0.0
                    if project_name and not project_name.startswith(('Project', 'Name', '-', 'Judge')):
                        projects.append((project_name, avg_score))
                except ValueError:
                    continue
                    
    return projects

def get_top_40_projects(projects: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """Return top 40 projects sorted by average score."""
    # Sort by score in descending order
    sorted_projects = sorted(projects, key=lambda x: x[1], reverse=True)
    # Return top 40
    return sorted_projects[:40]

def create_project_frequency_report(output_dir: str) -> None:
    """Create a report showing how often each project appears in judges' top 40 lists."""
    project_counts = {}
    judge_count = 0
    
    # Read all top 40 files and count project appearances
    for filename in os.listdir(output_dir):
        if filename.endswith('-top-40-projects.txt'):
            judge_count += 1
            with open(os.path.join(output_dir, filename), 'r', encoding='utf-8') as f:
                # Skip header lines
                next(f)  # Skip title
                next(f)  # Skip separator line
                
                for line in f:
                    # Extract project name from line (format: "1. Project Name: 9.50")
                    project = line.split(': ')[0].split('. ')[1].strip()
                    project_counts[project] = project_counts.get(project, 0) + 1
    
    # Sort projects by frequency (descending) and alphabetically for ties
    ranked_projects = sorted(project_counts.items(), 
                           key=lambda x: (-x[1], x[0]))
    
    # Write frequency report
    report_path = os.path.join(output_dir, 'project-frequency-report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Project Frequency in Judges' Top 40 Lists\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total number of judges: {judge_count}\n\n")
        
        for i, (project, count) in enumerate(ranked_projects, 1):
            percentage = (count / judge_count) * 100
            f.write(f"{i:3d}. {project}: {count}/{judge_count} judges ({percentage:.1f}%)\n")
    
    print(f"Created project frequency report at {report_path}")

def main():
    # Create projects directory if it doesn't exist
    output_dir = os.path.join('data-judges', 'projects')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each CSV file in data-judges directory
    data_dir = 'data-judges'
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            judge_name = filename.split(' - ')[1].split('.')[0]  # Extract judge name
            
            # Parse scores and get top 40
            projects = parse_csv_scores(filepath)
            top_40 = get_top_40_projects(projects)
            
            # Write results to output file in projects directory
            output_filename = os.path.join(output_dir, f"{judge_name}-top-40-projects.txt")
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f"Top 40 Projects - {judge_name}\n")
                f.write("-" * 50 + "\n")
                for i, (project, score) in enumerate(top_40, 1):
                    f.write(f"{i}. {project}: {score:.2f}\n")
            
            print(f"Created {output_filename}")
    
    # Create frequency report after processing all judges
    create_project_frequency_report(output_dir)

if __name__ == "__main__":
    main()