import { Routes, Route } from "react-router-dom";

import { locations } from "../library/constants";

import Registration from "./Registration";
import LocationSelection from "./LocationSelection";
import SignInSuccess from "./SignInSuccess";
import SignIn from "./SignIn";
import SignInError from "./SignInError";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<LocationSelection />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/success" element={<SignInSuccess />} />
      <Route path="/error" element={<SignInError />} />

      {/* makerspace specific routes */}
      {locations.map((location) => {
        const { slug } = location;
        return (
          <Route
            path={`/${slug}`}
            key={slug}
            element={<SignIn location={location} />}
          />
        );
      })}
    </Routes>
  );
};

export default App;
