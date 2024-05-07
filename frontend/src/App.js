import React, {useState} from 'react';
import Header from './components/Header';
// import Test from './components/Test';
import Dropdown from './components/Dropdown';
import CourseList from './components/CourseList';
import Instruction from './components/Instructions';


function App() {
  const [selectedCourse, setSelectedCourse] = useState({});
  const [abreviation, setAbreviation] = useState(String)

  return (
    <div>
      < Header/>
      < Instruction />
      {/* < Test /> */}
      < Dropdown setSelectedCourse={setSelectedCourse} setAbreviation={setAbreviation}/>
      <CourseList selectedCourse={selectedCourse} abreviation={abreviation} />
      
    </div>
  );
}

export default App;