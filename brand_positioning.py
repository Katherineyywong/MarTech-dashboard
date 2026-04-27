"""Brand Positioning Analysis Module for MarTech Dashboard"""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_brand_positioning(df: pd.DataFrame, lang: str) -> None:
    """Render brand positioning analysis page"""
    st.subheader("品牌定位分析" if lang == "zh-TW" else "Brand Positioning Analysis")
    
    brand_positioning = calculate_brand_positioning(df)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("**定位屬性評分表**" if lang == "zh-TW" else "**Positioning Attributes Scorecard**")
        display_df = brand_positioning[[
            "Brand", "Cocoa", "Luxury", "Complex", "Size", 
            "Tradition", "Prestige", "Flavor", "Feel", "Volume", "Profit"
        ]].copy()
        display_df["Cocoa"] = display_df["Cocoa"].round(1)
        display_df["Luxury"] = display_df["Luxury"].round(1)
        display_df["Complex"] = display_df["Complex"].round(1)
        display_df["Size"] = display_df["Size"].round(1)
        display_df["Tradition"] = display_df["Tradition"].round(1)
        display_df["Prestige"] = display_df["Prestige"].round(1)
        display_df["Flavor"] = display_df["Flavor"].round(1)
        display_df["Feel"] = display_df["Feel"].round(1)
        display_df["Profit"] = display_df["Profit"].round(1)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**2D 定位圖：奢侈度 vs 複雜度**" if lang == "zh-TW" else "**Positioning Map: Luxury vs Complexity**")
        _tpl = "plotly_dark" if st.session_state.get("theme_select") == "black" else "plotly_white"
        positioning_fig = px.scatter(
            brand_positioning,
            x="Luxury",
            y="Complex",
            size="Volume",
            color="Profit",
            hover_name="Brand",
            hover_data={"Luxury": ":.1f", "Complex": ":.1f", "Profit": ":.1f", "Volume": ":.0f"},
            title="品牌定位象限圖" if lang == "zh-TW" else "Brand Positioning Quadrant",
            template=_tpl,
            color_continuous_scale="RdYlGn",
            size_max=50,
        )
        positioning_fig.update_xaxes(range=[0, 10], title="奢侈程度" if lang == "zh-TW" else "Luxury Level")
        positioning_fig.update_yaxes(range=[0, 10], title="複雜程度" if lang == "zh-TW" else "Complexity Level")
        positioning_fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
        positioning_fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
        st.plotly_chart(positioning_fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### " + ("定位屬性說明" if lang == "zh-TW" else "Positioning Attributes Definition"))
    
    attributes_desc = {
        "zh-TW": {
            "Cocoa": "可可濃度 (1-10)：產品平均可可含量，高=70%+，低=<50%",
            "Luxury": "奢侈程度 (1-10)：基於毛利率，高毛利=高奢侈感",
            "Complex": "複雜程度 (1-10)：可可強度(60%) + 重量(40%)，風味與生產複雜度",
            "Size": "重量尺寸 (1-10)：基於產品平均重量",
            "Tradition": "傳統指數 (1-10)：收益排名反轉，高=品牌歷史強勢",
            "Prestige": "聲望指數 (1-10)：奢侈度(50%) + 傳統感(50%)，昂貴且有歷史的品牌",
            "Flavor": "風味豐富度 (1-10)：可可強度(60%) + 銷量多樣性代理(40%)",
            "Feel": "口感層次 (1-10)：重量(70%) + 可可(30%)，質地密度與濃度",
            "Volume": "銷售力 (相對值)：訂單數佔最大品牌的百分比",
            "Profit": "利潤貢獻度 (%)：毛利率百分比",
        },
        "en": {
            "Cocoa": "Cocoa Intensity (1-10): Avg cocoa %, high=70%+, low=<50%",
            "Luxury": "Luxury Level (1-10): Based on margin rate, high margin=high prestige",
            "Complex": "Complexity (1-10): Cocoa(60%) + Weight(40%), flavor & production complexity",
            "Size": "Physical Size (1-10): Based on average product weight",
            "Tradition": "Tradition Index (1-10): Inverse revenue rank, high=established brand",
            "Prestige": "Prestige Index (1-10): Luxury(50%) + Tradition(50%), expensive & heritage",
            "Flavor": "Flavor Diversity (1-10): Cocoa intensity(60%) + Volume diversity proxy(40%)",
            "Feel": "Mouth Feel (1-10): Weight(70%) + Cocoa(30%), texture density & intensity",
            "Volume": "Sales Power (relative): Order count as % of top brand",
            "Profit": "Profit Contribution (%): Margin rate percentage",
        }
    }
    
    desc_text = attributes_desc.get(lang, attributes_desc["en"])
    for attr, desc in desc_text.items():
        st.caption(f"• **{attr}**: {desc}")


def calculate_brand_positioning(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate brand positioning scores across 10 key attributes"""
    brand_metrics = (
        df.groupby("brand", as_index=False)
        .agg(
            cocoa_avg=("cocoa_percent", "mean"),
            weight_avg=("weight_g", "mean"),
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            margin_rate=("margin_rate", "mean"),
            orders=("order_id", "nunique"),
        )
    )
    
    brand_metrics = brand_metrics.sort_values("revenue", ascending=False)
    
    cocoa_norm = (brand_metrics["cocoa_avg"] / 100 * 10).clip(1, 10)
    margin_norm = ((brand_metrics["margin_rate"] * 100).clip(0, 50) / 5).clip(1, 10)
    weight_norm = (brand_metrics["weight_avg"] / 200 * 10).clip(1, 10)
    sales_rank = brand_metrics["revenue"].rank(method="dense", ascending=False) / len(brand_metrics) * 10
    volume_norm = (brand_metrics["orders"] / brand_metrics["orders"].max() * 10).clip(1, 10)
    tradition_norm = (11 - sales_rank).clip(1, 10)

    result = pd.DataFrame({
        "Brand": brand_metrics["brand"],
        "Cocoa": cocoa_norm,
        "Luxury": margin_norm,
        # cocoa(60%) + weight(40%): flavor depth × production complexity
        "Complex": (cocoa_norm * 0.6 + weight_norm * 0.4).clip(1, 10),
        "Size": weight_norm,
        "Tradition": tradition_norm,
        # margin(50%) + heritage(50%): expensive AND established
        "Prestige": ((margin_norm + tradition_norm) / 2).clip(1, 10),
        # cocoa intensity(60%) + volume diversity proxy(40%)
        "Flavor": (cocoa_norm * 0.6 + volume_norm * 0.4).clip(1, 10),
        # weight(70%) + cocoa(30%): texture density and intensity
        "Feel": (weight_norm * 0.7 + cocoa_norm * 0.3).clip(1, 10),
        "Volume": (brand_metrics["orders"] / brand_metrics["orders"].max() * 100).clip(1, 100),
        "Profit": (brand_metrics["margin_rate"] * 100).clip(0, 50),
    })
    
    return result
