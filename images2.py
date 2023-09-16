from PIL import Image, ImageOps, ImageFilter, UnidentifiedImageError
import os

def alter_image(image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        print(f"Cannot identify the image at {image_path}. Skipping...")
        return

    filename = os.path.basename(image_path).split('.')[0]

    # Convert to different color models and save
    for color_model in ['L', 'P', 'RGB', 'RGBA']:
        try:
            converted = img.convert(color_model)
            converted.save(os.path.join(output_folder, f'{filename}_{color_model}.png'))
        except Exception as e:
            print(f"Error while converting to {color_model}: {e}")

    # Extreme dimensions
    img.resize((1, 1)).save(os.path.join(output_folder, f'{filename}_1x1.png'))
    img.resize((3000, 3000)).save(os.path.join(output_folder, f'{filename}_3000x3000.png'))

    # Apply filters
    for filter_name, filter_obj in [("CONTOUR", ImageFilter.CONTOUR), ("EMBOSS", ImageFilter.EMBOSS)]:
        try:
            filtered_img = img.filter(filter_obj)
            filtered_img.save(os.path.join(output_folder, f'{filename}_{filter_name}.png'))
        except ValueError:
            # Convert to 'RGB' and then apply filter
            rgb_img = img.convert('RGB')
            filtered_img = rgb_img.filter(filter_obj)
            filtered_img.save(os.path.join(output_folder, f'{filename}_{filter_name}_fromRGB.png'))

if __name__ == "__main__":
    input_folder_path = 'test_images'
    output_folder_path = 'output_images'
    
    if not os.path.exists(input_folder_path):
        print(f"The folder {input_folder_path} does not exist.")
        exit(1)

    for filename in os.listdir(input_folder_path):
        if filename.lower().endswith('.png'):
            input_image_path = os.path.join(input_folder_path, filename)
            alter_image(input_image_path, output_folder_path)
