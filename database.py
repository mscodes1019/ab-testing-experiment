import pandas as pd
from country_converter import CountryConverter
import pandas as pd

class CSVRepository:
    """Repository class for interacting with applicant data from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing applicant data.

    Attributes
    ----------
    df : pandas.DataFrame
        All data will be extracted from and loaded to this DataFrame.
    """
    def __init__(self, filepath="mydata/admissions_dataset.csv"):
        self.path = filepath
        self.df = pd.read_csv(filepath)
        self.df["created_at"] = pd.to_datetime(self.df["created_at"], errors="coerce")
        self.df["admission_quiz"] = self.df["admission_quiz"].str.strip().str.lower()
        pass

    def get_nationality_value_counts(self, normalize=True):
        """Return nationality value counts.

        Parameters
        ----------
        normalize : bool, optional
            Whether to normalize frequency counts, by default True
    
        Returns
        -------
        pd.DataFrame
            Database results with columns: 'count', 'country_name', 'country_iso2',
            'country_iso3'.
        """
        # Count values and reset index
        nationality_counts = self.df["CountryISO2"].value_counts(ascending=False)
        df_nationality_df = nationality_counts.reset_index()
        df_nationality_df.columns = ['country_iso2', 'count']
    
        # Add country names and ISO3
        cc = CountryConverter()
        df_nationality_df["country_name"] = cc.convert(df_nationality_df["country_iso2"], to="name_short")
        df_nationality_df["country_iso3"] = cc.convert(df_nationality_df["country_iso2"], to="ISO3")
    
        # Add percentage if needed
        if normalize:
            df_nationality_df["count_pct"] = (
                df_nationality_df["count"] / df_nationality_df["count"].sum() * 100
            )
    
        return df_nationality_df  

    def get_ages(self):

        """Gets applicants ages from database.

        Returns
        -------
        pd.Series
        """
        df = self.df.copy()

        # Convert 'birthday' column to datetime, auto-format detection
        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
    
        # Today's date
        today = pd.to_datetime("today")
    
        # Calculate age
        df['age'] = df['birthday'].apply(
            lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if pd.notnull(dob) else None
        )

        # Return only the age Series
        return df['age']
    def __ed_sort(self, sort_order):

        """Helper function for self.get_ed_value_counts."""
        mapping = {
        "Bachelors": 1,
        "Masters": 2,
        "PhD": 3,
       }

        # Sort the degrees based on the mapping and return the corresponding sort order
        sort_order = counts.index.map(mapping)
    
        return sort_order
    
        # Assuming 'education' is a Series with degrees as the index (degree names)
        education = df["highest_degree_earned"].value_counts(ascending=False)
        
        # Create the mapping dictionary again for sorting purposes
        mapping = {
            "Bachelors": 1,
            "Masters": 2,
            "PhD": 3,
        }
    
        # Sort the education Series based on the custom sort order
        education_sorted = education.iloc[education.index.map(lambda x: mapping.get(x, 0)).argsort()]
    
        return education_sorted
        

    def get_ed_value_counts(self, normalize=False):
        """Gets value counts of applicant education levels.
    
        Parameters
        ----------
        normalize : bool, optional
            Whether or not to return normalized value counts, by default False
    
        Returns
        -------
        pd.Series
            Series with degree names as index and counts as values
        """
        # Get value counts from the DataFrame
        education = self.df["highest_degree_earned"].value_counts(normalize=normalize, ascending=False)
    
        # Optionally sort index based on custom logic (e.g., by a defined order)
        custom_order = ["Bachelors", "Masters", "PhD"]
        education = education.reindex(custom_order).dropna()
    
        return education


    def get_no_quiz_per_day(self):
        """Calculates number of no-quiz applicants per day.
    
        Returns
        -------
        pd.Series
        """
        observations_df = self.df.copy()
    
        # Ensure 'created_at' is datetime
        observations_df["created_at"] = pd.to_datetime(observations_df["created_at"])
    
        # Group by date and count
        daily_counts = (
            observations_df
            .groupby(observations_df["created_at"].dt.date)
            .size()
            .reset_index(name="users")
            .rename(columns={"created_at": "date"})
        )
    
        # Convert to Series: index = date, values = users
        no_quiz = (
            daily_counts
            .set_index("date")["users"]
            .sort_index()
        )
    
        return no_quiz

    def get_contingency_table(self):
        """After experiment is run, creates crosstab of experimental groups
        by quiz completion.
    
        Returns
        -------
        plotly.graph_objects.Figure
            A bar chart showing quiz completion by group.
        """
    
        # Step 1: Create the contingency table
        contingency = pd.crosstab(self.df["group"], self.df["admission_quiz"].str.title())
    
        # Step 2: Convert to long form for plotting
        df_plot = (
            contingency
            .reset_index()
            .melt(id_vars="group", value_vars=["Not Completed", "Completed"],
                  var_name="Outcome", value_name="Count")
        )
    
        # Step 3: Generate the bar chart
        fig = px.bar(
            df_plot,
            x="group",
            y="Count",
            color="Outcome",
            barmode="group",
            title="Quiz Completion by Group"
        )
    
        fig.update_layout(
            xaxis_title="Group",
            yaxis_title="Number of Users",
            legend_title="Outcome"
        )
    
        return fig

    
