import React from "react";
import PageCard from "../components/PageCard";
import { useNavigate } from "react-router-dom";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { signOut } from "aws-amplify/auth";
import { fetchAuthSession } from "aws-amplify/auth";
import { api_endpoint } from "../library/constants";
import "@aws-amplify/ui-react/styles.css";

const Admin = () => {
  const navigate = useNavigate();

  const handleQuizzesClick = () => {
    navigate("/quiz_status");
  };

  const handleDashboardClick = async () => {
    // User is signed in, proceed with API request
    try {
      const session = await fetchAuthSession();
      if (session) {
        try {
          const response = await fetch(`${api_endpoint}/dashboard`, {
            method: "GET",
            headers: {
              Accept: "text/plain",
            },
          });

          if (response.ok) {
            alert("Generating Dashboard Preview...");
            const responseData = await response.text();
            if (responseData.includes("https")) {
              window.open(responseData, "_blank");
            } else {
              console.error("Error:", responseData, response.statusText);
            }
          } else {
            console.error("HTTP Error:", response.status, response.statusText);
          }
        } catch (error) {
          console.error("Request Error:", error);
        }
      }
    } catch (error) {
      alert("Authentication Required to Access Dashboards. Sign In");
    }
  };

  async function handleSignOut() {
    try {
      await signOut({ global: true });
      navigate("/");
    } catch (error) {
      console.log("Error signing out: ", error);
    }
  }

  return (
    <PageCard title="Admin Page" subtitle="Analytics">
      <div className="d-flex flex-wrap justify-content-center">
        <div className="m-3">
          <button
            className="btn btn-pastel-purple"
            onClick={handleQuizzesClick}
          >
            Quizzes
          </button>
        </div>
        <div className="m-3">
          {/* Dashboard API Call Button */}
          <button
            className="btn btn-pastel-purple"
            onClick={handleDashboardClick}
          >
            Dashboard
          </button>
        </div>
      </div>
      <div className="d-flex flex-wrap justify-content-center">
        {/* Log Out Button */}
        <div className="m-5">
          <button className="btn btn-pastel-orange" onClick={handleSignOut}>
            Back
          </button>
        </div>
      </div>
    </PageCard>
  );
};

export default withAuthenticator(Admin, {
  hideSignUp: true,
});
