import os
from PIL import Image

def merge_pngs_to_pdf(output_path, input_dir):
    # Get a list of all PNG files in the directory
    png_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    png_files.sort()  # Optional: sort files by name

    # List to hold images
    image_list = []

    for png_file in png_files:
        file_path = os.path.join(input_dir, png_file)
        # Open the image file
        img = Image.open(file_path)
        img = img.convert("RGB")
        image_list.append(img)

    # Save the images as a single PDF
    if image_list:
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

if __name__ == '__main__':
    # Define the input directory and the output file path
    input_dir = 'output_plots/'  # Change this to your PNG directory
    output_path = '2DHits.pdf'  # Change this to your desired output PDF path

    # Merge the PNGs into a PDF
    merge_pngs_to_pdf(output_path, input_dir)

    print("PNGs have been merged successfully!")
