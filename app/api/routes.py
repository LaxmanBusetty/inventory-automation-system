from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.services.inventory_service import InventoryAnalyzer
from app.services.mock_supplier_api import MockSupplierAPI
from app.services.report_service import ReportService

router = APIRouter()
DATA_PATH = Path("data/inventory_sample.csv")
REPORTS_DIR = Path("reports")


def _get_analyzer() -> InventoryAnalyzer:
    return InventoryAnalyzer(DATA_PATH)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/inventory")
def get_inventory() -> list[dict]:
    analyzer = _get_analyzer()
    try:
        df = analyzer.load_inventory()
        return df.to_dict(orient="records")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/inventory/analyze")
def analyze_inventory() -> dict:
    analyzer = _get_analyzer()
    try:
        df = analyzer.load_inventory()
        analysis_df = analyzer.analyze_inventory(df)
        return {
            "summary": analyzer.summary(analysis_df),
            "items": analysis_df.to_dict(orient="records"),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/inventory/export-report")
def export_report() -> dict:
    analyzer = _get_analyzer()
    report_service = ReportService(REPORTS_DIR)
    try:
        df = analyzer.load_inventory()
        analysis_df = analyzer.analyze_inventory(df)
        report_path = report_service.export_csv(analysis_df, filename_prefix="restock_report")
        return {"message": "Report exported successfully", "report_path": report_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/inventory/sync-supplier")
def sync_supplier() -> dict:
    analyzer = _get_analyzer()
    try:
        df = analyzer.load_inventory()
        updates = MockSupplierAPI.fetch_stock_updates()

        for update in updates:
            sku = update["sku"]
            delta = update["stock_delta"]
            df.loc[df["sku"] == sku, "current_stock"] = df.loc[df["sku"] == sku, "current_stock"] + delta

        df.to_csv(DATA_PATH, index=False)
        analysis_df = analyzer.analyze_inventory(df)
        return {
            "message": "Supplier sync completed",
            "updates": updates,
            "summary": analyzer.summary(analysis_df),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
