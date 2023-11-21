import streamlit as st
import github_process
import gpt4_process
import pandas as pd

st.set_page_config(
    page_title="Kathalyst Web App",
    page_icon="images/codeAID_green.png",
)

st.header("Kathalyst - Automated Software Documentation")

github_link = st.sidebar.text_input("Github Link")
if st.sidebar.button("Submit"):
    #process if submit button is pressed
    print(f'Processing {github_link}')
    file_contents,file_names,dir = github_process.control(github_link)

    doc,vdd = st.tabs(["Documentation","Visual Dependency Diagram"])
    
    with doc:
        # print("\n\nInside Documentation Tab")
        output = gpt4_process.control(file_contents,file_names,dir)
        st.markdown(output)
    with vdd:
        # print("\n\nInside VDD Tab")
        st.write("Visual Dependency Diagram coming soon ...")
    
    pass

example_links = ["https://github.com/anushkasingh98/personal-portfolio"]
df = pd.DataFrame(example_links,columns=["Example Github Links"])

st.sidebar.table(df)