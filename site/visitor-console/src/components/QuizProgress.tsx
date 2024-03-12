import { useState, useEffect } from "react";
import { api_endpoint } from "../library/constants";
import { useSearchParams } from "react-router-dom";

const QuizProgress = () => {
  const [quizzes, setQuizzes] = useState<
    {
      quiz_id: string;
      state: number;
    }[]
  >([]);
  const [loading, setLoading] = useState(false);

  let [searchParams] = useSearchParams();
  const username = (searchParams.get("username") as string) || "/";

  useEffect(() => {
    fetch(`${api_endpoint}/quiz/${username}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setQuizzes(data); // Assuming the response data is an array of quiz objects
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  //This cuts the quiz progress into lengthOfTable quiz long objects so that the tables fit on the pagecard
  const renderTables = () => {
    const lengthOfTable = 4;

    const numQuizzes = quizzes.length;
    const numTables = Math.ceil(numQuizzes / lengthOfTable);

    return Array.from({ length: numTables }, (_, index) => {
      const startIdx = index * lengthOfTable;
      const endIdx = Math.min((index + 1) * lengthOfTable, numQuizzes);
      const tableQuizzes = quizzes.slice(startIdx, endIdx);

      return (
        <div key={index}>
          <table className="table table-bordered table-primary">
            <thead>
              <tr>
                {tableQuizzes.map((quiz, idx) => (
                  <th className="text-center align-middle" key={idx}>
                    {quiz.quiz_id}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {tableQuizzes.map((quiz, idx) => (
                  <td
                    key={idx}
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
        </div>
      );
    });
  };

  return <div>{loading ? <p>Loading...</p> : renderTables()}</div>;
};

export default QuizProgress;
