
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from ddg_search2 import get_search_result
from ddg_search2 import link
#from ddg_search import get_search_results
#from ddg_search import link
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
#import streamlit as st
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)





def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        #chunk_size=1000,
        chunk_size=500,
        #chunk_overlap=200,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #temperature=0.7
     
    temperature=0
    #temperature=0,
    #model_name='gpt-3.5-turbo'
    #'model': 'gpt-4-32k',
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.7, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def init():

    if load_dotenv(os.environ.get('OPENAI_API_KEY')) is None or load_dotenv(os.environ.get('OPENAI_API_KEY')) == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # # setup streamlit page
    # st.set_page_config(
    #     page_title="Customer Support ChatBot",
    #     page_icon="🤖"
    # )
   
def main():
    init()
    #st.title('WebWisdom :blue[Bot] ')
    st.title('Web-ChatBot Wisdom')
    st.header('Powered :blue[By]',)
    st.write('''<style>
"<style>.st-emotion-cache-1v0mbdj.e115fcil1 {
    max-width: 100px;
    display: flex;
} </style>''', unsafe_allow_html=True)
    image = Image.open('logo.jpeg')
    new_image = image.resize((400, 200))
    st.image(image, caption='')
    st.header('', divider='rainbow')
    # st.header('This is a header with a divider', divider='rainbow')
    #st.subheader('This is a subheader with a divider', divider='rainbow')
    # st.subheader('Enter Website Url to  :blue[Explore]')
    # xyz = st.text_input("Please enter Website url in e.g ihubiitmandi.in")
    my_bar = st.progress(0)
    status_text = st.empty()
    # st.header('This is a header with a divider', divider='rainbow')
    #st.subheader('This is a subheader with a divider', divider='rainbow')
    st.subheader('Enter Website Url to  :blue[Explore]')
    xyz = st.text_input("Please input the website URL here and Press Enter button: for example, ihubiitmandi.in.")
    #st.header('', divider='rainbow')
    main_contener = st.container()
    # link = st.chat_input("Type Your website link here and Press Enter button: ", key="user_input2")

   
    link(xyz)
    main_contener.style.width = "100px"  # Set the width
    main_contener.style.height = "300px"  # Set the height
    main_contener.style.overflow = "auto"  # Add both vertical and horizontal scrollbars
    #main_contener.title('_Streamlit_ is :blue[cool] :sunglasses:')
    user_input = st.chat_input("Type Your query here and Press Enter button: ", key="user_input")
    with main_contener:
        message("Hello! I'm an AI Assistant ready to help with your website queries.")
        # user_input = st.chat_input("Type Your query here and Press Enter button: ", key="user_input")
        #link = st.chat_input("Type Your website link here and Press Enter button: ", key="user_input2")
        #user_input = st.text_input("Type Your query here and Press Enter button: ", key="user_input")
        if user_input:
            #st.write(f"User has sent the following prompt: {user_input}")
            if "messages" not in st.session_state:
                st.session_state.messages = [
                    SystemMessage(content="You are a helpful Customer assistant.")
                    
                ]
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                raw_text = get_search_result(user_input)
                my_bar.progress(10)
                status_text.text(f'Operation in progress. Please wait: {10}%')
                #raw_text = get_search_results(user_input)
                my_bar.progress(20)
                status_text.text(f'Operation in progress. Please wait: {20}%')
                text_chunks = get_text_chunks(raw_text)
                my_bar.progress(30)
                status_text.text(f'Operation in progress. Please wait: {30}%')
                vectorstore = get_vectorstore(text_chunks)
                my_bar.progress(40)
                status_text.text(f'Operation in progress. Please wait: {40}%')
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                my_bar.progress(50)
                status_text.text(f'Operation in progress. Please wait: {50}%')
                #response = chat(st.session_state.messages)
                response = st.session_state.conversation({'question': user_input})
                my_bar.progress(60)
                status_text.text(f'Operation in progress. Please wait: {60}%')
                #st.write(response)
                st.session_state.chat_history = response['chat_history']
                my_bar.progress(70)
                status_text.text(f'Operation in progress. Please wait: {70}%')
                st.session_state.messages.append(
                AIMessage(content=response['answer']))
                my_bar.progress(80)
                status_text.text(f'Operation in progress. Please wait: {80}%')
                # display message history
                messages = st.session_state.get('messages', [])
                my_bar.progress(100)
                status_text.text(f'Operation in progress. Please wait: {100}%')
                #for i, message in enumerate(st.session_state.chat_history):
                for i, msg in enumerate(messages[1:]):
                    if i % 2 == 0:
                    
                        #message(message.content, is_user=True, key=str(i) + '_user')
                        message(msg.content, is_user=True, key=str(i) + '_user')
                    else:
                        #message(message.content, is_user=False, key=str(i) + '_ai')
                        message(msg.content, is_user=False, key=str(i) + '_ai')



if __name__ == '__main__':
    main()
