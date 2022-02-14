import glob
import bbva2pandas as b2p
import pandas as pd


def _extract_operations(path):
    documents = glob.glob(f"{path}/*.pdf")
    dfs = map(lambda x: b2p.Report(x).to_df(), documents)
    return pd.concat(dfs)


def _group_amount_by_year(df):
    df_by_year = df.groupby(df.date.dt.year).sum()
    df_by_year.index = df_by_year.index.to_flat_index()
    df_by_year.index.name = "year"
    return df_by_year.drop(columns="balance").squeeze()


def _group_amount_by_month(df):
    df_by_month = df.groupby([(df.date.dt.year), (df.date.dt.month)]).sum()
    df_by_month.index = df_by_month.index.to_flat_index().map(
        lambda x: f"{str(x[0])[2:]}-{x[1]}"
    )
    df_by_month.index.name = "month"
    return df_by_month.drop(columns="balance").squeeze()


def _group_amount_by_concept(df):
    df_by_concept = df.groupby(df.concept).sum()
    return df_by_concept.drop(columns="balance").squeeze()


class Operations:
    def __init__(self, path="."):
        self.operations = _extract_operations(path)
        self.incoming = self.operations.query("amount > 0")
        self.spending = self.operations.query("amount < 0")

    @property
    def by_year(self):
        return pd.concat(
            {
                "incoming": _group_amount_by_year(self.incoming),
                "spending": _group_amount_by_year(self.spending),
                "difference": _group_amount_by_year(self.incoming)
                + _group_amount_by_year(self.spending),
            },
            axis=1,
        )

    @property
    def by_month(self):
        return pd.concat(
            {
                "incoming": _group_amount_by_month(self.incoming),
                "spending": _group_amount_by_month(self.spending),
                "difference": _group_amount_by_month(self.incoming)
                + _group_amount_by_month(self.spending),
            },
            axis=1,
        )

    @property
    def by_concept(self):
        return pd.concat(
            {
                "incoming": _group_amount_by_concept(self.incoming),
                "spending": _group_amount_by_concept(self.spending),
                "difference": _group_amount_by_concept(self.incoming)
                + _group_amount_by_concept(self.spending),
            },
            axis=1,
        )
