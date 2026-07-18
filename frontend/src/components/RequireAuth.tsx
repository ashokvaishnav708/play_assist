import { Navigate, useLocation } from "react-router";
import type { ReactNode } from "react";
import { useAuth } from "../contexts/AuthContext";

function RequireAuth({ children }: { children: ReactNode }) {
    const { isAuthenticated, loading } = useAuth();
    const location = useLocation();

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh] text-gray-400">
                Loading...
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/auth_form" state={{ from: location }} replace />;
    }

    return <>{children}</>;
}

export default RequireAuth;
