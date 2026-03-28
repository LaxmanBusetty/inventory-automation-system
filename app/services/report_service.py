from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


class ReportService:
    def __init__(self, reports_dir: str | Path = "reports") -> None:
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def export_csv(self, df: pd.DataFrame, filename_prefix: str = "inventory_report") -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = self.reports_dir / f"{filename_prefix}_{timestamp}.csv"
        df.to_csv(path, index=False)
        return str(path)
