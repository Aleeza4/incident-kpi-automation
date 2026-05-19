"""
Incident KPI Automation System
Professional ITSM Analytics and Reporting
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set professional styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class IncidentKPIAnalyzer:
    """Professional incident KPI analysis and reporting system."""
    
    def __init__(self, data_path: str):
        """Initialize the analyzer with data source."""
        self.data_path = Path(data_path)
        self.df = None
        self.kpi_results = {}
        self.timestamp = datetime.now()
    
    def load_data(self) -> bool:
        """Load and validate incident data."""
        try:
            if not self.data_path.exists():
                logger.error(f"Data file not found: {self.data_path}")
                return False
            
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_excel(self.data_path)
            
            # Clean column names
            self.df.columns = self.df.columns.str.strip()
            
            # Validate required columns
            required_cols = ["Created time", "Resolution time", "Status", "Priority", "Topic", "Agent Group"]
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            if missing_cols:
                logger.error(f"Missing required columns: {missing_cols}")
                return False
            
            logger.info(f"Successfully loaded {len(self.df)} records")
            return True
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def preprocess_data(self) -> bool:
        """Preprocess and enrich the dataset."""
        try:
            logger.info("Preprocessing data")
            
            # Convert date columns
            self.df["Created time"] = pd.to_datetime(self.df["Created time"], errors='coerce')
            self.df["Resolution time"] = pd.to_datetime(self.df["Resolution time"], errors='coerce')
            
            # Calculate resolution hours
            self.df["Resolution Hours"] = (
                self.df["Resolution time"] - self.df["Created time"]
            ).dt.total_seconds() / 3600
            
            # Add additional metrics
            self.df["Resolved"] = self.df["Status"].isin(["Closed", "Resolved"]).astype(int)
            self.df["Priority Numeric"] = self.df["Priority"].map({
                "Critical": 1, "High": 2, "Medium": 3, "Low": 4
            })
            
            logger.info("Data preprocessing completed")
            return True
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            return False
    
    def calculate_kpis(self):
        """Calculate comprehensive KPIs."""
        try:
            logger.info("Calculating KPIs")
            
            total_tickets = len(self.df)
            resolved_tickets = self.df[self.df["Resolved"] == 1].shape[0]
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            
            self.kpi_results = {
                # Ticket Status Metrics
                "Total Tickets": total_tickets,
                "Open Tickets": self.df[self.df["Status"] == "Open"].shape[0],
                "Closed Tickets": self.df[self.df["Status"] == "Closed"].shape[0],
                "Resolved Tickets": self.df[self.df["Status"] == "Resolved"].shape[0],
                "In Progress Tickets": self.df[self.df["Status"] == "In Progress"].shape[0],
                
                # Priority Metrics
                "Critical Priority Count": self.df[self.df["Priority"] == "Critical"].shape[0],
                "High Priority Count": self.df[self.df["Priority"] == "High"].shape[0],
                "Medium Priority Count": self.df[self.df["Priority"] == "Medium"].shape[0],
                "Low Priority Count": self.df[self.df["Priority"] == "Low"].shape[0],
                
                # Performance Metrics
                "Resolution Rate %": round(resolution_rate, 2),
                "Avg Resolution Time (hrs)": round(self.df["Resolution Hours"].mean(), 2),
                "Median Resolution Time (hrs)": round(self.df["Resolution Hours"].median(), 2),
                "Max Resolution Time (hrs)": round(self.df["Resolution Hours"].max(), 2),
                
                # Top Items
                "Most Common Topic": self.df["Topic"].value_counts().idxmax(),
                "Top Assignment Group": self.df["Agent Group"].value_counts().idxmax(),
                
                # Additional Metrics
                "Avg Tickets per Group": round(total_tickets / self.df["Agent Group"].nunique(), 2),
                "Total Agent Groups": self.df["Agent Group"].nunique(),
                "Total Topics": self.df["Topic"].nunique(),
            }
            
            logger.info(f"KPI calculation completed: {len(self.kpi_results)} metrics calculated")
        except Exception as e:
            logger.error(f"Error calculating KPIs: {e}")
    
    def print_summary(self):
        """Print professional summary report."""
        print("\n" + "="*70)
        print(" INCIDENT KPI AUTOMATION - EXECUTIVE SUMMARY REPORT")
        print(f" Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        print("\n📊 TICKET STATUS OVERVIEW")
        print("-" * 70)
        print(f"  Total Tickets:           {self.kpi_results.get('Total Tickets', 0):>10}")
        print(f"  Resolved Tickets:        {self.kpi_results.get('Resolved Tickets', 0):>10}")
        print(f"  Open Tickets:            {self.kpi_results.get('Open Tickets', 0):>10}")
        print(f"  In Progress Tickets:     {self.kpi_results.get('In Progress Tickets', 0):>10}")
        
        print("\n⚡ PRIORITY BREAKDOWN")
        print("-" * 70)
        print(f"  Critical:                {self.kpi_results.get('Critical Priority Count', 0):>10}")
        print(f"  High:                    {self.kpi_results.get('High Priority Count', 0):>10}")
        print(f"  Medium:                  {self.kpi_results.get('Medium Priority Count', 0):>10}")
        print(f"  Low:                     {self.kpi_results.get('Low Priority Count', 0):>10}")
        
        print("\n⏱️  PERFORMANCE METRICS")
        print("-" * 70)
        print(f"  Resolution Rate:         {self.kpi_results.get('Resolution Rate %', 0):>10}%")
        print(f"  Avg Resolution Time:     {self.kpi_results.get('Avg Resolution Time (hrs)', 0):>10} hrs")
        print(f"  Median Resolution Time:  {self.kpi_results.get('Median Resolution Time (hrs)', 0):>10} hrs")
        print(f"  Max Resolution Time:     {self.kpi_results.get('Max Resolution Time (hrs)', 0):>10} hrs")
        
        print("\n👥 ORGANIZATION METRICS")
        print("-" * 70)
        print(f"  Top Assignment Group:    {self.kpi_results.get('Top Assignment Group', 'N/A'):>10}")
        print(f"  Total Agent Groups:      {self.kpi_results.get('Total Agent Groups', 0):>10}")
        print(f"  Avg Tickets per Group:   {self.kpi_results.get('Avg Tickets per Group', 0):>10}")
        print(f"  Most Common Topic:       {self.kpi_results.get('Most Common Topic', 'N/A'):>10}")
        
        print("\n" + "="*70 + "\n")
    
    def export_reports(self):
        """Export comprehensive reports to Excel and HTML."""
        try:
            logger.info("Exporting reports")
            
            # Create outputs directory
            Path("outputs").mkdir(exist_ok=True)
            
            # Export cleaned dataset
            output_file = "outputs/cleaned_incidents.xlsx"
            self.df.to_excel(output_file, index=False)
            logger.info(f"Cleaned dataset exported: {output_file}")
            
            # Export KPI summary
            kpi_df = pd.DataFrame(list(self.kpi_results.items()), columns=["KPI", "Value"])
            summary_file = "outputs/incident_summary.xlsx"
            kpi_df.to_excel(summary_file, index=False)
            logger.info(f"KPI summary exported: {summary_file}")
            
        except Exception as e:
            logger.error(f"Error exporting reports: {e}")
    
    def generate_visualizations(self):
        """Generate professional visualizations."""
        try:
            logger.info("Generating visualizations")
            Path("charts").mkdir(exist_ok=True)
            
            try:
                # Chart 1: Incident Topic Distribution (Top 10)
                plt.figure(figsize=(14, 6))
                topic_counts = self.df["Topic"].value_counts().head(10)
                colors = sns.color_palette("husl", len(topic_counts))
                topic_counts.plot(kind="barh", color=colors)
                plt.title("Top 10 Incident Topics", fontsize=14, fontweight='bold')
                plt.xlabel("Ticket Count", fontsize=11)
                plt.ylabel("Topic", fontsize=11)
                plt.tight_layout()
                plt.savefig("charts/incident_topic_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                logger.info("Generated: incident_topic_distribution.png")
            except Exception as e:
                logger.warning(f"Failed to generate incident_topic_distribution.png: {e}")
                plt.close()
            
            try:
                # Chart 2: Priority Distribution (Pie Chart)
                plt.figure(figsize=(10, 8))
                priority_data = self.df["Priority"].value_counts()
                colors_priority = {"Critical": "#d62728", "High": "#ff7f0e", "Medium": "#2ca02c", "Low": "#1f77b4"}
                pie_colors = [colors_priority.get(idx, "#1f77b4") for idx in priority_data.index]
                plt.pie(priority_data, labels=priority_data.index, autopct='%1.1f%%', 
                       colors=pie_colors, startangle=90)
                plt.title("Ticket Distribution by Priority", fontsize=14, fontweight='bold')
                plt.tight_layout()
                plt.savefig("charts/priority_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                logger.info("Generated: priority_distribution.png")
            except Exception as e:
                logger.warning(f"Failed to generate priority_distribution.png: {e}")
                plt.close()
            
            try:
                # Chart 3: Agent Group Distribution
                plt.figure(figsize=(14, 6))
                group_counts = self.df["Agent Group"].value_counts()
                colors_group = sns.color_palette("Set2", len(group_counts))
                group_counts.plot(kind="bar", color=colors_group)
                plt.title("Tickets by Agent Group", fontsize=14, fontweight='bold')
                plt.xlabel("Agent Group", fontsize=11)
                plt.ylabel("Ticket Count", fontsize=11)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig("charts/agent_group_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                logger.info("Generated: agent_group_distribution.png")
            except Exception as e:
                logger.warning(f"Failed to generate agent_group_distribution.png: {e}")
                plt.close()
            
            try:
                # Chart 4: Resolution Time Distribution
                plt.figure(figsize=(12, 6))
                self.df["Resolution Hours"].hist(bins=50, edgecolor='black', color='steelblue')
                plt.title("Distribution of Resolution Times", fontsize=14, fontweight='bold')
                plt.xlabel("Resolution Time (hours)", fontsize=11)
                plt.ylabel("Frequency", fontsize=11)
                plt.axvline(self.df["Resolution Hours"].mean(), color='red', linestyle='--', 
                           linewidth=2, label=f"Mean: {self.df['Resolution Hours'].mean():.2f} hrs")
                plt.legend()
                plt.tight_layout()
                plt.savefig("charts/resolution_time_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                logger.info("Generated: resolution_time_distribution.png")
            except Exception as e:
                logger.warning(f"Failed to generate resolution_time_distribution.png: {e}")
                plt.close()
            
            try:
                # Chart 5: Status Distribution
                plt.figure(figsize=(10, 6))
                status_counts = self.df["Status"].value_counts()
                colors_status = {"Closed": "#2ca02c", "Resolved": "#1f77b4", "Open": "#d62728", "In Progress": "#ff7f0e"}
                status_colors = [colors_status.get(idx, "#808080") for idx in status_counts.index]
                status_counts.plot(kind="bar", color=status_colors)
                plt.title("Tickets by Status", fontsize=14, fontweight='bold')
                plt.xlabel("Status", fontsize=11)
                plt.ylabel("Ticket Count", fontsize=11)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig("charts/status_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                logger.info("Generated: status_distribution.png")
            except Exception as e:
                logger.warning(f"Failed to generate status_distribution.png: {e}")
                plt.close()
            
            logger.info("Visualization generation completed")
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
    
    def run(self):
        """Execute complete analysis pipeline."""
        logger.info("Starting Incident KPI Analysis")
        
        if not self.load_data():
            logger.critical("Failed to load data. Exiting.")
            return False
        
        if not self.preprocess_data():
            logger.critical("Failed to preprocess data. Exiting.")
            return False
        
        self.calculate_kpis()
        self.print_summary()
        self.export_reports()
        logger.info("Starting visualization generation")
        self.generate_visualizations()
        
        logger.info("Analysis completed successfully")
        print("✅ All operations completed successfully!")
        print("📁 Files generated in 'outputs' and 'charts' directories")
        return True


if __name__ == "__main__":
    analyzer = IncidentKPIAnalyzer("data/ITSM_Dataset.csv.xlsx")
    analyzer.run()