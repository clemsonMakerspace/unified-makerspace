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
} from "../library/constants";
import FormSelect from "../components/FormSelect";
import FormMultiselect from "../components/FormMultiselect";
import PageCard from "../components/PageCard";

interface Schema {
  username: string;
  firstname: string;
  lastname: string;
  gender: string;
  birthday: Date;
  position: string;
  gradsemester?: string;
  gradyear?: string;
  major?: string[];
  minor?: string[];
}

const schema: SchemaOf<Schema> = yup
  .object({
    username: yup.string().required(),
    firstname: yup.string().required(),
    lastname: yup.string().required(),
    gender: yup.string().required(),
    birthday: yup.date().required(),
    position: yup.string().required(),
    gradsemester: yup.string(),
    gradyear: yup.string(),
    major: yup.array(),
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

  const register_user = (form_data: Schema): void => {
    const body = {
      username: form_data.username,
      firstName: form_data.firstname,
      lastName: form_data.lastname,
      Gender: form_data.gender,
      DOB: format_date(form_data.birthday),
      UserPosition: form_data.position,
      GradSemester: form_data.gradsemester,
      GradYear: form_data.gradyear,
      Major: form_data.major,
      Minor: form_data.minor,
    };

    fetch(`${api_endpoint}/register`, {
      method: "post",
      body: JSON.stringify(body),
    }).then((response) => {
      if (response.ok) {
        reset();
        setRegistered(true);
      } else {
        alert("Registration unsuccessful");
      }
    });
  };

  if (registered) return <PageCard title="Registration Successful" />;

  let userRole = watch("position");
  if (userRole && userRole === "Undergraduate Student") {
    document.getElementById("userRole")!.className = "col-md-12 mb-2";
    document.querySelectorAll("[id=undergradData]").forEach((element) => {
      element.setAttribute("style", "display:block");
    });
  } else if (userRole && userRole !== "Undergraduate Student") {
    document.getElementById("userRole")!.className = "col-md-12 mb-4";
    document.querySelectorAll("[id=undergradData]").forEach((element) => {
      element.setAttribute("style", "display:none");
    });
  }

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

          {/* firstname */}
          <div className="col-md-6 mb-2">
            <label htmlFor="firstname" className="form-label">
              Firstname
            </label>
            <input
              className="form-control col-md-6"
              type="text"
              id="firstname"
              placeholder="Firstname"
              {...register("firstname")}
            />
          </div>

          {/* lastname */}
          <div className="col-md-6 mb-2">
            <label htmlFor="firstname" className="form-label">
              Lastname
            </label>
            <input
              className="form-control"
              type="text"
              id="firstname"
              placeholder="Lastname"
              {...register("lastname")}
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
          <div id="userRole" className="col-md-12 mb-4">
            <label htmlFor="position" className="form-label">
              Position
            </label>
            <FormSelect
              control={control}
              name="position"
              values={userPosition}
            />
          </div>

          {/* Graduating Semester */}
          <div
            id="undergradData"
            style={{ display: "none" }}
            className="col-md-6 mb-2"
          >
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
          <div
            id="undergradData"
            style={{ display: "none" }}
            className="col-md-6 mb-2"
          >
            <label htmlFor="year" className="form-label">
              Graduating Year
            </label>
            <FormSelect control={control} name="gradyear" values={gradyears} />
          </div>

          {/* major */}
          <div
            id="undergradData"
            style={{ display: "none" }}
            className="col-12 mb-2"
          >
            <label htmlFor="major" className="form-label">
              Major(s)
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
          <div
            id="undergradData"
            style={{ display: "none" }}
            className="col-12 mb-4"
          >
            <label htmlFor="minor" className="form-label">
              Minor(s)
            </label>
            <FormMultiselect
              id="minor"
              name="minor"
              limit={2}
              control={control}
              values={minors}
            />
          </div>

          {/* submission options */}
          <div className="d-flex justify-content-between">
            <button type="submit" className="btn btn-secondary mr-5">
              Register
            </button>
            <Link to="/">
              <button className="btn btn-link text-light">Cancel</button>
            </Link>
          </div>
        </form>
      </div>
    </PageCard>
  );
};

export default Registration;
