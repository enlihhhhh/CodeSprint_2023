import streamlit as st
import hashlib
from PIL import Image
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# Setting Random Seed
random.seed(47)

# Function to hash passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
# Function to verify hashed password
def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# Initialize a dictionary to serve as a simple database
db = {"PSA": make_hashes("Admin")}

#Datasets
df_traffic_control = pd.read_csv('df_traffic_control.csv')
mockup_dataset = pd.read_csv('mockup_dataset.csv')

# Initialize session state
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                        """
# Function to display login page
def display_login():
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: Black;'>Login Page </h2>", unsafe_allow_html=True)
    # st.title("Login Page")
    st.image("logo.png", use_column_width='auto')
    st.empty()
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
     # New code: Submit button for the form
        submit_button = st.form_submit_button("Login")

    if username == "PSA" and password == "Admin":
            st.session_state['is_logged_in'] = True
            st.success("Logged in successfully")
    elif submit_button:  # New code: Check if the form was submitted
        st.warning("Invalid username or password")

# Function to display home page
def display_home():
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.markdown("""
                <h1 style='text-align: center; color: Black;'>Home Page </h2>
                """, unsafe_allow_html=True)
    st.markdown("""
                <div style='text-align: center; color: Black;'>
                Welcome to the PSA Visualisations Portal
                 </div>
                """, unsafe_allow_html=True)
    page_bg_img = """
    <style> 
    .stApp{
    background-image: url(https://wpassets.porttechnology.org/wp-content/uploads/2022/10/04095640/PSA-Singapore-Achieves-Record-Breaking-Moves-in-a-Single-Call-scaled-1.jpg);
    background-size: cover;
    opacity:0.9;
    }
    </style>
    """
    #st.markdown(page_bg_img, unsafe_allow_html=True)
    st.text(" ")
    # Styling the buttons using columns and markdown
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
     pass
    with col2:
        # Button to redirect to code for Example 1 and Example 2
        if st.button('PSA Public Websites'):
            # Open interface-1.py in a new terminal
            st.markdown("[PSA Singapore](https://www.singaporepsa.com/)")
            st.markdown("[PSA International](https://www.globalpsa.com/)")
            st.markdown("[PSA Marine](https://www.psamarine.com/)")
        with col3:
           pass
        with col4:
            # Button to redirect to code for Example 3
            if st.button('PSA Staff Website'):
                # Open interface-1.py in a new terminal
                st.markdown("[PSA International](https://www.globalpsa.com/)")
        with col5:
            pass

    # Custom HTML/CSS to make buttons visually appealing
    st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background-color: #004C99;
        border: true;
        padding: 14px 24px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
    }
    .stButton>button:hover {
        background-color: #00356B; 
    }
    """, unsafe_allow_html=True)


# Function to display visualizations
def display_visualizations():
    st.sidebar.title("Overview")

    # Chart 1: Histogram of Time Spent by Vessels
    st.write("## Chart 1: Histogram of Time Spent by Vessels")
    a = st.slider('Select the bin value', 1, 30, 15)
    if 'Time_in_Hours' in df_traffic_control.columns:
        fig, ax = plt.subplots()
        sns.histplot(df_traffic_control['Time_in_Hours'], bins=a, ax=ax)
        ax.set_title('Histogram of Time Spent by Vessels')
        ax.set_xlabel('Time in Hours')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.write("The column 'Time_in_Hours' does not exist in df_traffic_control.")


    # Chart 2: Containers Unloaded and Loaded
    st.write("## Chart 2: Containers Unloaded and Loaded")
    num_records = st.slider('Select the number of records', 10, 100, 50)
    df_sorted = df_traffic_control.sort_values('Timestamp_Entry').head(num_records)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df_sorted['Timestamp_Entry'], df_sorted['Containers_Unloaded (TEUs)'], label='Containers Unloaded', color='tab:blue')
    ax.plot(df_sorted['Timestamp_Entry'], df_sorted['Containers_Loaded (TEUs)'], label='Containers Loaded', color='tab:orange')
    ax.set_title('Time Series Plot of Containers Unloaded and Loaded')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Containers (TEUs)')
    ax.legend()
    # Display the plot in Streamlit
    st.pyplot(fig)
    # Close the plot to free up resources
    plt.close(fig)


    # Chart 3: Container Demand
    st.write("## Chart 3: Container Demand")
    # Plot type selection in main content
    plot_type = st.selectbox("Select Plot Type", ["Line Plot", "Box Plot", "Scatter Plot"])

    # Feature selection in main content
    feature = st.selectbox("Select Feature", ["Seasonality", "MarketTrends", "Temperature", "CompetitorPrices", "Demand"])

    # Create the plot based on user input
    fig, ax = plt.subplots()

    if plot_type == "Line Plot":
        sns.lineplot(x='Month', y=feature, data=mockup_dataset, ax=ax)
    elif plot_type == "Box Plot":
        sns.boxplot(x='Month', y=feature, data=mockup_dataset, ax=ax)
    elif plot_type == "Scatter Plot":
        sns.scatterplot(x='Month', y=feature, data=mockup_dataset, ax=ax)

    plt.title(f"{plot_type} of {feature} Over Months")
    plt.xlabel('Month')
    plt.ylabel(feature)
    st.pyplot(fig)


# Function to display Example 1 code
def display_example1():
    # Sidebar for user input
    st.title("Visualization Options")
    
    # User input for Entry and Exit Days
    entry_day_min = st.sidebar.slider("Min Entry Day", min_value=1, max_value=50, value=1)
    entry_day_max = st.sidebar.slider("Max Entry Day", min_value=1, max_value=50, value=50)
    exit_day_min = st.sidebar.slider("Min Exit Day", min_value=1, max_value=50, value=1)
    exit_day_max = st.sidebar.slider("Max Exit Day", min_value=1, max_value=50, value=50)
    
    # Filter data based on user input
    filtered_df = df_traffic_control[(df_traffic_control['Entry_Day'] >= entry_day_min) & (df_traffic_control['Entry_Day'] <= entry_day_max) & (df_traffic_control['Exit_Day'] >= exit_day_min) & (df_traffic_control['Exit_Day'] <= exit_day_max)]
    
    # Count the frequency of ships for each day
    entry_day_count = filtered_df['Entry_Day'].value_counts().sort_index()
    exit_day_count = filtered_df['Exit_Day'].value_counts().sort_index()
    
    # Create DataFrames for the plots
    df_heatmap_days = pd.DataFrame({
        'Entry': entry_day_count,
        'Exit': exit_day_count
    }).fillna(0)
    
    container_day_sum = filtered_df.groupby('Entry_Day')[['Containers_Loaded (TEUs)', 'Containers_Unloaded (TEUs)']].sum().sort_index()
    df_heatmap_containers = pd.DataFrame(container_day_sum).fillna(0)

    # Dropdown for selecting the type of plot
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Heatmap", "Bar Plot", "Line Plot"])

    # Main content
    st.title("Vessel and Cargo Movement Overview")

    if plot_type == "Heatmap":
        st.subheader("Heatmap of Vessel Movement Across Days")
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        sns.heatmap(df_heatmap_days, annot=True, cmap='coolwarm', fmt='g', ax=ax1)
        plt.title('Vessel Movement Across Days')
        plt.xlabel('Activity')
        plt.ylabel('Day of the Month')
        st.pyplot(fig1)

        st.subheader("Heatmap of Cargo Movement Across Days")
        fig2, ax2 = plt.subplots(figsize=(10, 10))
        sns.heatmap(df_heatmap_containers, annot=True, cmap='coolwarm', fmt='g', ax=ax2)
        plt.title('Cargo Movement Across Days')
        plt.xlabel('Activity')
        plt.ylabel('Day of the Month')
        st.pyplot(fig2)
        
    elif plot_type == "Bar Plot":
        st.subheader("Bar Plot of Vessel Movement Across Days")
        fig, ax = plt.subplots()
        df_heatmap_days.plot(kind='bar', ax=ax)
        plt.title('Vessel Movement Across Days')
        plt.xlabel('Day of the Month')
        plt.ylabel('Count')
        st.pyplot(fig)
        
    elif plot_type == "Line Plot":
        st.subheader("Line Plot of Vessel Movement Across Days")
        fig, ax = plt.subplots()
        df_heatmap_days.plot(kind='line', marker='o', ax=ax)
        plt.title('Vessel Movement Across Days')
        plt.xlabel('Day of the Month')
        plt.ylabel('Count')
        st.pyplot(fig)


# Function to display Example 2 code
def display_example2():
    st.title("3D plot of Demand Factors")
    # Sidebar for user input
    st.sidebar.title("Visualization Options")

    # User input for axis limits in sidebar
    temp_min = st.sidebar.slider("Min Temperature", min_value=0, max_value=40, value=0)
    temp_max = st.sidebar.slider("Max Temperature", min_value=0, max_value=40, value=40)
    price_min = st.sidebar.slider("Min Competitor Prices", min_value=10, max_value=200, value=10)
    price_max = st.sidebar.slider("Max Competitor Prices", min_value=10, max_value=200, value=200)
    demand_min = st.sidebar.slider("Min Demand", min_value=0, max_value=800, value=0)
    demand_max = st.sidebar.slider("Max Demand", min_value=0, max_value=800, value=800)

    # Color map selection in sidebar
    color_map = st.sidebar.selectbox("Select Color Map", ["viridis", "plasma", "inferno", "magma", "cividis"])

    # Filter data based on user input
    filtered_df = mockup_dataset[
        (mockup_dataset['Temperature'] >= temp_min) & (mockup_dataset['Temperature'] <= temp_max) &
        (mockup_dataset['CompetitorPrices'] >= price_min) & (mockup_dataset['CompetitorPrices'] <= price_max) &
        (mockup_dataset['Demand'] >= demand_min) & (mockup_dataset['Demand'] <= demand_max)
    ]

    # Create the 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    sc = ax.scatter(filtered_df['Temperature'], filtered_df['CompetitorPrices'], filtered_df['Demand'], c=filtered_df['Month'], cmap=color_map)

    # Set labels and title
    ax.set_xlabel('Temperature', labelpad=14)
    ax.set_ylabel('Competitor Prices', labelpad=14)
    ax.set_zlabel('Demand', labelpad=16)
    plt.title('3D Plot of Temperature, Competitor Prices, and Demand')

    # Add colorbar as legend
    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.1)
    cbar.set_label('Month', labelpad=14)

    st.pyplot(fig)
    

# Function to display Example 3 code
def display_example3():
    st.sidebar.title("Visualization Options")

    # Multi-select for choosing variables for the pair plot
    selected_vars = st.sidebar.multiselect("Select Variables for Pair Plot", list(mockup_dataset.columns), default=[])

    # Main content
    st.title("Pairplot Visualization Dashboard")

    # Create the pair plot based on user selection
    if len(selected_vars) >= 2:
        fig = sns.pairplot(mockup_dataset[selected_vars], hue='Month', diag_kind='kde', kind='scatter')
        plt.suptitle('Pair Plot of Multiple Dimensions', y=1.02)
        st.pyplot(fig)
    else:
        st.warning("Please select at least two variables for the pair plot.")

# Function to display Example 4 code
def display_example4():
    st.sidebar.title("Visualization Options")

    st.title("Projected Demand of Containers (After using Deep Learning Model)")
    demand_df = pd.read_csv("demand_data.csv")

    st.dataframe(demand_df)
    st.write("Optimal number of containers to unload (TEUs) per month : 4578.0")
    st.write("Optimal number of containers to load (TEUs) per month: 4543.0")
    st.title("Container Allocation Optimiser")

    input = st.text_input("Enter 0 for Day and 1 for Month:")
    if (input =="0"):
        season = st.text_input("Enter the seasonality factor :")
        market = st.text_input("Enter the market trends factor:")
        temperature = st.text_input("Enter the temperature:")
        price = st.text_input("Enter the competitor prices:")
        month_1 = st.text_input("Enter the Month(e.g., 1-12):")
        day = st.text_input("Enter the Day (e.g., 1-31):")
        if (day == "1"):
            allocated_df = pd.read_csv("1aug_allocated_containers.csv")
            st.dataframe(allocated_df)
            st.write("This is the result for the 1st of August")
        elif (day == "10"):
            allocated_df = pd.read_csv("10aug_allocated_containers.csv")
            st.dataframe(allocated_df)
            st.write("This is the result for the 10th of August")
        
    if (input == "1"):
        season = st.text_input("Enter the seasonality factor :")
        market = st.text_input("Enter the market trends factor:")
        temperature = st.text_input("Enter the temperature:")
        price = st.text_input("Enter the competitor prices:")
        month_2 = st.text_input("Enter the month (e.g., 1-12): ")
        if (month_2 == "8"):
            allocated_df = pd.read_csv("aug_allocated_containers.csv")
            st.dataframe(allocated_df)
            st.write("This is the result for the whole month of August")
  
    
        

    
# Function to display Example 5 code
def display_example5():
    st.sidebar.title("DataFrame Viewer")

    # Sidebar for user input
    st.sidebar.title("Options")

    # Select which DataFrame to display
    df_name = st.sidebar.selectbox("Select DataFrame", ["df_traffic_control", "mockup_dataset"])

    # Select number of rows to display
    rows = st.sidebar.slider("Number of Rows to Display", min_value=1, max_value=len(df_traffic_control), value=5)

    # Show the DataFrame
    if df_name == "df_traffic_control":
        st.dataframe(df_traffic_control.head(rows))
    else:
        st.dataframe(mockup_dataset.head(rows))

    # Allow user to expand or contract table
    expand = st.sidebar.checkbox("Expand Table", value=False)
    if expand:
        if df_name == "df_traffic_control":
            st.table(df_traffic_control.head(rows))
        else:
            st.table(mockup_dataset.head(rows))
    
    # Allow user to filter DataFrame based on columns
    if df_name == "df_traffic_control":
        filter_column = st.sidebar.selectbox("Filter Column", df_traffic_control.columns)
    else:
        filter_column = st.sidebar.selectbox("Filter Column", mockup_dataset.columns)

    filter_value = st.sidebar.text_input(f"Filter by {filter_column}")

    if filter_value:
        if df_name == "df_traffic_control":
            st.dataframe(df_traffic_control[df_traffic_control[filter_column] == filter_value])
        else:
            st.dataframe(mockup_dataset[mockup_dataset[filter_column] == filter_value])


# Main function for navigation
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Visualizations", "Vessel and Cargo Movement Overview", "3D plot of Demand Factors", "Pairplot Visualization Dashboard", "Allocation Optimization", "DataFrame Viewer"])

    if selection == "Home":
        display_home()
        
        # Information Popup
        st.write("### Latest News from PSA Singapore")
        # First News Snippet
        with st.expander("PSA Innovates with OptETruck, a Digital Solution for Singapore’s Haulier Sector to Achieve Fleet Optimisation and a Greener Footprint - July 26, 2023"):
            st.image("news1.jpeg", use_column_width=True)
            st.write("""
            As part of efforts to further digitalise and decarbonise the container trucking industry, PSA Singapore (PSA), with the support of Enterprise Singapore, has developed OptETruck, a proprietary cloud-based transport management solution which uses artificial intelligence (AI) to facilitate smarter trip planning and eliminate operational inefficiencies for the haulier community in Singapore. It will help hauliers improve asset utilisation, reduce carbon emissions, as well as optimise operating costs.

            One key feature of OptETruck is automated scheduling, which is enabled by a real-time resource-matching algorithm and predictive modelling to maximise resource utilisation. With this, OptETruck can match and recommend jobs so that hauliers are able to reduce the number of empty trips1 made across various supply chain nodes. Another important feature of OptETruck is asset pooling. This feature enables hauliers and their partners to share resources, allowing them to optimise their fleet and trips.

            Multiple haulier companies have already onboarded OptETruck and with the two key features, they have been able to reduce empty truck trips by over 50%. This translates to an annual reduction of about 10 million kg of CO2 emissions, which is equivalent to 300,000 trees planted in a year. Recently, OptETruck received the Digital Achievers (Team) award at the Tech Leader Awards 2023, a testament to PSA’s commitment in digital transformation to co-create agile, resilient, and sustainable supply chains with our partners and stakeholders.

            OptETruck, together with PSA’s two other digital solutions – *SmartBooking™ and iBOX™ – will be integrated to form an intelligent logistics ecosystem to digitally connect container terminals, depots, hauliers, and logistics facilities in Singapore.

            Ms Seow Hwee, Head of Port+ Business, PSA Southeast Asia, said, “OptETruck and the full suite of digital solutions will strengthen and bring about a smarter and more sustainable supply chain and logistics ecosystem in Singapore. Harnessing the support from our partners and stakeholders, PSA seeks to proliferate these innovative digital capabilities to the small and medium-sized enterprises, which will elevate the competitiveness of the haulage community, drive greater business agility, and aid them to achieve their sustainability targets.”

            Mr Law Chung Ming, Executive Director of Transport and Logistics at Enterprise Singapore, said, “Digitalisation and decarbonisation is key to future-proofing our SMEs in the logistics industry. As such, Enterprise Singapore will continue to support the development of innovative digital solutions such as OptETruck, which can enhance the productivity of SMEs at the industry-level by encouraging job and asset sharing. We hope to see more logistics companies benefit from such solutions that enable them to optimise manpower and resources and enjoy cost savings.”

            Mr Pandian Nachiappan, Managing Director at Paltrans Logistics Pte Ltd, said, “OptETruck seamlessly amalgamates the functionalities of depot booking, Portnet processes and transport management into a unified platform, offering invaluable support to SMEs like Paltrans. Being userfriendly, OptETruck effectively streamlines our operations by alleviating labour-intensive tasks, saving both time and expenses. Its exceptional features like recommendations for the fastest routes, truck pooling and automated scheduling greatly enhanced our efficiency and productivity.”
            """)
        
        # Second News Snippet
        with st.expander("PSA Jurong Island Terminal and JTC Celebrate 130K TEU Record Achievement in Push For a More Sustainable, Efficient and Resilient Supply Chain Ecosystem - March 14, 2023"):
            st.image("news2.jpg", use_column_width=True)
            st.write("""
            PSA Jurong Island Terminal achieved a record-breaking container throughput of more than 130,000 twenty-foot equivalent units (TEUs) in the year ending 31 December 2022. This is its highest volume since the terminal began operations in 2012 and a 30% increase since 2021.

            Transportation of container-on-barge is a greener mode of cargo transportation as compared to trucking. This also represents a reduction of more than 130,000 truck trips between Jurong Island and PSA Terminals on mainland Singapore, and a reduction of up to 37% of carbon emissions for each twenty-foot equivalent unit container, equivalent to savings of 1,950 tCO2e.

            This significant milestone is a result of the collaborative effort between PSA Singapore (PSA) and JTC to create a more sustainable, efficient and resilient supply chain ecosystem for companies on Jurong Island.

            In line with PSA’s goals of decarbonisation across ports and supply chains, electric yard cranes as well as electric-powered quay cranes are deployed at PSA Jurong Island Terminal. Electric or hybrid cranes can achieve at least 50% fuel savings as compared to diesel-powered variants, with the added benefit of reducing nitrogen oxides emissions.

            Ms Seow Hwee, Head of Port+ Business Division, Southeast Asia, PSA International, said, “This record volume is not just another milestone for PSA and JTC, but also establishes a firm foundation for the future of sustainable and efficient supply chains. With the strong support of our partners, customers and stakeholders, PSA continues to push for sustainable barging which will enable the businesses on Jurong Island to streamline their supply chain processes and enhance efficiency and cargo connectivity. Supply chain optimisation drives alignment and focus in achieving our national target to reach net zero emissions by 2050.”

            Ms Cindy Koh, Director of Energy & Chemicals Cluster, JTC, said, “Barging serves as an alternative cargo transportation mode, reducing on-road traffic movement as well as the overall carbon footprint on Jurong Island. This initiative with PSA is part of ongoing efforts by JTC to transform Jurong Island into a sustainable energy and chemicals park in support of the Singapore Green Plan 2030.”

            During the supply chain disruption caused by the pandemic, the barging arrangement provided the Jurong Island manufacturers with an alternative transportation mode for their cargoes, allowing faster response to unexpected disruptions. Today, more than ten companies on Jurong Island, including ExxonMobil, Sumitomo Chemical Asia and The Polyolefin Company, use barging as part of their sustainable supply chain management.
            """)
        
        # Third News Snippet
        with st.expander("PSA container throughput performance for 2022 - January 16, 2023"):
            st.image("news3.jpg", use_column_width=True)
            st.write("""
            PSA International Pte Ltd (PSA) handled container volumes of 90.9 million Twenty-foot Equivalent Units (TEUs) at its port projects around the world for the year ending 31 December 2022. The Group’s volume decreased by 0.7% over 2021, with flagship PSA Singapore contributing 37.0 million TEUs (-0.7%) and PSA terminals outside Singapore handling 53.9 million TEUs (-0.7%).

            Mr Tan Chong Meng, Group CEO of PSA, shared, “The world experienced another challenging year in 2022 and although most countries were emerging from the global pandemic, many continued to suffer from the negative aftershocks which were compounded by the war in Ukraine, higher energy prices, global inflation and supply chain disruptions.

            “Despite the challenges, I was heartened by the ability of our management, staff and unions to adapt and to honour promises to our customers across PSA’s ports, cargo solutions, marine and digital businesses – they showed their grit, resilience and an abiding commitment to excellence. Just as importantly, I am deeply grateful for the continued support of our customers and partners as we worked closely together to keep cargo moving and trade flowing.

            “Going into 2023, the world is experiencing deep transitions towards new realities and while these times of change can be uneasy, PSA stands steady against the headwinds that may come our way as we continue to build on our core business of ports and – coupled with the acquisition of BDP International last year – widen our focus in enabling more agile, resilient and sustainable supply chains. We will partner closely alongside our customers, partners and stakeholders to future-proof our journey ahead, and continue in our mission to be a supply chain orchestrator, realise an Internet of Logistics and bring about more sustainable global trade.”
            """)
        
    elif selection == "Visualizations":
        display_visualizations()
        
        # Progress Bar Example
        with st.spinner("Loading Data..."):
            # Simulate data loading
            st.write("Data loaded successfully!")
        
    elif selection == "Vessel and Cargo Movement Overview":
        display_example1()
        
    elif selection == "3D plot of Demand Factors":
        display_example2()
        
    elif selection == "Pairplot Visualization Dashboard":
        display_example3()
    
    elif selection == "Allocation Optimization":
        display_example4()
    
    elif selection == "DataFrame Viewer":
        display_example5()

    # Display Footer
    st.markdown("---")
    st.markdown("This webpage was made by AuroraAI for PSA")

if __name__ == "__main__":
    if not st.session_state['is_logged_in']:
        display_login()
    else:
        main()