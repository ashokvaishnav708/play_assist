// import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { Route, Routes } from 'react-router';
import NavigationBar from './components/NavigationBar';
import RequireAuth from './components/RequireAuth';
import AI from './pages/AI';
import AuthForm from './pages/AuthForm';
import Settings from './pages/Settings';
import { MovieProvider } from './contexts/MovieContext';
import { AuthProvider } from './contexts/AuthContext';

function App() {

  return (
    <AuthProvider>
      <MovieProvider >
        <div className="flex flex-col min-h-screen bg-black">
          <NavigationBar />
          <main className='flex-1 w-full'>
            <Routes>
              <Route path='/auth_form' element={ <AuthForm /> } />
              <Route path='/' element={<RequireAuth><Home/></RequireAuth>} />
              {/* <Route path='/favorites' element={<Favorites />} /> */}
              <Route path='/ask_ai' element={<RequireAuth><AI /></RequireAuth>} />
              <Route path='/settings' element={<RequireAuth><Settings /></RequireAuth>} />
            </Routes>
          </main>
        </div>
      </MovieProvider>
    </AuthProvider>
  );
}

export default App;
