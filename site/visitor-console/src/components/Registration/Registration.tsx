import { State, Props } from '../App/App';
import React, { useState, Dispatch, SetStateAction } from 'react';
import Select, { MultiValue } from 'react-select';
import { Link } from 'react-router-dom';

const Registration = (props: Props) => {
    const [firstname, setFirstname]: [string, Dispatch<SetStateAction<string>>] = useState<string>("");
    const [lastname, setLastname]: [string, Dispatch<SetStateAction<string>>] = useState<string>("");
    const [gender, setGender]: [string, Dispatch<SetStateAction<string>>] = useState<string>("");
    const [birthday, setBirthday]: [string, Dispatch<SetStateAction<string>>] = useState<string>("");
    const [expGradDate, setExpGradDate]: [string, Dispatch<SetStateAction<string>>] = useState<string>("");
    const [majors, setMajors]: [string[], Dispatch<SetStateAction<string[]>>] = useState<string[]>([]);
    const [minors, setMinors]: [string[], Dispatch<SetStateAction<string[]>>] = useState<string[]>([]);

    interface selectOption {
        value: string;
        label: string;
    }
    const genderOptions: selectOption[] = ["Male", "Female", "Other"].map(d => {return {value: d, label: d}});
    const majorOptions: selectOption[] = ["Accounting", "Agribusiness", "Agricultural Education", 
                    "Agricultural Mechanization and Business", "Agriculture", "Animal and Veterinary Sciences",
                    "Anthropology", "Applied Economics", "Applied Health Research and Evaluation",
                    "Applied Psychology", "Architecture", "Art", "Athletic Leadership", "Automotive Engineering",
                    "Biochemistry", "Biochemistry and Molecular Biology", "Bioengineering", "Biological Sciences", 
                    "Biomedical Engineering", "Biosystems Engineering", "Business Administration", "Chemical Engineering",
                    "Chemistry", "City and Regional Planning", "Civil Engineering", "Communication",
                    "Communication, Technology and Society", "Computer Engineering", "Computer Information Systems", 
                    "Computer Science", "Construction Science and Management", "Counselor Education", 
                    "Criminal Justice", "Curriculum and Instruction", "Data Science and Analytics", 
                    "Digital Production Arts", "Early Childhood Education", "Economics", "Educational Leadership", 
                    "Education Systems Improvement Science Ed.D.", "Electrical Engineering", "Elementary Education", 
                    "Engineering and Science Education", "English", "Entomology", "Environmental and Natural Resources", 
                    "Environmental Engineering", "Environmental Health Physics", "Environmental Toxicology", 
                    "Financial Management", "Food, Nutrition and Culinary Sciences", "Food, Nutrition and Packaging Sciences",
                    "Food Science and Human Nutrition", "Food Technology", "Forest Resource Management",
                    "Forest Resources", "Genetics", "Geology", "Graphic Communications", 
                    "Healthcare Genetics", "Health Science", "Historic Preservation", "History", "Horticulture",
                    "Human-Centered Computing", "Human Capital Education and Development", "Human Factors Psychology",
                    "Human Resource Development", "Hydrogeology", "Industrial Engineering",
                    "Industrial/Organizational Psychology", "International Family and Community Studies", 
                    "Landscape Architecture", "Language and International Health", "Language and International Business",
                    "Learning Sciences", "Literacy", "Literacy, Language and Culture", "Management", "Marketing", 
                    "Materials Science and Engineering", "Mathematical Sciences", "Mathematics Teaching",
                    "Mechanical Engineering", "Microbiology", "Middle Level Education", "Modern Languages",
                    "Nursing", "Packaging Science", "Pan African Studies", "Parks, Recreation and Tourism Management",
                    "Philosophy", "Photonic Science and Technology", "Physics", "Planning, Design and Built Environment",
                    "Plant and Environmental Sciences", "Policy Studies", "Political Science", "Prepharmacy",
                    "Preprofessional Health Studies", "Preveterinary Medicine", "Performing Arts",
                    "Professional Communication", "Psychology", "Public Administration", "Real Estate Development",
                    "Religious Studies", "Resilient Urban Design", "Rhetorics, Communication and Information Design",
                    "Science Teaching", "Secondary Education", "Sociology", "Social Science", "Special Education",
                    "Sports Communication", "Student Affairs", "Teacher Residency", "Teaching and Learning", 
                    "Transportation Safety Administration", "Turfgrass", "Wildlife and Fisheries Biology",
                    "Women's Leadership", "World Cinema", "Youth Development Leadership"].map(d => {return {value: d, label: d}});;
    const minorOptions: selectOption[] = ["Accounting", "Adult/Extension Education", "Aerospace Studies",
                    "Agricultural Business Management", "Agricultural Mechanization and Business", 
                    "American Sign Language Studies", "Animal and Veterinary Sciences", "Anthropology",
                    "Architecture", "Art", "Athletic Leadership", "Biochemistry", "Biological Sciences", 
                    "British and Irish Studies", "Brand Communications", "Business Administration", 
                    "Chemistry", "Chinese Studies", "Cluster", "Communication Studies",
                    "Computer Science", "Creative Writing", "Crop and Soil Environmental Science", 
                    "Cybersecurity", "Digital Production Arts", "East Asian Studies", "Economics", 
                    "English", "Entomology", "Entrepreneurship", "Environmental Science and Policy",
                    "Equine Industry", "Film Studies", "Financial Management", "Food Science",
                    "Forest Products", "Forest Resource Management", "French Studies", 
                    "Gender, Sexuality and Women's Studies", "Genetics", "Geography", "Geology",
                    "German Studies", "Global Politics", "Great Works", "History", "Horticulture",
                    "Human Resource Management", "International Engineering and Science",
                    "Italian Studies", "Japanese Studies", "Legal Studies", "Management",
                    "Management Information Systems", "Mathematical Sciences", "Microbiology",
                    "Middle Eastern Studies", "Military Leadership", "Music", 
                    "Natural Resource Economics", "Nonprofit Leadership", 
                    "Nuclear Engineering and Radiological Sciences", "Packaging Science",
                    "Pan African Studies", "Park and Protected Area Management", "Philosophy",
                    "Physics", "Plant Pathology", "Political and Legal Theory", "Political Science", 
                    "Precision Agriculture", "Psychology", "Public Policy", "Race, Ethnicity and Migration",
                    "Religious Studies", "Russian Area Studies", "Science and Technology in Society",
                    "Screenwriting", "Sociology", "Spanish Studies", "Spanish-American Area Studies",
                    "Sustainability", "Theatre", "Travel and Tourism", "Turfgrass", "Urban Forestry",
                    "Wildlife and Fisheries Biology", "Women's Leadership", "Writing", 
                    "Youth Development Studies"].map(d => {return {value: d, label: d}});;

    const handleFirstnameInput = (event: React.ChangeEvent<HTMLInputElement>): void => {
        setFirstname(event.currentTarget.value);
    }
    const handleLastnameInput = (event: React.ChangeEvent<HTMLInputElement>): void => {
        setLastname(event.currentTarget.value);
    }
    const handleGenderInput = (gender: selectOption | null): void => {
        setGender(gender ? gender.value : "Error")
    }
    const handleBirthdayInput = (event: React.ChangeEvent<HTMLInputElement>): void => {
        setBirthday(event.currentTarget.value);
    }
    const handleExpGradDateInput = (event: React.ChangeEvent<HTMLInputElement>): void => {
        setExpGradDate(event.currentTarget.value);
    }
    const handleMajorInput = (majors: MultiValue<selectOption>): void => {
        setMajors(majors.map(d => d.value));
    }
    const handleMinorInput = (minors: MultiValue<selectOption>): void => {
        setMinors(minors.map(d => d.value));
    }

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
        const params = {
            username: "username",
            firstName: firstname,
            lastName: lastname,
            Gender: gender,
            DOB: birthday,
            Grad_Date: expGradDate,
            Major: majors,
            Minor: minors
        };
        fetch("https://d1o39u66ph.execute-api.us-east-1.amazonaws.com/prod/register", {
            method:"post",
            body:JSON.stringify(params)
        }).then(response => {
            if (response.ok) {
                alert("Registration successful");
            } else {
                alert("Registration unsuccessful");
            }
        })
        event.preventDefault();
        setFirstname("");
        setLastname("");
        setGender("");
        setBirthday("");
        setExpGradDate("");
        setMajors([]);
        setMinors([]);
    }
  
    return (
        <div className="container bg-primary p-5 rounded" style={{height: "400px"}}>
        <h1 className="text-secondary fw-bold mb-4 text-center">Visit the Makerspace!</h1>
        <div className="d-flex justify-content-center">

        <div className="text-light">{"Please FIll in Registration Information"}
            <form onSubmit={handleSubmit}>
                <div>
                    <input type={"text"} 
                    value={firstname} 
                    onChange={handleFirstnameInput} 
                    placeholder={"firstname"}/>
                    <input type={"text"} 
                    value={lastname} 
                    onChange={handleLastnameInput} 
                    placeholder={"lastname"}/>
                    <br/>
                    <label>Gender:
                        <Select className="text-black"
                        options={genderOptions}
                        onChange={handleGenderInput}
                        />
                    </label>
                    <br/>
                    <label>Birthday:
                        <input type={"date"} 
                        value={birthday} 
                        onChange={handleBirthdayInput} 
                        placeholder={"birthday"}/>
                    </label>
                    <br/>
                    <label>Expected Graduation Date:
                        <input type={"date"} 
                        value={expGradDate} 
                        onChange={handleExpGradDateInput} 
                        placeholder={"expGradDate"}/>
                    </label>
                    <br/>
                    <label>Major(s):
                        <Select className="text-black"
                        options={majorOptions}
                        onChange={handleMajorInput}
                        isMulti
                        isSearchable
                        />
                    </label>
                    <label>Minor(s):
                        <Select className="text-black"
                        options={minorOptions}
                        onChange={handleMinorInput}
                        isMulti
                        isSearchable
                        />
                    </label>
                </div>
                <div className="d-flex justify-content-start">
                    <button type="submit" className="btn btn-secondary mr-5">Register</button>
                    <Link to="/"><button className="btn btn-link text-light">Cancel</button></Link>
                </div>
            </form>
        </div>

        </div>
    </div>
    );
}
 
export default Registration;