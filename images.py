from PIL import Image, ImageDraw
import os
import random
import numpy as np

# Create a directory to store generated images
directory_name = 'test_images'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def add_noise(image):
    np_image = np.array(image)
    noise = np.random.normal(0, 25, np_image.shape).astype(np.uint8)
    np_image += noise
    np_image = np.clip(np_image, 0, 255)
    return Image.fromarray(np_image, image.mode)

def generate_max_entropy_image(image):
    np_image = np.array(image)
    height, width, color_depth = np_image.shape
    
    # Generate random pixel values
    data = np.random.randint(0, 256, (height, width, color_depth), dtype=np.uint8)
    return Image.fromarray(data, 'RGBA')


def generate_sine_gradient(image, frequency, vertical):
    np_image = np.array(image)
    height, width = np_image.shape[:2]
    x_center, y_center = width // 2, height // 2

    for y in range(height):
        for x in range(width):
            dx = x - x_center
            dy = y - y_center
            distance = np.sqrt(dx * dx + dy * dy)
            phase_shift = distance / np.sqrt(width * width + height * height)
            
            if vertical:
                sine_val = int(127 * np.sin(2 * np.pi * frequency * (y / height + phase_shift)) + 128)
            else:
                sine_val = int(127 * np.sin(2 * np.pi * frequency * (x / width + phase_shift)) + 128)

            channel = random.choice([0,1,2])
            np_image[y, x, channel] = sine_val

    return Image.fromarray(np_image, 'RGBA')

def draw_fading_rectangle(draw, x0, y0, x1, y1, start_alpha, end_alpha, color, steps=10):
    alpha_delta = (end_alpha - start_alpha) / steps
    
    for i in range(steps):
        current_alpha = int(start_alpha + i * alpha_delta)
        current_color = color + (current_alpha,)
        
        if x0 < x1 and y0 < y1:
            draw.rectangle([x0, y0, x1, y1], fill=current_color)
        
        x0 += 1
        y0 += 1
        x1 -= 1
        y1 -= 1

def generate_image(image_number):
    width = random.randint(50, 500)
    height = random.randint(50, 500)
    
    image = Image.new('RGBA', (width, height), random_color() + (random.randint(0, 255),))
    draw = ImageDraw.Draw(image)
    
    elements = [ 
        # 'ellipse', 'line', 'polygon', 'point', 'fading_rectangle', 'noise',
                 'max_entropy']

    for _ in range(random.randint(1, 10)):  # Number of random elements to add
        element = random.choice(elements)
        
        x0, y0 = random.randint(0, width-1), random.randint(0, height-1)
        x1, y1 = random.randint(0, width), random.randint(0, height)
        # Sort coordinates
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        coords = [x0, y0, x1, y1]

        if element == 'rectangle':
            draw.rectangle(coords, fill=random_color())
        elif element == 'ellipse':
            draw.ellipse(coords, fill=random_color())
        elif element == 'line':
            draw.line([x0, y0, x1, y1], fill=random_color(), width=random.randint(1, 5))
        elif element == 'polygon':
            num_vertices = random.randint(3, 10)
            vertices = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_vertices)]
            draw.polygon(vertices, fill=random_color())
        elif element == 'point':
            for _ in range(random.randint(1, 100)):
                x, y = random.randint(0, width-1), random.randint(0, height-1)
                draw.point((x, y), fill=random_color())
        elif element == 'noise':
            image = add_noise(image)
            draw = ImageDraw.Draw(image)
        elif element == 'fading_rectangle':
            start_alpha = random.randint(0, 255)
            end_alpha = random.randint(0, 255)
            draw_fading_rectangle(draw, x0, y0, x1, y1, start_alpha, end_alpha, random_color())
        elif element == 'max_entropy':
            image = generate_max_entropy_image(image)
            draw = ImageDraw.Draw(image)
            
    
    # Randomly apply sine gradient to the whole image
    if random.choice([True, False]):
        frequency = random.uniform(0.1, 1.0)
        vertical = random.choice([True, False])
        image = generate_sine_gradient(image, frequency, vertical)
    
    # Save the image
    image_path = os.path.join(directory_name, f'image_{image_number}.png')
    image.save(image_path)
    print(f"Generated {image_path}")

# Generate 50 images
for i in range(50):
    generate_image(i)
