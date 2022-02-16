import { State, Props } from "../App/App";
import React, { useState, Dispatch, SetStateAction } from "react";
import Select, { MultiValue } from "react-select";
import { Link } from "react-router-dom";

const Registration = (props: Props) => {
  const [username, setUsername]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [firstname, setFirstname]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [lastname, setLastname]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [gender, setGender]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [birthday, setBirthday]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [expGradDate, setExpGradDate]: [
    string,
    Dispatch<SetStateAction<string>>
  ] = useState<string>("");
  const [majors, setMajors]: [string[], Dispatch<SetStateAction<string[]>>] =
    useState<string[]>([]);
  const [minors, setMinors]: [string[], Dispatch<SetStateAction<string[]>>] =
    useState<string[]>([]);
  const [registerSuccess, setRegisterSuccess]: [
    boolean,
    Dispatch<SetStateAction<boolean>>
  ] = useState<boolean>(false);

  interface selectOption {
    value: string;
    label: string;
  }
  const genderOptions: selectOption[] = ["Male", "Female", "Other"].map((d) => {
    return { value: d, label: d };
  });
  const majorOptions: selectOption[] = [
    "Accounting",
    "Agribusiness",
    "Agricultural Education",
    "Agricultural Mechanization and Business",
    "Agriculture",
    "Animal and Veterinary Sciences",
    "Anthropology",
    "Applied Economics",
    "Applied Health Research and Evaluation",
    "Applied Psychology",
    "Architecture",
    "Art",
    "Athletic Leadership",
    "Automotive Engineering",
    "Biochemistry",
    "Biochemistry and Molecular Biology",
    "Bioengineering",
    "Biological Sciences",
    "Biomedical Engineering",
    "Biosystems Engineering",
    "Business Administration",
    "Chemical Engineering",
    "Chemistry",
    "City and Regional Planning",
    "Civil Engineering",
    "Communication",
    "Communication, Technology and Society",
    "Computer Engineering",
    "Computer Information Systems",
    "Computer Science",
    "Construction Science and Management",
    "Counselor Education",
    "Criminal Justice",
    "Curriculum and Instruction",
    "Data Science and Analytics",
    "Digital Production Arts",
    "Early Childhood Education",
    "Economics",
    "Educational Leadership",
    "Education Systems Improvement Science Ed.D.",
    "Electrical Engineering",
    "Elementary Education",
    "Engineering and Science Education",
    "English",
    "Entomology",
    "Environmental and Natural Resources",
    "Environmental Engineering",
    "Environmental Health Physics",
    "Environmental Toxicology",
    "Financial Management",
    "Food, Nutrition and Culinary Sciences",
    "Food, Nutrition and Packaging Sciences",
    "Food Science and Human Nutrition",
    "Food Technology",
    "Forest Resource Management",
    "Forest Resources",
    "Genetics",
    "Geology",
    "Graphic Communications",
    "Healthcare Genetics",
    "Health Science",
    "Historic Preservation",
    "History",
    "Horticulture",
    "Human-Centered Computing",
    "Human Capital Education and Development",
    "Human Factors Psychology",
    "Human Resource Development",
    "Hydrogeology",
    "Industrial Engineering",
    "Industrial/Organizational Psychology",
    "International Family and Community Studies",
    "Landscape Architecture",
    "Language and International Health",
    "Language and International Business",
    "Learning Sciences",
    "Literacy",
    "Literacy, Language and Culture",
    "Management",
    "Marketing",
    "Materials Science and Engineering",
    "Mathematical Sciences",
    "Mathematics Teaching",
    "Mechanical Engineering",
    "Microbiology",
    "Middle Level Education",
    "Modern Languages",
    "Nursing",
    "Packaging Science",
    "Pan African Studies",
    "Parks, Recreation and Tourism Management",
    "Philosophy",
    "Photonic Science and Technology",
    "Physics",
    "Planning, Design and Built Environment",
    "Plant and Environmental Sciences",
    "Policy Studies",
    "Political Science",
    "Prepharmacy",
    "Preprofessional Health Studies",
    "Preveterinary Medicine",
    "Performing Arts",
    "Professional Communication",
    "Psychology",
    "Public Administration",
    "Real Estate Development",
    "Religious Studies",
    "Resilient Urban Design",
    "Rhetorics, Communication and Information Design",
    "Science Teaching",
    "Secondary Education",
    "Sociology",
    "Social Science",
    "Special Education",
    "Sports Communication",
    "Student Affairs",
    "Teacher Residency",
    "Teaching and Learning",
    "Transportation Safety Administration",
    "Turfgrass",
    "Wildlife and Fisheries Biology",
    "Women's Leadership",
    "World Cinema",
    "Youth Development Leadership",
  ].map((d) => {
    return { value: d, label: d };
  });
  const minorOptions: selectOption[] = [
    "Accounting",
    "Adult/Extension Education",
    "Aerospace Studies",
    "Agricultural Business Management",
    "Agricultural Mechanization and Business",
    "American Sign Language Studies",
    "Animal and Veterinary Sciences",
    "Anthropology",
    "Architecture",
    "Art",
    "Athletic Leadership",
    "Biochemistry",
    "Biological Sciences",
    "British and Irish Studies",
    "Brand Communications",
    "Business Administration",
    "Chemistry",
    "Chinese Studies",
    "Cluster",
    "Communication Studies",
    "Computer Science",
    "Creative Writing",
    "Crop and Soil Environmental Science",
    "Cybersecurity",
    "Digital Production Arts",
    "East Asian Studies",
    "Economics",
    "English",
    "Entomology",
    "Entrepreneurship",
    "Environmental Science and Policy",
    "Equine Industry",
    "Film Studies",
    "Financial Management",
    "Food Science",
    "Forest Products",
    "Forest Resource Management",
    "French Studies",
    "Gender, Sexuality and Women's Studies",
    "Genetics",
    "Geography",
    "Geology",
    "German Studies",
    "Global Politics",
    "Great Works",
    "History",
    "Horticulture",
    "Human Resource Management",
    "International Engineering and Science",
    "Italian Studies",
    "Japanese Studies",
    "Legal Studies",
    "Management",
    "Management Information Systems",
    "Mathematical Sciences",
    "Microbiology",
    "Middle Eastern Studies",
    "Military Leadership",
    "Music",
    "Natural Resource Economics",
    "Nonprofit Leadership",
    "Nuclear Engineering and Radiological Sciences",
    "Packaging Science",
    "Pan African Studies",
    "Park and Protected Area Management",
    "Philosophy",
    "Physics",
    "Plant Pathology",
    "Political and Legal Theory",
    "Political Science",
    "Precision Agriculture",
    "Psychology",
    "Public Policy",
    "Race, Ethnicity and Migration",
    "Religious Studies",
    "Russian Area Studies",
    "Science and Technology in Society",
    "Screenwriting",
    "Sociology",
    "Spanish Studies",
    "Spanish-American Area Studies",
    "Sustainability",
    "Theatre",
    "Travel and Tourism",
    "Turfgrass",
    "Urban Forestry",
    "Wildlife and Fisheries Biology",
    "Women's Leadership",
    "Writing",
    "Youth Development Studies",
  ].map((d) => {
    return { value: d, label: d };
  });

  const handleUsernameInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setUsername(event.currentTarget.value);
  };
  const handleFirstnameInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setFirstname(event.currentTarget.value);
  };
  const handleLastnameInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setLastname(event.currentTarget.value);
  };
  const handleGenderInput = (gender: selectOption | null): void => {
    setGender(gender ? gender.value : "Error");
  };
  const handleBirthdayInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setBirthday(event.currentTarget.value);
  };
  const handleExpGradDateInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setExpGradDate(event.currentTarget.value);
  };
  const handleMajorInput = (majors: MultiValue<selectOption>): void => {
    setMajors(majors.map((d) => d.value));
  };
  const handleMinorInput = (minors: MultiValue<selectOption>): void => {
    setMinors(minors.map((d) => d.value));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    const params = {
      username: username,
      firstName: firstname,
      lastName: lastname,
      Gender: gender,
      DOB: birthday,
      Grad_Date: expGradDate,
      Major: majors.toString(),
      Minor: minors.toString(),
    };

    fetch("https://api.cumaker.space/register", {
      method: "post",
      body: JSON.stringify(params),
    }).then((response) => {
      if (response.ok) {
        setRegisterSuccess(true);
      } else {
        alert("Registration unsuccessful");
      }
    });

    event.preventDefault();

    setUsername("");
    setFirstname("");
    setLastname("");
    setGender("");
    setBirthday("");
    setExpGradDate("");
    setMajors([]);
    setMinors([]);
  };

  if (registerSuccess) {
    return (
      <div
        className="container bg-primary p-5 rounded text-center"
        style={{ height: "150px" }}
      >
        <h1 className="text-secondary">Registration Successful</h1>
      </div>
    );
  } else {
    return (
      <div className="container bg-primary p-5 rounded">
        <div className="text-center mb-4">
          <h1 className="text-secondary fw-bold mb-1 text-center">
            Register to the Makerspace!
          </h1>
          <span className="text-center text-light">
            Please Fill in Registration Information
          </span>
        </div>
        <div className="d-flex flex-column align-items-center text-light">
          <form
            className="row"
            onSubmit={handleSubmit}
            style={{ maxWidth: "30rem" }}
          >
            {/* username */}
            <div className="col-12 mb-2">
              <label htmlFor="username" className="form-label">
                Username
              </label>
              <input
                id="username"
                className="form-control"
                type="text"
                value={username}
                onChange={handleUsernameInput}
                placeholder="Enter username here"
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
                value={firstname}
                onChange={handleFirstnameInput}
                placeholder="Firstname"
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
                value={lastname}
                onChange={handleLastnameInput}
                placeholder="Lastname"
              />
            </div>

            {/* gender */}
            <div className="col-md-6">
              <label htmlFor="gender" className="form-label">
                Gender
              </label>
              <Select
                className="text-black"
                id="gender"
                value={gender !== "" ? { value: gender, label: gender } : null}
                options={genderOptions}
                onChange={handleGenderInput}
                placeholder="Gender"
              />
            </div>

            {/* birthday */}
            <div className="col-md-6 mb-2">
              <label htmlFor="birthday" className="form-label">
                Birthday
              </label>
              <input
                className="form-control"
                type={"date"}
                value={birthday}
                id="birthday"
                onChange={handleBirthdayInput}
                placeholder="birthday"
              />
            </div>

            {/* grad date */}
            <div className="col-12 mb-2">
              <label htmlFor="graddate" className="form-label">
                Expected Graduation Date
              </label>
              <input
                type={"date"}
                className="form-control"
                value={expGradDate}
                id="graddate"
                onChange={handleExpGradDateInput}
              />
            </div>

            {/* major */}
            <div className="col-12 mb-2">
              <label htmlFor="major" className="form-label">
                Major(s)
              </label>
              <Select
                className="text-black"
                id="major"
                value={majors.map((d) => {
                  return { value: d, label: d };
                })}
                options={majorOptions}
                onChange={handleMajorInput}
                isMulti
                isSearchable
              />
            </div>

            {/* minor */}
            <div className="col-12 mb-4">
              <label htmlFor="minor" className="form-label">
                Minor(s)
              </label>
              <Select
                className="text-black"
                id="minor"
                value={minors.map((d) => {
                  return { value: d, label: d };
                })}
                options={minorOptions}
                onChange={handleMinorInput}
                isMulti
                isSearchable
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
      </div>
    );
  }
};

export default Registration;
