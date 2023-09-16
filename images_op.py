from PIL import Image, ImageDraw
import os
import random
import numpy as np

# Create a directory to store generated images
if not os.path.exists('test_images'):
    os.makedirs('test_images')

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to apply gradient opacity
def apply_gradient_opacity(image):
    np_image = np.array(image)
    gradient = np.linspace(0, 255, np_image.shape[0]).astype(np.uint8)
    np_image[:, :, 3] = gradient[:, None]
    return Image.fromarray(np_image, 'RGBA')

# Function to generate a random image
def generate_image(image_number):
    # Random dimensions between 50 and 500
    width = random.randint(50, 500)
    height = random.randint(50, 500)
    
    # Random color depth (either RGB or RGBA)
    color_depth = random.choice(['RGB', 'RGBA'])
    
    # Initialize image
    if color_depth == 'RGB':
        image = Image.new('RGB', (width, height), random_color())
    else:
        image = Image.new('RGBA', (width, height), random_color() + (random.randint(0, 255),))
        image = apply_gradient_opacity(image)
    
    draw = ImageDraw.Draw(image)
    
    # Draw some shapes to make it a bit more interesting
    for _ in range(5):
        shape_kind = random.choice(['rectangle', 'ellipse'])
        x0 = random.randint(0, width - 1)
        y0 = random.randint(0, height - 1)
        x1 = random.randint(x0, width)
        y1 = random.randint(y0, height)
        
        xy = [x0, y0, x1, y1]
        
        if shape_kind == 'rectangle':
            draw.rectangle(xy, fill=random_color())
        else:
            draw.ellipse(xy, fill=random_color())

    # Save the image
    image_path = os.path.join('test_images_op', f'image_{image_number}.png')
    image.save(image_path)
    print(f"Generated {image_path}")

# Generate 50 images
for i in range(50):
    generate_image(i)
