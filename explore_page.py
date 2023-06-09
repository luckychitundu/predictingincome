import streamlit as st 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def shorten(categories,threshold):
    new_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= threshold:
            new_map[categories.index[i]] = categories.index[i]
        else:
            new_map[categories.index[i]] = "Other"           
    return new_map  

def clean_experience(x):
    if x == "Less than 1 year":
        return 0.5 
    if x == "More than 50 years":
        return 50
    return float(x)

def clean_edlevel(x):
    if "Bachelor’s degree" in x:
        return "Bachelors degree"
    if "Master’s degree" in x:
        return "Masters degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    keepColumns = ["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]
    df = df[keepColumns]
    df = df.rename({"ConvertedComp":"Salary"},axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment",axis=1)
    catMap = shorten(df.Country.value_counts(),400)
    df["Country"] = df["Country"].map(catMap)
    df = df[df["Salary"] >= 10000]
    df = df[df["Salary"] <= 250000]
    df = df[df["Country"] != "Other"]
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_edlevel)
    return df 

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer Salaries")
    st.write("""### Stack Overflow Developer Survey 2020""")


    data = df["Country"].value_counts()
    fig1,ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal")
    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)


    st.write("""#### Mean Salary Based On Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary Based On Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)













