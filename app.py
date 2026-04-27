from __future__ import annotations

import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from brand_positioning import render_brand_positioning


TEXTS = {
    "zh-TW": {
        "title": "MarTech行銷報表",
        "subtitle": "以交易、客戶、產品、門市與折扣視角追蹤成長與獲利",
        "lang": "語言",
        "theme": "介面主題",
        "global_filters": "全域篩選",
        "date_range": "日期區間",
        "enable_comparison": "啟用比較期間",
        "comparison_range": "比較期間",
        "country": "國家",
        "city": "城市",
        "store_type": "店型",
        "brand": "品牌",
        "category": "品類",
        "loyalty": "會員狀態",
        "member": "會員",
        "non_member": "非會員",
        "overview": "總覽",
        "customer": "客戶分群",
        "product": "產品與品牌",
        "store": "門市通路",
        "discount": "折扣影響",
        "brand_positioning": "品牌定位",
        "kpi_revenue": "總營收",
        "kpi_profit": "總利潤",
        "kpi_margin": "毛利率",
        "kpi_orders": "訂單數",
        "kpi_customers": "活躍客數",
        "kpi_aov": "平均客單價",
        "kpi_discount": "平均折扣率",
        "time_comparison": "時間比較",
        "kpi_mom": "月比",
        "kpi_qoq": "季比",
        "kpi_yoy": "年比",
        "trend_title": "營收與利潤月趨勢",
        "segment_title": "會員 vs 非會員貢獻",
        "cohort_title": "新客 vs 舊客營收",
        "age_title": "客戶年齡層分布",
        "rfm_segment_title": "RFM 客群分布",
        "rfm_scatter_title": "RFM 客戶價值分佈",
        "rfm_table_title": "RFM 客群摘要",
        "rfm_segment": "RFM 客群",
        "rfm_recency": "最近消費天數",
        "rfm_frequency": "購買頻次",
        "rfm_monetary": "消費金額",
        "rfm_customer_count": "客戶數",
        "rfm_revenue": "客群營收",
        "brand_title": "品牌績效（營收 / 利潤）",
        "category_title": "品類貢獻",
        "cocoa_title": "可可濃度與毛利關聯",
        "store_country_title": "國家營收與毛利",
        "store_type_title": "店型表現",
        "city_title": "城市 Top 10 營收",
        "discount_bucket_title": "折扣區間效益",
        "discount_scatter_title": "折扣率與毛利率關係",
        "threat_alert": "威脅預警",
        "churn_risk": "客群流失風險",
        "margin_decline": "毛利下滑產品",
        "churn_high_risk": "高風險",
        "churn_medium_risk": "中風險",
        "churn_low_risk": "低風險",
        "margin_alert_title": "毛利下滑幅度 Top 10",
        "churn_detail_title": "高價值客群流失分析",
        "no_alerts": "目前無威脅警報",
        "advanced_analytics": "進階分析",
        "cac_ltv": "CAC / LTV 分析",
        "cac": "獲客成本",
        "ltv": "客戶終身價值",
        "ltv_cac_ratio": "LTV/CAC 比率",
        "promo_roi": "推廣 ROI",
        "marketing_funnel": "行銷漏斗",
        "new_customer_cost": "新客成本",
        "existing_customer_ltv": "舊客終身價值",
        "discount_investment": "折扣投入",
        "roas": "廣告投資回報率",
        "repeat_rate": "複購率",
        "cohort_ltv_title": "新舊客 LTV 對比",
        "discount_roi_title": "折扣區間 ROI 分析",
        "funnel_metrics_title": "行銷轉化漏斗",
        "empty_data": "目前篩選條件下沒有資料。",
        "data_quality": "資料品質",
        "date_coverage": "日期覆蓋",
        "null_count": "空值欄位數",
        "loaded_rows": "載入交易筆數",
        "footer": "指標說明：毛利率 = 利潤 / 營收；平均客單價 = 營收 / 訂單數。",
    },
    "en": {
        "title": "MarTech行銷報表",
        "subtitle": "Track growth and profitability across sales, customer, product, store, and discount dimensions",
        "lang": "Language",
        "theme": "Theme",
        "global_filters": "Global Filters",
        "date_range": "Date Range",
        "enable_comparison": "Enable Comparison Period",
        "comparison_range": "Comparison Period",
        "country": "Country",
        "city": "City",
        "store_type": "Store Type",
        "brand": "Brand",
        "category": "Category",
        "loyalty": "Loyalty Status",
        "member": "Member",
        "non_member": "Non-member",
        "overview": "Overview",
        "customer": "Customer",
        "product": "Product & Brand",
        "store": "Store Channel",
        "discount": "Discount Impact",
        "brand_positioning": "Brand Positioning",
        "kpi_revenue": "Revenue",
        "kpi_profit": "Profit",
        "kpi_margin": "Margin Rate",
        "kpi_orders": "Orders",
        "kpi_customers": "Active Customers",
        "kpi_aov": "Average Order Value",
        "kpi_discount": "Avg Discount Rate",
        "time_comparison": "Time Comparison",
        "kpi_mom": "MoM",
        "kpi_qoq": "QoQ",
        "kpi_yoy": "YoY",
        "trend_title": "Monthly Revenue and Profit Trend",
        "segment_title": "Member vs Non-member Contribution",
        "cohort_title": "New vs Existing Customer Revenue",
        "age_title": "Customer Age Group Distribution",
        "rfm_segment_title": "RFM Segment Distribution",
        "rfm_scatter_title": "RFM Customer Value Map",
        "rfm_table_title": "RFM Segment Summary",
        "rfm_segment": "RFM Segment",
        "rfm_recency": "Recency (days)",
        "rfm_frequency": "Frequency",
        "rfm_monetary": "Monetary",
        "rfm_customer_count": "Customers",
        "rfm_revenue": "Revenue",
        "brand_title": "Brand Performance (Revenue / Profit)",
        "category_title": "Category Contribution",
        "cocoa_title": "Cocoa Percentage vs Margin",
        "store_country_title": "Country Revenue and Profit",
        "store_type_title": "Store Type Performance",
        "city_title": "Top 10 Cities by Revenue",
        "discount_bucket_title": "Discount Bucket Impact",
        "discount_scatter_title": "Discount Rate vs Margin Rate",
        "threat_alert": "Threat Alerts",
        "churn_risk": "Customer Churn Risk",
        "margin_decline": "Margin Decline Products",
        "churn_high_risk": "High Risk",
        "churn_medium_risk": "Medium Risk",
        "churn_low_risk": "Low Risk",
        "margin_alert_title": "Top 10 Products with Margin Decline",
        "churn_detail_title": "High-Value Customer Churn Analysis",
        "no_alerts": "No threat alerts at the moment",
        "advanced_analytics": "Advanced Analytics",
        "cac_ltv": "CAC / LTV Analysis",
        "cac": "Customer Acquisition Cost",
        "ltv": "Customer Lifetime Value",
        "ltv_cac_ratio": "LTV/CAC Ratio",
        "promo_roi": "Promo ROI",
        "marketing_funnel": "Marketing Funnel",
        "new_customer_cost": "New Customer Cost",
        "existing_customer_ltv": "Existing Customer LTV",
        "discount_investment": "Discount Investment",
        "roas": "Return on Ad Spend",
        "repeat_rate": "Repeat Purchase Rate",
        "cohort_ltv_title": "New vs Existing Customer LTV",
        "discount_roi_title": "Discount Bucket ROI Analysis",
        "funnel_metrics_title": "Marketing Funnel Conversion",
        "empty_data": "No data available for the selected filters.",
        "data_quality": "Data Quality",
        "date_coverage": "Date Coverage",
        "null_count": "Columns with Nulls",
        "loaded_rows": "Loaded Sales Rows",
        "footer": "Metric notes: Margin Rate = Profit / Revenue; Average Order Value = Revenue / Orders.",
    },
}


def t(lang: str, key: str) -> str:
    return TEXTS[lang].get(key, key)


def _ph(lang: str) -> str:
    """Placeholder text for multiselect widgets."""
    return "請選擇" if lang == "zh-TW" else "Choose options"


def _fmt_money(value: float) -> str:
    """Format currency: use M suffix for millions, full format otherwise."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value:,.2f}"


def _fmt_count(value: float) -> str:
    """Format integer counts with K/M suffix for large values."""
    v = int(value)
    if v >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    if v >= 10_000:
        return f"{v / 1_000:.1f}K"
    return f"{v:,}"


# Option-level translations for filter dropdowns (brand names are proper nouns, kept as-is)
_OPT_ZH: dict[str, dict[str, str]] = {
    "store_type": {"Retail": "零售店", "Mall": "購物中心", "Airport": "機場店", "Online": "線上"},
    "country":    {"Canada": "加拿大", "France": "法國", "UK": "英國",
                   "USA": "美國", "Australia": "澳洲", "Germany": "德國"},
    "city":       {"Berlin": "柏林", "London": "倫敦", "Melbourne": "墨爾本",
                   "New York": "紐約", "Paris": "巴黎", "Sydney": "雪梨", "Toronto": "多倫多"},
    "category":   {"Truffle": "松露", "Praline": "果仁", "White": "白巧克力",
                   "Dark": "黑巧克力", "Milk": "牛奶巧克力"},
}


def _display_opts(values: list[str], field: str, lang: str) -> tuple[list[str], dict[str, str]]:
    """Return (display_labels, reverse_map: display→data) for a filter field."""
    if lang != "zh-TW" or field not in _OPT_ZH:
        return values, {v: v for v in values}
    trans = _OPT_ZH[field]
    display = [trans.get(v, v) for v in values]
    reverse = {trans.get(v, v): v for v in values}
    return display, reverse


_THEME_LABELS: dict[str, dict[str, str]] = {
    "zh-TW": {"black": "⚫ 黑", "white": "⚪ 白"},
    "en":    {"black": "⚫ Black", "white": "⚪ White"},
}

_THEMES: dict[str, dict[str, str]] = {
    "black": {
        "bg_main":   "linear-gradient(135deg, #0d1117 0%, #0f1923 55%, #0d1320 100%)",
        "text_main": "#e6edf3",
        "accent":    "#58a6ff",
        "card_bg":   "rgba(22, 28, 40, 0.94)",
        "border":    "rgba(240, 246, 252, 0.10)",
        "hero_bg":   "linear-gradient(135deg, rgba(30, 41, 59, 0.92) 0%, rgba(15, 23, 42, 0.96) 100%)",
    },
    "white": {
        "bg_main":   "linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%)",
        "text_main": "#0f172a",
        "accent":    "#334155",
        "card_bg":   "rgba(255, 255, 255, 0.96)",
        "border":    "rgba(15, 23, 42, 0.12)",
        "hero_bg":   "radial-gradient(circle at 10% 20%, rgba(51, 65, 85, 0.07), rgba(248, 250, 252, 0.90))",
    },
}


def _plotly_tpl() -> str:
    return "plotly_dark" if st.session_state.get("theme_select") == "black" else "plotly_white"


def _inject_style(theme: str = "white") -> None:
    c = _THEMES.get(theme, _THEMES["white"])
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&family=Noto+Sans+TC:wght@400;500;700&display=swap');

            :root {{
                --bg-main: {c['bg_main']};
                --text-main: {c['text_main']};
                --accent: {c['accent']};
                --card-bg: {c['card_bg']};
                --border: {c['border']};
            }}

            .stApp {{
                background: var(--bg-main);
                color: var(--text-main);
                font-family: 'Manrope', 'Noto Sans TC', sans-serif;
            }}

            .block-container {{
                padding-top: 1.4rem;
                padding-bottom: 1.2rem;
            }}

            .dashboard-hero {{
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 18px 22px;
                background: {c['hero_bg']};
                margin-bottom: 16px;
                backdrop-filter: blur(4px);
            }}

            .dashboard-hero h1 {{
                margin: 0;
                letter-spacing: 0.3px;
            }}

            .dashboard-hero p {{
                margin: 6px 0 0;
                opacity: 0.88;
            }}

            [data-testid="stMetric"] {{
                border: 1px solid var(--border);
                background: var(--card-bg);
                border-radius: 14px;
                padding: 10px 8px;
                overflow: visible;
                min-width: 0;
            }}

            [data-testid="stMetricValue"] > div {{
                font-size: clamp(14px, 1.4vw, 1.2rem) !important;
                line-height: 1.25;
                white-space: nowrap;
                overflow: visible;
            }}

            [data-testid="stMetricLabel"] p {{
                font-size: clamp(11px, 0.95vw, 13px) !important;
                white-space: normal;
                word-break: break-word;
                margin-bottom: 2px;
            }}

            [data-testid="stMetricDelta"] > div {{
                font-size: clamp(10px, 0.82vw, 11px) !important;
                white-space: normal;
                word-break: break-word;
                line-height: 1.3;
            }}

            {f'''
            /* ── Main content ── */
            .stApp p, .stApp span, .stApp li, .stApp td, .stApp th,
            .stApp label, .stApp div, .stMarkdown p, .stMarkdown li {{
                color: #e6edf3 !important;
            }}
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
                color: #f0f6fc !important;
            }}
            /* Tabs */
            [data-baseweb="tab-list"] {{
                background: #161c2a !important;
            }}
            [data-baseweb="tab"] button p, [data-baseweb="tab"] button span {{
                color: #8b949e !important;
            }}
            [aria-selected="true"] button p, [aria-selected="true"] button span {{
                color: #e6edf3 !important;
            }}
            /* Expander */
            [data-testid="stExpander"] summary p,
            [data-testid="stExpander"] summary span {{
                color: #e6edf3 !important;
            }}
            /* Caption / footer */
            .stApp small, [data-testid="stCaptionContainer"] p {{
                color: #8b949e !important;
            }}
            /* Metric */
            [data-testid="stMetricValue"] > div,
            [data-testid="stMetricValue"] span {{
                color: #f0f6fc !important;
            }}
            [data-testid="stMetricLabel"] p {{
                color: #8b949e !important;
            }}
            [data-testid="stMetricDelta"] > div {{
                color: #58a6ff !important;
            }}
            /* Dataframe */
            [data-testid="stDataFrame"] th,
            [data-testid="stDataFrame"] td {{
                color: #e6edf3 !important;
            }}
            /* ── Sidebar ── */
            [data-testid="stSidebar"] > div:first-child {{
                background: #0b1120 !important;
                border-right: 1px solid rgba(240,246,252,0.09) !important;
            }}
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span:not([data-baseweb]) {{
                color: #c9d1d9 !important;
            }}
            [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
                color: #e6edf3 !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="select"] > div {{
                background: #161c2a !important;
                border-color: rgba(240,246,252,0.18) !important;
                color: #e6edf3 !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="checkbox"] span {{
                border-color: rgba(240,246,252,0.35) !important;
            }}
            ''' if theme == "black" else ""}
        </style>
        """,
        unsafe_allow_html=True,
    )




def _build_merged_from_csv(base_dir: Path) -> pd.DataFrame:
    sales = pd.read_csv(
        base_dir / "sales.csv", parse_dates=["order_date"],
        usecols=["order_id", "order_date", "customer_id", "product_id", "store_id",
                 "quantity", "unit_price", "discount", "revenue", "profit"],
    )
    customers = pd.read_csv(
        base_dir / "customers.csv", parse_dates=["join_date"],
        usecols=["customer_id", "join_date", "age", "loyalty_member"],
    )
    products = pd.read_csv(
        base_dir / "products.csv",
        usecols=["product_id", "product_name", "brand", "category", "cocoa_percent", "weight_g"],
    )
    stores = pd.read_csv(
        base_dir / "stores.csv",
        usecols=["store_id", "city", "country", "store_type"],
    )

    merged = (
        sales.merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(stores, on="store_id", how="left")
    )

    merged["gross_sales"] = merged["quantity"] * merged["unit_price"]
    merged["discount_amount"] = (merged["gross_sales"] - merged["revenue"]).clip(lower=0)
    _safe_rev = merged["revenue"].where(merged["revenue"] != 0)
    merged["margin_rate"] = (merged["profit"] / _safe_rev).fillna(0)
    merged["avg_order_value"] = merged["revenue"]

    merged["age_bucket"] = pd.cut(
        merged["age"],
        bins=[0, 24, 34, 44, 54, 64, 120],
        labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        include_lowest=True,
    )
    tenure_days = (merged["order_date"] - merged["join_date"]).dt.days
    merged["customer_stage"] = None
    merged.loc[tenure_days <= 90, "customer_stage"] = "new"
    merged.loc[tenure_days > 90, "customer_stage"] = "existing"

    loyalty_map = {1: "member", 0: "non_member"}
    merged["loyalty_label"] = merged["loyalty_member"].map(loyalty_map).fillna("unknown")

    rfm_full = build_rfm(merged)
    merged = merged.merge(
        rfm_full[["customer_id", "rfm_segment", "recency_days", "r_score", "f_score", "m_score", "frequency", "monetary"]],
        on="customer_id", how="left",
    )
    return merged


@st.cache_resource(show_spinner="載入資料中…")
def load_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = _build_merged_from_csv(base_dir)
    merged["_order_date"] = merged["order_date"].dt.date

    quality = pd.DataFrame(
        {
            "loaded_rows": [len(merged)],
            "date_min": [merged["order_date"].min()],
            "date_max": [merged["order_date"].max()],
            "null_cols": [int((merged.isna().sum() > 0).sum())],
        }
    )
    return merged, quality


def apply_filters(
    df: pd.DataFrame, lang: str
) -> tuple[pd.DataFrame, pd.DataFrame, datetime.date | None, datetime.date | None, bool]:
    st.sidebar.subheader(t(lang, "global_filters"))

    date_min, date_max = df["_order_date"].min(), df["_order_date"].max()
    selected_dates = st.sidebar.date_input(
        t(lang, "date_range"),
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = date_min, date_max

    # Comparison period — opt-in via checkbox
    comp_enabled = st.sidebar.checkbox(t(lang, "enable_comparison"), value=False)
    if comp_enabled:
        _duration = end_date - start_date
        _default_comp_end = max(start_date - datetime.timedelta(days=1), date_min)
        _default_comp_start = max(_default_comp_end - _duration, date_min)
        comp_dates = st.sidebar.date_input(
            t(lang, "comparison_range"),
            value=(_default_comp_start, _default_comp_end),
            min_value=date_min,
            max_value=date_max,
            key="comparison_dates",
        )
        if isinstance(comp_dates, tuple) and len(comp_dates) == 2:
            comp_start, comp_end = comp_dates
        else:
            comp_start, comp_end = _default_comp_start, _default_comp_end
    else:
        comp_start, comp_end = None, None

    _all_countries = sorted(df["country"].dropna().unique().tolist())
    _country_disp, _country_rev = _display_opts(_all_countries, "country", lang)
    _country_sel = st.sidebar.multiselect(t(lang, "country"), _country_disp, placeholder=_ph(lang))
    countries = [_country_rev[v] for v in _country_sel]

    _avail_cities_raw = (
        df["city"].dropna().unique().tolist() if not countries
        else df[df["country"].isin(countries)]["city"].dropna().unique().tolist()
    )
    _city_disp, _city_rev = _display_opts(sorted(_avail_cities_raw), "city", lang)
    _city_sel = st.sidebar.multiselect(t(lang, "city"), _city_disp, placeholder=_ph(lang))
    cities = [_city_rev[v] for v in _city_sel]

    _all_store_types = sorted(df["store_type"].dropna().unique().tolist())
    _st_disp, _st_rev = _display_opts(_all_store_types, "store_type", lang)
    _st_sel = st.sidebar.multiselect(t(lang, "store_type"), _st_disp, placeholder=_ph(lang))
    store_types = [_st_rev[v] for v in _st_sel]

    brands = st.sidebar.multiselect(t(lang, "brand"), sorted(df["brand"].dropna().unique()), placeholder=_ph(lang))

    _all_categories = sorted(df["category"].dropna().unique().tolist())
    _cat_disp, _cat_rev = _display_opts(_all_categories, "category", lang)
    _cat_sel = st.sidebar.multiselect(t(lang, "category"), _cat_disp, placeholder=_ph(lang))
    categories = [_cat_rev[v] for v in _cat_sel]

    loyalty_options = [t(lang, "member"), t(lang, "non_member")]
    loyalty_selection = st.sidebar.multiselect(t(lang, "loyalty"), loyalty_options, placeholder=_ph(lang))
    loyalty_filter_map = {
        t(lang, "member"): "member",
        t(lang, "non_member"): "non_member",
    }

    # Apply non-date filters to build base_df (used for prior-period KPI lookups)
    base_df = df
    if countries:
        base_df = base_df[base_df["country"].isin(countries)]
    if cities:
        base_df = base_df[base_df["city"].isin(cities)]
    if store_types:
        base_df = base_df[base_df["store_type"].isin(store_types)]
    if brands:
        base_df = base_df[base_df["brand"].isin(brands)]
    if categories:
        base_df = base_df[base_df["category"].isin(categories)]
    if loyalty_selection:
        mapped_values = [loyalty_filter_map[v] for v in loyalty_selection]
        base_df = base_df[base_df["loyalty_label"].isin(mapped_values)]

    filtered = base_df[(base_df["_order_date"] >= start_date) & (base_df["_order_date"] <= end_date)]

    return filtered, base_df, comp_start, comp_end, comp_enabled


def render_kpi(
    df: pd.DataFrame,
    lang: str,
    base_df: pd.DataFrame,
    comp_start: datetime.date | None,
    comp_end: datetime.date | None,
    comp_enabled: bool,
) -> None:
    revenue = df["revenue"].sum()
    profit = df["profit"].sum()
    orders = df["order_id"].nunique()
    customers = df["customer_id"].nunique()
    margin = (profit / revenue) if revenue else 0
    aov = (revenue / orders) if orders else 0
    avg_discount = df["discount"].mean() if len(df) else 0

    revenue_delta: str | None = None
    if comp_enabled and comp_start is not None and comp_end is not None:
        prior_df = base_df[(base_df["_order_date"] >= comp_start) & (base_df["_order_date"] <= comp_end)]
        prior_revenue = prior_df["revenue"].sum()
        if prior_revenue > 0:
            pct = (revenue - prior_revenue) / prior_revenue * 100
            revenue_delta = f"{pct:+.1f}% vs {comp_start} ~ {comp_end}"

    # Row 1 — financial KPIs (4 cols)
    row1 = st.columns(4)
    with row1[0]:
        st.metric(t(lang, "kpi_revenue"), _fmt_money(revenue), revenue_delta)
    with row1[1]:
        st.metric(t(lang, "kpi_profit"), _fmt_money(profit))
    with row1[2]:
        st.metric(t(lang, "kpi_margin"), f"{margin:.2%}")
    with row1[3]:
        st.metric(t(lang, "kpi_aov"), f"${aov:,.2f}")

    # Row 2 — volume / engagement KPIs (3 cols)
    row2 = st.columns(3)
    with row2[0]:
        st.metric(t(lang, "kpi_orders"), _fmt_count(orders))
    with row2[1]:
        st.metric(t(lang, "kpi_customers"), _fmt_count(customers))
    with row2[2]:
        st.metric(t(lang, "kpi_discount"), f"{avg_discount:.2%}")


def render_overview(df: pd.DataFrame, lang: str) -> None:
    monthly = (
        df.set_index("order_date")
        .resample("ME")[["revenue", "profit"]]
        .sum()
        .reset_index()
    )
    trend = px.line(
        monthly,
        x="order_date",
        y=["revenue", "profit"],
        markers=True,
        title=t(lang, "trend_title"),
        template=_plotly_tpl(),
    )
    trend.update_xaxes(title="Date" if lang == "en" else "日期")
    trend.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    trend.update_layout(hovermode="x unified", height=400)
    st.plotly_chart(trend, use_container_width=True)

    seg = df.groupby("loyalty_label", as_index=False)[["revenue", "profit"]].sum()
    seg["loyalty_label"] = seg["loyalty_label"].map(
        {
            "member": t(lang, "member"),
            "non_member": t(lang, "non_member"),
            "unknown": "Unknown",
        }
    )
    seg_fig = px.bar(
        seg,
        x="loyalty_label",
        y=["revenue", "profit"],
        barmode="group",
        title=t(lang, "segment_title"),
        template=_plotly_tpl(),
    )
    seg_fig.update_xaxes(title="Loyalty Status" if lang == "en" else "會員狀態")
    seg_fig.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    seg_fig.update_layout(hovermode="x unified", height=400)
    st.plotly_chart(seg_fig, use_container_width=True)


def render_customer(df: pd.DataFrame, lang: str) -> None:
    period_note = f"{df['order_date'].min().date()} ~ {df['order_date'].max().date()}"

    stage = df.groupby("customer_stage", as_index=False)["revenue"].sum()
    stage["customer_stage"] = stage["customer_stage"].astype(str).replace({"new": "New", "existing": "Existing", "<NA>": "Unknown", "nan": "Unknown"})
    stage_fig = px.pie(
        stage, names="customer_stage", values="revenue", hole=0.5,
        title=f"{t(lang, 'cohort_title')} ({period_note})",
    )
    stage_fig.update_layout(height=400)
    st.plotly_chart(stage_fig, use_container_width=True)

    age = df.groupby("age_bucket", as_index=False)["customer_id"].nunique().rename(columns={"customer_id": "active_customers"})
    age_fig = px.bar(age, x="age_bucket", y="active_customers", title=t(lang, "age_title"), template=_plotly_tpl())
    age_fig.update_xaxes(title="Age Group" if lang == "en" else "年齡段")
    age_fig.update_yaxes(title="Customer Count" if lang == "en" else "客戶數", tickformat=",d")
    age_fig.update_layout(height=400)
    st.plotly_chart(age_fig, use_container_width=True)

    seg = df.groupby("rfm_segment", as_index=False).agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"))
    seg = seg.sort_values("revenue", ascending=False)

    seg_fig = px.bar(
        seg,
        x="rfm_segment",
        y="customers",
        color="revenue",
        title=f"{t(lang, 'rfm_segment_title')} ({period_note})",
        template=_plotly_tpl(),
    )
    seg_fig.update_xaxes(title="RFM Segment" if lang == "en" else "RFM 客群")
    seg_fig.update_yaxes(title="Customer Count" if lang == "en" else "客戶數", tickformat=",d")
    seg_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(seg_fig, use_container_width=True)

    # One point per customer (customer-level RFM values, not transaction-level)
    rfm_scatter_df = (
        df[["customer_id", "frequency", "monetary", "rfm_segment", "r_score", "f_score", "m_score"]]
        .drop_duplicates(subset="customer_id")
    )
    scatter = px.scatter(
        rfm_scatter_df,
        x="frequency",
        y="monetary",
        color="rfm_segment",
        size="monetary",
        hover_data=["customer_id", "r_score", "f_score", "m_score"],
        title=t(lang, "rfm_scatter_title"),
        template=_plotly_tpl(),
        opacity=0.7,
    )
    scatter.update_xaxes(title="Purchase Frequency" if lang == "en" else "購買頻次", tickformat=",d")
    scatter.update_yaxes(title="Lifetime Monetary Value ($)" if lang == "en" else "消費金額 ($)", tickprefix="$", tickformat=",.0f")
    scatter.update_layout(height=450, hovermode="closest")
    st.plotly_chart(scatter, use_container_width=True)

    st.markdown(f"**{t(lang, 'rfm_table_title')}**")
    _rev_col = t(lang, "rfm_revenue")
    _cust_col = t(lang, "rfm_customer_count")
    summary = seg.rename(columns={"rfm_segment": t(lang, "rfm_segment"), "customers": _cust_col, "revenue": _rev_col})
    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            _cust_col: st.column_config.NumberColumn(format="%,d"),
            _rev_col:  st.column_config.NumberColumn(format="$%,.0f"),
        },
    )


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("customer_id", as_index=False)
        .agg(
            last_order_date=("order_date", "max"),
            frequency=("order_id", "nunique"),
            monetary=("revenue", "sum"),
        )
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_order_date"]).dt.days

    rfm["r_score"] = score_to_quintile(rfm["recency_days"], low_is_better=True)
    rfm["f_score"] = score_to_quintile(rfm["frequency"], low_is_better=False)
    rfm["m_score"] = score_to_quintile(rfm["monetary"], low_is_better=False)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

    rfm["rfm_segment"] = "Potential"
    rfm.loc[(rfm["r_score"] >= 4) & (rfm["f_score"] >= 4) & (rfm["m_score"] >= 4), "rfm_segment"] = "Champions"
    rfm.loc[(rfm["r_score"] >= 3) & (rfm["f_score"] >= 3) & (rfm["m_score"] >= 3), "rfm_segment"] = "Loyal"
    rfm.loc[(rfm["r_score"] >= 4) & (rfm["f_score"] <= 2), "rfm_segment"] = "New"
    rfm.loc[(rfm["r_score"] <= 2) & (rfm["f_score"] >= 4) & (rfm["m_score"] >= 4), "rfm_segment"] = "At Risk High Value"
    rfm.loc[(rfm["r_score"] <= 2) & (rfm["f_score"] <= 2), "rfm_segment"] = "Hibernating"
    return rfm


def score_to_quintile(series: pd.Series, low_is_better: bool) -> pd.Series:
    ascending = not low_is_better
    ranks = series.rank(method="average", ascending=ascending, pct=True)
    scores = (ranks * 5).round().clip(lower=1, upper=5).astype(int)
    return scores


def render_product(df: pd.DataFrame, lang: str) -> None:
    top_n = 12
    brand = df.groupby("brand", as_index=False)[["revenue", "profit"]].sum().sort_values("revenue", ascending=False).head(top_n)
    brand_fig = px.bar(
        brand,
        x="brand",
        y=["revenue", "profit"],
        barmode="group",
        title=f"Top {top_n} · {t(lang, 'brand_title')}",
        template=_plotly_tpl(),
    )
    brand_fig.update_xaxes(title="Brand" if lang == "en" else "品牌")
    brand_fig.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    brand_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(brand_fig, use_container_width=True)

    category = df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    category_fig = px.treemap(category, path=["category"], values="revenue", title=t(lang, "category_title"))
    category_fig.update_traces(texttemplate="<b>%{label}</b><br>$%{value:,.0f}")
    category_fig.update_layout(height=400)
    st.plotly_chart(category_fig, use_container_width=True)

    cocoa = (
        df.groupby("cocoa_percent", as_index=False)[["revenue", "margin_rate"]]
        .mean()
        .sort_values("cocoa_percent")
    )
    cocoa_fig = px.scatter(
        cocoa,
        x="cocoa_percent",
        y="margin_rate",
        size="revenue",
        color="margin_rate",
        title=t(lang, "cocoa_title"),
        template=_plotly_tpl(),
    )
    cocoa_fig.update_xaxes(title="Cocoa Percentage (%)" if lang == "en" else "可可百分比 (%)", ticksuffix="%")
    cocoa_fig.update_yaxes(title="Margin Rate" if lang == "en" else "毛利率", tickformat=".2%")
    cocoa_fig.update_layout(height=400, hovermode="closest")
    st.plotly_chart(cocoa_fig, use_container_width=True)


def render_store(df: pd.DataFrame, lang: str) -> None:
    country = df.groupby("country", as_index=False)[["revenue", "profit"]].sum().sort_values("revenue", ascending=False)
    country_fig = px.bar(
        country,
        x="country",
        y=["revenue", "profit"],
        barmode="group",
        title=t(lang, "store_country_title"),
        template=_plotly_tpl(),
    )
    country_fig.update_xaxes(title="Country" if lang == "en" else "國家")
    country_fig.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    country_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(country_fig, use_container_width=True)

    stype = df.groupby("store_type", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    stype_fig = px.pie(stype, names="store_type", values="revenue", title=t(lang, "store_type_title"))
    stype_fig.update_traces(texttemplate="%{label}<br>$%{value:,.0f}<br>(%{percent})")
    stype_fig.update_layout(height=400)
    st.plotly_chart(stype_fig, use_container_width=True)

    city = df.groupby("city", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(10)
    city_fig = px.bar(city, x="city", y="revenue", title=t(lang, "city_title"), template=_plotly_tpl())
    city_fig.update_xaxes(title="City" if lang == "en" else "城市")
    city_fig.update_yaxes(title="Revenue ($)" if lang == "en" else "營收 ($)", tickprefix="$", tickformat=",.0f")
    city_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(city_fig, use_container_width=True)


def render_discount(df: pd.DataFrame, lang: str) -> None:
    bins = [-0.001, 0.0, 0.05, 0.10, 0.15, 1.0]
    labels = ["0%", "0-5%", "5-10%", "10-15%", "15%+"]

    work = df.copy()
    work["discount_bucket"] = pd.cut(work["discount"], bins=bins, labels=labels)

    bucket = (
        work.groupby("discount_bucket", as_index=False)
        .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"), profit=("profit", "sum"), margin_rate=("margin_rate", "mean"))
        .fillna(0)
    )

    bucket_fig = px.bar(
        bucket,
        x="discount_bucket",
        y=["revenue", "profit"],
        barmode="group",
        title=t(lang, "discount_bucket_title"),
        template=_plotly_tpl(),
    )
    bucket_fig.update_xaxes(title="Discount Bucket" if lang == "en" else "折扣區間")
    bucket_fig.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    bucket_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(bucket_fig, use_container_width=True)

    total_n = len(work)
    sample_n = min(total_n, 3000)
    scatter = px.scatter(
        work.sample(sample_n, random_state=42),
        x="discount",
        y="margin_rate",
        color="store_type",
        title=f"{t(lang, 'discount_scatter_title')} (n={sample_n:,} / {total_n:,})",
        template=_plotly_tpl(),
        opacity=0.6,
    )
    scatter.update_xaxes(title="Discount Rate" if lang == "en" else "折扣率", tickformat=".0%")
    scatter.update_yaxes(title="Margin Rate" if lang == "en" else "毛利率", tickformat=".2%")
    scatter.update_layout(height=400, hovermode="closest")
    st.plotly_chart(scatter, use_container_width=True)


def render_advanced_analytics(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "advanced_analytics"))
    
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs(
        [t(lang, "cac_ltv"), t(lang, "promo_roi"), t(lang, "marketing_funnel")]
    )
    
    with analytics_tab1:
        render_cac_ltv_analysis(df, lang)
    
    with analytics_tab2:
        render_promo_roi_analysis(df, lang)
    
    with analytics_tab3:
        render_marketing_funnel(df, lang)


def render_cac_ltv_analysis(df: pd.DataFrame, lang: str) -> None:
    new_customers = df[df["customer_stage"] == "new"].copy()
    existing_customers = df[df["customer_stage"] == "existing"].copy()
    
    new_discount_amount = new_customers["discount_amount"].sum()
    unique_new = new_customers["customer_id"].nunique()

    cac = (new_discount_amount / unique_new) if unique_new > 0 else 0
    
    new_ltv = new_customers.groupby("customer_id")["revenue"].sum().mean() if len(new_customers) > 0 else 0
    existing_ltv = existing_customers.groupby("customer_id")["revenue"].sum().mean() if len(existing_customers) > 0 else 0
    
    ltv_ratio = (existing_ltv / cac) if cac > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric(t(lang, "cac"), f"${cac:,.2f}")
    col2.metric(t(lang, "ltv"), f"${existing_ltv:,.2f}")
    col3.metric(t(lang, "ltv_cac_ratio"), f"{ltv_ratio:.2f}x", f"{'✅ Healthy' if ltv_ratio >= 3 else '⚠️ Needs Improvement'}")
    
    cohort_comparison = pd.DataFrame({
        "Customer Type": ["New", "Existing"],
        "Avg LTV": [new_ltv, existing_ltv],
        "Orders": [
            new_customers["customer_id"].nunique(),
            existing_customers["customer_id"].nunique()
        ]
    })
    cohort_fig = px.bar(
        cohort_comparison,
        x="Customer Type",
        y="Avg LTV",
        color="Orders",
        title=t(lang, "cohort_ltv_title"),
        template=_plotly_tpl(),
    )
    cohort_fig.update_xaxes(title="Cohort Type" if lang == "en" else "客戶類別")
    cohort_fig.update_yaxes(title="Avg LTV ($)" if lang == "en" else "平均 LTV ($)", tickprefix="$", tickformat=",.0f")
    cohort_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(cohort_fig, use_container_width=True)


def render_promo_roi_analysis(df: pd.DataFrame, lang: str) -> None:
    work = df.copy()
    bins = [-0.001, 0.0, 0.05, 0.10, 0.15, 1.0]
    labels = ["0%", "0-5%", "5-10%", "10-15%", "15%+"]
    work["discount_bucket"] = pd.cut(work["discount"], bins=bins, labels=labels)
    
    roi_analysis = (
        work.groupby("discount_bucket", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            discount_cost=("discount_amount", "sum")
        )
    )
    
    # profit already reflects discount deduction (revenue = gross_sales - discount)
    # ROI = profit return per dollar of discount invested
    _safe_cost = roi_analysis["discount_cost"].where(roi_analysis["discount_cost"] != 0)
    roi_analysis["roi_percent"] = (roi_analysis["profit"] / _safe_cost * 100).fillna(0)
    
    best_roi = roi_analysis.loc[roi_analysis["roi_percent"].idxmax()] if len(roi_analysis) > 0 else None
    
    if best_roi is not None:
        st.success(f"Best strategy: {best_roi['discount_bucket']} (ROI: {best_roi['roi_percent']:.2f}%)")
    
    roi_fig = px.bar(
        roi_analysis,
        x="discount_bucket",
        y=["revenue", "profit"],
        barmode="group",
        title=t(lang, "discount_roi_title"),
        template=_plotly_tpl(),
    )
    roi_fig.update_xaxes(title="Discount Bucket" if lang == "en" else "折扣區間")
    roi_fig.update_yaxes(title="Amount ($)" if lang == "en" else "金額 ($)", tickprefix="$", tickformat=",.0f")
    roi_fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(roi_fig, use_container_width=True)

    st.markdown("**ROI Analysis Detail**")
    roi_display = roi_analysis[["discount_bucket", "orders", "revenue", "profit", "discount_cost", "roi_percent"]].copy()
    roi_display.columns = ["Discount Bucket", "Orders", "Revenue ($)", "Profit ($)", "Discount Cost ($)", "ROI (%)"]
    st.dataframe(
        roi_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Orders":            st.column_config.NumberColumn(format="%,d"),
            "Revenue ($)":       st.column_config.NumberColumn(format="$%,.0f"),
            "Profit ($)":        st.column_config.NumberColumn(format="$%,.0f"),
            "Discount Cost ($)": st.column_config.NumberColumn(format="$%,.0f"),
            "ROI (%)":           st.column_config.NumberColumn(format="%.2f%%"),
        },
    )


def render_marketing_funnel(df: pd.DataFrame, lang: str) -> None:
    customers_count = df["customer_id"].nunique()
    order_counts = df.groupby("customer_id")["order_id"].nunique()
    repeat_count = int((order_counts > 1).sum())   # ≥2 orders
    loyal_count = int((order_counts >= 3).sum())   # ≥3 orders

    repeat_rate = (repeat_count / customers_count * 100) if customers_count > 0 else 0
    loyal_rate = (loyal_count / customers_count * 100) if customers_count > 0 else 0

    stage_labels = (
        ["活躍客戶", "複購客戶 (≥2筆)", "忠實客戶 (≥3筆)"]
        if lang == "zh-TW"
        else ["Active Customers", "Repeat Buyers (≥2 orders)", "Loyal Buyers (≥3 orders)"]
    )

    funnel_data = pd.DataFrame({
        "Stage": stage_labels,
        "Count": [customers_count, repeat_count, loyal_count],
    })

    funnel_fig = px.funnel(
        funnel_data,
        x="Count",
        y="Stage",
        title=t(lang, "funnel_metrics_title"),
        template=_plotly_tpl(),
    )
    funnel_fig.update_xaxes(title="Count" if lang == "en" else "數量", tickformat=",d")
    funnel_fig.update_layout(height=400, hovermode="closest")
    st.plotly_chart(funnel_fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Active Customers" if lang == "en" else "活躍客戶", f"{customers_count:,}")
    col2.metric(t(lang, "repeat_rate"), f"{repeat_rate:.2f}%")
    col3.metric("Loyal Rate (≥3)" if lang == "en" else "忠實率 (≥3筆)", f"{loyal_rate:.2f}%")



def render_threat_alert(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "threat_alert"))
    
    alert_cols = st.columns(2)
    
    with alert_cols[0]:
        st.markdown(f"### {t(lang, 'churn_risk')}", )
        churn_risk = calculate_churn_risk(df)
        if len(churn_risk) == 0:
            st.info(t(lang, "no_alerts"))
        else:
            churn_risk_display = churn_risk[["customer_id", "rfm_segment", "recency_days", "frequency", "monetary", "churn_score"]].copy()
            churn_risk_display.columns = ["客戶", "RFM", "天數", "頻次", "金額", "風險分"]
            
            for _, row in churn_risk.head(5).iterrows():
                risk_level = "🔴 " if row["churn_score"] > 0.7 else ("🟠 " if row["churn_score"] > 0.5 else "🟡 ")
                st.warning(
                    f"{risk_level} {row['customer_id']} | RFM: {row['rfm_segment']} | Risk: {row['churn_score']:.2f}"
                )
    
    with alert_cols[1]:
        st.markdown(f"### {t(lang, 'margin_decline')}", )
        margin_decline = calculate_margin_decline(df)
        if len(margin_decline) == 0:
            st.info(t(lang, "no_alerts"))
        else:
            for _, row in margin_decline.head(5).iterrows():
                st.error(
                    f"⛔ {row['product_name']} | 毛利率: {row['margin_rate']:.2%} | 銷量: {row['quantity']:,}"
                )
    
    st.markdown("---")
    st.markdown(f"**{t(lang, 'churn_detail_title')}**")
    churn_detail = churn_risk.head(10)[["customer_id", "rfm_segment", "recency_days", "frequency", "monetary"]].copy()
    churn_detail.columns = ["Customer ID", "RFM Segment", "Recency (days)", "Frequency", "Monetary ($)"]
    st.dataframe(
        churn_detail,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Recency (days)": st.column_config.NumberColumn(format="%,d days"),
            "Frequency":      st.column_config.NumberColumn(format="%,d"),
            "Monetary ($)":   st.column_config.NumberColumn(format="$%,.0f"),
        },
    )


_CHURN_RECENCY_W = 0.5    # recency is the strongest churn signal
_CHURN_FREQUENCY_W = 0.3
_CHURN_MONETARY_W = 0.2


def calculate_churn_risk(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)
    
    rfm = (
        df.groupby("customer_id", as_index=False)
        .agg(
            last_order_date=("order_date", "max"),
            frequency=("order_id", "nunique"),
            monetary=("revenue", "sum"),
            rfm_segment=("rfm_segment", "first"),
        )
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_order_date"]).dt.days
    
    max_recency = rfm["recency_days"].quantile(0.75)
    min_frequency = rfm["frequency"].quantile(0.25)
    min_monetary = rfm["monetary"].quantile(0.75)
    
    rfm["recency_norm"] = (rfm["recency_days"] / max_recency).clip(0, 1)
    rfm["frequency_norm"] = (min_frequency / (rfm["frequency"] + 1)).clip(0, 1)
    rfm["monetary_norm"] = (min_monetary / (rfm["monetary"] + 1)).clip(0, 1)
    
    rfm["churn_score"] = (
        _CHURN_RECENCY_W * rfm["recency_norm"]
        + _CHURN_FREQUENCY_W * rfm["frequency_norm"]
        + _CHURN_MONETARY_W * rfm["monetary_norm"]
    )
    
    at_risk = rfm[(rfm["monetary"] > rfm["monetary"].quantile(0.5)) & (rfm["churn_score"] > 0.4)].sort_values("churn_score", ascending=False)
    return at_risk


def calculate_margin_decline(df: pd.DataFrame) -> pd.DataFrame:
    product_metrics = (
        df.groupby("product_id", as_index=False)
        .agg(
            product_name=("product_name", "first"),
            brand=("brand", "first"),
            quantity=("quantity", "sum"),
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            margin_rate=("margin_rate", "mean"),
        )
    )
    
    product_metrics["margin_status"] = "normal"
    product_metrics.loc[
        (product_metrics["margin_rate"] < 0.2) & (product_metrics["quantity"] > 10),
        "margin_status"
    ] = "alert"
    
    decline_products = product_metrics[product_metrics["margin_status"] == "alert"].sort_values("margin_rate")
    return decline_products


def render_data_quality(quality: pd.DataFrame, lang: str) -> None:
    row = quality.iloc[0]
    with st.expander(t(lang, "data_quality"), expanded=False):
        st.write(f"{t(lang, 'loaded_rows')}: {int(row['loaded_rows']):,}")
        st.write(f"{t(lang, 'date_coverage')}: {row['date_min'].date()} ~ {row['date_max'].date()}")
        st.write(f"{t(lang, 'null_count')}: {int(row['null_cols'])}")


def main() -> None:
    st.set_page_config(page_title="MarTech行銷報表", page_icon="📊", layout="wide")

    _lang_now = st.session_state.get("_lang_sel", "zh-TW")
    _lang_label = "語言" if _lang_now == "zh-TW" else "Language"
    _LANG_DISPLAY = {"zh-TW": "繁體中文 / Traditional Chinese", "en": "英文 / English"}
    lang = st.sidebar.selectbox(
        _lang_label,
        options=["zh-TW", "en"],
        format_func=lambda x: _LANG_DISPLAY[x],
        index=0,
        key="_lang_sel",
    )
    theme = st.sidebar.selectbox(
        t(lang, "theme"),
        options=list(_THEME_LABELS[lang].keys()),
        format_func=lambda k: _THEME_LABELS[lang][k],
        key="theme_select",
    )

    _inject_style(theme)

    st.markdown(
        f"""
        <div class='dashboard-hero'>
            <h1>{t(lang, 'title')}</h1>
            <p>{t(lang, 'subtitle')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_dir = Path(__file__).parent / "data"
    df, quality = load_data(base_dir)
    filtered, base_df, comp_start, comp_end, comp_enabled = apply_filters(df, lang)

    if filtered.empty:
        st.warning(t(lang, "empty_data"))
        render_data_quality(quality, lang)
        return

    render_kpi(filtered, lang, base_df, comp_start, comp_end, comp_enabled)

    tabs = st.tabs(
        [
            t(lang, "overview"),
            t(lang, "customer"),
            t(lang, "product"),
            t(lang, "store"),
            t(lang, "discount"),
            t(lang, "brand_positioning"),
            t(lang, "advanced_analytics"),
            t(lang, "threat_alert"),
        ]
    )

    with tabs[0]:
        try:
            render_overview(filtered, lang)
        except Exception as e:
            st.error(f"Error in Overview tab: {str(e)}")
    with tabs[1]:
        try:
            render_customer(filtered, lang)
        except Exception as e:
            st.error(f"Error in Customer tab: {str(e)}")
    with tabs[2]:
        try:
            render_product(filtered, lang)
        except Exception as e:
            st.error(f"Error in Product tab: {str(e)}")
    with tabs[3]:
        try:
            render_store(filtered, lang)
        except Exception as e:
            st.error(f"Error in Store tab: {str(e)}")
    with tabs[4]:
        try:
            render_discount(filtered, lang)
        except Exception as e:
            st.error(f"Error in Discount tab: {str(e)}")
    with tabs[5]:
        try:
            render_brand_positioning(filtered, lang)
        except Exception as e:
            st.error(f"Error in Brand Positioning tab: {str(e)}")
    with tabs[6]:
        try:
            render_advanced_analytics(filtered, lang)
        except Exception as e:
            st.error(f"Error in Advanced Analytics tab: {str(e)}")
    with tabs[7]:
        try:
            render_threat_alert(filtered, lang)
        except Exception as e:
            st.error(f"Error in Threat Alert tab: {str(e)}")

    render_data_quality(quality, lang)
    st.caption(t(lang, "footer"))


if __name__ == "__main__":
    main()
