import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { Route, Routes } from 'react-router';
import NavigationBar from './components/NavigationBar';
import AI from './pages/AI';
import AuthForm from './pages/AuthForm';
import { MovieProvider } from './contexts/MovieContext';

function App() {

  return (
    <MovieProvider >
      <NavigationBar />
      <main className='flex-1 p-8 w-full flex flex-col'>
        <Routes>
          <Route path='/' element={<Home/>} />
          <Route path='/favorites' element={<Favorites />} />
          <Route path='/ask_ai' element={<AI />} />
          <Route path='/auth_form' element={ <AuthForm /> } />
        </Routes>
      </main>
    </MovieProvider>
  );
}

export default App;
