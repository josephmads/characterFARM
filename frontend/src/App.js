import React from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages';
import AllBasic from './pages/AllBasic';
import SearchBasic from './pages/SearchBasic';


function App() {
	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path='/' element={<Home />} />
				<Route path='/all-basic' element={<AllBasic />} />
				<Route path='/search-basic' element={<SearchBasic />} />
			</Routes>
		</Router>
	);
}

export default App;
