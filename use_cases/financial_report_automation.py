import os
from dotenv import load_dotenv

from autogen import AssistantAgent, UserProxyAgent
import pandas as pd
import streamlit as st

load_dotenv()

# Define LLM configuration
model = "gpt-3.5-turbo"
llm_config = {
    "model": model,
    "temperature": 0.9,
    "api_key": os.environ["OPENAI_API_KEY"],
}

# Define the data aggregation agent
data_aggregation_agent = AssistantAgent(
    name="Data_Aggregation_Agent",
    llm_config=llm_config,
    system_message="""
        You collect and aggregate financial data from the provided CSV file for the monthly financial report.

    """,
)

# Define the report generation agent
report_generation_agent = AssistantAgent(
    name="Report_Generation_Agent",
    llm_config=llm_config,
    system_message="""
    You generate detailed financial reports based on the aggregated data.
    """,
)

# Define the accuracy review agent
accuracy_review_agent = AssistantAgent(
    name="Accuracy_Review_Agent",
    llm_config=llm_config,
    system_message="""
    You check the financial report for accuracy and consistency.
    """,
)

# Define the compliance review agent
compliance_review_agent = AssistantAgent(
    name="Compliance_Review_Agent",
    llm_config=llm_config,
    system_message="""
    You ensure the financial report complies with financial regulations and standards.
    """,
)

# Define the summary generation agent
summary_generation_agent = AssistantAgent(
    name="Summary_Generation_Agent",
    llm_config=llm_config,
    system_message="""
    You summarize the financial report for executive presentations.
    """,
)

# Define the feedback agent
feedback_agent = AssistantAgent(
    name="Feedback_Agent",
    llm_config=llm_config,
    system_message="""
    You collect feedback from executives on the summary of the financial report.
    """,
)

# Define the user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "my_code",
        "use_docker": False,
    },
)


# Function to read CSV file and prepare data for aggregation
def read_csv_file():
    print("Reading CSV file...")
    df = pd.read_csv("financial_data.csv")
    return df.to_dict()


# Register nested chats with the user proxy agent
user_proxy.register_nested_chats(
    [
        {
            "recipient": report_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Generate a detailed financial report based on the following data: {read_csv_file()}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": accuracy_review_agent,
            "message": lambda recipient, messages, sender, config: f"Check this report for accuracy and consistency: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": compliance_review_agent,
            "message": lambda recipient, messages, sender, config: f"Ensure this report complies with financial regulations and standards: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": summary_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Summarize the financial report for an executive presentation: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": feedback_agent,
            "message": lambda recipient, messages, sender, config: f"Collect feedback on this summary from executives: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
    ],
    trigger=data_aggregation_agent,
)

# Define the initial data aggregation task
initial_task = (
    """Collect and aggregate financial data for the monthly financial report."""
)

# Start the nested chat
user_proxy.initiate_chat(
    recipient=data_aggregation_agent,
    message=initial_task,
    max_turns=2,
    summary_method="last_msg",
)

# Interfaz básica con Streamlit
st.title("Financial Report Automation")
st.write("This project automates the generation and review of financial reports using intelligent agents.")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        # Guardar el archivo subido para que los agentes lo usen
        df.to_csv("financial_data.csv", index=False)
        st.success("File uploaded successfully. Ready to process the report.")
    except Exception as e:
        st.error(f"Error reading the file: {e}")

if st.button("Generate and display summary of the financial report"):
    try:
        # Ejecutar el flujo de agentes
        user_proxy.initiate_chat(
            recipient=data_aggregation_agent,
            message=initial_task,
            max_turns=2,
            summary_method="last_msg",
        )
        # Suponiendo que el resumen generado está en la última respuesta del feedback_agent
        # (Ajusta esto según cómo tu framework devuelva los resultados)
        st.subheader("Summary generated by Summary_Generation_Agent:")
        for idx, msg in enumerate(summary_generation_agent.chat_messages[user_proxy]):
            st.markdown(f"**Mensaje {idx+1}:**")
            st.write(msg["content"])
    except Exception as e:
        st.error(f"Error generating the summary: {e}")
