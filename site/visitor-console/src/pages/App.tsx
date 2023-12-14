import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Amplify } from "aws-amplify";
import { locations } from "../library/constants";
import { getAmplifyConfig } from "../config/getAmplifyConfig";
import React, { useEffect } from "react";

import LocationSelection from "./LocationSelection";
import Registration from "./Registration";
import SignInSuccess from "./SignInSuccess";
import SignInError from "./SignInError";
import NotFoundPage from "./NotFoundPage";
import VisitForm from "../components/VisitForm";
import Admin from "./Admin";
import Quizzes from "./QuizStatus";

const App = () => {
  useEffect(() => {
    const config = getAmplifyConfig();
    Amplify.configure({
      Auth: {
        Cognito: {
          userPoolId: config.userPoolId,
          userPoolClientId: config.userPoolClientId,
        },
      },
    });
  }, []);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LocationSelection />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/success" element={<SignInSuccess />} />
        <Route path="/error" element={<SignInError />} />
        <Route path="*" element={<NotFoundPage />} />

        <Route path="/admin" element={<Admin />} />
        <Route path="/quiz_status" element={<Quizzes />} />

        {/* makerspace specific routes */}
        {locations.map((location) => {
          const { slug } = location;
          return (
            <Route
              path={`/${slug}`}
              key={slug}
              element={<VisitForm location={location} />}
            />
          );
        })}
      </Routes>
    </Router>
  );
};

export default App;
