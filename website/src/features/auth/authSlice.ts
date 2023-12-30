import { PayloadAction, createSlice } from "@reduxjs/toolkit"
import {
  IAuthUser,
  getCurrentUser,
  loginUser,
  registerUser,
} from "./authActions"
import { RootState } from "../../app/store"

export interface IAuthState {
  loading: boolean
  userInfo: IAuthUser | null
  error: string | null
  success: boolean
}

const initialState: IAuthState = {
  loading: false,
  userInfo: null,
  error: null,
  success: false,
}

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logoutUser: (state) => {
      state.userInfo = null
      state.success = false
      localStorage.removeItem("token")
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(registerUser.pending, (state) => {
        state.loading = true
      })
      .addCase(
        registerUser.fulfilled,
        (state, action: PayloadAction<IAuthUser>) => {
          state.loading = false
          state.success = true
          state.userInfo = action.payload

          localStorage.setItem("token", action.payload.token)
        },
      )
      .addCase(registerUser.rejected, (state) => {
        state.loading = false
        state.success = false
      })
      .addCase(loginUser.pending, (state) => {
        state.loading = true
      })
      .addCase(
        loginUser.fulfilled,
        (state, action: PayloadAction<IAuthUser>) => {
          state.loading = false
          state.success = true
          state.userInfo = action.payload

          localStorage.setItem("token", action.payload.token)
        },
      )
      .addCase(loginUser.rejected, (state) => {
        state.loading = false
        state.success = false
      })
      .addCase(getCurrentUser.pending, (state) => {
        state.loading = true
      })
      .addCase(
        getCurrentUser.fulfilled,
        (state, action: PayloadAction<IAuthUser>) => {
          state.loading = false
          state.success = true
          state.userInfo = action.payload
        },
      )
  },
})

export const logoutUser = authSlice.actions.logoutUser

export const selectAuth = (state: RootState) => state.auth

export default authSlice.reducer
