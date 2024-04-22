import { NavLink, useNavigate } from "react-router-dom";
import { useState } from "react"
import { useAuth } from "../context/auth"
import FormInput from "./FormInput";

const baseUrl = import.meta.env.VITE_API_BASE_URL;

function CreateAccountOptions(){
	return(
		<div className="flex flex-grow flex-row gap-5">
			<p className="text-white">Don't have an account?</p>
			<NavLink to="/register" className="text-yellow-400">
				Create an account
			</NavLink>
		</div>
	)
}

function LoginForm(){
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const [error, setError] = useState("");

	const navigate = useNavigate();

	const { login } = useAuth();

	const disabled = username === "" || password === "";

	const onSubmit = (e) => {
		e.preventDefault();

		fetch(
			`${baseUrl}/auth/token`,
			{
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({ username, password }),
			},
		).then((response) => {
			if (response.ok) {
			response.json().then(login);
			navigate("/");
			} else if (response.status === 401) {
			response.json().then((data) => {
				setError(data.detail.error_description);
			});
			} else {
			setError("error logging in");
			}
		});
	}

	return (
		<form onSubmit={onSubmit} className="flex grow flex-col justify-center items-center w-1/3">
			<FormInput label="username" type="text" setter={setUsername}/>
			<FormInput label="password" type="password" setter={setPassword} />
			<div className="flex justify-center items-center border-gray-100 border rounded-full w-1/2 mt-2">
				<button type="submit" disabled={disabled}>
					Login
				</button>
			</div>

		</form>
	)
}

function Login(){

	return (
		<div className="flex grow flex-col justify-center items-center p-5 gap-5">
			<LoginForm/>
			<CreateAccountOptions/>
		</div>
	)
}

export default Login;