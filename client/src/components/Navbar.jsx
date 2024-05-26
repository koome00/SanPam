import React from "react"
import logo  from "../assets/Icons/sampam3.png"
import "./Navbar.css"
function Navbar() {
    return (
            <nav>
                <ul>
                    <li><img src={logo} ></img></li>
                    <li><a href="#">HOME</a></li>
                    <li><a href="#">WHO WE ARE</a></li>
                    <li><a href="#">SERVICES</a></li>
                    <li><a href="#">PROJECTS</a></li>
                    <li><a href="#">CONTACT US</a></li>
                    <li id="quote-button"><a href="#">GET A QUOTE</a></li>
                </ul>
            </nav>
    );
}
export default Navbar