import { useState } from "react";
import Footer from "../components/Footer";
import { api_endpoint } from "../library/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { Link } from "react-router-dom";

const Qualifications = () => {
  const [searchUsername, setSearchUsername] = useState("");
  const [qualifications, setQualifications] = useState<{
    last_updated: string;
    trainings: { name: string; completion_status: string }[];
    waivers: { name: string; completion_status: string }[];
    miscellaneous: { name: string; completion_status: string }[];
  } | null>(null);

  const [loading, setLoading] = useState(false);
  const [userNotFound, setUserNotFound] = useState(false);
  const [refreshStatus, setRefreshStatus] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!searchUsername.trim()) {
      alert("Please enter a username.");
      return;
    }

    setLoading(true);
    setUserNotFound(false);
    setQualifications(null);

    try {
      const response = await fetch(
        `${api_endpoint}/qualifications/${searchUsername}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": "bY2BQ0boppPn3rnfSjsh68kgQKpBYMq4eP5uWLvd",
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          setUserNotFound(true);
        } else {
          throw new Error(
            `Error fetching qualifications: ${response.statusText}`
          );
        }
      } else {
        const data = await response.json();
        setQualifications(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setRefreshStatus(null);

    try {
      const response = await fetch(`${api_endpoint}/tiger_training`, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Error refreshing data: ${response.statusText}`);
      }

      setRefreshStatus("Data refreshed successfully.");
    } catch (error: any) {
      console.error("Error refreshing data:", error);
      setRefreshStatus("Failed to refresh data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="container bg-primary p-5 rounded d-flex flex-column"
      style={{ minHeight: "30%", maxWidth: "95%" }}
    >
      <div className="mb-4 text-center">
        <h1 className="text-secondary fw-bold mb-1">Student Qualifications</h1>
      </div>
      <div className="d-flex flex-column align-items-center justify-content-center text-white">
        <div className="d-flex align-items-end justify-content-between w-100">
          <div className="mb-3">
            <button
              className="btn btn-secondary"
              type="button"
              onClick={handleRefresh}
            >
              Refresh
            </button>
          </div>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">
              Search by Username:
            </label>
            <div className="input-group">
              <input
                type="text"
                className="form-control"
                id="username"
                value={searchUsername}
                onChange={(e) => setSearchUsername(e.target.value)}
              />
              <button
                className="btn btn-secondary"
                type="button"
                onClick={handleSearch}
              >
                Search
              </button>
            </div>
          </div>
        </div>
        {loading ? (
          <p>Loading...</p>
        ) : qualifications ? (
          <table className="table table-bordered table-primary">
            <thead>
              <tr>
                <th className="text-center align-middle">Type</th>
                <th className="text-center align-middle">Name</th>
                <th className="text-center align-middle">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                ...qualifications.trainings.map((training) => ({
                  ...training,
                  type: "Training",
                })),
                ...qualifications.waivers.map((waiver) => ({
                  ...waiver,
                  type: "Waiver",
                })),
                ...qualifications.miscellaneous.map((misc) => ({
                  ...misc,
                  type: "Miscellaneous",
                })),
              ].map((item, index) => (
                <tr key={index}>
                  <td className="text-center align-middle">{item.type}</td>
                  <td className="text-center align-middle">{item.name}</td>
                  <td className="text-center align-middle">
                    {item.completion_status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : userNotFound ? (
          <p>No qualifications found for the specified user.</p>
        ) : (
          <p>Search for a specific user to see their qualifications</p>
        )}
      </div>
      <div className="d-flex flex-wrap justify-content-center">
        <div className="m-5">
          <Link to={"/admin"} key={"Admin"}>
            <button className="btn btn-pastel-purple">Back</button>
          </Link>
        </div>
      </div>
      <div className="flex-grow-1"></div>
      <Footer />
    </div>
  );
};

export default Qualifications;

/*
export default withAuthenticator(Qualifications, {
  hideSignUp: true,
});
*/
