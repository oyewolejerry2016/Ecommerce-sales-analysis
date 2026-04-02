import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# ── Page Config ──────────────────────────────────
st.set_page_config(
    page_title = "Product Recommendation System",
    page_icon  = "🛒",
    layout     = "wide"
)

# ── Load Data ─────────────────────────────────────
@st.cache_data
def load_data():
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'customer_recommendations.csv')
    return pd.read_csv(file_path)

df = load_data()

# ── Header ────────────────────────────────────────
st.title("🛒 Product Recommendation System")
st.markdown("*Personalized product category recommendations powered by collaborative filtering*")
st.divider()

# ── KPI Cards ─────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label = "👥 Total Customers",
        value = f"{len(df):,}"
    )
with col2:
    top_rec = df['Recommendation_1'].value_counts().index[0]
    st.metric(
        label = "🏆 Most Recommended",
        value = top_rec
    )
with col3:
    avg_score = round(df['Score_1'].mean(), 4)
    st.metric(
        label = "📊 Avg Score",
        value = avg_score
    )
with col4:
    total_categories = df['Recommendation_1'].nunique()
    st.metric(
        label = "🏷️ Total Categories",
        value = total_categories
    )

st.divider()

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.title("🔍 Customer Lookup")
    st.markdown("Enter a Customer ID to get personalized recommendations")
    st.divider()

    customer_id = st.text_input(
        "Customer ID",
        placeholder = "e.g. CUST_00001"
    ).strip().upper()

    search = st.button("Get Recommendations", type="primary", use_container_width=True)

    st.divider()
    st.markdown("**About**")
    st.markdown(
        "This app provides personalized product category "
        "recommendations based on customer purchase behavior."
    )

# ── Customer Lookup ───────────────────────────────
if search and customer_id:
    customer = df[df['Customer_ID'] == customer_id]

    if customer.empty:
        st.error(f"⚠️ Customer **{customer_id}** not found. Please check the ID and try again.")
    else:
        st.subheader(f"🎯 Results for {customer_id}")
        already_buys = customer['Already_Buys'].values[0]
        st.info(f"📦 **Already Buys:** {already_buys}")

        st.markdown("#### Top 3 Recommended Categories")
        rec_col1, rec_col2, rec_col3 = st.columns(3)

        with rec_col1:
            st.success(
                f"### 🥇 {customer['Recommendation_1'].values[0]}\n\n"
                f"**Similarity Score:** {customer['Score_1'].values[0]}"
            )
        with rec_col2:
            st.success(
                f"### 🥈 {customer['Recommendation_2'].values[0]}\n\n"
                f"**Similarity Score:** {customer['Score_2'].values[0]}"
            )
        with rec_col3:
            st.success(
                f"### 🥉 {customer['Recommendation_3'].values[0]}\n\n"
                f"**Similarity Score:** {customer['Score_3'].values[0]}"
            )
        st.divider()

elif search and not customer_id:
    st.warning("⚠️ Please enter a Customer ID first.")

# ── Charts ────────────────────────────────────────
st.subheader("📊 Recommendation Insights")

chart_col1, chart_col2 = st.columns(2)

# Bar Chart — Most Recommended Categories
with chart_col1:
    rec_counts = df['Recommendation_1'].value_counts().reset_index()
    rec_counts.columns = ['Category', 'Count']

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    bars = ax1.bar(
        rec_counts['Category'],
        rec_counts['Count'],
        color='#00274D',
        edgecolor='white'
    )
    for bar in bars:
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            str(int(bar.get_height())),
            ha='center', va='bottom',
            fontsize=9, color='#444444'
        )
    ax1.set_title('Most Frequently Recommended Categories', fontsize=12, fontweight='bold', color='#00274D')
    ax1.set_xlabel('Product Category', fontsize=10)
    ax1.set_ylabel('Number of Customers', fontsize=10)
    ax1.set_facecolor('#F4F4F4')
    fig1.patch.set_facecolor('white')
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

# Pie Chart — Recommendation Distribution
with chart_col2:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    colors = ['#00274D', '#2E75B6', '#5B9BD5', '#9DC3E6',
              '#003f7f', '#1a5fa8', '#4a8fc4', '#7ab5d8']
    wedges, texts, autotexts = ax2.pie(
        rec_counts['Count'],
        labels      = rec_counts['Category'],
        autopct     = '%1.1f%%',
        colors      = colors,
        startangle  = 90,
        wedgeprops  = dict(width=0.6)
    )
    for text in autotexts:
        text.set_fontsize(8)
        text.set_color('white')
    ax2.set_title('Recommendation Distribution', fontsize=12, fontweight='bold', color='#00274D')
    fig2.patch.set_facecolor('white')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

st.divider()

# Second Row Charts
chart_col3, chart_col4 = st.columns(2)

# 2nd Recommendation Bar Chart
with chart_col3:
    rec2_counts = df['Recommendation_2'].value_counts().reset_index()
    rec2_counts.columns = ['Category', 'Count']

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    bars3 = ax3.bar(
        rec2_counts['Category'],
        rec2_counts['Count'],
        color='#2E75B6',
        edgecolor='white'
    )
    for bar in bars3:
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            str(int(bar.get_height())),
            ha='center', va='bottom',
            fontsize=9, color='#444444'
        )
    ax3.set_title('2nd Most Recommended Categories', fontsize=12, fontweight='bold', color='#00274D')
    ax3.set_xlabel('Product Category', fontsize=10)
    ax3.set_ylabel('Number of Customers', fontsize=10)
    ax3.set_facecolor('#F4F4F4')
    fig3.patch.set_facecolor('white')
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

# 3rd Recommendation Bar Chart
with chart_col4:
    rec3_counts = df['Recommendation_3'].value_counts().reset_index()
    rec3_counts.columns = ['Category', 'Count']

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    bars4 = ax4.bar(
        rec3_counts['Category'],
        rec3_counts['Count'],
        color='#5B9BD5',
        edgecolor='white'
    )
    for bar in bars4:
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            str(int(bar.get_height())),
            ha='center', va='bottom',
            fontsize=9, color='#444444'
        )
    ax4.set_title('3rd Most Recommended Categories', fontsize=12, fontweight='bold', color='#00274D')
    ax4.set_xlabel('Product Category', fontsize=10)
    ax4.set_ylabel('Number of Customers', fontsize=10)
    ax4.set_facecolor('#F4F4F4')
    fig4.patch.set_facecolor('white')
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

st.divider()

# ── Full Recommendations Table ─────────────────────
st.subheader("📋 All Customer Recommendations")

search_filter = st.text_input(
    "🔎 Search by Customer ID, Category or What They Already Buy",
    placeholder = "Type to filter table..."
)

if search_filter:
    filtered_df = df[
        df['Customer_ID'].str.contains(search_filter, case=False, na=False)      |
        df['Already_Buys'].str.contains(search_filter, case=False, na=False)     |
        df['Recommendation_1'].str.contains(search_filter, case=False, na=False) |
        df['Recommendation_2'].str.contains(search_filter, case=False, na=False) |
        df['Recommendation_3'].str.contains(search_filter, case=False, na=False)
    ]
else:
    filtered_df = df

st.dataframe(
    filtered_df,
    use_container_width = True,
    height              = 400
)
st.caption(f"Showing **{len(filtered_df):,}** of **{len(df):,}** customers")

# ── Footer ────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with Streamlit | E-Commerce Product Recommendation System</p>",
    unsafe_allow_html=True
)
