
**Classroom Availability Project Proposal**

By Sam (hongyid3), Ziye Tang (ziyet3), Bernard Zhu (bwz2), Faraaz Baig (fbaig5)

**Pitch**

Students at UIUC often want to study in different classrooms in their spare time, but aren’t sure which rooms are available at which times. Classroom Availability will display what classrooms are occupied at selected times by which professors, all dependent on the user’s input and specification. Classroom Availability will also give students the ability to login, and input their own schedules for a convenient way to check the time and location of their classes.

**Functionality**

Basic functionality:

1. Users can see a list of courses going on for the current semester.
1. Users can search courses by keywords, day, and time, etc.
1. Users can check for detailed information for each course like the time, location, and instructor, etc. Advanced functionality:
1. Users can create an account and log in with the username and password.
1. Users can build their own schedules.

**Components**

- Backend: The backend will be developed mainly through Python and Flask framework. All of our members know Python, and two of us have worked with the Flask framework, which has a lot of user support and documentation. It also supports the MongoDB database, which we plan to use to store classroom and user information. We will use UIUC Rest API Resources in the backend. In short, the backend should receive HTTP requests from the frontend, perform the action requested, and send back responses (with data requested, maybe). Specifically, the backend has the following jobs:
- Receive HTTP request, tell the request type, and extract data from the request.
  - Done using Flask
- Get all courses’ information, filter courses based on the rule from the request (i.e. keywords, time, location, etc), and send back the response with the required courses’ data to the frontend.
  - This information will be received using UIUC’s Rest API, then filtered using our algorithms
- Store usernames and passwords when a new account is created.
  - We will use a MongoDB database to store this. Flask has built-in support for Mongodb (Flask-PyMongo)
- Store or update a user’s schedule when that user creates or updates the schedule in the frontend

■ We will use a MongoDB database to store this. Flask has built-in support for Mongodb (Flask-PyMongo)

We can test each functionality by printing out the result to the log and see if it looks reasonable. We can also use PyTest to test our output, matching it to a schedule/availability we have personally verified.

- Frontend: The frontend will be written in the Javascript programming language using the React framework. We chose Javascript because we can utilize the React framework and we are not too familiar with Typescript, but have built previous projects using React. There is a lot of documentation for React and it is one of the most user-supported frameworks with tutorials online. Some of the following functions we want our front end to do are:
- Search by class
- Search by building
- Search by instructor
- Search by room number
- Filter by time
- Show the list of classes that satisfy the conditions
- Personal profile card with classes they select

We chose to have a separate frontend and backend in order to build a full REST API that allows the communication between the frontend and backend. In this way, we can utilize a database that stores all user information and course information, and the frontend can send requests to pull out the backend filtered information. This also allows us to have two separate teams, where each team can work with a fully-updated version of the other team’s portion with the necessary functionality. Additionally, this allows us to work on components that don’t require data from the other side.

![](chart.png)

**Continuous Integration**

For testing we will use react testing library to test our react components, write unit tests for Flask using PyTest, Selenium for testing the frontend, and Github workflow to automate these tests.

We will first initialize our main branch by creating a basic react app and a basic flask app and from there we will individually create a branch on a feature we will work on. We will make a PR once we have finished the feature we worked on and make a different person review the PR and make the judgment on whether or not they should approve it or not.

**Schedule**



|**Week # (Date)**|**Tasks**|
| - | - |
|Week 1 (9/18-9/24)|1\.Set up Github repository containing frontend and backend code 2.Team members will familiarize themselves with tech stacks 3.Get authorization from UIUC to utilize the API|
|Week 2 (9/25-10/1)|<p>1. Create basic Flask backend API that sends simple JSON output to frontend</p><p>2. Create basic React frontend page that displays sample JSON</p>|
|Week 3 (10/2-10/8)|<p>1. Set up initial MongoDB database</p><p>2. Collect all data for class information, add to database, and setup for flask to use</p><p>3. Create the search bars and dropdown filter that will be used in frontend</p>|
|Week 4 (10/9-10/15)|<p>1. Setup search bars and filters to send an HTTP request to backend</p><p>2. Flask backend will receive the HTTP request and filter by the data given</p><p>3. Backend will send back a list of courses that is filtered by the given HTTP request</p>|
|Week 5 (10/16-10/22)|<p>1. React will display received information as a list</p><p>2. Frontend will be updated for multiple screen sizes, including desktop, mobile, and tablet</p><p>3. Backend will set up user information portion of the database</p>|
|Week 6 (10/23-10/29)|<p>1\.Create a login page for frontend</p><p>2\.Create tests for backend, check if correct classes are shown based on received requests</p>|
|Week 7 (10/30-11/5)|<p>1\.Work on advanced functions</p><p>2\.Login page will send an HTTP request to backend with user information</p><p>3\.Backend will receive the HTTP request and conduct task requested by request (GET,</p><p>POST, etc)</p>|
|Week 8 (11/6-11/12)|<p>1\.Create the calendar/schedule system</p><p>2\.Create requests to allow users to add classes to their schedule</p><p>3\.Backend will receive requests from frontend and add classes to user documents</p>|
|Week 9 (11/13-11/19)|1\.Create tests for all functions and user experience 2.Work on continuous integration|
|Week 10 (11/27-12/3)|1\.Verify tests work and check application is fully functional 2.Check all components work and no components are overlapped|

**Risks**

1. The UIUC course API requires authentication so we need to get that first and it could delay our whole project if we don’t do that on time. We also don’t know if they have a rate limit on the amount of requests we make so we have to be careful on that.
1. One potential risk is the room information might not be up to date since a class could possibly be moved informally to a different room but it won’t be updated in the system
1. We do not have data for rooms being occupied by office hours, research labs, office space for professors, events, and meetings.

**Teamwork**

All members in our team use VScode, so we decided not to implement docker. We will use Git to keep track of the changes every programmer made.

Since we are a team of four people, we will divide into two sub-teams of two people each: a frontend team (Sam and Faraaz), and a backend team (Tommy and Bernie). We went for this division because Tommy wants to do the backend, and Sam thinks the frontend is more interesting. Bernie and Faraaz can help on both teams since they are more experienced in web design. We will mainly communicate through Discord group chat. We plan to have an in-person meeting on Tuesday to check our progress and ask teammates for help if needed. Apart from that in-person meeting, we will schedule an online meeting with our mentor/TA to do weekly updates.
