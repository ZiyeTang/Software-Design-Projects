import React, { useState } from "react";
import "./CourseList.css"

export default function CourseList({ selectedCourse, abreviation }) {
  const [showSections, setShowSections] = useState(false);
  const [selectedCourseNumber, setSelectedCourseNumber] = useState(null);

  const toggleSections = (courseNumber) => {
    setSelectedCourseNumber(courseNumber);
    setShowSections(!showSections);
  };

  const closePopup = () => {
    setShowSections(false);
  };

  return (
    <div className="courseContainer">
      {Object.keys(selectedCourse).length === 0 ? (
        <></>
      ) : (
        Object.keys(selectedCourse).map((courseNumber) => (
          <div key={courseNumber} className="title">
            <div className="cn">{abreviation} {courseNumber}</div>
            <div onClick={() => toggleSections(courseNumber)}>{selectedCourse[courseNumber].title}</div>
          </div>
        ))
      )}
      {showSections && selectedCourse[selectedCourseNumber] && (
        <div className={`popup ${showSections ? "active" : ""}`}>
          <div className="popup-inner">
            <button id = "b1" onClick={closePopup}>X</button>
            <h2>Section Details for {selectedCourse[selectedCourseNumber].title}</h2>
            {Object.entries(selectedCourse[selectedCourseNumber].sections).map(([sectionNumber, section]) => (
              <div key={sectionNumber}>
                <h3>{section.sectionNumber}</h3>
                <p>
                  Start: {section.meetings.meeting.start || "N/A"}<br />
                  End: {section.meetings.meeting.end || "N/A"}<br />
                  Days of the Week: {section.meetings.meeting.daysOfTheWeek || "N/A"}<br />
                  Building Name: {section.meetings.meeting.buildingName || "N/A"}<br />
                  Room Number: {section.meetings.meeting.roomNumber || "N/A"}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
