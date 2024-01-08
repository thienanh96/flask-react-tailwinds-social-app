import React, { useEffect, useState } from "react"
import parse from "html-react-parser"
import DOMPurify from "isomorphic-dompurify"
import dayjs from "dayjs"
import {
  ELikeType,
  IPost,
  createComment,
  createLike,
  deleteLike,
  getComments,
} from "./postActions"
import { useAppDispatch, useAppSelector } from "../../../app/hooks"
import Avatar from "react-avatar"
import { selectAuth } from "../../auth/authSlice"
import { Button } from "primereact/button"
import { InputTextarea } from "primereact/inputtextarea"

interface CardPostProps {
  post: IPost
}

const comments = [
  {
    content: "Content 1",
    username: "User 1",
  },
  {
    content: "Content 2",
    username: "User 2",
  },
  {
    content: "Content 3",
    username: "User 3",
  },
  {
    content: "Content 4",
    username: "User 4",
  },
]

export default function CardPost({ post }: CardPostProps) {
  const dispatch = useAppDispatch()

  return (
    <div className="w-full bg-white mt-3 p-5">
      <div className="flex justify-between">
        <p className="text-blue-600 font-semibold">{post.authorName}</p>
      </div>
      <div className="flex justify-between">
        <div className="mt-7 text-left w-11/12">
          {" "}
          <h1 className="mb-10 text-2xl font-semibold">{post.title}</h1>
          <div className="max-h-96 overflow-auto">
            {parse(DOMPurify.sanitize(post.content))}
          </div>
        </div>
        <div className="ml-5">
          <div className="mb-5">
            {" "}
            <i
              className={`pi pi-arrow-up cursor-pointer ${
                post.likedByMe ? "text-orange-600" : ""
              }`}
              style={{ fontWeight: 800 }}
              onClick={() => {
                if (post.likedByMe) {
                  dispatch(
                    deleteLike({
                      postId: post.id,
                      type: ELikeType.LIKE,
                    }),
                  )
                } else {
                  dispatch(
                    createLike({
                      postId: post.id,
                      type: ELikeType.LIKE,
                    }),
                  )
                }
              }}
            ></i>
          </div>
          <div className="mb-5 font-semibold">
            {post.likeCount - post.dislikeCount}
          </div>
          <div>
            <i
              className={`pi pi-arrow-down cursor-pointer ${
                post.dislikedByMe ? "text-blue-600" : ""
              }`}
              style={{ fontWeight: 800 }}
              onClick={() => {
                if (post.dislikedByMe) {
                  dispatch(
                    deleteLike({
                      postId: post.id,
                      type: ELikeType.DISLIKE,
                    }),
                  )
                } else {
                  dispatch(
                    createLike({
                      postId: post.id,
                      type: ELikeType.DISLIKE,
                    }),
                  )
                }
              }}
            ></i>
          </div>
        </div>
      </div>
      <div className="flex justify-flex-start mt-8 text-zinc-400">
        <div>{dayjs(post.createdAt).format("MMM DD, YYYY hh:mm a")}</div>
      </div>
      <InputComment postId={post.id} />
    </div>
  )
}

interface InputCommentProps {
  postId: string
  parentComment?: {
    parentId: string
    content: string
    username: string
  }
}

const InputComment = ({ postId, parentComment }: InputCommentProps) => {
  const auth = useAppSelector(selectAuth)
  const dispatch = useAppDispatch()

  const [showInput, setShowInput] = useState(false)

  const [currentComment, setCurrentComment] = useState<string>("")

  useEffect(() => {
    if (showInput) {
      dispatch(
        getComments({
          postId,
          parentId: parentComment?.parentId,
        }),
      )
    }
  }, [showInput])

  return (
    <div>
      {parentComment && (
        <>
          <div className="flex justify-flex-start mt-5 gap-3">
            <Avatar
              size={"45px"}
              textSizeRatio={2}
              round
              name={parentComment.username}
            />
            <div className="mt-3">{parentComment.content}</div>
          </div>
        </>
      )}
      <div
        className={`flex justify-flex-start mt-5 gap-3 ${
          parentComment ? "ml-16" : ""
        }`}
      >
        {showInput ? (
          <>
            <div>
              <Avatar
                size={"45px"}
                textSizeRatio={2}
                round
                name={auth?.userInfo?.username}
              />
              <InputTextarea
                value={currentComment}
                onChange={(e) => setCurrentComment(e.target.value)}
                autoResize
                rows={1}
                className="w-full"
              />
              <Button
                disabled={!currentComment}
                onClick={() => {
                  dispatch(
                    createComment({
                      postId,
                      parentId: parentComment?.parentId,
                      content: currentComment,
                    }),
                  )
                }}
                className="h-9"
              >
                Reply
              </Button>
            </div>
          </>
        ) : (
          <>
            <div
              className="cursor-pointer"
              onClick={() => setShowInput(!showInput)}
            >
              <i className="pi pi-comment mr-2 mt-2"></i>
              <span>See replies</span>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
