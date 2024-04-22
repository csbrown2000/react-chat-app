import { useState } from "react";
import { Link, useNavigate, NavLink} from "react-router-dom";
import { useAuth } from "../context/auth";
import FormInput from "./FormInput";

const baseUrl = import.meta.env.VITE_API_BASE_URL;

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function LoginOption(){
	return(
		<div className="flex flex-grow flex-row gap-5 justify-center py-5">
			<p className="text-white">Already have an account?</p>
			<NavLink to="/register" className="text-yellow-400">
				Login
			</NavLink>
		</div>
	)
}

function Registration() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const disabled = username === "" && email === "" && password === "";

  const onSubmit = (e) => {
    e.preventDefault();

    fetch(
      `${baseUrl}/auth/registration`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      },
    ).then((response) => {
      if (response.ok) {
        navigate("/login");
      } else if (response.status === 422) {
        response.json().then((data) => {
          setError(data.detail.entity_field + " already taken");
        });
      } else {
        setError("error logging in");
      }
    });
  }

  return (
    <div className="max-w-96 mx-auto py-8 px-4">
      <form onSubmit={onSubmit} className="flex flex-col items-center">
        <FormInput type="text" label="username" setter={setUsername} />
        <FormInput type="email" label="email" setter={setEmail} />
        <FormInput type="password" label="password" setter={setPassword} />
		<div className="flex justify-center items-center border-gray-100 border rounded-full w-1/2 mt-2">
			<button type="submit" disabled={disabled}>
				Create Account
			</button>
		</div>
        <Error message={error} />
      </form>
      <LoginOption/>
    </div>
  );
}

export default Registration;