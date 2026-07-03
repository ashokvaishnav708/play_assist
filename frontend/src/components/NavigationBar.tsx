import { Link } from "react-router";

function NavigationBar() {
    return (
        <nav className="bg-black/80 backdrop-blur-md px-6 py-4 flex justify-between items-center shadow-lg border-b border-gray-800/50 sticky top-0 z-50">
            <Link to='/' className="flex items-center gap-3 hover:opacity-80 transition-opacity group">
                <div className="w-8 h-8 bg-linear-to-r from-red-600 to-red-500 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-lg">▶</span>
                </div>
                <span className="text-2xl font-bold bg-linear-to-r from-red-600 to-red-500 bg-clip-text text-transparent">
                    Play Assist
                </span>
            </Link>
            
            <div className="flex gap-1">
                <Link to='/' className="px-4 py-2 rounded-lg text-gray-300 font-medium transition-all duration-200 hover:bg-gray-800/50 hover:text-white">
                    Home
                </Link>
                <Link to='/favorites' className="px-4 py-2 rounded-lg text-gray-300 font-medium transition-all duration-200 hover:bg-gray-800/50 hover:text-white">
                    ❤️ Favorites
                </Link>
                <Link to='/settings' className="px-4 py-2 rounded-lg text-gray-300 font-medium transition-all duration-200 hover:bg-gray-800/50 hover:text-white">
                    Settings
                </Link>
                <Link to='/ask_ai' className="px-4 py-2 rounded-lg text-gray-300 font-medium transition-all duration-200 hover:bg-gray-800/50 hover:text-white">
                    🤖 Ask AI
                </Link>
                <Link to='/auth_form' className="px-4 py-2 ml-2 rounded-lg bg-linear-to-r from-red-600 to-red-500 text-white font-medium transition-all duration-200 hover:shadow-lg hover:shadow-red-500/50">
                    Login
                </Link>
            </div>
        </nav>
    );
}

export default NavigationBar;