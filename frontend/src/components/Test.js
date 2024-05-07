import React, { useState, useEffect } from 'react'

const Test = () => {
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/test").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])

    return (
        <div>
            {(typeof data.test === 'undefined') ? (
                <p>Loading...</p>
            ) : (
                data.test.map((str, i) => (
                    <p key={i}> {str} </p>
                ))
            )}
        </div>
    )
}

export default Test