import axios from "axios"
import { createAsyncThunk } from "@reduxjs/toolkit"
import { toSnakeCase } from "../../../common/utils"

const apiUrl = "http://localhost:5000"

export interface IPost {
  id: string
  authorName: string
  likeCount: number
  dislikeCount: number
  content: string
  title: string
  createdAt: Date
  likedByMe?: boolean
  dislikedByMe?: boolean
}

export enum ELikeType {
  LIKE = 1,
  DISLIKE = 2,
}

export interface ILike {
  postId: string
  type: ELikeType
}

export interface IPaginatedPostResponses {}

export const createPost = createAsyncThunk<
  any,
  { createdBy: string; content: string; title: string }
>("post/create", async ({ createdBy, content, title }, { rejectWithValue }) => {
  try {
    const { data } = await axios.post<IPost>(
      `${apiUrl}/posts`,
      toSnakeCase({ createdBy, content, title }),
      {
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
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
})

export const getPosts = createAsyncThunk<any, void>(
  "post/get",
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await axios.get<IPost>(`${apiUrl}/posts`, {
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
      })
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

export const createLike = createAsyncThunk<any, ILike>(
  "like/create",
  async (data, { rejectWithValue }) => {
    try {
      await axios.post(`${apiUrl}/posts/likes`, toSnakeCase(data), {
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
      })

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
