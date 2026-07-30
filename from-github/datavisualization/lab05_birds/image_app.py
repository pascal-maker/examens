import gradio as gr
import cv2
import numpy as np
import torch
from torchvision import models
from PIL import Image, ImageOps
import json
import urllib.request

# Load standard ImageNet class labels for the recognition output
url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
try:
    with urllib.request.urlopen(url) as response:
        categories = [line.decode('utf-8').strip() for line in response.readlines()]
except Exception:
    categories = []

# Initialize the EfficientNet model (b0 is small and fast)
try:
    weights = models.EfficientNet_B0_Weights.DEFAULT
    model = models.efficientnet_b0(weights=weights)
    model.eval()
    preprocess = weights.transforms()
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")

def convert_to_grayscale(img: Image.Image):
    if img is None: return None
    return ImageOps.grayscale(img)

def get_image_details(img: Image.Image):
    if img is None: return "No image provided."
    details = {
        "Format": img.format or "Unknown (likely memory/array)",
        "Mode": img.mode,
        "Size": f"{img.width} x {img.height} pixels"
    }
    return json.dumps(details, indent=4)

def detect_edges(img: Image.Image):
    if img is None: return None
    # Convert PIL Image to OpenCV format (numpy array)
    img_cv = np.array(img.convert('RGB'))
    # Convert RGB to BGR for OpenCV
    img_cv = img_cv[:, :, ::-1].copy()
    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # Apply Canny Edge Detection
    edges = cv2.Canny(gray, threshold1=100, threshold2=200)
    # Convert back to PIL Image (L mode for grayscale)
    return Image.fromarray(edges)

def recognize_object(img: Image.Image):
    if img is None: return "No image provided."
    if model is None or not categories:
        return "Model or class labels failed to load."
    
    # Preprocess image
    img_tensor = preprocess(img.convert('RGB')).unsqueeze(0)
    
    # Inference
    with torch.no_grad():
        output = model(img_tensor)
        
    # Get top 3 predictions
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top3_prob, top3_catid = torch.topk(probabilities, 3)
    
    results = {}
    for i in range(top3_prob.size(0)):
        cat_name = categories[top3_catid[i].item()]
        prob = top3_prob[i].item() * 100
        results[cat_name] = f"{prob:.2f}%"
        
    return json.dumps(results, indent=4)


# Build the Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🖼️ Image Processing Studio")
    gr.Markdown("Upload an image or use your webcam to process it. Choose a tool from the tabs below!")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Enabling webcam and upload sources
            input_image = gr.Image(type="pil", label="Input Image", sources=["upload", "webcam", "clipboard"])
            
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.Tab("1. Grayscale"):
                    gr.Markdown("Convert your image to black and white.")
                    btn_gray = gr.Button("Convert to Grayscale", variant="primary")
                    out_gray = gr.Image(type="pil", label="Grayscale Output", interactive=False)
                    btn_gray.click(fn=convert_to_grayscale, inputs=input_image, outputs=out_gray)
                    
                with gr.Tab("2. Image Details"):
                    gr.Markdown("Extract basic metadata like format, size, and color mode.")
                    btn_details = gr.Button("Get Details", variant="primary")
                    out_details = gr.Code(language="json", label="Image JSON Data")
                    btn_details.click(fn=get_image_details, inputs=input_image, outputs=out_details)
                    
                with gr.Tab("3. Object Recognition (EfficientNet)"):
                    gr.Markdown("Use an AI model (`efficientnet_b0`) to classify the main object in the image.")
                    btn_recog = gr.Button("Recognize Object", variant="primary")
                    out_recog = gr.Code(language="json", label="Top 3 Predictions")
                    btn_recog.click(fn=recognize_object, inputs=input_image, outputs=out_recog)
                    
                with gr.Tab("Bonus: Edge Detection"):
                    gr.Markdown("Use OpenCV Canny Edge Detection to highlight sharp edges.")
                    btn_edges = gr.Button("Detect Edges", variant="primary")
                    out_edges = gr.Image(type="pil", label="Edges Output", interactive=False)
                    btn_edges.click(fn=detect_edges, inputs=input_image, outputs=out_edges)

if __name__ == "__main__":
    demo.launch()
