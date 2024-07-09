import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas
import pdb
# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'original_images' not in st.session_state:
    st.session_state.original_images = []

if 'masks' not in st.session_state:
    st.session_state.masks = []

if 'restored_images' not in st.session_state:
    st.session_state.restored_images = []

# Define restoration model options
restoration_models = ["Model A", "Model B", "Model C"]

# Upload page and parameter settings
with st.sidebar:
    st.title("Parameter Settings and Image Upload")
    uploaded_files = st.file_uploader("Select images to upload", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.session_state.original_images = [Image.open(file) for file in uploaded_files]
        st.session_state.masks = [None] * len(uploaded_files)
        st.session_state.restored_images = [None] * len(uploaded_files)
        st.session_state.current_index = 0

if st.session_state.uploaded_files:
    current_index = st.session_state.current_index

    # Use selectbox to manage image switching
    selected_image = st.selectbox(
        "Select Image",
        options=[file.name for file in st.session_state.uploaded_files],
        index=current_index,
        key="select_image"
    )

    new_index = [file.name for file in st.session_state.uploaded_files].index(selected_image)
    if new_index != current_index:
        st.session_state.current_index = new_index
        st.session_state.masks[new_index] = None
        st.session_state.restored_images[new_index] = None

    current_file = st.session_state.uploaded_files[st.session_state.current_index]
    original_image = st.session_state.original_images[st.session_state.current_index]
    # pdb.set_trace()
    st.write("Current Image:")
    st.write(f"{st.session_state.current_index + 1} / {len(st.session_state.uploaded_files)}")

# Display and annotation page
if st.session_state.uploaded_files:
    st.write("Original Image Before Restoration")
    brush_size = st.slider("Brush Size", 1, 50, 10)
    brush_shape = st.selectbox("Brush Shape", ["Circle", "Square"])
    brush_opacity = st.slider("Brush Opacity", 0, 255, 128)

    # Use streamlit_drawable_canvas to draw mask
    canvas_result = st_canvas(
        fill_color=f"rgba(255, 165, 0, {brush_opacity / 255})",  # Canvas fill color
        stroke_width=brush_size,
        stroke_color="#000000",
        background_image=original_image,
        update_streamlit=True,
        # height=original_image.height,
        # width=original_image.width,
        drawing_mode="freedraw",
        key="canvas",
    )

    # Save mask
    if canvas_result.image_data is not None:
        mask_image = Image.fromarray((canvas_result.image_data[:, :, 3] > 128).astype(np.uint8) * 255).resize(original_image.size)  # Extract alpha channel as mask and ensure size consistency
        st.session_state.masks[st.session_state.current_index] = mask_image

    if st.button("Generate Mask Automatically"):
        # Generate a simulated hand-drawn mask using random walk algorithm
        mask = Image.new("L", original_image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Parameters for random walk
        num_steps = 1000  # Number of steps in the random walk
        step_size = 10  # Size of each step
        
        x, y = np.random.randint(0, original_image.width), np.random.randint(0, original_image.height)
        
        for _ in range(num_steps):
            angle = np.random.uniform(0, 2 * np.pi)
            x_new = int(x + step_size * np.cos(angle))
            y_new = int(y + step_size * np.sin(angle))
            
            x_new = np.clip(x_new, 0, original_image.width - 1)
            y_new = np.clip(y_new, 0, original_image.height - 1)
            
            draw.line([x, y, x_new, y_new], fill=255, width=brush_size)
            
            x, y = x_new, y_new
                
        st.session_state.masks[st.session_state.current_index] = mask

    # Display mask
    if st.session_state.masks[st.session_state.current_index] is not None:
        st.image(st.session_state.masks[st.session_state.current_index], caption="Generated Mask", use_column_width=True)

    # Save and download mask directly
    if st.session_state.masks[st.session_state.current_index] is not None:
        buffer = io.BytesIO()
        st.session_state.masks[st.session_state.current_index].save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button(
            label="Save Mask",
            data=buffer,
            file_name="mask.png",
            mime="image/png"
        )

    st.write("Restored Image")
    if st.session_state.restored_images[st.session_state.current_index] is None:
        st.image(original_image, caption="Restored Image", use_column_width=True)
    else:
        st.image(st.session_state.restored_images[st.session_state.current_index], caption="Restored Image", use_column_width=True)

    # Select restoration model and start restoration
    restoration_model = st.selectbox("Select Restoration Model", restoration_models)
    if st.button("Start Restoration"):
        # Add restoration logic here
        mask = st.session_state.masks[st.session_state.current_index]
        if mask is not None:
            restored_image = Image.composite(original_image, ImageOps.invert(original_image), mask)
            st.session_state.restored_images[st.session_state.current_index] = restored_image
            st.success("Restoration Complete!")
        else:
            st.warning("Please generate or draw a mask first.")

    # Provide download option for restored image
    if st.session_state.restored_images[st.session_state.current_index] is not None:
        restored_image = st.session_state.restored_images[st.session_state.current_index]
        buffer = io.BytesIO()
        restored_image.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button(
            label="Download Restored Image",
            data=buffer,
            file_name="restored_image.png",
            mime="image/png"
        )