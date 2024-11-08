from flask import Flask, request, jsonify
import google.generativeai as genai
import PIL.Image
import io
import os
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

# Configure Gemini API - get key from https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model - UPDATED MODEL NAME HERE
model = genai.GenerativeModel('gemini-1.5-flash')  # Changed from gemini-pro-vision

def analyze_food_image(image_content) -> str:
    """
    Analyze image using Gemini API and return food description
    """
    try:
        prompt = """
        Look at this food image and:
        1. Identify the main dish/food item
        2. List visible ingredients or components
        3. Return ONLY a simple description in this format: [main dish] with [ingredients]
        For example: "pizza with cheese, tomatoes, basil" or "chocolate cake with frosting, berries"
        """
        
        # Convert bytes to PIL Image
        image_bytes = image_content.read()
        image = PIL.Image.open(io.BytesIO(image_bytes))
        
        # Generate response
        response = model.generate_content([prompt, image])
        
        # Clean and format the response
        description = response.text.strip().lower()
        description = description.replace('"', '').replace("'", '')
        
        return description if description else "food dish"
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return f"food dish (Error: {str(e)})"

# @app.route('/analyze-food-image', methods=['POST'])
# def handle_analyze_food_image():
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file provided"}), 400
            
#         file = request.files['image']
        
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
        
#         # Call the analyze function with the file
#         description = analyze_food_image(file)
        
#         return jsonify({
#             "success": True,
#             "generated_query": description
#         })
    
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

# @app.route('/', methods=['GET'])
# def upload_form():
#     return '''
#     <html>
#     <body>
#         <h1>Upload Food Image</h1>
#         <form action="/analyze-food-image" method="post" enctype="multipart/form-data">
#             <input type="file" name="image" accept="image/*">
#             <input type="submit" value="Analyze Image">
#         </form>
#     </body>
#     </html>
#     '''

if __name__ == '__main__':
    pass