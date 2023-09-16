from PIL import Image
import os

def alter_image(image_path, output_folder):
    print(f"Processing: {image_path}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open an image
    img = Image.open(image_path)
    
    # Extract the filename without extension to use for output filenames
    filename = os.path.basename(image_path).split('.')[0]
    
    # 1. Convert to grayscale
    grayscale = img.convert('L')
    grayscale.save(os.path.join(output_folder, f'{filename}_grayscale.png'))

    # 2. Rotate the image by 45 degrees
    rotated = img.rotate(45)
    rotated.save(os.path.join(output_folder, f'{filename}_rotated.png'))

    # 3. Flip the image horizontally
    flip_horizontal = img.transpose(Image.FLIP_LEFT_RIGHT)
    flip_horizontal.save(os.path.join(output_folder, f'{filename}_flip_horizontal.png'))

    # 4. Flip the image vertically
    flip_vertical = img.transpose(Image.FLIP_TOP_BOTTOM)
    flip_vertical.save(os.path.join(output_folder, f'{filename}_flip_vertical.png'))

    # 5. Resize the image
    resized = img.resize((100, 100))
    resized.save(os.path.join(output_folder, f'{filename}_resized.png'))

if __name__ == "__main__":
    # Input and output folder paths
    input_folder_path = 'test_images'
    output_folder_path = 'output_images'
    
    # Check if the input folder exists
    if not os.path.exists(input_folder_path):
        print(f"The folder {input_folder_path} does not exist.")
        exit(1)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.lower().endswith('.png'):
            input_image_path = os.path.join(input_folder_path, filename)
            alter_image(input_image_path, output_folder_path)
