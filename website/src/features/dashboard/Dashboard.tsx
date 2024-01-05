import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { Editor } from "primereact/editor"
import React, { useEffect, useRef, useState } from "react"
import { ELikeType, createLike, createPost, getPosts } from "./post/postActions"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { selectAuth } from "../auth/authSlice"
import { Message } from "primereact/message"
import { InputText } from "primereact/inputtext"
import { Form, Formik, FormikProps } from "formik"
import { selectPost } from "./post/postSlice"
import parse from "html-react-parser"
import DOMPurify from "isomorphic-dompurify"
import dayjs from "dayjs"

interface DashboardProps {}

export default function Dashboard(props: DashboardProps) {
  const [openDialog, setOpenDialog] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [orderBy, setOrderBy] = useState<"top" | "new">("new")

  const formRef = useRef<FormikProps<{
    title: string
    content: string
  }> | null>(null)

  const authData = useAppSelector(selectAuth)
  const postData = useAppSelector(selectPost)

  const dispatch = useAppDispatch()

  useEffect(() => {
    dispatch(getPosts())
  }, [])

  return (
    <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 mt-10">
      <div className="w-full flex justify-between bg-white p-5">
        <div>
          <Button text={orderBy !== "new"} label="New" />
          <span className="ml-3">
            <Button text={orderBy !== "top"} label="Top" />
          </span>
        </div>
        <Button
          label="Create new subreddit"
          className="h-12 p-3"
          onClick={() => setOpenDialog(true)}
        />
        <Dialog
          visible={openDialog}
          modal={true}
          header="Create post"
          style={{ width: "50vw" }}
          onHide={() => setOpenDialog(false)}
          footer={
            <div className="mt-5">
              <Button
                label="Cancel"
                icon="pi pi-times"
                onClick={() => setOpenDialog(false)}
              />
              <Button
                label="Save"
                type="button"
                icon="pi pi-check"
                severity="danger"
                autoFocus
                onClick={() => {
                  if (formRef?.current) {
                    formRef.current.submitForm()
                  }
                }}
              />
            </div>
          }
        >
          <Formik
            innerRef={formRef}
            initialValues={{
              title: "",
              content: "",
            }}
            onSubmit={async (values, actions) => {
              if (!values.content || !values.title || !authData?.userInfo?.id)
                return

              const createPostResponse = await dispatch(
                createPost({
                  content: values.content,
                  title: values.title,
                  createdBy: authData.userInfo.id,
                }),
              )

              if (createPostResponse.meta.requestStatus === "rejected") {
                setErrorMessage(createPostResponse.payload)
              } else {
                setOpenDialog(false)
              }

              actions.setSubmitting(false)
            }}
          >
            {(props) => {
              return (
                <Form>
                  <InputText
                    placeholder="Title"
                    className="w-full"
                    value={props.values.title}
                    onChange={(e) =>
                      props.setFieldValue("title", e.target.value)
                    }
                  />
                  <Editor
                    value={props.values.content ?? undefined}
                    onTextChange={(e) =>
                      props.setFieldValue("content", e.htmlValue)
                    }
                    className="mt-3 h-80"
                  />
                  {errorMessage && (
                    <div className="mt-14">
                      <Message severity="error" text={errorMessage} />
                    </div>
                  )}
                </Form>
              )
            }}
          </Formik>
        </Dialog>
      </div>
      {postData.posts.map((post) => {
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
                      dispatch(
                        createLike({
                          postId: post.id,
                          type: ELikeType.LIKE,
                        }),
                      )
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
                      dispatch(
                        createLike({
                          postId: post.id,
                          type: ELikeType.DISLIKE,
                        }),
                      )
                    }}
                  ></i>
                </div>
              </div>
            </div>
            <div className="flex justify-flex-start mt-8 text-zinc-400">
              <div>{dayjs(post.createdAt).format("MMM DD, YYYY hh:mm a")}</div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
