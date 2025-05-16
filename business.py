import math

import numpy as np
import plotly.express as px
import pandas as pd
import scipy
from database import CSVRepository
from statsmodels.stats.contingency_tables import Table2x2
from statsmodels.stats.power import GofChisquarePower
# from teaching_tools.ab_test.experiment import Experiment


# Tasks 7.4.7, 7.4.9, 7.4.10, 7.4.19s
class GraphBuilder:
    """Methods for building Graphs."""

    def __init__(self, repo=CSVRepository()):

        """init

        Parameters
        ----------
        repo : CSVRepository, optional
            Data source, by default CSVRepository()
        """
        self.repo = repo

    def build_nat_choropleth(self):

        """Creates nationality choropleth map.

        Returns
        -------
        Figure
        """
        # Get nationality counts from database
        df_nationality = self.repo.get_nationality_value_counts(normalize=True)
        # Create Figure
        fig = px.choropleth(
            data_frame=df_nationality,
            locations="country_iso3",
            locationmode="ISO-3",
            color="count_pct",
            projection="natural earth",
            color_continuous_scale=px.colors.sequential.Oranges,
            title="Applicants: Nationality",
            hover_name="country_name",
            hover_data=["count", "count_pct"]
        )

        return fig
        

    def build_age_hist(self):

        """Create age histogram.

        Returns
        -------
        Figure
        """
        # Get ages from respository
        ages = self.repo.get_ages()
        # Create Figure
        # Create Figure
        fig = px.histogram(
            x=ages,
            nbins=20,
            title="Applicants: Age"
        )

        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Frequency [count]",
            width=800,
            height=600
        )
    
        return fig

    def build_ed_bar(self):
        """Creates education level bar chart.
    
        Returns
        -------
        Figure
        """
        # Get education level value counts from repo
        degree = self.repo.get_ed_value_counts(normalize=True)
    
        # Create Figure
        fig = px.bar(
            x=degree.index,              # Degree names (e.g., Bachelors, Masters)
            y=degree.values,             # Frequency or % values
            title="Applicants: Highest Degree Earned",
            labels={"x": "Degree", "y": "Percentage of Applicants"}
        )
    
        # Update layout for better formatting
        fig.update_layout(
            xaxis_title="Degree",
            yaxis_title="Frequency [%]",
            xaxis_categoryorder='total descending',
            width=800,
            height=600
        )
    
        # Return Figure
        return fig


    def build_contingency_bar():

        """Creates side-by-side bar chart from contingency table.

        Returns
        -------
        Figure
        """
        # Get contingency table data from repo

        # Create Figure
        
        # Return Figure
        pass


# Tasks 7.4.12, 7.4.18, 7.4.20
class StatsBuilder:
    """Methods for statistical analysis."""

    def __init__(self, repo = None):

        """init

        Parameters
        ----------
        repo : CSVRepository, optional
            Data source, by default CSVRepository()
        """
        if repo is None:
            repo = CSVRepository()
        self.repo = repo
      
    

    def calculate_n_obs(self, effect_size):

        """Calculate the number of observations needed to detect effect size.

        Parameters
        ----------
        effect_size : float
            Effect size you want to be able to detect

        Returns
        -------
        int
            Total number of observations needed, across two experimental groups.
        """
        # Calculate group size, w/ alpha=0.05 and power=0.8
        chi_square_power = GofChisquarePower()
        group_size = int(
        chi_square_power.solve_power(effect_size=effect_size, alpha=0.05, power=0.8))
            
        # Return number of observations (group size * 2)
        return group_size * 2

    def calculate_cdf_pct(self, n_obs,days):

        """Calculate percent chance of gathering specified number of observations in
        specified number of days.

        Parameters
        ----------
        n_obs : int
            Number of observations you want to gather.s
        days : int
            Number of days you will run experiment.

        Returns
        -------
        float
            Percentage chance of gathering ``n_obs`` or more in ``days``.
        """
        no_quiz = self.repo.get_no_quiz_per_day()

        # Calculate mean and std of daily observations
        mean_daily = no_quiz.mean()
        std_daily = no_quiz.std()
    
        # Estimate distribution for total observations over `days` days
        total_mean = days * mean_daily
        total_std = np.sqrt(days) * std_daily
    
        # Compute P(X >= n_obs) using 1 - CDF
        prob = 1 - scipy.stats.norm.cdf(n_obs, loc=total_mean, scale=total_std)
    
        # Return as percentage
        return prob * 100

    def run_experiment(self, days=287, seed=42):
        """Run experiment. Add results to repository."""
        # Step 1: Load existing data from repo
        observations = self.repo.df.copy()

        # Step 2: Convert to DataFrame if needed
        if not isinstance(observations, pd.DataFrame):
            observations_df = pd.DataFrame(observations)
        else:
            observations_df = observations

        # Step 3: Ensure 'created_at' column is datetime
        observations_df["created_at"] = pd.to_datetime(observations_df["created_at"], errors="coerce")
        observations_df = observations_df.dropna(subset=["created_at"])

        # Step 4: Count users per day
        daily_counts = (
            observations_df.groupby(observations_df["created_at"].dt.date)
            .size()
            .reset_index(name="users")
            .rename(columns={"created_at": "date"})
            .sort_values("date")
        )

        if days > len(daily_counts):
            raise ValueError(f"Not enough days in dataset. Requested {days}, have {len(daily_counts)}.")

        # Step 5: Randomly sample days
        sampled_days = daily_counts.sample(n=days, replace=False, random_state=seed)

        # Step 6: Simulate new data
        simulated_docs = []
        for _, row in sampled_days.iterrows():
            for _ in range(row["users"]):
                simulated_docs.append({
                    "created_at": str(row["date"]),
                    "data": "simulated user event"
                })

        # Step 7: Append to repo.df and save manually
        new_df = pd.DataFrame(simulated_docs)
        self.repo.df = pd.concat([self.repo.df, new_df], ignore_index=True)
        self.repo.df.to_csv(self.repo.path, index=False)  # Save to same file

        return {
            "days_sampled": days,
            "total_users": len(simulated_docs),
            "daily_sample": sampled_days
        }

    def run_chi_square():

        """Tests nominal association.

        Returns
        -------
        A bunch containing the following attributes:

        statistic: float
            The chi^2 test statistic.

        df: int
            The degrees of freedom of the reference distribution

        pvalue: float
            The p-value for the test.
        """
        # Get data from repo

        # Create `Table2X2` from data

        # Run chi-square test

        # Return chi-square results
        pass
