import streamlit as st
import github_process
import gpt4_process
import llama2_process
import pandas as pd
import vdd_diagram
import vdd2
from st_pages import Page, show_pages, hide_pages
from streamlit_extras.switch_page_button import switch_page
from footer import show_footer
import subprocess
import os
import base64
from npm1 import install_npm

# st.set_page_config(
#     page_title="Kathalyst Web App",
#     page_icon="images/codeAID_green.png",
# )

# install_npm()

@st.cache_data
def vdd(file_contents,file_names):
    try:
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
    except Exception as e:
        print(e)
        st.info("We are working hard on our artistic skills to develop the best possible diagram for you. We will get back to you very soon!")

show_pages([
        Page("Hello.py","Home"),
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

st.markdown("""
            <p style="color: #f1f1f1; font-size: 14px; display: inline-block;">Disclaimer: The following documentation has been generated using Large Languages Models and shouldn't be considered sole source of truth. User discretion advised in usage and distribution.</p>
            """,
            unsafe_allow_html=True)

with st.expander("Directions to Use App"):

    st.markdown("""
                    1. Open the Left Side Bar and enter the link to a 'public' Github Repository. You can even pick one of the example Github Repositories we have provided.
                    2. Click Submit.
                    3. Wait for the results to load. This may take a few minutes.
                    4. Once the results are loaded, you can view the documentation and the visual dependency diagram.
                    5. If you scroll down, You can also download the documentation and the visual dependency diagram by clicking the respective Download buttons.
                    6. To give us Feedback, please click the "Give Us Feedback" button that will appear on your screen.
                    
                    We hope you find Kathalyst useful in your endeavors. We would love to hear your feedback!
                """)
    
    # st.markdown("""
    #                 1. Open the Left Side Bar and enter the link to a 'public' Github Repository. You can even pick one of the example Github Repositories we have provided.
    #                 2. Select the LLM Model you would like to use. We recommend using Llama2 for fastest results.
    #                 3. Click Submit.
    #                 4. Wait for the results to load. This may take a few minutes.
    #                 5. Once the results are loaded, you can view the documentation and the visual dependency diagram.
    #                 6. If you scroll down, You can also download the documentation and the visual dependency diagram by clicking the respective Download buttons.
    #                 7. To give us Feedback, please click the "Give Us Feedback" button that will appear on your screen.
                    
    #                 We hope you find Kathalyst useful in your endeavors. We would love to hear your feedback!
    #             """)



print("\n\n")

git,feedback = st.columns([3, 1])

github_link = st.sidebar.text_input("""
Github Link:

(Note: Please make your repository public before using the tool.)
""")

model = st.sidebar.radio("Which LLM Model would you like to use?",["Llama 2 70b"],index=0)
# model = st.sidebar.radio("Which LLM Model would you like to use?",["GPT-4","Llama 2 70b"],index=0)

submit = st.sidebar.button("Submit")

example_links = ["https://github.com/anushkasingh98/testing-repo2","https://github.com/Kathalyst/TaskManager"]
# ["https://github.com/anushkasingh98/personal-portfolio","https://github.com/anushkasingh98/demo-repo","https://github.com/anushkasingh98/CapitalisationProject"]
df = pd.DataFrame(example_links,columns=["Example Github Links"])
df.index = df.index + 1
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

show_footer()

if submit:

    if github_link == "":
        st.warning("Github Link not entered. Please Input a valid link.")
        st.stop()
    #process if submit button is pressed
    print(f'Processing {github_link}')

    if 'github_link' not in st.session_state:
        st.session_state['github_link'] = github_link
    else:
        st.session_state.github_link = github_link

    file_contents,file_names,directory,repo_name = github_process.control(github_link)

    st.session_state.repo_directory = directory
    st.session_state.repo_name = repo_name

    git.write("Processing Github Repo: "+str(github_link))
    feedback.link_button("Give Us Feedback","https://forms.office.com/r/DmyrfUnxGt")

    doc,vdd = st.tabs(["Documentation","Visual Dependency Diagram"])
    print(f"\n\n\nFile Names: {file_names}")

    with doc:
        # st.write("Done :)")
        print("\n\nInside Documentation Tab")
        with st.spinner(text="In progress..."):
            if model == "Llama 2 70b":
                output = llama2_process.control(file_contents,file_names)
            # elif model == "GPT-4":
            #     output = gpt4_process.control(file_contents,file_names,dir)
        st.markdown(output)
        st.download_button('Download Text File', output)
    
    with vdd:
        # run command npm install -g @softwaretechnik/dbml-renderer in python

        print("\n\nInside VDD Tab")
        try:
            print("Trying VDD ...")
            with st.spinner(text="In progress of VDD creation..."):
                        # fil_name = vdd.control(file_contents,file_names,"diagram")
                # fil_name = vdd_diagram.process_control(file_contents,file_names,"diagram")
                print("Inside spinner")

                dbml_file = vdd2.vdd_file_creation(file_contents,file_names,st.session_state.repo_name,st.session_state.repo_directory)
                print("DBML File: ",dbml_file)
                vdd_path = os.path.join(st.session_state.repo_directory, st.session_state.repo_name + ".svg")

                install_npm()

                subprocess.run(["dbml-renderer", "-i", dbml_file, "-o", vdd_path])
            st.image(vdd_path)
            with open(vdd_path, "rb") as file:
                btn = st.download_button(
                            label="Download image",
                            data=file,
                            file_name=st.session_state.repo_name + ".svg",
                            mime="image/svg+xml"
                        )
        except Exception as e:
            print(e)
            st.error(e)
            st.info("We are working hard on our artistic skills to develop the best possible diagram for you. We will get back to you very soon!")

