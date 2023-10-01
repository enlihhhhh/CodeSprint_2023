import streamlit as st
import hashlib
from PIL import Image
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

df_traffic_control = pd.read_csv('df_traffic_control.csv')
mockup_dataset = pd.read_csv('mockup_dataset.csv')

# Chart 1: Histogram of Time Spent by Vessels
    st.write("## Chart 1: Histogram of Time Spent by Vessels")
    a = st.slider('Select the bin value', 1, 30)
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


    # Example 1: Interactive Line Chart
    st.write("## Example 1: Interactive Line Chart")
    a = st.slider('Select a value for "a"', 1, 10)
    x = np.linspace(-10, 10, 100)
    y = a * x + 5
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_title(f"Line: y = {a}x + 5")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    st.pyplot(fig1)
    plt.close(fig1)

    # Example 2: Interactive Scatter Plot
    st.write("## Example 2: Interactive Scatter Plot")
    marker_type = st.selectbox('Select marker type', ('circle', 'square', 'triangle'))
    marker_dict = {'circle': 'o', 'square': 's', 'triangle': '^'}
    x = np.random.randn(50)
    y = x * 3 + np.random.randn(50)
    fig2, ax2 = plt.subplots()
    ax2.scatter(x, y, marker=marker_dict[marker_type])
    ax2.set_title(f"Scatter Plot with {marker_type} markers")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    st.pyplot(fig2)
    plt.close(fig2)

    # Example 3: Interactive Heatmap
    st.write("## Example 3: Interactive Heatmap")
    colormap = st.selectbox('Select a colormap', ('coolwarm', 'viridis', 'magma'))
    fig3, ax3 = plt.subplots()
    sns.heatmap(np.random.randn(10, 10), cmap=colormap, ax=ax3)
    ax3.set_title("Interactive Heatmap")
    st.pyplot(fig3)
    plt.close(fig3)