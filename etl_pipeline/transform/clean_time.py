import pandas as pd


def generate_time_dimension(sales_path, logistics_path, output_path):
    """Genera un CSV con la dimensión de tiempo basada en fechas únicas de ventas y logística,
    incluyendo la hora en una columna aparte."""

    sales_df = pd.read_csv(sales_path, usecols=["fecha"])
    logistics_df = pd.read_csv(logistics_path, usecols=["fecha_envio"])

    all_dates = pd.concat([sales_df["fecha"], logistics_df["fecha_envio"]]).dropna()
    all_dates = pd.to_datetime(all_dates, errors='coerce').dropna()

    unique_timestamps = sorted(all_dates.unique())
    time_df = pd.DataFrame({
        "tiempo_id": range(1, len(unique_timestamps) + 1),
        "fecha": [pd.Timestamp(ts).date() for ts in unique_timestamps],
        "hora": [pd.Timestamp(ts).time() for ts in unique_timestamps],
        "anio": [pd.Timestamp(ts).year for ts in unique_timestamps],
        "mes": [pd.Timestamp(ts).month for ts in unique_timestamps],
        "dia": [pd.Timestamp(ts).day for ts in unique_timestamps],
        "dia_nombre": [pd.Timestamp(ts).strftime('%A') for ts in unique_timestamps],
        "mes_nombre": [pd.Timestamp(ts).strftime('%B') for ts in unique_timestamps]
    })


    time_df.to_csv(output_path, index=False)
    print(f"📆 Dimensión de tiempo guardada en {output_path}")