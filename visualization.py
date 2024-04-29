import pandas as pd
import altair as alt
import queries as q


def bar_charts(series_ids: tuple):

    rec_series = q.q_series(series_ids)

    chart1 = (
        alt.Chart(rec_series)
        .mark_bar()
        .encode(
            x=alt.X("title:N", title=None),
            y=alt.Y("rating:Q"),
            tooltip="rating:Q",
        )
        .properties(title="IMDB score", width=600)
        .interactive()
    )

    chart2 = (
        alt.Chart(rec_series)
        .mark_bar()
        .encode(
            x=alt.X("title:N", title=None),
            y=alt.Y("vote_num:Q"),
            tooltip="vote_num:Q",
        )
        .properties(title="Number of votes", width=600)
        .interactive()
    )

    return chart1, chart2


def scatter_plot(series_ids: tuple):
    """Creates a scatter plot

    Args:
        series_ids (tuple): series_ids to be included

    Returns:
        alt.chart: an altair chart
    """
    rec_series = q.q_series(series_ids)

    chart = (
        alt.Chart(rec_series)
        .mark_point()
        .encode(
            x=alt.X("rating:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("vote_num:Q", scale=alt.Scale(zero=False)),
            tooltip="title:N",
        )
        .interactive()
    )

    return chart
