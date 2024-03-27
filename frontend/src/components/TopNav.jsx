import { NavLink } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

function NavItem({ to, name, right }) {
  const className = [
    "border-purple-400",
    "py-2 px-4",
    "hover:bg-slate-800",
	"text-center justify-center content-center",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-slate-1000" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function AuthenticatedNavItems() {
  const user = useUser();

  return (
	<>
		<NavLink to="/" className="text-white text-left text-2xl flex-1 py-2 px-4" >
			Pony Express
		</NavLink>
		<NavItem to="/profile" name={user?.username} right />
	</>
  );
}

function UnauthenticatedNavItems() {
  return (
	<>
		<NavLink to="/" className="text-white text-left text-2xl flex-1 py-2 px-4" >
			Pony Express
		</NavLink>
		<NavItem to="/login" name="Login" right />
	</>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="flex flex-row border-b-2 border-gray-300">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;
