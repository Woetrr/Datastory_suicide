import streamlit as st
import pandas as pd
import plotly.express as px
import json


# Page configuration
st.set_page_config(page_title="Suicides in the World", layout="wide", initial_sidebar_state="expanded")

#------------------------------------------------------------------------------------------------------------------

#style of the page:
# Apply the font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
body {
    font-family: 'Montserrat', Roboto;
}
</style>
""", unsafe_allow_html=True)
#------------------------------------------------------------------------------------------------------------------
#sidebar creatian
# Sidebar filters
st.sidebar.image("Pictures/Portret.jpg")

# Add a text block with a background
st.sidebar.markdown(
    """
    <div style="
        background-color: #cfd1d1; 
        padding: 15px; 
        border-radius: 10px;
        text-align: center;">
        <h3 style="color: #333;">About Me</h3>
        <p style="color: #555;">I'm Wouter Nobel, an student electrical engineering following the minor Big data & Design.</p>
        <p style="color: #555;">🔗 <a href='https://www.linkedin.com/in/wouter-nobel-870499224/' target='_blank'>LinkedIn</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
#------------------------------------------------------------------------------------------------------------------
#world view

# Create three columns: empty, content, empty
col1, col2, col3 = st.columns([1, 3, 1])  # Adjust the middle column width as needed

with col2:  # Everything inside col2 will be centered
    st.image("Pictures/header.png")
    st.markdown("## Suicide worldwide: Unveiling the Impact of Gender, Economy, and Society")
   
    st.write('''Suicide is a major public health concern that affects individuals, families, and entire communities.
             Every year, approximately 726,000 people take their own lives (about one death every 43 seconds), and countless others attempt suicide.
             Each loss is a tragedy with long-lasting emotional, social, and economic consequences for those left behind.
             Suicide is not limited to any one demographic, it occurs across all age groups and regions.
             It even was the third leading cause of death among 15–29-year-olds globally in 2021 (World Health Organization, 2024).
                ''')
                
    #------------------------------------------------------------------------------------------------------------------          
    st.markdown("""___""") # make a stripe to seperate the graphs                
    st.markdown("### 1. Worlwide data over the years")
    st.write('''When looking at the data, one key question arises: Is the situation improving or worsening? 
             The answer, based on the numbers, suicide rates have generally declined over time.
             Comparing the decade from 2006 to 2015 with the previous period (1996-2005), many countries show a notable decrease in suicides.
             This trend is visible across different age groups and both genders, suggesting a broader societal shift 
             rather than a temporary fluctuation. Though there are still some countries that show an increase.''')
                
    df = pd.read_csv("Data/Suicide_rates.csv") #load the dataset
    print(df.head(13))
    print(df.dtypes)
    
    #filters
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Place Gender Selector in the first column
    with col1:
        gender_selector = st.radio(
            "Select Sex",
            ("Both", "male", "female")
        )
    
    # Place Measure Selector in the second column
    with col2:
        measure_selector = st.radio(
            "Select Measure",
            ("Suicides per 100k", "Total Suicides")
        )
    
    age_options = ["All"] + df["age"].unique().tolist()
    
    # Age Group Selector 
    age_selector = st.multiselect(
        "Select Age Groups",
        options=age_options,  # Use the unique age groups from the dataset
        default=["All"]    # Default to all age groups selected
    )
    
    
    
    # Year Slider to choose the year
    selected_year_map = st.slider(
        "Select Year for map", 
        min_value=df["year"].min(), 
        max_value=df["year"].max(), 
        value=2000, 
        step=1
    )
    
    # Filter dataset based on the selected year
    filtered_data = df[df["year"] == selected_year_map]
    
    # Filter based on gender selection
    if gender_selector != "Both":
        filtered_data = filtered_data[filtered_data["sex"] == gender_selector]
    
    if "All" in age_selector:
        filtered_data = filtered_data
    else:    
        # Filter based on age group selection
        filtered_data = filtered_data[filtered_data["age"].isin(age_selector)]
    
    # Choose the column to display based on the measure selector
    if measure_selector == "Total Suicides":
        color_column = "suicides_no"
        color_title = "Total Suicides"
        # Aggregate suicides per country
        map_data = filtered_data.groupby("country", as_index=False)["suicides_no"].sum()
    else:
        color_column = "suicides_per_100k"
        color_title = "Suicides per 100k"
        # Aggregate suicides per country
        # Aggregating suicide numbers and population by country
        agg_suic_data = filtered_data.groupby("country", as_index=False)["suicides_no"].sum()
        agg_pop_data = filtered_data.groupby("country", as_index=False)["population"].sum()
    
        # Merging the aggregated data on country
        map_data = pd.merge(agg_suic_data, agg_pop_data, on="country")
    
        # Calculating the suicides per 100,000 people
        map_data["suicides_per_100k"] = (map_data["suicides_no"] / map_data["population"]) * 100000
        
    # Checkbox to show raw data
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.dataframe(filtered_data)
    
    
    
    # Create Choropleth Map
    fig = px.choropleth(
        map_data,
        locations="country",  # Country names
        locationmode="country names",  # Matches country names
        color=color_column,  # Use the selected measure for color intensity
        hover_name="country",  # Display country name on hover
        color_continuous_scale="Portland",  # Adjust color scale
        title=f"{color_title} in {selected_year_map}, (WHO, 2016)"  # Title reflecting the selected year and measure
    )
    
    # Customize the layout
    fig.update_layout(
    template='simple_white',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=0, r=0, t=50, b=0),
    height=400,
    geo=dict(
        bgcolor='#D2D2D2'
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text=color_title,
            side="right",
            font=dict(size=14)
            )
        )
    )
    
    # Display map
    st.plotly_chart(fig)
    
    st.markdown("""___""") # make a stripe to seperate the graphs
    
    #------------------------------------------------------------------------------------------------------------------
    #Sex view
    st.markdown("### 2. Difference between sexes")
    
    st.write("""Globally, there are significant disparities in suicide rates between men and women.
             While females are more likely to experience suicidal thoughts and attempt suicide, 
             males are more likely to die by suicide a phenomenon often referred to as the "gender paradox" in suicidal behavior. 
             This discrepancy is attributed to several factors, including the tendency of males to choose more lethal means
             and societal norms that discourage men from seeking help for mental health issues (Schrijvers et al., 2011).""")
    
     # Year Slider to choose the year
    selected_year_box = st.slider(
        "Select Year for box plot", 
        min_value=df["year"].min(), 
        max_value=df["year"].max(), 
        value=2000, 
        step=1
    )
    # Filter dataset based on the selected year
    filtered_data_box = df[df["year"] == selected_year_box]
    
    age_options = ["All"] + df["age"].unique().tolist()
    # Age Group Selector 
    age_selector_box = st.multiselect(
        "Select Age Groups for box plot",
        options=age_options,  # Use the unique age groups from the dataset
        default=["All"]    # Default to all age groups selected
    )
    
    if "All" in age_selector_box:
        filtered_data_box = filtered_data_box
    else:    
        # Filter based on age group selection
        filtered_data_box = filtered_data_box[filtered_data_box["age"].isin(age_selector_box)]
    
    
    # Aggregate suicides per country and sex
    agg_suic_data_box = filtered_data_box.groupby(["country", "sex","gdp_per_capita ($)"], as_index=False)["suicides_no"].sum()
    agg_pop_data_box = filtered_data_box.groupby(["country", "sex","gdp_per_capita ($)"], as_index=False)["population"].sum()
    
    # Merging the aggregated data on country and sex
    box_data = pd.merge(agg_suic_data_box, agg_pop_data_box, on=["country", "sex","gdp_per_capita ($)"])
    
    # Calculating the suicides per 100,000 people
    box_data["suicides_per_100k"] = (box_data["suicides_no"] / box_data["population"]) * 100000
    
    # Create Box Plot
    fig_box = px.box(
        box_data,
        x="sex",
        y="suicides_per_100k",
        color="sex",
        category_orders={"sex": ["female", "male"]},  # Ensure order remains consistent
        color_discrete_map={
            "male": "rgb(0,150,255)",   # Male = Blue
            "female": "rgb(255,16,240)" # Female = Pink
        },
        points="all",  # Show all individual points
        title=f"Sum worldwide {color_title} in {selected_year_box} comparing sex, (WHO, 2016)",
        labels={color_column: color_title, "sex": "Sex"},
        hover_data=["country"]  # Show country on hover
    )
    
    
    # Customize Layout
    fig_box.update_layout(
        template='simple_white',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=50, b=0),  # margins so title shows
        height=400
    )
    
    # Show Box Plot
    st.plotly_chart(fig_box)
    
    st.markdown("""___""") # make a stripe to seperate the graphs
    #------------------------------------------------------------------------------------------------------------------
    #comparing the GDP
    
    st.image("Pictures/geldzorgen.png") # picture about money isues
    
    st.markdown("### 3. Can Economic Growth Help Prevent Suicides?")
    
    st.write("""Suicide is a complex issue influenced by various social, psychological, and economic factors. 
             While wealthier nations generally have lower suicide rates, research suggests that economic growth alone does not guarantee protection
             against suicide. However, a global analysis found that for every 1,000 dollar increase in GDP per capita, 
             suicide rates decrease by 2%. This effect is particularly strong in low-income countries, where a small 
             economic boost can lead to a nearly 29% reduction in suicide rates.
             Interestingly, investing in suicide prevention 
             could be cost-effective. The study estimates that providing 1,000 dollar to 500 high-risk individuals could save at least one life,
             which is far less expensive than the estimated economic cost of a single suicide over 500,000 dollar. This suggests that governments 
             should not only focus on economic growth but also on direct social support to those most vulnerable during financial hardship (Meda et al., 2021). """)
             
    # Year Slider to choose the year for the scatter plot
    selected_year_scatter = st.slider(
        "Select Year for scatter plot", 
        min_value=df["year"].min(), 
        max_value=df["year"].max(), 
        value=2000, 
        step=1
    )
    
    # Filter dataset based on the selected year for the scatter plot
    filtered_data_scatter = df[df["year"] == selected_year_scatter]
    
    # Aggregate suicides per country and sex for the scatter plot
    agg_suic_data_scatter = filtered_data_scatter.groupby(["country", "sex", "gdp_per_capita ($)"], as_index=False)["suicides_no"].sum()
    agg_pop_data_scatter = filtered_data_scatter.groupby(["country", "sex", "gdp_per_capita ($)"], as_index=False)["population"].sum()
    
    # Merging the aggregated data on country, sex, and GDP per capita for the scatter plot
    scatter_data = pd.merge(agg_suic_data_scatter, agg_pop_data_scatter, on=["country", "sex", "gdp_per_capita ($)"])
    
    # Calculating the suicides per 100,000 people for the scatter plot
    scatter_data["suicides_per_100k"] = (scatter_data["suicides_no"] / scatter_data["population"]) * 100000
    
    # Create Scatter Plot
    fig_scatter = px.scatter(
        scatter_data,
        x="gdp_per_capita ($)",
        y="suicides_per_100k",
        color="sex",
        category_orders={"Sex": ["female", "male"]},  # Ensure order remains consistent
        
        color_discrete_map={
            "male": "rgb(0,150,255)",   # Male = Blue
            "female": "rgb(255,16,240)" # Female = Pink
        },
        title="Suicides per 100,000 People vs GDP per Capita, (World Bank, 2018),(WHO, 2016)",
        labels={"gdp_per_capita ($)": "GDP per Capita", "suicides_per_100k": "Suicides per 100,000 People"},
        hover_data=["country", "sex"]
    )
    
    # Show Scatter Plot
    st.plotly_chart(fig_scatter)
    
    st.markdown("""___""") # make a stripe to seperate the graphs
    #------------------------------------------------------------------------------------------------------------------
    
    df_1 = pd.read_excel("Data/Zelfdodingen_1970-2023_NL.xlsx",sheet_name= "Tabel 1", skiprows=4,skipfooter=3)

    # Rename columns 
    df_1.columns = ["Year", 
              "Men_Absolute", "Women_Absolute", "Total_Absolute","",
              "Men_Per100k", "Women_Per100k", "Total_Per100k","",
              "Men_Standardized", "Women_Standardized", "Total_Standardized"]
    print(df_1.dtypes)
    
    # Drop unnamed or empty columns
    df_1 = df_1.loc[:, df_1.columns != ""]

    # Now, convert the 'year' column to numeric (integer) values
    df_1['Year'] = pd.to_numeric(df_1['Year'], errors='coerce')
    print(df_1.head(8))
    print(df_1.dtypes)
    
    st.markdown("### 4. Lets zoom in: data in the Netherlands")
    
    st.write("""Suicide rates in the Netherlands follow a similar pattern to global trends, 
             with men consistently having higher suicide rates than women. This is largely due to the fact that men often choose more lethal
             methods, such as hanging. Additionally, suicide is a leading cause of death among young adults, with 3 out of 10 deaths
             in the 20-30 age group being attributed to suicide closely mirroring worldwide statistics. 
             While the overall suicide rate in the Netherlands has remained relatively stable since 2019,
             these figures highlight the ongoing need for mental health awareness and intervention efforts (CBS, 2024).
             """)
    #line charts is used to plot some variable:
    fig_line_NL = px.line(data_frame=df_1,
             x="Year",
             y=["Men_Standardized","Women_Standardized", "Total_Standardized"],
             title="""Suicide per 100K people in the Netherlands<br><sup>
             standardized by age from 2023</sup>""",
             labels={"value": "Suicides per 100K", "variable": "Sex"},
             color_discrete_map={
                 "Men_Standardized": "rgb(0,150,255)",   # Male = Blue
                 "Women_Standardized": "rgb(255,16,240)", # Female = Pink
                 "Total_Standardized": "rgb(17,217,87)"
             })
    
    # Rename legend labels
    fig_line_NL.for_each_trace(lambda t: t.update(name={
    "Men_Standardized": "Men",
    "Women_Standardized": "Women",
    "Total_Standardized": "Total"
    }.get(t.name, t.name)))
    
    # Show Scatter Plot
    st.plotly_chart(fig_line_NL)
    
    st.markdown("""___""") # make a stripe to seperate the graphs
    #------------------------------------------------------------------------------------------------------------------
    df_2 = pd.read_excel("Data/Zelfdodingen_1970-2023_NL.xlsx",sheet_name= "Tabel 3", skiprows=8,skipfooter=7)
    # Rename columns (assuming structure from your example)
    df_2.columns = ["provincie", 
              "2019", "2020","2021", "2022","2023",
               "absoluut-19-23", "p100k-19-23"]
    
    df_2.dropna(inplace=True)
    print(df_2.head(8))
    print(df_2.dtypes)
    
    # Load GeoJSON file
    with open("Data/provinces_nederland.geojson", "r", encoding="utf-8") as f:
        provincies = json.load(f)
    
    st.markdown("### 5. Regional Suicide Trends in the Netherlands")
    
    st.write("""The map provides an overview of suicide rates per province in the Netherlands, Regional differences have remained relatively stable over time, 
             though some provinces show exceptions. Utrecht, South Holland, and Flevoland have consistently lower suicide rates, 
             while Groningen and Drenthe have had high rates since the late 1990s. This trend continued into 2023.
             Urbanization also plays a key role in the distribution of suicide rates. In less urbanized areas such as Southwest
             Drenthe and Zeeuws-Vlaanderen, suicide rates are significantly higher than the national average, 
             whereas in highly urbanized regions like Greater Amsterdam and The Hague metropolitan area, 
             the numbers align more closely with the national average. Research suggests that rural areas face stronger 
             risk factors, including higher unemployment, social isolation, and substance abuse. Additionally, a greater stigma 
             surrounding mental health issues often makes it harder to seek help, limiting access to mental health services and 
             suicide prevention resources (CBS, 2021).
             """)
    
    # Create Choropleth Map
    map_nl = px.choropleth(
        df_2,
        geojson=provincies,
        locations="provincie",  # Column in the dataframe
        featureidkey="properties.name",  # Match with GeoJSON province names
        color="p100k-19-23",  # Change this to visualize another year
        hover_name="provincie",
        color_continuous_scale="Portland",
        title="Suicide Rate Netherlands, 2029-2023, (CBS, 2023)"
    )
    
    # Update layout to adjust the map size
    map_nl.update_geos(
        fitbounds="locations",  # Adjust the map to fit the bounds of the locations
        visible=False
    )
    
    map_nl.update_layout(
    template='simple_white',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=0, r=0, t=50, b=0),
    height=400,
    geo=dict(
        bgcolor='#D2D2D2'
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text=color_title,
            side="right",
            font=dict(size=14)
            )
        )
    )

    st.plotly_chart(map_nl, use_container_width=True)
    st.markdown("""___""") # make a stripe to seperate the graphs
    #------------------------------------------------------------------------------------------------------------------
    st.image("Pictures/psychological-support-concept-girl-feeling-anxiety-loneliness-helping-hand.jpg")
    st.markdown("### Conclusion")
    
    st.write("""Suicide remains a critical global issue, influenced by various factors such as gender, 
             economic conditions, and societal structures. Our data story highlights how men are more likely to die by suicide 
             due to the use of more lethal methods, a trend observed both in the Netherlands and worldwide. Additionally, economic 
             stability plays a crucial role, with lower-income countries experiencing significantly higher suicide rates, emphasizing 
             the need for targeted support systems. \n \n Despite slight variations across regions, the overall patterns remain consistent: suicide is a leading cause of death, 
             particularly among young adults, and addressing it requires a combination of mental health support, economic security, and 
             societal awareness. While suicide rates in some regions, such as the Netherlands, have remained stable in recent years, this
             should not lead to complacency. Understanding these patterns is essential for developing more effective prevention strategies 
             and ensuring that those at risk receive the help they need.
             """)
