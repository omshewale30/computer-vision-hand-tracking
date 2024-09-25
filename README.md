
# Hand Tracking & Finger Counting ✋🤚

This project implements **real-time hand tracking** and **finger counting** using **OpenCV** and **Python**. The program captures video from the webcam, processes each frame to detect a hand, and counts the number of extended fingers using computer vision techniques.

## 🚀 Features

- **Real-time Hand Detection**: Uses a region of interest (ROI) to isolate the hand and improve detection performance.
- **Background Subtraction**: Implements adaptive background subtraction to focus on the hand against a stable background.
- **Finger Counting**: Counts the number of extended fingers by identifying the hand’s convex hull and analyzing its contours.
- **Visual Feedback**: Displays the processed video feed with the detected hand contours and the number of fingers extended.

## 🛠 Technologies Used

- **Python**: Primary programming language used for building the project.
- **OpenCV**: For video capture, image processing, and contour detection.
- **NumPy**: Used for mathematical operations and matrix manipulations.
- **scikit-learn**: Utilized for calculating Euclidean distances between points.

## 🖥 How It Works

1. **Video Capture**: The program captures live video from the webcam using OpenCV.
2. **Region of Interest (ROI)**: A specific area of the frame (where the hand is expected) is processed to reduce computational load.
3. **Background Subtraction**: An accumulated weighted background model is used to subtract the background from the hand.
4. **Thresholding**: The difference between the hand and the background is thresholded to create a binary image of the hand.
5. **Contour Detection**: The contours of the hand are detected and analyzed to identify the hand's convex hull.
6. **Finger Counting**: The program calculates the number of extended fingers based on the convex hull and its relationship to the center of the hand.

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/hand-tracking-finger-counting.git
   ```
   
2. **Install dependencies**:
   Make sure you have Python installed, and then install the required libraries:
   ```bash
   pip install numpy opencv-python scikit-learn
   ```

3. **Run the project**:
   ```bash
   python hand_tracking.py
   ```

## 📋 Usage

- Upon running the script, a webcam feed will open up. Place your hand in the **Region of Interest (ROI)**.
- The first 60 frames are used to **calibrate the background**, so please wait until the message "Please wait, getting the background" disappears.
- After background calibration, the program will start detecting your hand and counting the number of extended fingers.
- Press the **ESC** key to exit the program.

## 🚩 Key Functions

1. **`cal_accum_weight()`**:
   - Updates the background model using a weighted average over time.
   
2. **`segment()`**:
   - Subtracts the background from the current frame and detects the hand by finding the largest contour.

3. **`count_fingers()`**:
   - Identifies the convex hull of the hand and counts the number of extended fingers by analyzing the distances from the center of the hand to its contours.

## 🧠 How Finger Counting Works

- The hand’s **convex hull** is computed using the detected contours.
- **Extreme points** on the convex hull (top, bottom, left, and right) are used to determine the hand’s geometry.
- The number of fingers is estimated based on the convexity defects of the hand and whether a given contour point is part of the wrist or an extended finger.

## 🧪 Example Output

- The output window will display:
  - The webcam feed with the **hand contour** drawn in blue.
  - A **rectangle** marking the region of interest (ROI).
  - The number of fingers detected will be displayed at the top left of the screen.

## 🔮 Future Improvements

- **Improved accuracy**: Fine-tune the model to account for complex backgrounds and variable lighting conditions.
- **Gesture Recognition**: Extend the project to recognize different hand gestures, not just counting fingers.
- **Multi-hand Support**: Add support for detecting multiple hands in the frame.

## 👨‍💻 About the Developer

I'm **Om Shewale**, a computer vision enthusiast with a passion for creating projects that combine artificial intelligence and human-computer interaction. For more of my projects, visit my [portfolio](https://omshewale30.github.io/2d-portfolio/).

---

Feel free to contribute, open issues, or provide feedback!
