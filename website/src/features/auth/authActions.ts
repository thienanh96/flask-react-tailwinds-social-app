import axios from "axios"
import { createAsyncThunk } from "@reduxjs/toolkit"

const backendURL = "http://localhost:5000"

export interface IAuthUser {
  id: string
  username: string
  token: string
}

export const registerUser = createAsyncThunk<
  any,
  { username: string; password: string }
>("auth/register", async ({ username, password }, { rejectWithValue }) => {
  try {
    const { data } = await axios.post<IAuthUser>(
      `${backendURL}/users/register`,
      { username, password },
      {
        headers: {
          "Content-Type": "application/json",
        },
      },
    )
    return data
  } catch (error: any) {
    // return custom error message from backend if present
    if (error.response && error.response.data.message) {
      return rejectWithValue(error.response.data.message)
    } else {
      return rejectWithValue(error.message)
    }
  }
})

export const loginUser = createAsyncThunk<
  any,
  { username: string; password: string }
>("auth/login", async ({ username, password }, { rejectWithValue }) => {
  try {
    const { data } = await axios.post<IAuthUser>(
      `${backendURL}/users/login`,
      { username, password },
      {
        headers: {
          "Content-Type": "application/json",
        },
      },
    )

    return data
  } catch (error: any) {
    // return custom error message from backend if present
    if (error.response && error.response.data.message) {
      return rejectWithValue(error.response.data.message)
    } else {
      return rejectWithValue(error.message)
    }
  }
})

export const getCurrentUser = createAsyncThunk(
  "auth/current",
  async (data, { rejectWithValue }) => {
    try {
      const { data } = await axios.get<IAuthUser>(
        `${backendURL}/users/current`,
        {
          headers: {
            "Content-Type": "application/json",
            Token: localStorage.getItem("token"),
          },
        },
      )

      return data
    } catch (error: any) {
      if (error.response && error.response.data.message) {
        return rejectWithValue(error.response.data.message)
      } else {
        return rejectWithValue(error.message)
      }
    }
  },
)
