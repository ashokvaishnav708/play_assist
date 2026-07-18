import { useState } from 'react';
import { fetchLatestMovies } from '../services/api';

function Settings() {

    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    
    async function handleClick(e: Event) {
            e.preventDefault();
            if (loading) return;
            setLoading(true);
    
            try {
                await fetchLatestMovies();
                setError(null);
            }catch(err) {
                console.log(err);
            } finally {
                setLoading(false);
            }
        }
    
    return (
        <div className='w-full min-h-[calc(100vh-80px)] bg-linear-to-b from-gray-900 via-gray-800 to-black'>
            <div className='max-w-7xl mx-auto px-4 py-8'>
                {/* Hero Section */}
                <div className='mb-12'>
                    <h1 className='text-5xl md:text-6xl font-bold text-white mb-4'>
                        Settings
                    </h1>
                    <p className='text-gray-400 text-lg mb-8'>Load or unload movie content here.</p>
                    
                    <form onSubmit={ handleClick } className='flex gap-3 max-w-xl'>
                        
                        <button type='submit' className='px-8 py-4 bg-linear-to-r from-red-600 to-red-500 text-white rounded-lg font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-red-500/50 whitespace-nowrap' >
                            {loading ? 'Loading movies...' : 'Load latest movies'}
                        </button>
                    </form>
                </div>

                {error && (
                    <div className='bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-8 text-red-300'>
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Settings;