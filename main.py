import os
import sys

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_KEY")

if openai_key == "<YOUR_OPENAI_KEY>":
    openai_key = ""

if openai_key == "":
    sys.exit("Please Provide Your OpenAI API Key")


def generate_image(text, model, quality, size):
    try:
        client = OpenAI(api_key=openai_key)

        response = client.images.generate(
            prompt=text,
            model=model,
            quality=quality,
            size=size,
            n=1,
        )
    except Exception as error:
        print(str(error))
        raise gr.Error("An error occurred while generating speech. Please check your API key and come back try again.")

    return response.data[0].url


with gr.Blocks() as demo:
    gr.Markdown("# <center> OpenAI Image Generate API with Gradio </center>")
    with gr.Row(variant="panel"):
        model = gr.Dropdown(choices=["dall-e-2", "dall-e-3"], label="Model", value="dall-e-3")
        quality = gr.Dropdown(choices=["standard", "hd"], label="Quality", value="standard")
        size = gr.Dropdown(choices=["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], label="Size",
                           value="1024x1024")

    text = gr.Textbox(label="Input Text",
                      placeholder="Enter your text and then click on the \"Image Generate\" button, "
                                  "or simply press the Enter key.")
    btn = gr.Button("Image Generate")
    output_image = gr.Image(label="Image Output")

    text.submit(fn=generate_image, inputs=[text, model, quality, size], outputs=output_image, api_name="generate_image")
    btn.click(fn=generate_image, inputs=[text, model, quality, size], outputs=output_image, api_name=False)

demo.launch()
