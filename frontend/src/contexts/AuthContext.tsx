import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "../services/types";
import {
    loginUser,
    signupUser,
    logoutUser,
    getMe,
    getAccessToken,
    AUTH_LOGOUT_EVENT,
} from "../services/api";

type AuthContextType = {
    user: User | null;
    isAuthenticated: boolean;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
    logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>(null as unknown as AuthContextType);

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function hydrate() {
            if (!getAccessToken()) {
                setLoading(false);
                return;
            }
            try {
                setUser(await getMe());
            } catch {
                setUser(null);
            } finally {
                setLoading(false);
            }
        }
        hydrate();
    }, []);

    useEffect(() => {
        function handleForcedLogout() {
            setUser(null);
        }
        window.addEventListener(AUTH_LOGOUT_EVENT, handleForcedLogout);
        return () => window.removeEventListener(AUTH_LOGOUT_EVENT, handleForcedLogout);
    }, []);

    async function login(email: string, password: string) {
        const data = await loginUser(email, password);
        setUser(data.user);
    }

    async function signup(email: string, password: string, firstName: string, lastName: string) {
        await signupUser(email, password, firstName, lastName);
    }

    async function logout() {
        await logoutUser();
        setUser(null);
    }

    const value = {
        user,
        isAuthenticated: !!user,
        loading,
        login,
        signup,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}
