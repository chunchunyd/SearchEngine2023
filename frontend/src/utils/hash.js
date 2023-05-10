import {
  Base64
} from 'js-base64'

export function myhash(mystring) {
  const str = Base64.encode(mystring)
  return str
}
