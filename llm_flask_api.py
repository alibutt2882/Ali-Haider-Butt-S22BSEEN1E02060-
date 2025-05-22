from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)
CORS(app)

# Load model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No JSON payload received"}), 400
        prompt = data.get('prompt', '')
        max_length = min(int(data.get('max_length', 50)), 200)
        
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)