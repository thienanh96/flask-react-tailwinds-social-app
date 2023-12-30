import { Field, Form, Formik } from "formik"
import React from "react"
import { useAppDispatch } from "../../app/hooks"
import { registerUser } from "../../features/auth/authActions"

interface RegisterFormProps {
  switchToLoginForm: () => void
}

export default function RegisterForm({ switchToLoginForm }: RegisterFormProps) {
  const dispatch = useAppDispatch()

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <img
          className="mx-auto h-10 w-auto"
          src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
        />
        <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          Register new account
        </h2>
      </div>

      <Formik
        initialValues={{
          username: "",
          password: "",
          comfirmPassword: "",
        }}
        onSubmit={(values, actions) => {
          const { username, password } = values
          dispatch(
            registerUser({
              username,
              password,
            }),
          )
          actions.setSubmitting(false)
        }}
      >
        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <Form className="space-y-6">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium leading-6 text-gray-900"
              >
                Username
              </label>
              <div className="mt-2">
                <Field
                  name="username"
                  type="text"
                  required
                  className="block w-full pl-2 pr-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Password
                </label>
              </div>
              <div className="mt-2">
                <Field
                  name="password"
                  type="password"
                  required
                  className="block w-full pl-2 pr-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Confirm Password
                </label>
              </div>
              <div className="mt-2">
                <Field
                  name="confirm-password"
                  type="password"
                  required
                  className="block w-full pl-2 pr-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Register
              </button>
            </div>
          </Form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Already has an account?{" "}
            <span
              className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500 cursor-pointer"
              onClick={() => switchToLoginForm()}
            >
              Login
            </span>
          </p>
        </div>
      </Formik>
    </div>
  )
}
