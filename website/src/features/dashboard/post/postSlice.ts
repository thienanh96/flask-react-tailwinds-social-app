import { PayloadAction, createSlice } from "@reduxjs/toolkit"
import {
  ELikeType,
  ILike,
  IPost,
  createLike,
  createPost,
  deleteLike,
  getPosts,
} from "./postActions"
import { RootState } from "../../../app/store"

interface IPostState {
  loading: boolean
  success: boolean
  posts: IPost[]
}

const initialState: IPostState = {
  loading: false,
  success: false,
  posts: [],
}

const postSlice = createSlice({
  name: "posts",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(createPost.pending, (state) => {
        state.loading = true
      })
      .addCase(createPost.fulfilled, (state, action: PayloadAction<IPost>) => {
        state.loading = false
        state.success = true
        state.posts = [action.payload, ...state.posts]
      })
      .addCase(createPost.rejected, (state) => {
        state.loading = false
        state.success = false
      })
      .addCase(getPosts.pending, (state) => {
        state.loading = true
      })
      .addCase(getPosts.fulfilled, (state, action: PayloadAction<IPost[]>) => {
        state.posts = action.payload
      })
      .addCase(createLike.fulfilled, (state, action: PayloadAction<ILike>) => {
        const post = state.posts.find((p) => p.id === action.payload.postId)
        if (post) {
          if (action.payload.type === ELikeType.LIKE) {
            post.likeCount++
            post.likedByMe = true
          } else if (action.payload.type === ELikeType.DISLIKE) {
            post.dislikeCount++
            post.dislikedByMe = true
            post.likedByMe = false
          }
        }
      })
      .addCase(deleteLike.fulfilled, (state, action: PayloadAction<ILike>) => {
        const post = state.posts.find((p) => p.id === action.payload.postId)
        if (post) {
          if (action.payload.type === ELikeType.LIKE) {
            post.likeCount--
            post.likedByMe = false
          } else if (action.payload.type === ELikeType.DISLIKE) {
            post.dislikeCount--
            post.dislikedByMe = false
          }
        }
      })
  },
})

export const selectPost = (state: RootState) => state.post

export default postSlice.reducer
