import { useState } from "react";
import { Link } from "react-router-dom";

import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { SchemaOf } from "yup";
import * as yup from "yup";

import {
  genders,
  majors,
  minors,
  api_endpoint,
  format_date,
  gradyears,
  gradsemesters,
  userPosition,
  class_list,
} from "../library/constants";
import FormSelect from "../components/FormSelect";
import FormMultiselect from "../components/FormMultiselect";
import PageCard from "../components/PageCard";

interface Schema {
  username: string;
  gender: string;
  birthday: Date;
  position: string;
  gradsemester?: string;
  gradyear?: string;
  class?: string;
  major?: string[];
  minor?: string[];
}

const schema: SchemaOf<Schema> = yup
  .object({
    username: yup.string().required(),
    gender: yup.string().required(),
    birthday: yup.date().required(),
    position: yup.string().required(),
    gradsemester: yup.string(),
    gradyear: yup.string(),
    class: yup.string(),
    major: yup.array().when("position", {
      is: (value: string) => value === "Undergraduate" || value === "Graduate",
      then: yup.array().required(),
    }),
    minor: yup.array(),
  })
  .required();

const Registration = () => {
  const [registered, setRegistered] = useState(false);
  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,

    // ! future, add validation display
    // formState: { errors },
  } = useForm({
    // validates the form with the above schema
    resolver: yupResolver(schema),
  });

  const onSubmit = handleSubmit((data) => register_user(data as Schema));

  const register_user = async (form_data: Schema): Promise<void> => {
    const body = {
      user_id: form_data.username,
      gender: form_data.gender,
      birthday: format_date(form_data.birthday),
      university_status: form_data.position,
      undergraduate_class: form_data.class,
      GradSemester: form_data.gradsemester,
      GradYear: form_data.gradyear,
      major: form_data.major,
      minor: form_data.minor,
    };

    try {
      const response = await fetch(`${api_endpoint}/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        console.log("User registered successfully.");
        setRegistered(true);
      } else {
        const errorData = await response.json();
        console.error("Registration failed:", errorData);
      }
    } catch (error) {
      console.error("Error during registration:", error);
    }
  };

  if (registered) return <PageCard title="Registration Successful" />;

  let userRole = watch("position");

  return (
    <PageCard
      title="Makerspace Registration"
      subtitle="Please Fill in Registration Information"
    >
      <div className="d-flex flex-column align-items-center text-light">
        <form className="row" onSubmit={onSubmit} style={{ maxWidth: "30rem" }}>
          {/* username */}
          <div className="col-12 mb-2">
            <label htmlFor="username" className="form-label">
              Username
            </label>
            <input
              id="username"
              className="form-control"
              type="text"
              placeholder="Enter username here"
              {...register("username")}
            />
          </div>

          {/* gender */}
          <div className="col-md-6">
            <label htmlFor="gender" className="form-label">
              Gender
            </label>
            <FormSelect control={control} name="gender" values={genders} />
          </div>

          {/* birthday */}
          <div className="col-md-6 mb-2">
            <label htmlFor="birthday" className="form-label">
              Birthday
            </label>
            <input
              className="form-control"
              type="date"
              id="birthday"
              placeholder="birthday"
              {...register("birthday")}
            />
          </div>

          {/* User Position */}
          <div id="userRole" className="col-md-12 mb-2">
            <label htmlFor="position" className="form-label">
              Position
            </label>
            <FormSelect
              control={control}
              name="position"
              values={userPosition}
            />
          </div>

          {userRole === "Graduate" && (
            <>
              {/* major */}
              <div className="col-12 mb-2">
                <label htmlFor="major" className="form-label">
                  Major
                </label>
                <FormMultiselect
                  id="major"
                  name="major"
                  limit={2}
                  control={control}
                  values={majors}
                />
              </div>
            </>
          )}

          {userRole === "Undergraduate" && (
            <>
              {/* Graduating Semester */}
              <div className="col-md-6 mb-2">
                <label htmlFor="semester" className="form-label">
                  Graduating Semester
                </label>
                <FormSelect
                  control={control}
                  name="gradsemester"
                  values={gradsemesters}
                />
              </div>

              {/* Graduating Year */}
              <div className="col-md-6 mb-2">
                <label htmlFor="year" className="form-label">
                  Graduating Year
                </label>
                <FormSelect
                  control={control}
                  name="gradyear"
                  values={gradyears}
                />
              </div>

              {/* class standing */}
              <div className="col-12 mb-2">
                <label htmlFor="class" className="form-label">
                  Class standing
                </label>
                <FormMultiselect
                  id="class"
                  name="class"
                  control={control}
                  values={class_list}
                />
              </div>

              {/* major */}
              <div className="col-12 mb-2">
                <label htmlFor="major" className="form-label">
                  Major
                </label>
                <FormMultiselect
                  id="major"
                  name="major"
                  limit={2}
                  control={control}
                  values={majors}
                />
              </div>

              {/* minor */}
              <div className="col-12 mb-2">
                <label htmlFor="minor" className="form-label">
                  Minor
                </label>
                <FormMultiselect
                  id="minor"
                  name="minor"
                  limit={2}
                  control={control}
                  values={minors}
                />
              </div>
            </>
          )}

          {/* submission options */}
          <div className="d-flex justify-content-between">
            <Link to="/">
              <button className="btn btn-link text-light">Cancel</button>
            </Link>
            <button type="submit" className="btn btn-secondary mr-5 mt-2">
              Register
            </button>
          </div>
        </form>
      </div>
    </PageCard>
  );
};

export default Registration;
