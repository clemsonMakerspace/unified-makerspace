import React from 'react';
import { Link } from 'react-router-dom';

class NotFoundPage extends React.Component{
    render(){
        return <div>
            <p style={{textAlign:"center", color:"white", paddingBottom: "100px"}}>
                <h1 style={{fontSize:"350%"}}>Error 404</h1>
                <h2>Page Not Found</h2>    
            </p>
            <p style={{textAlign:"center"}}>
                <Link to="/" style={{color:"white", paddingBottom: "100px", fontSize:"200%"}}>Go Back to Home Page</Link>
            </p>
            
          </div>;
    }
}
export default NotFoundPage;