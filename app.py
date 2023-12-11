import streamlit as st
import github_process
import gpt4_process
import llama2_process
import pandas as pd
import vdd_diagram
from st_pages import Page, show_pages, hide_pages
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Kathalyst Web App",
    page_icon="images/codeAID_green.png",
)

show_pages([
        Page("home.py","Home"),
        Page("app.py","App")
    ])

hide_pages(['Home'])

# placeholder = st.empty()

st.header("Kathalyst - Automated Software Documentation")

st.markdown(
            (
                '<hr style="background-color: #71eea8; margin-top: 0;'
                ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">'
            ),
            unsafe_allow_html=True,
        )

git,feedback = st.columns([3, 1])

github_link = st.sidebar.text_input("Github Link")

model = st.sidebar.radio("Which LLM Model would you like to use?",["GPT-4","Llama 2 70b"],index=0)

if st.sidebar.button("Submit"):
    #process if submit button is pressed
    print(f'Processing {github_link}')
    
    file_contents,file_names,dir = github_process.control(github_link)

    git.write("Processing Github Repo: "+str(github_link))

    doc,vdd = st.tabs(["Documentation","Visual Dependency Diagram"])

    with doc:
        # print("\n\nInside Documentation Tab")
        with st.spinner(text="In progress..."):
            if model == "GPT-4":
                output = gpt4_process.control(file_contents,file_names,dir)
            elif model == "Llama 2 70b":
                output = llama2_process.control(file_contents,file_names)
        st.markdown(output)
        st.download_button('Download Text File', output)
    
    with vdd:
        print("\n\nInside VDD Tab")
        with st.spinner(text="In progress..."):
            # fil_name = vdd.control(file_contents,file_names,"diagram")
            fil_name = vdd_diagram.process_control(file_contents,file_names,"diagram")
        st.image(fil_name)
        with open(fil_name, "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name=fil_name,
                mime="image/png"
            )
    feedback.link_button("Give Us Feedback","https://forms.office.com/r/DmyrfUnxGt")

example_links = ["https://github.com/anushkasingh98/personal-portfolio","https://github.com/anushkasingh98/demo-repo",
                 "https://github.com/anushkasingh98/CapitalisationProject"]
df = pd.DataFrame(example_links,columns=["Example Github Links"])

st.sidebar.table(df)

st.sidebar.markdown("Made with ❤️ by Kathalyst")

if st.sidebar.button("Log Out"):
    hide_pages(['App'])
    switch_page("Home")

# clear = st.sidebar.radio("Clear page?",["Yes","No"],index=1)
# if clear == "Yes":
#     placeholder.empty()
# elif clear == "No":
#     pass