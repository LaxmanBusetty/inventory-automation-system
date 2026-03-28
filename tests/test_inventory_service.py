from app.services.inventory_service import InventoryAnalyzer


def test_inventory_analysis_has_expected_columns():
    analyzer = InventoryAnalyzer("data/inventory_sample.csv")
    df = analyzer.load_inventory()
    analysis_df = analyzer.analyze_inventory(df)

    expected_columns = {
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
    }

    assert expected_columns.issubset(set(analysis_df.columns))


def test_summary_returns_valid_metrics():
    analyzer = InventoryAnalyzer("data/inventory_sample.csv")
    df = analyzer.load_inventory()
    analysis_df = analyzer.analyze_inventory(df)
    summary = analyzer.summary(analysis_df)

    assert summary["total_skus"] > 0
    assert summary["skus_requiring_reorder"] >= 0
    assert summary["total_recommended_units"] >= 0
