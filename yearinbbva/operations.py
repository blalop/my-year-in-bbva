import pandas as pd
import os
import sqlite3


class Operations:
    def __init__(self, path=os.getenv("MYYEARINBBVA_PATH", "movements.db")):
        self.conn = sqlite3.connect(path, check_same_thread=False)

    @property
    def all(self):
        return pd.read_sql(
            "SELECT * FROM MOVEMENTS ORDER BY date",
            self.conn,
        )

    @property
    def by_year(self):
        incoming = pd.read_sql(
            "SELECT STRFTIME('%Y', date) AS year, SUM(amount) AS incoming FROM MOVEMENTS WHERE amount > 0 GROUP BY year",
            self.conn,
            index_col="year",
        )
        spending = pd.read_sql(
            "SELECT STRFTIME('%Y', date) AS year, SUM(amount) AS spending FROM MOVEMENTS WHERE amount < 0 GROUP BY year",
            self.conn,
            index_col="year",
        )

        return pd.merge(incoming, spending, on="year")

    @property
    def by_month(self):
        incoming = pd.read_sql(
            "SELECT STRFTIME('%Y-%m', date) AS month, SUM(amount) AS incoming FROM MOVEMENTS WHERE amount > 0 GROUP BY month",
            self.conn,
            index_col="month",
        )
        spending = pd.read_sql(
            "SELECT STRFTIME('%Y-%m', date) AS month, SUM(amount) AS spending FROM MOVEMENTS WHERE amount < 0 GROUP BY month",
            self.conn,
            index_col="month",
        )

        return pd.merge(incoming, spending, on="month")

    @property
    def by_concept(self):
        incoming = pd.read_sql(
            "SELECT concept, SUM(amount) AS incoming FROM MOVEMENTS WHERE amount > 0 GROUP BY concept",
            self.conn,
            index_col="concept",
        )
        spending = pd.read_sql(
            "SELECT concept, SUM(amount) AS spending FROM MOVEMENTS WHERE amount < 0 GROUP BY concept",
            self.conn,
            index_col="concept",
        )

        return pd.merge(incoming, spending, on="concept", how="outer")

    @property
    def concepts(self):
        return pd.read_sql(
            "SELECT DISTINCT concept FROM MOVEMENTS",
            self.conn,
        )

    def query_by_month(self, month, amount):
        if amount > 0:
            return pd.read_sql(
                "SELECT STRFTIME('%Y-%m-%d', date) AS day, concept, subconcept, card, amount FROM MOVEMENTS WHERE STRFTIME('%Y-%m', date) = STRFTIME('%Y-%m', :month) AND amount > 0 ORDER BY date",
                self.conn,
                params={"month": month},
            )
        elif amount < 0:
            return pd.read_sql(
                "SELECT STRFTIME('%Y-%m-%d', date) AS day, concept, subconcept, card, amount FROM MOVEMENTS WHERE STRFTIME('%Y-%m', date) = STRFTIME('%Y-%m', :month) AND amount < 0 ORDER BY date",
                self.conn,
                params={"month": month},
            )

    def query_by_concept(self, concept, amount):
        if amount > 0:
            return pd.read_sql(
                "SELECT STRFTIME('%Y-%m-%d', date) AS day, subconcept, card, amount FROM MOVEMENTS WHERE concept = :concept AND amount > 0 ORDER BY date",
                self.conn,
                params={"concept": concept},
            )
        elif amount < 0:
            return pd.read_sql(
                "SELECT STRFTIME('%Y-%m-%d', date) AS day, subconcept, card, amount FROM MOVEMENTS WHERE concept = :concept AND amount < 0 ORDER BY date",
                self.conn,
                params={"concept": concept},
            )
