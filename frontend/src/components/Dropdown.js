import React, {useState} from 'react';
import Select from 'react-select';
import courses from './Courses';
import axios from 'axios';
import "./Dropdown.css"

const options = courses.map(item => ({
  value: item[0],
  label: item[0],
  altLabel: item[1],
}));

const Dropdown = ({setSelectedCourse, setAbreviation}) => {
  const [courseName, setCourseName] = useState("none");

  const handleChange = (selectedOption) => {
    setCourseName(selectedOption)
    setAbreviation(selectedOption.label)

    if (selectedOption !== "none") {
      const apiUrl = 'http://127.0.0.1:8080/courses';
      const labelParam = selectedOption.label;

      axios.get(apiUrl, { params: { subject: labelParam } })
        .then(response => {
          setSelectedCourse(response.data)
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
      }
  }

  const clearSelection = () => {
      handleChange("none");
      setSelectedCourse({})
  };

  
  return (
    <>
      <div className="container">
      <div className="searchable-select">
        <Select
          options={options}
          onChange={handleChange}
          value={courseName}
          isSearchable
          styles={{
            control: (provided, state) => ({
              ...provided,
              width: 300,
              height: 20,
              borderBlockColor: "#13294B",
            }),
          }}
        />
      </div>
      <button className="clear-button" onClick={clearSelection}>
        X
      </button>
    </div>
      <h1 className='text'> {courseName !== "none" ? courseName.altLabel : ''}</h1>
    </>
  );
};

export default Dropdown;