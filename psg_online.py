import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

# Safe retrieval of transposition methods for Pillow
ROT_90_CW = Image.Transpose.ROTATE_270
ROT_90_CCW = Image.Transpose.ROTATE_90
ROT_180 = Image.Transpose.ROTATE_180
FLIP_LR = Image.Transpose.FLIP_LEFT_RIGHT
FLIP_TB = Image.Transpose.FLIP_TOP_BOTTOM

def project_face(img_array, face, face_size, selected_mode, no_pinch=False):
    h_pano, w_pano, channels = img_array.shape
    u, v = np.meshgrid(np.linspace(-1, 1, face_size), np.linspace(-1, 1, face_size))
    
    if face == 'front':
        x = np.ones_like(u)
        y = -u
        z = -v
    elif face == 'back':
        x = -np.ones_like(u)
        y = u
        z = -v
    elif face == 'left':
        x = u
        y = np.ones_like(u)
        z = -v
    elif face == 'right':
        x = -u
        y = -np.ones_like(u)
        z = -v
    elif face == 'top':
        x = u
        y = -v
        z = np.ones_like(u)
    elif face == 'bottom':
        x = u
        y = v
        z = -np.ones_like(u)
        
    aspect = w_pano / h_pano
    
    if selected_mode == "standard":
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arcsin(z / r)
        px = ((theta + np.pi) / (2 * np.pi)) * (w_pano - 1)
        py = ((np.pi / 2 - phi) / np.pi) * (h_pano - 1)
    else:
        theta = np.arctan2(y, x)
        d = np.sqrt(x**2 + y**2)
        d_safe = np.where(d < 1e-5, 1e-5, d)
        v_ratio = z / d_safe
        px = ((theta + np.pi) / (2 * np.pi)) * (w_pano - 1)
        v_scale = aspect / 2.0
        py = (0.5 - (v_ratio * v_scale / 2.0)) * (h_pano - 1)
        
    px = np.clip(np.round(px).astype(int), 0, w_pano - 1)
    py = np.clip(np.round(py).astype(int), 0, h_pano - 1)
    
    if no_pinch and (face in ['top', 'bottom']):
        if face == 'top':
            avg_color = np.mean(img_array[0, :, :], axis=0)
        else:
            avg_color = np.mean(img_array[-1, :, :], axis=0)
            
        d_center = np.sqrt(u**2 + v**2)
        blend_radius = 0.5
        alpha = np.clip(d_center / blend_radius, 0.0, 1.0)
        alpha_3d = np.expand_dims(alpha, axis=-1)
        
        sampled_pixels = img_array[py, px]
        blended_pixels = (alpha_3d * sampled_pixels + (1.0 - alpha_3d) * avg_color).astype(np.uint8)
        return blended_pixels
    else:
        return img_array[py, px]

# --- Streamlit User Interface ---
st.set_page_chart_util = False
st.set_page_config(page_title="Skybox Generator", page_icon="🌤️", layout="centered")

st.title("🌤️ Panorama to Skybox Generator")
st.write("Upload a flat or spherical panoramic image and generate textures for games (e.g. Minecraft).")

uploaded_file = st.file_uploader("Choose a panorama file (JPG / PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    img = Image.open(uploaded_file).convert('RGB')
    img_array = np.array(img)
    h_pano, w_pano, _ = img_array.shape
    aspect = w_pano / h_pano
    
    st.image(img, caption=f"Loaded panorama: {uploaded_file.name} ({w_pano}x{h_pano}px, aspect ratio {aspect:.2f}:1)", use_container_width=True)
    
    st.sidebar.header("Generator Settings")
    
    # Face size selection
    face_size = st.sidebar.selectbox("Individual face size (px)", [512, 1024, 2048, 4096], index=1)
    
    # Projection mode selection
    mode_option = st.sidebar.selectbox(
        "Horizon Projection Mode", 
        ["Automatic (auto-detect)", "Spherical (flat horizon)", "
