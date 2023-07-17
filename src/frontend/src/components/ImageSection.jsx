import React from 'react';

const ImageSection = ({OpenData, Inps, PortalOpenData}) => {
  return (
    <div class="search-btns">
            <h2>Le nostre fonti dati</h2>
            <a href="https://bdap-opendata.rgs.mef.gov.it/">
              <img src={OpenData} alt="Gov" />
            </a>
            <a href="https://www.inps.it/it/it/dati-e-bilanci/open-data.html">
              <img src={Inps} alt="Inps"/>
            </a>
            <a href="http://www.datiopen.it/">
              <img src={PortalOpenData} alt="Portal"/>
            </a>
    </div>
  );
};

export default ImageSection;
