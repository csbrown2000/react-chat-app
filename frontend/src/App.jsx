import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route, Link } from 'react-router-dom';
import Chats from './components/Chats'
import './App.css'
import { AuthProvider, useAuth } from './context/auth';
import { UserProvider } from './context/user';
import TopNav from './components/TopNav';
import Login from './components/Login';
import Registration from './components/Registration';
import Profile from './components/Profile';

const queryClient = new QueryClient();

function AuthenticatedRoutes(){
	return (
		<Routes>
			<Route path="/" element={<Chats/>} />
			<Route path="/chats" element={<Chats/>} />
			<Route path="/chats/:chatId" element={<Chats/>} />
			<Route path="/profile" element={<Profile/>} />
		</Routes>
	)
}

function UnauthenticatedRoutes() {
	return (
	  <Routes>
		<Route path="/" element={<Home/>} />
		<Route path="/login" element={<Login/>} />
		<Route path="/register" element={<Registration/>} />
		<Route path="*" element={<Navigate to="/login" />} />
	  </Routes>
	);
  }

function Main() {
	const { isLoggedIn } = useAuth();

	return (
		<main className="max-h-screen">
		{isLoggedIn ?
			<AuthenticatedRoutes /> :
			<UnauthenticatedRoutes />
		}
		</main>
	);	
}

  function Home() {
	  return (
		  <div className='flex flex-grow flex-col justify-evenly items-center gap-5 max-w-full p-10'>
			  <h2 className='font-bold text-2xl'>Welcome to Pony Express</h2>
			  <p className='text-md max-w-lg text-center' >
				  Pony Express is a chat application built using a React frontend and FastAPI for the backend. 
				  This application allows user to view their chats and communicate with the other users in a chat room.
				  Additionally, Pony Express features user authentication and profiles.
			  </p>
			  <Link to={`/login`}>
				  <p className='text-yellow-500 text-md'>
					  get started
				  </p>
			  </Link>
		  </div>
	  )
  }
  
function App() {
	const className = [
		"h-screen max-h-screen",
		"w-screen mx-auto",
		"bg-gray-700 text-white",
		"flex flex-col",
	  ].join(" ");

	return (
		<QueryClientProvider client={queryClient}>
			<BrowserRouter>
				<AuthProvider>
					<UserProvider>
						<div className={className}>
							<TopNav/>
							<Main/>
						</div>
					</UserProvider>
				</AuthProvider>
			</BrowserRouter>
		</QueryClientProvider>
	);
}

export default App
