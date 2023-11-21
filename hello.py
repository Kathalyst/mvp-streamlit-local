import streamlit
import github_process
import pandas as pd

streamlit.header("Kathalyst - Automated Software Documentation")

github_link = streamlit.sidebar.text_input("Github Link")
if streamlit.sidebar.button("Submit"):
    #process if submit button is pressed
    print(f'Processing {github_link}')
    file_contents,file_names = github_process.control(github_link)

    doc,vdd = streamlit.tabs(["Documentation","Visual Dependency Diagram"])
    
    with doc:
        # print("\n\nInside Documentation Tab")
        streamlit.write(file_names)
    with vdd:
        # print("\n\nInside VDD Tab")
        streamlit.write(file_contents)
    
    pass

example_links = ["https://github.com/anushkasingh98/personal-portfolio"]
df = pd.DataFrame(example_links,columns=["Example Github Links"])

streamlit.sidebar.table(df)