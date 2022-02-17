import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { SchemaOf } from "yup";

import { MakerspaceLocation } from "../library/types";
import PageCard from "./PageCard";

interface Schema {
  username: string;
}

const schema: SchemaOf<Schema> = yup
  .object({
    username: yup.string().required(),
  })
  .required();

interface Props {
  location: MakerspaceLocation;
  field_label: string;
  field_type: "text" | "email";
  user_type: string;
  onCancel: () => any;
}

const SignInForm = ({
  location,
  field_label,
  field_type,
  user_type,
  onCancel,
}: Props) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });
  const onSubmit = handleSubmit((data) => signin_user(data as Schema));

  const signin_user = (form_data: Schema) => {
    const body = {
      username: form_data.username,
      location: location.name,
    };

    setLoading(true);
    fetch("https://api.cumaker.space/visit", {
      method: "post",
      body: JSON.stringify(body),
    }).then((response) => {
      setLoading(false);
      if (response.ok) {
        navigate(`/success?next=/${location.slug}`);
      } else {
        navigate(`/error?next=/${location.slug}`);
      }
    });
  };

  if (loading)
    return <PageCard title="Makerspace Sign-In" subtitle="loading..." />;

  return (
    <PageCard title="Makerspace Sign-In" subtitle={`as ${user_type}`}>
      <form onSubmit={onSubmit}>
        <div className="form-group mb-3">
          <label htmlFor="username" className="form-label">
            {field_label}
          </label>
          <input
            id="username"
            type={field_type}
            className="form-control"
            placeholder={field_label}
            {...register("username")}
          />
          {errors.username && (
            <span className="form-text text-danger d-block">
              Please enter your {field_label.toLowerCase()}.
            </span>
          )}
        </div>
        <div className="d-flex justify-content-between">
          <button type="submit" className="btn btn-secondary mr-5">
            Sign In
          </button>
          <button className="btn btn-link text-light" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </PageCard>
  );
};

export default SignInForm;
