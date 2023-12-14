import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { signOut } from "aws-amplify/auth";

import PageCard from "../components/PageCard";
import { locations } from "../library/constants";

const LocationSelection = () => {
  useEffect(() => {
    async function handleSignOut() {
      try {
        await signOut({ global: true });
        // User is signed out, but stays on the same page
      } catch (error) {
        console.error("Error signing out: ", error);
      }
    }

    handleSignOut();
  }, []);

  return (
    <PageCard title="Makerspace Sign-In" subtitle="Location Selection">
      <div className="d-flex flex-wrap justify-content-center">
        {locations.map(({ slug, name }) => (
          <div className="m-2">
            <Link to={`/${slug}`} key={slug}>
              <button className="btn btn-secondary">{name}</button>
            </Link>
          </div>
        ))}
        <div className="w-100 d-flex justify-content-center mt-3">
          <Link to={"/admin"} key={"Admin"}>
            <button className="btn btn-pastel-purple">Admin</button>
          </Link>
        </div>
      </div>
    </PageCard>
  );
};

export default LocationSelection;
