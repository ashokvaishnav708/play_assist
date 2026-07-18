/**
 * Global authentication state: current user, auth actions, and session
 * hydration/forced-logout handling. Wrap the app in <AuthProvider> and read
 * state via the `useAuth()` hook.
 */
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

/** Shape of the value exposed by AuthContext / useAuth(). */
type AuthContextType = {
    user: User | null;
    isAuthenticated: boolean;
    /** True while the initial session hydration (getMe) is in flight. */
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
    logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>(null as unknown as AuthContextType);

/** Hook for consuming auth state/actions anywhere under <AuthProvider>. */
export function useAuth() {
    return useContext(AuthContext);
}

/** Provides auth state to the app and keeps it in sync with stored tokens. */
export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    // On mount, try to restore the session from a stored access token.
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

    // Any API call can dispatch AUTH_LOGOUT_EVENT (e.g. refresh token expired)
    // to force this context back to a logged-out state.
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
