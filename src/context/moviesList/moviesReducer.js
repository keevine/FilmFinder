import {
  GET_MOVIES,
  SET_LOADING,
  MOVIES_ERROR,
  SEARCH_MOVIES,
  SEARCH_MOVIES_DIRECTOR,
  SEARCH_MOVIES_GENRE,
} from "../types";

export default (state, action) => {
  switch (action.type) {
    case GET_MOVIES:
      console.log(action.payload);
      return {
        ...state,
        movies: action.payload,
        loading: !state.loading,
      };
    case SEARCH_MOVIES:
      return {
        ...state,
        movies: action.payload,
        loading: !state.loading,
      };
    case SEARCH_MOVIES_GENRE:
      return {
        ...state,
        movies: action.payload,
        loading: !state.loading,
      };
    case SEARCH_MOVIES_DIRECTOR:
      return {
        ...state,
        movies: action.payload,
        loading: !state.loading,
      };
    case SET_LOADING:
      console.log(state.loading);
      return {
        ...state,
        loading: !state.loading,
      };
    case MOVIES_ERROR:
      console.log(action.payload);
    default:
      return state;
  }
};
