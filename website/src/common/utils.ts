import { transform, snakeCase, isArray, isObject } from "lodash"

export const toSnakeCase = (obj: Record<string, any>) =>
  transform(obj, (acc: Record<string, any>, value, key, target) => {
    const camelKey = isArray(target) ? key : snakeCase(key)

    acc[camelKey] = isObject(value) ? toSnakeCase(value) : value
  })
