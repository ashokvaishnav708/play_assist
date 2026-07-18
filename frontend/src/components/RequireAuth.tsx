import { Navigate, useLocation } from "react-router";
import type { ReactNode } from "react";
import { useAuth } from "../contexts/AuthContext";

/**
 * Route guard: renders `children` only once auth state has hydrated and the
 * user is authenticated; otherwise shows a loading state or redirects to
 * /auth_form (preserving the originating location for a post-login return).
 */
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
