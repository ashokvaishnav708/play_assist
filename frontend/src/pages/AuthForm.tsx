import { useState } from "react";
import { loginUser, signupUser } from "../services/api";

function AuthForm() {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e: Event) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const loginData = await loginUser(email, password);

            localStorage.setItem("token", loginData.token);
            alert("Login successful!");
            setEmail("");
            setPassword("");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Login failed");
        } finally {
            setLoading(false);
        }
    };

    const handleSignUp = async (e: Event) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);

        try {
            await signupUser(email, password, firstName, lastName);

            alert("Sign up successful! Please log in.");
            setIsLogin(true);
            setFirstName("");
            setLastName("");
            setEmail("");
            setPassword("");
            setConfirmPassword("");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Sign up failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-900 via-gray-800 to-black px-4">
            <div className="w-full max-w-md">
                {/* Card Container */}
                <div className="bg-gray-800/50 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-700/50 p-8">
                    {/* Logo / Title */}
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold bg-linear-to-r from-red-600 to-red-500 bg-clip-text text-transparent mb-2">
                            Play Assist
                        </h1>
                        <p className="text-gray-400 text-sm">Your entertainment companion</p>
                    </div>

                    {/* Tab Toggle */}
                    <div className="flex gap-4 mb-8 bg-gray-900/50 p-1 rounded-lg">
                        <button
                            onClick={() => {
                                setIsLogin(true);
                                setError("");
                            }}
                            className={`flex-1 py-2 px-4 rounded-md font-semibold transition-all duration-300 ${
                                isLogin
                                    ? "bg-red-600 text-white shadow-lg"
                                    : "text-gray-400 hover:text-gray-200"
                            }`}
                        >
                            Login
                        </button>
                        <button
                            onClick={() => {
                                setIsLogin(false);
                                setError("");
                            }}
                            className={`flex-1 py-2 px-4 rounded-md font-semibold transition-all duration-300 ${
                                !isLogin
                                    ? "bg-red-600 text-white shadow-lg"
                                    : "text-gray-400 hover:text-gray-200"
                            }`}
                        >
                            Sign Up
                        </button>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                            <p className="text-red-300 text-sm">{error}</p>
                        </div>
                    )}

                    {/* Login Form */}
                    {isLogin ? (
                        <form onSubmit={handleLogin} className="space-y-4">
                            <div>
                                <label className="block text-gray-300 text-sm font-medium mb-2">
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@example.com"
                                    required
                                    className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                />
                            </div>

                            <div>
                                <label className="block text-gray-300 text-sm font-medium mb-2">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                />
                            </div>

                            <div className="flex justify-end">
                                <a
                                    href="#"
                                    className="text-sm text-red-500 hover:text-red-400 transition-colors"
                                >
                                    Forgot password?
                                </a>
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-3 bg-linear-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white font-bold rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                            >
                                {loading ? "Logging in..." : "Login"}
                            </button>

                            <p className="text-center text-gray-400 text-sm">
                                Don't have an account?{" "}
                                <button
                                    type="button"
                                    onClick={() => setIsLogin(false)}
                                    className="text-red-500 hover:text-red-400 font-semibold transition-colors"
                                >
                                    Sign up now
                                </button>
                            </p>
                        </form>
                    ) : (
                        <form onSubmit={handleSignUp} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        First Name
                                    </label>
                                    <input
                                        type="text"
                                        value={firstName}
                                        onChange={(e) => setFirstName(e.target.value)}
                                        placeholder="John"
                                        required
                                        className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Last Name
                                    </label>
                                    <input
                                        type="text"
                                        value={lastName}
                                        onChange={(e) => setLastName(e.target.value)}
                                        placeholder="Doe"
                                        required
                                        className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-gray-300 text-sm font-medium mb-2">
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@example.com"
                                    required
                                    className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                />
                            </div>

                            <div>
                                <label className="block text-gray-300 text-sm font-medium mb-2">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                />
                            </div>

                            <div>
                                <label className="block text-gray-300 text-sm font-medium mb-2">
                                    Confirm Password
                                </label>
                                <input
                                    type="password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className="w-full px-4 py-3 rounded-lg bg-gray-900/50 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-3 bg-linear-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white font-bold rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                            >
                                {loading ? "Creating account..." : "Create Account"}
                            </button>

                            <p className="text-center text-gray-400 text-sm">
                                Already have an account?{" "}
                                <button
                                    type="button"
                                    onClick={() => setIsLogin(true)}
                                    className="text-red-500 hover:text-red-400 font-semibold transition-colors"
                                >
                                    Login now
                                </button>
                            </p>
                        </form>
                    )}
                </div>

                {/* Footer */}
                <p className="text-center text-gray-500 text-xs mt-6">
                    Your entertainment data is safe with us
                </p>
            </div>
        </div>
    );
}

export default AuthForm;