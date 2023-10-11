import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

def load_data_once_daily(url):
    @st.experimental_memo
    def get_data() -> pd.DataFrame:
        return pd.read_csv(url)

def plot_data(df):
    # top-level filters
    job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

    # creating a single-element container
    placeholder = st.empty()

    # dataframe filter
    df = df[df["job"] == job_filter]

    # near real-time / live feed simulation
    for seconds in range(200):

        df["age_new"] = df["age"] * np.random.choice(range(1, 5))
        df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

        # creating KPIs
        avg_age = np.mean(df["age_new"])

        count_married = int(
            df[(df["marital"] == "married")]["marital"].count()
            + np.random.choice(range(1, 30))
        )

        balance = np.mean(df["balance_new"])

        with placeholder.container():

            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Age ⏳",
                value=round(avg_age),
                delta=round(avg_age) - 10,
            )
            
            kpi2.metric(
                label="Married Count 💍",
                value=int(count_married),
                delta=-10 + count_married,
            )
            
            kpi3.metric(
                label="A/C Balance $",
                value=f"$ {round(balance,2)} ",
                delta=-round(balance / count_married) * 100,
            )

            # create two columns for charts
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.markdown("### First Chart")
                fig = px.density_heatmap(
                    data_frame=df, y="age_new", x="marital"
                )
                st.write(fig)
                
            with fig_col2:
                st.markdown("### Second Chart")
                fig2 = px.histogram(data_frame=df, x="age_new")
                st.write(fig2)

            time.sleep(1)

def main():
    # Page Title
    st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)
    # Dashboard Title
    st.title("Real-Time / Live Data Science Dashboard")

    # Get annotations from DB
    df = load_data_once_daily(dataset_url)

    plot_data(df)

# %%
if __name__ == "__main__":
    main()
