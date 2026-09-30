# import streamlit as st
# import preprocessor
# import helper
# import matplotlib.pyplot as plt
# import seaborn as sns

# # ==================== PAGE CONFIG ====================
# st.set_page_config(
#     page_title="WhatsApp Chat Analyzer",
#     page_icon="💬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ==================== CUSTOM STYLING (CSS) ====================
# st.markdown("""
#     <style>
#     /* Headings ko dark aur sharp rakhne ke liye */
#     h1, h2, h3, h4, h5, h6 {
#         color: #1f2937 !important;
#         font-weight: 700 !important;
#     }
    
#     /* Metric cards styling */
#     .metric-card {
#         background-color: #f3f4f6;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
#         text-align: center;
#         border: 1px solid #e5e7eb;
#     }
#     </style>
# """, unsafe_allow_html=True)
# # ==================== SIDEBAR ====================
# st.sidebar.title("💬 Chat Analyzer")
# st.sidebar.markdown("### Upload Your WhatsApp Chat")

# uploaded_file = st.sidebar.file_uploader("Choose a .txt file", type=["txt"])

# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
    
#     with st.spinner("Processing chat data... Please wait 🚀"):
#         df = preprocessor.preprocess(data)

#     # Fetch unique users safely
#     user_list = df['user'].unique().tolist()
#     if 'group_notification' in user_list:
#         user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, 'Overall')

#     st.sidebar.markdown("---")
#     st.sidebar.subheader("📊 Filter Options")
#     selected_user = st.sidebar.selectbox("Show analysis with respect to:", user_list)

#     if st.sidebar.button("🚀 Show Analysis", use_container_width=True):
        
#         # Main Header
#         st.title(f"📈 Analytics Dashboard — [{selected_user}]")
#         st.markdown("---")

#         # ==================== TOP STATISTICS ====================
#         try:
#             num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
#             st.subheader("📌 Top Statistics")
            
#             col1, col2, col3, col4 = st.columns(4)

#             with col1:
#                 st.markdown(f"""
#                     <div class="metric-card">
#                         <p style="color: #a0aec0; font-size: 14px; margin-bottom: 0;">Total Messages</p>
#                         <h2 style="color: #00df9a; margin-top: 5px;">{num_messages:,}</h2>
#                     </div>
#                 """, unsafe_allow_html=True)

#             with col2:
#                 st.markdown(f"""
#                     <div class="metric-card">
#                         <p style="color: #a0aec0; font-size: 14px; margin-bottom: 0;">Total Words</p>
#                         <h2 style="color: #3b82f6; margin-top: 5px;">{words:,}</h2>
#                     </div>
#                 """, unsafe_allow_html=True)

#             with col3:
#                 st.markdown(f"""
#                     <div class="metric-card">
#                         <p style="color: #a0aec0; font-size: 14px; margin-bottom: 0;">Media Shared</p>
#                         <h2 style="color: #f59e0b; margin-top: 5px;">{num_media_messages:,}</h2>
#                     </div>
#                 """, unsafe_allow_html=True)

#             with col4:
#                 st.markdown(f"""
#                     <div class="metric-card">
#                         <p style="color: #a0aec0; font-size: 14px; margin-bottom: 0;">Links Shared</p>
#                         <h2 style="color: #ec4899; margin-top: 5px;">{num_links:,}</h2>
#                     </div>
#                 """, unsafe_allow_html=True)
                
#         except Exception as e:
#             st.error(f"Error loading stats: {e}")

#         st.markdown("<br>", unsafe_allow_html=True)

#         # ==================== TIMELINES ====================
#         col_t1, col_t2 = st.columns(2)

#         with col_t1:
#             st.subheader("📅 Monthly Timeline")
#             try:
#                 timeline = helper.monthly_timeline(selected_user, df)
#                 if timeline is not None and not timeline.empty:
#                     fig, ax = plt.subplots(figsize=(6, 4))
#                     ax.plot(timeline['time'], timeline['message'], color='#00df9a', marker='o', linewidth=2)
#                     plt.xticks(rotation='vertical')
#                     st.pyplot(fig)
#                 else:
#                     st.info("No data available for monthly timeline.")
#             except Exception:
#                 st.info("Could not generate monthly timeline.")

#         with col_t2:
#             st.subheader("📈 Daily Timeline")
#             try:
#                 daily_timeline = helper.daily_timeline(selected_user, df)
#                 if daily_timeline is not None and not daily_timeline.empty:
#                     fig, ax = plt.subplots(figsize=(6, 4))
#                     ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#3b82f6', linewidth=1.5)
#                     plt.xticks(rotation='vertical')
#                     st.pyplot(fig)
#                 else:
#                     st.info("No data available for daily timeline.")
#             except Exception:
#                 st.info("Could not generate daily timeline.")

#         st.markdown("---")

#         # ==================== ACTIVITY MAP ====================
#         st.subheader("⏰ Activity Map")
#         col_a1, col_a2 = st.columns(2)

#         with col_a1:
#             st.markdown("##### Most Busy Day")
#             try:
#                 busy_day = helper.week_activity_map(selected_user, df)
#                 if busy_day is not None and not busy_day.empty:
#                     fig, ax = plt.subplots(figsize=(5, 3.5))
#                     ax.bar(busy_day.index, busy_day.values, color='#8b5cf6')
#                     plt.xticks(rotation='vertical')
#                     st.pyplot(fig)
#                 else:
#                     st.info("No data.")
#             except Exception:
#                 st.info("Not enough data for busy day.")

#         with col_a2:
#             st.markdown("##### Most Busy Month")
#             try:
#                 busy_month = helper.month_activity_map(selected_user, df)
#                 if busy_month is not None and not busy_month.empty:
#                     fig, ax = plt.subplots(figsize=(5, 3.5))
#                     ax.bar(busy_month.index, busy_month.values, color='#f97316')
#                     plt.xticks(rotation='vertical')
#                     st.pyplot(fig)
#                 else:
#                     st.info("No data.")
#             except Exception:
#                 st.info("Not enough data for busy month.")

#         st.markdown("---")

#         # ==================== HEATMAP ====================
#         st.subheader("🔥 Weekly Activity Heatmap (Hourly)")
#         try:
#             user_heatmap = helper.activity_heatmap(selected_user, df)
#             if user_heatmap is not None and not user_heatmap.empty and user_heatmap.size > 0:
#                 fig, ax = plt.subplots(figsize=(10, 4))
#                 sns.heatmap(user_heatmap, ax=ax, cmap="Purples")
#                 st.pyplot(fig)
#             else:
#                 st.info("No data available for weekly activity heatmap.")
#         except Exception:
#             st.info("Heatmap could not be generated for this user/chat.")

#         # ==================== MOST BUSY USERS (GROUP) ====================
#         if selected_user == 'Overall':
#             st.markdown("---")
#             st.subheader("👑 Most Busy Users in Group")
#             try:
#                 x, new_df = helper.most_busy_users(df)
#                 if x is not None and not x.empty:
#                     col_u1, col_u2 = st.columns(2)
#                     with col_u1:
#                         fig, ax = plt.subplots(figsize=(5, 4))
#                         ax.bar(x.index, x.values, color='#ef4444')
#                         plt.xticks(rotation='vertical')
#                         st.pyplot(fig)
#                     with col_u2:
#                         st.dataframe(new_df, use_container_width=True)
#                 else:
#                     st.info("No busy users data available.")
#             except Exception:
#                 st.info("Could not analyze busy users.")

#         st.markdown("---")

#         # ==================== WORDCLOUD & COMMON WORDS ====================
#         col_w1, col_w2 = st.columns(2)

#         with col_w1:
#             st.subheader("☁️ Wordcloud")
#             try:
#                 df_wc = helper.create_wordcloud(selected_user, df)
#                 if df_wc is not None:
#                     fig, ax = plt.subplots(figsize=(5, 4))
#                     ax.imshow(df_wc)
#                     ax.axis('off')
#                     st.pyplot(fig)
#                 else:
#                     st.info("Not enough text to generate wordcloud.")
#             except Exception:
#                 st.info("Wordcloud could not be generated.")

#         with col_w2:
#             st.subheader("🔤 Most Common Words")
#             try:
#                 most_common_df = helper.most_common_words(selected_user, df)
#                 if most_common_df is not None and not most_common_df.empty:
#                     fig, ax = plt.subplots(figsize=(5, 4))
#                     ax.barh(most_common_df[0], most_common_df[1], color='#06b6d4')
#                     plt.xticks(rotation='vertical')
#                     st.pyplot(fig)
#                 else:
#                     st.info("No common words found.")
#             except Exception:
#                 st.info("Could not fetch common words.")

#         st.markdown("---")

#         # ==================== EMOJI ANALYSIS ====================
#         st.subheader("😀 Emoji Analysis")
#         try:
#             emoji_df = helper.emoji_helper(selected_user, df)
#             if emoji_df is not None and not emoji_df.empty:
#                 col_e1, col_e2 = st.columns(2)
#                 with col_e1:
#                     st.dataframe(emoji_df, use_container_width=True)
#                 with col_e2:
#                     fig, ax = plt.subplots(figsize=(5, 4))
#                     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", startangle=140)
#                     st.pyplot(fig)
#             else:
#                 st.info("No emojis found in this chat.")
#         except Exception:
#             st.info("Emoji analysis not available for this chat.")
# else:
#     # Landing Page UI when no file is uploaded
#     st.title("👋 Welcome to WhatsApp Chat Analyzer")
#     st.info("👈 Please upload your exported WhatsApp chat text file from the sidebar to begin the analysis.")



import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="WhatsApp Chat Analyzer Pro",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Global Matplotlib Dark Style
plt.style.use('dark_background')

# ==================== ELEGANT DARK MODE CSS ====================
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; font-weight: 600 !important; }
    .metric-card {
        background-color: #1e293b;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        text-align: center;
        border: 1px solid #334155;
    }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    </style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
st.sidebar.title("💬 Chat Analyzer Pro")
st.sidebar.markdown("### Upload WhatsApp Chat")

uploaded_file = st.sidebar.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    with st.spinner("Processing chat data... 🚀"):
        df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Filter Options")
    selected_user = st.sidebar.selectbox("Show analysis with respect to:", user_list)

    # Date Range Filter
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Date Range Filter")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

    df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]

    if st.sidebar.button("🚀 Show Analysis", width='stretch'):
        
        st.title(f"📈 Analytics Dashboard — [{selected_user}]")
        st.markdown(f"<span style='color: #94a3b8;'>**Analysis Period:** {start_date} to {end_date}</span>", unsafe_allow_html=True)
        st.markdown("---")

        df_user = df[df['user'] == selected_user] if selected_user != 'Overall' else df

        # ==================== TOP STATISTICS ====================
        try:
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            st.subheader("📌 Top Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            metrics = [
                ("Total Messages", f"{num_messages:,}", "#38bdf8", col1),
                ("Total Words", f"{words:,}", "#818cf8", col2),
                ("Media Shared", f"{num_media_messages:,}", "#fbbf24", col3),
                ("Links Shared", f"{num_links:,}", "#f472b6", col4)
            ]
            for title, val, color, col in metrics:
                with col:
                    st.markdown(f"""
                        <div class="metric-card">
                            <p style="color: #94a3b8; font-size: 13px; font-weight: 500; margin-bottom: 0; text-transform: uppercase;">{title}</p>
                            <h2 style="color: {color}; margin-top: 8px; font-weight: 700;">{val}</h2>
                        </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading stats: {e}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ==================== SENTIMENT ANALYSIS ====================
        st.subheader("🎭 Chat Sentiment Analysis")
        try:
            non_media_df = df_user[df_user['message'] != '<Media omitted>\n']
            if not non_media_df.empty:
                polarities = non_media_df['message'].apply(lambda msg: TextBlob(str(msg)).sentiment.polarity)
                avg_polarity = polarities.mean()
                mood = "😊 Mostly Positive & Friendly" if avg_polarity > 0.05 else ("😠 Slightly Negative / Critical" if avg_polarity < -0.05 else "😐 Neutral / Informational")
                color = "#34d399" if avg_polarity > 0.05 else ("#f87171" if avg_polarity < -0.05 else "#fbbf24")
                st.markdown(f"**Overall Chat Tone:** <span style='color:{color}; font-size:16px; font-weight:600;'>{mood}</span> (Score: {avg_polarity:.2f})", unsafe_allow_html=True)
        except Exception:
            pass

        st.markdown("---")

        # ==================== TIMELINES ====================
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("📅 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            if timeline is not None and not timeline.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(timeline['time'], timeline['message'], color='#38bdf8', marker='o', linewidth=2)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        with col_t2:
            st.subheader("📈 Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            if daily_timeline is not None and not daily_timeline.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#818cf8', linewidth=1.5)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        st.markdown("---")

        # ==================== HOURLY BREAKDOWN ====================
        st.subheader("⏰ Hourly Activity Breakdown")
        hourly_counts = df_user['hour'].value_counts().sort_index()
        if not hourly_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 3.5))
            ax.bar(hourly_counts.index, hourly_counts.values, color='#38bdf8', alpha=0.85)
            ax.set_xticks(range(24))
            st.pyplot(fig)

        st.markdown("---")

        # ==================== ACTIVITY MAP ====================
        st.subheader("📊 Activity Map")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown("##### Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            if busy_day is not None and not busy_day.empty:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.bar(busy_day.index, busy_day.values, color='#818cf8')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        with col_a2:
            st.markdown("##### Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            if busy_month is not None and not busy_month.empty:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.bar(busy_month.index, busy_month.values, color='#fbbf24')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        st.markdown("---")

        # ==================== HEATMAP ====================
        st.subheader("🔥 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if user_heatmap is not None and not user_heatmap.empty and user_heatmap.size > 0:
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.heatmap(user_heatmap, ax=ax, cmap="mako")
            st.pyplot(fig)

        # ==================== BUSY USERS (GROUP) ====================
        if selected_user == 'Overall':
            st.markdown("---")
            st.subheader("👑 Most Busy Users in Group")
            x, new_df = helper.most_busy_users(df)
            if x is not None and not x.empty:
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    fig, ax = plt.subplots(figsize=(5, 4))
                    ax.bar(x.index, x.values, color='#f472b6')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col_u2:
                    st.dataframe(new_df, width='stretch')

        st.markdown("---")

        # ==================== WORDCLOUD & COMMON WORDS ====================
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.subheader("☁️ Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc is not None:
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.imshow(df_wc)
                ax.axis('off')
                st.pyplot(fig)

        with col_w2:
            st.subheader("🔤 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            if most_common_df is not None and not most_common_df.empty:
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.barh(most_common_df[0], most_common_df[1], color='#38bdf8')
                st.pyplot(fig)

        st.markdown("---")


        # ==================== EMOJI ANALYSIS ====================
        st.subheader("😀 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if emoji_df is not None and not emoji_df.empty:
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.dataframe(emoji_df, width='stretch')
            with col_e2:
                fig, ax = plt.subplots(figsize=(5, 4))
                # Updated to use column names 'Emoji' and 'Count' instead of 0 and 1
                ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f%%", startangle=140, textprops={'color':'#e2e8f0'}, colors=sns.color_palette("mako"))
                st.pyplot(fig)
        else:
            st.info("No emojis found in this chat.")

    
        # ==================== DOWNLOAD ====================
        st.markdown("---")
        st.subheader("📥 Download Cleaned Data")
        st.download_button(
            label="📥 Download Filtered Chat Data as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='whatsapp_filtered_analysis.csv',
            mime='text/csv',
            width='stretch'
        )

else:
    st.title("👋 Welcome to WhatsApp Chat Analyzer Pro")
    st.info("👈 Please upload your exported WhatsApp chat text file from the sidebar to start analyzing.")