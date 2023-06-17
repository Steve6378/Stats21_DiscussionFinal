import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import time

matplotlib.use("tkagg")

if "disabled" not in st.session_state:
    st.session_state.disabled = False
    
def change_disabled():
    st.session_state.disabled = not (st.session_state.disabled)
    
# Main program here
st.write("Welcome to our EDA application, where we will help you get a quick look on how your dataset looks like!")
st.write("To start everything, let's upload a csv file for your data!")
uploaded_file = st.file_uploader("Choose a csv file", type = "csv")
if uploaded_file != None:
    df = pd.read_csv(uploaded_file)
    st.write("The first ten rows are printed below:")
    st.write(df.head(10))
    st.write("Basic information about the dataset is shown below:")
    st.write("Dimension of dataset:", df.shape)
    st.write("Column names and details:", pd.DataFrame({"name": df.columns, "non-nulls": len(df) - df.isnull().sum().values, "nulls": df.isnull().sum().values, "type": df.dtypes.values}))
    st.write("Now that we have general information about the dataset, please select a column you want to know more information on:")
    desired_col = st.selectbox("List of columns:", ["Choose column:"] + df.columns.tolist(), disabled = st.session_state.disabled, on_change = lambda: change_disabled())
    while st.session_state.disabled == False:
        time.sleep(0.25)
    if desired_col != "Choose column:":
        if df.dtypes[desired_col] == "category":
            st.write("This is a categorical column! Below is a bar plot.")
            counter = Counter(df[desired_col])
            for key in list(counter.keys()):
                counter[key] = [counter[key]]
            count_df = pd.DataFrame.from_dict(counter)
            st.write(count_df)
            fig, ax = plt.subplots()
            sns.barplot(count_df, alpha = 0.4)
            plt.xlabel("Categorical Values")
            plt.ylabel("Frequency")
            plt.title("Bar Plot of Catgorical Variable " + desired_col)
            st.pyplot(fig)           
        elif df[desired_col].dtype.kind in "biufc":
            st.write("This is a numeric column! Below is the five number summary and a KDE plot.")
            st.write((df[desired_col].describe()))
            fig, ax = plt.subplots()
            sns.kdeplot(df, x = desired_col, alpha = 0.4, color = "blue", fill = True)
            plt.xlabel("Values")
            plt.ylabel("Percentage")
            plt.title("Probability Density Function of Numerical Variable " + desired_col)
            st.pyplot(fig)
        else:
            st.write("Unfortunately we're not equipped to provide more information on this column as this column type is currently unsupported.")
        st.snow()
        st.write("This is the end of this relatively short EDA.")
        st.write("If you want to refer to this information later on, feel free to save this page as a PDF.")
        st.write("Thank you for using our service!")
    else:
        st.exception("If you see this the code is not coding right. Please report to me, thanks!")
        