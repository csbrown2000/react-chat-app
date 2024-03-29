function FormInput({label, type, setter}){
	let handleChange;
	if (setter){
		handleChange = (e) => setter(e.target.value);
	}

	return (
		<div className="flex flex-col p-3 w-full gap-2">
			<label htmlFor={label} className="font-bold">
				{label}
			</label>
			<input type={type} onChange={handleChange} className="border rounded bg-transparent text-white focus:border-orange-400 appearance-none p-1"/>
		</div>
	)
}

export default FormInput