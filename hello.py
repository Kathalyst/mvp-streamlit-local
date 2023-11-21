import streamlit
import github_process

streamlit.header("Kathalyst - Automated Software Documentation")

github_link = streamlit.sidebar.text_input("Github Link")
if streamlit.sidebar.button("Submit"):
    #process if submit button is pressed
    print(f'Processing {github_link}')
    file_contents,file_names = github_process.control(github_link)

    streamlit.write(file_names)
    streamlit.write(file_contents)
    pass
