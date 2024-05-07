import "./Instructions.css"

// Function to prompt the user for input and search for the class
function Instruction() {
  // Prompt the user to enter the course title
  return (
    // <body>
    //   <h1> Instruction: </h1>

    //   <p id = "SearchByClass"> Enter Course Title (e.g. BIOE for Bioengineering): </p>

    // </body>
    <body>

      
        <h1>Instruction for Checking Classroom Availability</h1>

        <ol>
          <li><strong>Select Class:</strong> Choose the Course Title (e.g. BIOE for Bioengineering) where you want to check classroom availability from the dropdown menu.</li>

          <li><strong>Choose Date and Time:</strong> Pick the date and time slot you are interested in using the calendar and time picker.</li>

          <li><strong>View Results:</strong> Check the list of available classrooms along with details such as room number, capacity, and any additional information by clicking on the course.</li>

          <li><strong>Make a Reservation (TODO):</strong> If you find a suitable classroom, follow the reservation link or button to book it for your use.</li>
        </ol>

        <p>Remember to respect the booking policies and ensure that the classrooms are used responsibly. Enjoy your study session!</p>
      

    </body>
  )
}

// Call the searchByClass function when the script is loaded
export default Instruction;