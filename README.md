# Mural Image Restoration under Low-light Measurement condition using Multi-level Interactive Siamese Filtering Strategy

## Web service of MISFR platform

# Tutorial: Using the Web-based Mural Restoration Service

This tutorial will guide you through using the web-based mural restoration service to upload, annotate, and restore mural images.

## Step 1: Install Required Packages

Before running the service, ensure you have the necessary packages installed. You can install them using the following command:

```sh
pip install streamlit pillow numpy streamlit-drawable-canvas

```

## Step 2: Run the Streamlit Application

Start the Streamlit application by running the following command in your terminal:

```sh
streamlit run st_mural_restoration.py
```

Replace st_mural_restoration.py with the name of your Python file if it is different.



## Step 3: Upload Images

1. Open the web service.
2. In the sidebar, you will see a section titled **Parameter Settings and Image Upload**.
3. Click on **Browse files** or drag and drop your images (in PNG, JPG, or JPEG format) into the designated area.
4. The uploaded images will be listed with their names and sizes.

## Step 4: Select and Adjust Image

1. In the main area, use the **Select Image** dropdown to choose the image you want to work on.
2. The current image's position in the list will be displayed (e.g., 1/3).
3. You will see the selected image under the **Original Image Before Restoration** section.

## Step 5: Brush Adjustment

1. Adjust the brush settings for mask creation:
   - **Brush Size**: Use the slider to set the brush size (1 to 50).
   - **Brush Shape**: Choose between **Circle** and **Square** shapes.
   - **Brush Opacity**: Use the slider to set the brush opacity (0 to 255).

## Step 6: Create Mask

1. Use the canvas to draw the mask on the image. The canvas will display the image with the brush settings applied.
2. Alternatively, click the **Generate Mask Automatically** button to create a mask using a random walk algorithm. This will generate a simulated hand-drawn mask.

## Step 7: Display and Save Mask

1. If a mask is created, it will be displayed under the **Generated Mask** section.
2. Click the **Save Mask** button to download the mask as a PNG file.

## Step 8: Image Restoration

1. In the **Restored Image** section, the original image is displayed until the restoration process is complete.
2. Select a restoration model from the **Select Restoration Model** dropdown.
3. Click the **Start Restoration** button to begin the restoration process. The restored image will be generated using the selected model and the created mask.

## Step 9: Save Restored Image

1. Once the restoration is complete, the restored image will be displayed.
2. Click the **Download Restored Image** button to save the restored image as a PNG file.



