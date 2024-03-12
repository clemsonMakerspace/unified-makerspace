import Countdown from "react-countdown";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import PageCard from "../components/PageCard";
import QuizProgress from "../components/QuizProgress";

const SignInSuccess = () => {
  const navigate = useNavigate();
  let [searchParams] = useSearchParams();
  const next_page = (searchParams.get("next") as string) || "/";

  const renderer = () => (
    <PageCard title="Sign-In Successful">
      <h1>Your Safety Quiz Progress</h1>
      <QuizProgress />
      <Link to={next_page} className="btn btn-secondary">
        Continue
      </Link>
    </PageCard>
  );

  return (
    <Countdown
      date={Date.now() + 10000}
      renderer={renderer}
      onComplete={() => navigate(next_page)}
    />
  );
};

export default SignInSuccess;
