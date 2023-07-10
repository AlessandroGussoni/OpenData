import React from 'react';

const ImageSection = () => {
  return (
    <section id="image-section" className="image-section">
      <h2 className="section-title">Images</h2>
      <div className="image-grid">
        <img src="image1.jpg" alt="OpenData 1" />
        <img src="image2.jpg" alt="OpenData 2" />
        <img src="image3.jpg" alt="OpenData 3" />
        <img src="image4.jpg" alt="OpenData 4" />
        <img src="image5.jpg" alt="OpenData 5" />
      </div>
    </section>
  );
};

export default ImageSection;
