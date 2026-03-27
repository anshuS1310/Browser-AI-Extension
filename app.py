from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = Flask(__name__)
# CORS is required for the Chrome Extension to communicate with this server
CORS(app)

# 1. Load the Model and Tokenizer
# flan-t5-base is ~1GB. It's smart and follows instructions well.
model_id = "google/flan-t5-small" #can use any flan-t5 variant, but smaller models are faster and still good for our use case.
print(f"Starting AI Engine with {model_id}...")

# Check if you have an NVIDIA GPU (CUDA), otherwise use CPU (-1)
device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

# Initialize the pipeline
pipe = pipeline(
    "text2text-generation", 
    model=model, 
    tokenizer=tokenizer, 
    device=device
)

print("🚀 AI Engine is Online and Ready.")

@app.route('/')
def home():
    return "<h1>Bouncy AI Backend</h1><p>Status: Online. Waiting for extension requests...</p>"

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        task = data.get('task', 'explain')

        if not user_input:
            return jsonify({"output": "Input is empty. Please scan some text!"})

        # 2. Prompt Engineering
        # We tell the model what its 'job' is so it doesn't just copy the text.
        if task == "summarize":
            prompt = f"Provide a detailed and long-form technical summary of the following content: {user_input}"
        else:
            prompt = f"Explain the following text in great detail like a helpful AI assistant: {user_input}"

        # 3. Generation Parameters (The Fix for 'Rubbish' looping)
        result = pipe(
            prompt[:2500],          # Limit input to prevent memory crashes
            max_new_tokens=3072,     # Allow for long, detailed answers
            min_length=10,          # Force the AI to be descriptive
            do_sample=True,         # Enables creative word selection
            temperature=0.7,        # 0.7 is the 'sweet spot' for balanced answers
            top_p=0.9,              # Nucleus sampling
            repetition_penalty=2.5, # STOPS the repeating text bug
            no_repeat_ngram_size=3  # Specifically blocks repeating 3-word phrases
        )
        
        response_text = result[0]['generated_text']
        
        print(f"Generated Output: {response_text[:50]}...")
        
        return jsonify({
            "status": "success",
            "output": response_text
        })

    except Exception as e:
        print(f"Error encountered: {e}")
        return jsonify({
            "status": "error",
            "output": f"AI Engine Error: {str(e)}"
        })

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=False)