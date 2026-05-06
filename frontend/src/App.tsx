import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { Route, Routes } from 'react-router';
import NavigationBar from './components/NavigationBar';
import './css/App.css';
import { MovieProvider } from './contexts/MovieContext';

function App() {

  return (
    <MovieProvider>
      <NavigationBar />
      <main className='main-content'>
        <Routes>
          <Route path='/' element={<Home/>} />
          <Route path='/favorites' element={<Favorites />} />
        </Routes>
      </main>
    </MovieProvider>
  );
}

export default App;
