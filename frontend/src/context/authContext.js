import { createContext } from "react";

export const AuthContext = createContext({
  isLoggedIn: false,
  userID: null,
  login: () => {},
  logout: () => {},
});
