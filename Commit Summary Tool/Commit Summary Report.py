import csv
import pandas as pd

# Function to read the CSV file
def read_statistics_csv(filename='statistics.csv'):
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

# Function to analyze the data and generate a summary
def analyze_commit_statistics(df):
    if df is None or df.empty:
        print("No data to analyze.")
        return None
    
    summary = {}
    
    # Total commits across all repositories
    summary['Total Commits'] = df['Commits in Last 365 Days'].sum()
    
    # Average commits per repository
    summary['Average Commits per Repository'] = df['Commits in Last 365 Days'].mean()
    
    # Repository with the highest commits
    summary['Repository with Most Commits'] = df.loc[df['Commits in Last 365 Days'].idxmax(), 'Repository']
    summary['Highest Commit Count'] = df['Commits in Last 365 Days'].max()
    
    # Repository with the lowest commits
    summary['Repository with Least Commits'] = df.loc[df['Commits in Last 365 Days'].idxmin(), 'Repository']
    summary['Lowest Commit Count'] = df['Commits in Last 365 Days'].min()

    return summary

# Function to generate the Commit Summary Report
def generate_commit_summary_report(summary, filename='commit_summary_report.txt'):
    try:
        with open(filename, 'w') as file:
            file.write("Commit Summary Report\n")
            file.write("=====================\n\n")
            file.write(f"Total Commits: {summary['Total Commits']}\n")
            file.write(f"Average Commits per Repository: {summary['Average Commits per Repository']:.2f}\n\n")
            file.write(f"Repository with Most Commits: {summary['Repository with Most Commits']} ({summary['Highest Commit Count']} commits)\n")
            file.write(f"Repository with Least Commits: {summary['Repository with Least Commits']} ({summary['Lowest Commit Count']} commits)\n")
        
        print(f"Commit Summary Report saved to {filename}")
    except Exception as e:
        print(f"Error generating report: {e}")

# Main function
def main():
    # Step 1: Read the CSV file
    df = read_statistics_csv('statistics.csv')
    
    # Step 2: Analyze the data
    summary = analyze_commit_statistics(df)
    
    # Step 3: Generate the summary report
    if summary:
        generate_commit_summary_report(summary)

if __name__ == "__main__":
    main()
