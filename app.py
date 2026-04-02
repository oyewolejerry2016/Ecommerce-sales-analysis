import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ─────────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit command
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title = "Product Recommendation System",
    page_icon  = "🛒",
    layout     = "wide"
)

# ─────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'customer_recommendations.csv')
    df        = pd.read_csv(file_path)
    return df

df = load_data()

# ─────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=80)
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
    st.markdown("This app provides personalized product category recommendations based on customer purchase behavior.")

# ─────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────
st.title("🛒 Product Recommendation System")
st.markdown("*Personalized product category recommendations powered by collaborative filtering*")
st.divider()

# ─────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────
# CUSTOMER LOOKUP RESULT
# ─────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────
st.subheader("📊 Recommendation Insights")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    rec_counts = df['Recommendation_1'].value_counts().reset_index()
    rec_counts.columns = ['Category', 'Count']
    
    fig1 = px.bar(
        rec_counts,
        x                    = 'Category',
        y                    = 'Count',
        title                = 'Most Frequently Recommended Categories',
        color                = 'Count',
        color_continuous_scale = 'Blues',
        text                 = 'Count'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        showlegend       = False,
        plot_bgcolor     = 'white',
        xaxis_title      = 'Product Category',
        yaxis_title      = 'Number of Customers'
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    fig2 = px.pie(
        rec_counts,
        names  = 'Category',
        values = 'Count',
        title  = 'Recommendation Distribution',
        hole   = 0.4,
        color_discrete_sequence = px.colors.sequential.Blues_r
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────
# SECOND ROW CHARTS
# ─────────────────────────────────────────────────
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    # Top 2 recommendations combined
    rec2_counts = df['Recommendation_2'].value_counts().reset_index()
    rec2_counts.columns = ['Category', 'Count']
    
    fig3 = px.bar(
        rec2_counts,
        x                    = 'Category',
        y                    = 'Count',
        title                = '2nd Most Recommended Categories',
        color                = 'Count',
        color_continuous_scale = 'Blues',
        text                 = 'Count'
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(
        showlegend   = False,
        plot_bgcolor = 'white',
        xaxis_title  = 'Product Category',
        yaxis_title  = 'Number of Customers'
    )
    st.plotly_chart(fig3, use_container_width=True)

with chart_col4:
    rec3_counts = df['Recommendation_3'].value_counts().reset_index()
    rec3_counts.columns = ['Category', 'Count']
    
    fig4 = px.bar(
        rec3_counts,
        x                      = 'Category',
        y                      = 'Count',
        title                  = '3rd Most Recommended Categories',
        color                  = 'Count',
        color_continuous_scale = 'Blues',
        text                   = 'Count'
    )
    fig4.update_traces(textposition='outside')
    fig4.update_layout(
        showlegend   = False,
        plot_bgcolor = 'white',
        xaxis_title  = 'Product Category',
        yaxis_title  = 'Number of Customers',
        yaxis        = dict(rangemode='tozero')
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────
# FULL RECOMMENDATIONS TABLE
# ─────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with Streamlit | E-Commerce Product Recommendation System</p>",
    unsafe_allow_html=True
)
