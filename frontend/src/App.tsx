import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { Route, Routes } from 'react-router';
import NavigationBar from './components/NavigationBar';
import AI from './pages/AI';
import './css/App.css';
import { MovieProvider } from './contexts/MovieContext';

function App() {

  return (
    <div>
      <NavigationBar />
      <main className='main-content'>
        <Routes>
          <Route path='/' element={<Home/>} />
          <Route path='/favorites' element={<Favorites />} />
          <Route path='/ask_ai' element={<AI />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
