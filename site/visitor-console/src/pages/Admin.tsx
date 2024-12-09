import React from "react";
import PageCard from "../components/PageCard";
import { Link } from "react-router-dom";
import { api_endpoint } from "../library/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { signOut } from "aws-amplify/auth";
import { fetchAuthSession } from "aws-amplify/auth";
import "@aws-amplify/ui-react/styles.css";

const Admin = () => {
  return (
    <PageCard title="Admin Page" subtitle="Dashboards">
      <div className="d-flex flex-wrap justify-content-center">
        <a href="https://www.google.com">
          <button className="btn btn-secondary me-2">Sign-In</button>
        </a>
        <Link to={"/qualifications"}>
          <button className="btn btn-secondary me-2">Qualifications</button>
        </Link>
        <Link to={"/visits"}>
          <button className="btn btn-secondary me-2">Visits</button>
        </Link>
        <Link to={"/equipment_usage"}>
          <button className="btn btn-secondary">Equipment Logs</button>
        </Link>
      </div>
      <div className="d-flex flex-wrap justify-content-center">
        <div className="m-5">
          <Link to={"/"}>
            <button className="btn btn-pastel-purple">Back</button>
          </Link>
        </div>
      </div>
    </PageCard>
  );
};

export default Admin;

/*
export default withAuthenticator(Admin, {
  hideSignUp: true,
});
*/
