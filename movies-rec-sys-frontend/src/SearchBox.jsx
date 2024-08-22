// search box component

import axios from "axios";
import { useState, useEffect } from "react";


// import PropTypes from 'prop-types';

const SearchBox = () => {
    const [movies, setMovies] = useState([]);
    const [allMovies, setAllMovies] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    const [results, setResults] = useState([]);

    const getRecommendations = async (movie) => {
        setSearchTerm(movie.title);
        try {
            const response = await axios.get(`http://localhost:8000/recommendations/${movie.title}/${movie.imdbId}`);
            // console.log(response.data);
            console.log(response.data.recommendations);
            setResults(response.data.recommendations);
        } catch (error) {
            console.log(error); 
        }
    }
    
    const searchChange = (event) => {
        setResults([]);
        setSearchTerm(event.target.value);
        const filteredMovies = allMovies.filter((movie) => {
            if(searchTerm.length >= 3) {
                return movie.title.toLowerCase().includes(searchTerm.toLowerCase());
            }
        });

        // console.log(filteredMovies);
        setMovies(filteredMovies);
        // console.log(filteredMovies);

    }

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const response = await axios.get('http://localhost:8000/movies');
                setAllMovies(response.data.movies);
            } catch (error) {
                console.log(error);
            }
        };

        fetchMovies();
    }, []);

    return (
        <div className=''>
            <input
                className='py-2 px-3 my-5 border border-gray-300 rounded-lg'
                type='search'
                placeholder='Enter Movie Title'
                onChange={searchChange}
            />

            <div className='container mx-auto my-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {movies.map((movie) => (
                    <div key={movie.imdbId} className=' border border-gray-300 rounded-lg p-2' onClick={()=>{getRecommendations(movie)}} style={{cursor: 'pointer'}}>
                        <h1 className='text-xl font-bold'>{movie.title}</h1>
                    </div>
                ))}   
            </div>

            <div className=""></div>
                {results.length > 0 && (
                    <div className="container  my-11">
                        <h2 className='text-2xl font-bold'>Results for {searchTerm}:</h2>
                        {results.length > 0 && results.map((result) => ( 
                            <div key={result} className='border border-gray-300 rounded-lg p-4' >
                                <h1 className='text-xl font-bold'>{result}</h1>
                            </div>
                        ))}
                    </div>
                )}
            </div>
    );
};

// SearchBox.propTypes = {
//   setMovies: PropTypes.func.isRequired
// };

export default SearchBox;