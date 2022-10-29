
import React, { useEffect, useState } from "react";
const Header = () => {
    const [url, setUrl] = useState(null)

    useEffect(() => {
        var url = window.location.href;
        if(url.includes('checkDominance')) {
            setUrl('checkDominance')
        }
        else {
            setUrl('')
        }
    })

    return (

        <div className='header'>
            {
              url === 'checkDominance'  ?
              <div className='text-header text-light'>
                <h2>
                  Blockchain Analytic Tool 
                </h2>
                </div>
              :
              <div className='text-header text-light'>
                <h2>
                  Compare Crypto 
                </h2>
                <button>
                  Blockchain analysis
                </button>
              </div> 
            }
            {/* <div className='text-header text-light'> Compare Crypto </div> */}
        </div>

    )
}

export default Header