import React from 'react';
import { Link } from 'react-router-dom';

class NotFoundPage extends React.Component{
    render(){
        return <div className="container bg-primary p-5 rounded" style={{height: "400px"}}>
            <p style={{textAlign:"center", color:"white", paddingBottom: "100px"}}>
                <div className="text-center mb-4">

                    <h1 className="text-secondary fw-bold mb-1 text-center" style={{fontSize:"350%"}}>ERROR 404 :(</h1>
                    <h2 className="text-white fw-bold mb-1 text-center">Page Not Found</h2>
                </div>
    
            </p>
            <div className="text-secondary fw-bold mb-4 text-center">
                <p style={{textAlign:"center"}}>
                    <Link to="/" style={{color:"white", paddingBottom: "50px", fontSize:"150%"}}>Go Back to Home Page</Link>
                </p>
            </div>

          </div>;
    }
}
export default NotFoundPage;