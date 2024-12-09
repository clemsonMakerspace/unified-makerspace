import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { signOut } from "aws-amplify/auth";

import PageCard from "../components/PageCard";
import { locations } from "../library/constants";

const Home = () => {
  return (
    <PageCard
      title="Welcome to the Makerspace!"
      subtitle="How can we help you today?"
    >
      <div className="d-flex flex-wrap justify-content-center">
        <div className="m-2">
          <a href="https://tigertraining.clemson.edu/">
            <button className="btn btn-secondary me-2">Tiger Training</button>
          </a>
          <Link to={"/register"}>
            <button className="btn btn-secondary me-2">Register</button>
          </Link>
          <Link to={"/equipment_form"}>
            <button className="btn btn-secondary">Equipment Form</button>
          </Link>
        </div>
        <div className="w-100 d-flex justify-content-center mt-3">
          <Link to={"/admin"}>
            <button className="btn btn-pastel-purple">Admin</button>
          </Link>
        </div>
      </div>
    </PageCard>
  );
};

export default Home;
