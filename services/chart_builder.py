import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


def get_first_numeric_column(df: pd.DataFrame) -> str | None:
    numeric_columns = df.select_dtypes(include="number").columns  # get only numeric columns
    if len(numeric_columns) == 0:
        return None  # no numeric data to chart
    return numeric_columns[0]  # just grab the first one for now


def build_chart(df: pd.DataFrame, column: str):
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)  # create a chart canvas, high-res
    df[column].dropna().hist(ax=ax, bins=30, color="#4C72B0", edgecolor="white")  # histogram, ignoring missing values
    ax.set_title(f"Distribution of {column}", fontsize=13, fontweight="bold")
    ax.set_xlabel(column, fontsize=10)
    ax.set_ylabel("Frequency", fontsize=10)
    ax.grid(axis="y", alpha=0.3)  # light gridlines for readability
    fig.tight_layout()  # avoid labels getting cut off
    return fig


def encode_chart_to_base64(fig) -> str:
    buffer = io.BytesIO()               # create an empty "fake file" in memory
    fig.savefig(buffer, format="png")   # save the chart image into that fake file (not to disk)
    plt.close(fig)                      # free up memory now that we're done with the chart
    buffer.seek(0)                      # rewind to the start so we can read the full image
    encoded = base64.b64encode(buffer.read()).decode("utf-8")  # convert image bytes -> text string for JSON
    return encoded