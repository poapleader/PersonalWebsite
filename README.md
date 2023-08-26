# David's Personal Website

This personal website project started as an exploration in Open AI tutorials and grew from there.  
I am in the process of updating and cleaning things up in prepartion for public hosting.  Created as an exploration in learning to code and establishing a shareable resource for AI related projects.  

 [quickstart tutorial](https://beta.openai.com/docs/quickstart). It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Check out the tutorial or follow the instructions below to get set up.

## Git Commands

1. Git status  ##Check the branch and status of local change
2. Git add . #adds changes 
3. Git commit -m "insert notes on updates"

## Updating the AWS Linux Webserver
1.  Open git Bash
2.  SSH into the EC2 Instance with command: ssh -i Downloads/MyLinuxWebServer.pem ec2-user@ec2-54-80-50-151.compute-1.amazonaws.com
3.  Is the server running?
   1. If so then run "ps aux | grep gunicorn" to find the process id and then kill -HUP [MASTER_PID] to update the process
   2. If not start the server with "gunicorn app:app --bind 0.0.0.0:8000"



## Website Diagram
```mermaid
   pie title Chocolate Cakes
      "Best" : 70
      "Worst" : 30
```

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd openai-quickstart-python
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! For the full context behind this example app, check out the [tutorial](https://beta.openai.com/docs/quickstart).
