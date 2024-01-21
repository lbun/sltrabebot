import streamlit as st
from streamlit.logger import get_logger
from utils_aws_s3 import AwsClient
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello TradeBot24",
        page_icon="👋",
    )

    st.write("# Welcome to TradeBot Dashboard! 👋")

    st.sidebar.success("Select a demo above.")

    portfolio_values = AwsClient().load_portfolio_values()
    df = pd.DataFrame(portfolio_values)
    df.set_index("time", inplace=True)
    df.sort_index(ascending=True, inplace=True)


    st.dataframe(df)
       
    st.line_chart(df["value"])
    st.line_chart(df["pct_return"])

if __name__ == "__main__":
    run()
