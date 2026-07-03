import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { Route, Routes } from 'react-router';
import NavigationBar from './components/NavigationBar';
import AI from './pages/AI';
import AuthForm from './pages/AuthForm';
import Settings from './pages/Settings';
import { MovieProvider } from './contexts/MovieContext';

function App() {

  return (
    <MovieProvider >
      <div className="flex flex-col min-h-screen bg-black">
        <NavigationBar />
        <main className='flex-1 w-full'>
          <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/favorites' element={<Favorites />} />
            <Route path='/ask_ai' element={<AI />} />
            <Route path='/auth_form' element={ <AuthForm /> } />
            <Route path='/settings' element={ <Settings /> } />
          </Routes>
        </main>
      </div>
    </MovieProvider>
  );
}

export default App;
