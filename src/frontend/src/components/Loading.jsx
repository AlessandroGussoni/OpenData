import React from 'react'
import "./loading.scss"

const NumberReviews = ({LoadingFlag}) => {
  return (
    <div>
      {LoadingFlag && (
        <div className="container">
          <div className="📦" key={1}></div>
          <div className="📦" key={2}></div>
          <div className="📦" key={3}></div>
          <div className="📦" key={4}></div>
          <div className="📦" key={5}></div>
        </div>
      )}
    </div>
  )
}

export default NumberReviews