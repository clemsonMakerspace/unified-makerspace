import React from "react";
import { FormStageProps } from "../types";

import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { SchemaOf } from "yup";
import PageCard from "../../PageCard";

interface Schema {
  username: string;
}

const schema: SchemaOf<Schema> = yup
  .object({
    username: yup.string().required(),
  })
  .required();

const UsernameStage = ({ data, finalize, location, reset }: FormStageProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });
  const onSubmit = handleSubmit((data) => finalize_stage(data as Schema));

  let user_type: string;
  let field_label: string;
  let field_type: "text" | "email";

  if (data.type === "student") {
    user_type = "Clemson Student";
    field_label = "Username";
    field_type = "text";
  } else {
    user_type = "Guest Visitor";
    field_label = "Email";
    field_type = "email";
  }

  const finalize_stage = ({ username }: Schema) => {
    finalize({ ...data, username });
  };

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
          <button className="btn btn-link text-light" onClick={reset}>
            Cancel
          </button>
        </div>
      </form>
    </PageCard>
  );
};

export default UsernameStage;
