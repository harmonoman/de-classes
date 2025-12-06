import io
import pandas as pd


class DataFormatService:
    """Handles converting DataFrames to/from serialized formats."""

    # --- CSV ---
    @staticmethod
    def df_to_csv_bytes(df):
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue().encode("utf-8")

    @staticmethod
    def csv_bytes_to_df(data_bytes):
        return pd.read_csv(io.BytesIO(data_bytes))

    # --- PARQUET ---
    @staticmethod
    def df_to_parquet_bytes(df):
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        return buffer.getvalue()

    @staticmethod
    def parquet_bytes_to_df(data_bytes):
        return pd.read_parquet(io.BytesIO(data_bytes))

    # --- JSON ---
    @staticmethod
    def df_to_json_bytes(df):
        text = df.to_json(orient="records")
        return text.encode("utf-8")

    @staticmethod
    def json_bytes_to_df(data_bytes):
        text = data_bytes.decode("utf-8")
        return pd.read_json(io.StringIO(text))