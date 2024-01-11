import { PayloadAction, createSlice } from "@reduxjs/toolkit"
import {
  ELikeType,
  IComment,
  ILike,
  IPost,
  createLike,
  createPost,
  deleteLike,
  getComments,
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
      .addCase(
        getComments.fulfilled,
        (
          state,
          action: PayloadAction<{
            comments: Array<IComment>
            paths: Array<string>
          }>,
        ) => {
          const parentId = action.payload.comments[0]?.parentId
          const paths = action.payload.paths

          for (const comment of action.payload.comments) {
            const post = state.posts.find((p) => p.id === comment.postId)
            if (post) {
              if (!parentId) {
                post.comments = action.payload.comments
              } else {
                const targetedComment = getPostRecursiveComments(post, paths)
                if (targetedComment) {
                  targetedComment.comments = action.payload.comments
                }
              }
            }
          }
        },
      )
  },
})

export const selectPost = (state: RootState) => state.post

const getPostRecursiveComments = (
  post: IPost,
  paths: Array<string> = [],
): IComment | undefined => {
  let nextComment: IComment | undefined

  for (const path of paths) {
    nextComment = (nextComment ? nextComment.comments : post.comments)?.find(
      (c) => c.id === path,
    )
  }

  return nextComment
}

export default postSlice.reducer
