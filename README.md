##💡 Inspiration

Are you a shutterbug, always trying to capture the world in photographs but forgetting to live in the moment? Do you find it difficult and unrewarding to take staged photos? Maybe you're someone who is often forced behind the lens in their social circles, being overlooked by the fact that you too deserve some nice pictures. 

Or perhaps you relate to @annaclendening...
![](https://static.demilked.com/wp-content/uploads/2019/07/5d2c220dbaa5b-photos-i-take-of-my-boyfriend-vs-photos-he-takes-2-5d284867244a5__700.jpg)

Our point is everyone has been a victim of a bad photo, of having the joy sucked out of photography. With pic-perfect, we aim to provide people with the best solution for effortlessly capturing their moments, ensuring that every shot is a keeper. Our robot will independently follow your movements and employ a pre-trained facial detection algorithm to keep your face in focus. Whenever you feel the moment is perfect, simply signal your approval with a thumbs-up gesture.

## 🔍 What it does

The pic-perfect is our friendly robot companion. It follows you wherever you go, using our backend facial detection model. With just a thumbs-up signal, it meticulously captures pictures of you and adds filters to create the most perfectly crafted portraits. These enhanced images are then displayed on a web app, with the intention of later storing them on a cloud service. The facial detection model is configured to position the robot at the proper angle and distance to center-align the person within the frame. Additionally, we utilize a hand gesture recognition algorithm to signal the robot when to begin capturing pictures.

## ⚙️ Our Tech Stack

![](https://imgur.com/a/OJ6PuLP.png)
- **Hardware**: The robot was built using the Viam Rover Kit and Raspberry Pi 4. We mounted our own webcam for better positioning of the camera. We had initially planned to 3D print a camera stand to achieve a better camera perspective. However, due to unforeseen challenges and time constraints, we were unable to continue with this concept.
- **Backend**: We utilized Python to establish connections with the Viam robot, access the necessary pre-trained models for our design, and augment our image processing capabilities. For recognizing hand gestures, we used MediaPipe and Tensorflow to recognize the "thumb's up" hand sign while facial recognition was done through openCV and a Haar Cascade Classifier.
- **Frontend**: We designed a simple and straightforward user interface with the primary goal of offering users an attractive platform for viewing their images.

## 🚧 Challenges we ran into

Building a hardware AI hack using advanced technologies like the Viam Rover kit was quite a blissful learning curve. We also underwent a very exhaustive testing process for both our machine learning algorithms to configure the robot appropriately for a smooth user experience.
- Hand Gesture Recognition: While using MediaPipe, TensorFlow, and OpenCV for hand gesture recognition, we encountered challenges related to model accuracy and real-world performance. Tuning the model and achieving consistent recognition accuracy was a significant task.
- Camera Mounting: Initially, we had planned to 3D print a camera stand to achieve a better camera perspective. However, due to unexpected difficulties and time constraints, we were unable to proceed with this plan, which impacted the quality of the camera positioning.

## ✔️ Accomplishments that we're proud of

- We are proud to have achieved a fully functional prototype, which has the potential to become a highly marketable product.
- Throughout the project, we gained valuable experience and developed new skills in hardware integration, computer vision, and user interface design. 
- A lot of firsts! We had never worked with the Viam Rover kit, and most of us had little experience with computer vision or photography.

## 📚 What we learned

Coming into this project, our team did not have as much experience with hardware-to-software interfacing, robotics, or AI/ML algorithms. Having a project combining all three elements was a challenge we wanted to take and learn from. Due to the nature of the project, we also needed to consider mechanical factors such as the positioning of the camera, the height of the mount, as well as determine suitable velocities that allow for the movement of the robot and polling of the live camera feed at the same time. Exercising technology like Python's OpenCV, and Tensorflow, and picking up a new skill with building robots with Viam, we were glad to have overcome the learning curve and come up with a final product to present.

## 🔭 What's next for ###

We plan on using servo motors to control the vertical aspect of clicking pictures more accurately. We also had discussions on further refining the robot by building Collison detection models and obstacle sensitivity intelligence.  Furthermore, we would like to have it speak to us about when the photo is being clicked, communicate with us its thoughts about positioning, and give encouraging feedback about it. Another possibility is uploading the images it takes into the user's personal Google Drive , or integrate it with a backend for use with different users.
