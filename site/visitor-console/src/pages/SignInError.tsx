import Countdown from "react-countdown";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import PageCard from "../components/PageCard";

const SignInSuccess = () => {
  const navigate = useNavigate();
  let [searchParams] = useSearchParams();
  const next_page = (searchParams.get("next") as string) || "/";

  const renderer = () => (
    <PageCard title="Sign-In Failed" subtitle="there was a problem signing in">
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
