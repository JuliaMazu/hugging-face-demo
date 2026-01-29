import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer explicitly to avoid "Unknown Task" errors
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def predict(text):
    if not text.strip():
        return "Please enter some text."
    
    # T5 requires the prefix "summarize: "
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Simple AI Summarizer")
    with gr.Row():
        input_text = gr.Textbox(label="Long Text", placeholder="Paste your article here...", lines=10)
        output_text = gr.Textbox(label="Summary", lines=5)
    btn = gr.Button("Summarize")
    btn.click(fn=predict, inputs=input_text, outputs=output_text)

demo.launch()