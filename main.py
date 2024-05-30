import io
from fastapi import FastAPI
from langchain_openai import ChatOpenAI

from core.workflow import build_workflow
from langchain_core.messages import HumanMessage

app = FastAPI()


@app.post("/topic")
async def topic():
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    members = [
        "Topic_Agent"
    ]

    graph = build_workflow(llm, members)
    config = {"recursion_limit": 20}

    def generate_graph_image():
        # Assuming graph.get_graph(xray=True).draw_mermaid_png() generates the image data
        image_data = graph.get_graph().draw_mermaid_png()

        # Use io.BytesIO to handle the binary data
        image_bytes = io.BytesIO(image_data)

        # Save the binary data to a file
        with open('output_image.png', 'wb') as file:
            file.write(image_bytes.getbuffer())

    generate_graph_image()

    async def process_chat_stream():
        captured_messages = []
        for message in await graph.stream(
            {
                "messages": [
                    HumanMessage(
                        content="Create a blog post on the topic 'The Future of AI in Healthcare'."
                    )
                ]
            }, config=config
        ):
            print(message)
            if "__end__" not in message:
                captured_messages.append(message)
        return captured_messages

    return process_chat_stream()
