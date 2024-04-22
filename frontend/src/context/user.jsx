import { createContext, useContext, useEffect } from "react";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./auth";

const UserContext = createContext();
const baseUrl = import.meta.env.VITE_API_BASE_URL;

function UserProvider({ children }) {
  const { isLoggedIn, logout, token } = useAuth();
  const navigate = useNavigate();

  const { data } = useQuery({
    queryKey: ["users", token],
    enabled: isLoggedIn,
    staleTime: Infinity,
    queryFn: () => (
      fetch(
        `${baseUrl}/users/me`,
        {
          headers: {
            "Authorization": "Bearer " + token,
          },
        },
      ).then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          logout();
          navigate("/login");
        }
      })
    ),
  });

  return (
    <UserContext.Provider value={data?.user}>
      {children}
    </UserContext.Provider>
  );
}

const useUser = () => useContext(UserContext);

export { UserProvider, useUser };