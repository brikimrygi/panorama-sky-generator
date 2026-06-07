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
        ["Automatic (auto-detect)", "Spherical (flat horizon)", "Standard (full 360 sphere)"]
    )
    
    selected_mode = "auto"
    if mode_option == "Standard (full 360 sphere)":
        selected_mode = "standard"
    elif mode_option == "Spherical (flat horizon)":
        selected_mode = "spherical"
    else:
        selected_mode = "standard" if (1.95 <= aspect <= 2.05) else "spherical"
        
    st.sidebar.subheader("Filters & Optimizations")
    no_pinch = st.sidebar.checkbox("Remove vortex/pinch (No Pinch)", value=True, help="Blends and smoothes the zenith/nadir poles")
    
    # Bypass filters
    st.sidebar.markdown("**Disable filters for specific faces:**")
    nf_top = st.sidebar.checkbox("No filter for TOP face", value=False)
    nf_bottom = st.sidebar.checkbox("No filter for BOTTOM face", value=False)
    nf_front = st.sidebar.checkbox("No filter for FRONT face", value=False)
    nf_back = st.sidebar.checkbox("No filter for BACK face", value=False)
    nf_left = st.sidebar.checkbox("No filter for LEFT face", value=False)
    nf_right = st.sidebar.checkbox("No filter for RIGHT face", value=False)
    
    # Output layout options
    output_option = st.sidebar.radio("What do you want to generate?", ["Everything (individual faces + templates)", "Only starfield02.png (3x2 Grid)", "Only individual sky_*.png faces"])

    raw_mode = (output_option == "Only individual sky_*.png faces")
    final_mode = (output_option == "Only starfield02.png (3x2 Grid)")

    if st.button("Start Conversion", type="primary"):
        with st.spinner("Processing image... Please wait."):
            faces = ['front', 'back', 'right', 'left', 'top', 'bottom']
            generated_images = {}
            
            # Generate faces
            for face in faces:
                if face == 'left' and not nf_left:
                    face_image = generated_images['right'].transpose(FLIP_LR)
                else:
                    face_data = project_face(img_array, face, face_size, selected_mode, no_pinch)
                    face_image = Image.fromarray(face_data)
                
                if not raw_mode and not final_mode:
                    # Apply classic filters
                    if face == 'top' and not nf_top:
                        face_image = face_image.transpose(FLIP_TB)
                    elif face == 'bottom' and not nf_bottom:
                        face_image = face_image.transpose(ROT_180)
                    elif face == 'front' and not nf_front:
                        right_half = face_image.crop((face_size // 2, 0, face_size, face_size))
                        mirrored_left = right_half.transpose(FLIP_LR)
                        face_image.paste(mirrored_left, (0, 0))
                    elif face == 'back' and not nf_back:
                        left_half = face_image.crop((0, 0, face_size // 2, face_size))
                        mirrored_right = left_half.transpose(FLIP_LR)
                        face_image.paste(mirrored_right, (face_size // 2, 0))
                
                generated_images[face] = face_image.copy()
                
            # Prepare ZIP archive in memory
            zip_buffer = io.BytesIO()
            
            # We also define these variables outside the block so they are accessible for rendering previews
            starfield02 = None
            
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                # Save individual faces to ZIP
                if not final_mode:
                    for face in faces:
                        # Copy bottom with 90 CW rotation for the standalone file
                        face_img_to_save = generated_images[face].copy()
                        if face == 'bottom' and not nf_bottom:
                            face_img_to_save = face_img_to_save.transpose(ROT_90_CW)
                        
                        img_byte_arr = io.BytesIO()
                        face_img_to_save.save(img_byte_arr, format='PNG')
                        zip_file.writestr(f"sky_{face}.png", img_byte_arr.getvalue())
                
                if not raw_mode:
                    # Build vertical 1x3 strip in memory
                    strip_1x3 = Image.new('RGB', (face_size, face_size * 3))
                    strip_1x3.paste(generated_images['top'], (0, 0))
                    strip_1x3.paste(generated_images['front'], (0, face_size))
                    
                    sky_bottom_rotated = generated_images['bottom']
                    if not nf_bottom:
                        sky_bottom_rotated = sky_bottom_rotated.transpose(ROT_90_CW)
                    strip_1x3.paste(sky_bottom_rotated, (0, face_size * 2))
                    
                    if not nf_bottom:
                        left_half_bottom = strip_1x3.crop((0, face_size * 2, face_size // 2, face_size * 3))
                        mirrored_right_bottom = left_half_bottom.transpose(FLIP_LR)
                        strip_1x3.paste(mirrored_right_bottom, (face_size // 2, face_size * 2))
                        
                    if not final_mode:
                        img_byte_arr = io.BytesIO()
                        strip_1x3.save(img_byte_arr, format='PNG')
                        zip_file.writestr("skybox_strip_1x3.png", img_byte_arr.getvalue())
                    
                    # Generate starfield02.png
                    starfield02 = Image.new('RGB', (face_size * 3, face_size * 2))
                    top_from_1x3 = strip_1x3.crop((0, 0, face_size, face_size))
                    front_from_1x3 = strip_1x3.crop((0, face_size, face_size, face_size * 2))
                    bottom_from_1x3 = strip_1x3.crop((0, face_size * 2, face_size, face_size * 3))
                    
                    starfield02.paste(bottom_from_1x3, (0, 0))
                    starfield02.paste(top_from_1x3, (face_size, 0))
                    starfield02.paste(generated_images['back'], (face_size * 2, 0))
                    starfield02.paste(generated_images['left'], (0, face_size))
                    starfield02.paste(front_from_1x3, (face_size, face_size))
                    starfield02.paste(generated_images['right'], (face_size * 2, face_size))
                    
                    img_byte_arr = io.BytesIO()
                    starfield02.save(img_byte_arr, format='PNG')
                    zip_file.writestr("starfield02.png", img_byte_arr.getvalue())
                    
                    # Generate auxiliary 3x2 grid with labels
                    if not final_mode:
                        grid_3x2 = Image.new('RGBA', (face_size * 3, face_size * 2), (0, 0, 0, 0))
                        grid_3x2.paste(generated_images['back'].convert('RGBA'), (face_size * 2, 0))
                        grid_3x2.paste(generated_images['left'].convert('RGBA'), (0, face_size))
                        grid_3x2.paste(generated_images['right'].convert('RGBA'), (face_size * 2, face_size))
                        
                        draw = ImageDraw.Draw(grid_3x2)
                        try:
                            font = ImageFont.load_default(size=int(face_size * 0.08))
                        except TypeError:
                            font = ImageFont.load_default()
                            
                        red_color = (255, 0, 0, 255)
                        draw.text((face_size // 2, face_size // 2), "bottom", fill=red_color, font=font, anchor="mm")
                        draw.text((face_size + face_size // 2, face_size // 2), "top", fill=red_color, font=font, anchor="mm")
                        draw.text((face_size + face_size // 2, face_size + face_size // 2), "front", fill=red_color, font=font, anchor="mm")
                        
                        img_byte_arr = io.BytesIO()
                        grid_3x2.save(img_byte_arr, format='PNG')
                        zip_file.writestr("skybox_grid_3x2.png", img_byte_arr.getvalue())
            
            st.success("Conversion completed successfully!")
            
            # Offer download ZIP button
            st.download_button(
                label="📁 Download ZIP archive with textures",
                data=zip_buffer.getvalue(),
                file_name="skybox_textures.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # --- Previews Section (Displayed below the download button) ---
            st.markdown("---")
            st.subheader("🖼️ Generated Textures Preview")
            
            # 1. Preview of starfield02.png composite grid
            if not raw_mode and starfield02 is not None:
                st.write("**starfield02.png (3x2 Composite Layout):**")
                st.image(starfield02, caption="starfield02.png", use_container_width=True)
            
            # 2. Previews of individual faces (sky_*.png)
            if not final_mode:
                st.write("**Individual Skybox Faces:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(generated_images['top'], caption="sky_top.png (Zenith)", use_container_width=True)
                    st.image(generated_images['left'], caption="sky_left.png", use_container_width=True)
                with col2:
                    st.image(generated_images['front'], caption="sky_front.png", use_container_width=True)
                    
                    # For bottom preview, we also show the 90 CW rotated file version as on disk
                    bottom_preview = generated_images['bottom'].copy()
                    if not nf_bottom:
                        bottom_preview = bottom_preview.transpose(ROT_90_CW)
                    st.image(bottom_preview, caption="sky_bottom.png (Nadir)", use_container_width=True)
                with col3:
                    st.image(generated_images['right'], caption="sky_right.png", use_container_width=True)
                    st.image(generated_images['back'], caption="sky_back.png", use_container_width=True)