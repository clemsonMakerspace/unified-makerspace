import { useState, useEffect } from "react";
import Footer from "../components/Footer";
import { api_endpoint } from "../library/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { Link } from "react-router-dom";

const StudentQuizProgress = () => {
  const [searchUsername, setSearchUsername] = useState("");
  const [user, setUser] = useState<string | null>(null);
  const [quizzes, setQuizzes] = useState<
    {
      quiz_id: string;
      state: number;
    }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    // Construct the URL for your API endpoint
    setLoading(true);

    fetch(`${api_endpoint}/quiz/${searchUsername}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setQuizzes(data); // Assuming the response data is an array of quiz objects
        setUser(searchUsername);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  };

  useEffect(() => {}, []);

  return (
    <div
      className="container bg-primary p-5 rounded d-flex flex-column"
      style={{ minHeight: "30%", maxWidth: "95%" }}
    >
      <div className="mb-4 text-center">
        <h1 className="text-secondary fw-bold mb-1">Student Quiz Progress</h1>
      </div>
      <div className="d-flex flex-column align-items-center justify-content-center text-white">
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
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table table-bordered table-primary">
            <thead>
              <tr>
                <th className="text-center align-middle">Username</th>
                {quizzes.map((quiz, index) => (
                  <th className="text-center align-middle" key={index}>
                    {quiz.quiz_id}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="text-center align-middle">{user}</td>
                {quizzes.map((quiz, index) => (
                  <td
                    key={index}
                    className={
                      quiz.state === 1
                        ? "bg-success text-center align-middle" // Passed
                        : quiz.state === 0
                        ? "bg-danger text-center align-middle" // Failed
                        : "text-center align-middle" // Not Attempted
                    }
                  >
                    {quiz.state === 1
                      ? "Passed"
                      : quiz.state === 0
                      ? "Failed"
                      : "Not Attempted"}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
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

export default withAuthenticator(StudentQuizProgress, {
  hideSignUp: true,
});
