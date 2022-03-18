import { Routes, Route } from "react-router-dom";

import { locations } from "../library/constants";

import Registration from "./Registration";
import LocationSelection from "./LocationSelection";
import SignInSuccess from "./SignInSuccess";
import SignInError from "./SignInError";
import NotFoundPage from "./NotFoundPage";
import VisitForm from "../components/VisitForm";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<LocationSelection />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/success" element={<SignInSuccess />} />
      <Route path="/error" element={<SignInError />} />
      <Route path="*" element={<NotFoundPage />} />

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
  );
};

export default App;
