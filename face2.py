import cv2
import face_recognition
import numpy as np
import os
import time

def load_reference_image(image_path):
    """
    Load the reference image and encode the face in it.
    
    Args:
        image_path (str): Path to the reference image
    
    Returns:
        tuple: (reference_image, face_encoding) or (None, None) if no face found
    """
    if not os.path.exists(image_path):
        print(f"Error: Reference image not found at {image_path}")
        return None, None
    
    # Load the image
    reference_image = face_recognition.load_image_file(image_path)
    
    # Find face locations in the image
    face_locations = face_recognition.face_locations(reference_image)
    
    if not face_locations:
        print("Error: No face found in the reference image")
        return reference_image, None
    
    # Get the encoding of the first face found
    face_encoding = face_recognition.face_encodings(reference_image, face_locations)[0]
    
    return reference_image, face_encoding

def verify_face(reference_encoding, tolerance=0.7):
    """
    Use webcam to verify if the current person matches the reference face.
    
    Args:
        reference_encoding: Face encoding of the reference image
        tolerance (float): Matching tolerance (lower is stricter)
    """
    if reference_encoding is None:
        print("Cannot verify without a reference face encoding")
        return
    
    # Initialize webcam
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("\nStarting face verification...")
    print("Press 'q' to quit")
    print("Press 'v' to verify current face")
    
    process_this_frame = True
    verification_requested = False
    
    while True:
        # Grab a single frame from the webcam
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read from webcam")
            break
        
        # Only process every other frame to save time
        if process_this_frame:
            # Resize frame to 1/4 size for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert the image from BGR (OpenCV uses) to RGB (face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            if verification_requested:
                try:
                    # Find all faces in the current frame
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    
                    if face_locations:
                        # Get face encodings for faces in the frame - with error handling
                        face_encodings = []
                        for face_location in face_locations:
                            try:
                                # Process one face at a time
                                top, right, bottom, left = face_location
                                face_image = rgb_small_frame[top:bottom, left:right]
                                encodings = face_recognition.face_encodings(face_image)
                                if encodings:
                                    face_encodings.append(encodings[0])
                            except Exception as e:
                                print(f"Error encoding face: {e}")
                                continue
                        
                        # Initialize verification results
                        matches = []
                        face_distances = []
                        
                        # Check each face found in the webcam frame
                        for face_encoding in face_encodings:
                            # Compare with reference face
                            match = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=tolerance)[0]
                            distance = face_recognition.face_distance([reference_encoding], face_encoding)[0]
                            
                            matches.append(match)
                            face_distances.append(distance)
                        
                        # Display results
                        print("\n--- Verification Results ---")
                        if True in matches:
                            match_idx = matches.index(True)
                            confidence = (1 - face_distances[match_idx]) * 100
                            print(f"✅ Match found! Confidence: {confidence:.2f}%")
                        else:
                            if face_distances:
                                best_distance = min(face_distances)
                                confidence = (1 - best_distance) * 100
                                print(f"❌ No match found. Best confidence: {confidence:.2f}%")
                            else:
                                print("❌ No match found.")
                        
                        # Draw boxes for visualization
                        for (top, right, bottom, left), match in zip(face_locations, matches):
                            # Scale back up face locations since we resized to 1/4
                            top *= 4
                            right *= 4
                            bottom *= 4
                            left *= 4
                            
                            # Draw a box around the face
                            color = (0, 255, 0) if match else (0, 0, 255)  # Green for match, red for no match
                            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                            
                            # Display match status
                            status = "MATCH" if match else "NO MATCH"
                            cv2.putText(frame, status, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
                    else:
                        print("No faces detected in the current frame.")
                
                except Exception as e:
                    print(f"Error in face processing: {e}")
                
                verification_requested = False
        
        process_this_frame = not process_this_frame
        
        # Display the resulting image
        cv2.imshow('Face Verification', frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        # If 'q' is pressed, exit the loop
        if key == ord('q'):
            break
        # If 'v' is pressed, verify the current face
        elif key == ord('v'):
            verification_requested = True
    
    # Release the webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()
    
def main():
    print("=== Face Verification System ===")
    
    # Get reference image path from user
    reference_image_path = '/Users/harshita/vs code/Hackerz3.0/image4.jpeg'
    
    # Load reference image and get face encoding
    _, reference_encoding = load_reference_image(reference_image_path)
    
    if reference_encoding is not None:
        # Start the verification process
        verify_face(reference_encoding)
    else:
        print("Verification cannot proceed without a valid reference image with a face.")

if __name__ == "__main__":
    main()