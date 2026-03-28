from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class InventoryConfig:
    target_stock_days: int = 20


class InventoryAnalyzer:
    def __init__(self, csv_path: str | Path, config: InventoryConfig | None = None) -> None:
        self.csv_path = Path(csv_path)
        self.config = config or InventoryConfig()

    def load_inventory(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Inventory file not found: {self.csv_path}")

        df = pd.read_csv(self.csv_path)
        required_cols = {
            "sku",
            "product_name",
            "category",
            "current_stock",
            "safety_stock",
            "lead_time_days",
            "last_7d_sales",
            "supplier",
            "max_capacity",
        }
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        return df

    def analyze_inventory(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        result["daily_sales_avg"] = (result["last_7d_sales"] / 7).round(2)
        result["daily_sales_avg"] = result["daily_sales_avg"].replace(0, 0.01)

        result["days_of_cover"] = (result["current_stock"] / result["daily_sales_avg"]).round(2)
        result["reorder_point"] = (
            result["lead_time_days"] * result["daily_sales_avg"] + result["safety_stock"]
        ).round(2)

        target_stock = self.config.target_stock_days * result["daily_sales_avg"]
        result["recommended_reorder_qty"] = np.maximum(target_stock - result["current_stock"], 0)
        result["recommended_reorder_qty"] = np.minimum(
            result["recommended_reorder_qty"], result["max_capacity"]
        ).round(0).astype(int)

        result["priority"] = result.apply(self._assign_priority, axis=1)
        result["needs_reorder"] = result["recommended_reorder_qty"] > 0

        cols = [
            "sku",
            "product_name",
            "category",
            "supplier",
            "current_stock",
            "daily_sales_avg",
            "days_of_cover",
            "lead_time_days",
            "safety_stock",
            "reorder_point",
            "recommended_reorder_qty",
            "priority",
            "needs_reorder",
        ]
        return result[cols].sort_values(by=["needs_reorder", "priority", "days_of_cover"], ascending=[False, True, True])

    @staticmethod
    def _assign_priority(row: pd.Series) -> str:
        current_stock = float(row["current_stock"])
        days_of_cover = float(row["days_of_cover"])
        lead_time_days = float(row["lead_time_days"])

        if current_stock <= 0:
            return "Critical"
        if days_of_cover <= lead_time_days:
            return "High"
        if days_of_cover <= lead_time_days + 3:
            return "Medium"
        return "Low"

    def summary(self, analysis_df: pd.DataFrame) -> dict:
        reorder_df = analysis_df[analysis_df["needs_reorder"]]
        return {
            "total_skus": int(len(analysis_df)),
            "skus_requiring_reorder": int(len(reorder_df)),
            "critical_items": int((analysis_df["priority"] == "Critical").sum()),
            "high_priority_items": int((analysis_df["priority"] == "High").sum()),
            "total_recommended_units": int(reorder_df["recommended_reorder_qty"].sum()),
        }
