import React from 'react'
import at1 from "../assets/Icons/at1.png"
import clock1 from "../assets/Icons/clock1.png"
import facebook1 from "../assets/Icons/facebook1.png"
import linkedin1 from "../assets/Icons/linkedin1.png"
import phone1 from "../assets/Icons/phone1.png"
import pintrest1 from "../assets/Icons/pintrest1.png"
import twitter1 from "../assets/Icons/twitter1.png"
import "./Socials.css"

function Socials() {
    return(
        <>
            <div>
                <div className="contacts-one">
                    <h3><img src={phone1}></img>+(254) 712345678</h3>
                    <h3><img src={at1} ></img>sampam@gmail.com</h3>
                    <h3><img src={clock1}></img>Mon - Sat 8:00 - 17:00, Sunday - Closed</h3>
                </div>
                <div className='contacts-two'>
                    <img src={linkedin1} ></img>
                    <img src={twitter1} ></img>
                    <img src={facebook1}></img>
                    <img src={pintrest1}></img>
                </div>
            </div>
         </>
    );
}

export default Socials