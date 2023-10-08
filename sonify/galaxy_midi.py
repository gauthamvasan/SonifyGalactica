import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load your image
    image = cv2.imread('/Users/gautham/Downloads/nasa_space_image.jpg')
    
    image = cv2.resize(image, dsize=(100, 100))

    # Convert to grayscale if it's a color image
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram
    hist = cv2.calcHist([image], [0], None, [12], [0, 256])

    # Define your musical notes
    NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

    # Map each bin to a musical note
    note_histogram = {}
    for i in range(len(NOTES)):
        note_histogram[NOTES[i]] = hist[i][0]

    # Print the histogram mapping
    for note, count in note_histogram.items():
        print(f'{note}: {count}')

    # Optionally, you can plot the histogram

    plt.bar(NOTES, [hist[i][0] for i in range(len(NOTES))])
    plt.xlabel('Notes')
    plt.ylabel('Bin Count')
    plt.title('Histogram of Image')
    plt.show()
