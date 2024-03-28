import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
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
		<Route path="/" element={<Chats/>} />
		<Route path="/login" element={<Login/>} />
		<Route path="/register" element={<Registration/>} />
		<Route path="*" element={<Navigate to="/login" />} />
	  </Routes>
	);
  }

function Main() {
	const { isLoggedIn } = useAuth();

	return (
		<main className="max-h-main">
		{isLoggedIn ?
			<AuthenticatedRoutes /> :
			<UnauthenticatedRoutes />
		}
		</main>
	);	
}

function Home() {
	const { isLoggedIn, logout } = useAuth();
  
	return (
	  <div className="max-w-full mx-auto text-center px-4 py-8">
		<div className="py-2">
		  logged in: {isLoggedIn.toString()}
		</div>
	  </div>
	);
  }

function App() {
	const className = [
		"h-screen w-screen",
		"max-w-full mx-auto",
		"min-w-full",
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
