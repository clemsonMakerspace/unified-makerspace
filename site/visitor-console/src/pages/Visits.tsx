import { useState, useEffect } from "react";
import Footer from "../components/Footer";
import { api_endpoint } from "../library/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { Link } from "react-router-dom";

// Define the type for a visit
interface Visit {
  location: string;
  user_id: string;
  timestamp: string;
}

interface VisitLog extends Visit {
  _ignore?: string;
}

const Visits = () => {
  const [searchUsername, setSearchUsername] = useState("");
  const [visits, setVisits] = useState<Visit[]>([]);
  const [locationFilter, setLocationFilter] = useState("All");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVisits = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${api_endpoint}/visits?limit=50`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-Api-Key": import.meta.env.VITE_BACKEND_KEY,
          },
        });

        if (!response.ok) {
          throw new Error(`Error fetching visits: ${response.statusText}`);
        }

        const data = await response.json();
        console.log(`Data received:\n${JSON.stringify(data, null, 2)}`);
        const logs: VisitLog[] = Array.isArray(data.visits) ? data.visits : [];

        setVisits(logs);
      } catch (error: any) {
        console.error("Fetch error:", error);
        setError(error.message || "An unknown error occurred.");
        setVisits([]);
      } finally {
        setLoading(false);
      }
    };

    fetchVisits();
  }, []);

  const appendLogs = (logs: VisitLog[]) => {
    setVisits((prevLogs) => {
      // Create a Map to ensure unique logs based on user_id and timestamp
      const logMap = new Map();

      // Add previous logs to the Map
      prevLogs.forEach((log) => {
        const key = `${log.user_id}-${log.timestamp}`; // Composite key
        logMap.set(key, log); // Add the log to the Map
      });

      // Add new logs from the fetched data to the Map
      logs.forEach((log) => {
        const key = `${log.user_id}-${log.timestamp}`; // Composite key
        logMap.set(key, log); // Add the log to the Map
      });

      // Convert the Map back to an array and return it
      return Array.from(logMap.values());
    });
  };

  const handleSearch = async (user_id: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${api_endpoint}/visits/${user_id}?limit=50`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-Api-Key": import.meta.env.VITE_BACKEND_KEY,
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Error fetching visits for ${user_id}: ${response.statusText}`
        );
      }

      const data = await response.json();
      console.log(`Data received:\n${JSON.stringify(data, null, 2)}`);
      const logs: VisitLog[] = Array.isArray(data.visits) ? data.visits : [];

      appendLogs(logs);
    } catch (error) {
      console.error("Error fetching visits:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${api_endpoint}/visits?limit=50`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-Api-Key": import.meta.env.VITE_BACKEND_KEY,
        },
      });

      if (!response.ok) {
        throw new Error(`Error fetching visits: ${response.statusText}`);
      }

      const data = await response.json();
      console.log(`Data received:\n${JSON.stringify(data, null, 2)}`);
      const logs: VisitLog[] = Array.isArray(data.visits) ? data.visits : [];

      appendLogs(logs);
    } catch (error) {
      console.error("Error fetching visits:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredVisits = visits.filter(
    (visit) =>
      (locationFilter === "All" || visit.location === locationFilter) &&
      visit.user_id.toLowerCase().includes(searchUsername.toLowerCase())
  );

  return (
    <div
      className="container bg-primary p-5 rounded d-flex flex-column"
      style={{ minHeight: "30%", maxWidth: "95%" }}
    >
      <div className="mb-4 text-center">
        <h1 className="text-secondary fw-bold mb-1">Makerspace Visits</h1>
      </div>
      <div className="d-flex flex-column align-items-center justify-content-center text-white">
        <div className="d-flex align-items-end justify-content-between w-100">
          <div className="d-flex mb-3">
            <button
              className={`btn btn-secondary me-2 ${
                locationFilter === "All" ? "active" : ""
              }`}
              onClick={() => setLocationFilter("All")}
            >
              All
            </button>
            <button
              className={`btn btn-secondary me-2 ${
                locationFilter === "Watt" ? "active" : ""
              }`}
              onClick={() => setLocationFilter("Watt")}
            >
              Watt
            </button>
            <button
              className={`btn btn-secondary me-2 ${
                locationFilter === "Cooper" ? "active" : ""
              }`}
              onClick={() => setLocationFilter("Cooper")}
            >
              Cooper
            </button>
            <button
              className={`btn btn-secondary me-2 ${
                locationFilter === "CU ICAR" ? "active" : ""
              }`}
              onClick={() => setLocationFilter("CU ICAR")}
            >
              CU ICAR
            </button>
            <button
              onClick={() => handleRefresh()}
              className="btn btn-secondary"
              type="button"
            >
              Refresh Visits
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
                onClick={() => handleSearch(searchUsername)}
                className="btn btn-secondary"
                type="button"
              >
                Search
              </button>
            </div>
          </div>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table table-bordered table-primary">
            <thead>
              <tr>
                <th className="text-center align-middle">Location</th>
                <th className="text-center align-middle">Username</th>
                <th className="text-center align-middle">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {filteredVisits.map((visit, index) => (
                <tr key={index}>
                  <td className="text-center align-middle">{visit.location}</td>
                  <td className="text-center align-middle">{visit.user_id}</td>
                  <td className="text-center align-middle">
                    {new Date(visit.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <div className="d-flex flex-wrap justify-content-center">
        <div className="m-5">
          <Link to={"/admin"}>
            <button className="btn btn-pastel-purple">Back</button>
          </Link>
        </div>
      </div>
      <div className="flex-grow-1"></div>
      <Footer />
    </div>
  );
};

export default withAuthenticator(Visits, {
  hideSignUp: true,
});
