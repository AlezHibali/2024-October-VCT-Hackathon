# 2024-October-VCT-Hackathon

![Logo](assets/img/logo.png)

Welcome to the **2024-October-VCT-Hackathon** project repository! This project was developed during the October 2024 VCT (Valorant Champions Tour) hackathon. It focuses on building an innovative solution that interacts with Valorant-related data.

## Project Overview

This hackathon project provides access to Valorant information, including team data, match details, and player stats. The application allows users to query the latest updates in Valorant esports.

### Features:
- Fetches and displays Valorant team and match info.
- Provides detailed player statistics and info cards.
- Responsive user interface for easy navigation.

## Demo

You can access the live demo of the application here:

**[2024-October-VCT-Hackathon Demo](http://98.83.233.139:5001/)**

### Demo Video

Watch the demo video to see the application in action:

[link](https://www.youtube.com/watch?v=jdHyaDYFnfo)

### Screenshot Demo

Here are some screenshots of the application:

![Screenshot Home](assets/img/home.png)
![Screenshot Response](assets/img/response.png)
![Screenshot Team Planner and Eval](assets/img/eval.png)

## PDF Report

You can view our project report here:

[link](https://drive.google.com/file/d/18IluqYHskcRQp12X4Z4pNzl6kuzy7iNk/view?usp=sharing)


## Tech Stack

- **Backend**: Python, AWS Bedrock, AWS Lambda, beautifulsoup
- **Frontend**: HTML/CSS, JavaScript, Bootstrap
- **Database**: AWS S3
- **Deployment**: AWS Codedeploy, CodePipeline, EC2, Flask (Waitress as the WSGI server)

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/AlezHibali/2024-October-VCT-Hackathon.git
   ```

2. Navigate into the project directory:

   ```bash
   cd 2024-October-VCT-Hackathon
   ```

3. Create a virtual environment:

   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:

    - On macOS/Linux:

     ```bash
     source env/bin/activate
     ```
    - On Windows:

     ```bash
     env/Scripts/activate
     ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
6. Set the environmental variables for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

7. Run the application locally:

   ```bash
   python -m waitress --host=0.0.0.0 --port=5001 project.app:app
   ```

8. Access the application by opening `http://127.0.0.1:5001/` in your browser.

## Usage

Once the application is running, you can:
- Search for team info.
- Check out player stats and details.
- Build team of five players based on users' requirement.
- Evaluate a self-defined team of five players from different aspects.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

Steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Add your changes (`git add <changed files>`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License. 
