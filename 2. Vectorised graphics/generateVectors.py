import cv2
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

def count_black_pixels(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size
    black_pixel_count = 0
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == (0, 0, 0):
                black_pixel_count += 1
    return black_pixel_count

def find_optimal_point(binary_image):
    height, width = binary_image.shape
    max_black_squares = 5
    for y in range(max_black_squares, height - max_black_squares):
        for x in range(max_black_squares, width - max_black_squares):
            if all(binary_image[y+dy, x+dx] == 255 for dy in range(-max_black_squares, max_black_squares + 1) for dx in range(-max_black_squares, max_black_squares + 1)):
                return (x, y)
    return None

def contour_to_lines_and_draw(contour, draw_image):
    instructions = []
    for i in range(len(contour)):
        point1 = ((contour[i][0][0] * 0.1) - 51.0, (contour[i][0][1] * 0.1) - 51.0)
        point2 = ((contour[(i + 1) % len(contour)][0][0] * 0.1) - 51.0, (contour[(i + 1) % len(contour)][0][1] * 0.1) - 51.0)
        point1 = (round(point1[0], 2), round(point1[1], 2))
        point2 = (round(point2[0], 2), round(point2[1], 2))
        instructions.append(f"s.Line(point1={point1}, point2={point2})")
        draw_point1 = (int((point1[0] + 51.0) / 0.1), int((point1[1] + 51.0) / 0.1))
        draw_point2 = (int((point2[0] + 51.0) / 0.1), int((point2[1] + 51.0) / 0.1))
        cv2.line(draw_image, draw_point1, draw_point2, (0, 255, 0), 2)
    return instructions

folderA = 'fontImages'
folderB = 'vectorisedProfiles'

plotting = True

for filename in os.listdir(folderA):
    pathA = os.path.join(folderA, filename)
    pathB = os.path.join(folderB, filename)
    mass = count_black_pixels(pathA)
    density = 1E9 / mass
    image = cv2.imread(pathA, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    draw_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    all_instructions = []
    for contour in contours:
        # Approximate contour to reduce the number of points
        epsilon = 0.001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Limit the number of points to 20
        instructions = contour_to_lines_and_draw(approx, draw_image)
        all_instructions.extend(instructions)
    optimal_point = find_optimal_point(binary_image)
    point_coords = ""
    if optimal_point:
        x, y = optimal_point
        point_coords = (round((x * 0.1) - 51.0, 2), round((y * 0.1) - 51.0, 2))
        cv2.circle(draw_image, (x, y), 5, (255, 0, 0), -1)
    output_text_path = pathB.replace('.png', '.txt')
    with open(output_text_path, 'w') as f:
        f.write(f"filename = {os.path.splitext(filename)[0]}, density = {density:.2f}, point = {point_coords}\n")
        for instruction in all_instructions:
            f.write(instruction + '\n')
    if plotting:
        output_image_path = pathB.replace('.png', '_sketch.png')
        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(draw_image, cv2.COLOR_BGR2RGB))
        plt.title(f'Final Sketch: {filename}')
        plt.axis('off')
        plt.savefig(output_image_path)
        plt.close()

def list_txt_files(folder_path):
    files = os.listdir(folder_path)
    txt_files = [file for file in files if file.endswith('.txt')]
    output_file_path = os.path.join(folder_path, 'fontsToTest.txt')
    with open(output_file_path, 'w') as output_file:
        for txt_file in txt_files:
            output_file.write(txt_file + '\n')
    print(f"List of text files has been written to {output_file_path}")

folder_path = '/'
list_txt_files(folder_path)


