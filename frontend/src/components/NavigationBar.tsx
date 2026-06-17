import { Link } from "react-router";

function NavigationBar() {
    return (
        <nav className="bg-black px-8 py-4 flex justify-between items-center shadow-md">
            <div className="text-2xl font-bold">
                <Link to='/'><img src="./app_logo.svg" className="w-6 h-6 inline mr-2" />Play Assist</Link>
            </div>
            <div className="flex gap-8">
                <Link to='/' className="text-base px-4 py-2 rounded transition-colors hover:bg-white/10">Home</Link>
                <Link to='/favorites' className="text-base px-4 py-2 rounded transition-colors hover:bg-white/10">Favorites</Link>
                <Link to='/auth_form' className="text-base px-4 py-2 rounded transition-colors hover:bg-white/10">Login</Link>
                <Link to='/ask_ai' className="text-base px-4 py-2 rounded transition-colors hover:bg-white/10">🫧 Ask AI 🤖</Link>
            </div>
        </nav>
    );
}

export default NavigationBar;