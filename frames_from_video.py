import numpy as np
import cv2
import glob

def frames_from_video(video_frames_dir):

    fps = []
    for file in glob.glob(video_frames_dir + "*.png"):
        frame = cv2.imread(file)
        fps.append(frame)

    height, width, layers = fps[0].shape
    fps = np.array(fps)
    
    print(fps.shape)

    return height, width, layers

def main():

    video_frames_dir = '/Users/varshiniprakash/Downloads/cosmic_reef-3840x2160-0745-1143/'
    h, w, l = frames_from_video(video_frames_dir)
    print(h,w,l)

if __name__ == "__main__":
    main()