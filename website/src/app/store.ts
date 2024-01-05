import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit"
import counterReducer from "../features/counter/counterSlice"
import authReducer from "../features/auth/authSlice"
import postReducer from "../features/dashboard/post/postSlice"

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    auth: authReducer,
    post: postReducer,
  },
})

export type AppDispatch = typeof store.dispatch
export type RootState = ReturnType<typeof store.getState>
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>
