"""
AUTOMATED INCIDENT REPORTING SYSTEM v1
Professional ITSM Analytics and Automation

Author: Aleeza Iftikhar
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from datetime import datetime

# =========================
# CONFIGURATION
# =========================

DATA_FILE = "data/ITSM_Dataset.csv.xlsx"

OUTPUT_DIR = Path("output")
CHART_DIR = Path("charts")

OUTPUT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

REPORT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================
# VISUAL SETTINGS
# =========================

sns.set_style("whitegrid")

plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

# =========================
# MAIN CLASS
# =========================

class AutomatedIncidentReportingSystem:

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.df = None
        self.kpis = {}

    # =========================
    # LOAD DATA
    # =========================

    def load_data(self):

        try:
            logger.info("Loading dataset...")

            if not self.file_path.exists():
                raise FileNotFoundError(f"Dataset not found: {self.file_path}")

            self.df = pd.read_excel(self.file_path)

            self.df.columns = self.df.columns.str.strip()

            logger.info(f"Dataset loaded successfully | Rows: {len(self.df)}")

        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise

    # =========================
    # CLEAN & PREPROCESS
    # =========================

    def preprocess_data(self):

        try:
            logger.info("Cleaning and preprocessing dataset...")

            # Remove important nulls
            self.df = self.df.dropna(
                subset=[
                    "Status",
                    "Priority",
                    "Topic",
                    "Agent Group"
                ]
            )

            # Rename columns
            self.df = self.df.rename(columns={
                "Topic": "Incident Type",
                "Agent Group": "Assignment Group"
            })

            # Convert dates
            self.df["Created time"] = pd.to_datetime(
                self.df["Created time"],
                errors="coerce"
            )

            self.df["Resolution time"] = pd.to_datetime(
                self.df["Resolution time"],
                errors="coerce"
            )

            # Resolution hours
            self.df["Resolution Hours"] = (
                self.df["Resolution time"] -
                self.df["Created time"]
            ).dt.total_seconds() / 3600

            # Month extraction
            self.df["Month"] = (
                self.df["Created time"]
                .dt.to_period("M")
                .astype(str)
            )

            # Resolved flag
            self.df["Resolved Flag"] = (
                self.df["Status"]
                .isin(["Closed", "Resolved"])
                .astype(int)
            )

            logger.info("Preprocessing completed")

        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            raise

    # =========================
    # KPI CALCULATIONS
    # =========================

    def calculate_kpis(self):

        logger.info("Calculating KPIs...")

        total_tickets = len(self.df)

        resolved_tickets = self.df[
            self.df["Resolved Flag"] == 1
        ].shape[0]

        resolution_rate = round(
            (resolved_tickets / total_tickets) * 100,
            2
        )

        self.kpis = {

            # Core Metrics
            "Total Tickets": total_tickets,
            "Open Tickets": self.df[
                self.df["Status"] == "Open"
            ].shape[0],

            "Closed Tickets": self.df[
                self.df["Status"] == "Closed"
            ].shape[0],

            "Resolved Tickets": self.df[
                self.df["Status"] == "Resolved"
            ].shape[0],

            "In Progress Tickets": self.df[
                self.df["Status"] == "In Progress"
            ].shape[0],

            # Priority Metrics
            "Critical Priority Count": self.df[
                self.df["Priority"] == "Critical"
            ].shape[0],

            "High Priority Count": self.df[
                self.df["Priority"] == "High"
            ].shape[0],

            # Performance Metrics
            "Resolution Rate %": resolution_rate,

            "Average Resolution Time (hrs)": round(
                self.df["Resolution Hours"].mean(),
                2
            ),

            "Median Resolution Time (hrs)": round(
                self.df["Resolution Hours"].median(),
                2
            ),

            # Top Categories
            "Most Common Incident Type": self.df[
                "Incident Type"
            ].value_counts().idxmax(),

            "Top Assignment Group": self.df[
                "Assignment Group"
            ].value_counts().idxmax(),

            # Organizational Metrics
            "Total Assignment Groups": self.df[
                "Assignment Group"
            ].nunique(),

            "Total Incident Types": self.df[
                "Incident Type"
            ].nunique()
        }

        logger.info("KPI calculation completed")

    # =========================
    # PRINT SUMMARY
    # =========================

    def print_summary(self):

        print("\n" + "=" * 70)
        print(" AUTOMATED INCIDENT REPORTING SYSTEM ")
        print("=" * 70)

        print(f"\nGenerated: {REPORT_TIME}")

        for kpi, value in self.kpis.items():
            print(f"{kpi:<40}: {value}")

        print("\n" + "=" * 70)

    # =========================
    # EXPORT REPORTS
    # =========================

    def export_reports(self):

        logger.info("Exporting reports...")

        # Cleaned data
        self.df.to_excel(
            OUTPUT_DIR / "cleaned_incidents.xlsx",
            index=False
        )

        # KPI Summary
        summary_df = pd.DataFrame(
            list(self.kpis.items()),
            columns=["KPI", "Value"]
        )

        summary_df.to_excel(
            OUTPUT_DIR / "incident_summary.xlsx",
            index=False
        )

        # High Priority Export
        high_priority_df = self.df[
            self.df["Priority"].isin(["Critical", "High"])
        ]

        high_priority_df.to_excel(
            OUTPUT_DIR / "high_priority_incidents.xlsx",
            index=False
        )

        logger.info("Reports exported successfully")

    # =========================
    # GENERATE CHARTS
    # =========================

    def generate_charts(self):

        logger.info("Generating charts...")

        # =========================
        # INCIDENT TYPE CHART
        # =========================

        plt.figure()

        self.df["Incident Type"] \
            .value_counts() \
            .head(10) \
            .plot(kind="bar")

        plt.title("Top Incident Types")
        plt.xlabel("Incident Type")
        plt.ylabel("Ticket Count")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(
            CHART_DIR / "incident_type_chart.png",
            dpi=300
        )

        plt.close()

        # =========================
        # PRIORITY CHART
        # =========================

        plt.figure()

        self.df["Priority"] \
            .value_counts() \
            .plot(kind="pie", autopct="%1.1f%%")

        plt.ylabel("")

        plt.title("Priority Distribution")

        plt.tight_layout()

        plt.savefig(
            CHART_DIR / "priority_distribution_chart.png",
            dpi=300
        )

        plt.close()

        # =========================
        # MONTHLY TREND CHART
        # =========================

        plt.figure()

        monthly_trend = (
            self.df["Month"]
            .value_counts()
            .sort_index()
        )

        monthly_trend.plot(marker="o")

        plt.title("Monthly Incident Trend")
        plt.xlabel("Month")
        plt.ylabel("Ticket Count")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(
            CHART_DIR / "monthly_incident_trend.png",
            dpi=300
        )

        plt.close()

        # =========================
        # ASSIGNMENT GROUP CHART
        # =========================

        plt.figure()

        self.df["Assignment Group"] \
            .value_counts() \
            .head(10) \
            .plot(kind="barh")

        plt.title("Top Assignment Groups")
        plt.xlabel("Ticket Count")
        plt.ylabel("Assignment Group")

        plt.tight_layout()

        plt.savefig(
            CHART_DIR / "assignment_group_chart.png",
            dpi=300
        )

        plt.close()

        logger.info("Charts generated successfully")

    # =========================
    # MAIN EXECUTION
    # =========================

    def run(self):

        logger.info("Starting Automated Incident Reporting System")

        self.load_data()

        self.preprocess_data()

        self.calculate_kpis()

        self.print_summary()

        self.export_reports()

        self.generate_charts()

        logger.info("Automation completed successfully")

        print("\nAll files generated successfully.")
        print("Check:")
        print("1. output/")
        print("2. charts/")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app = AutomatedIncidentReportingSystem(DATA_FILE)

    app.run()