import numpy as np
from PIL import Image
from pydub import AudioSegment
from pydub.generators import Sine

def main():
    # Load the NASA space image
    image = Image.open("/Users/gautham/Downloads/nasa_space_image.jpg")

    # Convert the image to grayscale
    image = image.convert("L")
    # Resize the image to a desired size (e.g., 100x100)
    new_size = (100, 100)
    image = image.resize(new_size)

    # Extract pixel data as a NumPy array
    pixel_data = np.array(image)

    # Normalize pixel values to the range [0, 1]
    normalized_pixel_data = pixel_data / 255.0

    # Define audio parameters
    sample_rate = 44100  # Sample rate in Hz
    duration = 0.1  # Duration of each audio segment in seconds
    amplitude = 0.5  # Amplitude of the audio

    # Create an empty audio segment
    audio = AudioSegment.empty()

    # Iterate through pixel data and create audio samples
    total = normalized_pixel_data.shape[0] * normalized_pixel_data.shape[1]
    count = 0
    for row in normalized_pixel_data:
        for pixel_value in row:
            count += 1
            # Map pixel value to frequency (adjust as needed)
            frequency = 100 + pixel_value * 1000  # Example mapping

            # Create a sine wave for this pixel value
            sine_wave = Sine(frequency).to_audio_segment(duration=duration * 1000)
            sine_wave = sine_wave - amplitude

            # Add this segment to the audio
            audio += sine_wave
            print(f"{count}/{total}")
    print("Done")
    # Export the audio to a file
    audio.export("nasa_space_audio.wav", format="wav")

if __name__ == "__main__":
    main()