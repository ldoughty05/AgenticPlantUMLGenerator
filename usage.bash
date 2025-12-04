# Install dependency
pip install google-generativeai

# Set your API key
export GEMINI_API_KEY="your-key-here"

# Run it
python er_verifier.py diagram.jpg \
    --description "An e-commerce system with customers, orders, products, and inventory tracking" \
    --output result.puml

# See full analysis (not just the code)
python er_verifier.py diagram.jpg \
    --description "University course registration system" \
    --full-response