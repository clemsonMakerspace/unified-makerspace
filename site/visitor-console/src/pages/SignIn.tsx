import { useState } from "react";
import PageCard from "../components/PageCard";
import { MakerspaceLocation } from "../library/types";
import SignInForm from "../components/SignInForm";

interface Props {
  location: MakerspaceLocation;
}

export enum SignInType {
  CHOOSING,
  CLEMSON,
  GUEST,
}

const SignIn = ({ location }: Props) => {
  const [state, setState] = useState<SignInType>(SignInType.CHOOSING);

  const cancel = () => setState(SignInType.CHOOSING);

  if (state === SignInType.CLEMSON)
    return (
      <SignInForm
        user_type="Clemson Student"
        field_label="Username"
        field_type="text"
        location={location}
        onCancel={cancel}
      />
    );
  if (state === SignInType.GUEST)
    return (
      <SignInForm
        user_type="Guest Visitor"
        field_label="Email"
        field_type="email"
        location={location}
        onCancel={cancel}
      />
    );

  return (
    <PageCard title="Makerspace Sign-In" subtitle={`at ${location.name}`}>
      <div>
        <button
          className="btn-lg btn-secondary mb-3 d-block"
          style={{ width: "250px" }}
          onClick={() => setState(SignInType.CLEMSON)}
        >
          Clemson User
        </button>

        <button
          className="btn-lg btn-accent d-block"
          style={{ width: "250px" }}
          onClick={() => setState(SignInType.GUEST)}
        >
          Guest User
        </button>
      </div>
    </PageCard>
  );
};

export default SignIn;
