import { useUser } from '../context/user'
import { useAuth } from '../context/auth'

function ProfileLineItem({label, value}){
	return (
		<div className="px-2 py-2 flex flex-row justify-between border-t border-gray-400">
			<p className="text-gray-300">{label}</p>
			<p className="text-white">{value}</p>
		</div>
	)
}

function LogoutButton() {
	const { logout } = useAuth();

	return (
		<button type="button" className='border rounded-md p-2' onClick={logout} >
			Logout
		</button>
	)
}

function ProfileContainer() {

	const user = useUser();

	return (
		<>
			<div className="border-2 border-slate-500 rounded w-1/3 pt-5 pb-1">
				<h2 className='font-bold ps-3 pb-2 text-lg'>Details</h2>
				<ProfileLineItem label="username" value={user.username}/>
				<ProfileLineItem label="email" value={user.email}/>
				<ProfileLineItem label="member since" value={new Date(user.created_at).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}/>
			</div>

			<div className='pt-5'>
				<LogoutButton/>
			</div>
		</>
	)
}

function Profile(){
	return (
		<div className='flex flex-col items-center pt-16'>
			<ProfileContainer/>
		</div>
	)
}

export default Profile;